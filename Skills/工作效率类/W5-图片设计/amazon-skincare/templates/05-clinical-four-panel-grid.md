---
type: component
priority: "High"
tags: ["#四格临床对比", "#Proof_Data"]
balance_category: "Proof / Data"
match_keywords: ["day 1", "day 28", "clinical", "临床", "before after", "grid", "四格", "对比区域"]
---
# 05-四格临床对比 (clinical_four_panel_grid)

## 骨架排版规则
- **视觉焦点**：四格网格，展示不同区域前后对比
- **图层结构**：
  - Layer 1 (each panel top, small, sans-serif): "DAY 1" / "DAY 28"
  - Layer 2 (each panel, large numbers, bold): percentage_change
  - Layer 3 (bottom, small): SGS logo
*(注：本结构严禁硬编码颜色，渲染时自动套用全局皮肤。)*

## 视觉提示词基底 (AI Prompt Base)
four-panel grid of clinical before and after comparisons, each panel showing skin texture closeup with DAY 1 and DAY 28 labels, SGS logo, {background}, professional medical photography, {lighting}, clinical precision, {aesthetic}
