# 场景/风景

## 判定条件

路由到此场景的信号：
- 关键词：风景/场景/landscape/scenery/背景/background/环境/environment/夜景/暗光/氛围图
- 场景特征：构图+光影+配色三要素控制，需要"恰好是你想要的那种好看"
- 典型请求："画一片迷雾森林"/"赛博朋克城市夜景"/"黄金时刻的湖边"/"暗光概念图"

核心难点（为什么要路由到这里）：
- AI默认出正面居中构图——偏离需要显式指令且效果不总是可靠
- 场景情绪70%来自光影——模糊的光照描述=模糊的情绪
- 没有色彩锁定时模型用训练数据中的"平均配色"→Generic配色
- 未提及的元素由模型自行填充——要什么、不要什么必须显式控制

---

## Prompt组装

### 模板A：氛围风景（通用）

```
a [主体] at [时间/季节], [核心光影], [构图方向], [色彩基调]
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 主体 | ✅ | 画什么场景 | 简洁具体 | misty mountain valley / ancient forest clearing |
| 时间/季节 | 选填 | 时间语境 | 强烈影响光影和配色 | at dawn / in autumn / at blue hour |
| 核心光影 | ✅ | 光照三要素 | 类型+方向+色温，避免"dramatic lighting"等宽泛词 | golden light breaking through clouds / volumetric light rays through canopy |
| 构图方向 | 选填 | 景别/视角 | `close-up`比`rule of thirds`可靠（共现频率差异） | looking down from a cliff / wide shot from slightly above |
| 色彩基调 | 选填 | 色调锁定 | 用三层配色：基调+具体色+情绪 | cool blue and warm amber palette / jewel tones emerald and gold |

**构图控制方式选择**：

| 方式 | 模型 | 可靠性 | 关键操作 |
|------|------|--------|---------|
| 文本构图词 | 所有 | 有限 | 景别词(close-up/wide shot)比构图法(rule of thirds)可靠 |
| `--ar`参数 | MJ | 非常可靠 | `--ar 16:9`宽屏/`2:3`竖屏/`1:1`方图，比文本词直接100倍 |
| 柔和省略 | Flux | 可靠 | 想俯拍→只写地面元素不写天花板；想仰拍→只写天空不写地面 |
| ControlNet | SD | 精确 | Depth/MLSD约束空间结构；灰度构图图约束画面重心 |

**光照三要素**（跨模型通用）：
1. **光源类型**：key light / rim light / backlight / volumetric light / softbox
2. **方向**：from upper left / from behind / overhead / 45-degree angle
3. **色温/质感**：warm 3200K / cool 6500K / golden hour / harsh specular

**专业光源术语**（比描述效果更有效——与训练数据中特定视觉模式高共现）：

| 术语 | 视觉效果 | 适用场景 |
|------|---------|---------|
| Rembrandt lighting | 面颊三角形光斑 | 戏剧性人像 |
| chiaroscuro | 强明暗对比 | 暗黑概念图 |
| volumetric lighting | 体积光/丁达尔效应 | 雾中森林/教堂 |
| golden hour | 温暖侧光+长阴影 | 户外风景 |
| blue hour | 冷色调暮光 | 城市天际线 |
| rim light | 边缘发光 | 人物/物体轮廓分离 |

**模糊词→精确词替换**：
- "dramatic lighting" → "rim lighting from upper left, warm 3200K key light"
- "beautiful light" → "soft diffused key light from overhead, warm golden hour"
- "moody" → "low-key single source from behind, rim light only, deep shadows on 80% of frame"

**配色三层词**（跨模型通用）：
1. **色彩基调词**（锁定整体色调分布）：`pastel colors` / `jewel tones` / `monochromatic` / `complementary colors`
2. **具体颜色**（锁定关键色）：`deep crimson` / `navy` / `sage` / `emerald` / `amber`
3. **色彩情绪**（锁定情感方向）：`melancholic blue` / `cheerful macaron` / `vintage sepia`

> 三层组合效果远强于任何单层——"pastel colors"锁基调，"sage green"锁色相，"melancholic"锁情绪。

渐变色注意：SD中渐变色难出（CLIP将颜色编码为离散向量）→加权重增强；Flux中直接用自然语言描述渐变（T5理解"gradient"的过渡含义）。

#### 示例

用户："画一片迷雾山谷的黎明"
→ `a misty mountain valley at dawn, golden light breaking through clouds, looking down from a cliff, cool blue and warm amber palette`

用户："赛博朋克城市"
→ `neon-lit cyberpunk city at night, neon glow reflecting on wet streets, from street level looking up, vivid pink and cyan palette`

---

### 模板B：MJ风景（参数精确控制）

```
[主体描述], [光影描述], [氛围词],
[色彩基调词], [构图词],
--ar [宽高比] --s [风格化强度] --v 7
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 主体描述 | ✅ | 画什么 | | ancient forest clearing |
| 光影描述 | ✅ | 三要素 | | volumetric light rays through canopy |
| 氛围词 | 选填 | 情绪 | | mystical atmosphere |
| 色彩基调词 | 选填 | 锁色 | | jewel tones emerald and gold |
| 构图词 | 选填 | 景别 | | wide shot from slightly above |
| --ar | ✅ | 宽高比 | 比文本构图词直接100倍 | --ar 16:9 / --ar 2:3 |
| --s | 选填 | 风格化强度 | 500-750适合风格化风景 | --s 500 |

