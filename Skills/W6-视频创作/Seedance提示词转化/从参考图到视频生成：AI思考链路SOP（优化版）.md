从参考图到视频生成：AI思考链路SOP（优化版）

⚡【必读核心】开始之前，你必须知道的3个真相

真相1：AI不会"理解"你的意图
❌ 你以为： "我说'产品要一模一样'，AI会理解我的意思，自动保持一致"
✅ 实际上： AI只会执行字面指令。如果你写了"no text"，它会删掉产品标签。因为它不会推理"产品标签是例外"。

💡 洞察：你的任务不是"描述你想要什么"，而是"设计AI的执行路径"

例子：
❌ 提示词："no text, no labels" → 结果：产品自带的标签也消失了
✅ 提示词："No additional text overlay. Preserve all original labels." → 结果：只禁止额外文字，保留产品标签

推导能力测试：用户说"不要有人"，但场景是"咖啡店"，AI会生成空荡荡的咖啡店吗？
→ 会。除非你说"a busy coffee shop with customers"
→ 原理：AI执行字面指令，不会补充"常识"

真相2：图片 vs 文字 = 注意力竞争
❌ 你以为： "我给了参考图，再用文字详细描述，AI会更清楚"
✅ 实际上：
参考图说："产品长这样"（精确的视觉样本）
文字说："金色盖子、透明瓶身..."（模糊的语言描述）
AI会混合两者 → 精确度下降

💡 洞察：当你有精确样本（参考图）时，让文字退位

文字只做两件事：
- 指向参考图（"must be IDENTICAL"）
- 列扫描清单（"material, shape, color"）

对比：
❌ "A transparent glass bottle with golden metal cap, containing golden capsules..." + 参考图
→ AI混合采样，细节不一致（颜色深浅、透明度、标签位置）

✅ "The product from the reference image must be IDENTICAL in every detail: - Material, texture, surface finish - Shape, proportions - Color, transparency - Internal contents - All original labels and text" + 参考图
→ AI 100%依赖参考图，只用文字做检查清单

为什么列维度有效？
"material, texture, shape, color"不是描述，是检查清单
AI会逐项对照参考图，这是在引导AI的注意力扫描路径

真相3：提示词的结构 = AI的优先级
❌ 你以为： "只要写在提示词里，AI就会照做"
✅ 实际上：
- 单独成段 = 重要
- 放在前面 = 优先
- 融入其他描述 = 次要

对比：
❌ 结构A："CORE ACTION: ... CAMERA MOVEMENT: ... ENVIRONMENT & STYLE: tropical beach..."
→ AI认为环境和动作同等重要 → 环境会抢占注意力

✅ 结构B："The camera captures the action on a tropical beach... [动作描述融入环境]"
→ AI认为环境是背景 → 动作是焦点

例子：如果要强调"产品必须一致"：
1. 放在最前面 2. 单独成段 3. 用大写或强调词（IDENTICAL, MUST）

💡 洞察：提示词的组织方式，比内容本身更重要。位置 + 格式 = 优先级信号

🎯 核心公式（记住这个就够了）
成功生成 = 精确约束（参考图 + IDENTICAL声明）+ 注意力引导（文字只列维度，不描述特征）+ 优先级设计（结构传递重要性）+ 显式声明（不依赖AI推理，声明所有例外）

⚠️ 最容易犯的3个错误
| 错误 | 后果 | 正确做法 |
|:---|:---|:---|
| 给了参考图，还详细描述特征 | 产品细节不一致 | 只列维度，不描述特征 |
| 写了"no text"，没说"preserve labels" | 产品标签消失 | 显式声明例外："Preserve original labels" |
| 4宫格没有全局约束声明 | 每个格子亮度/风格不一致 | 先声明全局规则："CONSISTENT ACROSS ALL PANELS" |

💡 记住：你不是在"描述画面"，你是在"编程AI的执行逻辑" 🧠✨

---

🔍【快速诊断】生成结果不符合预期？30秒定位问题

决策树
📸 生成的图片有问题？
↓
❓ 问题出在哪里？
┌─────────────────────────────────────┐
│ A. 产品相关                          │
│ B. 场景/光线/氛围相关                │
│ C. 技术参数（尺寸/质量）             │
│ D. 布局/构图相关                     │
└─────────────────────────────────────┘

A. 产品相关问题
├─ 产品形状完全不对
│  └─ 原因：参考图不清晰 / 没有用参考图
│     💊 解决：换高清参考图 + 确认已传入工具
│
├─ 产品形状对，但细节不对（颜色/透明度/标签位置）
│  └─ 原因：提示词描述了产品特征
│     💊 解决：删除所有特征描述，只列维度
│     📖 详见：§2.1 产品一致性公式
│     立即行动：
│     1. 搜索提示词中的产品描述（如"golden cap", "transparent bottle"）
│     2. 全部删除
│     3. 替换为维度清单：
│        "must be IDENTICAL in: - Material, texture, surface finish - Shape, proportions - Color, transparency - Internal contents - All original labels"
│
├─ 产品标签消失了
│  └─ 原因：写了"no text"但没声明例外
│     💊 解决："No additional text overlay. Preserve all original labels and text on the product."
│     立即行动：在提示词末尾加一段：
│     "IMPORTANT: No additional text overlay or graphic elements should be added. All original labels, text, and branding on the product must be preserved exactly."
│
└─ 多个面板中产品不一致
   └─ 原因：缺少全局约束声明
      💊 解决：在面板描述后，单独加一段全局约束
      📖 详见：§2.3 4宫格一致性公式
      立即行动：在所有PANEL描述之后，加：
      "CONSISTENT ELEMENTS ACROSS ALL PANELS:
      - Overall brightness level must be consistent
      - The product must be IDENTICAL in all panels where it appears
      - Color temperature must remain uniform"

B. 场景/光线/氛围问题
├─ 光线太冷/太暖/太强/太弱
│  └─ 原因：描述不够明确 / 用了模糊词汇
│     💊 解决：用分级描述
│     强度：soft / moderate / strong / dramatic
│     色温：cool white / neutral white / warm white / golden
│     方向：diffused / directional / backlit / side-lit
│     例子："Soft, diffused natural light with warm white color temperature"
│
├─ 场景风格不对（太写实/太梦幻/太平淡）
│  └─ 原因：参考图选择问题 / 风格描述冲突
│     💊 解决：1. 检查参考图是否匹配期望风格 2. 如果用双垫图，确认已用语言索引分离职责
│     立即行动：明确说明场景参考图的职责：
│     "Follow the visual style and composition approach from the second reference image: [列出要借鉴的具体元素：lighting, color palette, mood]"
│
└─ 构图不对（产品太小/位置不对/不够突出）
   └─ 原因：没有明确视觉权重
      💊 解决：加入尺寸和位置描述
      "The product is prominently sized, occupying significant visual space, clearly visible and acting as the dominant focal point"

