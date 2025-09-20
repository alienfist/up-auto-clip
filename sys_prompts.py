# default prompt
DEFAULT_PROMPT = {
    "video_edit_role_desc": {
        "zh": """你是一个专业的视频编辑。""",
        "en": """You are a professional video editor."""
    },

    "screenwriter_role_desc": {
        "zh": """你是一个专业的短视频编辑和脚本策划师，擅长根据视频内容创作吸引人的短视频脚本。""",
        "en": """You are a professional short video editor and script planner, skilled at creating engaging short video scripts based on video content."""
    },
    
    "one_frame": {
        "zh": """请分析这张图片,并以JSON格式返回结果,包含以下字段:
            - desc: 图片的详细描述（中文）
            - tag: 能代表图片具体特征的标签列表,
                tag必须包含镜头元素(近景、远景、中景)
                tag必须包含主体元素(人物、动物、车辆等)
                tag必须包含场景元素(城市、乡村、 自然风光等)
            请直接返回JSON格式,不要包含其他文字。
            示例格式：{
                "desc": "一个美丽的少女长发飘飘走在绿色的草地上...", 
                "tag": ["近景", "少女", "长发", "草地", "美丽", "人物", "自然风光"]
            }""",
        "en": """Please analyze this image and return the result in JSON format, containing the following fields:
            - desc: A detailed description of the image (in English)
            - tag: A list of tags that represent the specific features of the image (in English)
                tag must contain lens element (near, far, medium)
                tag must contain subject element (person, animal, vehicle, etc.)
                tag must contain scene element (city, countryside, nature, etc.)
            Please return the JSON format directly, without any additional text.
            Example format: {
                "desc": "A beautiful young girl with long hair is walking on the green grass...", 
                "tag": ["close-up", "young girl", "long hair", "grassland", "beautiful", "person", "natural scenery"]
            }"""
    },

    "multi_frame": {
        "zh": """这是一个视频片段的连续帧画面，请仔细分析这组图片的时间序列变化，并以JSON格式返回结果：

            分析要求：
            1. 观察画面中的动态变化、人物动作、场景转换
            2. 识别主要元素：人物、物体、环境、动作
            3. 注意镜头运动：推拉摇移、景别变化
            4. 捕捉情感氛围和视觉风格

            返回字段：
            - desc: 详细描述视频内容，包括场景、人物、动作、变化过程（150-200字，中文）
            - tag: 精确的标签列表，必须包含以下类别（中文）：
            * 镜头类型：[特写/近景/中景/远景/全景]
            * 主体对象：[人物/动物/物体/建筑等]
            * 场景环境：[室内/室外/城市/自然/等]
            * 动作行为：[具体的动作描述]
            * 情感氛围：[欢快/安静/紧张/温馨等]
            * 视觉风格：[明亮/昏暗/色彩丰富等]

            请直接返回JSON格式，不要包含其他文字。
            示例格式：{
                "desc": "一位身穿白色连衣裙的年轻女子在阳光明媚的公园里缓缓走过绿色草坪，她停下脚步弯腰捡起地上的一片落叶，仔细观察后露出微笑，然后轻快地跳跃着向前跑去，整个画面充满了青春活力和自然和谐的美感", 
                "tag": ["中景", "远景", "年轻女子", "白色连衣裙", "公园", "草坪", "室外", "自然环境", "走路", "弯腰", "捡拾", "跳跃", "奔跑", "欢快", "活力", "阳光明媚", "绿色"]
            }""",
        
        "en": """This is a sequence of consecutive frames from a video segment. Please carefully analyze the temporal changes in this group of images and return the result in JSON format:

            Analysis Requirements:
            1. Observe dynamic changes, character actions, scene transitions
            2. Identify main elements: people, objects, environment, actions
            3. Notice camera movements: push/pull/pan/tilt, shot size changes
            4. Capture emotional atmosphere and visual style

            Return Fields:
            - desc: Detailed description of video content, including scenes, characters, actions, and change processes (150-200 words, in English)
            - tag: Precise tag list, must include the following categories (in English):
            * Shot types: [close-up/medium-shot/long-shot/wide-shot]
            * Main subjects: [person/animal/object/building/etc.]
            * Scene environment: [indoor/outdoor/urban/nature/etc.]
            * Actions/behaviors: [specific action descriptions]
            * Emotional atmosphere: [joyful/calm/tense/warm/etc.]
            * Visual style: [bright/dim/colorful/etc.]

            Please return JSON format directly, without any additional text.
            Example format: {
                "desc": "A young woman in a white dress walks slowly across a green lawn in a sunny park. She stops to bend down and pick up a fallen leaf, examines it carefully with a smile, then jumps and runs forward playfully. The entire scene is filled with youthful vitality and natural harmony.", 
                "tag": ["medium-shot", "long-shot", "young woman", "white dress", "park", "lawn", "outdoor", "natural environment", "walking", "bending", "picking up", "jumping", "running", "joyful", "energetic", "sunny", "green"]
            }"""
    },
    "video_script": {
        "zh": """根据以下视频分段信息，创作一个精彩的短视频脚本，总时长控制在15-30秒：
            视频分段信息如下：
            {video_segment_info_list}
            
            请分析视频内容的亮点和故事线，然后生成短视频脚本。要求：
            1. 选择最精彩、最有吸引力的片段进行剪辑
            2. 确保内容连贯，有完整的故事性或明确的主题
            3. 时间安排要紧凑，节奏要快
            4. 为每个片段提供具有感染力的文本用于配音
            5. 如果有必要，可以为片段提供文本用于字幕
            
            **重要：请严格按照JSON格式输出，不要包含任何其他文字、解释或markdown标记**
            
            输出JSON数组格式，每个对象包含以下字段：
            - start: 原视频裁切开始时间（数字，单位秒）
            - end: 原视频裁切结束时间（数字，单位秒）
            - screen_text: 显示在屏幕上的文字（字符串，如果没有特别好的内容，可为空字符串""）
            - narration: TTS旁白内容（字符串，可为空字符串""）
            
            请直接输出JSON数组，不要添加任何前缀、后缀或解释文字。
            参照示例格式：[{{"start": 10.5, "end": 15.2, "screen_text": "震撼开场", "narration": "接下来你将看到令人惊叹的一幕"}}]
        """,
        "en": """Based on the following video segment information, create an exciting short video script with a total duration of 15-30 seconds:
            Video segment information:
            {video_segment_info_list}
            
            Please analyze the highlights and storyline of the video content, then generate a short video script. Requirements:
            1. Select the most exciting and attractive segments for editing
            2. Ensure content coherence with a complete story or clear theme
            3. Keep timing tight with fast-paced rhythm
            4. Provide compelling text for voiceover for each segment
            5. If necessary, provide text for subtitles for segments
            
            **Important: Please output strictly in JSON format, without any other text, explanations, or markdown markers**
            
            Output JSON array format, each object contains the following fields:
            - start: Original video clip start time (number, in seconds)
            - end: Original video clip end time (number, in seconds)
            - screen_text: Text displayed on screen (string, can be empty string "" if no particularly good content)
            - narration: TTS voiceover content (string, can be empty string "")
            
            Please output the JSON array directly, without adding any prefix, suffix, or explanatory text.
            Reference example format: [{{"start": 10.5, "end": 15.2, "screen_text": "Stunning Opening", "narration": "You are about to witness an amazing scene"}}]
        """,
    },
}