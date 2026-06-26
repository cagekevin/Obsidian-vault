# 角色设计

## 判定条件

路由到此场景的信号：
- 关键词：角色/人物/人物设计/character/character design/人像/portrait/设定图/reference sheet/多角度/换姿势/换服装
- 场景特征：需要多角度一致性 + 跨场景身份保持 + 精确姿态控制
- 典型请求："画一个女骑士角色设定图"/"换个姿势但保持同一个人"/"写实人像，不要油腻感"/"Q版角色设计"

核心难点（为什么要路由到这里）：
- 同一角色在不同角度/场景/姿态下必须保持可辨识——AI每次独立采样没有"记忆"能力
- 身份特征（发色/瞳色/伤疤/配饰）容易在不同生成中漂移
- 手部/肢体崩坏是写实角色的最大痛点

---

## Prompt组装

### 模板A：角色设定图（多角度）

```
[格式锚定] of [角色描述],
multiple views: front view, side view, back view, 3/4 angle,
[不可变特征如 hair color, eye color, signature items],
white background, flat design, clean lines
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 格式锚定 | ✅ | 设定图类型 | "character reference sheet"与多角度图在训练数据中高共现 | character reference sheet / turnaround sheet |
| 角色描述 | ✅ | 画什么角色 | 简洁概括身份 | a young female knight / a sci-fi mercenary |
| 不可变特征 | ✅ | 跨场景不变的身份锚点 | 发色/瞳色/标志性配饰必须显式列出；位置放前面（R03注意力前置） | silver hair, red eyes, scar across left cheek |
| 背景 | 选填 | 默认white background | 设定图用白底保证干净 | white background |
| 视角列表 | ✅ | 需要哪些角度 | 通用写法见模板；Flux用四宫格变体（见下） | front view, side view, back view, 3/4 angle |

**Flux专用变体**（四宫格——一次出四角度，天然一致）：
```
same character, four views: front, side, back, 3/4 angle,
[角色描述], [不可变特征]
```

**多角度一致性方案可靠性排序**：
1. Flux四宫格——一次出四角度，天然一致
2. 角色设定图模板——"reference sheet"与多角度图高共现
3. 图生图锚定——先出满意角色图→用该图作参考→图生图出其他角度（重绘幅度0.3-0.5）
4. LoRA训练——上传5-20张角色图训练专属LoRA，最强一致性但门槛最高

#### 示例

用户："画一个银发红瞳的女骑士设定图"
→ `character reference sheet of a young female knight, multiple views: front view, side view, back view, 3/4 angle, silver hair, red eyes, scar across left cheek, white background, flat design, clean lines`

用户（Flux）："做这个角色的四角度参考"
→ `same character, four views: front, side, back, 3/4 angle, young female knight, silver hair, red eyes`

---

### 模板B：角色场景图（换场景保持身份）

```
[身份锚点前缀: 发色 hair, 瞳色 eyes, 标志性特征],
[角色身份描述] in [新场景],
[服装/姿态], [场景光影], [氛围]
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 身份锚点前缀 | ✅ | 不可变特征 | 必须放提示词最前面——位置权重效应（R03）；发色+瞳色+标志性特征 | silver hair, red eyes, scar across left cheek |
| 角色身份描述 | ✅ | 角色是谁 | 简洁身份+场景 | young female knight in ancient ruins |
| 服装/姿态 | 选填 | 当前场景的服装和动作 | 可变特征，写这里 | wearing dark cape, sword drawn |
| 场景光影 | 选填 | 场景光照 | 用光影三要素：类型+方向+色温 | warm torchlight from the left, volumetric light |
| 氛围 | 选填 | 情绪方向 | 词要具体 | mysterious, ancient, somber |

**关键原理**：不可变特征（发色/瞳色/种族/伤疤/配饰）写成固定前缀，可变特征（服装/姿态/表情/场景）写成可替换后缀。身份锚点必须在最前面——靠前的token权重更高（R03）。

#### 示例

用户："让之前的女骑士站在废墟里"
→ `silver hair, red eyes, scar across left cheek, young female knight in ancient ruins, wearing dark cape, sword drawn, warm torchlight from the left, volumetric light, mysterious atmosphere`

---

### 模板C：角色变体（换服装/表情）

```
图生图模式，参考图为锚定角色图，重绘幅度[0.3-0.5]

[身份锚点前缀], wearing [新服装], [新表情/姿态]
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 身份锚点前缀 | ✅ | 同模板B的固定前缀 | 保持与锚定图一致 | silver hair, red eyes, scar across left cheek |
| 新服装 | ✅ | 变体维度 | 只改一个维度，观察漂移 | wearing formal white dress |
| 新表情/姿态 | 选填 | 变体维度 | 与新服装搭配 | smiling gently, hands clasped |

**重绘幅度控制**：
- 0.2-0.3：微调（只改表情/光照）
- 0.3-0.5：中变（换服装/姿态）
- 0.5-0.7：大变（换场景/动作，但角色可能漂移）

---

### 模板D：写实人像

```
a [年龄段] [性别] with [发色发型], [瞳色] eyes,
natural skin texture, visible pores, matte finish,
[服装], [姿态],
[场景], [光影描述],
shot on [相机+镜头], shallow depth of field
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 年龄段+性别 | ✅ | 基本身份 | Flux中不写"one girl"（触发汪格尔综合症→出动漫风），写"girl"或具体自然语言 | a young woman / a middle-aged man |
| 发色发型 | ✅ | 不可变特征 | 越具体越好 | long wavy auburn hair |
| 瞳色 | 选填 | 不可变特征 | 亚洲角色显式指定`monolid eyes`对抗训练偏见 | hazel eyes / monolid brown eyes |
| 皮肤质感词 | ✅ | 对抗油腻感 | 必加——训练数据"好人像"=磨皮→光滑反光=好皮肤的错误映射 | natural skin texture, visible pores, matte finish |
| 服装 | 选填 | 可变特征 | 按场景搭配 | wearing black turtleneck |
| 姿态 | 选填 | 动作 | | looking slightly to the left, subtle smile |
| 场景 | 选填 | 环境 | | in a dimly lit café |
| 光影描述 | 选填 | 光照三要素 | 类型+方向+色温 | Rembrandt lighting, warm 3200K key light from 45° left |
| 相机+镜头 | 选填 | 增加写实感 | 模型见过带EXIF的专业照片 | Canon EOS R5, 85mm f/1.4 |

