---
type: concept
title: "AI 室内光控制"
complexity: intermediate
domain: image-generation
aliases:
  - "室内布光"
  - "室内光影"
created: 2026-06-27
updated: 2026-06-27
tags:
  - concept
  - image-generation
  - lighting
  - interior
status: developing
related:
  - "[[AI打光五法]]"
  - "[[光线布置模块化]]"
  - "[[AI环境空间设计]]"
  - "[[AI氛围与色彩控制]]"
  - "[[摄影语言锚定质感]]"
  - "[[concepts/_index]]"
---

# AI 室内光控制

室外光和室内光是两套完全不同的生成机制。室外有默认的天光（太阳），你不需要解释光从哪来。但室内是一个封闭的黑盒子——如果你不指定光源，AI 就会开启"上帝视角"的漫反射白光，这就是室内画面"平"、"假"、"塑料廉价感"的根源。

---

## 方法一：先定义光源，再定义方向

### 问题

很多人这样写室内光：
```
A cozy living room, warm light, 8k resolution.
```
只给了"暖光"指令，没告诉 AI 光从哪来。AI 随机抓取画面中的物体充当光源，光线出现在错误的地方，破坏构图重心。

### 解法

为光找一个"宿主"——在提示词中明确植入发光体。

**公式**：[场景描述] + [具体光源实体] + [光线投射动作] + [受光物体]

**自然光示例**（窗帘作为光源实体）：
```
A cozy living room in the late afternoon. Sunlight streams through
a large white curtain, casting soft, diffused light across the room.
The curtain glows warmly, becoming the primary light source.
```

**人造光示例**（霓虹灯作为光源实体）：
```
A dark bedroom illuminated only by a flickering neon sign
outside the window. The pink and blue light cuts across the wall,
casting long, colored shadows across the empty bed.
```

---

## 方法二：写衰减路径，而不是写强度

### 问题

很多人写室内光用感觉词：soft、weak、bright。但 AI 不是通过调整"亮度滑块"来理解光的，它是通过像素的明暗对比和过渡来构建空间的。只写"柔光"，AI 会把所有阴影提亮，导致画面变灰。

### 解法

描述光从亮到暗的过程——光的衰减路径（Falloff）。告诉 AI 光从哪里开始、在哪里结束。

**公式**：[主体动作] + [光照起点（强）] + [光照终点（衰减/消失）]

**示例**（书桌阅读场景）：
```
Close-up of an elderly scholar reading a thick book in a dark library.
A single small candle strictly illuminates the pages and his fingers,
the light rapidly falling off towards his shoulders, leaving the
background bookshelves in deep shadow. Chiaroscuro, Rembrandt lighting.
```
→ 蜡烛照亮书页和手指，光线向肩膀处迅速衰减，背景书架处于深重阴影。

### 关键词库

| 关键词 | 效果 | 适合场景 |
|--------|------|----------|
| Rapid falloff / High contrast falloff | 快速衰减，强烈戏剧感 | 黑色电影、悬疑风格 |
| Gradual fade / Soft gradient | 渐变消失，光线像水漫延 | 日系小清新、家居广告 |
| Pool of light | 光潭，把光限制在一个圆圈内 | 舞台感、聚焦主体 |

> **核心心法**：别告诉 AI"这里很暗"，要告诉它"光走不到这里"。AI 会自动拉开明暗差，层次感就出来了。

---

## 方法三：室内亮度靠反射，不靠直射

### 问题

新手认为要把房间照亮就需要大灯直射，但会造成生硬的"探照灯效应"——阴影死黑，高光过曝。真正把空间填亮的是光线撞击墙面、地板后的漫反射（Bounce Light）。

### 解法

不仅要写主光源，还要写环境光是如何产生的——光线撞击材质后的反弹。

**公式**：[材质环境] + [主光源撞击] + [反射后的环境色填充]

**示例**（白色房间+木地板）：
```
A spacious, minimalist art gallery space, pure white walls.
Strong afternoon sunlight strikes the polished orange wood floor,
warm color bounces upward and illuminates the white ceiling and walls,
filling the shadows with a subtle orange tint.
Photorealistic, global illumination rendering.
```
→ 阳光（白色）撞击木地板（黄色），反射出暖黄色光填充暗部。写出这种色温传递，真实感指数级上升。

### 材质对反射的影响

- **Matte / Rough textures（哑光/粗糙）** — 吸收光线，反射柔和，适合温馨复古感
- **Glossy / Polished surfaces（光面/抛光）** — 强反射，有镜面光，适合科技感、现代奢华

> **核心心法**：室内光的本质不是"亮度控制"，而是"空间理解"。通过描述反射，强迫 AI 理解房间的三维结构——墙在哪里、地在哪里、光怎么弹来弹去。

---

## 总结

1. **定义光源实体** — 告诉 AI 光是从具体的窗户或灯具出来的，拒绝无源之光
2. **描绘衰减路径** — 描述光从亮到暗的过程，而不是单纯调整亮度参数
3. **利用反射机制** — 描写光线撞击物体后的反弹，用漫反射填充暗部

> 与 [[光线布置模块化]] 配合使用：将上述三个方法写入独立的 `【光线布置】` 段落。
