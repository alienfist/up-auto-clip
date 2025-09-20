# -*- coding: UTF-8 -*-
# main.py

import json
from typing import List
from pydantic import BaseModel

from utils.video_tool import split_video_by_scenes, is_valid_video
from utils.common import get_md5
from utils.gpt_tool import get_gpt_response
from analysisi_video import analyze_video_multi_frames
from config import TEMP_DIR, DEFAULT_LANGUAGE
from sys_prompts import DEFAULT_PROMPT
from logger import logger


def preprocess_video_segment(video_path, video_segment_info_json_path=None):
    """preprocess video
    split video by scene and get video clip info
    Args:
        video_path (str): video path
    Returns:
        str: temp video path
    """
    output_folder = f"{TEMP_DIR}{get_md5(video_path)}/"
    res_split = split_video_by_scenes(video_path, output_folder)
    if not res_split:
        return None
    with open(res_split, 'r') as f:
        video_timeline_json = json.loads(f.read())

    video_segment_info_list = []
    for video_scene in video_timeline_json:
        video_path = f"{output_folder}{video_scene['video_name']}"
        if not is_valid_video(video_path):
            logger.error(f"video {video_path} is invalid, skip")
            continue
        video_info = analyze_video_multi_frames(video_path)
        if not video_info:
            logger.error(f"video {video_path} analyze failed, skip")
            continue
        video_info.update(video_scene)
        print(video_info)
        video_segment_info_list.append(video_info)

    if not video_segment_info_json_path:
        video_segment_info_json_path = f"{output_folder}video_segment_info.json"
    with open(video_segment_info_json_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(video_segment_info_list, ensure_ascii=False, indent=2))
    return video_segment_info_json_path
        

def get_video_script(video_segment_info_json_path, video_script_json_path=None):
    with open(video_segment_info_json_path, 'r', encoding='utf-8') as f:
        video_segment_info_list = f.read()
    role_desc = DEFAULT_PROMPT['screenwriter_role_desc'][DEFAULT_LANGUAGE]
    prompt = DEFAULT_PROMPT['video_script'][DEFAULT_LANGUAGE].format(video_segment_info_list=video_segment_info_list)
    class VideoClip(BaseModel):
        start: float
        end: float
        screen_text: str
        narration: str
    class VideoClipArray(BaseModel):
        video_clips: List[VideoClip]
    script = get_gpt_response(prompt, response_format=VideoClipArray.model_json_schema(), role_desc=role_desc)
    if script:
        if not video_script_json_path:
            video_script_json_path = video_segment_info_json_path.replace('video_segment_info.json', 'video_script.json')
        with open(video_script_json_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(script['video_clips'], ensure_ascii=False, indent=2))
        return script['video_clips']
    return None
    

if __name__ == "__main__":
    video_path = f"{TEMP_DIR}test.webm"
    # preprocess video segment: get video segmemt info 
    video_segment_info_json_path = preprocess_video_segment(video_path)
    # get video script by video segment info
    video_script = get_video_script(video_segment_info_json_path)
    print(video_script)
