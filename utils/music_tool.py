# -*- coding: UTF-8 -*-
# music_tool.py

import os
import json
import random
import requests
import subprocess
from config import MUSIC_CACHE_DIR, MUSIC_API_CONFIG
from logger import logger


class MusicAPI:
    """music api
    free music api
    """
    
    def __init__(self, api_type="jamendo"):
        """api_type: "jamendo" 或 "freesound"""
        self.api_type = api_type
        self.cache_dir = MUSIC_CACHE_DIR
        os.makedirs(self.cache_dir, exist_ok=True)
        self.config = MUSIC_API_CONFIG
    
    def search_music(self, style, duration=None, limit=10):
        """search music by music style
        :param style: music style example "upbeat", "relaxing", "cinematic" etc.
        :param duration: wish music duration
        :param limit: wish music number    
        :return: music list
        """
        if self.api_type == "jamendo":
            return self._search_jamendo(style, duration, limit)
        elif self.api_type == "freesound":
            return self._search_freesound(style, duration, limit)
        else:
            logger.error(f"no support api type: {self.api_type}")
            return []
    
    def _search_jamendo(self, style, duration=None, limit=10):
        """search music by jamendo api
        :param style: music style example "upbeat", "relaxing", "cinematic" etc.
        :param duration: wish music duration
        :param limit: wish music number    
        :return: music list
        """
        try:
            params = {
                "client_id": self.config["jamendo"]["client_id"],
                "format": self.config["jamendo"]["format"],
                "limit": limit,
                "tags": style,
                "include": "musicinfo",
                "boost": "popularity_total"
            }
            
            if duration:
                min_duration = max(30, duration - 30)   # min duration 30s
                max_duration = duration + 60            # max duration 60s
                params["durationbetween"] = f"{min_duration}_{max_duration}"
            
            url = f"{self.config['jamendo']['base_url']}{self.config['jamendo']['tracks_endpoint']}"
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                logger.error(f"jamendo api request error: {response.status_code}, {response.text}")
                return []
            
            data = response.json()
            tracks = []
            for track in data.get("results", []):
                tracks.append({
                    "id": track.get("id"),
                    "name": track.get("name"),
                    "artist": track.get("artist_name"),
                    "duration": track.get("duration"),
                    "url": track.get("audio"),
                    "license": track.get("license_ccurl"),
                    "source": "jamendo"
                })
            
            return tracks
            
        except Exception as e:
            logger.error(f"search jamendo music error: {str(e)}")
            return []
    
    def _search_freesound(self, style, duration=None, limit=10):
        """search music by freesound api
        :param style: music style example "upbeat", "relaxing", "cinematic" etc.
        :param duration: wish music duration
        :param limit: wish music number    
        :return: music list
        """
        try:
            params = {
                "token": self.config["freesound"]["api_key"],
                "query": f"{style} music",
                "page_size": limit,
                "fields": "id,name,username,duration,previews,license",
                "filter": "duration:[5 TO 300]",  # min duration 5s, max duration 5min
                "sort": "rating_desc"
            }
            
            if duration:
                min_duration = max(5, duration - 30)
                max_duration = duration + 60
                params["filter"] = f"duration:[{min_duration} TO {max_duration}]"

            url = f"{self.config['freesound']['base_url']}{self.config['freesound']['search_endpoint']}"
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                logger.error(f"freesound api request error: {response.status_code}, {response.text}")
                return []
            
            data = response.json()
            tracks = []
            for track in data.get("results", []):
                tracks.append({
                    "id": track.get("id"),
                    "name": track.get("name"),
                    "artist": track.get("username"),
                    "duration": track.get("duration"),
                    "url": track.get("previews", {}).get("preview-hq-mp3"),
                    "license": track.get("license"),
                    "source": "freesound"
                })
            
            return tracks
        except Exception as e:
            logger.error(f"search freesound music error: {str(e)}")
            return []
    
    def download_music(self, track, target_path=None):
        """download music
        :param track: music info dict (id、source、url)
        :param target_path: music file path, if None, save to cache dir
        :return: music file path
        """
        try:
            track_id = track.get("id")
            source = track.get("source")
            file_name = f"{source}_{track_id}.mp3"
            
            if target_path is None:
                target_path = os.path.join(self.cache_dir, file_name)
            
            if os.path.exists(target_path):
                logger.info(f"use cache music file: {target_path}")
                return target_path
            
            url = track.get("url")
            
            if not url:
                logger.error(f"music url is empty: {track}")
                return None
            
            logger.info(f"download music: {url} -> {target_path}")
            response = requests.get(url, stream=True)
            
            if response.status_code != 200:
                logger.error(f"download music failed: {response.status_code}, {response.text}")
                return None
            
            with open(target_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"download music success: {target_path}")
            return target_path
        except Exception as e:
            logger.error(f"download music error: {str(e)}")
            return None


