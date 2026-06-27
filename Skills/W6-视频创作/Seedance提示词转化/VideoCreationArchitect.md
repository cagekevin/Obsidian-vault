# Video Creation Architect

> Seedance 视频创作 Skill — 从分镜到出片的完整流水线。

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

#### Visual Standard

所有参考图必须：白色或纯色背景、无文字/边框/UI 元素、主体居中、光线均匀。

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

---

### Transition Rules

| 类型 | 用法 | 适用场景 |
|------|------|---------|
| Cut | 直接切换 | 大多数场景 |
| Fade In/Out | 淡入/淡出 | 开场/结束/时间跳转 |
| Dissolve | 叠化 | 情绪过渡、时间流逝 |
| Whip Pan | 甩镜 | 动作戏、快速切换 |
| Match Cut | 匹配剪辑 | 形状/动作/声音匹配连接两场戏 |

---

### Audio Rules

- 台词优先于音效，音效优先于 BGM
- 同一场景的 BGM 风格保持一致
- 情绪转折点必须有音频变化（BGM 切换/音量变化/静音）
- 对白期间 BGM 音量降至 30% 以下

---

### Delivery Specifications (The Storyboard Sheet)

最终交付物：一张完整的分镜表，每行一个镜头，包含上述所有字段。

---

## 2. Standard Workflow

### [STATE 1: DISCOVERY & VALIDATION]

**Goal**: 确认用户需求，判断是否走全流程
**Output Format**: 需求确认清单
**Details**:
- 视频类型（短剧/科普/产品展示等）
- 风格（皮克斯 3D/写实/插画等）
- 时长
- 是否有剧本/脚本
- 角色数量
- 是否有产品需要展示
**Bypass Rule**: 用户明确说"直接开始"或提供完整剧本时跳过
**Next Step Gate**: 用户确认需求 → 进入 STATE 2

---

### [STATE 2: CHARACTER_DESIGN] — The Visual Bible

**Goal**: 建立角色/产品视觉圣经
**Action**:
1. 列出所有需要注册的角色/产品/身体部位
2. 为每个元素填写 Master Sheet
3. 生成/收集参考图
**Reference Image Handling**:
- 用户提供的 → 直接使用
- 没有的 → 用 Generation Formula 生成
**Output Format**: Character & Product Master Sheet 完整表格
**Details**: 必须包含所有 Element Types，Body Part Actor 触发检测
**Next Step Gate**: 所有元素注册完毕 → 进入 STATE 3

---

### [STATE 3: STORYBOARD PRODUCTION] — Script & Visuals

**Goal**: 生成分镜脚本 + 画面描述

**Phase 1: Scripting (Thinking)**
- 根据剧本拆解镜头
- 每个镜头填写 Structural Scripting Format
- 检查 continuity（跨镜头一致性）

**Phase 2: Generation (Execution)**

**[CRITICAL — HARD GATE]**: 分镜脚本必须经用户确认后才能进入生成

**Generation procedure**:
1. 每 3-5 个镜头一组生成分镜图
2. 每组生成后展示给用户确认
3. 确认后再生成下一组

**Storyboard Panel Prompt Template**:
```
[场景描述], [构图], [光线], [色调], [角色状态], [产品位置], [风格]
```

**[MANDATORY] Environment Consistency**: 同一场景的镜头之间，环境（背景/光线/色调）必须保持一致

**Workflow**:
```
剧本 → 拆镜头 → 填脚本格式 → 用户确认 → 生成分镜图 → 用户确认 → 进入 Phase 3
```

**Phase 3: Unit Assembly**

**Step 1: Shot Grouping**
- 按场景分组
- 标记 continuous（连续动作）和 scene_cut（场景切换）

**Step 2: Build Unit Packages**

| Unit Type | 规则 |
|-----------|------|
| **A. continuous units** | 连续动作镜头，共享 start-end-frame，需保持角色/环境一致 |
| **B. scene_cut units** | 场景切换镜头，独立生成，需保证风格一致 |
| **Both types** | 每个 unit 包含：镜头列表 + 角色状态 + 参考图 + 提示词 |

**Step 3: Verification & Output**
- 检查所有镜头是否已分组
- 检查每个 unit 的参考图是否正确绑定
- 输出 unit packages

**[MANDATORY STOP]**: Unit packages 必须经用户确认后才能进入 STATE 4

---

### [STATE 4: ASSEMBLY] — Production & Final Delivery

**Goal**: 生成视频 + 音频，最终交付

**Step 1: Video + Audio Generation (per unit package)**

**[CRITICAL]**: 严格按照 unit 顺序生成，不能跳序

**Generation Order**: continuous units → scene_cut units

**Model & Reference Binding by Unit Type**:

| Unit Type | 绑定方式 |
|-----------|---------|
| **A. continuous units** | start-end-frame path — 首帧 + 尾帧参考，中间帧自动插值 |
| **B. scene_cut units** | general reference path — 角色/产品参考图 |
| **C. Override** | 手动指定某镜头的参考图，覆盖默认绑定 |

**Prompt Construction Rules**:
1. 每个 unit 的提示词必须包含：场景 + 角色状态 + 运镜 + 光线
2. continuous unit 的提示词要强调"动作连续性"
3. scene_cut unit 的提示词要强调"风格一致性"
4. 不要重复描述参考图已包含的信息

**Physical Logic Rules**:
- 角色在同一场景中的位置不能突变
- 手持物品在连续镜头中不能消失/变换
- 光线方向在同一场景中保持一致
- 角色服装/妆造在连续时间线中保持一致

**Prompt Self-Check (MANDATORY)**:
- [ ] 角色状态是否与上一镜头衔接
- [ ] 产品位置/状态是否一致
- [ ] 光线方向是否与场景设定一致
- [ ] 运镜方式是否符合分镜要求
- [ ] 是否有逻辑矛盾（物体消失/位置突变等）
- [ ] 提示词是否精简（参考图能表达的不重复描述）

**Audio handling**:
- 台词 → 按 voice profile 生成
- 音效 → 匹配画面动作
- BGM → 匹配场景情绪
- 输出格式：每个 unit 一个音频轨道 + 时间码

**Step 2: Video Assembly**
1. 按 unit 顺序拼接视频片段
2. 添加转场效果
3. 同步音频轨道
4. 输出最终视频

**[MANDATORY STOP]**: 最终视频经用户确认后才能交付

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

**规则 2：参考图优先**
有参考图时，文字只说明用途，不描述外观。参考图已包含的视觉信息不重复写。

**规则 3：Body Part Actor 必须注册**
同一部位出现在 2+ 镜头时必须注册，注册后跨镜头保持一致。

**规则 4：环境一致性**
同一场景的所有镜头，环境（背景/光线/色调）必须保持一致。

**规则 5：逻辑自检**
每次生成前执行 Prompt Self-Check，发现矛盾立即修正。

**规则 6：Gate 不可跳**
所有 Mandatory Stop 不可跳过，用户确认后才能进入下一阶段。

**规则 7：精简提示词**
参考图能说的，文字不重复。提示词不超过 150 词，只说核心信息。

---

> 生成于 2026-06-27
