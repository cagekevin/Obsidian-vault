# 文字海报/排版设计

## 判定条件

路由到此场景的信号：
- 关键词：海报/poster/Logo/排版/typography/封面/cover/文字/文字渲染/text/标题/title/品牌/brand/社交媒体封面/banner
- 场景特征：需要在画面中渲染可读文字 + 控制文字位置/字体/与视觉风格融合
- 典型请求："做一张夏日音乐节海报"/"设计一个Logo"/"中文海报标题用黑体"/"社交媒体封面带标题"

核心难点（为什么要路由到这里）：
- 文字渲染是AI最硬的技术瓶颈——绝大多数模型不理解拼写，只理解语义，文字乱码是常态
- 文字在画面中的位置、大小、对齐方式需要精确控制——自然语言无法精确指定"标题在顶部居中24px"
- 中文汉字和英文字母的渲染难度不同——不同模型的中英文能力差异极大
- 文字必须和画面视觉风格统一——不能"画面很美但字像贴上去的"

---

## Prompt组装

### 模板A：事件海报（GPT Image 2）

```
a poster for [事件名], featuring [画面主体],
title "[大标题]" in [字体风格如 bold sans-serif / elegant script],
[副标题/日期/地点等信息],
[视觉风格如 minimalist / vintage / cyberpunk],
[色彩基调]
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 事件名 | ✅ | 海报主题 | | summer music festival / product launch |
| 画面主体 | ✅ | 海报的视觉核心 | | a sunset beach stage / a glowing product silhouette |
| 大标题 | ✅ | 需要渲染的文字 | **必须用引号包裹**——区分"要渲染的文字"和"描述文字的词" | "SUMMER FESTIVAL" |
| 字体风格 | ✅ | 文字的视觉特征 | 指定视觉风格而非字体名——`bold sans-serif`有效，`Helvetica`无效（模型不关联字体名到视觉） | bold sans-serif / elegant script / handwritten / neon sign |
| 副标题/信息 | 选填 | 辅助文字 | **短文字比长文字可靠**——3-5词标题成功率远高于整段文字；**大字比小字可靠**；多行文字分行描述位置和内容 | subtitle "JULY 2025" at the bottom, "NYC" in small text |
| 视觉风格 | 选填 | 海报整体风格 | | minimalist / vintage / cyberpunk / hand-drawn |
| 色彩基调 | 选填 | 色调锁定 | | warm amber palette / neon pink and cyan |

**GPT Image 2特有**：可多轮对话式迭代——先生成基础海报，再要求"把标题字体改成手写体"或"把日期移到右下角"

#### 示例

用户："做一张夏日音乐节海报"
→ `a poster for summer music festival, featuring a sunset beach stage with silhouettes of palm trees, title "SUMMER FESTIVAL" in bold sans-serif, subtitle "JULY 2025" at the bottom, minimalist style, warm amber and coral palette`

---

### 模板B：Logo设计（Ideogram JSON）

```json
{
  "high_level_description": "logo for [品牌], [行业/调性]",
  "style_description": "[风格如 modern minimalist / vintage / playful]",
  "compositional_elements": [
    {"type": "object", "position": "center", "prompt": "[图标元素描述]"},
    {"type": "text", "position": "bottom", "prompt": "[品牌名]"}
  ]
}
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| high_level_description | ✅ | 总描述 | 品牌+行业+调性 | "logo for BrewCraft, artisan coffee brand" |
| style_description | ✅ | 风格 | | "modern minimalist, clean lines" |
| compositional_elements | ✅ | 画面元素 | 每个元素有独立语义空间——不会颜色污染 | 图标+文字各为一个元素 |
| type | ✅ | object或text | 区分图形元素和文字元素 | |
| position | ✅ | 位置 | 可视化工具可画区域框+填描述→自动生成 | center / top / bottom |
| prompt | ✅ | 元素描述 | text类型填需要渲染的文字内容 | "BrewCraft" |

**Ideogram优势**：JSON格式精确控制元素位置，每个元素独立语义空间防止颜色污染。Prompt Builder可视化工具可画区域框+填描述→自动生成JSON。

