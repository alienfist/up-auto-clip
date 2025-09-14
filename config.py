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
    "vision": {
        "zh": """请分析这张图片，并以JSON格式返回结果，包含以下字段：
            - desc: 图片的详细描述（中文）
            - tag: 能代表图片具体特征的标签列表（中文）
        请直接返回JSON格式，不要包含其他文字。
        示例格式：{"desc": "一个美丽的少女长发飘飘走在绿色的草地上", "tag": ["少女", "长发", "草地", "美丽", "人物"]}""",

        "en": """Please analyze this image and return the result in JSON format, containing the following fields:
            - desc: A detailed description of the image (in English)
            - tag: A list of tags that represent the specific features of the image (in English)
        Please return the JSON format directly, without any additional text.
        Example format: {"desc": "A cute cat sitting on the window sill", "tag": ["cat", "pet", "window sill", "cute"]}"""
    },
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
