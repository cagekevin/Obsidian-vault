---
type: component
priority: "Low"
tags: ["#产品对比表", "#Comparison_Benefit"]
balance_category: "Comparison / Benefit"
match_keywords: ["vs", "versus", "对比", "比较", "traditional", "ordinary", "普通", "传统", "better than", "优于", "替代", "alternative", "competitor"]
---
# 20-产品对比表 (product_comparison_table)

## 骨架排版规则
- **视觉焦点**：两栏或三栏对比布局
- **图层结构**：
  - Layer 1 (left column top, medium, sans-serif bold): competitor_product_name
  - Layer 2 (left column, small, sans-serif): competitor_points (with X marks)
  - Layer 3 (middle column, large, serif bold): "VS"
  - Layer 4 (middle column, small, sans-serif): comparison_criteria
  - Layer 5 (right column top, medium, serif bold): hero_product_name
  - Layer 6 (right column, small, sans-serif): hero_product_points (with checkmarks)
  - Layer 7 (right column, small, sans-serif): hero_subtitle
*(注：本结构严禁硬编码颜色，渲染时自动套用全局皮肤。)*

## 视觉提示词基底 (AI Prompt Base)
product comparison layout, left side: competitor product on grey background with X marks, right side: {packaging} on golden pedestal with warm beige background and check marks, {background}, professional product photography, {lighting}, comparison infographic style, {aesthetic}
