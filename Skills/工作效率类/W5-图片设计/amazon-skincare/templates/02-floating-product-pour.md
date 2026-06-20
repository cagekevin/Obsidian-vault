---
type: component
priority: "Low"
tags: ["#漂浮倒液图", "#Product_Hero"]
balance_category: "Product Hero"
match_keywords: ["pour", "liquid", "golden", "倒", "液体", "滴落", "drop", "高浓度", "concentration"]
---
# 02-漂浮倒液图 (floating_product_pour)

## 骨架排版规则
- **视觉焦点**：产品倾斜，液体倾泻
- **图层结构**：
  - Layer 1 (top, small, sans-serif): top_label
  - Layer 2 (mid-top, large, caps, serif bold): title
  - Layer 3 (below title, medium, serif): subtitle
  - Layer 4 (mid, small, sans-serif): body_description
  - Layer 5 (bottom, small, sans-serif): benefits_list with + marks
*(注：本结构严禁硬编码颜色，渲染时自动套用全局皮肤。)*

## 视觉提示词基底 (AI Prompt Base)
tilted {packaging}, golden liquid pouring from top, a single serum drop falling from bottom with subtle golden splashes, {background}, professional product photography, {lighting}, {aesthetic}, dynamic liquid motion

## 排他规则
- 若产品形态为胶囊（capsule），排除此模板
