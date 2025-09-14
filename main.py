from analysisi_video import analyze_video_frames
from config import TEMP_DIR

if __name__ == "__main__":
    video_path = f"{TEMP_DIR}test.mp4"
    result = analyze_video_frames(video_path)
    print(result)
