---
name: 闭环开发与调试
description: Write new features (TDD) or diagnose hard bugs (debug loop). Both revolve around building a fast, deterministic feedback loop, then iterating to green. Use when user wants to build features, fix bugs, or diagnose failures.
---

# 闭环开发与调试大师

<what-to-do>
无论是写新业务还是修老Bug，核心逻辑相同：**建立确定性反馈环 → 改代码 → 整理干净**。严禁盲目动手，严格按以下阶段推进。

---

### 阶段 1：构建确定性反馈环 (Build Feedback Loop)
**这是整个技能的灵魂。** 拒绝看代码死猜。投入最高优先级精力，构建一个**自动化、快速、完全确定**的 Pass/Fail 断言信号。

#### 1.1 构建序列
按优先级尝试，直到建立成功：
1. 编写一个直击底层的**集成或单元测试**（参见 `tests.md` 区分好测试与坏测试）。
2. 编写一个针对开发服务器的 **Curl / HTTP 脚本**。
3. **CLI 调用**，将 stdout 与已知正确的 Snapshot 比对。
4. **Playwright / Puppeteer** 无头浏览器脚本。
5. **Replay 重放**：将真实的请求 Payload 保存到磁盘，在隔离环境回放。
6. **Throwaway 测试桩**：启动系统的最小子集，单个函数调用触发目标路径。
7. **属性 / 模糊测试循环**：运行 1000 次随机输入，寻找失败模式。
8. **Bisection 二分查找桩**：自动化"在状态 X 启动 → 检查 → 重复"流程，配合 `git bisect run`。
9. **Differential 差分对比**：同一输入在新旧版本下对比输出差异。
10. **HITL bash 脚本**：最后底牌——使用 `scripts/hitl-loop.template.sh` 由脚本驱动人类操作，输出反馈给 AI。

#### 1.2 循环自检
- **确认反馈环输出的错误与用户描述的原始症状完全一致**（只是恰好失败的附近 Bug 是没有价值的）。
- 确认失败可稳定复现（非确定性 Bug 至少达到可调试的复现率——跑 100 次、并行化、压时间窗口、注入 sleep 来提升）。
- 确认后写新需求必须先看到 RED（测试失败）。
- **优化反馈环本身**：能不能更快？信号能不能更清晰？能不能更确定？

#### 1.3 真构建不出反馈环的退路
明确告诉用户。列出尝试过的方法。向用户请求：(a) 能复现的环境访问权，(b) 捕获的 Artifact（HAR 文件、日志转储、录屏带时间戳），(c) 在生产环境加临时探针的授权。**绝不能在没有反馈环的情况下进入假设阶段。**

> 无确定性信号只看代码 = 浪费时间。在拥有你相信的反馈环之前，不要继续。

---

### 阶段 2：规划与设计验证 (Planning & Hypothesis)

#### 2.1 新需求规划
在动工前，完成以下确认（优先确认用户最关注的行为——不可能测试一切）：
- [ ] **接口变化**：公共接口长什么样？需不需要用户确认？
- [ ] **测试策略**：哪些外部行为最核心？（拒绝测私有实现细节，参见 `mocking.md` 规范。）
- [ ] **深模块机会**：识别可封装复杂逻辑的深模块候选（`deep-modules.md`）。
- [ ] **可测试性**：按 `interface-design.md` 为测试设计接口。

#### 2.2 硬核 Bug 诊断
在修改任何变量前，必须列出 **3-5 个排名的、可证伪的假设**：
> 格式：*"如果是 X 引起的，那么改变 Y 就会导致 Bug 消失/变糟。"*

在假设结构形成前，严禁单假设锚定。**向用户展示排名列表**，他们往往有领域知识能瞬间重排。不要阻塞——用户不在线则按 AI 排名进行。

依假设精准下达探测针：
- 优先用 **Debugger / REPL 断点**（一个断点胜过十条日志）。
- 其次用**定向日志**，每条使用唯一前缀 `[DEBUG-xxxx]`。
- 禁止"什么都要记然后 grep"。
- **性能回退不走日志**。建立基线测量（`performance.now()` / Profiler / Query Plan），然后二分。

---

### 阶段 3：垂直红绿迭代 (Tracer-Bullet Implementation)

| 错误方式（水平切片） | 正确方式（垂直示踪弹） |
|---|---|
| RED: test1, test2, test3... | RED→GREEN: test1→impl1 |
| GREEN: impl1, impl2, impl3... | RED→GREEN: test2→impl2 |

**规则 (红线)：**
- 一次只写一个测试（一个 Assertion 通过）。
- 只写能让当前测试通过的最小代码，不为未来设想功能写多余代码。
- 若涉及外部系统（DB、外部 API、时间），按 `mocking.md` 通过依赖注入 Mock。**严禁对内部模块乱用 Mock**。
- **Regression Test**：对于 Bug 修复，在修复前写回归测试——但要确认存在**正确的 seam**（能在调用点真实复现 Bug 模式）。如果没有正确 seam，这本身就是发现——说明架构阻止了 Bug 被锁定，记录此问题。
- **修改前确认用户批准计划。**

---

### 阶段 4：重构与战利品清理 (Refactor & Cleanup)
反馈环全绿后，对照 `refactoring.md` 执行：

#### 4.1 代码消肿
- [ ] 消灭重复，提炼长函数。
- [ ] 将复杂逻辑往深模块推（Deep Module）。
- [ ] 在自然的地方应用 SOLID 原则。
- [ ] 每个重构成步骤后重新运行反馈环。

#### 4.2 痕迹清理 (红线)
- [ ] **全局 `grep`**，将所有 `[DEBUG-xxxx]` 带前缀的临时日志删干净。
- [ ] 删除所有临时编写的 throwaway 验证原型。
- [ ] 重新跑原始（未最小化的）场景确认 Bug 不再复现。
- [ ] 回归测试通过（或确认不存在正确 seam 已记录）。
- [ ] 修复后，在 Commit Message 中记录最终成立的那个假设——让下一个调试者学习。

#### 4.3 架构改善建议
问自己：**什么架构调整本来可以阻止这个 Bug？**如果答案是"没有好的测试 seam"或"耦合太深"，将细节交办给 S7-代码架构优化。

### Checklist Per Cycle

```
[ ] 测试描述外部行为，而非实现细节
[ ] 只使用公开接口
[ ] 重构后测试仍能通过
[ ] 代码只够通过当前测试
[ ] 没有添加未来设想功能
```
</what-to-do>

<supporting-info>
## 引用文件
- `deep-modules.md` — 深模块设计规范
- `interface-design.md` — 可测试性接口规范
- `mocking.md` — Mock 边界规范
- `refactoring.md` — 重构候选清单
- `tests.md` — 好坏测试对照表
- `scripts/hitl-loop.template.sh` — 人工探针脚本
</supporting-info>
