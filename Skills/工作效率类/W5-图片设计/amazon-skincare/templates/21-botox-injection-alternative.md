---
type: component
priority: "Low"
tags: ["#注射替代方案", "#Comparison_Benefit"]
balance_category: "Comparison / Benefit"
match_keywords: ["botox", "injection", "needle", "肉毒", "注射", "针剂", "fillers", "整形", "non-invasive", "无创"]
---
# 21-注射替代方案 (botox_injection_alternative)

## 骨架排版规则
- **视觉焦点**：左右分栏对比（注射 vs 精华），模特脸部
- **图层结构**：
  - Layer 1 (left side, medium, sans-serif bold): injection_label
  - Layer 2 (left side, small, sans-serif): injection_warnings
  - Layer 3 (right side, medium, serif bold): serum_label
  - Layer 4 (right side, small, sans-serif): serum_benefits
  - Layer 5 (scattered, large, numbers): percentage_data
  - Layer 6 (bottom): SGS logo
*(注：本结构严禁硬编码颜色，渲染时自动套用全局皮肤。)*

## 视觉提示词基底 (AI Prompt Base)
split comparison layout, left side: syringe with warning triangle on dark background representing injections, right side: {capsule_form} on golden pedestal with warm background, model face with serum droplets evenly distributed on skin, SGS logo, {background}, professional cosmetic photography, {lighting}, {aesthetic}
