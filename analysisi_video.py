# -*- coding: UTF-8 -*-
# analysisi_video.py

import os
import shutil
import base64
import time
import json
import math
import cv2
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from logger import logger
from utils.video_tool import extract_video_frames_use_thread, get_video_fps
from utils.gpt_tool import analyze_image, analyze_multi_images


def _analyze_frame_in_thread(frame_data: tuple) -> Dict | None:
    """analyze frame in thread
    Args:
        frame_data: (frame_path, second, frame)
    Returns: Dict
    """
    frame_path, second, frame = frame_data
    try:
        result = analyze_image(image_path=frame_path)
        if not result:
            return None
        
        return {
            "file": frame_path,
            "desc": result["desc"],
            "tag": result["tag"],
            "frame": int(frame),
            "second": int(second)
        }
    except Exception as e:
        logger.error(f"analyze frame {frame_path} failed: {str(e)}")
        return None


def analyze_video_frames(video_path: str, interval: int = 0, max_workers: int = 6, clear_cache: bool = False) -> List[Dict] | None:
    """Analyze video frames
    Args:
        video_path: video path
        interval: analysis interval (seconds), default 0
        max_workers: maximum number of threads, default 6
        clear_cache: whether to clear cache, defalt False
    Returns: List[Dict]
    """
    try:
        if not os.path.exists(video_path):
            logger.error(f"video file not exists: {video_path}")
            return None
        
        video_dir = os.path.dirname(os.path.abspath(video_path)) + "/"
        frames_folder = f"{video_dir}frames/"
        if clear_cache:
            shutil.rmtree(frames_folder, ignore_errors=True)
        os.makedirs(frames_folder, exist_ok=True)
        
        # get video info
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error(f"open video file failed: {video_path}")
            return None
            
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = get_video_fps(video_path)
        duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps)     # get video duration (seconds)
        total_frames = int(duration * fps)                          # calculate total frames
        cap.release()
        
        if fps is None:
            logger.error(f"get video fps failed: {video_path}")
            return None
            
        # calculate scale ratio
        min_dimension = min(width, height)
        target_min_dimension = 300
        
        if min_dimension < target_min_dimension:
            # if original resolution is too small, keep original resolution
            scale_ratio = 1.0
            logger.warning(f"video resolution is too small ({width}x{height}), will keep original resolution")
        else:
            # 计算缩放比例，确保最小边不小于300像素
            scale_ratio = max(target_min_dimension / min_dimension, 0.5)
            # 向上取整到0.1
            scale_ratio = math.ceil(scale_ratio * 10) / 10
        logger.info(f"video resolution: {width}x{height}, using scale ratio: {scale_ratio}")
        
        # 1.extract video frames
        max_frame_workers = 6
        frame_paths = extract_video_frames_use_thread(
            video_path=video_path,
            frames_folder=frames_folder,
            interval=interval,
            scale_ratio=scale_ratio,
            max_workers=max_frame_workers
        )
        if not frame_paths:
            logger.error(f"extract video frames failed: {video_path}")
            return None
            
        # 2.analyze video frames
        frame_tasks = []
        for frame_path in frame_paths:
            frame_info = os.path.basename(frame_path).split('_')
            second = frame_info[1]
            frame = frame_info[3].split('.')[0]
            frame_tasks.append((frame_path, second, frame))
        
        # thread analyze video frames
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_frame = {
                executor.submit(_analyze_frame_in_thread, task): task 
                for task in frame_tasks
            }
            
            for future in as_completed(future_to_frame):
                frame_path = future_to_frame[future][0]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    logger.error(f"analyze frame {frame_path} failed: {str(e)}")
        
        # sort results by second and frame
        results.sort(key=lambda x: (x['second'], x['frame']))
        
        # save analysis results to json file
        analysis_result = {
            "video_path": video_path,
            "duration": duration, 
            "total_frames": total_frames,
            "analyzed_frames": len(results),
            "video_fps": fps,
            "video_resolution": f"{width}x{height}",
            "scale_ratio": scale_ratio,
            "analysis_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "frames": results
        }
        
        json_path = os.path.join(video_dir, "frames_analysis.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
                
        logger.info(f"analyze video frames completed, total frames: {total_frames}, analyzed frames: {len(results)}")
        return json_path
        
    except Exception as e:
        logger.error(f"analyze video frames failed: {str(e)}")
        return None


def analyze_video_multi_frames(video_path: str, interval: int = 0, target_width: int = 320):
    """analyze multi video frames
    Args:
        video_path (str): video path
        interval (int): interval seconds
        target_width (int): target width for resizing frames to reduce token usage, default 320
    Returns:
        dict: {"desc": "", "tag": [], "duration": 0, "fps": 0, "total_frames": 0, "analyzed_frames": 0, "frames": []}
    """
    try:
        if not os.path.exists(video_path):
            logger.error(f"video file not exists: {video_path}")
            return None
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error(f"open video file failed: {video_path}")
            return None
        
        fps = get_video_fps(video_path)
        if fps is None:
            logger.error(f"get video fps failed: {video_path}")
            cap.release()
            return None
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = int(total_frames / fps)
        
        images_data = []
        for second in range(0, duration, interval + 1 if interval > 0 else 1):
            # set frame number
            frame_number = second * fps
            if frame_number >= total_frames:
                break
                
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            
            if not ret:
                logger.warning(f"failed to read frame at second {second}, frame number: {frame_number}")
                continue
            
            # resize frame to reduce token usage
            height, width = frame.shape[:2]
            if width > target_width:
                # calculate new height maintaining aspect ratio
                new_height = int(height * target_width / width)
                frame = cv2.resize(frame, (target_width, new_height), interpolation=cv2.INTER_AREA)
                logger.debug(f"resized frame from {width}x{height} to {target_width}x{new_height}")
            
            # frame to base64 with optimized quality
            encode_params = [cv2.IMWRITE_JPEG_QUALITY, 70]  # further reduce quality to minimize size
            _, buffer = cv2.imencode('.jpg', frame, encode_params)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            images_data.append(frame_base64)
            
            if len(images_data) == 1:
                logger.info(f"single frame base64 size: {len(frame_base64) / 1024:.2f} KB")
        
        cap.release()
        logger.info(f"extracted {len(images_data)} frames from video, duration: {duration}s")
        
        res_analyze = analyze_multi_images(images_data)
        if not res_analyze:
            logger.error(f"analyze multi images failed")
            return None

        desc = res_analyze.get("desc", "")
        tag = res_analyze.get("tag", [])
        if not tag:
            tag = ["video_frames", "base64_encoded"]

        video_info = {
            "desc": desc,
            "tag": tag,
            "duration": duration,
            "fps": fps,
            "total_frames": total_frames,
            "analyzed_frames": len(images_data)
        }
        
        return video_info
    except Exception as e:
        logger.error(f"analyze video multi frames failed: {str(e)}")
        if 'cap' in locals():
            cap.release()
        return None