#### 示例

用户："写实人像，亚洲女性，不要油腻"
→ `a young woman with long straight black hair, monolid brown eyes, natural skin texture, visible pores, matte finish, wearing white linen shirt, looking at camera with gentle expression, in a sunlit studio, soft diffused key light from overhead, shot on Canon EOS R5, 85mm f/1.4, shallow depth of field`

---

### 模板E：卡通/风格化角色

```
[角色概念],
[风格锚定],
[关键特征],
[姿态/动作],
white background, character design
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 角色概念 | ✅ | 核心创意 | 用视觉语言描述 | a small knight with an oversized sword |
| 风格锚定 | ✅ | 具体风格词 | "卡通风格"太模糊→Generic；用具体锚定词（R07） | chibi proportions, cel-shaded, anime style |
| 关键特征 | ✅ | 身份辨识特征 | 具体到颜色+形状 | silver armor with blue cape, determined expression |
| 姿态/动作 | 选填 | 动态 | | holding sword with both hands, ready stance |

**风格锚定词速查**（比"卡通风格"精确）：
- anime style / cel-shaded — 日式动画
- chibi — Q版大头
- semi-realistic — 半写实
- western cartoon — 美式卡通
- concept art — 概念设计

---

### 姿态控制强度梯度

| 强度 | 方式 | 适用 | 关键词/工具 |
|------|------|------|------------|
| 弱 | 文本描述 | 所有模型 | `standing, arms crossed` / `sitting on chair, leaning forward` |
| 中 | 姿态关键词 | 所有模型 | `dynamic pose` / `contrapposto` / `action stance` |
| 强 | OpenPose + ControlNet | SD系列 | 指定精确关节位置 |
| 强 | 参考图图生图 | 跨模型通用 | 上传参考姿态图 |

---

## 诊断路由

| 观察到 | 可能原因 | 修复动作 | 规则 |
|--------|---------|---------|------|
| 不同角度不像同一人 | 每次独立采样无记忆 | 用四宫格/设定图模板，或图生图锚定 | R10 |
| 角色特征漂移 | 不可变特征未显式指定/未前置 | 固定前缀写身份锚点，位置放最前面 | R03 |
| 手部崩坏 | 手部训练数据不足+空间定位弱 | SD: ADetailer+负向词；其他: 局部重绘修复 | P03 |
| 写实人像油腻 | 磨皮数据→光滑=好皮肤的错误映射 | 加"natural skin texture, visible pores, matte finish" | P02 |
| Flux出动漫风 | "one girl"与动漫数据共现 | 写"girl"或具体自然语言描述，不写"one girl" | R12 |
| 风格化不够/像Generic | 只写"cartoon"太模糊 | 用具体风格锚定词（chibi/cel-shaded等） | R07 |
| 角色像别人 | Generic特征占主导 | 增加特异性描述——具体发型/脸型/疤痕/配饰 | P02 |
| 角色换场景后认不出 | 身份锚点丢失 | 检查身份前缀是否在提示词最前面；图生图锚定 | R03/R10 |
| 迭代中漂移越来越严重 | 在漂移的图上继续迭代 | 回到锚定图重新出发 | R10 |

---

## 场景必检项

```
□ 身份锚点已确定？（不可变特征: 发色/瞳色/伤疤/配饰 → 写成固定前缀）
□ 身份锚点在提示词最前面？（R03位置权重）
□ 多角度需求已选方案？（四宫格/设定图模板/图生图锚定/LoRA）
□ 姿态控制方式已选定？（文本/姿态词/OpenPose/参考图）
□ 写实人像：皮肤质感词已加？（anti-油腻）
□ 写实人像：有无训练偏见风险？（亚洲人→显式指定monolid eyes等）
□ 卡通/风格化：风格锚定够具体？（不是"卡通"而是"chibi, cel-shaded"）
□ 迭代策略：每次只改一个维度？（服装/姿态/场景，观察漂移）
□ 漂移严重？→ 回到锚定图重新出发，不在漂移的图上继续迭代
```

---

## 模型注意

- **多角度一致性**：Flux四宫格是目前最简单有效方案（`same character, four views`）。SD需LoRA+ControlNet OpenPose组合
- **写实人像**：Flux人像油腻需抗油腻词；训练偏见（亚洲人→双眼皮）需显式指定特征
- **风格化角色**：MJ审美加工强但可控性差——需`--s`调低+`--niji`切换二次元
- **卡通角色**：SD+角色LoRA是像素级一致路径，但需要训练门槛
- **GPT Image 2**：对话式迭代适合角色设计（先出基础→要求"把头发改成蓝色"），但风格化弱
- **图生图锚定**：跨模型通用——先出锚定图，再图生图出变体，重绘幅度0.3-0.5
