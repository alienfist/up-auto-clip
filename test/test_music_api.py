# -*- coding: utf-8 -*-
# test_music_api.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.music_tool import get_music_by_style


def test_music_apis():
    """Test different music APIs"""
    
    test_styles = ["upbeat", "relaxing", "cinematic"]
    apis = ["jamendo", "freesound"]
    
    print("Testing Music APIs")
    print("=" * 50)
    
    for api in apis:
        print(f"\nTesting {api.upper()} API:")
        print("-" * 40)
        
        success_count = 0
        total_count = len(test_styles)
        
        for style in test_styles:
            print(f"Searching for '{style}' style music...")
            try:
                music_path = get_music_by_style(style, duration=30, api_type=api)
                if music_path:
                    print(f"  ✓ Found music: {music_path}")
                    success_count += 1
                else:
                    print(f"  ✗ No music found")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        success_rate = (success_count / total_count) * 100
        print(f"\n{api.upper()} API success rate: {success_rate:.1f}%")
    
    print(f"\nMusic API testing completed!")

if __name__ == "__main__":
    test_music_apis()
