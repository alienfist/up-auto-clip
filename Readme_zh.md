# 🎬 UP AUTO CLIP

**Language**: [English](./Readme.md) | 中文

> 完全本地化的视频自动处理剪辑工具, 主要是省钱, 省钱, 再省钱
尚未完工, 项目代码正在整理中...

## ✨ 功能特性

### 📹 第一步：视频预处理
- [√] 将完整视频按场景切换自动切分为多个场景片段
- [√] 逐个分析场景视频内容
- [√] 自动生成视频描述和标签，存储为JSON格式

### 📝 第二步：智能文案生成 ⏳
- [√] 根据指定主题，利用对话模型生成完整文案
- [√] 通过文案内容与视频片段描述和标签进行智能匹配
- [ ] 自动批量生成视频拼接方案

### 🎵 第三步：自动化后期制作 ⏳
- [ ] 根据文本内容进行AI语音配音
- [ ] 智能匹配主题背景音乐
- [ ] 自动视频转场和拼接，输出完整成品视频

## 💻 系统要求

### 最低配置
- **GPU**: RTX 3060 12GB 或更高
- **内存**: 16GB RAM 推荐
- **存储**: 至少 50GB 可用空间

## 🤖 AI 模型配置

### 视觉模型
```bash
# 安装 qwen2.5vl 视觉模型
ollama run qwen2.5vl
```

### 对话模型
```bash
# 安装 qwen3:14b 对话模型
ollama run qwen3:14b
```

# 背景音乐API配置说明
### Jamendo
- **注册地址**: https://developer.jamendo.com/
- **配置**: 需要获取Client ID
- **特点**: 音乐质量高，分类丰富

### Freesound
- **注册地址**: https://freesound.org/apiv2/
- **配置**: 需要获取API Key
- **特点**: 音效丰富，适合短音频

## 🚀 快速开始

### 环境安装
```bash
# 创建虚拟环境
conda create -n up-auto-clip python=3.12

# 激活环境
conda activate up-auto-clip

# 安装依赖
pip install -r requirements.txt
```

### 配置环境变量
1. 把.env.example改名为.env
2. 并填写对应音乐和图片的API Key
3. 修改默认语言中文zh，英文en

### 使用方法
```bash
# 运行主程序
python main.py
```

## 📁 项目结构
```
up-auto-clip/
├── .env.example     # 环境变量模板
├── .gitignore       # Git忽略文件
├── Readme.md        # 英文文档
├── Readme_zh.md     # 中文文档
├── analysisi_video.py # 视频分析脚本
├── config.py        # 配置文件
├── logger.py        # 日志模块
├── main.py          # 主程序入口
├── requirements.txt # 依赖列表
├── test/            # 测试模块
│   ├── test_image_api.py # 图像API测试
│   └── test_music_api.py # 音乐API测试
└── utils/           # 工具模块
    ├── __init__.py  # 包初始化文件
    ├── audio_tool.py # 音频处理工具
    ├── common.py    # 通用工具函数
    ├── gpt_tool.py  # AI模型接口
    ├── music_tool.py # 音乐处理工具
    ├── pic_tool.py  # 图像处理工具
    ├── tts_tool.py  # 文本转语音工具
    └── video_tool.py # 视频处理工具
```

## 📄 许可证

MIT License

---

**注意**: 本项目需要足够的GPU显存来运行AI模型，请确保您的硬件配置满足要求。