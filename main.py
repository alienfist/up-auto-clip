# -*- coding: UTF-8 -*-
# main.py

import os
import json
import time
import shutil
import subprocess
import concurrent.futures
from turtle import st
from typing import List
from pydantic import BaseModel

from utils.tts_tool import generate_tts
from utils.video_tool import split_video_by_scenes, is_valid_video, cut_video_by_time, merge_video_audio, concat_video
from utils.common import get_md5
from utils.gpt_tool import get_gpt_response
from analysisi_video import analyze_video_multi_frames
from config import TEMP_DIR, DEFAULT_LANGUAGE
from sys_prompts import DEFAULT_PROMPT, MULTI_PERSPECTIVE_PROMPTS
from logger import logger


class AutoClip(BaseModel):
    video_path: str
    video_name: str = ""
    temp_dir: str = ""
    re_preprocess: bool = False
    re_generate_scripts: bool = False
    video_segment_info_json_path: str = ""
    video_script_json_path: str = ""

    def __init__(self, video_path, **data):
        super().__init__(video_path=video_path, **data)
        self.video_name = get_md5(video_path)
        self.temp_dir = f"{TEMP_DIR}{self.video_name}/"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        self.video_segment_info_json_path = f"{self.temp_dir}video_segment_info.json"
        self.video_script_json_path = f"{self.temp_dir}video_script.json"

    def preprocess_video_segment(self):
        """preprocess video
        split video by scene and get video clip info
        """
        if os.path.exists(self.video_segment_info_json_path):
            if self.re_preprocess:
                os.remove(self.video_segment_info_json_path)
            else:
                with open(self.video_segment_info_json_path, 'r', encoding='utf-8') as f:
                    video_segment_info_list = json.loads(f.read())
                if video_segment_info_list:
                    return True
        
        res_split = split_video_by_scenes(self.video_path, self.temp_dir)
        if not res_split:
            return None
        with open(res_split, 'r', encoding='utf-8') as f:
            video_timeline_json = json.loads(f.read())

        video_segment_info_list = []
        for video_scene in video_timeline_json:
            video_scene_path = f"{self.temp_dir}{video_scene['video_name']}"
            if not is_valid_video(video_scene_path):
                logger.error(f"video {video_scene_path} is invalid, skip")
                continue
            video_scene_info = analyze_video_multi_frames(video_scene_path)
            if not video_scene_info:
                logger.error(f"video {video_scene_path} analyze failed, skip")
                continue
            video_scene_info.update(video_scene)
            video_segment_info_list.append(video_scene_info)

        with open(self.video_segment_info_json_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(video_segment_info_list, ensure_ascii=False, indent=2))
        return True
            
    def generate_video_scripts(self, perspective=None):
        if not os.path.exists(self.video_segment_info_json_path):
            logger.error(f"video segment info json file {self.video_segment_info_json_path} not exist, skip")
            return None

        # 如果指定了视角，使用带视角的文件名
        script_file_path = self.video_script_json_path
        if perspective:
            script_file_path = self.video_script_json_path.replace('.json', f'_{perspective}.json')

        if os.path.exists(script_file_path):
            if self.re_generate_scripts:
                os.remove(script_file_path)
            else:
                with open(script_file_path, 'r', encoding='utf-8') as f:
                    video_script = json.loads(f.read())
                if video_script:
                    return video_script
            
        with open(self.video_segment_info_json_path, 'r', encoding='utf-8') as f:
            video_segment_info_list = json.loads(f.read())
        
        role_desc = DEFAULT_PROMPT['screenwriter_role_desc'][DEFAULT_LANGUAGE]
        
        # 根据视角选择不同的提示词
        if perspective:
            prompt = self._get_perspective_prompt(video_segment_info_list, perspective)
        else:
            prompt = DEFAULT_PROMPT['video_script'][DEFAULT_LANGUAGE].format(video_segment_info_list=json.dumps(video_segment_info_list, ensure_ascii=False, indent=2))
        
        # response class
        class VideoClip(BaseModel):
            start: float
            end: float
            screen_text: str
            narration: str

        class VideoClipArray(BaseModel):
            video_clips: List[VideoClip]

        script = get_gpt_response(prompt, response_format=VideoClipArray.model_json_schema(), role_desc=role_desc)
        if script:
            with open(script_file_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(script['video_clips'], ensure_ascii=False, indent=2))
            return script['video_clips']
        return None
        
    def generate_segment_video_by_script(self, video_script, index, output_folder):
        """generate segment video by video script
        Args:
            video_script (dict): video script
            output_folder (str): output folder
        Returns:
            dict: video script with final video path
        """
        try:
            start = video_script['start']
            end = video_script['end']
            screen_text = video_script['screen_text']
            narration = video_script['narration']
            
            # 生成文件名
            segment_name = f"segment_{index:02d}_{start}_{end}"
            audio_filename = f"{segment_name}.wav"
            video_segment_filename = f"{segment_name}_cut.mp4"
            final_video_filename = f"{segment_name}_final.mp4"
            
            audio_path = os.path.join(output_folder, audio_filename)
            video_segment_path = os.path.join(output_folder, video_segment_filename)
            final_video_path = os.path.join(output_folder, final_video_filename)
            
            # step 1: generate tts
            logger.info(f"Step 1: Generating TTS for segment {start}-{end}")
            tts_result = generate_tts(narration, output=audio_path)
            
            if not tts_result:
                logger.error(f"Failed to generate TTS for segment {start}-{end}")
                return video_script
            
            # step 2: cut video
            logger.info(f"Step 2: Cutting video segment {start}-{end}")
            cut_result = cut_video_by_time(self.video_path, start, end, video_segment_path)
            
            if not cut_result:
                logger.error(f"Failed to cut video segment {start}-{end}")
                return video_script
            
            # step 3: merge audio and video
            logger.info(f"Step 3: Merging audio and video for segment {start}-{end}")
            merge_result = merge_video_audio(video_segment_path, audio_path, final_video_path)
            
            if merge_result:
                video_script['audio_path'] = audio_path
                video_script['srt_path'] = audio_path.replace('.wav', '.srt')
                video_script['video_segment_path'] = video_segment_path
                video_script['final_video_path'] = final_video_path
                logger.info(f"Complete video segment generated successfully: {final_video_path}")
            else:
                logger.error(f"Failed to merge audio and video for segment {start}-{end}")
                
            return video_script
        except Exception as e:
            logger.error(f"Error processing video segment {video_script.get('start', 'unknown')}: {e}")
            return video_script

    def generate_segment_video(self, perspective=None):
        """
        generate segment video by video script 
        with concurrent processing: TTS + video cutting + merging
        """
        # 根据视角选择对应的脚本文件
        script_file_path = self.video_script_json_path
        if perspective:
            script_file_path = self.video_script_json_path.replace('.json', f'_{perspective}.json')
            
        if not os.path.exists(script_file_path):
            logger.error(f"video script file {script_file_path} not exist, skip")
            return None
        
        with open(script_file_path, 'r', encoding='utf-8') as f:
            video_scripts = json.load(f)
        
        # 为不同视角创建不同的输出文件夹
        output_folder = f"{self.temp_dir}video_segment/"
        if perspective:
            output_folder = f"{self.temp_dir}video_segment_{perspective}/"
            
        if os.path.isdir(output_folder):
            shutil.rmtree(output_folder, ignore_errors=True)
        os.makedirs(output_folder, exist_ok=True)
        
        logger.info(f"Starting concurrent processing for {len(video_scripts)} segments with perspective: {perspective or 'default'}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            future_to_script = {
                executor.submit(self.generate_segment_video_by_script, video_script, index, output_folder): video_script
                for index, video_script in enumerate(video_scripts, start=1)
            }
            
            processed_scripts = []
            for future in concurrent.futures.as_completed(future_to_script):
                original_script = future_to_script[future]
                try:
                    result = future.result()
                    processed_scripts.append(result)
                    logger.info(f"Successfully processed segment {original_script.get('start', 'unknown')}-{original_script.get('end', 'unknown')}")
                except Exception as e:
                    logger.error(f"Task failed with exception: {e}")
                    processed_scripts.append(original_script)
        
        logger.info(f"Completed processing for all {len(processed_scripts)} segments")
        return processed_scripts
    
    def _get_perspective_prompt(self, video_segment_info_list, perspective):
        """根据不同视角生成对应的提示词"""
        if perspective in MULTI_PERSPECTIVE_PROMPTS:
            return MULTI_PERSPECTIVE_PROMPTS[perspective][DEFAULT_LANGUAGE].format(
                video_segment_info_list=json.dumps(video_segment_info_list, ensure_ascii=False, indent=2)
            )
        else:
            # 默认使用原有的提示词
            return DEFAULT_PROMPT['video_script'][DEFAULT_LANGUAGE].format(
                video_segment_info_list=json.dumps(video_segment_info_list, ensure_ascii=False, indent=2)
            )
    
    def generate_multiple_perspective_videos(self, perspectives=None):
        """生成多个不同视角的视频"""
        if perspectives is None:
            perspectives = ['default', 'emotional', 'educational', 'entertaining', 'inspirational', 'aesthetic', 'trending', 'lifestyle', 'professional', 'storytelling']
        
        results = []
        
        for perspective in perspectives:
            logger.info(f"Processing perspective: {perspective}")
            
            # 1. 生成该视角的脚本
            video_scripts = self.generate_video_scripts(perspective=perspective)
            if not video_scripts:
                logger.error(f"Failed to generate scripts for perspective: {perspective}")
                continue
            
            # 2. 生成该视角的视频片段
            processed_scripts = self.generate_segment_video(perspective=perspective)
            if not processed_scripts:
                logger.error(f"Failed to generate segments for perspective: {perspective}")
                continue
            
            # 3. 合并该视角的视频
            segments_video_list = [s['final_video_path'] for s in processed_scripts if 'final_video_path' in s]
            segments_video_list.sort()
            
            if segments_video_list:
                output_video_path = f"{self.temp_dir}{time.strftime('%Y%m%d%H%M%S', time.localtime())}_{perspective}.mp4"
                res_concat_video = concat_video(segments_video_list, output_video_path)
                
                if res_concat_video:
                    results.append({
                        'perspective': perspective,
                        'video_path': output_video_path,
                        'segments_count': len(segments_video_list)
                    })
                    logger.info(f"Successfully generated {perspective} video: {output_video_path}")
                    
                    # 清理临时文件
                    shutil.rmtree(f"{self.temp_dir}video_segment_{perspective}/", ignore_errors=True)
                else:
                    logger.error(f"Failed to concat video for perspective: {perspective}")
            else:
                logger.error(f"No valid segments found for perspective: {perspective}")
        
        return results
    
    
if __name__ == "__main__":
    auto_clip = AutoClip(video_path = f"{TEMP_DIR}test.webm")
    
    # 1. preprocess video segment: get video segmemt info 
    res_preprocess_video_segment = auto_clip.preprocess_video_segment()
    print(f"视频预处理结果: {res_preprocess_video_segment}")
    
    if res_preprocess_video_segment:
        # 2. 生成多个不同视角的视频（默认生成6个视角）
        print("开始生成多视角视频...")
        
        # 可以自定义视角列表，这里使用默认的6个视角
        # perspectives = ['emotional', 'educational', 'entertaining', 'inspirational', 'aesthetic']
        # results = auto_clip.generate_multiple_perspective_videos(perspectives)
        
        results = auto_clip.generate_multiple_perspective_videos()
        
        # 3. 输出结果
        print(f"\n=== 多视角视频生成完成 ===")
        print(f"成功生成 {len(results)} 个不同视角的视频:")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. 【{result['perspective']}】视角 - {result['video_path']} (包含{result['segments_count']}个片段)")
        
        if results:
            print(f"\n所有视频已保存到: {auto_clip.temp_dir}")
        else:
            print("\n未能成功生成任何视频，请检查日志")
    else:
        print("视频预处理失败，无法继续生成视频")
