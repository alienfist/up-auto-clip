# -*- coding: UTF-8 -*-
# tts_tool.py

import os
import time
import edge_tts
from config import TEMP_DIR
from logger import logger


def generate_tts(text, voice="zh-CN-XiaoxiaoNeural", output=None, rate="+0%", pitch="+0Hz", volume="+0%"):
    """generate tts
    Args:
        text (str): text
        voice (str, optional): voice. Defaults to "zh-CN-XiaoxiaoNeural".
        rate (str, optional): rate. Defaults to "+0%".
        pitch (str, optional): pitch. Defaults to "+0Hz".
        volume (str, optional): volume. Defaults to "+0%".
    Returns:
        str: audio path
    """
    try:
        if output is None:
            output = f"{TEMP_DIR}{time.time()}.wav"
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume)
        submaker = edge_tts.SubMaker()
        
        # save audio file
        with open(output, "wb") as audio_file:
            for chunk in communicate.stream_sync:
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] in ["WordBoundary", "SentenceBoundary"]:
                    # SubMaker chunk data
                    submaker.feed(chunk)
        
        # save srt file
        srt_content = submaker.get_srt()
        with open(output.replace(".wav", ".srt"), "w", encoding="utf-8") as f:
            f.write(srt_content)
        return output
    except Exception as e:
        logger.error(e)
        return None
        

async def async_generate_tts(text, voice="zh-CN-XiaoxiaoNeural", output=None, rate="+0%", pitch="+0Hz", volume="+0%"):
    """generate tts async
    Args:
        text (str): text
        voice (str, optional): voice. Defaults to "zh-CN-XiaoxiaoNeural".
        rate (str, optional): rate. Defaults to "+0%".
        pitch (str, optional): pitch. Defaults to "+0Hz".
        volume (str, optional): volume. Defaults to "+0%".
    Returns:
        str: audio path
    """
    try:
        if output is None:
            output = f"{TEMP_DIR}{time.time()}.wav"
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume)
        submaker = edge_tts.SubMaker()
        
        # save audio file
        with open(output, "wb") as audio_file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] in ["WordBoundary", "SentenceBoundary"]:
                    # SubMaker chunk data
                    submaker.feed(chunk)
        
        # save srt file
        srt_content = submaker.get_srt()
        with open(output.replace(".wav", ".srt"), "w", encoding="utf-8") as f:
            f.write(srt_content)
        return output
    except Exception as e:
        logger.error(e)
        return None