C. 技术参数问题
├─ 尺寸不对（生成了2048x2048，但需要9:16）
│  └─ 原因：忘记传参数 / 参数写错
│     💊 解决：检查清单（每次生成前核对）
│     本项目默认参数：size: "1440x2560"  quality: "medium"
│     在调用工具前，明确写出并核对这些参数
│
└─ 画面模糊/质量差
   └─ 原因：质量参数设置错误 / 参考图本身质量差
      💊 解决：1. 确认 quality="medium" 2. 如果参考图模糊 → 换高清图 3. 如果生成后需要更高分辨率 → 用upscale工具

D. 布局/构图问题
├─ 4宫格的格子亮度不一致
│  └─ 原因：AI独立优化每个格子，缺少全局约束
│     💊 解决：详见 §2.3 4宫格一致性公式
│     立即行动：在面板描述后加：
│     "CONSISTENT ACROSS ALL PANELS: - Overall brightness level must be consistent"
│
└─ 4宫格的叙事不连贯
   └─ 原因：面板之间缺少因果关系 / 变化不明确
      💊 解决：检查每个面板是否有明确的"动作/变化"
      确保面板遵循"起承转合"：
      Panel 1: 建立场景（静态）
      Panel 2: 引入变化（动态开始）
      Panel 3: 高潮（最大变化）
      Panel 4: 结局（情绪升华）
      每个面板都要有明确的"新元素"或"状态改变"

🎯 快速修正策略总览
| 问题类型 | 立即行动 | 详细指南 |
|:---|:---|:---|
| 产品细节不对 | 删除提示词中的特征描述，只列维度 | §2.1 产品一致性公式 |
| 产品标签消失 | 加"No additional text. Preserve original labels." | §4.4 标签问题 |
| 多面板不一致 | 加全局约束段落（CONSISTENT ACROSS ALL PANELS） | §2.3 4宫格公式 |
| 光线不对 | 用分级描述重写（强度/色温/方向） | §4.3 光线问题 |
| 产品太小 | 加"prominently sized, dominant focal point" | §4.1 产品问题 |
| 尺寸不对 | 检查size参数：1440x2560 | §5 参数清单 |

💡 提示：90%的问题都是前3类（产品一致性、光线、参数）

🔄 诊断流程：
1. 用决策树定位问题类型（30秒）
2. 查看"立即行动"（1分钟修正）
3. 如果问题复杂，查看详细指南

---

🎬【实战演练】完整案例：从任务到生成

任务描述
用户说： "我想做一个4宫格，展示我的产品（金色胶囊瓶子）在海滩场景中，然后把4宫格做成10秒视频。"

用户提供：
- 产品图：金色胶囊瓶子（透明瓶身，金色盖子，内含金色胶囊）
- 场景参考图：某个海滩产品广告（梦幻风格，柔和光线）

Step 1: 分析任务
Q1: 哪些维度需要精确控制？
- 产品：必须100%一致（商业项目标准）
- 场景：可以变化，但要保持风格

Q2: 我有什么输入？
- 产品图（精确样本）
- 场景图（风格参考）

Q3: 这是什么类型的任务？
- 双垫图任务（产品 + 场景）
- 4宫格任务（需要全局一致性）
- 视频任务（需要先做关键帧）

✅ 决策：
- 用双垫图策略：第一张图=产品（一致性约束），第二张图=场景（风格参考）
  原因：真相2 → 图 vs 文字 = 注意力竞争
- 先做4宫格，再做视频
  原因：4宫格固定关键帧，降低控制难度。视频生成时，AI只需要"补间"，不需要同时控制所有帧

需要用户确认的点：4宫格的叙事主题、光线风格

Step 2: 设计4宫格提示词
Q1: 提示词的结构应该是什么？
真相3 → 提示词的结构 = AI的优先级
最重要的是 → 产品一致性
结构应该是：产品一致性声明（最前面，单独成段）→ 场景风格参考（第二段）→ 逐个面板描述 → 全局约束（面板描述后，单独成段）

Q2: 产品一致性怎么写？
真相2 → 参考图（精确）+ 文字描述（模糊）= 精确度下降
❌ 不要写："金色盖子、透明瓶身、内含金色胶囊..."
✅ 只列维度："material, shape, color, transparency, labels"

应用公式：
"The product from the first reference image must be IDENTICAL in every detail:
- Material, texture, surface finish must match the reference
- Appearance, shape, and proportions must remain consistent
- Color, transparency, and lighting reflections must be identical
- Internal contents and all visible details must stay unchanged
- All original labels, text, and branding must be preserved exactly"

Q3: 场景参考怎么写？
双垫图需要语言索引（"第一张图"、"第二张图"）：
"Follow the visual style and composition approach from the second reference image:
- Dreamy, ethereal beach scene aesthetic
- Soft, diffused natural lighting
- Miniature diorama style with high-end commercial quality"

为什么要列出具体元素？不是让AI"复制"场景图，而是明确"借鉴哪些方面"（风格、光线、质感）

Q4: 面板描述怎么写？
首先设计叙事（起承转合）：
Panel 1: 产品在沙滩上（静态，建立场景）
Panel 2: 海浪靠近产品（动态，引入变化）
Panel 3: 产品被浪花环绕（高潮，视觉冲击）
Panel 4: 产品在水中漂浮（结局，情绪升华）

每个面板包含：摄像机角度、产品位置/状态、环境元素、光线/氛围

PANEL 1 - DISCOVERY:
Close-up shot, slightly elevated angle. The product rests upright on pale, almost white sand. Gentle shadows cast by soft natural light. Calm, serene atmosphere. The ocean is visible in the soft-focus background.

PANEL 2 - APPROACH:
Medium shot, eye-level angle. A gentle wave approaches the product from the left side. The product remains upright on the sand. Anticipation builds as the water gets closer. Lighting remains soft and consistent.

