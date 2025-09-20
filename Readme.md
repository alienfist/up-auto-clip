# 🎬 UP AUTO CLIP

**Language**: English | [中文](./Readme_zh.md)

> Fully localized automated video processing and editing tool, mainly for saving money, saving money, and saving money again
The project is not yet completed, and the project code is currently being organized ..

## ✨ Features

### 📹 Step 1: Video Preprocessing ✅
- [√] Automatically split complete videos into multiple scene segments based on scene transitions
- [√] Analyze each scene video individually
- [√] Generate video descriptions and tags, stored in JSON format

### 📝 Step 2: Intelligent Script Generation ⏳
- [ ] Generate complete scripts based on specified themes using dialogue models
- [ ] Intelligently match script content with video segment descriptions and tags
- [ ] Automatically generate a lot of video splicing solutions

### 🎵 Step 3: Automated Post-Production ⏳
- [ ] AI voice dubbing based on text content
- [ ] Intelligent matching of theme background music
- [ ] Automatic video transitions and splicing, output complete finished videos

## 💻 System Requirements

### Minimum Configuration
- **GPU**: RTX 3060 12GB or higher
- **Memory**: 16GB RAM recommended
- **Storage**: At least 50GB available space

## 🤖 AI Model Configuration

### Vision Model
```bash
# Install qwen2.5vl vision model
ollama run qwen2.5vl
```

### Dialogue Model
```bash
# Install qwen3:14b dialogue model
ollama run qwen3:14b
```

# Background Music API Configuration
### Jamendo
- **Registration**: https://developer.jamendo.com/
- **Configuration**: Need to obtain Client ID
- **Features**: High-quality music, rich categories

### Freesound
- **Registration**: https://freesound.org/apiv2/
- **Configuration**: Need to obtain API Key
- **Features**: Rich sound effects, suitable for short audio

## 🚀 Quick Start

### Environment Setup
```bash
# Create virtual environment
conda create -n up-auto-clip python=3.12

# Activate environment
conda activate up-auto-clip

# Install dependencies
pip install -r requirements.txt
```

### Configuration
1. Rename .env.example to .env
2. Fill in the corresponding music and image API keys
3. Modify the default language to Chinese (zh) or English (en)

### Usage
```bash
# Run main program
python main.py
```

## 📁 Project Structure
```
up-auto-clip/
├── .env.example     # Environment variables template
├── .gitignore       # Git ignore file
├── Readme.md        # English documentation
├── Readme_zh.md     # Chinese documentation
├── analysisi_video.py # Video analysis script
├── config.py        # Configuration file
├── logger.py        # Logging module
├── main.py          # Main program entry
├── requirements.txt # Dependencies list
├── test/            # Test modules
│   ├── test_image_api.py # Image API tests
│   └── test_music_api.py # Music API tests
└── utils/           # Utility modules
    ├── __init__.py  # Package initialization
    ├── audio_tool.py # Audio processing tools
    ├── common.py    # Common utility functions
    ├── gpt_tool.py  # AI model interface
    ├── music_tool.py # Music processing tools
    ├── pic_tool.py  # Image processing tools
    ├── tts_tool.py  # Text-to-speech tools
    └── video_tool.py # Video processing tools
```

## 📄 License

MIT License

---

**Note**: This project requires sufficient GPU memory to run AI models. Please ensure your hardware configuration meets the requirements.
