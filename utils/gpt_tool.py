# -*- coding: UTF-8 -*-
# gpt_tool.py

import os
import re
import ollama
import json
import base64
from utils.common import retry_decorator
from config import OLLAMA_HOST, OLLAMA_VISION_MODEL, OLLAMA_CHAT_MODEL, DEFAULT_LANGUAGE, OLLAMA_OPTIONS
from sys_prompts import DEFAULT_PROMPT
from logger import logger


client = ollama.Client(host=OLLAMA_HOST, timeout=60)


@retry_decorator(max_retries=3, delay=2)
def analyze_image(image_path: str, prompt=None, role_desc=None):
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
            raise FileNotFoundError(f"Image file not found: {image_path}")

        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        if not prompt:
            prompt = DEFAULT_PROMPT["one_frame"][DEFAULT_LANGUAGE]
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
        result = json.loads(result_text)
        if 'desc' not in result or 'tag' not in result:
            logger.error(f"analyze image error:{result_text}")
            raise ValueError(f"Invalid result format: {result_text}")

        return result
            
    except Exception as e:
        logger.error(f"analyze image error:{e}")
        raise e


@retry_decorator(max_retries=3, delay=2)
def analyze_multi_images(images_data: list, prompt=None, role_desc=None):
    """analyze multi images
    Args:
        images_data (list): image data list
    Returns:
        dict: {"desc": "", "tag": []}
    """
    try:
        if not role_desc:
            role_desc = DEFAULT_PROMPT["role_desc"][DEFAULT_LANGUAGE]
        
        if not prompt:
            prompt = DEFAULT_PROMPT["multi_frame"][DEFAULT_LANGUAGE]
         
        logger.info(f"start analyze {len(images_data)} images...")

        total_size = sum(len(img) for img in images_data)
        logger.info(f"images data total size: {total_size / 1024 / 1024:.2f} MB")
        
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
                    'images': images_data
                }
            ],
            format='json'
        )
        
        logger.info(f"ollama response success, start parse result...")
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
            
    except ollama.ResponseError as e:
        logger.error(f"ollama response error: {e}")
        raise e
    except ollama.RequestError as e:
        logger.error(f"ollama request error: {e}")
        raise e
    except TimeoutError as e:
        logger.error(f"ollama request timeout: {e}")
        raise e
    except json.JSONDecodeError as e:
        logger.error(f"json decode error: {e}")
        raise e
    except Exception as e:
        logger.error(f"analyze image error:{e}")
        logger.error(f"exception type: {type(e).__name__}")
        raise e


@retry_decorator(max_retries=3, delay=2)
def get_gpt_response(prompt, response_format='', role_desc=None):
    """get gpt response
    Args:
        prompt (str): prompt
        response_format (str, optional): format. Defaults to ''.
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
            format=response_format,
            options=OLLAMA_OPTIONS,
        )
        result_text = response['message']['content'].strip()
        try:
            if response_format:
                result = json.loads(result_text)
                return result
            else:
                # remove think content
                result_text = remove_think_tags(result_text)
                return result_text
        except json.JSONDecodeError:
            logger.error(f"get gpt response error:{result_text}")
            return None

    except Exception as e:
        logger.error(f"get gpt response error:{e}")
        raise e


def remove_think_tags(text):
    """remove think tags
    Args:
        text (str): text
    Returns:
        str: cleaned text
    """
    try:
        cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text
    except Exception as e:
        logger.error(f"remove think tags error:{e}")
        return text
