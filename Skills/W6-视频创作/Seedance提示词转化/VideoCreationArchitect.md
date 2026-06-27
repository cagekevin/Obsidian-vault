# Video Creation Architect

> Seedance 视频创作 Skill — 从分镜到出片的完整流水线。
>
> **Wiki 知识引用**：本 Skill 大量引用 Wiki 概念页中的实战经验。标记 `📖 Wiki:` 的内容可直接查阅对应页面获取完整方法论。

---

## 1. Technical Specifications

### Aspect Ratio

| 用途 | 比例 | 说明 |
|------|------|------|
| 竖屏短视频 | 9:16 | 默认，抖音/小红书/Reels |
| 横屏叙事 | 16:9 | 电影感、B站、YouTube |
| 方形 | 1:1 | 产品展示、Instagram |

### The Character & Product Master Sheet

角色/产品主表，每次项目必须先建立。

📖 Wiki: [[AI角色资产搭建]] — 人物资产三件套（脸部三视图/全身三视图/融合输出）、妆造提示词公式、活人感、微表情三控

#### Visual Standard

所有参考图必须：白色或纯色背景、无文字/边框/UI 元素、主体居中、光线均匀。

📖 Wiki: [[参考图优先原则]] — 参考图比一千字描述都管用，能图生图就不要纯文字生图

#### Style Adaptation

渲染风格必须匹配项目整体视觉风格（如皮克斯 3D、写实、水墨等），角色和产品在同一风格体系内。

#### Unique Identifier

每个角色/产品有一个短 ID，格式：`[type]_[name]`，如 `hero_maya`、`product_jar`、`villain_draven`。

#### Element Types & Fields

| Type | Required Fields |
|------|----------------|
| **Character** | id, name, appearance (身高/体型/年龄), outfit_description (服装/配饰/材质/颜色), face_reference (脸型/五官/肤色), hair, makeup, special_features (疤痕/纹身等), voice_profile_id |
| **Product** | id, name, type (瓶装/胶囊/软管等), dimensions, color, material, texture, label_design, cap_color |
| **Non-Human Character** | id, name, species, size, color_pattern, texture, movement_style, special_abilities |
| **Body Part Actor** | id, body_part (hands/feet/eyes等), belongs_to (所属角色), shots_appears_in, reference_image |

#### [CRITICAL — BODY PART ACTOR DETECTION]

当同一角色的同一个身体部位出现在 **2 个及以上镜头**时，必须注册为 Body Part Actor。注册后该部位在所有镜头中保持一致的尺寸、肤色、角度和光影。

#### Reference Image Rule

| 情况 | 规则 |
|------|------|
| 有产品参考图 | 直接使用，文字只说用途，不描述外观 |
| 无参考图 | 用 Generation Formula 生成一张 |
| 风格参考 | "in the style of" + 参考图 |
| 编辑基础 | "Based on" + Changes/Keep 分层 |

#### Reference Sheet Formats

- **角色**: 脸部三视图 + 全身三视图 + 关键妆造特写
- **产品**: 正视图 + 45° 视图 + 俯视图 + 材质特写
- **非人角色**: 全貌 + 细节特征特写

#### Generation Formula

```
[元素类型] + [唯一标识符] + [核心外观描述] + [风格] + [背景要求]
```

---

### Voice Profiles

| Field | Description |
|-------|-------------|
| voice_id | 唯一标识 |
| character_id | 所属角色 |
| tone | 音色（温暖/冷峻/活泼/沉稳等） |
| pace | 语速（慢/中/快） |
| pitch | 音高（低/中/高） |
| accent | 口音（如有） |
| emotion_range | 情绪表现力（克制/丰富/夸张） |

---

### Structural Scripting Format (Per Shot)

每个镜头的脚本结构：

