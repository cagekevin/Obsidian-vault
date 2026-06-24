---
type: source
title: "Seedance 2.5 Prompt Guide"
created: 2026-06-24
updated: 2026-06-24
tags:
  - source
  - video-generation
  - prompt-engineering
status: ingested
related:
  - "[[AI Camera Movements]]"
---

# Seedance 2.5 Prompt Guide

> GitHub 仓库：[anil-matcha/Awesome-Seedance-2.5-API-Prompts](https://github.com/anil-matcha/Awesome-Seedance-2.5-API-Prompts)
> 来源类型：第三方社区整理的 Seedance 2.5 提示词指南（非字节跳动官方）
> 语言：英文

## 内容概要

一个针对字节跳动 Seedance 2.5 AI 视频生成模型的提示词指南，包含：

1. **6 步公式**：`[主体] + [动作] + [环境] + [镜头] + [风格] + [约束条件]`，前 20-30 词最重要
2. **运镜词汇表**：13 种常用运镜的英文精确术语
3. **灯光词汇表**：18 种灯光关键词，强调"一个灯光关键词 > 十个形容词"
4. **分类提示词模板**：电影级/社交媒体/动漫/广告/多镜头序列
5. **API 调用参考**：通过 MuAPI 中转调用 Seedance 2.5

## 提炼到 Wiki 的概念

- [[AI Camera Movements]] — 运镜词汇速查 + 灯光词汇表（已追加）

## 关键洞察

- 灯光描述对 AI 视频生成质量的影响最大，一个精确的灯光关键词胜过一堆抽象形容词
- 前 20-30 个词决定输出质量，主体和动作要前置
- 运镜词要用精确英文术语（如 `dolly zoom` 而非"推拉变焦"）
