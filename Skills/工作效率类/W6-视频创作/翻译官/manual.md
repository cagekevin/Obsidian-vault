---
name: translator
description: 翻译官——storyboard → 英文提示词 的无缝翻译管线。提炼角色、保证格式绝对正确、过滤幻觉源、强制资产隔离、全自动静默导出。
---

## 自检清单（导出前逐项过）
        □ elements 里每个元素是否都有 name / english_name / appearance / is_background
        □ 非参考元素是否标记了 `reference: false`（不标记则默认出参考图）
        □ `reference: false` 的元素是否确实是材质变体/内部零件/单组专用角色/单次道具
        □ 出镜 ≥ 2 次的元素是否都列进了 elements
        □ 只出现 1 次的元素是否没进 elements
        □ 每个 group 的 element_refs 是否只列出了本组场景中实际出镜的元素
        □ element_refs 中的每个元素是否在本组至少一个 scene 的 description 中出现或可被合理推断
        □ 如果 storyboard 有 Archetype 分组表，分组是否严格遵循
        □ 每组 scene 数量是否 ≤ 5 个（估算时长 ≤ 13s）
        □ 每组里的 Scene 编号是否连续、不跳序
        □ 所有背景描述是否不含角色物体
        □ 所有角色描述是否不含环境光影
        □ 有没有残留的中文（"友好的"、"高大上"）——QC 报告会自动检测此项
        □ 有没有残留的具体作品名（Inside Out / Kurzgesagt）
        □ **修改 scene description 后，逐词对比原版，确认没有丢失关键视觉细节**（如绿光、same frame构图、关键词弹出等——写新描述时容易只想着"改什么"而忘了"保留什么"）
        □ **description 中有跨镜引用（scene \d+）的 scene，是否写了 storyboard_desc**——没有的话 QC 会报 error 阻止导出
        □ **有没有使用 HDR/8K/超高清/高细节/锐利/ultra sharp 等过锐堆料词**——QC 报告也会自动检测并给出警告
        □ **description 中是否写了技术说明或后期操作**（如"这个画面要跟 X 镜接"、"后期用剪映叠加"、"key 光参数"）——只写当前画面可见的东西，不写制作指示
        □ **同一组内相邻镜头的 camera 是否大幅跳跃**——文戏场景不应频繁切换焦段

[七条铁律]

    1. 提炼角色与资产绝对隔离
        把 storyboard 里需要出参考图的复用视觉资产全部抓出来，列进 elements 数组。
        **必须保持物理分离**：当 `is_background: true` 时，环境描述中严禁出现任何角色或非环境的主体物件；当 `is_background: false` 时，角色外观描述中严禁混入环境光影或背景设定。

    2. 画面一致性
        同一个元素在不同 Scene 里的外观描述必须**完全一致**。
        不能 Scene 1 写 "golden sphere"，Scene 4 写 "golden star-shaped"。
        elements 数组里的 appearance 是所有画面的基准——所有 Scene 里的描述要跟 appearance 对得上，不能矛盾。

    3. 格式不走样
        严格锁定 project-template.json 的原有字段，**严禁自定义新字段**。
        elements 里只保留 name / english_name / appearance / is_background / reference。
        storyboard_groups 里每个 group 需包含 element_refs（本组场景实际出镜的 element name 列表）。
        storyboard_groups 里每个 scene 只保留 scene_num / title / description / storyboard_desc / camera。
        每个 scene 的 description 可以有跨镜引用（"same as scene 09"），但必须补一句 storyboard_desc 给故事板用。
        storyboard_desc 是独立描述，不自称"与 scene X 相同"，必须是完整的画面。

    4. 过滤幻觉源
        这条是重点——分三类处理：

        ✅ 允许保留：通用风格类 + "style" / "-like" 后缀
        "Pixar style 3D animation" → 允许（渲染风格，AI 能准确理解）
        "rounded expressive 3D animation style" → 允许
        "claymation style" → 允许
        "Octane render" / "Redshift" / "RenderMan" / "Arnold" → 允许（渲染器名称，不影响画面内容）
        
        ❌ 必须删掉：具体角色名称（防止模型画出原有角色或Logo）
        "Inside Out" → 删
        "Kurzgesagt" → 删
        "Apple Keynote" → 删
        "Nintendo" → 删
        "Disney" → 删
        
        ⚠️ 替换方式：不说作品名，说它代表的视觉特性
        "Inside Out" → "emotionally expressive soft rounded 3D characters"
        "Kurzgesagt" → "flat 3D scientific visualization with clean geometric forms"
        "Apple Keynote" → "minimal presentation layout with large typography"

    5. 保留视觉细节密度
        scene description 翻译时必须保留原文的视觉细节量。
        原文写"金色粒子缓慢飘落，嫩绿色卷须轻柔环绕" →
        "golden particles slowly drifting down, delicate green tendrils gently wrapping around"
        不能压缩成 "golden particles with tendrils"。
        描述的长度 = 信息量，不要替用户做减法。

    6. 不瞎编，只润色
        原文写了什么就翻译什么，不创造原文没有的信息。
        原文没有 hex → 不写 hex；原文没说材质 → 不补材质描述。

        但为了英文通顺可以加：
            - 冠词：the / a / an
            - 介词：around / from / with / in / through
            - 连词：and / with / while
            - 时态词：-ing / -ed
            这些不创造新内容，只让句子读起来像人写的。

        关于 visual_style：必须从 storyboard 原文中提取或由用户/风格文件明确指定。
        若 storyboard 原文没有视觉风格描述，且用户没有提供风格文件，则在 project.json
        中将 visual_style 留空 "[]"，由用户自行填写。严禁 AI 推断或编造视觉风格。

    7. project.json 纯净输出
        翻译完成后只输出 project.json，不得在 JSON 外部附加任何解释文字。
        若某 Scene 的描述里没有明确背景，从 Scene description 的上文推断补全，
        不要留空。

