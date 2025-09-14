# -*- coding: UTF-8 -*-
# config.py

import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_FOLDER = f"{os.path.dirname(os.path.abspath(__file__))}/"
OUTPUT_DIR = f"{PROJECT_FOLDER}output/"
TEMP_DIR = f"{PROJECT_FOLDER}temp/"
RESOURCE_DIR = f"{PROJECT_FOLDER}resource/"

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_VISION_MODEL = 'qwen2.5vl'
OLLAMA_CHAT_MODEL = 'deepseek-r1:8b'

# default video language
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "zh")

# default prompt
DEFAULT_PROMPT = {
    "role_desc": {
        "zh": """你是一个专业的视频编辑。""",
        "en": """You are a professional video editor."""
    },
    "one_frame": {
        "zh": """请分析这张图片,并以JSON格式返回结果,包含以下字段:
            - desc: 图片的详细描述（中文）
            - tag: 能代表图片具体特征的标签列表,
                tag必须包含镜头元素(近景、远景、中景)
                tag必须包含主体元素(人物、动物、车辆等)
                tag必须包含场景元素(城市、乡村、 自然风光等)
        请直接返回JSON格式,不要包含其他文字。
        示例格式：{
            "desc": "一个美丽的少女长发飘飘走在绿色的草地上...", 
            "tag": ["近景", "少女", "长发", "草地", "美丽", "人物", "自然风光"]
        }""",
        "en": """Please analyze this image and return the result in JSON format, containing the following fields:
            - desc: A detailed description of the image (in English)
            - tag: A list of tags that represent the specific features of the image (in English)
                tag must contain lens element (near, far, medium)
                tag must contain subject element (person, animal, vehicle, etc.)
                tag must contain scene element (city, countryside, nature, etc.)
        Please return the JSON format directly, without any additional text.
        Example format: {
            "desc": "A beautiful young girl with long hair is walking on the green grass...", 
            "tag": ["close-up", "young girl", "long hair", "grassland", "beautiful", "person", "natural scenery"]
        }"""
    },
    "multi_frame": {
        "zh": """这一组连贯的图片是一个视频的每秒连续帧，请分析这一组图片，并以JSON格式返回结果，包含以下字段：
            - desc: 通过这一组视频图片，对这个视频做出详细的描述（中文）
            - tag: 能代表这一组视频图片的具体特征的标签列表（中文）
        请直接返回JSON格式，不要包含其他文字。
        示例格式：{
            "desc": "A beautiful young girl with long hair walked on the green grass, bent down to pick up a leaf on the ground, and then jumped happily and ran away.", 
            "tag": ["少女", "长发", "草地", "美丽", "人物"]
        }""",
        "en": """Please analyze this group of video frames and return the result in JSON format, containing the following fields:
            - desc: A detailed description of the video (in English)
            - tag: A list of tags that represent the specific features of the video (in English)
        Please return the JSON format directly, without any additional text.
        Example format: {
            "desc": "A cute cat sitting on the window sill", 
            "tag": ["close-up", "young girl", "long hair", "grassland", "beautiful", "person", "natural scenery"]
        }"""
    }
}

# music api config
MUSIC_API_CONFIG = {
    "jamendo": {
        "base_url": "https://api.jamendo.com/v3.0",
        "client_id": os.getenv("JAMENDO_CLIENT_ID", "YOUR_JAMENDO_CLIENT_ID"),
        "tracks_endpoint": "/tracks/",
        "format": "json"
    },
    "freesound": {
        "base_url": "https://freesound.org/apiv2",
        "api_key": os.getenv("FREESOUND_API_KEY", "YOUR_FREESOUND_API_KEY"),
        "search_endpoint": "/search/text/",
        "format": "json"
    }
}

# music cache dir
MUSIC_CACHE_DIR = os.path.join(PROJECT_FOLDER, "cache", "music")

# image api config
PIXABAY_API_CONFIG = {
    "base_url": "https://pixabay.com/api/",
    "api_key": os.getenv("PIXABAY_API_KEY", "YOUR_PIXABAY_API_KEY"),
    "format": "json"
}