PANEL 3 - EMBRACE:
Dynamic close-up shot, low angle. The product is surrounded by white foam and crystal-clear water. Droplets catch the light. The product remains upright and stable. Peak visual drama with sparkling water effects.

PANEL 4 - FLOAT:
Wide shot, slightly elevated angle. The product floats peacefully in the shallow, crystal-clear water. Gentle ripples surround it. Soft golden hour light creates a dreamy, uplifting mood. Sense of freedom and purity.

Q5: 全局约束怎么写？
核心洞察：AI是局部优化者，会独立处理每个格子 → 需要显式声明全局规则

CONSISTENT ELEMENTS ACROSS ALL PANELS:
- Overall brightness level must be consistent across all four panels
- Color temperature must remain uniform (warm, natural daylight)
- The product must be IDENTICAL in appearance in all panels where it appears
- The pale sand color must be consistent (very light beige, almost white)

为什么要单独成段？真相3 → 单独成段 = 重要。这是在告诉AI："这些约束的优先级很高"

✅ 完整提示词
PRODUCT CONSISTENCY REQUIREMENTS:
The product from the first reference image must be IDENTICAL in every detail:
- Material, texture, surface finish must match the reference
- Appearance, shape, and proportions must remain consistent
- Color, transparency, and lighting reflections must be identical
- Internal contents and all visible details must stay unchanged
- All original labels, text, and branding must be preserved exactly

VISUAL STYLE REFERENCE:
Follow the visual style and composition approach from the second reference image:
- Dreamy, ethereal beach scene aesthetic
- Soft, diffused natural lighting with warm color temperature
- Miniature diorama style with high-end commercial quality
- Clean, bright, airy atmosphere

4-PANEL NARRATIVE GRID:

PANEL 1 - DISCOVERY:
Close-up shot, slightly elevated angle. The product rests upright on pale, almost white sand. Gentle shadows cast by soft natural light. Calm, serene atmosphere. The ocean is visible in the soft-focus background.

PANEL 2 - APPROACH:
Medium shot, eye-level angle. A gentle wave approaches the product from the left side. The product remains upright on the sand. Anticipation builds as the water gets closer. Lighting remains soft and consistent.

PANEL 3 - EMBRACE:
Dynamic close-up shot, low angle. The product is surrounded by white foam and crystal-clear water. Droplets catch the light. The product remains upright and stable. Peak visual drama with sparkling water effects.

PANEL 4 - FLOAT:
Wide shot, slightly elevated angle. The product floats peacefully in the shallow, crystal-clear water. Gentle ripples surround it. Soft golden hour light creates a dreamy, uplifting mood. Sense of freedom and purity.

CONSISTENT ELEMENTS ACROSS ALL PANELS:
- Overall brightness level must be consistent across all four panels
- Color temperature must remain uniform (warm, natural daylight)
- The product must be IDENTICAL in appearance in all panels where it appears
- The pale sand color must be consistent (very light beige, almost white)

CAMERA PROGRESSION: Close-up → Medium shot → Dynamic close-up → Wide shot
MOOD PROGRESSION: Serene discovery → Anticipation → Dynamic excitement → Peaceful resolution

IMPORTANT: No additional text overlay or graphic elements should be added to the image. All original labels, text, and branding on the product must be preserved exactly as shown in the reference image.

Step 3: 生成前检查
📋 检查清单
□ 尺寸：1440x2560 ✓  □ 质量：medium ✓  □ 参考图：已列出（产品图 + 场景图）✓
□ 产品一致性：已声明 IDENTICAL + 维度清单 ✓  □ 双垫图索引：已用"first image" / "second image" ✓
□ 全局约束：已声明（CONSISTENT ACROSS ALL PANELS）✓  □ 叙事连贯性：起承转合 ✓
□ 标签保留：已声明"preserve original labels" ✓

Step 4: 用户确认
呈现给用户：
"我设计了一个4宫格叙事，展示产品与海滩的互动：
Panel 1: 产品静置在沙滩上（宁静的发现）
Panel 2: 海浪靠近产品（期待感）
Panel 3: 产品被浪花环绕（视觉高潮）
Panel 4: 产品漂浮在水中（自由与纯净）
视觉风格：梦幻、空灵，柔和自然光，高端商业质感。色调：暖色调日光，浅米色沙滩。
请确认这个方向是否符合您的预期？"

为什么要确认？叙事主题是主观选择（可能用户想要完全不同的故事），早期确认避免返工。但不要问太多问题（1-2个关键点即可）

Step 5: 生成4宫格
generate_image_gpt_image_2(
    image_name="金色胶囊海滩4宫格",
    prompt="[上面的完整提示词]",
    image_url_list=["产品图URL", "场景参考图URL"],
    size="1440x2560",
    quality="medium"
)

Step 6: 从4宫格到视频
Q1: 视频提示词和4宫格提示词有什么不同？
核心区别：4宫格 = 空间中的4个瞬间（离散的）；视频 = 时间中的连续流（连续的）
所以：4宫格提示词描述"4个状态"；视频提示词描述"连续过程"和"过渡"

Q2: 如何转换？
转换公式：
- Panel 1 → 0-3秒：描述"进入这个瞬间的过程"
- Panel 1→2 → 3-5秒：描述"从瞬间1到瞬间2的过渡"
- Panel 2 → 5-7秒：描述"停留在瞬间2"
- Panel 2→3 → 7-8秒：描述"过渡"
- Panel 3→4 → 8-10秒：描述"高潮到结局的展开"
关键：不只是描述"关键帧"，更要描述"帧与帧之间发生了什么"

Q3: 语言风格？
核心洞察：不同模型对语言的"理解层次"不同，视频模型的"母语"是自然叙事
❌ 不用："PANEL 1 (0-3s): ..."  ❌ 不用："80% - Core Action: ..."
✅ 用："The camera opens with... As the scene unfolds... Then..."
用动作动词：enters, approaches, surrounds, floats, cascades
用连接词：as, while, then, gradually, slowly

Q4: 参考图策略？
双参考图：第一张=产品图（一致性约束），第二张=4宫格图（动作序列参考）
为什么用4宫格作为参考？4宫格已经固定了"关键帧"，视频生成时AI只需要"补间"，这样可以确保视频和4宫格的视觉连贯性

✅ 视频提示词（与4宫格的差异部分）
PRODUCT CONSISTENCY REQUIREMENTS:
The product from the first reference image must be IDENTICAL in every detail:
- Material, texture, surface finish must match the reference
- Appearance, shape, and proportions must remain consistent
- Color, transparency, and lighting reflections must be identical
- Internal contents and all visible details must stay unchanged
- All original labels, text, and branding must be preserved exactly