[分镜板生成规则——storyboard board prompt 构成]

    导出脚本 export.py 按以下规则生成分镜板 prompt：

    1. 摄像机运动不在 Frame 中独立存在
       每个 Frame 的描述是**正文的一部分**，描述中已自然包含摄像机运动
       （如"gently rotates"、"slowly drifting down"、"fades into"）。
       **严禁**在 Frame 末尾附加 "Camera: {cam}" 标签——摄像机信息已融入描述正文。

    2. camera 字段的用途
       camera 字段（如 "Medium · Slow push · Eye level"）只用于：
       - 全片总览的 SCENE TOP-DOWN DIAGRAM 中的镜头路径标注
       - 图片单帧 prompt（image-shot-xx.txt）中的单独 CAMERA 行
       不分镜板 Frame 中重复出现。

    3. SCENE TOP-DOWN DIAGRAM — 画俯视摄像机路线图，不是写文字标注
       放在 ENVIRONMENT REFERENCE 下方，紧凑区域。指令格式：
       ```
       SECTION 3 - SCENE DESIGN (below character panel, compact):
       Top-down floor plan view of camera path.
       Camera arc: '{title1} → {title2} → ... → {titleN}'
       Dotted line with directional arrows connecting shot positions.
       Shot numbers labeled at each camera position.
       ```
       让 AI 画出带箭头和虚线的俯视路线图，而不是写一行纯文字。
       全片总览改用各组 label 串联：`'源起之地 → 古老契约 → 山野到实验室'`
       无 title 字段时降级为纯编号范围。

    4. title 字段用于分镜板 Frame 标注和 TOP BAR
       每个 Frame 格式：
       `Frame 01: 'Shot 01 — 胶囊悬浮发光. Kelly standing in front of mountains...'`
       即 `Shot {num} — {title}. {description}`。
       
       TOP BAR 格式：
       `'4 组分镜（胶囊悬浮发光→符号浮现→金光闪烁→淡入阳光浴室）'`
       即 `'{num}镜：{group_label}（{title1}→{title2}→...）'`
       
       无 title 字段时降级为：
       `Frame 01: '{description}'`（去掉 Shot 前缀）

