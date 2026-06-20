---
type: component
priority: "High"
tags: ["#临床数据特写", "#Proof_Data"]
balance_category: "Proof / Data"
match_keywords: ["%", "SGS", "clinically", "proven", "临床", "数据", "improvement", "increase", "reduction", "decrease", "test", "测试"]
---
# 06-临床数据特写 (clinical_data_showcase)

## 骨架排版规则
- **视觉焦点**：皮肤纹理特写 + 数据叠层
- **图层结构**：
  - Layer 1 (top, large, serif bold): title
  - Layer 2 (below, medium, serif): subtitle
  - Layer 3 (scattered, large numbers, bold): data_values with arrows
  - Layer 4 (below each number, small, sans-serif): data_labels
  - Layer 5 (bottom corner): SGS logo
*(注：本结构严禁硬编码颜色，渲染时自动套用全局皮肤。)*

## 视觉提示词基底 (AI Prompt Base)
extreme close-up of {closeup} with moisturizing serum drops on skin surface, SGS certification logo, large percentage improvement numbers with golden arrows, {background}, professional medical photography, {lighting}, clinical grade detail, {aesthetic}
