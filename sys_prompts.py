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
            2. 识别画面主要元素：人物、动物、机器、物体、自然环境、动作
            3. 注意镜头运动：推拉摇移、景别变化
            4. 捕捉情感氛围和视觉风格

            返回字段：
            - desc: 详细描述视频内容，包括场景、人物、动作、变化过程（150-300字，中文）
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
            6. 关于视觉风格的描述不要出现在脚本中，只关注视频内容的描述
            7. 未必完全按照时间顺序排列视频分段，根据视频内容的重要性和吸引力，调整片段的顺序
            8. 视频的片头很重要
            
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
            6. Do not include visual style descriptions in the script, only focus on video content descriptions
            
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

# 多视角视频脚本生成提示词
MULTI_PERSPECTIVE_PROMPTS = {
    "default": {
        "zh": """根据以下视频分段信息，创作一个精彩的短视频脚本，总时长控制在15-30秒：
            视频分段信息如下：
            {video_segment_info_list}
            
            请分析视频内容的亮点和故事线，然后生成短视频脚本。要求：
            1. 选择最精彩、最有吸引力的片段进行剪辑
            2. 确保内容连贯，有完整的故事性或明确的主题
            3. 时间安排要紧凑，节奏要快
            4. 为每个片段提供具有感染力的文本用于配音
            5. 适应不同类型视频：生活记录、教学演示、娱乐表演、风景展示等
            6. 保持中性客观的叙述风格，适合大众观看
            7. 根据视频内容的重要性和吸引力，合理调整片段顺序
            8. 注重开头的吸引力，确保前3秒能抓住观众注意力
            
            **重要：请严格按照JSON格式输出，不要包含任何其他文字、解释或markdown标记**
            
            输出JSON数组格式，每个对象包含以下字段：
            - start: 原视频裁切开始时间（数字，单位秒）
            - end: 原视频裁切结束时间（数字，单位秒）
            - screen_text: 显示在屏幕上的文字（字符串，如果没有特别好的内容，可为空字符串""）
            - narration: TTS旁白内容（字符串，可为空字符串""）
            
            请直接输出JSON数组，不要添加任何前缀、后缀或解释文字。
            参照示例格式：[{{"start": 10.5, "end": 15.2, "screen_text": "精彩瞬间", "narration": "让我们一起来看看这个令人印象深刻的时刻"}}]
        """,
        "en": """Based on the following video segment information, create an exciting short video script with a total duration of 15-30 seconds:
            Video segment information:
            {video_segment_info_list}
            
            Please analyze the highlights and storyline of the video content, then generate a short video script. Requirements:
            1. Select the most exciting and attractive segments for editing
            2. Ensure content coherence with a complete story or clear theme
            3. Keep timing tight with fast-paced rhythm
            4. Provide compelling text for voiceover for each segment
            5. Adapt to different video types: lifestyle, tutorials, entertainment, scenery, etc.
            6. Maintain neutral and objective narrative style suitable for general audience
            7. Reasonably adjust segment order based on content importance and appeal
            8. Focus on opening appeal, ensure first 3 seconds grab audience attention
            
            **Important: Please output strictly in JSON format, without any other text, explanations, or markdown markers**
            
            Output JSON array format, each object contains the following fields:
            - start: Original video clip start time (number, in seconds)
            - end: Original video clip end time (number, in seconds)
            - screen_text: Text displayed on screen (string, can be empty string "" if no particularly good content)
            - narration: TTS voiceover content (string, can be empty string "")
            
            Please output the JSON array directly, without adding any prefix, suffix, or explanatory text.
            Reference example format: [{{"start": 10.5, "end": 15.2, "screen_text": "Amazing Moment", "narration": "Let's take a look at this impressive moment together"}}]
        """
    },
    
    "emotional": {
        "zh": """根据以下视频分段信息，创作一个充满情感共鸣的短视频脚本，总时长控制在15-30秒：
            视频分段信息如下：
            {video_segment_info_list}
            
            请从情感角度分析视频内容，生成能触动人心的脚本。要求：
            1. 挖掘视频中的情感元素：温暖、感动、怀念、治愈等
            2. 选择最能引起情感共鸣的片段
            3. 文案要有感染力，能唤起观众的情感记忆
            4. 适合表达情感的视频类型：家庭聚会、成长记录、友情时光、爱情故事、宠物陪伴等
            5. 使用温暖、亲切的语调
            6. 注重情感的递进和升华
            7. 结尾要有情感的升华或感悟
            
            **重要：请严格按照JSON格式输出，不要包含任何其他文字、解释或markdown标记**
            
            输出JSON数组格式，每个对象包含以下字段：
            - start: 原视频裁切开始时间（数字，单位秒）
            - end: 原视频裁切结束时间（数字，单位秒）
            - screen_text: 显示在屏幕上的文字（字符串，情感化表达）
            - narration: TTS旁白内容（字符串，温暖感人的叙述）
            
            请直接输出JSON数组，不要添加任何前缀、后缀或解释文字。
            参照示例格式：[{{"start": 5.0, "end": 10.0, "screen_text": "那些美好的时光", "narration": "每一个平凡的瞬间，都藏着最珍贵的回忆"}}]
        """,
        "en": """Based on the following video segment information, create an emotionally resonant short video script with a total duration of 15-30 seconds:
            Video segment information:
            {video_segment_info_list}
            
            Please analyze the video content from an emotional perspective and generate a heart-touching script. Requirements:
            1. Discover emotional elements in the video: warmth, touching moments, nostalgia, healing, etc.
            2. Select segments that can evoke emotional resonance
            3. Copy should be infectious and awaken audience's emotional memories
            4. Suitable for emotional video types: family gatherings, growth records, friendship moments, love stories, pet companionship, etc.
            5. Use warm and intimate tone
            6. Focus on emotional progression and elevation
            7. Ending should have emotional elevation or insight
            
            **Important: Please output strictly in JSON format, without any other text, explanations, or markdown markers**
            
            Output JSON array format, each object contains the following fields:
            - start: Original video clip start time (number, in seconds)
            - end: Original video clip end time (number, in seconds)
            - screen_text: Text displayed on screen (string, emotional expression)
            - narration: TTS voiceover content (string, warm and touching narration)
            
            Please output the JSON array directly, without adding any prefix, suffix, or explanatory text.
            Reference example format: [{{"start": 5.0, "end": 10.0, "screen_text": "Those Beautiful Times", "narration": "Every ordinary moment holds the most precious memories"}}]
        """
    },
    
    "educational": {
        "zh": """根据以下视频分段信息，创作一个知识科普类的短视频脚本，总时长控制在15-30秒：
            视频分段信息如下：
            {video_segment_info_list}
            
            请从教育科普角度分析视频内容，生成有学习价值的脚本。要求：
            1. 提取视频中的知识点、技能或有趣现象
            2. 用通俗易懂的语言解释专业概念
            3. 适合科普类视频：实验演示、技能教学、自然现象、历史文化、科技产品等
            4. 结构清晰：提出问题→解释原理→总结要点
            5. 语言严谨但不失趣味性
            6. 鼓励观众思考和学习
            7. 可以适当提出引发思考的问题
            
            **重要：请严格按照JSON格式输出，不要包含任何其他文字、解释或markdown标记**
            
            输出JSON数组格式，每个对象包含以下字段：
            - start: 原视频裁切开始时间（数字，单位秒）
            - end: 原视频裁切结束时间（数字，单位秒）
            - screen_text: 显示在屏幕上的文字（字符串，知识要点或关键词）
            - narration: TTS旁白内容（字符串，科普解说）
            
            请直接输出JSON数组，不要添加任何前缀、后缀或解释文字。
            参照示例格式：[{{"start": 3.0, "end": 8.0, "screen_text": "科学原理", "narration": "你知道这背后的科学原理吗？让我来为你揭秘"}}]
        """,
        "en": """Based on the following video segment information, create an educational short video script with a total duration of 15-30 seconds:
            Video segment information:
            {video_segment_info_list}
            
            Please analyze the video content from an educational perspective and generate a learning-valuable script. Requirements:
            1. Extract knowledge points, skills, or interesting phenomena from the video
            2. Explain professional concepts in easy-to-understand language
            3. Suitable for educational videos: experiment demonstrations, skill tutorials, natural phenomena, history and culture, tech products, etc.
            4. Clear structure: raise question → explain principle → summarize key points
            5. Language should be rigorous but interesting
            6. Encourage audience to think and learn
            7. Can appropriately raise thought-provoking questions
            
            **Important: Please output strictly in JSON format, without any other text, explanations, or markdown markers**
            
            Output JSON array format, each object contains the following fields:
            - start: Original video clip start time (number, in seconds)
            - end: Original video clip end time (number, in seconds)
            - screen_text: Text displayed on screen (string, knowledge points or keywords)
            - narration: TTS voiceover content (string, educational explanation)
            
            Please output the JSON array directly, without adding any prefix, suffix, or explanatory text.
            Reference example format: [{{"start": 3.0, "end": 8.0, "screen_text": "Scientific Principle", "narration": "Do you know the scientific principle behind this? Let me reveal it for you"}}]
        """
    },
    
    "entertaining": {
        "zh": """根据以下视频分段信息，创作一个轻松娱乐的短视频脚本，总时长控制在15-30秒：
            视频分段信息如下：
            {video_segment_info_list}
            
            请从娱乐角度分析视频内容，生成有趣幽默的脚本。要求：
            1. 挖掘视频中的搞笑元素、意外瞬间或有趣细节
            2. 使用幽默、轻松的语调
            3. 适合娱乐类视频：搞笑日常、宠物趣事、意外状况、模仿表演、游戏娱乐等
            4. 可以适当夸张和调侃，但要保持善意
            5. 节奏要轻快，符合娱乐视频的特点
            6. 可以使用网络流行语或梗，但要适度
            7. 结尾要有笑点或惊喜
            
            **重要：请严格按照JSON格式输出，不要包含任何其他文字、解释或markdown标记**
            
            输出JSON数组格式，每个对象包含以下字段：
            - start: 原视频裁切开始时间（数字，单位秒）
            - end: 原视频裁切结束时间（数字，单位秒）
            - screen_text: 显示在屏幕上的文字（字符串，搞笑文案或表情）
            - narration: TTS旁白内容（字符串，幽默解说）
            
            请直接输出JSON数组，不要添加任何前缀、后缀或解释文字。
            参照示例格式：[{{"start": 2.0, "end": 7.0, "screen_text": "哈哈哈哈", "narration": "这也太搞笑了吧，我都要笑出腹肌了"}}]
        """,
        "en": """Based on the following video segment information, create a light and entertaining short video script with a total duration of 15-30 seconds:
            Video segment information:
            {video_segment_info_list}
            
            Please analyze the video content from an entertainment perspective and generate a funny and humorous script. Requirements:
            1. Discover funny elements, unexpected moments, or interesting details in the video
            2. Use humorous and relaxed tone
            3. Suitable for entertainment videos: funny daily life, pet antics, unexpected situations, imitation performances, gaming entertainment, etc.
            4. Can be appropriately exaggerated and teasing, but maintain goodwill
            5. Rhythm should be brisk, fitting entertainment video characteristics
            6. Can use internet slang or memes, but moderately
            7. Ending should have a punchline or surprise
            
            **Important: Please output strictly in JSON format, without any other text, explanations, or markdown markers**
            
            Output JSON array format, each object contains the following fields:
            - start: Original video clip start time (number, in seconds)
            - end: Original video clip end time (number, in seconds)
            - screen_text: Text displayed on screen (string, funny copy or expressions)
            - narration: TTS voiceover content (string, humorous commentary)
            
            Please output the JSON array directly, without adding any prefix, suffix, or explanatory text.
            Reference example format: [{{"start": 2.0, "end": 7.0, "screen_text": "Hahaha", "narration": "This is so hilarious, I'm about to laugh my abs out"}}]
        """
    },
    
    "inspirational": {
        "zh": """根据以下视频分段信息，创作一个励志激励的短视频脚本，总时长控制在15-30秒：
            视频分段信息如下：
            {video_segment_info_list}
            
            请从励志角度分析视频内容，生成正能量满满的脚本。要求：
            1. 挖掘视频中的奋斗精神、坚持不懈、突破自我等元素
            2. 传递积极向上的价值观和人生态度
            3. 适合励志类视频：运动健身、学习成长、工作奋斗、克服困难、追求梦想等
            4. 语言要有力量感和感召力
            5. 可以引用名言警句或人生感悟
            6. 鼓励观众行动起来，追求更好的自己
            7. 结尾要有升华和激励效果
            
            **重要：请严格按照JSON格式输出，不要包含任何其他文字、解释或markdown标记**
            
            输出JSON数组格式，每个对象包含以下字段：
            - start: 原视频裁切开始时间（数字，单位秒）
            - end: 原视频裁切结束时间（数字，单位秒）
            - screen_text: 显示在屏幕上的文字（字符串，励志标语或金句）
            - narration: TTS旁白内容（字符串，激励性解说）
            
            请直接输出JSON数组，不要添加任何前缀、后缀或解释文字。
            参照示例格式：[{{"start": 1.0, "end": 6.0, "screen_text": "永不放弃", "narration": "每一次的坚持，都是在为梦想铺路，你准备好了吗？"}}]
        """,
        "en": """Based on the following video segment information, create an inspirational and motivational short video script with a total duration of 15-30 seconds:
            Video segment information:
            {video_segment_info_list}
            
            Please analyze the video content from an inspirational perspective and generate a positive energy script. Requirements:
            1. Discover elements of fighting spirit, perseverance, self-breakthrough, etc. in the video
            2. Convey positive values and life attitudes
            3. Suitable for inspirational videos: sports and fitness, learning and growth, work struggle, overcoming difficulties, pursuing dreams, etc.
            4. Language should be powerful and inspiring
            5. Can quote famous sayings or life insights
            6. Encourage audience to take action and pursue a better self
            7. Ending should have elevation and motivational effect
            
            **Important: Please output strictly in JSON format, without any other text, explanations, or markdown markers**
            
            Output JSON array format, each object contains the following fields:
            - start: Original video clip start time (number, in seconds)
            - end: Original video clip end time (number, in seconds)
            - screen_text: Text displayed on screen (string, inspirational slogans or golden quotes)
            - narration: TTS voiceover content (string, motivational commentary)
            
            Please output the JSON array directly, without adding any prefix, suffix, or explanatory text.
            Reference example format: [{{"start": 1.0, "end": 6.0, "screen_text": "Never Give Up", "narration": "Every persistence is paving the way for dreams. Are you ready?"}}]
        """
    },
    
    "aesthetic": {
        "zh": """根据以下视频分段信息，创作一个美学艺术的短视频脚本，总时长控制在15-30秒：
            视频分段信息如下：
            {video_segment_info_list}
            
            请从美学角度分析视频内容，生成富有艺术感的脚本。要求：
            1. 关注视频的视觉美感：色彩、构图、光影、质感等
            2. 挖掘画面的艺术价值和美学意境
            3. 适合美学类视频：风景摄影、艺术创作、时尚穿搭、建筑设计、手工制作等
            4. 使用优美、诗意的语言
            5. 可以引用艺术理论或美学概念
            6. 培养观众的审美情趣
            7. 营造沉浸式的美学体验
            
            **重要：请严格按照JSON格式输出，不要包含任何其他文字、解释或markdown标记**
            
            输出JSON数组格式，每个对象包含以下字段：
            - start: 原视频裁切开始时间（数字，单位秒）
            - end: 原视频裁切结束时间（数字，单位秒）
            - screen_text: 显示在屏幕上的文字（字符串，美学词汇或诗意表达）
            - narration: TTS旁白内容（字符串，优美的艺术解说）
            
            请直接输出JSON数组，不要添加任何前缀、后缀或解释文字。
            参照示例格式：[{{"start": 4.0, "end": 9.0, "screen_text": "光影之美", "narration": "光与影的交织，诉说着时间的诗意，每一帧都是艺术的呈现"}}]
        """,
        "en": """Based on the following video segment information, create an aesthetic and artistic short video script with a total duration of 15-30 seconds:
            Video segment information:
            {video_segment_info_list}
            
            Please analyze the video content from an aesthetic perspective and generate an artistic script. Requirements:
            1. Focus on visual beauty of the video: color, composition, light and shadow, texture, etc.
            2. Discover artistic value and aesthetic mood of the frames
            3. Suitable for aesthetic videos: landscape photography, artistic creation, fashion styling, architectural design, handicrafts, etc.
            4. Use beautiful and poetic language
            5. Can quote art theory or aesthetic concepts
            6. Cultivate audience's aesthetic taste
            7. Create immersive aesthetic experience
            
            **Important: Please output strictly in JSON format, without any other text, explanations, or markdown markers**
            
            Output JSON array format, each object contains the following fields:
            - start: Original video clip start time (number, in seconds)
            - end: Original video clip end time (number, in seconds)
            - screen_text: Text displayed on screen (string, aesthetic vocabulary or poetic expression)
            - narration: TTS voiceover content (string, beautiful artistic commentary)
            
            Please output the JSON array directly, without adding any prefix, suffix, or explanatory text.
            Reference example format: [{{"start": 4.0, "end": 9.0, "screen_text": "Beauty of Light and Shadow", "narration": "The interweaving of light and shadow tells the poetry of time, every frame is an artistic presentation"}}]
        """
    },
    
    "trending": {
        "zh": """根据以下视频分段信息，创作一个热点话题的短视频脚本，总时长控制在15-30秒：
            视频分段信息如下：
            {video_segment_info_list}
            
            请从热点话题角度分析视频内容，生成紧跟潮流的脚本。要求：
            1. 结合当下热门话题、流行趋势或社会现象
            2. 使用网络流行语、热梗或时下流行的表达方式
            3. 适合热点类视频：社会现象、流行文化、网络热点、时事评论、潮流趋势等
            4. 语言要新潮、有活力，符合年轻人的表达习惯
            5. 可以适当蹭热点，但要与视频内容相关
            6. 引发观众的讨论和互动
            7. 保持敏锐的时代感和话题性
            
            **重要：请严格按照JSON格式输出，不要包含任何其他文字、解释或markdown标记**
            
            输出JSON数组格式，每个对象包含以下字段：
            - start: 原视频裁切开始时间（数字，单位秒）
            - end: 原视频裁切结束时间（数字，单位秒）
            - screen_text: 显示在屏幕上的文字（字符串，热点词汇或流行语）
            - narration: TTS旁白内容（字符串，紧跟潮流的解说）
            
            请直接输出JSON数组，不要添加任何前缀、后缀或解释文字。
            参照示例格式：[{{"start": 0.5, "end": 5.5, "screen_text": "这就是传说中的...", "narration": "兄弟们，这波操作我直接看呆了，这不就是最近很火的那个吗？"}}]
        """,
        "en": """Based on the following video segment information, create a trending topic short video script with a total duration of 15-30 seconds:
            Video segment information:
            {video_segment_info_list}
            
            Please analyze the video content from a trending topic perspective and generate a script that follows current trends. Requirements:
            1. Combine current hot topics, popular trends, or social phenomena
            2. Use internet slang, hot memes, or currently popular expressions
            3. Suitable for trending videos: social phenomena, pop culture, internet hotspots, current affairs commentary, fashion trends, etc.
            4. Language should be trendy and energetic, fitting young people's expression habits
            5. Can appropriately ride on hot topics, but must be relevant to video content
            6. Trigger audience discussion and interaction
            7. Maintain sharp sense of the times and topicality
            
            **Important: Please output strictly in JSON format, without any other text, explanations, or markdown markers**
            
            Output JSON array format, each object contains the following fields:
            - start: Original video clip start time (number, in seconds)
            - end: Original video clip end time (number, in seconds)
            - screen_text: Text displayed on screen (string, trending vocabulary or popular phrases)
            - narration: TTS voiceover content (string, trend-following commentary)
            
            Please output the JSON array directly, without adding any prefix, suffix, or explanatory text.
            Reference example format: [{{"start": 0.5, "end": 5.5, "screen_text": "This is the legendary...", "narration": "Guys, this operation left me stunned, isn't this the thing that's been trending recently?"}}]
        """
    },
    
    "lifestyle": {
        "zh": """根据以下视频分段信息，创作一个生活方式的短视频脚本，总时长控制在15-30秒：
            视频分段信息如下：
            {video_segment_info_list}
            
            请从生活方式角度分析视频内容，生成贴近日常的脚本。要求：
            1. 关注日常生活的美好瞬间和实用技巧
            2. 分享生活经验、小窍门或生活态度
            3. 适合生活类视频：美食制作、居家整理、穿搭分享、旅行记录、日常vlog等
            4. 语言亲切自然，像朋友间的分享
            5. 提供实用价值或生活灵感
            6. 营造温馨、舒适的生活氛围
            7. 鼓励观众享受生活、热爱生活
            
            **重要：请严格按照JSON格式输出，不要包含任何其他文字、解释或markdown标记**
            
            输出JSON数组格式，每个对象包含以下字段：
            - start: 原视频裁切开始时间（数字，单位秒）
            - end: 原视频裁切结束时间（数字，单位秒）
            - screen_text: 显示在屏幕上的文字（字符串，生活小贴士或温馨话语）
            - narration: TTS旁白内容（字符串，亲切的生活分享）
            
            请直接输出JSON数组，不要添加任何前缀、后缀或解释文字。
            参照示例格式：[{{"start": 3.5, "end": 8.5, "screen_text": "生活小妙招", "narration": "分享一个我最近发现的生活小技巧，真的超级实用哦"}}]
        """,
        "en": """Based on the following video segment information, create a lifestyle short video script with a total duration of 15-30 seconds:
            Video segment information:
            {video_segment_info_list}
            
            Please analyze the video content from a lifestyle perspective and generate a daily life-oriented script. Requirements:
            1. Focus on beautiful moments and practical tips in daily life
            2. Share life experiences, tips, or life attitudes
            3. Suitable for lifestyle videos: food preparation, home organization, outfit sharing, travel records, daily vlogs, etc.
            4. Language should be friendly and natural, like sharing between friends
            5. Provide practical value or life inspiration
            6. Create warm and comfortable life atmosphere
            7. Encourage audience to enjoy and love life
            
            **Important: Please output strictly in JSON format, without any other text, explanations, or markdown markers**
            
            Output JSON array format, each object contains the following fields:
            - start: Original video clip start time (number, in seconds)
            - end: Original video clip end time (number, in seconds)
            - screen_text: Text displayed on screen (string, life tips or warm words)
            - narration: TTS voiceover content (string, friendly life sharing)
            
            Please output the JSON array directly, without adding any prefix, suffix, or explanatory text.
            Reference example format: [{{"start": 3.5, "end": 8.5, "screen_text": "Life Hack", "narration": "Let me share a life tip I recently discovered, it's really super useful"}}]
        """
    },
    
    "professional": {
        "zh": """根据以下视频分段信息，创作一个专业技能的短视频脚本，总时长控制在15-30秒：
            视频分段信息如下：
            {video_segment_info_list}
            
            请从专业技能角度分析视频内容，生成具有专业价值的脚本。要求：
            1. 突出视频中的专业技能、工艺流程或技术要点
            2. 用专业但易懂的语言解释技术细节
            3. 适合专业类视频：技能演示、工艺制作、技术教学、职场技巧、专业知识等
            4. 体现专业性和权威性
            5. 提供有价值的专业见解或技巧
            6. 激发观众的学习兴趣和专业追求
            7. 可以分享行业经验或专业心得
            
            **重要：请严格按照JSON格式输出，不要包含任何其他文字、解释或markdown标记**
            
            输出JSON数组格式，每个对象包含以下字段：
            - start: 原视频裁切开始时间（数字，单位秒）
            - end: 原视频裁切结束时间（数字，单位秒）
            - screen_text: 显示在屏幕上的文字（字符串，专业术语或关键技巧）
            - narration: TTS旁白内容（字符串，专业解说）
            
            请直接输出JSON数组，不要添加任何前缀、后缀或解释文字。
            参照示例格式：[{{"start": 2.0, "end": 7.0, "screen_text": "核心技巧", "narration": "这个步骤是整个流程的关键，注意手法的精准度和时机把握"}}]
        """,
        "en": """Based on the following video segment information, create a professional skill short video script with a total duration of 15-30 seconds:
            Video segment information:
            {video_segment_info_list}
            
            Please analyze the video content from a professional skill perspective and generate a professionally valuable script. Requirements:
            1. Highlight professional skills, craft processes, or technical points in the video
            2. Use professional but understandable language to explain technical details
            3. Suitable for professional videos: skill demonstrations, craft making, technical teaching, workplace skills, professional knowledge, etc.
            4. Demonstrate professionalism and authority
            5. Provide valuable professional insights or techniques
            6. Inspire audience's learning interest and professional pursuit
            7. Can share industry experience or professional insights
            
            **Important: Please output strictly in JSON format, without any other text, explanations, or markdown markers**
            
            Output JSON array format, each object contains the following fields:
            - start: Original video clip start time (number, in seconds)
            - end: Original video clip end time (number, in seconds)
            - screen_text: Text displayed on screen (string, professional terms or key techniques)
            - narration: TTS voiceover content (string, professional commentary)
            
            Please output the JSON array directly, without adding any prefix, suffix, or explanatory text.
            Reference example format: [{{"start": 2.0, "end": 7.0, "screen_text": "Core Technique", "narration": "This step is the key to the entire process, pay attention to the precision of technique and timing"}}]
        """
    },
    
    "storytelling": {
        "zh": """根据以下视频分段信息，创作一个故事叙述的短视频脚本，总时长控制在15-30秒：
            视频分段信息如下：
            {video_segment_info_list}
            
            请从故事叙述角度分析视频内容，生成具有故事性的脚本。要求：
            1. 构建完整的故事结构：开端、发展、高潮、结局
            2. 挖掘视频中的戏剧冲突或转折点
            3. 适合故事类视频：生活故事、成长经历、意外事件、人物传记、情感故事等
            4. 使用生动的叙述语言，营造画面感
            5. 注重情节的紧凑性和吸引力
            6. 可以设置悬念或反转
            7. 结尾要有意义或启发性
            
            **重要：请严格按照JSON格式输出，不要包含任何其他文字、解释或markdown标记**
            
            输出JSON数组格式，每个对象包含以下字段：
            - start: 原视频裁切开始时间（数字，单位秒）
            - end: 原视频裁切结束时间（数字，单位秒）
            - screen_text: 显示在屏幕上的文字（字符串，故事标题或关键情节）
            - narration: TTS旁白内容（字符串，故事叙述）
            
            请直接输出JSON数组，不要添加任何前缀、后缀或解释文字。
            参照示例格式：[{{"start": 1.5, "end": 6.5, "screen_text": "故事开始", "narration": "那是一个平凡的下午，没人想到接下来会发生什么..."}}]
        """,
        "en": """Based on the following video segment information, create a storytelling short video script with a total duration of 15-30 seconds:
            Video segment information:
            {video_segment_info_list}
            
            Please analyze the video content from a storytelling perspective and generate a narrative script. Requirements:
            1. Build complete story structure: beginning, development, climax, ending
            2. Discover dramatic conflicts or turning points in the video
            3. Suitable for story videos: life stories, growth experiences, unexpected events, character biographies, emotional stories, etc.
            4. Use vivid narrative language to create visual imagery
            5. Focus on plot compactness and appeal
            6. Can set suspense or plot twists
            7. Ending should be meaningful or inspiring
            
            **Important: Please output strictly in JSON format, without any other text, explanations, or markdown markers**
            
            Output JSON array format, each object contains the following fields:
            - start: Original video clip start time (number, in seconds)
            - end: Original video clip end time (number, in seconds)
            - screen_text: Text displayed on screen (string, story title or key plot)
            - narration: TTS voiceover content (string, story narration)
            
            Please output the JSON array directly, without adding any prefix, suffix, or explanatory text.
            Reference example format: [{{"start": 1.5, "end": 6.5, "screen_text": "Story Begins", "narration": "It was an ordinary afternoon, no one expected what would happen next..."}}]
        """
    }
}