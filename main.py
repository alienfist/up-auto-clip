# -*- coding: UTF-8 -*-
# main.py

import json
from utils.video_tool import split_video_by_scenes, is_valid_video
from utils.common import get_md5
from analysisi_video import analyze_video_multi_frames
from config import TEMP_DIR
from logger import logger


def preprocess_video(video_path):
    """preprocess video
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

    with open(f"{output_folder}video_info.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(video_segment_info_list, ensure_ascii=False, indent=2))
    return f"{output_folder}video_info.json"
        
    
if __name__ == "__main__":
    video_path = f"{TEMP_DIR}test.webm"
    preprocess_video(video_path)
