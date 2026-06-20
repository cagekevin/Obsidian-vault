---
type: component
priority: "High"
tags: ["#Before/After对比", "#Proof_Data"]
balance_category: "Proof / Data"
match_keywords: ["before", "after", "对比", "前后", "results", "效果", "visible", "transformation", "改善"]
---
# 03-Before/After两格对比 (before_after_two_panel)

## 骨架排版规则
- **视觉焦点**：双栏并排对比，SGS 认证 + 百分比数据
- **图层结构**：
  - Layer 1 (top center, large, serif bold): title
  - Layer 2 (below title, medium, serif): subtitle
  - Layer 3 (left panel, medium, sans-serif): left_label
  - Layer 4 (right panel, medium, sans-serif): right_label
  - Layer 5 (between panels, large numbers, bold): data_points with arrows
  - Layer 6 (bottom corner, small): SGS certification logo
*(注：本结构严禁硬编码颜色，渲染时自动套用全局皮肤。)*

## 视觉提示词基底 (AI Prompt Base)
two-panel before and after comparison, left side: {problem_visual}, right side: {improvement_visual}, SGS certification logo, percentage improvement data with golden arrows, {background}, professional cosmetic photography, {lighting}, {aesthetic}