| Section | Content |
|---------|---------|
| **Core** | 镜头编号 + 场景 + 时长 |
| **Visual** | 画面描述（构图/光线/色调/运镜） |
| **Keyframes** | 起始帧 + 关键动作帧 + 结束帧 |
| **Continuity** | 与前镜头的衔接方式 + 需保持一致的元素 |
| **Characters** | 本镜头出现的角色/产品及其状态 |
| **Audio** | 台词 + 音效 + 背景音乐 |
| **Transition Description** | 入/出镜方式（淡入/切/推等） |
| **What to leave OUT** | 明确禁止出现的元素 |

📖 Wiki: [[AI镜头语言进阶]] — 反向写提示词（镜头包裹动作）、以摄像机为参照系、低角度原理
📖 Wiki: [[AI Camera Movements]] — 完整运镜词库（推拉摇移跟环绕等）
📖 Wiki: [[AI打光五法]] — 侧逆光/轮廓光/蝴蝶光/伦勃朗光/环形光
📖 Wiki: [[AI氛围与色彩控制]] — 氛围三要素（明暗/冷暖/虚实）、调色三法
📖 Wiki: [[视觉平衡与动线构图]] — 三分法、负空间、动线引导

---

### Transition Rules

| 类型 | 用法 | 适用场景 |
|------|------|---------|
| Cut | 直接切换 | 大多数场景 |
| Fade In/Out | 淡入/淡出 | 开场/结束/时间跳转 |
| Dissolve | 叠化 | 情绪过渡、时间流逝 |
| Whip Pan | 甩镜 | 动作戏、快速切换 |
| Match Cut | 匹配剪辑 | 形状/动作/声音匹配连接两场戏 |

📖 Wiki: [[Cut Priority Method]] — 删减优先级（安全→较安全→有风险→绝对不能删）

---

### Audio Rules

- 台词优先于音效，音效优先于 BGM
- 同一场景的 BGM 风格保持一致
- 情绪转折点必须有音频变化（BGM 切换/音量变化/静音）
- 对白期间 BGM 音量降至 30% 以下

📖 Wiki: [[AI角色声音控制]] — 声音公式控制音色、声音过程控制语气、标点符号控制语速

---

### Delivery Specifications (The Storyboard Sheet)

最终交付物：一张完整的分镜表，每行一个镜头，包含上述所有字段。

