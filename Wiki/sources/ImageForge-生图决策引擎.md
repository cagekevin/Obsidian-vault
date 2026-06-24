---
type: source
title: "ImageForge 生图决策引擎"
created: 2026-06-24
updated: 2026-06-24
tags:
  - source
  - image-generation
  - prompt-engineering
  - skill
status: ingested
related:
  - "[[AI 生图决策规则]]"
---

# ImageForge 生图决策引擎

> GitHub 仓库：[c3115644151/imageforge-skill](https://github.com/c3115644151/imageforge-skill)
> 来源类型：第三方开发的 AI 生图决策引擎 Skill（MIT 协议）
> 语言：中文

## 内容概要

一个面向 AI Agent 的生图决策引擎，核心是 5 步可执行流程：请求解析→场景路由→Prompt组装→质量门控→失败诊断。内置 19 条 if-then 决策规则和 6 个场景文件。

## 提炼到 Wiki 的概念

- [[AI 生图决策规则]] — 从 imageforge rules.md 提炼的 6 条可复用规则

## 关键洞察

- 场景经验 > 模型经验：模型会过时，场景最佳实践不会
- 决策规则 > 教育原理：if-then 比"理解为什么"更适合 AI 执行
- 模板填充 > 自由写作：AI 需要 slot 和填充规则，不是灵感
- 诊断路由 > 修复建议：按场景分类的失败→修复映射，带规则引用
