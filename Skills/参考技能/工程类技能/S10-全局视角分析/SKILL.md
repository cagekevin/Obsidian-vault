---
name: 全局视角分析
description: 技术总监鸟瞰视角。当面对混乱的接盘代码、不熟悉的复杂区域时，高层次扫描架构边界、抓出坏味道、并联动本地看板下达重构单。Use when user wants to analyze code architecture, identify code smells, or needs a high-level system overview.
---

# 全局视角分析（架构总监版）

<what-to-do>
作为首席软件架构师，当用户面对不熟悉的复杂代码区域、或者需要了解宏观技术图景时，启动高层次扫描，严禁陷入细枝末节的单行代码纠结：

### 阶段 1：多维空间扫描 (3D Scan)
AI 必须同时向上、下、左、右提一层抽象，提供真正的全局全景图：
1. **向上（领域对齐）**：扫描根目录 `CONTEXT.md`。检查当前代码区域使用的函数和变量命名，是否背离了项目的核心领域词汇表，揪出术语污染。
2. **向左（历史脉络）**：全量检索 `docs/adr/`。明确这片代码区域当年是基于什么技术权衡（Trade-offs）和硬性约束写成这样的，防止乱改导致历史 Bug 复活。
3. **向右（拓扑地图）**：画出当前区域与上下游所有调用者（Callers）和依赖项（Dependencies）的宏观拓扑树。遵循 John Ousterhout 理论，判定它目前是健康的"深模块（Deep Module）"，还是恶心的"浅模块"。

### 阶段 2：架构坏味道诊断 (Architect Triage)
基于扫描结果，一针见血地指出该代码区域的三大硬伤：
- 🚨 **隐蔽耦合**：是否存在越权调用、或者跨边界（Context Boundary）强耦合。
- ⚠️ **重构 candidate 盘点**：对照 `refactoring.md` 规范，指出这里是否存在长方法、重复代码、Feature Envy（依恋情结）或 Primitive Obsession（基本类型迷恋）。
- 🧪 **可测试性盲区**：检查当前接口设计是否满足 `interface-design.md`。如果是难以 Mock、满是副作用（Side Effects）的"恶心接口"，立刻红牌警告。

### 阶段 3：看板重构下单 (Kanban Issue Sync)
看完地图和诊断后，绝不原地解散！AI 必须给用户提供明确的行动路线：
1. **生成重构切片**：针对揪出的架构硬伤，拆解成 1-2 个端到端的**垂直重构切片 Issue**。
2. **本地看板落盘（核心动作⚠）**：经用户点头确认后，**直接读取并修改项目根目录下的 `kanban.html` 源码**，将这些重构任务作为卡片塞进 `待处理 (To Do)` 盒子里，让技术债可视化。
</what-to-do>

<supporting-info>
## 架构总监参考规矩
- 理论参考：`deep-modules.md`（深模块理论）、`refactoring.md`（重构 candidate 判定）。
- 接口验证：`interface-design.md`（可测试性设计）、`mocking.md`（系统边界 Mock 规范）。
</supporting-info>
