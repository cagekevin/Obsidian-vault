---
type: concept
title: "AI 生图两段式"
address: c-000016
status: developing
tags:
  - concept
  - image-generation
  - video-generation
  - workflow
  - prompt-engineering
created: 2026-06-30
related:
  - "[[sources/何止维AI创作系列合辑]]"
  - "[[AI视觉语法体系]]"
  - "[[AI底层机制与高级控制]]"
  - "[[AI氛围与色彩控制]]"
  - "[[AI影调控制]]"
  - "[[何止维]]"
---

# AI 生图两段式：信息版 → 情绪版

> 来源：[[sources/何止维AI创作系列合辑]] — [[何止维]]《一步错步步错》
>
> 相关概念：[[AI影调控制]]（情绪版的核心是影调控制）

## 核心原则

生图有顺序。先做**信息版**，再做**情绪版**。顺序错了就会无限套娃抽卡。

---

## 第一步：信息版

**目标**：平光、可读性最高、所有细节看得清。

**为什么**：AI 在暗部和高光里看不清，看不清就会开始脑补——凭空加东西、改结构。所以人物、道具、构图、内容调整，**必须在信息版里做完**。

**写法**：用均匀柔和的正面光，不强调明暗对比，让所有元素清晰可见。

---

## 第二步：情绪版

**目标**：在内容锁死的基础上，叠加影视化效果。

**可叠加的元素**：
- 影调氛围（低长调、高长调等）
- 情绪色彩（色温、色调）
- 明暗对比
- 轮廓光、逆光、体积光
- 舞烟、雨、雪等气氛
- 胶片感、颗粒、色彩风格

**这一步才是镜头语言的表演阶段**，但它必须建立在内容稳定的基础上。

---

## 核心规则

1. **内容锁死之后再上影调** — 信息版确认内容无误后，再叠情绪版
2. **不要在情绪版上修改内容** — 如果发现内容需要改，回到信息版重做，不要在情绪版上直接改
3. **换光影风格要回信息版** — 如果要换完全不同的一套光影风格，需要回到信息版重做
4. **否则无限套娃** — 影调会吞信息 → AI 看不清 → 脑补乱加 → 你改内容 → 影调风格被吞 → 再调影调 → 又吞信息 → ...

---

## 示例流程

**信息版提示词**：
```
A young woman in a white shirt, sitting at a wooden desk,
soft even lighting, all details clearly visible,
neutral expression, centered composition.
```

**确认内容无误后，叠情绪版**：
```
[信息版提示词保留]
Low-key lighting, high contrast, warm tungsten light from the right,
deep shadows on the left side, volumetric smoke in the air,
cinematic color grading with teal and orange tones,
subtle film grain.
```
