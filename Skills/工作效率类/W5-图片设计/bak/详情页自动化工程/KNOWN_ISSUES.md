# 待修复问题

## 开发流程原则

**先定义模板，后实现渲染。** 如果 `layout-defaults.json` 里没有某个布局的完整定义（spatial_prompt_injection、gestalt_rules、text_zone 等），renderer 就不应该实现它——没有模板定义，render 什么？

## layout-defaults.json 与 renderer.py 不匹配

### 1. `split_before_after` — 缺少图区

- **问题**：`layout-defaults.json` 的 `spatial_prompt_injection` 描述为左右对比图（左使用前/右使用后）+ 底部 20% 留白文字区。但 `renderer.py` 的 `_t_split` 模板输出全文字卡片，没有 `.img-zone`。
- **影响**：生图提示词说"画面垂直分割左暖调右冷调"，但 HTML 里没有预留对比图的位置。
- **修复方向**：`_t_split` 需要加两个图区（左/右），底部放文字卡片。

### 2. `texture_smear_bottom_text` — 图文位置不符

- **问题**：`layout-defaults.json` 的 `spatial_prompt_injection` 原为"图在上 65%"，但实际需求为文上图下（文字在上 45%，图区在下 55%）。模板已修，spatial 也已同步更新。
- **状态**：✅ 已修复（2026-06-09）

---

## 未来需求

### 3. 可视化图片编辑器（`ui/index.html` 升级）

- **背景**：当前流程是 AI 生成 HTML + flow_prompt，图片区用渐变占位。生图 API 出图后，没有工具把图片放回 HTML。
- **需求**：
  1. 加载 `output/detail_xxx.html` 预览效果
  2. 点击图区（`.img-zone`）可上传/粘贴图片 URL，替换渐变占位
  3. 拖拽图区边缘调整图片占比（如 45%↔55%）
  4. 导出最终 HTML（含真实图片）
- **不做的**：不动字体、颜色、布局——这些由 JSON 控制，改 JSON 重跑 pipeline。
- **难度**：低（图片替换）+ 中（拖拽调整）= 1 天基础版