---

### 模板C：中文海报（GPT Image 2 / Seedream）

```
一张[类型]海报，主题是"[主题]",
主标题"[大标题]"用[字体风格如 黑体/手写体/宋体],
[副标题/信息],
[画面描述], [色彩基调]
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 类型 | ✅ | 海报类型 | | 活动宣传 / 产品推广 / 节日祝福 |
| 主题 | ✅ | 海报主题 | 用引号包裹 | "中秋节" / "新年特卖" |
| 大标题 | ✅ | 需渲染的中文文字 | 用引号包裹；中文渲染必须选对模型 | "花好月圆" |
| 字体风格 | ✅ | 中文字体特征 | 黑体=无衬线/宋体=衬线/手写体=书写感 | 黑体 / 宋体 / 手写体 |
| 副标题/信息 | 选填 | 辅助文字 | 简短为佳 | 副标题"阖家团圆" |
| 画面描述 | 选填 | 视觉内容 | | 月亮、桂花、玉兔剪影 |
| 色彩基调 | 选填 | 色调 | | 暖金色和深蓝色调 |

**中文渲染模型选择**：GPT Image 2中文渲染高 + Seedream 5.0中文渲染强。其他模型中文弱。

#### 示例

→ `一张节日祝福海报，主题是"中秋节"，主标题"花好月圆"用宋体，副标题"阖家团圆"，月亮桂花玉兔剪影，暖金色和深蓝色调`

---

### 模板D：社交媒体封面

```
[宽屏构图描述],
text "[标题]" in [字体风格] at [位置如 top center],
[背景画面], [色彩基调],
social media banner, 16:9 aspect ratio
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 宽屏构图描述 | ✅ | 横向布局 | 适配16:9 | minimalist geometric shapes on left side |
| 标题 | ✅ | 需渲染文字 | 引号包裹 | "CREATIVE STUDIO" |
| 字体风格 | ✅ | 文字视觉 | | bold sans-serif |
| 位置 | ✅ | 文字在哪 | | top center / right side |
| 背景画面 | 选填 | 视觉内容 | | gradient background / photo of mountain |
| 色彩基调 | 选填 | 色调 | | deep navy and gold |

---

### 模板E：图文融合海报

文字作为画面中的物理元素（非排版元素）：

