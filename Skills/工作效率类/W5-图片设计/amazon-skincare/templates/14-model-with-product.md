---
type: component
priority: "Fallback"
tags: ["#模特+产品", "#Model_Lifestyle"]
balance_category: "Model / Lifestyle"
match_keywords: ["model", "woman", "模特", "女性", "beautiful", "elegant", "portrait", "人像", "lifestyle"]
---
# 14-模特+产品 (model_with_product)

## 骨架排版规则
- **视觉焦点**：模特一侧，产品另一侧
- **图层结构**：
  - Layer 1 (opposite model, large, serif bold): title
  - Layer 2 (below, medium, serif): subtitle
  - Layer 3 (below, small, sans-serif): feature_list (with checkmark bullets)
*(注：本结构严禁硬编码颜色，渲染时自动套用全局皮肤。)*

## 视觉提示词基底 (AI Prompt Base)
beautiful woman, {model_focus}, elegant pose looking at camera, {packaging} placed beside her with scattered golden capsules, {background}, professional cosmetic photography, {lighting}, aspirational lifestyle aesthetic, {aesthetic}

## 兜底规则
- 若某卖点未命中任何模板关键词，强制使用此模板兜底
