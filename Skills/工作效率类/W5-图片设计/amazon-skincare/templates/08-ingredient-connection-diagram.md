---
type: component
priority: "Medium"
tags: ["#成分连线图", "#Ingredient"]
balance_category: "Ingredient / Fragrance"
match_keywords: ["ingredient", "成分", "连线", "配方", "formula", "contains", "含有", "squalane", "oil", "extract"]
---
# 08-成分连线图 (ingredient_connection_diagram)

## 骨架排版规则
- **视觉焦点**：产品+精华质地居右，成分标签+连线居左
- **图层结构**：
  - Layer 1 (top left, large, serif bold): title_top
  - Layer 2 (below, large, serif): title_main
  - Layer 3 (left side, medium, sans-serif): ingredient_names
  - Layer 4 (below each name, small, sans-serif): ingredient_descriptions
*(注：本结构严禁硬编码颜色，渲染时自动套用全局皮肤。)*

## 视觉提示词基底 (AI Prompt Base)
skincare ingredient composition diagram, {capsule_form} with serum texture smear on the right, connecting line indicators to ingredient labels on the left, floating serum bubbles, {background}, professional cosmetic photography, {lighting}, clean infographic style, {aesthetic}
