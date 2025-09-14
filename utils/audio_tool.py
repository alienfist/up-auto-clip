# -*- coding: utf-8 -*-
# audio_tool.py

import os
import shutil
from pydub import AudioSegment
from typing import List, Optional
from logger import logger


def get_audio_duration(audio_path: str) -> Optional[float]:
    """get audio duration in seconds
    Args:
        audio_path (str)
    Returns:
        float: audio duration in seconds
    """
    try:
        sound_seg = AudioSegment.from_file(audio_path)
        return sound_seg.duration_seconds
    except Exception as e:
        logger.error(f"An error occurred while retrieving audio duration for '{audio_path}': {e}")
        return None


def reduce_audio_silence(input_audio_path: str, output_audio_path: str, start_silence_millisecond: int = 0, end_silence_millisecond: int = 500) -> Optional[str]:
    """reduce audio silence
    Args:
        input_audio_path (str): input audio file path
        output_audio_path (str): output audio file path
        start_silence_millisecond (int): start silence duration in milliseconds, default 0ms
        end_silence_millisecond (int): end silence duration in milliseconds, default 500ms
    Returns:
        str: output audio file path if successful, None otherwise
    """
    if start_silence_millisecond < 0 or end_silence_millisecond < 0:
        raise ValueError("Silence durations must be non-negative.")

    try:
        audio = AudioSegment.from_file(input_audio_path)
        logger.info(f"audio duration: {len(audio)}ms")

        if start_silence_millisecond + end_silence_millisecond > len(audio):
            raise ValueError("The total silence duration exceeds the audio length.")

        trimmed_audio = audio[start_silence_millisecond:len(audio) - end_silence_millisecond]
        trimmed_audio.export(output_audio_path, format="wav")
        return output_audio_path
    except Exception as e:
        logger.error(f"An error occurred while reducing silence for '{input_audio_path}': {e}")
        return None


def audio_combination(audio_path_list: List[str], output_path: str) -> Optional[str]:
    """combine multiple audio files into one
    Args:
        audio_path_list (List[str]): list of audio file paths
        output_path (str): output audio file path
    Returns:
        Optional[str]: output audio file path if successful, None otherwise
    """
    if not audio_path_list:
        logger.error("No audio files provided for merging.")
        return None

    if len(audio_path_list) == 1:
        shutil.copy(audio_path_list[0], output_path)
        return output_path

    final_seg = AudioSegment.empty()
    for audio_path in audio_path_list:
        if not os.path.isfile(audio_path):
            logger.warning(f"Audio file does not exist: {audio_path}")
            continue
        try:
            audio_seg = AudioSegment.from_file(audio_path)
            final_seg += audio_seg
        except Exception as e:
            logger.error(f"Error processing file '{audio_path}': {e}")

    if final_seg:
        final_seg.export(output_path, format="wav")
        return output_path
    else:
        logger.error("No valid audio segments to combine.")
        return None
