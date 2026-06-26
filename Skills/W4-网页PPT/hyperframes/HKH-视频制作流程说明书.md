# HKH Plant Retinol 视频制作 · 全流程中文说明书

本文档说明如何使用 `video-spec-builder` + `HyperFrames` 两个 Skill 制作一条 30 秒抖音竖屏品牌视频。

---

## 一、文件清单

### 1.1 Skill 文件（在 skills-main 仓库内）

| 文件路径 | 作用 |
|----------|------|
| `skills/工作效率类/W4-网页PPT/hyperframes/SKILL.md` | **video-spec-builder 主技能**。定义所有追问、分镜拆解、交付物格式。AI 读这份文件来执行"帮用户理清想法→产出 video-spec.md"的完整流程 |
| `skills/工作效率类/W4-网页PPT/hyperframes/templates/video-spec-template.md` | **分镜脚本模板**。每个 `[方括号]` 是占位符，AI 按此格式生成最终的 `video-spec.md` |
| `skills/工作效率类/W4-网页PPT/hyperframes/references/components-catalog.md` | **69 个标准组件目录**。填写分镜表时每镜要锚定一个组件 ID（如 `broll-hero.big-type`），定义了每个组件的用途/何时用/何时不用 |
| `skills/工作效率类/W4-网页PPT/hyperframes/references/spec-rules.md` | 字段约束和自检清单，交付前 AI 必须过一遍 |
| `skills/工作效率类/W4-网页PPT/hyperframes/references/scene-breakdown.md` | 逐字稿拆分成镜的方法论 |
| `skills/工作效率类/W4-网页PPT/hyperframes/references/pacing-rules.md` | 节奏/时长/转场密度规范 |
| `skills/工作效率类/W4-网页PPT/hyperframes/references/question-bank.md` | 追问问题库（5 个 Phase），防止 AI 漏问关键信息 |
| `skills/工作效率类/W4-网页PPT/hyperframes/references/dialogue-style.md` | 对话风格范本 |
| `skills/工作效率类/W4-网页PPT/hyperframes/references/workflow-0-1.md` | 从零开始做视频的 5 阶段详细步骤 |
| `skills/工作效率类/W4-网页PPT/hyperframes/references/workflow-iteration.md` | 已有视频脚本后迭代修改的流程 |
| `skills/工作效率类/W4-网页PPT/hyperframes/examples/video-spec-spacex.md` | 示例：SpaceX 视频的完整分镜脚本，作为产出格式参考 |
| `skills/工作效率类/W4-网页PPT/hyperframes/Full Code/app.jsx` | HyperFrames 渲染引擎主入口 |
| `skills/工作效率类/W4-网页PPT/hyperframes/Full Code/styles.css` | 渲染引擎全局样式 |
| `skills/工作效率类/W4-网页PPT/hyperframes/Full Code/tokens.css` | 设计变量 |
| `skills/工作效率类/W4-网页PPT/hyperframes/Full Code/tweaks-panel.jsx` | 调试面板 |
| `skills/工作效率类/W4-网页PPT/hyperframes/Full Code/sections/*.jsx` | 11 个渲染组件（aroll / broll-hero / broll-charts 等） |
| `skills/工作效率类/W4-网页PPT/hyperframes/README.zh.md` | 中文使用说明 |

### 1.2 HyperFrames 渲染端文件（项目 `.agents/skills/hyperframes/` 下）

| 文件路径 | 作用 |
|----------|------|
| `.agents/skills/hyperframes/SKILL.md` | **HyperFrames 渲染技能**。HTML 组成规范、GSAP 动效规则 |
| `.agents/skills/hyperframes/house-style.md` | 设计基调（颜色、背景层、动效） |
| `.agents/skills/hyperframes/visual-styles.md` | 8 个视觉预设 |
| `.agents/skills/hyperframes/references/video-composition.md` | 构图规则：每镜 8-10 元素、色彩要求 |
| `.agents/skills/hyperframes/references/motion-principles.md` | GSAP 动效原则 |
| `.agents/skills/hyperframes/references/prompt-expansion.md` | 提示词扩展规范 |
| `.agents/skills/hyperframes/references/typography.md` | 字体规范 |
| `.agents/skills/hyperframes/references/beat-direction.md` | 每场设计格式 |
| `.agents/skills/hyperframes/references/design-picker.md` | 设计选择器 |
| `.agents/skills/hyperframes/palettes/*.md` | 9 套配色预设 |

### 1.3 依赖 Skill（自动安装）

| 名称 | 作用 |
|------|------|
| `hyperframes-cli` | CLI：`hyperframes render` / `init` / `lint` / `preview` |
| `hyperframes-media` | 媒体处理：TTS 配音、字幕、去背景 |
| `gsap` | 动画引擎 |
| `animejs` / `three` / `waapi` / `tailwind` | 备选渲染库 |
| `remotion-to-hyperframes` | Remotion 转换 |

---

## 二、全流程步骤

### 第 1 步：安装

```bash
npx skills add heygen-com/hyperframes
npx skills add feicaiclub/video-spec-builder
```

**前置：** Node.js ≥ 22

### 第 2 步：产出分镜脚本 `video-spec.md`

AI 读 `hyperframes/SKILL.md` 对话收集需求 → 按 `video-spec-template.md` 格式输出。

引用文件：
- `components-catalog.md`（选组件 ID）
- `spec-rules.md`（字段约束）
- `question-bank.md`（追问题库）

### 第 3 步：扩展为精细制作说明 `.hyperframes/expanded-prompt.md`

AI 读 `prompt-expansion.md`，将 `video-spec.md` 扩展为逐场设计。

引用文件：
- `house-style.md` / `video-composition.md` / `motion-principles.md`
- `beat-direction.md` / `typography.md`

### 第 4 步：写 HTML 组成 `index.html`

AI 按 HyperFrames SKILL.md Step 3 构建：
1. 先写 CSS 最终布局
2. 再加 GSAP 动画
3. 注册 `window.__timelines.root = tl`

### 第 5 步：渲染

```bash
npx hyperframes render . -o renders/视频名.mp4 --quality=high
```

### 第 6 步：迭代

看 MP4 → 反馈 → 改 `index.html` → 重新渲染
