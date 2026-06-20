---
name: 界面淬炼
description: 专业前端界面设计精修工作流，包含 22 个专业子命令覆盖构建/评估/精修/增强/修复/迭代全流程。内置品牌（Brand）与产品（Product）双 Register 机制，7 条防 AI 千篇一律的审美禁止规则。Use when user wants to [craft] [shape] [critique] [audit] [polish] [bolder] [quieter] [distill] [harden] [animate] [colorize] [typeset] [layout] [delight] [clarify] [adapt] [optimize] or [live] a frontend interface.
metadata:
  pattern: pipeline+tool-wrapper
  source: https://github.com/pbakaus/impeccable
---

# 界面淬炼（Impeccable）

专业前端界面设计精修工作流。生成生产级代码，坚持设计取舍，追求非凡工艺。

来源识别：本技能由 pbakaus 创建与维护，规范源仓库为 https://github.com/pbakaus/impeccable 。Apache 2.0 许可。

---

## 快速路由：用户需求 → 对应子命令

| 用户需求 | 子命令 | 参考文件 |
|---------|--------|---------|
| **从零构建** 从需求到实现 | `craft` / `shape` | reference/craft.md / reference/shape.md |
| **设定设计语境** 产品/设计文档 | `teach` / `document` | reference/teach.md / reference/document.md |
| **提取设计系统** 从代码中提取规范 | `extract` | reference/extract.md |
| **评审/审计** UX 评分 / 技术审查 | `critique` / `audit` | reference/critique.md / reference/audit.md |
| **精修** 抛光/放大/缩小/提纯/加固 | `polish` / `bolder` / `quieter` / `distill` / `harden` | 对应参考文件 |
| **增强** 动画/配色/排版/布局/趣味/极限 | `animate` / `colorize` / `typeset` / `layout` / `delight` / `overdrive` | 对应参考文件 |
| **修复** 文案/适配/性能 | `clarify` / `adapt` / `optimize` | 对应参考文件 |
| **实时迭代** 浏览器选元素生成方案 | `live` | reference/live.md |

---

## 初始化设置（必须先执行）

在任何设计工作或文件编辑前：

1. **加载上下文**：调用 `scripts/load-context.mjs` 加载 PRODUCT.md 和 DESIGN.md
2. **识别 Register**：确定任务是 **brand**（营销/品牌）还是 **product**（工具/产品 UI）
3. **加载 Register 参考文件**：`reference/brand.md` 或 `reference/product.md`
4. **加载子命令参考文件**：如果用户调用了子命令（如 `craft`、`shape`），加载对应的参考文件

### 上下文文件

| 文件 | 必填 | 说明 |
|------|------|------|
| PRODUCT.md | ✅ 必需 | 用户、品牌、语气、反参考、战略原则 |
| DESIGN.md | 强烈推荐 | 颜色、排版、层级、组件 |

加载命令：
```bash
node scripts/load-context.mjs
```

### Register 识别规则

1. 任务线索（"landing page" → brand，"dashboard" → product）
2. 当前页面的表面类型
3. PRODUCT.md 中的 `register` 字段

加载对应参考文件：
- `reference/brand.md` — 品牌注册设计规范
- `reference/product.md` — 产品注册设计规范

---

## 共享设计法则（两者通用）

### 配色
- 使用 OKLCH 色彩空间，接近 0 或 100 明度时降低色度
- 不要用纯 `#000` 或 `#fff`，每个中性色向品牌色偏 0.005–0.01 chroma
- 选择**色彩策略**后再选颜色：
  - **Restrained**（克制）：染色中性色 + 一个强调色 ≤10%
  - **Committed**（投入）：一个饱和色覆盖 30–60% 表面
  - **Full palette**（全调色板）：3–4 个命名角色
  - **Drenched**（浸透）：表面本身就是颜色

### 字体
- 正文行长度控制在 65–75ch
- 层级通过字号+字重对比实现（≥1.25 比例），避免扁平标尺

### 布局
- 变化间距来创造节奏，统一间距 = 单调
- 卡片不是万能答案，嵌套卡片永远是错的
- 不需要把所有东西包在容器里

### 动效
- 不要动画 CSS 布局属性
- 缓出用指数曲线（ease-out-quart / quint / expo），不要弹跳或弹性

### 七条绝对禁止
1. **侧边条纹边框** — `border-left/right > 1px` 彩色装饰线
2. **渐变文字** — `background-clip: text` 渐变
3. **玻璃拟态作为默认** — 随意使用的毛玻璃
4. **英雄指标模板** — 大数字+小标签+折线图+渐变
5. **相同卡片网格** — 图标+标题+正文的重复卡片
6. **模态框作为首选** — 非模态方案优先
7. **AI 雷同检测** — 让人一看就是 AI 做的就是失败