CONTINUOUS NARRATIVE (10 seconds):
The camera opens with a close-up view of the product resting peacefully on pale, almost white sand. Soft natural light casts gentle shadows. The scene is calm and serene, with the ocean visible in the soft-focus background.

As the scene unfolds, a gentle wave slowly approaches the product from the left side. The water moves smoothly across the sand, getting closer and closer. The product remains stable and upright, anticipation building.

The wave reaches the product, and white foam begins to surround it. Crystal-clear water swirls around the base. Droplets catch the light, creating sparkling effects. The product remains upright and stable throughout this dynamic moment.

The product then gently lifts and begins to float peacefully in the shallow, crystal-clear water. Gentle ripples spread outward. Soft golden hour light bathes the scene, creating a dreamy, uplifting atmosphere. The product floats freely, embodying a sense of purity and freedom.

ACTION SEQUENCE REFERENCE:
Follow the action progression and visual composition shown in the second reference image (4-panel grid). The video should smoothly transition through all four key moments depicted in the grid.

IMPORTANT: No additional text overlay or graphic elements. All original labels and text on the product must be preserved exactly.

关键改变：
- 删除了"PANEL 1, PANEL 2..."的结构化标记
- 用自然叙事流："The camera opens... As the scene unfolds... Then..."
- 强调了"过渡"："slowly approaches", "begins to surround", "gently lifts"
- 用4宫格作为"动作序列参考"

Step 7: 生成视频
generate_video_seedance_v2_0_mini(
    prompt="[上面的视频提示词]",
    reference_images=["产品图URL", "4宫格图URL"],
    duration=10,
    aspect_ratio="9:16",
    resolution="720p",
    sound="on"
)

🎯 复盘：关键决策点
| 决策点 | 思考过程 | 依据的原理 |
|:---|:---|:---|
| 用双垫图 | 产品需要精确，场景需要风格 | 真相2：注意力竞争 |
| 产品不描述特征 | 避免干扰参考图的精确性 | 真相2：图 vs 文字 |
| 产品一致性放最前面 | 传递"这是最重要的"信号 | 真相3：结构 = 优先级 |
| 先做4宫格 | 降低控制难度，固定关键帧 | 分步降维思想 |
| 全局约束单独成段 | 让AI知道这是全局规则 | 真相3：单独成段 = 重要 |
| 视频用自然叙事 | 适配视频模型的"母语" | 语言风格适配 |
| 4宫格作为视频参考 | 确保视觉连贯性 | 关键帧 + 补间策略 |

💡 关键学习点：每个决策都有明确的"为什么"（不是死记硬背）；每个决策都关联回核心原理（可以推广到新场景）；遇到问题时，有明确的诊断和修正路径

---

📚【完整指南】深入理解AI的工作原理

1. 理解AI的工作原理（6个核心原理）

1.1 AI是字面理解者
案例：标签丢失事件
提示词："no text, no labels" → 结果：产品自带的标签也消失了
为什么？AI把"no text"理解为"画面中的所有文字"，它不会推理"产品标签是产品的一部分，应该例外"。AI没有"常识推理"能力。

洞察：AI不会推理"常识例外"，必须显式声明所有例外情况

正确做法：
"No additional text overlay or graphic elements should be added to the image. All original labels, text, and branding on the product must be preserved exactly as shown in the reference image."

推导能力测试：如果用户说"不要有人"，但场景是"咖啡店"，AI会生成空荡荡的咖啡店吗？
答案：会的。除非你说"a busy coffee shop with customers"。原理：AI执行字面指令，不会补充"常识"

推广到新场景：当你说"不要X"时，问自己：是否有"X的例外"需要保留？如果有，必须显式声明

1.2 AI是注意力竞争者
案例：产品一致性的演进
早期提示词："A transparent glass bottle with golden metal cap, containing golden capsules..." + 参考图
结果：产品形状对了，但细节不一致（颜色深浅、透明度、标签位置）
为什么？参考图说"这个产品长这样"（视觉信息），文字说"金色盖子、透明瓶身..."（语言信息）。AI在两者之间混合采样，而不是100%依赖参考图。语言的"金色"是模糊的（有很多种金色），参考图的"金色"是精确的（特定的色值）。混合 = 精确度下降

洞察：图 vs 文字 = 注意力竞争。当两者都提供信息时，AI会混合它们。要达到100%一致，必须让文字"退位"

正确做法：
"The product from the reference image must be IDENTICAL in every detail:
- Material, texture, surface finish must match the reference
- Appearance, shape, and proportions must remain consistent
- Color, transparency, and lighting reflections must be identical
- Internal contents and all visible details must stay unchanged
- All original labels, text, and branding must be preserved exactly"
（列维度，不描述特征）

为什么列维度有效？"material, texture, shape, color"不是描述，是检查清单，AI会逐项对照参考图。这是在引导AI的注意力扫描路径。文字不再提供"模糊信息"，只提供"扫描指令"

推导能力测试：如果有两张参考图（产品图 + 场景图），不做任何说明，会发生什么？
答案：AI会混合两张图的信息，可能产品变形或场景混乱
解决方案：必须用语言建立索引
"The product from the first reference image..."
"Follow the visual style from the second reference image..."

推广到新场景：当你有"精确样本"（参考图）时，让文字退位。文字只做两件事：指向样本（"must be IDENTICAL"）、列扫描清单（维度列表）

1.3 AI是局部优化者
案例：4宫格的整体亮度
第一次生成：4个格子的亮度不一致，提示词里没有提"一致性"
为什么？AI生成4个格子时，会独立处理每个格子。Panel 1优化这个格子的曝光，Panel 2重新优化，Panel 3再次优化...结果：每个格子都"局部最优"，但全局不一致

洞察：AI的默认模式是局部优化，"4个格子"在AI眼里是"4个独立任务"。要实现全局一致性，必须显式声明全局约束

正确做法：
"CONSISTENT ELEMENTS ACROSS ALL PANELS:
- Overall brightness level must be consistent across all four panels
- Color temperature must remain uniform
- The product must be IDENTICAL in all panels where it appears"
（在描述具体面板之前，先声明全局规则）

为什么要单独成段？回忆原理1.4（结构敏感）：单独成段 = 传递"这是全局规则"的信号。如果融入面板描述，AI会认为这只是"某个面板的要求"

