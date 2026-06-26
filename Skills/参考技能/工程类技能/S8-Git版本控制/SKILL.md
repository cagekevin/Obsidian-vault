---
name: Git版本控制
description: Git 工作流标准化——Conventional Commits 规范、分支策略、冲突解决、常用操作速查。贯穿所有开发环节的基础设施。触发词：提交、分支、冲突、merge、push、pull。
metadata:
  pattern: tool-wrapper
---

# Git 版本控制

<what-to-do>

## Commit 规范（Conventional Commits）

```
<type>(<scope>): <简短描述>

<可选详细说明>
```

| Type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `refactor` | 重构（不修 Bug 不加功能） |
| `test` | 增加/修改测试 |
| `docs` | 文档 |
| `chore` | 构建/工具/依赖 |
| `style` | 代码格式（非逻辑变更） |

## 分支策略

- `main` — 生产就绪，只接收合并
- `feat/<名称>` — 功能开发分支
- `fix/<名称>` — Bug 修复分支
- 完成后 squash merge 回 main，保持历史干净

## 冲突解决流程

1. `git merge <源分支>` → 看到冲突
2. 搜索 `<<<<<<<` 定位冲突
3. 逐块决定保留哪边（或组合）
4. 删掉 `<<<<<<<` `=======` `>>>>>>>` 标记
5. `git add . && git commit` 完成合并

## 常用操作

| 要做什么 | 命令 |
|---------|------|
| 新分支 | `git checkout -b feat/xxx` |
| 暂存改动 | `git stash` / `git stash pop` |
| 修改上次 commit | `git commit --amend` |
| 交互式 rebase | `git rebase -i HEAD~N` |
| 撤销工作区改动 | `git checkout -- <file>` |

</what-to-do>
