# -*- coding: UTF-8 -*-
# gpt_tool.py

import os
import re
import ollama
import json
import base64
from .common import retry_decorator
from config import OLLAMA_HOST, OLLAMA_VISION_MODEL, OLLAMA_CHAT_MODEL, DEFAULT_PROMPT, DEFAULT_LANGUAGE
from logger import logger


client = ollama.Client(host=OLLAMA_HOST)


@retry_decorator(max_retries=3, delay=1)
def analyze_image(image_path, prompt=None, role_desc=None):
    """analyze image
    Args:
        image_paths (list): image path list
    Returns:
        dict: {"desc": "", "tag": []}
    """
    try:
        if not role_desc:
            role_desc = DEFAULT_PROMPT["role_desc"][DEFAULT_LANGUAGE]
        
        if not os.path.isfile(image_path):
            logger.error(f"image not exist:{image_path}")
            return None

        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        if not prompt:
            prompt = DEFAULT_PROMPT["vision"][DEFAULT_LANGUAGE]
        response = client.chat(
            model=OLLAMA_VISION_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': role_desc
                },
                {
                    'role': 'user',
                    'content': prompt,
                    'images': [image_data]
                }
            ],
            format='json'
        )

        result_text = response['message']['content'].strip()
        try:
            result = json.loads(result_text)
            if 'desc' not in result or 'tag' not in result:
                logger.error(f"analyze image error:{result_text}")
                return None

            return result
        except json.JSONDecodeError:
            logger.error(f"analyze image error:{result_text}")
            return None
            
    except Exception as e:
        logger.error(f"analyze image error:{e}")
        return None


@retry_decorator(max_retries=3, delay=1)
def get_gpt_response(prompt, format='', role_desc=None):
    """get gpt response
    Args:
        prompt (str): prompt
        format (str, optional): format. Defaults to 'text'.
    Returns:
        str: response
    """
    try:
        if not role_desc:
            role_desc = DEFAULT_PROMPT["role_desc"][DEFAULT_LANGUAGE]
        
        response = client.chat(
            model=OLLAMA_CHAT_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': role_desc
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            format=format
        )
        if format == 'json':
            model_response = response['message']['content'].strip()
            try:
                result = json.loads(model_response)
                return result
            except json.JSONDecodeError:
                logger.error(f"get gpt response error:{model_response}")
                return None
        else:
            model_response = response['message']['content'].strip()
            final_answer = re.sub(r'<think>.*?</think>\s*', '', model_response, flags=re.DOTALL).strip()
            return final_answer

    except Exception as e:
        logger.error(f"get gpt response error:{e}")
        return None
