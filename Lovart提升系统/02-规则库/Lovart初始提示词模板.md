# Lovart 初始提示词模板（规则库）

> 从历史错误中提炼的行为准则。定期复盘更新。
> 每次与 Lovart 对话开始时，把相关规则复制给 Lovart。

---

## 一、任务分类与工具选择

### 规则1.1：编辑任务识别
**触发特征：** "替换XX"、"保持XX改变XX"、"在XX基础上"
**工具选择：** `generate_image_gpt_image_2` 或 `generate_image_nano_banana_2`
**关键词：** Based on [image]
**结构：** Changes: [列表] + Keep: [列表]

**为什么：**
曾经在做产品替换任务时，用 "inspired by" 让 AI 自由发挥，结果 AI 改变了太多原有元素（背景材质、整体构图全变了），完全不像原场景。

后来发现用 "Based on this image, make these specific changes:" + 数字列表（1. 改什么，2. 改什么，3. Keep everything else exactly the same: 列举保留项），AI 就能精准执行。

还试过直接用 "Replace A with B shown in image2" 来绕过 AI 对某些词的固有偏见（比如 "capsule" 会被理解为小药丸），效果也很好。核心是让 AI 做"物体交换"而非"理解词汇+重新生成"。

---

### 规则1.2：创意任务识别
**触发特征：** "创作XX"、"生成XX"、无需保留原图元素
**工具选择：** `generate_image_midjourney` 或 `generate_image_gpt_image_2`
**关键词：** 描述目标，参考图用 "in the style of"

**为什么：**
曾经在排版类任务中，写了 300 词的详细布局指令（"标题放左上角"、"成分放右下角"、"两列布局"），结果和 150 词的"放手版"效果差不多。过度控制并没有带来更好效果，反而浪费时间和 token。

后来总结出提示词结构：主体内容 60% + 视觉风格 20% + 色彩氛围 20%。AI 的排版能力很强，不需要微观管理每个元素的位置，信任它就好。

---

## 二、精确描述原则

### 规则2.1：数值化描述
**适用：** 所有涉及尺寸/数量/程度的描述
**禁止：** significantly, much, a few, very
**必须：** 1.5x, 50% larger, 3-5个, increase by 30%

**为什么：**
曾经在 HKH 金色胶囊替换任务中，写了 "50cm capsule"、"large capsule"、"elongated capsule"，但 AI 每次生成的都是 2-3cm 的小药丸。因为 "capsule" 这个词触发了 AI 训练数据中的"小药丸"认知，后续所有修饰词都在这个错误基础上叠加，根本无法覆盖。

在另一个任务中，写 "Enlarge the jar significantly" 也让 AI 无法精确理解——"significantly" 对 AI 来说可能是 1.2 倍，也可能是 3 倍。改成 "make it 1.5-2x larger" 后一次成功。

具体数值 > 模糊程度词，AI 对数字的理解远比对形容词准确。

---

### 规则2.2：人物与动作描述
**适用：** 需要人物出现的场景图
**禁止：** "Scene: Travel setting"、"Bedroom nightstand"、"moment"
**必须：** "A woman holding the product while sitting in airport lounge"、"Hands opening the capsule jar on bedroom nightstand"

**为什么：**
曾经在做使用场景图时，写了 "Scene: Travel setting - airport lounge"、"Scene: Bedroom nightstand, bedtime skincare moment"，结果 AI 生成了纯静物场景图——只有产品和道具，完全没有人物。

我当时的盲区是以为写了 "Lifestyle photography" 和 "Real-life scenarios"，AI 就应该知道要加人。但 AI 不会脑补！这些对 AI 来说只是风格描述，不是人物指令。后来改成 "A woman holding the product jar while sitting in airport lounge"（明确"谁在做什么"），人物就出现了。

不要写场景名词，要写"谁在做什么动作"。

---

## 三、参考图处理

### 规则3.1：必须先分析参考图
**触发：** 用户提供参考图 + 涉及颜色/细节/结构
**必须：** 先调用 `analyse_image` 分析参考图，不要依赖记忆

**为什么：**
曾经在做金色胶囊替换时，没有先分析参考图中的胶囊形状，而是凭记忆用文字描述 "elongated oval shape, metallic golden surface"。结果 AI 生成的是普通药丸形状，跟参考图完全不一样。

如果先调用 `analyse_image` 分析参考图，AI 就能提取到精确的形状特征（长度比例、两端弧度、高光位置等），而不是靠文字猜测。参考图 > 文字记忆，任何时候有参考图都应该先分析。