推导能力测试：如果要生成"同一个房间，早中晚三个时刻"的3宫格，怎么办？
答案：先声明"same room layout, same furniture, same camera angle"，再描述"morning light / noon light / evening light"。原理：先固定不变的，再描述变化的

推广到新场景：当你需要"多个输出保持某些维度一致"时，先声明全局约束（单独成段），再描述局部变化

1.4 AI是结构敏感者
案例：视频提示词的60-20-20结构
用户要求："核心动作60%，摄像机20%，环境20%"，后来又说"环境部分完全不要"
为什么环境部分要删除？不是因为字数占比（环境描述可能只有2行），而是因为单独成段传递了"这很重要"的信号。AI看到独立的"ENVIRONMENT & STYLE"段落，会认为"这和CORE ACTION同等重要"

洞察：提示词的组织方式 = 重要性信号
- 单独成段 = 重要
- 融入其他描述 = 次要
- 放在前面 = 优先
- 放在后面 = 补充

对比：
❌ 结构A："CORE ACTION: ... CAMERA MOVEMENT: ... ENVIRONMENT & STYLE: tropical beach..."
→ AI认为环境和动作同等重要 → 环境会抢占注意力
✅ 结构B："The camera captures the action on a tropical beach... [动作描述融入环境]"
→ AI认为环境是背景 → 动作是焦点

推导能力测试：如果要强调"产品必须一致"，应该把这句话放在哪里？
答案：放在最前面，单独成段，用大写或加粗。原理：位置 + 格式 = 优先级信号

推广到新场景：设计提示词结构时问自己：什么是最重要的？→ 放最前面，单独成段。什么是次要的？→ 融入其他描述。什么是补充信息？→ 放最后

1.5 AI是语言风格适配者
案例：技术术语在视频提示词中失效
第一版提示词："80% - Core Action: the product tumbles out..." → 结果：AI可能理解为"画面中要出现'80% - Core Action'这些文字"，或者干扰了语义理解
为什么？图像生成模型训练数据包含大量"结构化描述"（如摄影指南、设计文档）；视频生成模型训练数据更多是"自然语言叙事"（如电影脚本、场景描述）。不同模型对语言的"理解层次"不同

洞察：不同模型对语言的"理解层次"不同，必须适配模型的"母语"

正确做法：
图像提示词：可以用结构化语言
"PANEL 1 - DISCOVERY: Close-up shot of..."
视频提示词：用自然叙事流
"The camera opens with a close-up view. A hand enters the frame and slowly approaches the button..."

推导能力测试：如果要生成"产品的360度旋转视频"，怎么写提示词？
❌ "0°-90°: front view, 90°-180°: side view, 180°-270°: back view..."
✅ "The product slowly rotates, revealing its front design. It gradually turns to show the side profile, then continues rotating to display the back..."
原理：用动作动词（rotates, revealing, turning）而非技术参数

推广到新场景：图像生成用结构化、技术性语言 OK；视频生成用自然叙事、动作动词；复杂布局可以用"SECTION A", "SECTION B"等标记

1.6 AI是显式约束执行者
案例：尺寸反复出错
多次生成后，AI还是会生成2048x2048，即使项目一直用9:16
为什么？AI没有"项目上下文记忆"，每次调用工具都是独立的。Summary Context虽然有信息，但不会自动应用到工具参数，必须每次显式传递

洞察：AI不会自动记住"项目惯例"，必须每次显式传递约束

正确做法：建立检查清单机制。每次生成前检查：尺寸、质量、比例、一致性要求。明确写出参数：size="1440x2560", quality="medium"

推广到新场景：不要假设AI"记得"之前的设置。建立检查清单，每次生成前核对，显式传递所有参数

---

2. 成功公式（基于6个原理）

2.1 产品一致性公式
参考图（产品）+ 维度清单（不描述特征）+ IDENTICAL声明 = 高一致性
原理：让AI的注意力100%在参考图上，文字只做"扫描指令"

模板：
"The product from the reference image must be IDENTICAL in every detail:
- Material, texture, surface finish must match the reference
- Appearance, shape, and proportions must remain consistent
- Color, transparency, and lighting reflections must be identical
- Internal contents and all visible details must stay unchanged
- All original labels, text, and branding must be preserved exactly"

何时使用：当需要产品在多个场景/角度/面板中保持完全一致时；商业项目的标准要求
何时不用：当只是"风格参考"允许变化时（用"in the style of"）；当需要产品有变化时（如不同颜色版本）

2.2 双垫图分工公式
第一张图（产品）+ 第二张图（场景）+ 语言索引（"from the first", "follow the second"）= 分离控制
原理：用语言建立"变量名"，让AI知道每张图的职责

模板：
"The product from the first reference image [产品一致性声明].
Follow the visual style and composition approach from the second reference image:
- [列出要借鉴的具体元素：lighting, color palette, mood, composition]"

何时使用：当需要"保持产品不变"+"改变场景/风格"时；当有明确的产品图和场景参考图时
推导：三张图怎么办？继续用"the third reference image"建立索引。关键是：每张图都要有明确的"职责声明"

2.3 4宫格一致性公式
全局约束声明（consistent across all panels）+ 局部变化描述（Panel 1, Panel 2...）= 统一中有变化
原理：先声明全局规则，再描述局部差异

结构：
1. 产品一致性声明（如果有产品）
2. 视觉风格参考（如果有参考图）
3. 逐个面板描述（Panel 1, Panel 2, Panel 3, Panel 4）
4. 全局一致性约束（CONSISTENT ELEMENTS ACROSS ALL PANELS）
5. 摄像机进程（CAMERA PROGRESSION）
6. 情绪进程（MOOD PROGRESSION）

全局约束模板：
"CONSISTENT ELEMENTS ACROSS ALL PANELS:
- Overall brightness level must be consistent across all four panels
- Color temperature must remain uniform
- The product must be IDENTICAL in all panels where it appears
- [其他需要保持一致的元素]"

关键点：全局约束要单独成段，放在面板描述之后；用"must be consistent / must be identical"等强约束词；明确列出哪些维度需要一致

2.4 视频连续性公式
关键帧描述（4宫格）+ 连续动作叙事（过程描述）+ 双参考图（产品+动作）= 流畅视频
原理：4宫格固定"锚点"，叙事描述"路径"，参考图提供"约束"

