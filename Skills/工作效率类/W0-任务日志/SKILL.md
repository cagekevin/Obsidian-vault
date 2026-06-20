---
name: 任务日志
description: 任务+知识双管理。触发词：log、任务、待办、记一下、要做什么、汇总、存一下、note、备忘、查一下、探索、调研。
metadata:
  pattern: tool-wrapper
---

# 任务日志

<what-to-do>

## 上下文检测

| 工作区特征 | 模式 | 操作目标 |
|-----------|------|---------|
| 有 `backlog/` 目录 | **看板模式** | `backlog/active.md`（待办）+ `backlog/note.md`（备忘）+ `backlog/work/`（探索） |
| 无 `backlog/` | **项目模式** | `TODO.md`（待办，没有则自动创建）+ `NOTE.md`（备忘，按需创建） |

> **看板模式** = 在 skills-main 自身运行。所有操作走 backlog/ 三件套。
> **项目模式** = 在 `1_Active/` 下或任意外部项目目录。待办走 TODO.md，备忘走 NOTE.md。

## 操作表

### 看板模式（skills-main）

| 你说 | AI 行为 |
|------|---------|
| `记一下 XXX` | 追加到 `backlog/active.md`，自动分配 `#n` 编号 |
| `要做什么` / `log` / `今天干嘛` | 读 `backlog/active.md`，分组显示：活跃 → 待办 → 阻塞中 |
| `开始做 #n` | 标记为 `[active]`，检查依赖是否就绪 |
| `#n 做完了` | 标记为 `[done]`，然后删行（保持清爽），提示哪些被阻塞的任务现在可以做了 |
| `#n 卡住了` / `#n 等 XXX` | 标记为 `[blocked]`，记录阻塞原因 |
| `存一下 XXX` | 追加到 `backlog/note.md` |
| `探索一下 XXX` / `调研 XXX` | 写入 `backlog/work/` 目录 |
| `查一下 XXX` / `我的XX在哪` | 搜索 `backlog/note.md` + `backlog/work/` |
| `汇总` | 扫描 `1_Active/` 下所有项目 TODO.md → 询问是否并入 active.md |
| `清理一下` | 找出 active.md 中长期未动的待办，逐条确认删除 |

### 项目模式（外部项目）

| 你说 | AI 行为 |
|------|---------|
| `记一下 XXX` | 追加到 `TODO.md`（没有则自动创建） |
| `要做什么` / `log` / `今天干嘛` | 读 `TODO.md`，列未完成 |
| `XXX 做完了/修好了` | 从 `TODO.md` 删除该行 |
| `存一下 XXX` | 追加到 `NOTE.md`（没有则自动创建，独立于 TODO.md） |
| `查一下 XXX` | 搜索当前项目文件 |
| `探索一下 XXX` | 在当前项目创建 `Temp/` 目录并写入 |
| `项目做完了` | TODO.md 还有 n 项未完成，询问"要全部带回主看板吗？" → 确认后追加到 `backlog/active.md`，清空 TODO.md + NOTE.md |

### 跨模式通用

| 你说 | AI 行为 |
|------|---------|
| `归一下档` | 将 active.md 中超过 1 个月未动的项移入 `backlog/archive/`（不是已完成项，是被遗忘项） |

**关键原则**：
- AI 主动理解完成语义，不需要用户说特定格式。
- **查询时**：主动判断用户想查的是待办还是备忘：
  - "密码/地址/链接/账号/XX在哪" → 搜 note.md
  - "今天干嘛/有什么做/任务/待办/要做" → 读 active.md
- **依赖感知**：做完一个任务时，检查是否有其他任务 `(wait: #n)` 依赖它，告知用户。
- **分辨不清必须问用户，不要猜。**
- 项目模式下 `汇总` 不可用，提示回到看板模式操作。
- **项目做完了** 仅在项目模式下可用，看板模式下无效。

## 任务格式

```
- [ ] #5 [active] 设计Logo          ← 进行中
- [ ] #3 [blocked] 用户登录 (wait: #2)  ← 被 #2 阻塞
- [ ] #7 [pending] 产品主图 (wait: #5)  ← 等 #5 做完
- [ ] #5.1 [active] 出初稿          ← 子任务
```

- **`#n`** — 自动编号，父子级用点号（`#5.1`）
- **`[status]`** — `[active]` 进行中 / `[blocked]` 阻塞 / `[pending]` 等待中（不写 = pending）
- **`(wait: #n)`** — 依赖关系，该任务依赖的任务编号
- **`[标题](相对路径)`** — 附件型任务，引用文件不复制

**做完删行原则不变** — `[done]` 只是标记，最终还是会删掉保持清爽。

## 文件结构

```
skills-main（看板模式）:
backlog/
├── active.md    ← 待办，做完即删，保持 <50行
├── note.md      ← 固定备忘（密码/网址/常用信息，反复查询）
├── work/          ← 探索/调研/实验中转
├── archive/     ← 被遗忘任务归档

外部项目（项目模式）:
TODO.md          ← 待办
NOTE.md          ← 项目备忘
Temp/            ← 探索笔记（按需创建）
```

</what-to-do>

<supporting-info>

## 详细示例

见 `skills/工作效率类/W0-任务日志/references/examples.md`

</supporting-info>
