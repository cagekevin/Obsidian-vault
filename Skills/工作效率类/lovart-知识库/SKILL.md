---
name: lovart-kb
description: >-
  Lovart AI 设计平台的逆向工程知识库管理和维护。三层管线：(1)数据收集 — run-pipeline.py 编排 W7 lovart.py batch 钓鱼；
  (2)数据整理 — promote.py 晋升碎片，generate-index.py --rebuild 维护索引；
  (3)数据导出 — export-for-notebook.py 合并全量供 NotebookLM 使用。
  Lovart 对话类脚本已迁移至 W7-API链接/lovart-skill/，本知识库只做本地文件操作。
  当用户涉及"深挖/研究/探索 Lovart 知识"或"整理碎片/维护索引/合并导出"时使用。
  工作目录固定为 skills/工作效率类/lovart-知识库/。
---

# Lovart 知识库管理 Skill

## 触发词与激活条件

以下任意情况激活本 Skill：

- "查一下 Lovart 的…" / "Lovart 知识库里关于…"
- "整理 Lovart 碎片 / 晋升 / promote"
- "更新知识库索引 / rebuild / 刷新目录"
- "合并导出知识库 / export / NotebookLM"
- "看看 Lovart 知识库的架构 / catalog"
- "Lovart 有哪些分类 / 目录结构"
- "运行钓鱼 / 深挖 / 套一套"
- "分析图片 / 提取设计规范"（→ 由 W7-API链接 Hub 处理，不经过本 Skill）

---

## 架构总览

```
W7-API链接/lovart-skill/             本知识库 lovart-知识库/
(Lovart 对话唯一入口)                  (纯本地文件操作)
─────────────────────────            ─────────────────────────
agent_skill.py ← 官方API客户端        scripts/catalog.py     ← 配置加载
lovart_client.py  ← 统一封装          scripts/promote.py     ← 碎片晋升
lovart.py ← 对话入口(ask/analyze/    scripts/generate-index.py ← 索引生成
            batch/pipeline)           scripts/run-pipeline.py  ← 编排（调 W7 lovart.py）
run_image_generator.py ← 生图        scripts/export-for-notebook.py ← 导出
run_video_generator.py ← 生视频      00-钓鱼话术/ ← 原始渔获暂存
projects/  ← JSON配置目录            01~08/       ← 分类知识
                                      _meta/       ← 元数据配置
```

**原则：需要跟 Lovart 对话 → W7 / 只看本地文件 → 本知识库**

---

## 快速索引

| 文档 | 内容 |
|------|------|
| [`PIPELINE.md`](PIPELINE.md) | 命题驱动工作流、管线完成后 AI 动作、数据流向、知识库脚本行为 |
| `W7-API链接/lovart-skill/SKILL.md` | agent_skill.py 命令参数 + W7 脚本行为 |
| `W7-API链接/lovart-skill/SKILL.md` | Lovart 生成 SOP |

## 核心命令速查

```bash
# 工作目录
cd skills/工作效率类/lovart-知识库/

# ── 知识库管线 ──
python scripts/run-pipeline.py                 # 一键：钓鱼→晋升→重建索引
python scripts/run-pipeline.py --no-delete     # 不删原始文件
python scripts/promote.py --check              # 检查晋升状态
python scripts/promote.py --batch --delete     # 批量晋升+清理
python scripts/generate-index.py --rebuild     # 重建全部索引
python scripts/export-for-notebook.py          # 导出 NotebookLM

# ── Lovart 对话（经 W7 lovart.py） ──
# 所有模式由一个 JSON 配置控制，项目文件放在 projects/ 目录
python ../../W7-API链接/lovart-skill/lovart.py projects/analyze.json
```

---

## 知识库检索流程（回答用户问题）

当用户说"查一下 Lovart 的…"或类似问题时，按以下流程从已有知识库中找答案：

### 检索步骤

1. **读根索引** → 打开 `data_structure.md`，了解各分类目录的用途
2. **选分类** → 根据问题关键词选择 1-2 个最相关的分类目录（如"图片生成"选 02-提示与生成）
3. **读子索引** → 打开选中目录的 `data_structure.md`，找到最相关的文件名
4. **grep 定位** → 用 `grep` 在选中文件中搜索关键词，定位到具体段落
5. **窗口读取** → 用 `read_file` 配合 offset/limit 读取匹配段落（不要读整文件）
6. **迭代** → 不够就换关键词或换文件，最多 5 轮
7. **回答** → 用找到的内容回答，标注来源文件名

### 检索注意事项

- ❌ 不要直接 `read_file` 读整个文件（知识库文件可能很大）
- ✅ 优先从稳定文章（无 `碎片-` 前缀）中找答案
- ✅ 如果稳定文章不够，再查 `碎片-*.md`（中间态，可能不完整）
- ❌ 不要从 `00-钓鱼话术/` 或 `_meta/` 中找答案（它们不参与检索）
- 如果知识库里没有答案，告诉用户并建议走"深挖"流程来补充

---

## 知识库目录结构

```
lovart-知识库/
├── _meta/                          ← 元数据（不参与导出）
│   ├── catalog.json                ← 配置源：分类、关键词、导出范围
│   ├── fish_tasks.json             ← 钓鱼管线任务队列
│   ├── 跟踪表.md / 套取话术策略.md
├── 00-钓鱼话术/                    ← 原始渔获暂存（不导出）
├── 01-入门/ ~ 08-参考/             ← 整理后知识库
│   ├── data_structure.md           ← 自动生成索引
│   ├── 碎片-*.md                   ← 中间态（原始 Lovart 回复）
│   └── *.md                        ← 稳定文章（手工提炼终态）
├── scripts/                        ← 本地文件操作脚本
├── SKILL.md                        ← 本文档
├── PIPELINE.md                     ← 管线手册+脚本行为
└── README.md                       ← 带自动索引
```

---

## catalog.json 字段说明

```json
{
  "categories": [{
    "dir": "02-提示与生成",
    "label": "核心生成机制与提示词工程",
    "desc": "...",
    "export": true,
    "index_in_readme": true,
    "keywords": ["提示词", "prompt"]
  }],
  "paths": {
    "agent_skill": "W7-API链接/lovart-skill/agent_skill.py"
  }
}
```

---

## 注意事项

- **所有 Lovart 提问必须使用思考模式**：W7 脚本已默认 `--mode thinking`
- **`data_structure.md` 全部自动生成**，不要手工编辑。文件变更后跑 `--rebuild`
- **`promote.py --batch` 按关键词匹配分类**，不准时用手动 `--from/--to`
- **自动分类**基于 `catalog.json` 的 `keywords`，不命中 → `00-钓鱼话术`
- **export 只导出 `export: true` 的目录**，`00` 和 `_meta` 不导出