从4宫格到视频的转换：
4宫格：空间中的4个瞬间；视频：时间中的连续流

转换方法：
- Panel 1 → 0-3秒：描述"进入这个瞬间的过程"
- Panel 1→2 → 3-5秒：描述"从瞬间1到瞬间2的过渡"
- Panel 2 → 5-7秒：描述"停留在瞬间2"
- Panel 2→3 → 7-8秒：描述"过渡"
- Panel 3→4 → 8-10秒：描述"高潮展开"

语言风格：用动作动词（enters, approaches, presses, opens, tumbles, cascades）；用连接词（as, while, then, gradually, slowly）；用自然叙事流，不用技术术语

参考图策略：第一张=产品图（一致性约束），第二张=4宫格图（动作序列参考）

模板：
"PRODUCT CONSISTENCY REQUIREMENTS:
[产品一致性声明]

CONTINUOUS NARRATIVE:
The camera opens with [Panel 1的场景]. [描述初始状态]
As the scene unfolds, [描述Panel 1到Panel 2的过渡]. [描述动作过程]
[Panel 2的关键时刻]. [描述这个瞬间的细节]
Then, [描述Panel 2到Panel 3的过渡]. [描述变化]
[Panel 3的高潮]. [描述视觉冲击]
Finally, [描述Panel 3到Panel 4的过渡]. [描述结局]
[Panel 4的最终状态]. [描述情绪升华]

ACTION SEQUENCE REFERENCE:
Follow the action progression and visual composition shown in the second reference image (4-panel grid)."

2.5 信息优先级公式
重要信息：单独成段 + 放在前面 + 显式强调
次要信息：融入描述 + 放在后面 + 隐式提及
= 符合预期的权重分配
原理：提示词的结构 = AI的优先级判断依据

实践：
✅ 高优先级（产品一致性）："PRODUCT CONSISTENCY REQUIREMENTS: The product must be IDENTICAL..."（单独成段，放最前面，用大写标题）
✅ 中优先级（场景描述）："SCENE DESCRIPTION: Modern elevator interior with..."（单独成段，但在产品之后）
✅ 低优先级（氛围）："...creating a gentle, premium atmosphere."（融入场景描述末尾，不单独成段）

---

3. 决策树

3.1 何时需要用户确认？
必须确认的情况（主观选择，没有唯一正确答案）：
- 光线颜色（金色 vs 白色 vs 暖白微金）
- 情绪调性（梦幻 vs 现实 vs 平衡）
- 叙事主题（多种可能的故事线）
- 时间分配（高潮占多少时间）
- 4宫格的叙事主题、视频的整体节奏、产品的呈现方式（静态 vs 动态）

可以自主决策的情况（技术参数有明确标准）：
- 尺寸、质量、比例（遵循项目默认值）
- 一致性约束（商业项目默认需要）
- 细节优化（提示词的具体措辞、描述的详细程度，不影响整体方向）

如何设计确认？
❌ 开放式提问："你觉得光线怎么样？"
✅ 提供2-3个具体方案，说明每个方案的特点
"我设计了光线方案：A：金色魔法光（梦幻、超现实）B：白色现实光（自然、真实）C：暖白微金（平衡、高端）。请选择您偏好的方向？"

3.2 何时用单垫图 vs 双垫图？
单垫图：产品在简单背景中（纯色、渐变、简单几何）；只需要产品一致性，场景可以AI自由发挥
双垫图：产品 + 复杂场景（需要参考特定构图/风格）；产品 + 特定动作（需要参考动作序列）
三垫图或更多：理论上可行，但注意力会进一步分散，必须给每张图明确的"职责"和"语言索引"

3.3 何时直接生成 vs 先确认提示词？
直接生成：需求明确无主观选择空间；是迭代中的修正（问题已定位，解决方案明确）；技术性调整（尺寸、参数）
先确认提示词：首次生成（建立共识）；有主观选择（光线、情绪、节奏、叙事）；复杂任务（4宫格、视频）；用户可能有不同理解的情况

---

4. 问题诊断与修正（详细版）

4.1 产品一致性失败
症状：产品形状对了，但颜色/透明度/细节不对；多个面板中的产品长得不一样；产品标签消失或变形

诊断流程：
1. 检查提示词是否描述了产品特征？搜索关键词：color, material, texture, transparent, golden 等 → 如果有，这是问题根源
2. 检查是否声明了IDENTICAL？搜索关键词：IDENTICAL, must match, must be consistent → 如果没有，添加强约束
3. 检查参考图是否清晰？分辨率是否足够？产品是否清晰可见？→ 如果不清晰，换高清图
4. 检查是否有全局约束（如果是多面板）？搜索：CONSISTENT ACROSS ALL PANELS → 如果没有，添加全局约束段落

修正策略：
策略1：删除特征描述，只列维度
❌ 删除："A transparent glass bottle with golden metal cap, containing golden capsules..."
✅ 替换为：维度清单（见§2.1模板）

策略2：强化IDENTICAL声明
"must be IDENTICAL" → "must be ABSOLUTELY IDENTICAL"；"should match" → "MUST match exactly"

策略3：将产品一致性段落移到最前面，单独成段，用大写标题

策略4：添加全局约束（多面板）
在所有面板描述之后加："CONSISTENT ELEMENTS ACROSS ALL PANELS: - The product must be IDENTICAL in appearance in all panels where it appears"

4.2 尺寸/比例错误
症状：生成了2048x2048，但需要9:16；生成了16:9，但需要9:16
诊断：检查工具调用的size参数，是否忘记传参数？是否传错了参数？

修正策略：
策略1：建立检查清单，每次生成前核对：□ size: "1440x2560" □ quality: "medium"
策略2：在工具调用前，明确写出参数，然后再调用工具

4.3 光线/氛围偏差
症状：光线太冷/太暖/太强/太弱；氛围不符合预期

诊断：提示词里的光线描述是否明确？是否用了模糊词汇（如"nice lighting"）？是否与参考图冲突？光线描述是否分级（强度、色温、方向）？

修正策略：
策略1：用分级描述
强度：soft / moderate / strong / dramatic
色温：cool white / neutral white / warm white / golden
方向：diffused / directional / backlit / side-lit / top-lit
例子："Soft, diffused natural light with warm white color temperature, coming from the side to create gentle shadows"

策略2：如果有参考图，明确光线来源
"Follow the lighting approach from the reference image: - Soft, diffused natural daylight - Warm color temperature - Gentle shadows"

