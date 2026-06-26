# 风格化/艺术方向

## 判定条件

路由到此场景的信号：
- 关键词：水彩/油画/版画/炭笔/素描/风格化/艺术/artistic/watercolor/oil painting/charcoal/woodblock/概念图/concept art/风格融合/暗黑/哥特/DST
- 场景特征：需要精确风格锚定 + 媒介物理特征保持 + 可能涉及多风格融合
- 典型请求："画个水彩风"/"暗黑概念图"/"浮世绘×赛博朋克融合"/"DST风格角色"

核心难点（为什么要路由到这里）：
- 抽象风格词（"artistic"/"stylized"）指向宽泛分布→出Generic风格化图，风格化比写实更容易出Generic
- 模型的"清理化"倾向会丢掉媒介的物理特征——水彩的"脏边"被修干净，炭笔的"飞白"被补齐
- 多风格混搭时模型倾向取"平均"而非"创造性组合"
- "画个水彩风"出标准水彩——但你要的是"Tim Burton式的暗黑水彩"，风格锚定精确度决定输出独特性

---

## Prompt组装

### 模板A：媒介锚定模板

```
[画面内容], [具体媒介+技法描述],
[媒介物理特征如 visible brushstrokes / wet edges / stray marks],
[色调/色板], [构图],
on [纸张/画布类型如 textured paper / cold-pressed watercolor paper / aged canvas]
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 画面内容 | ✅ | 画什么 | | abandoned lighthouse / mountain temple |
| 具体媒介+技法 | ✅ | 用什么画+怎么画 | 比单纯"水彩"精确得多（R07） | watercolor on cold-pressed paper, wet-on-wet technique / charcoal and ink on aged paper |
| 媒介物理特征 | ✅ | 媒介的独有痕迹 | **必须显式描述**——对抗模型的"清理化"倾向 | wet-on-wet blending, pigment pooling at edges, visible water marks / impasto brushstrokes, visible canvas texture |
| 色调/色板 | 选填 | 色彩方向 | | muted earth tones with touches of cerulean |
| 构图 | 选填 | 画面组织 | | centered composition / diagonal composition |
| 纸张/画布类型 | 选填 | 承载媒介 | 增加媒介真实感 | textured paper / cold-pressed watercolor paper / aged canvas |

**风格锚定的精度层级**（R07核心）：

| 锚定精度 | 描述方式 | 效果 | 示例 |
|---------|---------|------|------|
| 极模糊 | 抽象风格词 | Generic风格化 | "artistic style" |
| 模糊 | 大类风格词 | 方向对但没特色 | "watercolor style" |
| 中等 | 具体媒介+技法 | 有媒介感但可能Generic | "watercolor on cold-pressed paper, wet-on-wet technique" |
| 精确 | 媒介+技法+年代+地域 | 独特可辨识 | "Japanese woodblock print, Edo period, ukiyo-e style, flat color areas with bold outlines" |
| 最精确 | 参考具体作品/流派 | 精确匹配意图 | "in the style of Hokusai's Great Wave, indigo blue palette" |

**核心逻辑**：共现频率决定编码精度——"watercolor"与无数风格的水彩画共现→编码模糊；"Edo period ukiyo-e"与特定视觉特征高度共现→编码精确。

**媒介物理特征速查**（每种媒介的关键痕迹——风格辨识度的核心）：

| 媒介 | 关键物理特征 | 提示词关键词 |
|------|-------------|-------------|
| 水彩 | 水渍边缘、颜料沉积、湿接渐变 | `wet-on-wet blending, pigment pooling at edges, visible water marks` |
| 油画 | 厚涂笔触、肌理、釉染层叠 | `impasto brushstrokes, visible canvas texture, layered glazing` |
| 炭笔 | 飞白、擦痕、手印、灰阶层次 | `charcoal sketch, smudged edges, stray marks, white chalk highlights` |
| 版画 | 硬边线、有限色板、套色偏移 | `woodblock print, hard edge outlines, limited color palette, registration marks` |
| 丝网印刷 | 平面色块、网点、重复对齐 | `silkscreen print, flat color areas, halftone dots, bold outlines` |
| 铅笔 | 细线条、阴影交叉排线 | `pencil drawing, cross-hatching, graphite shading, fine lines` |

**为什么必须描述物理特征**：模型默认倾向把所有风格"清理化"——水彩的"脏边"被修干净，炭笔的"飞白"被补齐，版画的"套色偏移"被对齐。描述物理痕迹是对抗清理倾向的有效方式（P10）。

**GPT Image 2的house style问题**：清理化倾向特别强——artistic/sketchy风格会被"整理"成干净数字风。对抗方式：描述具体视觉特征而非风格标签——`"chalk pastel on textured paper, visible strokes, rough edges"`而非`"artistic sketchy"`。

#### 示例

用户："画一幅水彩废弃灯塔"
→ `abandoned lighthouse, watercolor on cold-pressed paper, wet-on-wet blending, pigment pooling at edges, muted earth tones with touches of cerulean, centered composition, visible water marks, on textured paper`

---

### 模板B：风格融合模板

```
[内容层描述], rendered in [技法层如 ukiyo-e / watercolor / charcoal sketch],
[构图/结构如 diagonal composition / flat perspective / symmetrical],
[色彩方向如 muted earth tones / neon glow on wet surface]
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 内容层 | ✅ | 画面画什么 | 决定叙事 | cyberpunk neon city / medieval knight charging |
| 技法层 | ✅ | 用什么媒介画 | 决定质感 | ukiyo-e style / watercolor on textured paper / charcoal sketch |
| 构图/结构 | 选填 | 怎么组织画面 | 决定结构 | diagonal composition / flat perspective / symmetrical composition |
| 色彩方向 | 选填 | 色调 | | muted earth tones / neon glow on wet surface |

