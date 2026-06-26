---
name: Seedance 提示词转化 / Seedance Prompt Generator
description: Seedance 2.0 视频提示词生成器集合。接收场景/剧本/品牌描述，输出 Seedance 引擎可用的视频提示词。支持 15 种风格（电影/CGI/电商/品牌/动漫等）和通用导演模式。Use when user wants to create Seedance video prompts, generate video prompts for any style, cinematic, brand story, ecommerce ad, fight scenes, or any Seedance 2.0 prompt generation.
---

# Seedance 提示词转化

根据用户需求自动路由到对应风格的提示词生成器。

<what-to-do>

## 分流规则

| 路由 | 文件 | 触发关键词 |
|------|------|-----------|
| **通用导演（默认）** | 通用偏冲突/SKILL.md | Seedance, 视频提示词, 场景描述, 剧本转提示词（默认路由） |
| 电影级 | 01-cinematic/SKILL.md | 电影, cinematic, 电影感, 剧情片 |
| 3D CGI | 02-3d-cgi/SKILL.md | 3D, CGI, 三维, 渲染, Pixar, Unreal |
| 卡通/动画 | 03-cartoon/SKILL.md | 卡通, cartoon, 手绘, 水彩, 动画 |
| 漫画转视频 | 04-comic-to-video/SKILL.md | 漫画, 动漫, 条漫, webtoon, 分镜转视频 |
| 打斗/动作 | 05-fight-scenes/SKILL.md | 打斗, 动作, fight, 战斗, 武打 |
| 动效广告 | 06-motion-design-ad/SKILL.md | 动效, motion, SaaS, 产品演示, UI 动画 |
| 电商广告 | 07-ecommerce-ad/SKILL.md | 电商, ecommerce, 产品广告, 带货, TikTok Shop |
| 动漫动作 | 08-anime-action/SKILL.md | 日漫, anime, 番剧, 二次元 |
| 产品 360° | 09-product-360/SKILL.md | 产品展示, product 360, 产品旋转, 开箱 |
| 音乐视频 | 10-music-video/SKILL.md | 音乐视频, MV, music video, 演唱会 |
| 社交钩子 | 11-social-hook/SKILL.md | 短视频, 社交, 抖音, TikTok, Reels, 爆款 |
| 品牌故事 | 12-brand-story/SKILL.md | 品牌故事, brand story, 企业宣传, 创始人故事 |
| 时尚画册 | 13-fashion-lookbook/SKILL.md | 时尚, fashion, 走秀, 穿搭, 画册 |
| 美食饮料 | 14-food-beverage/SKILL.md | 美食, 餐饮, 烹饪, 食品, 餐厅 |
| 房产展示 | 15-real-estate/SKILL.md | 房产, real estate, 样板房, 室内设计 |

## 选择指引

- **默认**：任何场景/剧本/视频描述 → **通用导演**（自动解析场景类型）
- 用户明确指定风格 → 对应风格的提示词生成器
- 所有生成器输出均为 Seedance 2.0 兼容格式

</what-to-do>