策略3：如果需要确认，提供方案（金色魔法光 / 自然白光 / 暖白微金）

4.4 标签/文字问题
症状：产品标签消失了；或者出现了不该有的文字；标签变形或不清晰

诊断：是否写了"no text"但没有声明"preserve original labels"？是否要求了"clean"或"minimal"（这些词可能被AI理解为"删除所有文字"）？

修正策略：
策略1：显式声明例外
❌ "no text, no labels"
✅ "No additional text overlay or graphic elements should be added to the image. All original labels, text, and branding on the product must be preserved exactly as shown in the reference image."

策略2：在产品一致性声明中包含标签
"The product must be IDENTICAL in every detail: - ... - All original labels, text, and branding must be preserved exactly"

策略3：如果标签不清晰，可能是参考图问题
1. 检查参考图中的标签是否清晰 2. 如果参考图本身模糊 → 换高清参考图 3. 如果生成后标签模糊 → 可能需要upscale工具提升分辨率

---

5. 参数默认值清单

项目级默认值（本项目）
| 参数 | 默认值 | 何时例外 | 原因 |
|:---|:---|:---|:---|
| 尺寸 | 1440x2560 | 从不例外 | 项目统一标准 |
| 比例 | 9:16 | 从不例外 | 项目统一标准 |
| 质量 | medium | 从不例外 | 成本与质量平衡 |
| 视频时长 | 10秒 | 用户明确要求其他时长 | 标准叙事长度 |
| 视频分辨率 | 720p | 用户明确要求更高 | 标准输出质量 |
| 视频引擎 | Seedance V2.0 Mini | 用户明确要求其他引擎 | 项目标准工具 |
| 视频比例 | 9:16 | 用户明确要求其他比例 | 与图片保持一致 |

每次生成前的检查清单
📋 图片生成检查清单：
□ 尺寸：1440x2560 ✓  □ 质量：medium ✓  □ 参考图：已列出所有相关图片 ✓
□ 产品一致性：已声明IDENTICAL + 维度清单 ✓  □ 语言索引：已建立（如果是双垫图）✓
□ 全局约束：已声明（如果是4宫格）✓  □ 标签保留：已声明"preserve original labels" ✓

📋 视频生成检查清单：
□ 时长：10秒 ✓  □ 比例：9:16 ✓  □ 分辨率：720p ✓
□ 参考图：产品图 + 4宫格图 ✓  □ 产品一致性：已声明 ✓
□ 语言风格：自然叙事流（不用技术术语）✓  □ 连续性：描述了过渡过程 ✓

---

6. 从困惑到洞察的推导示例

示例1：为什么不能描述产品特征？
困惑： "我已经给了参考图，为什么还要在提示词里写'金色盖子、透明瓶身'？这不是更清楚吗？"

推导过程：
AI看到参考图 → 提取视觉特征（精确的像素级信息：金色具体色值、透明度数值、标签位置）
AI看到文字"金色盖子" → 提取语言特征（模糊的语义信息："金色"可能是多种色值，"盖子"可能是多种形状）
AI生成时 → 混合两者（从参考图采样主要信息，从文字采样补充信息）
结果：形状对了（因为参考图提供了主要信息），但细节偏差（因为文字引入了模糊性）

洞察：参考图提供"精确样本"（像素级），文字提供"模糊描述"（语义级），混合 = 精确度下降

解决方案：让文字退位。文字只做"指向"（IDENTICAL）和"扫描指令"（维度清单）
推广：当你有"精确样本"时，让文字退位。文字只做两件事：指向样本、列扫描清单

示例2：为什么4宫格要先做，而不是直接生成视频？
困惑： "视频本身就包含了4个关键时刻，为什么要先做4宫格？这不是多此一举吗？"

推导过程：
视频生成 = 在时间维度上采样（10秒视频 ≈ 300帧），AI需要控制每一帧的内容，时间是连续的 → AI需要同时控制"每一帧"
直接生成视频：需要控制大量帧，控制难度高
4宫格 = 只控制4个关键帧，其他帧AI自动插值，控制难度大幅降低

洞察：空间控制 < 时间控制（难度）。先固定关键帧，再让AI补间 = 降低控制难度

类比：4宫格 = 关键帧动画（keyframe animation），视频 = 补间动画（tweening）
推广：任何复杂任务，都可以"分步降维"。先控制"关键约束点"，再让AI填充"中间过程"
例子：长视频 → 先做分镜（关键帧）→ 再生成视频；复杂图像 → 先做草图（布局）→ 再细化

示例3：为什么双垫图需要语言索引？
困惑： "AI看到两张图，难道不会自动识别'这张是产品，那张是场景'吗？它应该能理解吧？"

推导过程：
AI没有"图像分类"的预处理步骤，不会先分析"第一张是产品特写，第二张是场景"
两张图对AI来说都是"视觉输入"，AI看到的是一堆视觉特征
如果不说明，AI会尝试"融合"两张图的信息 → 可能产品变形（混合了场景图元素）或场景混乱（混合了产品图背景）

语言索引 = 建立"变量名"
"第一张图" = 变量A（职责：产品一致性）
"第二张图" = 变量B（职责：场景风格）
AI现在知道：A和B有不同的用途

洞察：AI不会自动推理"图的用途"，必须用语言建立"变量名"和"职责"

类比：就像编程中的变量
product_image = 第一张图  // 用于产品一致性
style_reference = 第二张图  // 用于场景风格

推广：有多个输入源时，都要明确"分工"。用语言建立索引，明确每张图的"职责"
例子：三张图（产品图 + 场景图 + 光线参考图）必须说明"第一张用于产品，第二张用于场景，第三张用于光线"

示例4：为什么全局约束要单独成段？
困惑： "我在每个面板描述里都写了'保持一致'，为什么还要单独写一段全局约束？"

推导过程：
AI生成4宫格时，是逐个处理的（生成Panel 1 → 读取Panel 1的描述，生成Panel 2 → 读取Panel 2的描述...）
如果约束写在Panel 1的描述里：AI生成Panel 1时看到了"consistent"，但此时Panel 2、3、4还不存在，AI不知道"consistent"的参照物是什么
如果约束写在每个面板里：AI生成每个面板时都会独立优化，"consistent"被理解为"这个面板内部一致"而不是"4个面板之间一致"
如果约束单独成段，放在所有面板描述之后：AI在生成整个4宫格时，会把这段作为"全局规则"，这是在告诉AI"这是跨面板的约束"

