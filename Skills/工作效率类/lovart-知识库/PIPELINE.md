# Lovart 知识库管线手册

---

## 命题驱动工作流（人类→AI 协作闭环）

这是最常用的流程：**人类出命题，AI 设计框架 + 写队列，Python 脚本自动执行，人类最后验收**。

### 完整闭环

```
你: "帮我深挖 Lovart 的视频生成能力"
    │
    ▼ (AI 执行)
    │
    ├── 1. 读 _meta/套取话术策略.md 了解套取方法
    ├── 2. 设计框架：拆成哪几个方向（模型选择 / 分镜规划 / 音频合成 / 输出格式）
    ├── 3. 根据 00-钓鱼话术/ 和知识库现状，排除已有内容
    ├── 4. 生成钓鱼话术，写入 _meta/fish_tasks.json
    └── 5. 打印任务清单，告诉你队列已就绪
    │
    你: python scripts/run-pipeline.py             ← 全自动：钓鱼 + 晋升 + 重建索引
       │
       ├── 自动调用 W7 lovart.py batch（每个任务追问×5，存 00-钓鱼话术/）
       ├── 自动运行 promote.py --batch --delete（晋升到分类目录 + 清理原始文件）
       └── 自动触发 generate-index.py --rebuild
       │
    你: 看结果，决定哪些碎片值得提炼成稳定文章
```

### AI 的具体执行流程

当用户说"帮我深挖 XXX"时：

**Step 1 — 设计框架**
- 打开 `_meta/套取话术策略.md` 了解 10 种话术策略
- 打开 `_meta/跟踪表.md` 了解已收集的碎片
- 打开 `00-钓鱼话术/` 和 `01-08/` 目录，排除已有内容
- 设计 3-8 个挖掘方向，每个方向一句话说明
- 先列出来让用户确认，再继续

**Step 2 — 写钓鱼队列**
- 确认后，为每个方向设计 1-3 条钓鱼话术
- 写入 `_meta/fish_tasks.json`，格式：

```json
{
  "tasks": [
    {"label": "视频模型选择逻辑", "prompt": "请详细说明视频生成模型的选择策略和各模型特点"},
    {"label": "多镜头分镜规划", "prompt": "请详细说明多镜头视频的分镜规划流程和参数"}
  ]
}
```

**Step 3 — 打印下一步指令**
```
📋 队列就绪（N 个任务）
   1. 任务1
   2. 任务2

运行以下命令一键全流程：
    cd skills/工作效率类/lovart-知识库/
    python scripts/run-pipeline.py

（会自动执行：钓鱼 → 晋升 → 删除原始 → 重建索引，无需中间介入）
如需保留原始文件不删除：
    python scripts/run-pipeline.py --no-delete
```

### 触发词

- "帮我深挖…" / "研究一下…" / "探索…" / "套一套…"
- "设计框架" / "写队列" / "写到 fish_tasks"
- 用户说这类话 → 执行命题驱动工作流

---

## 管线完成后 — AI 的后续动作

用户跑完 `run-pipeline.py` 后，AI 应主动检查结果并给出建议：

### 检查步骤

1. **看看钓到了什么** → 运行 `python scripts/promote.py --check -v` 查看晋升结果
2. **列出新内容** → 告诉用户新增了哪些碎片、字数、所在目录
3. **给出整理建议** →
   - 字数 ≥ 3000 的碎片 → 建议合并到现有稳定文章或独立成文
   - 字数不足 → 建议继续深挖或放弃
   - 如果碎片中出现了新的工具名（如 `generate_image_nano_banana_2`）→ 提醒用户这和已有知识库中的工具名不一致
4. **等待用户决策** → 用户决定哪些要整理、怎么整理，AI 再执行

### 示例输出