def get_music_by_style(style, duration=None, api_type="jamendo"):
    """get music by style
    :param style: "upbeat", "relaxing", "cinematic", etc.
    :param duration: music duration in seconds
    :param api_type: api type "jamendo" or "freesound"
    :return: music file path, None if failed
    """
    try:
        # Initialize music API
        api = MusicAPI(api_type=api_type)
        
        # Search music
        tracks = api.search_music(style, duration=duration, limit=10)
        
        if not tracks:
            logger.warning(f"No {style} style music found, trying other API")
            if api_type == "jamendo":
                return get_music_by_style(style, duration, "freesound")
            elif api_type == "freesound":
                logger.warning(f"All available music APIs failed to find {style} style music")
                return None
            else:
                logger.warning(f"All music APIs failed to find {style} style music")
                return None
        
        # Randomly select a track
        track = random.choice(tracks)
        
        # Download music
        music_path = api.download_music(track)
        return music_path
    except Exception as e:
        logger.error(f"Error occurred while getting music: {str(e)}")
        return None


def add_video_background_music(video_path, output_path, music_style="upbeat", volume=0.3, api_type="jamendo"):
    """
    Add royalty-free background music to video
    
    Args:
        video_path: Input video file path
        output_path: Output video file path
        music_style: Music style such as "upbeat", "relaxing", "cinematic", etc.
        volume: Music volume, float between 0.0-1.0, default 0.3
        api_type: API type, options: "jamendo" or "freesound", default is jamendo
        
    Returns:
        Output path on success, None on failure
    """

    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Get video duration
        video_info_cmd = f'ffprobe -v error -show_entries format=duration -of json "{video_path}"'
        video_info = subprocess.check_output(video_info_cmd, shell=True)
        video_info = json.loads(video_info)
        video_duration = float(video_info['format']['duration'])
        
        # Get music
        music_path = get_music_by_style(music_style, duration=video_duration, api_type=api_type)
        
        if not music_path:
            logger.error(f"Unable to get {music_style} style music")
            return None
        
        # Get music duration
        music_info_cmd = f'ffprobe -v error -show_entries format=duration -of json "{music_path}"'
        music_info = subprocess.check_output(music_info_cmd, shell=True)
        music_info = json.loads(music_info)
        music_duration = float(music_info['format']['duration'])
        
        # Create temporary file path
        temp_dir = os.path.dirname(output_path)
        temp_music_path = os.path.join(temp_dir, "temp_music.mp3")
        
        # If music duration is shorter than video duration, need to loop the music
        if music_duration < video_duration:
            # Calculate how many times to repeat
            repeat_count = int(video_duration / music_duration) + 1
            
            # Create looped music file
            concat_file = os.path.join(temp_dir, "concat.txt")
            with open(concat_file, 'w', encoding='utf-8') as f:
                for _ in range(repeat_count):
                    f.write(f"file '{music_path}'\n")
            
            loop_cmd = f'ffmpeg -f concat -safe 0 -i "{concat_file}" -c copy -t {video_duration} -y "{temp_music_path}"'
            logger.info(f"Creating looped music: {loop_cmd}")
            ret1 = subprocess.run(loop_cmd, shell=True)
            
            if ret1.returncode != 0:
                logger.error("Failed to create looped music")
                return None
            
            os.remove(concat_file)
            music_path = temp_music_path
        elif music_duration > video_duration:
            # If music duration is longer than video duration, trim the music
            trim_cmd = f'ffmpeg -i "{music_path}" -t {video_duration} -y "{temp_music_path}"'
            logger.info(f"Trimming music: {trim_cmd}")
            ret1 = subprocess.run(trim_cmd, shell=True)
            
            if ret1.returncode != 0:
                logger.error("Failed to trim music")
                return None
            
            music_path = temp_music_path
        
        # Merge music with video, keep original video audio but reduce volume
        merge_cmd = f'ffmpeg -i "{video_path}" -i "{music_path}" -filter_complex "[0:a]volume=1.0[a1];[1:a]volume={volume}[a2];[a1][a2]amix=inputs=2:duration=longest[aout]" -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest -y "{output_path}"'
        logger.info(f"Merging video and music: {merge_cmd}")
        ret2 = subprocess.run(merge_cmd, shell=True)
        
        # Clean up temporary files
        try:
            if os.path.exists(temp_music_path):
                os.remove(temp_music_path)
        except Exception as e:
            logger.warning(f"Failed to clean up temporary files: {str(e)}")
        
        if ret2.returncode == 0 and os.path.exists(output_path):
            logger.info(f"Successfully added background music: {output_path}")
            return output_path
        else:
            logger.error(f"Failed to add background music, return code: {ret2.returncode}")
            return None
            
    except Exception as e:
        logger.error(f"Error occurred while adding background music: {str(e)}")
        return None