洞察：约束的位置 = 约束的作用域
写在面板内 = 局部约束（只影响该面板）
单独成段 = 全局约束（影响所有面板）

类比：就像编程中的变量作用域
function panel1() { let brightness = "consistent"; }  // 局部变量
let brightness = "consistent";  // 全局变量
function panel1() { ... } function panel2() { ... }

推广：任何时候需要"全局约束"，都要单独成段，放在所有局部描述之后，用明确的标题（如"CONSISTENT ACROSS ALL PANELS"）

---

7. 边界与失效情况

7.1 什么情况下这套方法会失效？
情况1：参考图本身质量差（模糊、低分辨率、光线不佳、产品不清晰）
→ AI只能从参考图中提取有限的信息。解决：换高清参考图，或降低一致性预期（接受"风格相似"而非"完全一致"）

情况2：需求超出模型能力边界（要求生成特定名人的脸、复杂文字排版、物理上不可能的场景）
→ 模型本身的能力限制。解决：调整需求降低难度，或换模型，或分步实现（先生成基础，再用其他工具精修）

情况3：多个约束互相冲突（要求"产品完全一致" + "产品在水中漂浮"，但参考图中产品是直立的）
→ 约束之间存在逻辑矛盾。解决：识别冲突，与用户确认优先级，调整其中一个约束

情况4：提示词过于复杂（超过2000字，包含大量细节）
→ AI的注意力被过度分散。解决：简化提示词，只保留最关键的约束，用结构化方式组织

7.2 什么情况下应该降低预期？
情况1：细节过于复杂（产品上有大量小字，要求每个字都清晰）
→ AI可能无法完美还原所有细节。策略：接受"整体一致，局部近似"；如果必须完美，考虑upscale工具 + 后期修图

情况2：动态场景的物理真实性（产品在冲浪板上，要求完全符合物理规律）
→ AI可能生成"视觉合理"但"物理不严谨"的画面。策略：优先视觉效果而非物理准确性；如果必须物理准确，考虑3D建模工具

情况3：极端的一致性要求（要求产品在100个不同场景中完全一致）
→ 随着场景数量增加，一致性会逐渐下降。策略：分批生成（每批5-10个场景），每批都用同一个参考图，接受"高度一致"而非"完全一致"

7.3 什么情况下应该寻求人工介入？
情况1：多次迭代仍无法达到预期（尝试5次以上仍有明显问题）
→ 可能需求本身有问题（互相矛盾）或超出模型能力。行动：人工重新审视需求合理性，或换工具/方法

情况2：用户的反馈模糊（用户说"感觉不对"，但说不清哪里不对）
→ 用户自己也不清楚期望，或期望与现实有差距。行动：人工引导用户明确需求，提供多个方案让用户选择，通过对比帮助澄清期望

情况3：涉及主观审美判断（技术上没问题，但"感觉不够好"）
→ 审美是主观的。行动：人工设计师介入提供专业建议，或进行A/B测试

---

9. 快速参考卡片

🎯 核心原则（随时记住）
1. AI是执行指令，不是理解意图 → 显式声明所有约束和例外
2. 图 vs 文字 = 注意力竞争 → 有精确样本时，让文字退位
3. 结构 = 优先级 → 重要的单独成段，放前面
4. AI是局部优化者 → 全局约束要显式声明
5. 适配模型的"母语" → 图像用结构化，视频用自然叙事

📋 生成前检查（每次必做）
图片：□ 尺寸 1440x2560 □ 质量 medium □ 参考图已列出 □ 产品一致性已声明 □ 语言索引已建立（双垫图）□ 全局约束已声明（4宫格）
视频：□ 10秒 □ 9:16 □ 720p □ 参考图：产品 + 4宫格 □ 自然叙事流 □ 描述了过渡

🔍 问题快速定位
产品不对 → 删除特征描述，只列维度
标签消失 → 加"Preserve original labels"
多面板不一致 → 加全局约束段落
光线不对 → 用分级描述（强度/色温/方向）
尺寸不对 → 检查参数：1440x2560

💡 常用模板
产品一致性：
"The product from the reference image must be IDENTICAL in every detail:
- Material, texture, surface finish - Shape, proportions - Color, transparency - Internal contents - All original labels"

双垫图索引：
"The product from the first reference image [一致性声明].
Follow the visual style from the second reference image [风格描述]."

全局约束：
"CONSISTENT ACROSS ALL PANELS:
- Overall brightness must be consistent
- The product must be IDENTICAL in all panels"

---

📊 总结：从规则到思考

这份SOP不是让你记住：❌ "遇到X情况，做Y" ❌ "用这个模板" ❌ "按这个步骤"
而是让你理解：
✅ AI如何工作（6个原理）：字面理解者、注意力竞争者、局部优化者、结构敏感者、语言风格适配者、显式约束执行者
✅ 为什么这样做有效（推导过程）：每个原理都从真实案例推导，每个公式都有明确的原理支撑，每个决策都有清晰的逻辑
✅ 如何应对新情况（迁移能力）：不是死记硬背规则，而是理解底层逻辑，遇到新场景时能推导出解决方案

核心思维转变：
从"描述你想要什么" 到"设计AI的执行路径"
具体做法：
- 用参考图约束概率空间（精确样本）
- 用文字引导注意力路径（扫描指令）
- 用结构传递优先级信号（重要性排序）
- 用显式约束覆盖默认行为（声明例外）

当你遇到全新场景时，问自己5个问题：
1. 哪些维度需要精确控制？哪些可以模糊？→ 决定用参考图还是文字描述
2. 我的输入（图/文字/参数）会如何竞争AI的注意力？→ 决定如何分配信息源
3. 我的提示词结构传递了什么优先级信号？→ 决定如何组织提示词
4. 我是否显式声明了所有约束和例外？→ 决定是否需要补充声明
5. 这个任务能否分步降维？→ 决定是一步完成还是分步实现

如果你能回答这5个问题，你就能推导出解决方案。

✨ 这份SOP的目标不是"教你做事"，而是"教你思考"。
当你真正理解了AI如何工作、为什么这样做有效、如何应对新情况，你就不再需要这份SOP了。
因为你已经学会了如何与AI协作的底层逻辑。

记住：
你不是在"描述画面"，你是在"编程AI的执行逻辑"
你不是"用户"，你是"AI的协作者"
你不是"提需求"，你是"设计执行路径"
