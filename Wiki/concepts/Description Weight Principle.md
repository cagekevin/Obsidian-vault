---
type: concept
title: "Description Weight Principle"
complexity: intermediate
domain: image-generation
aliases:
  - "描述比重原则"
  - "主次比例原则"
created: 2026-06-23
updated: 2026-06-23
tags:
  - concept
  - image-generation
  - prompt-engineering
status: mature
related:
  - "[[Visual Description First Principle]]"
  - "[[Restraint Principle]]"
  - "[[Consistency Anchor Principle]]"
sources:
---

# 描述比重原则

画面元素的描述字数，要和它的重要性成正比。次要元素描述多了，就会喧宾夺主。

---

## 核心内容

AI 生成图片时，是按"字数权重"来分配注意力的。你写得越多的东西，AI 越觉得它重要，越会在画面中突出它。

所以：
- **主体元素**：描述要详细，占总字数的 50-60%
- **次要元素**：描述要简短，占总字数的 20-30%
- **环境/氛围**：点到为止，占总字数的 10-15%
- **情绪/感受**：极度克制，占总字数的 5-10%

---

## 为什么重要

很多人做 AI 出图的误区是"每个元素都写详细一点"，但结果往往是：
- 次要元素抢了主体的戏
- 画面重点不突出
- 整体感觉杂乱

比如你想画"一朵花，旁边有一只手轻轻托着"，如果手部描述写了 40% 的字数，最后出来的图可能手比花还大还突出。

正确的做法是：主体详细写，次要元素一笔带过，让 AI 知道谁是主角。

---

## 应用场景

- **产品图**：产品描述详细，背景/环境简单带过
- **场景图**：主体详细，环境/氛围点到为止
- **人物互动**：主体详细，互动的部分简短描述
- **燃烧/特效场景**：主体 60%，燃烧效果 30%，环境 10%

---

## 常见误区

1. **平均用力**：每个元素都写同样多的描述 → 没有重点
2. **次要元素过度描述**：比如背景写得比主体还详细 → 喧宾夺主
3. **情绪词堆砌**：用一堆形容词描述感受 → 反而让画面失真

---

## Connections

- [[Visual Description First Principle]] — 描述不仅要有比重，还要是视觉化的
- [[Restraint Principle]] — 克制不仅体现在数量上，也体现在程度上
- [[Consistency Anchor Principle]] — 同系列图片的比重分配要保持一致
