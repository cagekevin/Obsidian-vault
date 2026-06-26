---
name: 图片设计
description: Routes to the correct image prompt generator based on platform/context. Supports Amazon skincare main images, Chinese e-commerce (Taobao/Tmall/1688) main images, and detail page generation. Use when user needs to generate product image prompts, main image designs, or e-commerce detail pages.
metadata:
  pattern: pipeline+generator
---

# 图片提示词生成

根据用户需求自动分流到对应生成器：

<what-to-do>

## 分流规则

读取用户需求，匹配关键词：

| 路由 | 文件 | 触发关键词 |
|---|---|---|
| ImageForge 生图决策引擎 | imageforge-skill/SKILL.md | 按5步流程生图, 通用出图, 场景路由, 质量门控, 提示词组装, 角色设计, 产品摄影, 风景, 海报 |
| Amazon 护肤品主图 | amazon-skincare/amazon-skincare.md | Amazon, 亚马逊, English prompt, skincare, 护肤品主图, 英文提示词 |
| 电商中文主图 | ecommerce-image/ecommerce-image.md | 淘宝, 天猫, Taobao, Tmall, 1688, 电商主图, 中文提示词 |
| GPT图像生成 | GPT图像生成-GPTImage2/GPT图像生成-GPTImage2.md | GPT image, GPT Image 2, 图像生成, 图片生成, AI绘画, 海报, 漫画, 信息图 |
| 详情页生成器 | 详情页生成器/详情页生成器.md | 详情页, 产品详情, detail page, 详情描述, 详情设计, 商品详情 |
| 图片需求整理 | 图片需求整理/图片需求整理.md | 图片需求整理, 需求整理, 图片需求, 需求理解, 需求重构, 整理需求, 理解需求, 结构化需求, 词不达意, 跳跃表达, 海报需求 |
| Lovart API 出图 | lovart图片/lovart图片.md | lovart, Lovart, 出图, 图片生成, 设计规范, 海报设计, 主图设计, 品牌设计, 生图 |
| 小红书微信图文 | 社交卡片/SKILL.md | 小红书, 小红书图文, Rednote, Xiaohongshu, 社交卡片, social card, carousel, 轮播图, 微信公众号封面, WeChat cover, 21:9, 1:1, 杂志风, 瑞士风, Swiss Style |

**如有歧义**（两个都匹配或都不明确匹配），反问用户一句确认即可，不要猜测。

**如有 Excel 数据**，先执行 `skills/工作效率类/read-excel.ps1 $FILE_PATH`（或 `.sh`）读取，再进入子技能。

</what-to-do>
