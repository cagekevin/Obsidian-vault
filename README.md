# 我的第二大脑

Obsidian vault 管理我的知识体系、技能库、项目文档和个人笔记。

## 结构

- `Context/` — 我是谁（身份、目标、品牌、风格、Schema）
- `Skills/` — 我的工作方法论（AI 技能定义）
- `Tools/` — 实用脚本
- `Reading/` — 读书笔记
- `Clippings/` — 网页剪藏 + `raw/` 原始资料
- `Wiki/` — AI 构建的知识图谱
- `Daily Notes/` — 每日工作日志
- `Projects/` — 项目文档

## 首次使用

```bash
# Python 依赖
uv pip install -r requirements.txt

# Node 依赖（如果有）
pnpm install
```

## 快捷指令

| 指令 | 作用 |
|------|------|
| `bash sync.sh` | 扫描技能清单 → commit → push |
| 全推 / 注册一下 | 自动扫描、更新配置、commit、push |
| 全拉 | git stash → git pull → git stash pop |
| "兔子" / "tools" | 去 Tools/ 找对应脚本 |
| "用 S1" / "加载 W5" | 去 Skills/ 找对应技能 |

## 大文件处理

GitHub 只存纯文本（.md、.py、.json、.sh 等）。

- 临时下载的文件放 `Temp/`（已 gitignore）
- 模型文件按工具默认位置下载，Git 不跟踪
- AI 发现 vault 里有非文本文件会自动加 `.gitignore`