```
a [物理载体] reading "[文字]" on [位置/表面],
[场景描述如 rainy street / dark alley],
[光影如 neon glow reflecting on wet surface],
[氛围如 cyberpunk / noir]
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 物理载体 | ✅ | 文字附着的物体 | 文字融入场景的关键 | neon sign / shop sign / book cover / graffiti |
| 文字 | ✅ | 需渲染文字 | 引号包裹 | "OPEN" / "BAR" |
| 位置/表面 | ✅ | 在哪 | | on a brick wall / on a glass door |
| 场景描述 | 选填 | 环境 | | rainy street / dark alley |
| 光影 | 选填 | 光线如何与文字互动 | 文字和画面共享质感的关键 | neon glow reflecting on wet surface |
| 氛围 | 选填 | 整体调性 | | cyberpunk / noir / warm café |

**风格统一原则**——文字必须和画面视觉风格一致：
- **手绘风海报**：`handwritten text, ink on textured paper`——文字和画面共享手绘质感
- **现代极简**：`clean sans-serif, geometric layout, white space`——文字和画面共享极简逻辑
- **复古海报**：`vintage letterpress type, aged paper texture, retro color palette`——文字和画面共享年代感
- **赛博朋克**：`neon sign text, glowing edges, dark urban background`——文字作为发光元素融入场景

#### 示例

→ `a neon sign reading "OPEN" on a brick wall, rainy street at night, neon glow reflecting on wet surface, cyberpunk atmosphere`

---

### 文字渲染模型选择——生死线

文字场景的模型选择不是优化决策，是生死决策（R09）：

| 能力等级 | 模型 | 英文 | 中文 |
|---------|------|------|------|
| 顶级 | GPT Image 2 | 99%+ | 高 |
| 顶级 | Ideogram v3 | 90-95% | 一般 |
| 强 | Seedream 5.0 | 一般 | 中文强 |
| 中等 | Flux 2 Pro | ~65% | 弱 |
| 弱 | MJ V7 | <40% | 弱 |
| 不可用 | SD 1.5/XL | 几乎不可 | 不可 |

**选择逻辑**：
- 英文海报/Logo → Ideogram v3（JSON精确排版）或 GPT Image 2（对话式迭代）
- 中文海报 → GPT Image 2 或 Seedream 5.0
- 短文字+强视觉 → GPT Image 2（综合画面质量+文字渲染都强）
- 长文字+精确排版 → Ideogram v3（JSON格式精确控制元素位置）
- SD+ControlNet版式：预排版文字图→Canny约束→风格填充。最笨但最可控

---

### 文字渲染黄金规则

1. **文字内容用引号包裹**——区分"要渲染的文字"和"描述文字的词"
2. **短文字比长文字可靠**——3-5个词的标题成功率远高于整段文字
3. **先确认文字，再调版式**——文字渲染是硬约束，版式是软约束
4. **大字比小字可靠**——"标题"比"正文"容易渲染对
5. **指定字体风格而非字体名**——`bold sans-serif`有效，`Helvetica`无效
6. **英文比中文可靠**（多数模型）——除了Seedream/GPT Image 2
7. **多行文字分行描述**——不要把多行塞进一个引号，每行单独描述位置和内容
8. **迭代比一次到位可靠**——先出文字正确的基础版，再调整版式和风格

---

## 诊断路由

| 观察到 | 可能原因 | 修复动作 | 规则 |
|--------|---------|---------|------|
| 文字乱码 | 编码器不理解拼写 | 换文字渲染强的模型（GPT Image 2/Ideogram/Seedream） | R09 |
| 文字位置不对 | 自然语言无法精确定位 | 用Ideogram JSON指定position；或GPT Image 2多轮迭代调整 | R09 |
| 中文字渲染差 | 模型中文训练数据少 | 用GPT Image 2或Seedream 5.0 | R09 |
| 文字风格和画面不搭 | 文字描述和视觉风格脱节 | 文字描述加入视觉特征（手写/霓虹/金属等） | P09 |
| 排版太拥挤 | 模型默认填满画面 | 加"generous white space, minimalist layout" | R06 |
| 多行文字对不齐 | 模型不理解排版规则 | 减少文字行数；或用SD+预排版文字图+ControlNet | R09 |
| 文字颜色被场景污染 | 文字和画面在同一语义空间 | 用Ideogram JSON分元素描述；SD用BREAK隔离 | P01 |
| GPT Image 2粗糙手写风出不来 | House style偏干净 | 描述具体视觉特征而非风格标签 | P10 |

---

## 场景必检项

```
□ 模型选对了吗？（文字渲染模型选择表——这是生死线，不是优化选项）
□ 文字内容用引号包裹了？（区分渲染文字和描述词）
□ 字体风格指定了视觉特征？（bold sans-serif有效，Helvetica无效）
□ 文字和画面风格统一了？（手绘→手写体/赛博朋克→霓虹字/极简→无衬线）
□ 多行文字分行描述了？（每行单独位置+内容）
□ 中文文字？→ 确认用GPT Image 2或Seedream
□ 精确排版需求？→ 用Ideogram JSON
□ 短文字优先？大字优先？（硬约束先满足，版式是软约束后调整）
```

---

## 模型注意

- **GPT Image 2**：中英文文字渲染都强；对话式迭代可逐步调整版式；但house style偏干净——粗糙手写风难出
- **Ideogram v3**：英文文字渲染最精确；JSON格式精确控制位置；但中文弱，综合画面质量不如S级
- **Seedream 5.0**：中文文字渲染强；直接用中文提示词；但英文弱
- **Flux/MJ/SD**：文字渲染不可靠——需文字时换模型
- **SD+ControlNet**：预排版文字图→Canny约束，最笨但最可控的方案