[视觉风格预设——按需加载]

    触发条件：
        - 用户明确要求换风格、试风格、生成某个风格版本；
        - 用户对当前视觉效果不满意；
        - storyboard/project.json 没有明确 visual_style，且用户希望从预设中选择。

    若用户已经明确指定预设 key，直接读取 `styles/styles.json` 中对应预设。
    若用户只说"换个风格"或"更电影/更动画/更真实"，先展示 3-5 个最匹配选项，
    等用户选择后再执行。

    每个预设包含：
        - visual_style：进入 prompt 的总体风格语言
        - accent_color：色系描述，可为空，不写 hex
        - camera_language：shot_types / movement / composition / lighting_story
        - description_language：角色、物体、环境、运动的描述规范

    可用预设 key：
        - `pixar` — 圆润 expressive 3D 动画；适合角色故事，不适合真实人物/纯产品。
        - `lyrical-realism` — 诗意纪实；适合人物故事、自然、生活方式。
        - `pro-cinematic` — 专业电影；通用性强，适合叙事和产品展示。
        - `natgeo-documentary` — 自然纪录片；适合自然风光、户外、环境叙事。
        - `stop-motion` — 定格动画；适合手工感、微缩布景、触觉材质。
        - `traditional-2d-anime` — 传统二维动画；适合角色驱动、手绘背景。
        - `product-hero-cinematic` — 产品英雄广告；适合产品、液体、微距 B-roll。
        - `action-handheld` — 动态手持；适合运动、户外、动作场景。
        - `streaming-prestige` — 精品剧集；适合现代剧情、对话、人物驱动。
        - `sunlit-lifestyle` — 阳光生活方式；适合居家、日常、轻商业。
        - `hollywood-epic` — 大片史诗；适合大场面、冲突、戏剧张力。
        - `selfie-vlog` — 自拍 Vlog；适合第一人称、创作者口吻、真实记录。
        - `micro-cosmos` — 3D 微观宇宙；适合科技、生物、成分可视化。

    预设 key 只是内部标签。写入 project.json / prompt 时，必须使用
    styles.json 中的通用视觉描述，不要把具体品牌、作品、角色、Logo 写进 prompt。

[切换风格操作步骤]

    切换风格不是替换 visual_style 一行，而是从同一份纯叙事重新生成一套
    project_{风格名}.json。必须同时重写：
        - visual_style
        - accent_color
        - elements[].appearance
        - scenes[].description
        - scenes[].camera

    **步骤① 准备 story-narrative.json**
    优先使用 storyboard.md 或已有 story-narrative.json 提取纯叙事。
    如果没有 story-narrative.json，则从当前 project.json 提取：
        - 保留"谁 + 在哪里 + 做什么/发生什么"
        - 剥离镜头运动、光线、材质、渲染、风格词
        - 按 `templates/story-narrative.json` 输出到 storyboard 同级目录

    注意：提取纯叙事时只做减法，不新增剧情，不补不存在的动作。

    **步骤② 确定目标风格**
    从 `styles/styles.json` 读取目标预设的全部字段。
    若用户没有明确指定风格，只展示最匹配的 3-5 个预设让用户选。

    **步骤③ 确定 accent_color**
    如果预设已有 accent_color，直接使用其色系描述。
    如果预设 accent_color 为空，询问用户色系方向，例如：
        `"调色板用什么色系？比如暖金色调 / 森绿色系 / 冷白+琥珀"`
    用户确认后写入 `project_{风格名}.json`，只写英文色系描述，不编造 hex。

    **步骤④ 按风格体系重写 project**
    从 story-narrative.json 出发，用目标风格的 camera_language 和
    description_language 重新翻译所有 elements 与 scenes。
    不只是换词汇，而是按目标风格重做镜头设计、材质语言、环境语言和运动语言。

    七个维度都要对齐：
        - 镜头类型：shot_types
        - 摄像机运动：movement
        - 构图：composition
        - 光线叙事：lighting_story
        - 人物/主体语言：description_language
        - 物体/材质语言：description_language
        - 环境/空间语言：description_language

    **camera 字段必须重写**，不能沿用旧风格的 camera。

    **camera 字段融合规则**（从 styles.json 的 camera_language 合并为 scene.camera 的一个字符串）：
        从四个子字段各选 1 个最匹配当前画面的元素，按以下顺序组合为一句：
        `[shot_type] · [movement] · [composition]`
        例如：`"Medium close-up · Slow push · Low angle hero shot"`
        lighting_story 不进入 scene.camera，它用于单帧/视频 prompt 中的光线描述。
        如果 scene 是对话/静态镜头，composition 优先于 shot_type 和 movement。

    scene description 中也要自然包含可拍到的运动，但不要在分镜板 Frame 末尾
    额外附加 Camera 标签。

    **步骤⑤ 另存为 project_{风格名}.json**
    不覆盖原 project.json。风格名用 styles/styles.json 中的 key：
        - project_pixar.json
        - project_pro-cinematic.json
        - project_product-hero-cinematic.json

    **步骤⑥ 重跑导出并生成 HTML**
    运行：
        `python3 export.py [项目目录] --input project_{风格名}.json --html`

    导出脚本会输出到 `output_{风格名}/`，不覆盖原 output/。
    用户通过 HTML 工作台查看故事版、图片单帧、视频镜头、参考图、QC 和资产索引。

    确认规则：
        - 需要用户确认：目标风格不明确、accent_color 为空、用户要求多风格对比。
        - 不需要用户确认：提取 story-narrative.json、生成 project_{风格名}.json、
          运行 export.py 导出 HTML。

