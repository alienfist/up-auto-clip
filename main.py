from analysisi_video import analyze_video_frames, analyze_video_multi_frames
from config import TEMP_DIR
import os

if __name__ == "__main__":
    video_path = f"{TEMP_DIR}test.mp4"

    # frames_info = analyze_video_frames(video_path)
    # print(frames_info)

    video_info = analyze_video_multi_frames(video_path)
    print(video_info)
