# -*- coding: UTF-8 -*-
# demo_multi_perspective.py
# 多视角视频生成演示脚本

import os
from main import AutoClip
from config import TEMP_DIR

def demo_multi_perspective_generation():
    """
    演示多视角视频生成功能
    """
    print("=== 多视角视频生成演示 ===")
    
    # 初始化AutoClip实例
    video_path = f"{TEMP_DIR}test.webm"  # 请确保这个视频文件存在
    
    if not os.path.exists(video_path):
        print(f"错误: 视频文件 {video_path} 不存在")
        print("请将您的视频文件放置到指定路径，或修改video_path变量")
        return
    
    auto_clip = AutoClip(video_path=video_path)
    
    print(f"处理视频: {video_path}")
    print(f"临时目录: {auto_clip.temp_dir}")
    
    # 1. 视频预处理
    print("\n步骤1: 视频预处理...")
    res_preprocess = auto_clip.preprocess_video_segment()
    
    if not res_preprocess:
        print("视频预处理失败，请检查视频文件")
        return
    
    print("视频预处理完成")
    
    # 2. 选择要生成的视角
    print("\n步骤2: 选择视角...")
    
    # 方案1: 生成所有10个视角的视频
    print("生成所有10个视角的视频...")
    results_all = auto_clip.generate_multiple_perspective_videos()
    
    # 方案2: 只生成指定的几个视角
    # selected_perspectives = ['emotional', 'entertaining', 'inspirational']
    # print(f"生成指定视角的视频: {selected_perspectives}")
    # results_selected = auto_clip.generate_multiple_perspective_videos(selected_perspectives)
    
    # 3. 显示结果
    print("\n=== 生成结果 ===")
    
    if results_all:
        print(f"成功生成 {len(results_all)} 个不同视角的视频:")
        
        for i, result in enumerate(results_all, 1):
            perspective_names = {
                 'default': '默认通用',
                 'emotional': '情感共鸣',
                 'educational': '知识科普',
                 'entertaining': '轻松娱乐',
                 'inspirational': '励志激励',
                 'aesthetic': '美学艺术',
                 'trending': '热点话题',
                 'lifestyle': '生活方式',
                 'professional': '专业技能',
                 'storytelling': '故事叙述'
             }
            
            perspective_cn = perspective_names.get(result['perspective'], result['perspective'])
            print(f"{i}. 【{perspective_cn}】视角")
            print(f"   文件路径: {result['video_path']}")
            print(f"   片段数量: {result['segments_count']}")
            print(f"   文件大小: {get_file_size(result['video_path'])}")
            print()
        
        print(f"所有视频文件保存在: {auto_clip.temp_dir}")
        print("\n视角说明:")
        print("- 默认通用: 适合各种类型视频，平衡全面")
        print("- 情感共鸣: 突出情感元素，温馨感人")
        print("- 知识科普: 突出教育价值，专业清晰")
        print("- 轻松娱乐: 突出有趣幽默，轻松愉快")
        print("- 励志激励: 突出正能量，鼓舞人心")
        print("- 美学艺术: 突出美感艺术，优雅诗意")
        print("- 热点话题: 突出流行趋势，容易传播")
        print("- 生活方式: 突出日常生活，实用贴近")
        print("- 专业技能: 突出技能展示，专业权威")
        print("- 故事叙述: 突出故事情节，引人入胜")
        
    else:
        print("未能成功生成任何视频，请检查:")
        print("1. 视频文件是否有效")
        print("2. 网络连接是否正常（需要调用GPT API）")
        print("3. 配置文件是否正确")
        print("4. 查看日志文件获取详细错误信息")

def get_file_size(file_path):
    """获取文件大小的友好显示"""
    try:
        size = os.path.getsize(file_path)
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    except:
        return "未知"

if __name__ == "__main__":
    demo_multi_perspective_generation()