### 主题选择
不要默认选暗色或亮色。先写一句**物理场景**描述（谁、在哪、什么光线、什么心情），直到场景本身强制决定主题。

---

## 子命令一览

| 命令 | 分类 | 说明 | 参考文件 |
|------|------|------|---------|
| `craft [feature]` | 构建 | 从规划到构建完整功能 | reference/craft.md |
| `shape [feature]` | 构建 | 写代码前规划 UX/UI | reference/shape.md |
| `teach` | 构建 | 设置 PRODUCT.md 和 DESIGN.md | reference/teach.md |
| `document` | 构建 | 从现有代码生成 DESIGN.md | reference/document.md |
| `extract [target]` | 构建 | 提取可复用 token 到设计系统 | reference/extract.md |
| `critique [target]` | 评估 | UX 设计审查 + 启发式评分 | reference/critique.md |
| `audit [target]` | 评估 | 技术质量检查（a11y/性能/响应式） | reference/audit.md |
| `polish [target]` | 精修 | 发货前的最终质量检查 | reference/polish.md |
| `bolder [target]` | 精修 | 放大平淡的设计 | reference/bolder.md |
| `quieter [target]` | 精修 | 压低过度刺激的设计 | reference/quieter.md |
| `distill [target]` | 精修 | 剥离到本质 | reference/distill.md |
| `harden [target]` | 精修 | 生产级强化（错误/i18n/边界） | reference/harden.md |
| `onboard [target]` | 精修 | 引导流程、空状态、激活 | reference/onboard.md |
| `animate [target]` | 增强 | 添加有目的的动画 | reference/animate.md |
| `colorize [target]` | 增强 | 为单色 UI 加色彩 | reference/colorize.md |
| `typeset [target]` | 增强 | 改进排版层级和字体 | reference/typeset.md |
| `layout [target]` | 增强 | 修复间距、节奏、视觉层次 | reference/layout.md |
| `delight [target]` | 增强 | 添加个性和记忆点 | reference/delight.md |
| `overdrive [target]` | 增强 | 突破常规极限 | reference/overdrive.md |
| `clarify [target]` | 修复 | 改进 UX 文案和错误信息 | reference/clarify.md |
| `adapt [target]` | 修复 | 适配不同设备和屏幕尺寸 | reference/adapt.md |
| `optimize [target]` | 修复 | 诊断并修复 UI 性能 | reference/optimize.md |
| `live` | 迭代 | 浏览器实时选元素生成方案 | reference/live.md |

---

## 路由规则

1. **无参数**：显示命令菜单，询问用户想做什么
2. **首词匹配命令**：加载对应参考文件，命令后的内容为 target
3. **首词不匹配**：常规设计调用，使用设计法则和 register 参考

---

## 参考文件系统

子命令参考位于 `reference/` 目录，包含：
- craft.md, shape.md, teach.md, document.md, extract.md
- critique.md, audit.md, polish.md
- bolder.md, quieter.md, distill.md, harden.md, onboard.md
- animate.md, colorize.md, typeset.md, layout.md, delight.md, overdrive.md
- clarify.md, adapt.md, optimize.md, live.md
- brand.md, product.md（Register 参考）
- cognitive-load.md, color-and-contrast.md, interaction-design.md
- motion-design.md, personas.md, responsive-design.md
- spatial-design.md, typography.md, ux-writing.md
- heuristics-scoring.md, codex.md

## 脚本系统

辅助脚本位于 `scripts/` 目录：
- `load-context.mjs` — 加载 PRODUCT.md / DESIGN.md 上下文
- `live.mjs` + `live-*.mjs` — 浏览器实时迭代系统
- `pin.mjs` / `unpin.mjs` — 快捷方式管理
- `impeccable-paths.mjs` — 路径解析
- 其他实用脚本

## 子 Agent 系统

子 Agent 指令位于 `agents/` 目录：
- `impeccable-asset-producer.md` — 素材制作 Agent（在 craft 工作流中处理图片裁剪、去背景、格式转换等任务，由主 Agent 委派调用）

---

## 设计模式选择决策树

```
用户需求 → 属于哪种场景？

  ├─ 输出设计代码 → 返回 S8-网页设计 Hub 分流
  ├─ 设计规划/UX 评审 → 界面淬炼 critique / audit
  ├─ 设计精修/视觉提升 → 界面淬炼 polish / bolder / quieter
  ├─ 设计增强/加动画加色彩 → 界面淬炼 animate / colorize
  └─ 设计修复/文案优化 → 界面淬炼 clarify / adapt / optimize
```
