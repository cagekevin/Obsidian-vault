# 第二大脑入口

我是 Kevin。这个 vault 不只是我的笔记库——它是 AI 了解我这个人、跟上我的思维方式的入口。AI 每次运行必须先读这个文档。

---

## 首次启动流程

AI 第一次进入这个 vault 时，按这个顺序做，不要跳步：

1. **读本文件（CLAUDE.md）** — 了解我是谁、文件夹地图、核心规则
2. **去 `Context/` 读必读的 4 个文件**（profile/goals/brand/style）— 了解我的身份、目标、品牌、风格、做事方式。schema.md 需要处理新资料时再读
3. **去 `Daily Notes/` 读最近几天的日志** — 了解我最近在做什么
4. **等 Kevin 给第一个任务** — 在这之前不要自作主张做任何事

**之后每次新 session（包括首次之后的所有 session）：**

1. 读本文件（CLAUDE.md）
2. **读 `.codebuddy/memory/` 下最近 3 天的校准日志** — 了解 AI 最近犯过什么错、沉淀了什么规则
3. 读 `Daily Notes/` 最近几天的日志 — 了解我最近在做什么
4. 读 `Context/` 的必读 4 个文件（只需读一次，后续 session 跳过）
5. 读 `.codebuddy/memory/MEMORY.md` — 长期记忆（只需读一次，后续 session 跳过）

---

## 关于我

我是 Kevin。我做两件事：
1. **技能创作** — 设计 AI 工作流，让机器替我干重复活
2. **视频制作** — 从剧本到出片的 AI 视频流水线，皮克斯 3D 动画风格

我不是在"记笔记"。我是在**搭建一个属于我自己的 AI 分身**。这个 vault 里的每一条笔记、每一个技能、每一个项目，都是训练数据。AI 读得越多，就越了解我是谁、我在乎什么、我怎么思考。

详细的我是谁 → 去读 `Context/`：
- `Context/profile.md` — 我的身份、领域、技术栈
- `Context/goals.md` — 我的核心目标
- `Context/brand.md` — 我的个人品牌和内容调性
- `Context/style.md` — 我的表达风格和做事方式
- `Context/schema.md` — **AI 加工信息的完整工作流（Ingest → Query → Lint）**

**AI 每次 session 启动流程：**

1. 读本文件（CLAUDE.md）
2. **读 `.codebuddy/memory/` 下最近 3 天的校准日志** — 了解 AI 最近犯过什么错、沉淀了什么规则
3. 读 `Daily Notes/` 最近几天的日志 — 了解我最近在做什么
4. 读 `Context/` 的必读 4 个文件（profile/goals/brand/style，**只需读一次**，后续 session 跳过）
5. 读 `.codebuddy/memory/MEMORY.md` — 长期记忆（**只需读一次**，后续 session 跳过）

---

## 文件夹地图——我的世界是怎么组织的

每个文件夹都反映了我生活的一个侧面。**AI 按这个地图导航，不要扫整个 vault。**

