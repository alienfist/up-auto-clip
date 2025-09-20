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
