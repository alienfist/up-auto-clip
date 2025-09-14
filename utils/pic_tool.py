# -*- coding: UTF-8 -*-
# pic_tool.py

import os
import random
import requests
from PIL import Image
from config import PIXABAY_API_CONFIG
from logger import logger


class PixabayAPI:
    """Pixabay API client for searching and downloading images
    """
    
    def __init__(self):
        self.config = PIXABAY_API_CONFIG
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", "images")
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def search_images(self, query, category="all", image_type="photo", orientation="all", 
                     min_width=0, min_height=0, per_page=20):
        """Search images from Pixabay
        :param query: Search keywords
        :param category: Image category (backgrounds, fashion, nature, science, education, feelings, health, people, places, animals, industry, computer, food, sports, transportation, travel, buildings, business, music)
        :param image_type: Image type (all, photo, illustration, vector)
        :param orientation: Image orientation (all, horizontal, vertical)
        :param min_width: Minimum width
        :param min_height: Minimum height
        :param per_page: Number of results per page (3-200)
        :return: List of images
        """
        try:
            params = {
                "key": self.config["api_key"],
                "q": query,
                "image_type": image_type,
                "orientation": orientation,
                "category": category,
                "min_width": min_width,
                "min_height": min_height,
                "per_page": min(per_page, 200),  # max200
                "safesearch": "true"
            }
            
            response = requests.get(self.config["base_url"], params=params)
            
            if response.status_code != 200:
                logger.error(f"Pixabay API request failed: {response.status_code}, {response.text}")
                return []
            
            data = response.json()
            images = []
            
            for hit in data.get("hits", []):
                images.append({
                    "id": hit.get("id"),
                    "tags": hit.get("tags"),
                    "preview_url": hit.get("previewURL"),
                    "web_url": hit.get("webformatURL"),
                    "large_url": hit.get("largeImageURL"),
                    "full_hd_url": hit.get("fullHDURL"),
                    "width": hit.get("imageWidth"),
                    "height": hit.get("imageHeight"),
                    "size": hit.get("imageSize"),
                    "views": hit.get("views"),
                    "downloads": hit.get("downloads"),
                    "likes": hit.get("likes"),
                    "user": hit.get("user")
                })
            
            logger.info(f"Found {len(images)} images for query: {query}")
            return images
            
        except Exception as e:
            logger.error(f"Error searching Pixabay images: {str(e)}")
            return []
    
    def download_image(self, image_info, target_path=None, quality="web"):
        """Download image from Pixabay
        :param image_info: Image information dictionary
        :param target_path: Target path, if None save to cache directory
        :param quality: Image quality (preview, web, large, fullhd)
        :return: Downloaded image path
        """
        try:
            image_id = image_info.get("id")
            
            # Select URL based on quality
            url_map = {
                "preview": image_info.get("preview_url"),
                "web": image_info.get("web_url"),
                "large": image_info.get("large_url"),
                "fullhd": image_info.get("full_hd_url")
            }
            
            download_url = url_map.get(quality, image_info.get("web_url"))
            
            if not download_url:
                logger.error(f"Unable to get image download URL: {image_info}")
                return None
            
            # Determine file extension
            file_extension = ".jpg"  # Pixabay mainly provides JPG format
            if "png" in download_url.lower():
                file_extension = ".png"
            
            file_name = f"pixabay_{image_id}_{quality}{file_extension}"
            
            if target_path is None:
                target_path = os.path.join(self.cache_dir, file_name)
            
            # If file already exists, return directly
            if os.path.exists(target_path):
                logger.info(f"Using cached image: {target_path}")
                return target_path
            
            logger.info(f"Downloading image: {download_url} -> {target_path}")
            response = requests.get(download_url, stream=True)
            
            if response.status_code != 200:
                logger.error(f"Failed to download image: {response.status_code}")
                return None
            
            # Ensure target directory exists
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            with open(target_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Image downloaded successfully: {target_path}")
            return target_path
            
        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}")
            return None


def search_and_download_image(query, category="all", image_type="photo", orientation="all", quality="web", target_path=None):
    """Search and download image from Pixabay
    :param query: Search keywords
    :param category: Image category
    :param image_type: Image type
    :param orientation: Image orientation
    :param quality: Image quality
    :param target_path: Target path
    :return: Downloaded image path, None if failed
    """
    try:
        api = PixabayAPI()
        
        # Search images
        images = api.search_images(query, category, image_type, orientation)
        
        if not images:
            logger.warning(f"No images found for query: {query}")
            return None
        
        # Randomly select an image
        selected_image = random.choice(images)
        
        # Download image
        image_path = api.download_image(selected_image, target_path, quality)
        return image_path
        
    except Exception as e:
        logger.error(f"Error searching and downloading image: {str(e)}")
        return None


def get_pic_size(pic_path):
    """get pic size
    Args:
        pic_path (str): pic path
    Returns:
        tuple: (width, height)
    """
    try:
        if not os.path.isfile(pic_path):
            return None
        pic_size = Image.open(pic_path).size
        return pic_size
    except Exception as e:
        logger.error(e)
        return None
        

def gen_pure_pic(pic_size, pic_color, save_pic_path):
    """gen pure pic
    Args:
        pic_size (tuple): pic size
        pic_color (str): pic color
        save_pic_path (str): save pic path
    Returns:
        str: save pic path
    """
    try:
        bg_img = Image.new('RGB', pic_size, pic_color)
        bg_img.save(save_pic_path)
        return save_pic_path
    except Exception as e:
        logger.error(e)
        return None


def get_random_pic_from_folder(folder_path):
    """get random pic from folder
    Args:
        folder_path (str): folder path
    Returns:
        str: random pic path
    """
    if not os.path.isdir(folder_path):
        logger.error(f"image folder not exists. {folder_path}")
        return None
    all_files = os.listdir(folder_path)
    image_extensions = ('.png', '.jpg', '.bmp', '.jpeg')
    image_files = [file for file in all_files if file.lower().endswith(image_extensions)]
    if not image_files:
        logger.error(f"image files not exists. {image_files}")
        return None
    random_image = random.choice(image_files)
    random_image_path = os.path.join(folder_path, random_image)
    if not random_image_path:
        logger.error(f"image file not exists. {random_image_path}")
        return None
    return random_image_path


def adjust_pic_size(pic_path, new_size, output_path=None):
    """adjust pic size
    Args:
        pic_path (str): pic path
        new_size (tuple): new size
        output_path (str, optional): output path. Defaults to None.
    Returns:
        str: output path
    """
    try:
        if not os.path.exists(pic_path):
            logger.error(f"pic not exitsts. {pic_path}")
            return None

        pic_suffix = os.path.splitext(pic_path)[-1]
        if pic_suffix not in ['.jpg', '.jpeg', '.png']:
            logger.error(f"pic format not support. {pic_path}")
            return None

        pic = Image.open(pic_path)
        original_size = pic.size
        if original_size != new_size:
            if not output_path:
                output_path = os.path.splitext(pic_path)[0] + '_new' + pic_suffix
            pic = pic.resize(new_size)
            pic.save(output_path)
            return output_path
        else:
            return pic_path
    except Exception as e:
        logger.error(e)
        return None
