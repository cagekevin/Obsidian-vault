---
name: 技能创建工具
description: 技能全生命周期管理——两大模式覆盖建设与优化（重构作为附属功能内嵌在创建中）。Use when user wants to create a new skill, optimize an existing skill, rename/move/delete a skill, package skill for distribution, validate skill, run eval to test a skill, or optimize trigger words. 任何时候用户提到"创建技能"、"设计skill"、"写个技能"、"改技能"、"评测技能"、"触发优化"、"优化技能"时，都必须使用本技能。
metadata:
  pattern: pipeline+tool-wrapper
---

# 技能创建与维护工具

## 路由表

| 意图 | 模式 | 入口 |
|------|------|------|
| 创建新技能 | **Mode 1: Greenfield Build** | [`技能创建/SKILL.md`](技能创建/SKILL.md) |
| 优化已有技能 | **Mode 2: Incremental Forge** | [`技能优化/SKILL.md`](技能优化/SKILL.md) |
| 提示词工程参考 | **Reference: Prompt Engineering** | [`提示词工程专家/SKILL.md`](提示词工程专家/SKILL.md) |