[翻译纪律——分项对照]

    | 字段 | 语言 | 说明 |
    |------|------|------|
    | element name | **中文** | 用户看的，不进 prompt，用于文件名和中文说明 |
    | element english_name | **英文** | 进画面 prompt，必须和 Frame description 里的叫法一致 |
    | element appearance | 英文 | 进画面 prompt |
    | scene title | **中文** | 4-6字概括画面动作/内容，用于分镜板 Frame 标注和 TOP BAR |
    | scene description | 英文 | 进画面 prompt |
    | camera | 英文 | 进画面 prompt |
    | label (分组名) | 中文 | 用户看的，不进画面 prompt |
    | visual_style | 英文 | 进画面 prompt |
    | accent_color | 英文（色系描述，不写 hex 码） | 进画面 prompt |

[输出结构]
    W6-视频创作/翻译官/
    ├── SKILL.md
    ├── export.py
    ├── styles/
    │   └── styles.json
    ├── templates/
    │   ├── project-template.json
    │   └── story-narrative.json
    └── examples/
        └── sample-storyboard/
            └── storyboard.md       ← 测试用样例分镜，首次使用可复制到项目目录运行

[活性检测——QC 报告新增检查]
    export.py 的 QC 报告在原有检查基础上新增两项：

    11. **术语一致性检查**
        自动扫描每个 element 的 english_name，比对它在不同 Scene 的 description
        中是否被一致引用。如果某 Scene 用了同义词/变体而不是 english_name 的
        核心词，QC 会报 Warning。
        例如：english_name 是 "capsule"，但某 Scene 描述中写的是 "the pill"
        或 "the white object"——标记出来供人工修正。

    12. **描述压缩率检测**
        如果项目目录中存在 storyboard.md，自动读取其中文画面描述，
        与 project.json 中的英文 description 做字数对比。
        若英文单词数远少于按中文字数折算的期望值（比率 < 50%），
        标记为"可能丢失视觉细节"。
        折算标准：1 个中文字 ≈ 1.8 个英文词。
        注意：这依赖于 storyboard.md 的存在及其格式规范性，若找不到
        storyboard.md 则跳过此项检查。

[导出产物说明]
    export.py 当前默认导出七类资产：
        1. 分组故事版 prompt：每组一个，用于生成图片故事版。
        2. 全片总览 prompt：把所有组串成一个总览板。
        3. 图片单帧 prompt（image-shot-xx.txt）：每个 Scene 一个，用于单独补图或重做某一镜。
        4. 视频镜头 prompt（video-shot-xx.txt）：每个 Scene 一个，用于图生视频或文生视频。
        5. 参考图 prompt：从 elements 生成角色概念表和环境概念表。
        6. QC 报告（qc-report.md）：自动检查 visual_style/accent_color/element 完整性/编号连续性/中文残留/品牌名/引用完整性。
        7. 资产索引（asset-index.md）：追踪每个角色/场景出现在哪些镜头和分组中。

    故事版 prompt 现包含 ENVIRONMENT REFERENCE，将本组出镜的背景元素单独列出。

    HTML 查看：
        使用 `python3 export.py [项目目录] --html` 时，HTML 按以下标签展示所有资产：
        故事版 | 全片总览 | 图片单帧 | 视频镜头 | 角色和场景 | 质检报告 | 资产索引 | 已生成图片
        
        复制按钮按类型自动适配：
        - 故事版/总览：[ COPY ]
        - 图片单帧：[ COPY IMAGE PROMPT ]
        - 视频镜头：[ COPY VIDEO PROMPT ]
        - 参考图：[ COPY REF PROMPT ]

    视频镜头 prompt 结构：
        VIDEO SHOT — Scene XX
        REFERENCE: [角色/场景参考图 + 对应 image-shot 锁定视觉]
        FIRST FRAME: [从 scene description 提取静态起始画面]
        ACTION: [主体动作描述]
        CAMERA MOTION: [来自 scene.camera]
        CONTINUITY: [跨镜头一致性约束]
        DURATION: 3 seconds
        AVOID: [避错约束]

    参考图 prompt 是一致性层，不是可有可无的附属产物。
    角色/主体使用 CHARACTER CONCEPT SHEET，背景使用 ENVIRONMENT CONCEPT SHEET。
    后续生成图片故事版时，应优先使用参考图来锁定角色、主体物件和复杂环境。

[脚本用法]
    python3 skills/工作效率类/W6-视频创作/翻译官/export.py [项目目录] --html
    脚本生成全部资产后自动打开 HTML 工作台。
