# -*- coding: UTF-8 -*-
# common.py

import os
import time
import math
from functools import wraps
from typing import Any, Callable


def retry_decorator(max_retries: int = 3, delay: float = 1.0):
    """retry decorator
    Args:
        max_retries (int): max retries
        delay (float): delay time(seconds)
    Returns:
        Callable: wrapper function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def generate_temp_dir(file_path: str, temp_dir_name: str = None):
    """generate temp dir
    Args:
        file_path (str): file path
        temp_dir_name (str, optional): temp dir name. Defaults to None.
    Returns:
        str: temp dir path
    """
    temp_dir = os.path.dirname(file_path)
    if not temp_dir_name:
        temp_dir_name = time.strftime('%Y%m%d%H%M%S')
    temp_dir = f"{temp_dir}/{temp_dir_name}"
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir


def ms_to_str(ms):
    """convert ms to str
    Args:
        ms (int): ms
    Returns:
        str: str
    """
    try:
        second = ms / 1000
        f = int(math.modf(second)[0] * 1000)  # extract the decimal part of the second, convert to integer
        m, s = divmod(second, 60)
        h, m = divmod(m, 60)
        timestr = "%02d:%02d:%02d,%03d" % (h, m, s, f)  # for subtitle
        return timestr
    except Exception as e:
        print(e)
        return None
