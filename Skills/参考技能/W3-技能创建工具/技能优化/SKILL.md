---
name: Incremental Forge
description: 'Skill 增量优化流程——定目标 → 诊断基线 → 注入测试 → 迭代锻造 → 门禁上线。Use when an existing skill has poor trigger accuracy, low output quality, or needs performance evaluation. 创建新 Skill 请用 W3-技能创建工具 Mode 1。'
metadata:
  pattern: pipeline
---

# 增量优化锻造台

> 职责：优化已有 Skill。从零创建请走 W3 Hub 的 Mode 1。

---

## 执行流程

### Phase 0：定目标

> 没有目标，诊断就无从谈起。先搞清楚"优化到什么程度算赢"。

逐一确认以下信息，一次只问一题：

1. **要优化哪个 Skill？** — 让用户指定目标 skill 目录路径

2. **你的 Skill 目前有什么问题？**
   - a) 触发不准
   - b) 输出质量差
   - c) AI 不遵守 skill 指令——执行时偏离了 skill 的规定
   - d) 篇幅不合适
   - e) 兼容性差
   - f) 其他

3. **你希望优化到什么程度？**
   - 直接问用户：触发率目标是多少？输出质量目标是多少？误触发率上限是多少？

4. **有没有特定的失败案例？**
   - 问用户：有没有用户说了什么但它没触发的情况？或者它触发了但输出不对的情况？

确认后展示目标摘要，用户确认方可进入 Phase 1。

> **门禁**：用户确认目标摘要。

---

### Phase 1：诊断基线

> 不改任何东西，跑当前版本的评测，拿到基线数据。

根据 Phase 0 确定的问题类型，选择对应的诊断方式：

**问题：触发不准**
- 扫描目标 Skill 目录，检查 `evals/evals.json`、`changelog/`、`benchmark.json`
- 执行 AI 视角通读（详见参考规范）
- 跑触发率基线：
  ```bash
  python3 ../技能创建/scripts/run_eval.py \
    --eval-set <技能目录>/evals/evals.json \
    --skill-path <技能目录> \
    --runs-per-query 3 \
    --verbose
  ```
  输出记录为 `<技能目录>/changelog/baseline.json`
- 展示基线报告：触发率、误触发率、与目标差距

**问题：输出质量差 / AI 不遵守 skill 指令 / 篇幅不合适 / 兼容性差**
- 扫描目标 Skill 目录，检查 `evals/evals.json`、`changelog/`、`benchmark.json`
- 执行 AI 视角通读（详见参考规范）
- 手动触发 skill，看 3-5 个典型输出的实际效果
- 记录当前输出存在的问题（是 skill 指令不清晰，还是 AI 执行时偏离了）

> **门禁**：用户看过基线报告。

---

### Phase 2：注入测试

> 根据目标和基线，补充/更新测试用例。

1. 生成 20 条 query（10条应触发 + 10条不应触发）
   - 应触发：覆盖用户提到的失败案例 + 正常使用场景
   - 不应触发：选近义词陷阱，不选明显不相关的
   - query 必须真实具体
2. 用户审核通过后，写入 `<技能目录>/evals/evals.json`
3. 如目标涉及输出质量，补充 `expectations`（正面+反面双向门禁）

> **门禁**：用户审核通过 20 条 query。

---

### Phase 3：迭代锻造

> 改 → 跑 Eval → 看分数 → 再改。用数据说话。

1. **确定修改方向**：

   | 问题类型 | 优先修改位置 |
   |---------|------------|
   | 触发率低 | description |
   | 误触发高 | description |
   | 输出质量差 | SKILL.md 正文 |
   | 格式不对 | 模板 / references |

2. **修改并记录到 changelog**
3. **跑 Eval**：
   ```bash
   python3 ../技能创建/scripts/run_eval.py \
     --eval-set <技能目录>/evals/evals.json \
     --skill-path <技能目录> \
     --runs-per-query 3 \
     --verbose
   ```
4. **自动优化 description**（可选，瓶颈时启用）：
   ```bash
   python3 ../技能创建/scripts/improve_description.py \
     --eval-results <最新eval输出.json> \
     --skill-path <技能目录> \
     --model <当前使用的模型>
   ```
5. **判断结果**：
   - 达标 → Phase 4
   - 有进步未达标 → 继续
   - 连续 2 轮无进展 → 熔断

**盲比（高阶）**：连续 2 轮无实质进展时，隐藏版本标签让独立分析师打分。

> **门禁**：达标进入 Phase 4，或用户主动中止，或熔断触发。

---

### Phase 4：门禁上线

> 分数达标后，正式更新 SKILL.md 并注册。

1. **量化门禁检查**：

   | 门禁项 | 合格线 |
   |--------|-------|
   | 触发率 | ≥ 80% |
   | 误触发率 | ≤ 20% |
   | 输出质量（如适用） | ≥ 7/10 |
   | 用户确认验收 | 是 |

   全部通过才能上线。

2. **更新 SKILL.md**（description / 正文 / 版本号）
3. **记录锻造档案**到 `<技能目录>/changelog/`
4. **同步环境**：
   - **macOS**：`chmod +x skills-init.command && ./skills-init.command`
   - **Windows**：`.\skills-init.ps1`

> **最终门禁**：4 项门禁通过 + 文件已更新 + 环境已同步。

---

## 参考规范

> 以下内容按需查阅，不打断执行流程。

### 熔断规则

| 条件 | 动作 |
|------|------|
| 连续 2 轮迭代无分数提升 | 切换策略：换模型 / 换方案 / 启用盲比 |
| 连续 3 轮迭代无实质进展 | 强制停机，输出报告提交用户决策 |
| 用户主动中止 | 保存进度到 changelog，标记"未完成" |

### AI 视角通读检查清单

Phase 1 诊断时执行：假装自己是第一次读到目标 SKILL.md 的 AI，逐段记录以下问题：

| 检查项 | 说明 |
|--------|------|
| 卡点 | 读到哪一步不知道该干什么？ |
| 歧义 | 哪段话可以有多种理解？ |
| 路径错误 | 引用的文件路径是否存在？ |
| 缺失信息 | 执行某步需要的信息在前面是否已提供？ |
| 重复逻辑 | 同一件事是否在多处出现？ |
| 顺序颠倒 | 步骤是否需要在更前面执行？ |

输出问题清单，作为后续迭代修改的依据。
