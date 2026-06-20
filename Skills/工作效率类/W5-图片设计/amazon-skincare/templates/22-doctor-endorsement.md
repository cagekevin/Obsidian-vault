---
type: component
priority: "Low"
tags: ["#医生推荐", "#Comparison_Benefit"]
balance_category: "Comparison / Benefit"
match_keywords: ["doctor", "dermatologist", "ophthalmologist", "医生", "专家", "皮肤科", "recommended", "推荐", "endorsed", "white coat"]
---
# 22-医生推荐 (doctor_endorsement)

## 骨架排版规则
- **视觉焦点**：医生一侧，产品主张另一侧
- **图层结构**：
  - Layer 1 (opposite doctor, large, serif bold): title
  - Layer 2 (below, medium, sans-serif): endorsement_claims (with checkmark bullets)
  - Layer 3 (below, large, bold numbers): percentage_data
  - Layer 4 (bottom, small): doctor_signature
*(注：本结构严禁硬编码颜色，渲染时自动套用全局皮肤。)*

## 视觉提示词基底 (AI Prompt Base)
professional doctor in white coat with arms crossed and confident expression on one side, {packaging} with percentage efficacy data and signature on the other side, {background}, clinical photography style, professional medical aesthetic, {lighting}, {aesthetic}
