from analysisi_video import analyze_video_frames
from utils.gpt_tool import analyze_multi_images
from config import TEMP_DIR, OUTPUT_DIR
import os

if __name__ == "__main__":
    # video_path = f"{TEMP_DIR}0914.mp4"
    # result = analyze_video_frames(video_path)
    # print(result)


    image_paths = os.listdir(f"{TEMP_DIR}frames/")
    image_paths = [f"{TEMP_DIR}frames/{image_path}" for image_path in image_paths]
    print(image_paths)
    res = analyze_multi_images(image_paths=image_paths)
    print(res)
