# -*- coding: UTF-8 -*-
# video_tool.py

import os
import cv2
import time
import ffmpeg
import subprocess
import numpy as np
from typing import Optional
from pathlib import Path
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.video_splitter import split_video_ffmpeg
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import OUTPUT_DIR, TEMP_DIR
from logger import logger


def get_video_fps(video_path: str) -> int | None:
    """get video fps
    Args:
        video_path (str): video path
    Returns:
        int | None: fps
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return int(fps)


def get_video_duration(video_path: str, unit: str = 'seconds') -> float | None:
    """get video duration
    Args:
        video_path (str): video path
        unit (str, optional): unit. Defaults to 'seconds' or 'millisecond'.
    Returns:
        float | None: duration
    """
    try:
        if not os.path.isfile(video_path):
            print("video not exist:%s" % video_path)
            return None
        info = ffmpeg.probe(video_path).get("streams")[0]
        if unit == 'seconds':
            video_duration = float(info.get("duration"))
        else:
            video_duration = float(info.get("duration")) * 1000
        return video_duration
    except Exception as e:
        print(e)
        return None


def split_video_by_scenes(video_path: str, output_folder: str = None, threshold: int = 30, downscale_factor: int = 1, split_video: bool = True):
    """split video by scenes
    Args:
        video_path (str): video path
        output_folder (str, optional): output folder. Defaults to None.
        threshold (int, optional): threshold. Defaults to 30.
        downscale_factor (int, optional): downscale factor. Defaults to 1.
        split_video (bool, optional): split video. Defaults to True.
    Returns:
        List[tuple] | None: scene timeline list
    """
    if not os.path.exists(video_path):
        logger.error(f"video not exist: {video_path}")
        return None

    video_file = Path(video_path)
    video_name = video_file.name.replace(video_file.suffix, "")

    if video_file.suffix not in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
        logger.error("unsupported video format, please use MP4, AVI, MOV, MKV or WEBM format")
        return None

    if not output_folder:
        output_folder = f"{OUTPUT_DIR}/{video_name}_clip/"
    os.makedirs(output_folder, exist_ok=True)

    split_timeline_txt = f"{output_folder}split_timeline.txt"
    if os.path.isfile(split_timeline_txt):
        os.remove(split_timeline_txt)

    try:
        video_manager = VideoManager([video_path])
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=threshold))    # 添加内容检测器，并设置检测阈值（threshold），用于判断场景切换
        video_manager.set_downscale_factor(downscale_factor)                # 设置视频降采样因子，用于降低分辨率以加快处理速度
        video_manager.start()                                               # 启动视频管理器，开始读取视频帧
        scene_manager.detect_scenes(frame_source=video_manager)             # 利用视频管理器作为帧源，检测视频中的场景切换点
        scene_timeline_list = scene_manager.get_scene_list()                # 获取检测到的场景列表

        if not scene_timeline_list:
            logger.warning("no scene timeline found")
            return []

        if split_video:
            split_video_ffmpeg(video_path, scene_timeline_list, output_folder, show_progress=True)
            logger.info(f"video split success, scene count: {len(scene_timeline_list)}")
        else:
            logger.info(f"video analysis success, scene count: {len(scene_timeline_list)}")
        for scene_timeline in scene_timeline_list:
            with open(split_timeline_txt, "a", encoding="utf-8") as f:
                f.write(str(scene_timeline)+"\n")
        return split_timeline_txt

    except Exception as e:
        logger.error(f"video process error: {str(e)}")
        return None


def is_black_frame(frame: np.ndarray, threshold: int = 30) -> bool:
    """detect black frame
    Args:
        frame: video frame
        threshold: brightness threshold, below this value is considered a black frame
    Returns:
        bool: whether it is a black frame
    """

    if frame is None:
        return True
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # transform to gray
    mean_brightness = np.mean(gray)                 # calculate mean brightness
    return mean_brightness < threshold


def extract_video_specific_frame(video_path: str, output_folder: str,frame_number: Optional[int] = None, custom_filename: Optional[str] = None, max_check_seconds: int = 10):
    """extract video specified frame
    Args:
        video_path: video path
        output_folder: output folder path
        frame_number: if specified, extract specified frame number, else extract first non-black frame
        custom_filename: custom output filename
        max_check_seconds: maximum check seconds
    
    Returns:
        str: saved image path
    
    Raises:
        ValueError: if all frames are black or cannot be processed
    """
    if not os.path.exists(video_path):
        logger.error(f"video file not exist: {video_path}")
        return None
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error("open video failed")
            return None

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            logger.error("get video fps failed")
            return None
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        max_check_frames = int(fps * max_check_seconds)
        
        # detect specified frame
        if frame_number is not None:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            if not ret:
                logger.error(f"read frame failed: {frame_number}")
                return None
            
            if not is_black_frame(frame):
                output_filename = custom_filename or f"frame_{frame_number}.png"
                output_path = os.path.join(output_folder, output_filename)
                cv2.imwrite(output_path, frame)
                cap.release()
                logger.info(f"success extract frame {frame_number} and save as png: {output_path}")
                return output_path
        
        # detect non-black frame
        checked_frames = 0
        while checked_frames < max_check_frames and checked_frames < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, checked_frames)
            ret, frame = cap.read()
            if not ret:
                break
                
            if not is_black_frame(frame):
                current_second = checked_frames / fps
                output_filename = custom_filename or f"frame_{checked_frames}.png"
                output_path = os.path.join(output_folder, output_filename)
                cv2.imwrite(output_path, frame)
                cap.release()
                
                logger.info(f"{current_second:.1f}s find non-black frame and save as png: {output_path}")
                return output_path
                
            # detect next non-black frame by second
            checked_frames += int(fps)
        
        # all frames are black
        cap.release()
        logger.error(f"video {video_path} all frames are black, max check seconds: {max_check_seconds}")
        return None

    except Exception as e:
        logger.error(f"extract frame error: {str(e)}")
        if 'cap' in locals():
            cap.release()
        return None


def is_valid_video(video_path: str, check_seconds: int = 10) -> bool:
    """check video is valid (whether there is a non-black frame)
    Args:
        video_path: video file path
        check_seconds: check seconds
    Returns:
        bool: video is valid
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error("open video failed")
            return False

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            logger.error("get video fps failed")
            return False
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        max_check_frames = int(fps * check_seconds)
        
        checked_frames = 0
        while checked_frames < max_check_frames and checked_frames < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, checked_frames)
            ret, frame = cap.read()

            if not ret:
                break

            if not is_black_frame(frame):
                cap.release()
                return True

            checked_frames += int(fps)
            
        cap.release()
        return False
    except Exception as e:
        logger.error(f"check video validity error: {str(e)}")
        if 'cap' in locals():
            cap.release()
        return False


