---
name: 视频创作
description: 视频创作自动化流水线，默认走全流程管线。Use when user wants anything related to video creation, storyboards, short videos, or automated video production. Only route to seedance or Russian script sub-skills when explicitly named.
---

# 视频创作

<what-to-do>
根据用户输入自动匹配下方路由。**默认优先级：剧本到视频全流程 > Seedance提示词转化 > 俄语详细剧本**。video 相关关键词优先匹配全流程，其他两个子路由只在用户显式点名时触发。

# <route-table>
| 优先级 | 路由 | 文件 | 触发关键词 |
|--------|------|------|-----------|
| 🥇 默认 | **剧本到视频全流程** | **screenplay-to-video/SKILL.md** | **视频, video, 分镜, storyboard, 短剧, 微短剧, 科普视频, 自动化出片, 视频生成, 视频流水线, 从剧本到视频, pipeline, 镜头, 定妆, 参考图, 美术指导, 画面描述, 提示词, prompt, 场景描述, scene, 0_skill, 0-skill, 0号skill** |
| 🥇 仅点名 | **OpenMontage 全自动视频制作** | **OpenMontage视频制作系统/CLAUDE.md** | **openmontage, OpenMontage, 全自动视频, 自动出片, AI视频制作系统** |
| 🥈 仅点名 | 视频提示词生成 | Seedance提示词转化/SKILL.md | seedance（仅在用户明确提到"seedance"时触发） |
| 🥉 仅点名 | 剧本创作 | 俄语详细剧本/SKILL.md | 俄语剧本, 俄语编剧（仅在用户明确提到"俄语剧本"时触发） |

选择指引：
- **默认**：任何视频/分镜/提示词相关 → 走 **剧本到视频全流程**（自动管线）
- 仅当用户明确说"**seedance**" → 走 **Seedance提示词转化**
- 仅当用户明确说"**俄语剧本**"或"**俄语编剧**" → 走 **俄语详细剧本**
</what-to-do>
