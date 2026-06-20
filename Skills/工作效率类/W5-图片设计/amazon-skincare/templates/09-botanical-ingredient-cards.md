---
type: component
priority: "Medium"
tags: ["#植物配料卡片", "#Ingredient"]
balance_category: "Ingredient / Fragrance"
match_keywords: ["botanical", "plant", "植物", "花", "seed", "petri", "培养皿", "天然", "natural", "extract"]
---
# 09-植物配料卡片 (botanical_ingredient_cards)

## 骨架排版规则
- **视觉焦点**：左侧三个培养皿植物，右侧四个配料卡片
- **图层结构**：
  - Layer 1 (top, large, serif bold): title_top
  - Layer 2 (below, large, serif): title_main
  - Layer 3 (each card, medium, sans-serif bold): ingredient_name
  - Layer 4 (below name, small, sans-serif): ingredient_description
  - Layer 5 (each card, small): ingredient_icon
*(注：本结构严禁硬编码颜色，渲染时自动套用全局皮肤。)*

## 视觉提示词基底 (AI Prompt Base)
botanical ingredients display, three glass petri dishes with delicate flowers and seeds on the left, four elegant ingredient information cards on the right with small icons, {background}, professional cosmetic photography, {lighting}, scientific botanical aesthetic, {aesthetic}