def _save_frame_in_thread(frame_data):
    """save frame in thread
    Args:
        frame_data: include(frame, output_path, scale_ratio)
    Returns:
        str: output path
    """
    frame, output_path, scale_ratio = frame_data
    if scale_ratio != 1.0:
        height, width = frame.shape[:2]
        new_width = int(width * scale_ratio)
        new_height = int(height * scale_ratio)
        frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
    cv2.imwrite(output_path, frame)
    return output_path


def extract_video_frames_use_thread(video_path: str, frames_folder: str, frame_index: int = 10, interval: int = 0, scale_ratio: float = 1.0, max_workers: int = 4) -> list[str] | None:
    """extract video frames use thread
    Args:
        video_path: video path
        frames_folder: frames folder path
        frame_index: frame index (default: 0)
        interval: interval (default: 0)
        scale_ratio: scale ratio (default: 1.0)
        max_workers: max workers (default: 4)
    Returns:
        list[str] | None: saved paths
    """
    try:
        if not os.path.exists(video_path):
            logger.error(f"video not exists: {video_path}")
            return None
            
        if not 0 < scale_ratio <= 1.0:
            logger.error(f"scale ratio must be in 0-1.0: {scale_ratio}")
            return None
            
        os.makedirs(frames_folder, exist_ok=True)
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error(f"open video failed: {video_path}")
            return None
            
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps <= 0:
            logger.error(f"get video fps failed: {fps}")
            return None
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        save_count = 0
        futures = []
        saved_paths = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            second_count = 0
            while True:
                # calculate current second frame index
                target_frame = second_count * fps + frame_index
                if target_frame >= total_frames:
                    break
                    
                # set video to current second frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
                ret, frame = cap.read()
                
                if not ret:
                    break
                    
                if interval == 0 or second_count % (interval + 1) == 0:
                    output_path = os.path.join(
                        frames_folder, 
                        f"sec_{second_count:04d}_frame_{target_frame:06d}.jpg"
                    )
                    future = executor.submit(
                        _save_frame_in_thread, 
                        (frame.copy(), output_path, scale_ratio)
                    )
                    futures.append(future)
                    save_count += 1
                second_count += 1
                
            for future in as_completed(futures):
                try:
                    saved_path = future.result()
                    saved_paths.append(saved_path)
                    logger.debug(f"save frame success: {saved_path}")
                except Exception as e:
                    logger.error(f"save frame failed: {str(e)}")
                    
        cap.release()
        logger.info(f"extract video all frames success, total frames: {save_count}")
        return sorted(saved_paths)
        
    except Exception as e:
        logger.error(f"extract video all frames failed: {str(e)}")
        if 'cap' in locals():
            cap.release()
        return None


def concat_video(video_path_list: list, output_video_path: str):
    """concat video
    Args:
        video_path_list (list): video path list
        output_video_path (str): output video path
    Returns:
        str: output path
    """
    try:
        temp_txt_path = f"{TEMP_DIR}{time.strftime('%Y%m%d%H%M%S')}.temp.txt"
        for video_path in video_path_list:
            with open(temp_txt_path, "a", encoding="utf-8") as f:
                f.write(f"""file '{video_path}'\n""")
        ffmpeg_exec = f"ffmpeg -f concat -safe 0 -i {temp_txt_path} -c:v libx264 -crf 18 -y {output_video_path}"
        ret = subprocess.run(ffmpeg_exec, shell=True)
        if ret.returncode == 0:
            if os.path.exists(temp_txt_path):
                os.remove(temp_txt_path)
            logger.info(f"concat video success, output path: {output_video_path}")
            return output_video_path
        else:
            logger.error(f"concat video failed, output path: {output_video_path}")
            return None
    except Exception as e:
        logger.error(str(e))
        return None
    finally:
        if os.path.exists(temp_txt_path):
            os.remove(temp_txt_path)
