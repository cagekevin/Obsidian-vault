---
type: component
priority: "Medium"
tags: ["#香调说明图", "#Ingredient"]
balance_category: "Ingredient / Fragrance"
match_keywords: ["fragrance", "scent", "香调", "香味", "note", "前调", "中调", "后调", "top note", "middle note", "base note", "aroma"]
---
# 13-香调说明图 (fragrance_notes)

## 骨架排版规则
- **视觉焦点**：左侧产品+大花，右侧香调说明
- **图层结构**：
  - Layer 1 (top, large, serif bold): title
  - Layer 2 (right, medium, sans-serif bold): "Top Note"
  - Layer 3 (below, small, sans-serif): top_note_items
  - Layer 4 (right, medium, sans-serif bold): "Middle Note"
  - Layer 5 (below, small, sans-serif): middle_note_items
  - Layer 6 (right, medium, sans-serif bold): "Base Note"
  - Layer 7 (below, small, sans-serif): base_note_items
*(注：本结构严禁硬编码颜色，渲染时自动套用全局皮肤。)*

## 视觉提示词基底 (AI Prompt Base)
{packaging} with a large blooming flower beside it on the left, floating petals scattered elegantly, fragrance notes structure on the right, {background}, professional product photography, {lighting}, romantic luxurious aesthetic, {aesthetic}

## 排他规则
- 若产品形态为胶囊（capsule），排除此模板