#### 示例

→ `ancient forest clearing, volumetric light rays through canopy, mystical atmosphere, jewel tones emerald and gold, wide shot from slightly above, --ar 16:9 --s 500 --v 7`

---

### 模板C：SD风景（加法式+BREAK防污染）

```
[主体], [场景细节], BREAK [光影描述], [氛围词], [色彩基调],
best quality, masterpiece, highly detailed landscape
```

参数：CFG 7-8 | Steps 25-30 | DPM++ 2M Karras

---

### 模板D：暗光/夜景

```
[主体], [单一光源描述],
low-key lighting with 80% of the frame in deep shadow,
[暗区描述如 'impenetrable shadow'],
[亮区描述如 'warm amber light illuminating only the path'],
volumetric lighting with visible light rays fading into ambient darkness
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 主体 | ✅ | 暗光中的核心对象 | | a lone figure on a forest path |
| 单一光源描述 | ✅ | 光从哪来 | 明确单一光源方向 | single warm key light from upper left |
| 暗区比例 | ✅ | 暗区占多大 | 标准CFG在暗区过度结构化→需特殊参数 | 80% of the frame in deep shadow |
| 暗区描述 | ✅ | 暗区有什么 | 不要只写"dark"——太模糊 | impenetrable shadow swallowing the edges |
| 亮区描述 | ✅ | 亮区有什么 | 光照亮了什么 | warm amber light illuminating only the path |
| 体积光 | 选填 | 空气感 | | volumetric light rays fading into ambient darkness |

**SD暗光专用参数**：
- CFG：5.5-7.0（降低——标准CFG在暗区过度结构化产生噪点）
- Steps：40-60（增加——暗区渐变需要更多步数才平滑）
- 采样器：DPM++ 2M Karras（弱光过渡区梯度收敛更稳定）

#### 示例

→ `a lone figure on a forest path, single warm key light from upper left, low-key lighting with 80% of the frame in deep shadow, impenetrable shadow swallowing the edges, warm amber light illuminating only the path, volumetric lighting with visible light rays fading into ambient darkness`

---

### 模板E：光影特效速查

| 效果 | 提示词 | 适用场景 |
|------|--------|---------|
| 逆光剪影 | `backlit silhouette, sun behind subject, rim light` | 日落/日出 |
| 霓虹辉光 | `neon glow, colorful reflections on wet surface` | 赛博朋克 |
| 丁达尔光 | `volumetric light, Tyndall effect, god rays` | 雾中森林 |
| 黄金时刻 | `golden hour, warm amber light, long shadows` | 户外风景 |
| 蓝调时刻 | `blue hour, cool twilight, soft diffused light` | 城市天际线 |

---

## 诊断路由

| 观察到 | 可能原因 | 修复动作 | 规则 |
|--------|---------|---------|------|
| 构图不是想要的 | 文本构图词效果有限 | MJ用`--ar`参数；SD用ControlNet；Flux用"只写什么出什么" | R06 |
| 光影太模糊 | 用了"dramatic lighting"等宽泛词 | 用三要素（类型+方向+色温）精确描述 | R08 |
| 配色Generic | 未指定色彩基调 | 用三层配色词（基调+具体色+情绪） | R05/R07 |
| 堆砌画质词画面反而差 | "4K/best quality"把去噪方向推向"更多元素" | Flux/国产模型删画质词；SD精简到1-2个 | R11 |
| 暗区死黑 | 标准CFG在暗区过度结构化 | SD: 降CFG到5.5-7.0 + 增步数到40-60 | — |
| 亮区漂浮 | 光源与场景不融合 | 描述光线在场景中的传播（反射/衰减/散射） | R05 |
| 语义冲突 | 同时写矛盾概念（冷+暖色调） | 一次一个色调方向，用具体描述替代矛盾标签 | R04/R09 |
| 渐变色出不来（SD） | CLIP将颜色编码为离散向量 | 加权重增强；或换Flux用自然语言描述渐变 | R12 |

---

## 场景必检项

```
□ 核心意象已确定？（主体+时间+氛围三要素）
□ 构图方式已选定？（文本词/MJ参数/Flux省略/SD ControlNet）
□ 光影三要素已写？（类型+方向+色温，避免模糊词）
□ 配色已锁？（三层：基调+具体色+情绪）
□ 暗光场景：暗区比例+单一光源+体积光？SD参数已调？
□ SD风景：BREAK防污染？画质词精简？
□ MJ风景：--ar已设？--s已设？
□ 每次迭代只改一个维度（构图/光影/配色），观察效果
```

---

## 模型注意

- **MJ**：构图/光影/氛围的审美加工能力最强——`--ar`直接控制宽高比比任何文本构图词都强；`--s 500-750`适合风格化风景
- **Flux**：减法思维——只写要出现的元素，利用信息不对称控制构图；T5理解渐变色比SD强
- **SD**：需画质词+负向词+BREAK防污染；暗光场景需特殊参数（低CFG+高步数）；ControlNet Depth/MLSD精确空间控制
- **GPT Image 2**：自然语言描述即可，风格化弱——风景的场景感好但艺术加工不如MJ
- **国产模型**：中文描述风景效果可能比英文更好——"烟雨江南"比"misty rain Jiangnan"编码更精确
