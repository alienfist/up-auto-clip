import os
import shutil
import time
import json
import math
import cv2
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from logger import logger
from utils.video_tool import extract_video_frames_use_thread, get_video_fps
from utils.gpt_tool import analyze_image


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


def analyze_video_frames(video_path: str, interval: int = 1, max_workers: int = 6, clear_cache: bool = False) -> List[Dict] | None:
    """Analyze video frames
    Args:
        video_path: video path
        interval: analysis interval (seconds), default 1
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
        
        # 获取视频信息
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
                    logger.error(f"处理帧 {frame_path} 的结果时出错: {str(e)}")
        
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
