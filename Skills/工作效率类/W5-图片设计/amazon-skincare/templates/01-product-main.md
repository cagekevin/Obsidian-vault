---
type: component
priority: "Always"
tags: ["#产品主图", "#Product_Hero"]
balance_category: "Product Hero"
match_keywords: ["product", "产品", "主图", "包装", "全套", "set", "box", "accessories"]
---
# 01-产品主图 (product_main)

## 骨架排版规则
- **视觉焦点**：产品居中，配件环绕
- **图层结构**：
  - Layer 1 (top, small, gold sans-serif): top_label
  - Layer 2 (center, medium, serif bold): brand_name
  - Layer 3 (center below, large, serif): product_name
  - Layer 4 (bottom, small, sans-serif): package_description
*(注：本结构严禁硬编码颜色，渲染时自动套用全局皮肤。)*

## 视觉提示词基底 (AI Prompt Base)
luxury skincare {form} set, {packaging}, product box, golden massage tool, small scissors, white flower, serum smear with bubbles, {background}, professional product photography, {lighting}, {aesthetic}