| 文件夹 | 这是关于我的什么 | AI 要怎么做 |
|--------|-----------------|-----------|
| `Context/` | **我是谁** — 我的身份、目标、品牌、风格 | **每次 session 启动先读这里所有文件** |
| `Skills/` | **我的工作方法论** — 自动化流程和最佳实践 | Kevin 需要 AI 做事时，**来这里找对应技能的 SKILL.md** |
| `Reading/` | **我的知识来源** — 我看过的书、受过的启发 | Kevin 导入读书高亮后，**AI 来这里整理成规范笔记** |
| `Clippings/` | **我关注的世界** — 我在网上保存的有价值内容 | Kevin 说"吸收"/"ingest"时，**AI 来这里读原始资料 → 按 Wiki/skills/ingest.md 流程整理到 Wiki/**。Kevin 需要引用之前保存的内容时，也**来这里找** |
| `Daily Notes/` | **我今天的脑子** — 我每天在想什么、卡在哪里 | **新 session 先读最近 3 天的日志**，跟上 Kevin 的节奏 |
| `Projects/` | **我做过的项目** — 我的实战经验 | 开始或继续项目时，**来这里找项目入口文件** |
| `Wiki/` | **AI 构建的知识图谱** — 从原始资料提取的原子化概念页面 | Kevin 放入新资料后，**AI 来这里创建/更新页面**；Kevin 提问时，**优先基于这里回答**。说"吸收"/"ingest"/"lint"/"query"/"save"时，**去 SKILLS.md 找对应入口** |
| `Tools/` | **我的工具箱（兔子）** — 我常用的实用脚本 | Kevin 说"兔子"、"用 xx 工具"时，**来这里找对应脚本**。**"网页工具"** = `Tools/网页工具.py`（原 browser_control.py） |

**什么情况下不用读：**
- 日常聊天、简单问答 → 不用读任何文件夹
- 只需要查一个信息 → 先去 CLAUDE.md 判断去哪个文件夹，**只读那一层**

**具体场景举例：**
- Kevin 要写视频脚本 → **先去读 `Context/brand.md`** 了解内容调性，**再去 `Skills/` 找视频创作技能**
- Kevin 导入了 Apple Books 高亮 → **去 `Reading/` 把高亮内容整理成规范笔记**
- Kevin 要继续昨天的项目 → **先读最近几天的 `Daily Notes/`** 了解进度，**再去 `Projects/` 找对应项目**
- Kevin 突然有了灵感或碎碎念 → 记录到当天的 `Daily Notes/` 里，**AI 后续主动帮 Kevin 整理和二次创作**
- Kevin 想整理读书笔记 → **去 `Reading/` 文件夹看**
- 不知道怎么处理 Token 消耗 → **去读 Daily Notes 的 instructions.md**，里面有渐进式披露的规则

---

## AI 的工作流程

每次 Kevin 让 AI 做任何事，按这个流程走：

1. **先读 CLAUDE.md**（这个文件）——了解 Kevin 是谁、有哪些文件夹、规则是什么
2. **读 SKILLS.md 和 TOOLS.md** —— 知道仓库里有哪些技能和工具
3. **判断要去哪个文件夹** —— 根据任务类型决定
4. **读目标文件夹的 instructions.md** —— 了解这个文件夹的结构、命名规则、操作方法
5. **执行任务** —— 去对应的子文件夹读写文件

**AI 永远只读当下需要的那一层。** 不需要把整个笔记库全扫一遍。

---

## 核心规则

1. **进入任何文件夹前，必须先读该文件夹里的 instructions.md** — 这是强制规则。
2. **渐进式披露，按需索取** — 每次只给 AI 当前任务所需的上下文。
3. **Daily Notes 接力 + 待办提取** — 新 session 先读最近几天的 Daily Notes 了解进度。一天结束时把今天做了什么、需要跟进的事情**追加**到当天日志末尾，不删不改原有内容。同时检查末尾是否有"明天要做/下周要做"的内容，自动提取到 `TODO.md`（无则创建）。**session 结束前检查当天日志和校准日志是否已写，没写就提醒 Kevin。**
4. **不改 Context/** — Context/ 下的文件由 Kevin 手动维护，AI 不要修改。
5. **本地文件 + 代码化 = AI 最擅长** — 能本地化、能用代码编译的东西，AI 就可以很好地操作。
6. **Folder as a App** — 在 AI 时代，很多问题用一个文件夹就能解决。文件按结构组织好，AI 就能当应用用。
7. **非文本文件不进 Git** — 图片/视频/音频/模型/设计源文件等非文本文件不进仓库。**下载的文件放 `Temp/`**（已 gitignore），转录完的文字稿移入 `Clippings/raw/`。**如果 AI 发现 vault 里有非文本文件，自动把它加到 `.gitignore` 里**，然后告诉 Kevin 加了什么。文本文件（.md/.py/.json/.sh 等）正常进 Git。
9. **记忆写入规则** — 当 Kevin 说"写入记忆"时，用 `replace_in_file` **追加**到当天校准日志 `.codebuddy/memory/YYYY-MM-DD.md`，不覆盖。除非 Kevin 明确说"写到长期记忆"才写 `.codebuddy/memory/MEMORY.md`。**AI 不得擅自修改 MEMORY.md。**
8. **周复盘分析** — 新 session 发现 `复盘/` 有未填分析的复盘文件时，按文件中的 1→6 顺序依次填写，每填完一项等确认再填下一项。

---

## 直接说就行

不用懂这套系统怎么搭的：

- "请帮我把我最近的碎碎念整理成一篇文章"
- "给我几个创作的灵感"
- "帮我整理一下今天的 Daily Notes"
- "这个项目做到哪了？下一步要做什么？"
- "帮我读一下这本书的笔记，总结核心观点"
- "把这篇推文保存到我的 Clippings"

---

## 依赖安装

### 核心原则

依赖统一装在最合适的层级，**能共享就不重复装**。

| 类型 | 安装位置 | 管理工具 |
|------|---------|---------|
| Node | vault 根目录（`g:/Obsidian-vault/node_modules/`） | npm（Windows）/ pnpm（Mac） |
| Python | 系统全局（不建虚拟环境） | uv |

Node.js 会自动向上搜索 `node_modules`，子项目不需要安装。

### Node 依赖

```bash
# 首次安装
cd <vault根目录>
npm install

# 新增依赖
npm install <包名>
```

### Python 依赖

```bash
# 首次安装
uv pip install -r requirements.txt

# 新增依赖
uv pip install <包名>
```

Python 统一用 `uv` 管理，不建虚拟环境。依赖记录在 vault 根目录的 `requirements.txt` 中。

### 各项目特殊依赖

如果某个项目有无法共享的特殊依赖，在该项目目录下放自己的 `requirements.txt`（Python）或 `package.json`（Node），并在该项目文件夹的 `instructions.md` 中注明。

### 环境差异

| 环境 | Node 包管理器 | Python 包管理器 |
|------|-------------|----------------|
| Mac | pnpm（主环境） | uv |
| Windows | npm（双机环境） | uv |

`package.json` 和 `requirements.txt` 保持跨平台一致。

---

## 关于这个系统

**Obsidian 是 IDE，AI 是程序员，Wiki 是代码库。** — Karpathy
AI 的身份不是聊天机器人，是这个知识库的"程序员"：维护 Wiki、更新交叉引用、保持内容一致。Kevin 负责策展来源和提问题，AI 负责执行。

这个系统没有"完成"状态。我的工作流还在不断改进中。**几个月以前这个 vault 还是空的，但现在一旦开了口，它就能认出我这个人了。**

> 我们每天接触大量的原始信息——推文、文章、会议记录、读书笔记。这些信息乱七八糟的，不好直接使用。如果用 LLM 把这些信息本地结构化地编译，然后用 Obsidian + AI 去查看和操作，那就拥有了一个随着时间积累、越来越强的个人知识系统。

这不是某个 AI 公司卖给我的功能，这是我完全自己搭建出来的、完全本地化、完全私有的、任何 AI 都可以使用的系统。
