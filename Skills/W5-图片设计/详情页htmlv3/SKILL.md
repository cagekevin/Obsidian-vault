---
name: 详情页HTML-v3.1
description: Generate a brand showcase page (HTML + long screenshot + image prompts) from 1 product image + copy. Used when user requests a detail page, showcase page, product landing page, or marketing long-image. Supports Route A (user provides copy) and Route B (AI drafts from claim seeds).
---

# 详情页 HTML v3.1 工作流

## 项目位置

```
skills/工作效率类/W5-图片设计/详情页htmlv3/
```


## 目录结构

```
详情页htmlv3/
├── SKILL.md              # 技能入口文档（核心工作流）
├── PRD.md                # 产品需求文档
│
├── 模板/                 # JSON 模板（供 AI 参考结构后填入项目数据）
│   └── 模板.json
│
├── templates/            # HTML 模板骨架
│   └── template.html     # 通用 HTML 模板
│
├── tokens/               # 设计令牌（11 套主题 CSS）
│   ├── theme-pilgrim-dawn.css     # 朝圣黎明（默认）
│   ├── theme-lyrical-ocean.css    # 诗意深海
│   ├── theme-parisian-chic.css    # 巴黎先锋
│   ├── theme-dark-nexus.css       # 暗夜星云
│   ├── theme-swiss-industrial.css # 瑞士工业
│   ├── theme-apothecary-folio.css # 药剂师文库
│   ├── theme-data-ink.css         # 数据时报
│   ├── theme-brutalist.css        # 野兽派
│   ├── theme-mid-century.css      # 世纪中叶
│   ├── theme-cupertino.css        # 加州白皮书
│   └── theme-data-terminal.css    # 极客终端
│
├── references/           # 参考文档
│   └── references.md     # 结构说明 + visual_description 指南 + 问题排查
│
├── scripts/              # Node.js 自动化脚本
│   ├── init-project.cjs      # Step 1  建项目、复制模板
│   ├── render.cjs            # Step 2  渲染 HTML + 截图 + 生图 Prompt
│   └── check.cjs             # Step 3  全面校验（叙事/合规/模板/输出物）
│
```

## 核心流程（6 步）

### Step 0 · 项目初始化与数据抽取（AI 完成）
1. 在 `1_Active/` 下创建项目目录（如 `1_Active/XX产品名/`）
2. 运行 `init-project.cjs` 建目录、复制 HTML 模板 + 默认主题 + JSON 模板
3. AI 修改项目根目录下的 `brand-spec.json`，把模板字段替换为项目数据
4. 确认用户是否有产品图（无图则退出）
5. 判断路由：
   - **路由 A**：用户有完整 8 屏文案 → AI 填入 JSON
   - **路由 B**：用户仅有产品图 + 至少 3 个核心声明 → AI 扩写 8 屏文案，回问用户确认
6. 结构参考 `references/references.md`
7. `visual_description` 写法参考 `references/references.md`

### Step 1-3 · 顺序执行
```bash
# 用法一（项目建在 Temp/ 下）：
node scripts/init-project.cjs <ProjectName>    # 建目录、复制模板
node scripts/render.cjs <ProjectName>           # 渲染 HTML + 生成 Prompt
node scripts/check.cjs <ProjectName>            # 全面校验（有问题就改）
node psd/html-to-psd.cjs <ProjectName> "<ProjectRootDir>"  # 导出截图 + PSD

# 用法二（指定项目目录，如 1_Active 下）：
node scripts/init-project.cjs <ProjectName> "<ProjectRootDir>"
node scripts/render.cjs <ProjectName> "<ProjectRootDir>"
node scripts/check.cjs <ProjectName> "<ProjectRootDir>"
node psd/html-to-psd.cjs <ProjectName> "<ProjectRootDir>"
```

## 核心规则

1. **brand-spec.json 驱动一切** — 所有脚本从 JSON 读取数据，不靠 AI 改代码
2. **文案/视觉解耦** — `text_exact` 只进 HTML，`visual_description` 只进 Prompt，绝对不能串
3. **Fail Fast** — 报错就中断，不做静默修补
4. **展示页定位** — 禁止电商转化词（立即购买/加购/领券/限时/包邮等）

## 遇到问题

先查 `references/references.md` 的"常见问题排查"章节，找不到再问用户。

## 输出物

```
<ProjectRootDir>/
├── index.html          # 渲染完的 8 屏展示页 HTML
├── copy.md             # 8 段文案复核稿
├── tokens/theme.css    # 当前主题（由 theme 字段自动注入）
└── output/
    ├── screen_01~08.png    # 单屏切片
    ├── full_long.png       # 拼接长图
    └── prompt_01~08.txt    # 8 段生图 Prompt
```