📖 Wiki: [[Show Don't Tell]] — 用动作/物件/画面展示信息，不用描述性语言直接说出来
📖 Wiki: [[Scene Value]] — 每个场景必须有价值变化（+→- 或 -→+），没有价值变化的场景只是描述

---

## 2. Standard Workflow

### [STATE 1: DISCOVERY & VALIDATION]

**Current Step**: STATE 1: DISCOVERY & VALIDATION
**Next Step**: STATE 2 (Character Design)

**Goal**: 锁定技术规格和风格指南，确保在进入角色设计和脚本制作前，所有关键参数已明确。

**Output Format**: 需求确认清单

**Details** — 收集以下信息：

**项目基础信息：**
- 视频类型：产品广告/品牌故事/教学演示/短剧叙事/科普解说等
- 总时长：目标视频长度（秒）
- 画幅比例：16:9（横屏）/ 9:16（竖屏）/ 1:1（方形）

**视觉风格：**
- 写实摄影风格 / 2D 插画/动画 / 3D 渲染（如皮克斯风格）/ 动漫/二次元 / 手绘素描 / 其他

**内容准备情况：**
- 剧本/脚本：是否已有完整剧本或分镜脚本
- 参考素材：是否有参考图片、视频或风格参考

**主要元素：**
- 角色数量：几个主要角色（人物/吉祥物/虚拟角色等）
- 产品展示：是否需要展示产品，几个产品
- 特殊元素：需要特别注意的视觉元素（身体部位特写/品牌logo/特效等）

**音频需求：**
- 对白：角色是否需要说话/唱歌
- 旁白：是否需要画外音解说
- 音效/BGM：对音频有特殊要求吗

**镜头结构：**
- 多镜头叙事（有剪辑、转场）还是单镜头连续拍摄（一镜到底）

**Bypass Rule**: 用户提供完整创意 brief（含类型/时长/比例/风格/角色数量/产品/音频需求等关键信息）→ 快速总结确认 → 直接进入 STATE 2

**Next Step Gate**: 用户确认需求 → 进入 STATE 2

---

### [STATE 2: CHARACTER_DESIGN] — The Visual Bible

**Current Step**: STATE 2: CHARACTER_DESIGN
**Next Step**: STATE 3 (Storyboard Production)

**Goal**: 建立所有角色/产品的视觉圣经（Visual Bible），确保后续所有镜头使用一致的视觉资产。

---

**Step 1: 识别需要注册的元素**

根据 STATE 1 确认的信息，列出所有需要建立视觉标准的元素：

| 元素类型 | 触发条件 |
|---------|---------|
| **角色 (Character)** | 所有主要人物/虚拟角色 |
| **产品 (Product)** | 需要展示的产品 |
| **非人类角色 (Non-Human Character)** | 动物、吉祥物、机器人等 |
| **身体部位演员 (Body Part Actor)** | 同一身体部位（如手部、眼睛）在 2 个及以上镜头中出现 |

---

**Step 2: 为每个元素建立档案**

**A. 角色 (Character)**
- `unique_id`：唯一标识符（如 hero_maya）
- `role`：角色定位（主角/配角/反派等）
- `appearance`：年龄、体型、身高、肤色、面部特征
- `outfit_description`：服装、配饰、材质、颜色
- `voice_actor_id`：如果有对白，分配配音 ID

📖 Wiki: [[AI角色资产搭建]] — 男/女角色妆造差异、妆造提示词公式、状态决定细节、活人感、微表情三控

**B. 产品 (Product)**
- `unique_id`：唯一标识符（如 product_jar）
- `appearance`：形状、颜色、材质、尺寸
- `mechanical_properties`：如何使用、如何展示

**C. 非人类角色 (Non-Human Character)**
- `unique_id`、`species_or_type`、`appearance`、`movement_style`

**D. 身体部位演员 (Body Part Actor)**
- `unique_id`、`body_part`、`appearance`（肤色、质感等）

---

**Step 3: 参考图生成规则**

| 情况 | 操作 |
|------|------|
| 用户提供了参考图 | 直接使用作为视觉标准 |
| 知名公众人物/产品 | 先网络搜索官方图像，展示给用户确认后使用 |
| 原创虚构元素 | 生成参考图（Reference Sheet），等待用户批准 |

---

**Step 4: 生成标准参考图 (Reference Sheet)**

根据元素类型生成不同格式的参考图：

- **角色/产品**: 三视图（正面、3/4侧面、背面），白色背景，无文字标注
- **身体部位**: 多角度参考图
- **会变形的对象**: 初始状态 + 最终状态两套图

**生成公式**:
```
[类型]: [角度] of [主体] + [详细特征] + [视觉风格] + 左右排列在白色背景上，无文字、无水印、无标注
```

---

**Step 5: 配音档案（如有对白/旁白）**

为每个需要说话的角色/旁白定义：
- `voice_actor_id`：配音 ID
- `type`：画内对白 or 画外旁白
- `gender`、`tone`、`pace`、`language`
- 生成语音样本供用户确认，确认后作为锁定的配音参考音频

---

**Output Format**

以项目列表形式输出：

```
【视觉圣经 - 元素注册表】

角色 1: hero_maya
- 角色定位：主角
- 外观：[年龄/体型/发色等]
- 服装：[描述]
- 配音：voice_maya（温暖、中速、女声）

产品 1: product_jar
- 类型：玻璃瓶装护肤品
- 外观：[形状/颜色/材质]
- 标签：[描述]

【参考图生成计划】
- hero_maya: 三视图（正面/侧面/背面）
- product_jar: 三视图 + 材质特写

【配音样本】
- voice_maya: [生成5秒测试音频]
```

**Next Step Gate** — **[CRITICAL — HARD GATE]**

所有参考图和配音样本生成后，必须等待用户批准：
- ✅ 所有角色/产品外观是否符合预期
- ✅ 参考图质量是否满意
- ✅ 配音样本是否符合角色设定

**只有在用户明确批准后，才能进入 STATE 3（分镜脚本制作）。**

---

### [STATE 3: STORYBOARD PRODUCTION] — Script & Visuals

**Current Step**: STATE 3: STORYBOARD PRODUCTION
**Next Step**: STATE 4 (Assembly)

**Goal**: 将叙事蓝图转化为结构化脚本和视觉预览面板，确保角色/产品一致性并执行分镜图生成。

STATE 3 分为三个阶段：

---

#### Phase 1: Scripting (Thinking) — 脚本编写

**目标**: 将叙事转换为结构化的镜头脚本

**内部工作**: 为每个镜头填写完整的脚本格式，包含以下字段：

**核心字段：**
- 镜头编号、时长（建议 3-5 秒/镜头）
- 叙事功能（建立场景/发展/高潮/解决/过渡/补充）
- 状态（待生成/已生成）

**视觉字段：**
- 视觉提示词（主体 + 动作 + 环境）
- 景别（特写/中景/全景等）
- 机位运动（推拉摇移跟）
- 光线、转场描述

📖 Wiki: [[AI镜头语言进阶]] — 反向写提示词、以摄像机为参照系、低角度原理
📖 Wiki: [[AI Camera Movements]] — 运镜词库（推镜/拉镜/摇镜/移镜/环绕/手持/甩镜/POV 等）

**关键帧：**
- 第一帧描述（构图 + 内容 + 环境/时间/光线）
- 最后一帧描述（构图 + 内容 + 环境/时间/光线）
- 如果相邻镜头是 continuous 边界，它们共享一个关键帧图像

**连续性：**
- 镜头间边界类型（continuous 连续 / scene_cut 场景切换）
- 转场出、转场入

**角色/产品：**
- 本镜头出现的角色/产品 ID 列表
- 外观注意事项

**音频：**
- 音频类型（对白/旁白/无声，三选一）
- 配音 ID、对白内容、旁白内容、音效

📖 Wiki: [[AI角色声音控制]] — 声音公式控制音色、语气、语速

**转场描述：** 每个镜头必须写一段叙事性文字，包含：
- 主体（如已有参考图，不重复描述外观）
- 空间位置关系
- 关键动作（因果链，2-4 个动作）
- 运动方向（左/右/向前/远离）
- 环境 + 时间 + 光线
- 面部表情（单个情绪词，如"惊讶""微笑"）

📖 Wiki: [[AI环境空间设计]] — 环境三层写法（前/中/远景）、环境因果逻辑、场景一致性
📖 Wiki: [[AI导演创作思维]] — 调度优先原则、核心行动驱动、补拍与重构思维
📖 Wiki: [[AI空镜设计]] — 三类空镜（环境/道具/情绪）、节奏控制
📖 Wiki: [[Show Don't Tell]] — 用动作展示信息，不用描述性语言
📖 Wiki: [[Scene Value]] — 每个场景必须有价值变化，否则只是描述

**不要写的内容：**
- 参考图已覆盖的外观细节
- 中间过渡姿态
- 抽象电影术语
- 无动机的视角跳跃

**展示给用户的内容：** 简化版，每个镜头显示：
- 镜头编号 + 时长
- 叙事功能
- 内容描述
- 角色/产品引用（带缩略图）
- 音频信息

**参考图需求汇总：** 脚本完成后，输出一个表格，列出哪些元素需要哪些角度的参考图。

**🛑 Gate**: 必须等待用户批准脚本后才能进入 Phase 2。

---

#### Phase 2: Generation (Execution) — 分镜面板生成

**🚨 [CRITICAL — HARD GATE]**: 这个阶段绝对不能跳过！必须生成面板并获得批准后才能进行任何视频生成。

**目标**: 生成分镜预览面板

**Step 1: 构建去重的关键帧列表**
- 每个镜头需要"第一帧"和"最后一帧"
- 如果镜头 N 和 N+1 共享 continuous 边界，它们共享交界处的关键帧（只生成一次）
- scene_cut 边界的镜头各自独立
- 示例：3 个连续镜头 → 生成 [KF-A, KF-B, KF-C, KF-D] = 4 张图，而不是 6 张

**Step 2: 生成分镜面板图像**

**分镜面板提示词模板：**
```
1. [视觉风格]. [地点], [时段], [光线].
2. [空间布局+主体状态描述]
3. [参考图绑定]：第一张图作为[角色参考]，第二张图作为[产品参考]...
4. 不包含：参考图已覆盖的外观、电影术语、通用质量关键词
```

**[MANDATORY] 环境一致性**: 每个面板提示词必须指定地点、时间、光线、天气/氛围（如相关）。如果脚本未指定，从叙事上下文推断并在 Phase 1 锁定。

**Step 3: 批量生成并展示**
- 批量生成所有面板
- 展示所有面板
- 标注每张图服务于哪些镜头

**🛑 Gate**: 必须等待用户批准所有面板后才能进入 Phase 3。

---

#### Phase 3: Unit Assembly — 生成单元组装

**目标**: 将镜头打包成适合 AI 生成的单元（每个 ≤ 15 秒）

**Step 1: Shot Grouping — 镜头分组**

**合并条件：**
- 同场景
- continuous 边界
- 相同音频类型
- 合并后总时长 ≤ 15 秒

**拆分条件：**
- scene_cut 边界
- 不同音频类型
- 合并后总时长 > 15 秒

**规则：**
- 每单元 2-3 个镜头最佳，4 个为上限
- 每单元覆盖一个连贯的动作弧
- 严格分区，不重叠

**Step 2: Build Unit Packages — 构建单元包**

**A. continuous 单元（无缝视觉过渡 — 使用首尾帧路径）：**
- `start_frame`：单元的第一个关键帧图像（Phase 2 批准的面板）
- `end_frame`：单元的最后一个关键帧图像
- 对于共享关键帧：使用相同的资源（相同 URL/ID）作为前一单元的 end_frame
- `motion_prompt`：只描述帧之间的运动和过渡，不重复描述起止状态
- `master_references`：主体参考图（如模型支持在首尾帧之外附加额外参考）
- `duration`、`audio_type`、`audio_content`、`voice_reference_audio`（如适用）

**B. scene_cut 单元（硬切或创意转场 — 使用通用参考路径）：**
- `combined_prompt`：合并成员镜头的转场描述为一个叙事段落，添加 `@ImageN as [角色]` 内联引用。提示词必须可以直接发送。
- `reference_images`：首尾关键帧面板 + 主体参考图，总数 ≤ 9 张。共享关键帧只计一次。优先级：身份锚点 > 关键帧面板。
- `duration`、`audio_type`、`audio_content`、`voice_reference_audio`（如适用）

**两种类型共同规则：** 不要重复描述关键帧图像已锚定的起止状态。提示词处理它们之间发生的事情。

**Step 3: Verification & Output — 验证与输出**

展示单元包计划：
- 编号列表：单元 N → 覆盖的镜头、时长、边界类型、提示词预览、参考图数量
- 验证摘要：总单元数、总镜头数（必须 = 脚本镜头数）、总时长（必须 = STATE 1 目标）

**🛑 [MANDATORY STOP]**: 必须等待用户批准单元包后才能进入 STATE 4。

---

#### Output Format

**Phase 1 输出示例：**
```
【分镜脚本】

镜头 1 (3秒) - 建立场景
内容：清晨咖啡店内，阳光透过窗户...
角色：hero_maya [缩略图]
音频：无声
边界：continuous → 镜头2

镜头 2 (4秒) - 发展
内容：Maya拿起产品瓶，特写手部...
角色：hero_maya, product_jar [缩略图]
身体部位：hands_maya
音频：旁白 "全新配方..."
边界：continuous → 镜头3

【参考图需求汇总】
- hero_maya: 已有三视图 ✓
- product_jar: 已有三视图 ✓
- hands_maya: 需要多角度手部参考图
```

**Phase 2 输出示例：**
```
【分镜面板】

关键帧 A (服务于镜头1首帧)
[生成的图像]

关键帧 B (服务于镜头1尾帧 / 镜头2首帧 - 共享)
[生成的图像]
```

**Phase 3 输出示例：**
```
【生成单元包】

单元 1 (continuous, 7秒)
- 覆盖镜头：1, 2
- 起始帧：关键帧A
- 结束帧：关键帧B
- 运动提示词：Maya walks to counter, picks up jar...
- 参考图：hero_maya三视图, product_jar三视图, hands_maya多角度
- 音频：旁白 "全新配方..."

单元 2 (scene_cut, 5秒)
- 覆盖镜头：3
- 组合提示词：@Image1 as Maya, @Image2 as product jar...
- 参考图：关键帧C, 关键帧D, hero_maya, product_jar (共4张)
- 音频：无声

【验证】
- 总单元数：2
- 总镜头数：3 ✓
- 总时长：12秒 ✓
```

---

#### 关键执行规则

- **Phase 2 不可跳过** — 这是硬性要求
- **环境一致性** — 同场景镜头的环境必须一致
- **关键帧去重** — continuous 边界共享关键帧，只生成一次
- **单元时长限制** — 每单元 ≤ 15 秒
- **严格门控** — 每个 Phase 完成后必须等待用户确认

---

### [STATE 4: ASSEMBLY] — Production & Final Delivery

**Current Step**: STATE 4: ASSEMBLY
**Next Step**: 交付完成

**Goal**: 生成视频 + 音频，最终交付

---

#### Step 1: Video + Audio Generation (per unit package)

**🚨 [CRITICAL]**: 每个单元包 = 一次视频生成调用。绝不能将单元拆回单个镜头。

**生成顺序**: 所有单元并行启动生成。

**模型选择与参考绑定（按单元类型）：**

**A. continuous 单元 → 首尾帧路径（视频插值 VideoInterp）**

首尾帧路径强制模型在两个精确帧之间插值，比通用参考路径产生更优秀的视觉连续性。

| 音频情况 | 模型选择 | 参数绑定方式 |
|---------|---------|-------------|
| 有音频 | Seedance 2.0 | 通过专用 API 参数传递 start_frame_image + tail_frame_image（不是通过 image_list 参考模式）。额外的主体参考图可以作为 image_list 与帧一起传递。 |
| 无音频 | 优先 MiniMax Hailuo 2.3 或 Kling V2.5 Turbo | 它们的专用首尾帧转视频端点产生更优秀的插值。注意：这些模型只接受起始+结束帧，没有额外参考槽位。 |

提示词：使用单元包的 motion_prompt，只关注运动/过渡，不使用 @ImageN 语法（帧通过 API 参数绑定）。

共享关键帧绑定：同一图像资源必须作为单元 N 的 end_frame 和单元 N+1 的 start_frame 传递。使用相同的 URL/资源。

**B. scene_cut 单元 → 通用参考路径**

| 模型 | 参考绑定 |
|------|---------|
| Seedance 2.0 或 Seedance 2.0 Fast | 附加主体参考图 + 关键帧面板作为参考图像 |

提示词：使用单元包的 combined_prompt，包含 `@ImageN as [角色]` 内联绑定。

规则：
- 每个 `@ImageN` 必须对应一张附加图像
- 每张附加图像必须在提示词中出现并标注角色
- Seedance 2.0 限制：图像 ≤ 9 张，视频 ≤ 3 个，音频 ≤ 3 个
- 最佳：3-5 个参考图

**C. Override — 覆盖**

如果用户指定不同模型，使用用户指定的模型。

**注意：不要依赖工具默认值 — 始终显式指定模型。**

---

**提示词构建规则：**

用户提供详细提示词时：不要重写核心动作描述。锁定 STATE 2 的参考图，如果 > 15 秒则分段，添加绑定，去除抽象约束。只保留具体的视觉描述。

提示词风格：一个连续的叙事段落。顺序讲故事，使用过渡词。前置环境和空间关系。无电影术语。

📖 Wiki: [[AI视觉语法体系]] — 提示词五板块结构（情绪/主体/光线/环境/色彩）
📖 Wiki: [[描述比重原则]] — 主体 50-60%、次要元素 20-30%、环境光线 10-15%、情绪氛围 5-10%
📖 Wiki: [[AI底层机制与高级控制]] — 误解机制三类型（缺省/抽象/不确定）、风格泄漏三解法
📖 Wiki: [[时间补偿机制与动态词学]] — 时间词三态触发（过去式/现在式/将来式）、运动矢量反推
📖 Wiki: [[AI视频动作设计]] — ARC 视角、打斗前摇/中/后结构、减少动词增加方式词
📖 Wiki: [[AI氛围与色彩控制]] — 氛围三要素（明暗/冷暖/虚实）、减法审美
📖 Wiki: [[AI打光五法]] — 侧逆光/轮廓光/蝴蝶光/伦勃朗光/环形光
📖 Wiki: [[一致性锚点原则]] — 锚点保持风格一致，参考图是最有效的锚点
📖 Wiki: [[AI环境空间设计]] — 环境三层写法、因果逻辑、场景一致性

**提示词结构（针对 scene_cut 单元；continuous 单元使用简化的 motion_prompt）：**

```
时长+场景声明：[N]秒。[风格]，[环境]，[时间]，[光线]。
动作开始前的空间布局
动作序列（因果链，每个镜头段2-4个动作）
内联参考绑定：@ImageN as [角色]
音频指示（如有）
约束条件（仅针对该镜头的真实风险）
```

**多主体镜头的物理逻辑规则：**
- 动作前进行空间锚定
- 因果链形式的动作 — 📖 Wiki: [[Causal Chain Audit]]
- 指定运动方向 — 📖 Wiki: [[视觉平衡与动线构图]]

**提示词自检清单（发送前必查）：**
- [ ] 提示词开头标注时长（秒）
- [ ] 指定环境/时间/光线
- [ ] 多主体镜头：动作前说明空间位置
- [ ] 动作形成因果链
- [ ] continuous 单元：首尾帧通过 API 参数绑定；提示词仅运动
- [ ] scene_cut 单元：所有 @ImageN ↔ 附加图像 1:1 匹配
- [ ] 包含音频时设置 sound: "on"
- [ ] 模型匹配边界类型
- [ ] 提示词 ≤ 200 词（简单镜头 30-80 词）。如果超出，拆分单元。
- [ ] 描述字数与元素重要性成正比（次要元素描述不能超过主体）

---

**音频处理：**

| 音频类型 | 处理方式 | 输出 |
|---------|---------|------|
| 对白（dialogue） | 提示词中写"角色说：文本"。视频模型生成带口型同步。 | 嵌入视频 |
| 音效 | 提示词中描述音效。视频模型生成。 | 嵌入视频 |
| 旁白（模型支持音频参考） | 附加锁定的配音参考音频 + 提示词中写 旁白说："文本" | 嵌入视频 |
| 旁白（模型不支持音频参考） | TTS（每个镜头，通过 voice_actor_id 链接） | 独立音轨 |

**🚨 [CRITICAL]**: 绝不对画内对白/歌唱使用 TTS。视频模型生成带口型同步的音频。

**Seedance 2.0 注意事项：**
- 任何音频 → sound: "on"
- 倾向于产生背景音乐幻觉，所以如果只要音效，添加"仅音效，无背景音乐"

---

#### Step 2: Video Assembly — 视频组装

使用视频编辑工具（edit_video_ffmpeg 或 synthesize_media with api_name: concat_video）拼接。

**拼接规则：**

| 边界类型 | 处理方式 |
|---------|---------|
| Continuous 边界 | 后续片段设置 trim_start: 0.3 跳过重叠的共享关键帧画面 |
| Scene-cut 边界 | 无修剪 — 硬切或创意转场 |

**音频处理：**
- 叠加 BGM/旁白轨道（如需要）
- 确保音频同步

**验证：**
- 总时长与 STATE 1 目标一致（考虑每个 continuous 连接处约 0.3 秒的修剪）

**🛑 [MANDATORY STOP]**: 展示最终组装的视频，等待用户确认交付。

---

#### Output Format

**Step 1 输出示例：**
```
【视频生成进度】

单元 1 (continuous, 7秒) - 生成中...
- 模型：Seedance 2.0
- 起始帧：[图像A]
- 结束帧：[图像B]
- 提示词：Maya walks to counter, camera follows smoothly...
- 音频：旁白嵌入
✓ 生成完成

单元 2 (scene_cut, 5秒) - 生成中...
- 模型：Seedance 2.0 Fast
- 参考图：4张（关键帧C, D + hero_maya + product_jar）
- 提示词：5 seconds. Morning cafe, warm lighting...
- 音频：无声
✓ 生成完成

【所有单元生成完毕，准备组装】
```

**Step 2 输出示例：**
```
【视频组装】

拼接顺序：
1. 单元1 (0-7秒)
2. [continuous连接，修剪0.3秒]
3. 单元2 (7-11.7秒)

总时长：11.7秒 ✓
音频轨道：已同步 ✓

【最终视频】
[展示视频]

请确认是否满意，或需要调整？
```

---

#### 关键执行规则（不可违反）

1. 连续单元必须通过专用 API 参数传递首尾帧
2. 场景切换单元必须附加主体参考图 + 关键帧面板
3. 不能跳过 STATE 3 Phase 2（分镜面板生成）
4. 画内对白/歌唱永远不用 TTS，由视频模型处理口型同步
5. 每个视频提示词必须以时长（秒）开头
6. 相同 voice_actor_id = 全程相同声音
7. 一个单元包 = 一次视频调用，不能再拆分

---

## 3. Execution Logic & Rules

### Protocol

所有操作遵循：**用户确认 → 执行 → 展示 → 用户确认** 的循环。

### Flow Control

**Intelligent Bypass (GO)**:
- 用户说"直接开始"或提供完整材料 → 跳过部分确认环节
- 项目类型为"标准产品展示"且有模板 → 走快速通道

**Strict Breakpoints (STOP)**:
- STATE 2 → STATE 3: 所有角色/产品注册完毕
- Phase 1 → Phase 2: 分镜脚本经用户确认
- Phase 2 → Phase 3: 分镜图经用户确认
- Phase 3 → STATE 4: Unit packages 经用户确认
- STATE 4 Step 1 → Step 2: 所有 unit 生成完毕
- STATE 4 Step 2 → 交付: 最终视频经用户确认

**Reversion**:
- 任何 STAGE 用户不满意 → 回到上一个 Gate，修改后重新推进
- 不允许跳过 Gate 直接进入下一阶段

### Interaction Guidance

- 每个 STAGE 开始时先说明当前阶段和目标
- 每个 Gate 到达时明确提示用户需要做什么
- 用户修改需求时，同步更新所有相关文档
- 遇到不确定的视觉细节（如角色服装颜色），先问用户，不自己猜

### Critical Rules (non-negotiable)

**规则 1：确认前不动手**
未收到用户明确确认之前，不执行任何生成操作。

**规则 2：参考图优先** — 📖 Wiki: [[参考图优先原则]]
有参考图时，文字只说明用途，不描述外观。参考图已包含的视觉信息不重复写。

**规则 3：Body Part Actor 必须注册** — 📖 Wiki: [[AI角色资产搭建]]
同一部位出现在 2+ 镜头时必须注册，注册后跨镜头保持一致。

**规则 4：环境一致性** — 📖 Wiki: [[AI环境空间设计]]
同一场景的所有镜头，环境（背景/光线/色调）必须保持一致。

**规则 5：描述比重** — 📖 Wiki: [[描述比重原则]]
主体描述占 50-60%，次要元素不超过 20-30%，次要元素的描述字数不能超过主体。

**规则 6：逻辑自检**
每次生成前执行 Prompt Self-Check，发现矛盾立即修正。

**规则 7：Gate 不可跳**
所有 Mandatory Stop 不可跳过，用户确认后才能进入下一阶段。

**规则 8：精简提示词**
参考图能说的，文字不重复。提示词不超过 200 词（简单镜头 30-80 词），只说核心信息。

---

> 生成于 2026-06-27
