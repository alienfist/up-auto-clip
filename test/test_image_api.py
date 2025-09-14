# -*- coding: UTF-8 -*-
# test_pixabay_images.py
# Test Pixabay image search and download functionality

import os
import sys

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pic_tool import PixabayAPI, search_and_download_image
from logger import logger

def test_pixabay_api():
    """Test Pixabay API functionality"""
    print("Starting Pixabay image API test...")
    
    try:
        # Test search functionality
        api = PixabayAPI()
        print("\n1. Testing image search functionality...")
        
        # Search for nature landscape images
        images = api.search_images("nature landscape", category="nature", per_page=5)
        
        if images:
            print(f"✓ Search successful, found {len(images)} images")
            for i, img in enumerate(images[:3]):
                print(f"  Image {i+1}: ID={img['id']}, Tags={img['tags'][:50]}...")
        else:
            print("✗ Search failed, no images found")
            return False
        
        # Test download functionality
        print("\n2. Testing image download functionality...")
        if images:
            test_image = images[0]
            downloaded_path = api.download_image(test_image, quality="web")
            
            if downloaded_path and os.path.exists(downloaded_path):
                print(f"✓ Download successful: {downloaded_path}")
                file_size = os.path.getsize(downloaded_path)
                print(f"  File size: {file_size} bytes")
            else:
                print("✗ Download failed")
                return False
        
        # Test convenience function
        print("\n3. Testing convenience search and download function...")
        image_path = search_and_download_image("cat", category="animals", quality="web")
        
        if image_path and os.path.exists(image_path):
            print(f"✓ Convenience function test successful: {image_path}")
        else:
            print("✗ Convenience function test failed")
            return False
        
        print("\n✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error occurred during testing: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Pixabay Image Functionality Test")
    print("=" * 50)
    
    # Check environment variables
    from config import PIXABAY_API_CONFIG
    if PIXABAY_API_CONFIG["api_key"] == "YOUR_PIXABAY_API_KEY":
        print("⚠️  Warning: Please set PIXABAY_API_KEY in .env file")
        print("   Test will use default value and may fail")
    
    # Run tests
    success = True
    
    # Test image API (if API key is available)
    if PIXABAY_API_CONFIG["api_key"] != "YOUR_PIXABAY_API_KEY":
        if not test_pixabay_api():
            success = False
    else:
        print("\nSkipping Pixabay image API test (API key not set)")
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Image API test passed!")
    else:
        print("❌ Image API test failed, please check the code")
    print("=" * 50)