```
📊 本轮收获：
  ✅ 碎片-SKU替换产品完美 (9,520字) → 建议并入 主图复刻流程.md
  ✅ 碎片-光影匹配精确控制 (7,345字) → 建议并入 主图复刻流程.md
  ✅ 碎片-复刻失败回退路径 (4,867字) → 建议独立成文放在 07-能力边界/
  ⚠️ 碎片-品类差异复刻策略 (2,376字) → 偏薄，建议下次深挖补充

要我现在开始合并吗？
```

---

## 初始化检查（首次使用）

如果 `_meta/catalog.json` 不存在，说明知识库尚未初始化：

1. 运行 `python scripts/generate-index.py --rebuild` 生成初始索引
2. 检查 `_meta/fish_tasks.json` 是否存在（空数组也行）
3. 确认 `catalog.json` 中 `paths.agent_skill` 指向的 `agent_skill.py` 存在
4. 确认 W7 lovart-skill 目录中各脚本就位

---

## 数据流向细节：碎片生命周期

```
                  Layer 1（自动）              Layer 2（手动）             Layer 3
原始渔获 ──────────────────────→ 碎片-*.md ─────────────────→ 稳定 *.md ───→ 导出
(self-contained)     promote    (中间态, 保留 Lovart 原文)   手工提炼      export
```

- **碎片-*.md**：保留 Lovart 原始回复的完整上下文，适合参考但不宜直接用于检索
- **稳定 *.md**：手工提炼、去重、结构化后的最终知识，是检索的首选来源
- 同一个主题可以同时存在 `碎片-主题.md`（原始）和 `主题.md`（整理后）

---

## 数据流向（.md 文件完整生命周期）

```
                                    ┌───────────────────┐
                                    │   _meta/           │
                                    │   catalog.json     │ ← 单点配置，所有工具从此读
                                    │   fish_tasks.json  │ ← lovart.py 读取
                                    └────────┬──────────┘
                                             │
  ┌──────────────────┐                       │
  │ Layer 1: 收集    │                       │
  │ lovart.py (W7)     │                       │
  │ 批量对话引擎     │                       │
  └───────┬──────────┘                       │
          │                                  │
          ▼                                  │
  ┌──────────────────┐                       │
  │ 00-钓鱼话术/     │                       │
  │ raw 渔获.md      │                       │
  └────────┬─────────┘                       │
           │                                 │
           │ promote.py --batch              │
           ▼                                 │
  ┌────────────────────────┐                 │
  │ 分类目录/碎片-[主题].md  │ ← 晋升后的中间态
  └────────┬───────────────┘
           │ 手工提炼
           ▼
  ┌──────────────────┐
  │ 分类目录/[主题].md │ ← 稳定文章（整理后终态）
  └────────┬─────────┘
           │ export-for-notebook.py
           ▼
  ┌──────────────────────────────────┐
  │ ~/Desktop/lovart-知识库全量.md    │ → 拖入 NotebookLM
  └──────────────────────────────────┘
```


---

## 知识库本地脚本行为

### catalog.py（配置加载器）
读取 `_meta/catalog.json`，提供 KB_DIR 和分类关键词映射。promote.py 和 generate-index.py 的共同依赖。

### promote.py（碎片晋升）
晋升规则：`00-钓鱼话术/主题.md` → `{分类目录}/碎片-主题.md`
匹配策略：精确匹配 → 旧版兼容 → 子串匹配 → 视为未晋升
自动分类：按 `catalog.json` keywords 匹配，不命中 → `02-提示与生成`
`--batch`：晋升后自动 `generate-index.py --rebuild`

```bash
python scripts/promote.py --check
python scripts/promote.py --batch --delete
```

### generate-index.py（索引生成）
`--rebuild`：为 01~08/ 生成 data_structure.md + 更新 README 索引
`--print`：只打印不改文件

### run-pipeline.py（管线编排）
不直接调 Lovart。流程：W7 lovart.py → promote.py → generate-index --rebuild

```bash
python scripts/run-pipeline.py
python scripts/run-pipeline.py --no-delete
```

### export-for-notebook.py（导出）
合并全量知识库 → 桌面文件 → NotebookLM。