**避免"平均化"**（R04一次一个意图的延伸）：
- ❌ `watercolor and cyberpunk style` → 模型取两者平均→既不水彩也不赛博朋克
- ✅ `cyberpunk cityscape rendered in watercolor, neon lights bleeding into wet paper, traditional ukiyo-e composition` → 明确哪个是内容、哪个是技法、哪个是构图

**风格融合三要素**：
1. **内容层**：画面画什么（决定叙事）
2. **技法层**：用什么媒介画（决定质感）
3. **构图层**：怎么组织画面（决定结构）

#### 示例

用户："浮世绘风格画赛博朋克"
→ `cyberpunk neon city, rendered in ukiyo-e style, flat color, bold outlines, symmetrical composition, indigo and vermilion palette`

用户："水彩画中世纪骑士"
→ `medieval knight charging, rendered in watercolor on textured paper, diagonal composition, wet-on-wet color bleeding, muted steel and crimson tones`

---

### 模板C：暗黑概念图模板

```
[主体描述], dark fantasy concept art,
[媒介如 charcoal and ink on aged paper],
[光影如 low-key single source from upper left, chiaroscuro],
[氛围如 unsettling atmosphere, creeping shadows],
[色调如 muted earth tones, limited palette of ochre and umber],
sketchy lines, stray marks, textured paper
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 主体描述 | ✅ | 画什么 | | ancient creature in a ruined cathedral |
| 媒介 | 选填 | 默认charcoal+ink | 暗黑风适合粗糙媒介 | charcoal and ink on aged paper |
| 光影 | ✅ | 单一光源+大面积阴影 | 不是纯黑，是"有温度的暗" | low-key single source from upper left, chiaroscuro |
| 氛围 | ✅ | 情绪方向 | 具体词 | unsettling atmosphere, creeping shadows, ancient decay |
| 色调 | 选填 | 低饱和暖色暗色 | 赭石/土褐/深棕——不是纯黑 | muted earth tones, limited palette of ochre and umber |
| 质感词 | ✅ | 粗糙纹理+手绘线 | 对抗清理化 | sketchy lines, stray marks, textured paper |

---

### 模板D：DST风格模板

```
[主体描述], Don't Starve Together style,
Tim Burton aesthetic, hand-drawn ink sketch,
rough sketchy lines with stray marks, charcoal and ink on aged paper,
limited color palette (9-14 colors), low saturation, warm undertones,
cut-paper shadow effect, textured paper background
```

**DST风格关键视觉特征**（Don't Starve Together = Tim Burton + Edward Gorey）：
- 线条：反复描、毛刺飞白、stray marks——不是干净向量线
- 色板：极有限（9-14色）、低饱和、暖色调
- 纸张感：纹理叠加、cut-paper投影阴影
- ❌ 不是像素风，不是干净数字绘，不是过度做旧

⚠️ **GPT Image 2注意**：直接写"sketchy, artistic style"会被house style清理化。必须写具体物理特征："rough sketchy lines with stray marks, charcoal texture, visible smudges on textured paper"（P10）

---

### 模板E：水彩专用（SD参数）

水彩在SD中需要特殊参数——高CFG破坏水彩的不确定性美感：

- **CFG**：7-8（不要太高——水彩的美在"不可控"的颜料行为，高CFG强行控制反而出丙烯感）
- **Steps**：30+（高步数让渐变过渡更自然）
- **负向词**：排除厚重/油画质感——`oil painting, impasto, thick paint, heavy texture`
- **采样器**：DPM++ SDE Karras（比2M更适合水彩的柔和过渡）

---

## 诊断路由

| 观察到 | 可能原因 | 修复动作 | 规则 |
|--------|---------|---------|------|
| 风格Generic | 风格锚定太模糊 | 升级锚定精度——具体媒介+技法+年代+地域 | R07 |
| 水彩出丙烯感 | 高CFG破坏不确定性 | SD: CFG降到7-8，负向词排除厚重质感 | R11 |
| 风格融合平均化 | 没区分内容层/技法层/构图层 | 明确每层用哪个风格，不写"X and Y style" | R04 |
| 媒介物理特征丢失 | 模型"清理化"倾向 | 显式描述物理痕迹（水渍/飞白/套色偏移） | P10 |
| GPT Image 2清理化 | House style倾向 | 描述具体视觉特征而非风格标签 | P10 |
| 像素风出不来 | AI默认高分辨率软边缘 | 用像素LoRA+触发词+Aseprite后处理（见scene-game-assets.md） | R12 |
| 艺术家风格不像 | 编码器对名字的映射弱 | Flux/国产模型：描述风格特征而非引用名字 | R07 |
| 暗黑风变成纯黑 | 没有指定"有温度的暗" | 用低饱和暖色暗色（赭石/土褐/深棕）+单一光源 | R08 |

---

## 场景必检项

```
□ 风格锚定精度够吗？（不是"水彩"而是"水彩湿画法在冷压纸上"）
□ 媒介物理特征写了？（水渍/飞白/套色偏移/笔触——对抗清理化）
□ 风格融合？→ 三要素明确了吗？（内容层/技法层/构图层）
□ GPT Image 2？→ 描述具体视觉特征，不写风格标签
□ 暗黑风？→ 有温度的暗（低饱和暖色）+ 单一光源 + 粗糙质感
□ DST风格？→ 关键视觉特征对齐（反复描线条/极有限色板/纸张感）
□ SD水彩？→ CFG 7-8 + DPM++ SDE Karras + 负向词排除油画
```

---

## 模型注意

- **MJ**：风格化能力最强——艺术家名直接写有效（训练数据中名字-风格配对密集）；`--s 500-750`高风格化强度；`--niji 6`二次元
- **Flux**：描述风格特征比引用名字更有效——"thick impasto brushstrokes"比"by Van Gogh"好；减法思维——不写画质词
- **SD**：水彩/暗光需特殊参数；ControlNet可约束构图；LoRA生态最丰富（特定风格LoRA）
- **GPT Image 2**：House style会清理化——必须写具体物理特征；对话式迭代可逐步调整风格
- **国产模型**：中文风格描述效果好——"工笔画"、"水墨风"比英文编码更精确
