# default prompt
DEFAULT_PROMPT = {
    "role_desc": {
        "zh": """你是一个专业的视频编辑。""",
        "en": """You are a professional video editor."""
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
    }
}