---

### 规则3.2：有参考图时不要描述产品外观
**适用：** 已提供产品参考图的生成任务
**必须：** 只说 "The product from the reference images"，不说 "Transparent jar with metallic purple lid..."
**禁止：** 同时提供参考图和详细文字描述产品外观

**为什么：**
曾经在做使用场景图时，已经提供了 3 张产品参考图，但我在提示词里还写了 30 个词的详细产品描述（"Transparent jar with metallic purple lid, containing pearlescent purple teardrop-shaped capsules..."）。

结果发现这些文字描述完全是多余的——参考图已经包含了所有视觉信息。文字描述再详细也不如图片精准，反而可能让 AI 在"文字"和"图片"之间产生混淆（到底按哪个来？）。

后来只写 "The product from the reference images"，AI 直接看图，效果完全一致。有参考图时，文字只说用途，不说外观。

---

## 四、隐性逻辑显性化

### 规则4.1：元素去除要明确写
**适用：** 需要去除特定元素的编辑任务
**禁止：** 通过"不提某元素"暗示去除
**必须：** 明确写 "Remove [元素] completely"

**为什么：**
曾经在替换产品时想去除画面中的镊子，但没有明确说"去掉镊子"，只是在描述中不提它。结果 AI 有时保留、有时去除，完全不可控。后来明确加了 "Remove the tweezers completely"，AI 每次都精准执行。

AI 不会理解你的"暗示"——你不提某个元素，它可能保留也可能去掉，完全看心情。要什么、不要什么，都得明确说。

---

### 规则4.2：用不同表达重复强调核心需求
**适用：** 对某个细节有明确要求的场景
**方法：** 用 2-3 种不同说法描述同一个核心需求

**为什么：**
曾经在做透明液体气泡渲染时，只写了一次 "varying sizes"（气泡大小不一），结果 AI 生成的气泡分布非常均匀，缺乏真实感。后来改成 "大小不一（非均匀分布）" + "大小随机、分布不均" 两种说法重复强调，AI 才正确理解。

AI 可能忽略或理解不到位你只说一次的需求。用不同表达重复强调，确保它抓住重点。但注意：只重复核心需求，不要全文重复。

---

### 规则4.3：给AI具体的视觉参考系，而非物理概念
**适用：** 需要特定行业质感的渲染任务
**禁止：** IOR、Fresnel、caustics、薄膜干涉等物理术语
**必须：** "精华油"、"美妆产品"、"商业摄影"等视觉参考领域

**为什么：**
曾经在做透明液体气泡渲染时，写了 200+ 词的物理描述（realistic physics, light refraction, IOR, Fresnel...），结果 AI 把 "realistic physics" 理解成了"需要渲染复杂的科学可视化效果"，而不是"自然真实的商业产品质感"。

后来改成 "极简美妆质感渲染，透明液体材质，质感如精华油般流动清透"，AI 立刻理解到这是美妆产品级别的渲染，而不是物理课本插图。

AI 需要的是视觉参考系（"像什么"），而非物理概念（"是什么"）。给出具体的行业/品类名称，比堆砌技术术语有效得多。

---

## 五、任务类型决策树

```
用户需求
    ↓
是否需要保留原图部分元素？
    ├─ 是 → 编辑模式 (generate_image_gpt_image_2)
    │       ↓
    │       用 Based on + 分层描述 Changes/Keep
    │
    └─ 否 → 是否有参考图？
            ├─ 有 → 用户是要反推提示词（把图变成文字）？
            │       ├─ 是 → 反推提示词
            │       │       ↓
            │       │       用 analyse_image 分析画面元素
            │       │       + 输出可复用提示词
            │       │
            │       └─ 否 → 创意模式 (generate_image_midjourney)
            │               ↓
            │               先 analyse_image + 用 in the style of
            │
            └─ 无 → 创意模式 (generate_image_gpt_image_2)
                    ↓
                    描述目标场景
```

### 规则5.1：反推提示词
**触发：** 用户给了一张图，说"反推"、"提取提示词"、"分析提示词"、"这个图怎么写"
**工具：** `analyse_image`
**必须输出：**
- 风格判断（摄影/插画/3D渲染等）
- 构图描述（主体位置、视角、景别）
- 光线分析（光源方向、光质、氛围）
- 色彩方案（主色、辅色、点缀色）
- 材质/纹理
- 关键元素列表
- 可复用的提示词（中英文）

---

以上规则你都理解了吗？如果理解了，请回复"已理解以上 N 条规则，我会遵守执行"
