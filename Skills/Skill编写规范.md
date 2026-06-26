# Skill 编写规范

AI 对机器可读格式（如 Markdown 树状结构、XML 标签、小数点层级）的理解力远超纯文本缩进。

## 核心原则

1. **一层用一种编号，不混用。** Module 用 `[Module X]`，Phase 用 `Phase N`，子步骤用 `N.x`，细项用 `-`。
2. **区分"执行流"与"数据流"。** 执行流走 Phase，数据/规则走 XML 标签。
3. **流程越复杂，越要严格遵循规范。** 简单 Skill 可以省略部分标签，但一旦流程多起来（Phase >3 或子步骤 >10），必须完整使用。

## 编号层级

| 层级 | 语义定义 | 编号/符号 | 说明 |
| --- | --- | --- | --- |
| **模块 (Module)** | 逻辑隔离区 | `## [Module X]` | `[]` 强提示符 + `##`，建立绝对作用域 |
| **规则/数据 (XML)** | 静态参数与全局设定 | `<XML标签>` | 包裹后 AI 视作高权重系统环境 |
| **执行阶段 (Phase)** | 按顺序执行的宏观动作 | `Phase N.` | `Phase` 强关联序列化执行 |
| **子步骤 (Sub-step)** | 具体操作动作 | `N.x` | 十进制绑定，消除跨层级错误 |
| **细项 (Item)** | 并列信息、枚举 | `-` 或 `*` | 不干预执行流 |

## XML 标签清单

按需选用，流程越复杂建议用得越全：

| 标签 | 用途 | 适合场景 |
|------|------|----------|
| `<Skill_Meta>` | Skill 名称、版本、目标环境 | 所有 Skill |
| `<Global_Config>` | 核心原则、平台参数等背景知识 | 有全局约束的 Skill |
| `<Global_Rules>` | 执行铁律（交互限制、语义约束） | 流程型 Skill |
| `<Permission_Control>` | 权限校验规则（需审批的操作、错误处理策略） | 流程型 Skill |
| `<Environment>` | 操作系统路径映射 | 需要操作文件的 Skill |
| `<Interface_API>` | 外部工具/API 的调用规范（payload、返回值） | 依赖外部调用的 Skill |
| `<Asset_Catalog>` | 外部资产挂载点（字典、映射文件路径） | 依赖外部文件的 Skill |
| `<Session_State>` | 跨 Phase 缓存变量 | 多步骤有状态的 Skill |
| `<Error_Trace_Format>` | 错误报告模板 | 流程型 Skill（>3 个 Phase） |
| `<Output_Format>` | 输出数据结构约束 | 需要结构化输出的 Skill |

## 模板

### 完整版（复杂流程 Skill）

```markdown
<Skill_Meta>
- Name: [Skill 名称]
- Version: [版本号]
- Target: [执行环境/目标系统]
</Skill_Meta>

<Environment>
- OS_Mac_Root: /Users/.../AgentSpace/1_Active/
- OS_Win_Root: G:\AgentSpace\1_Active\
- Current_Workspace: $OS_[Type]_Root/...
</Environment>

<Permission_Control>
- Require_Approval: 方案多选、覆盖写入、文件删除
- Action_On_Error: 首错即停并分析，严禁循环试错
</Permission_Control>

<Global_Rules>
1. 交互限制：终端式输出，禁止任何主观解释与寒暄语。
2. 语义约束：[如视听生成场景] 强制使用摄影机位与物理材质语言，摒弃主观情绪词及传统电商摄影描述。
</Global_Rules>

<Interface_API>
- Tool_Name: [如 HTML_to_PSD_JSX_Router]
- Input_Payload: [要求的数据结构]
- Expected_Return: [预期的返回状态]
</Interface_API>

<Asset_Catalog>
- Rules_Dict: [逻辑判断字典文件路径]
- Style_Dict: [风格/骨架映射文件路径]
</Asset_Catalog>

<Session_State>
- Current_Node: Null
- Cache_Data: Null
</Session_State>

## [Module A] 主干执行流

Phase 1. 初始化与挂载
  1.1 解析 `<Environment>` 与 `<Asset_Catalog>`，校验依赖。
  1.2 冻结 `<Session_State>` 初始状态。

Phase 2. 核心流与外部调用
  2.1 准备 `<Interface_API>` 要求的 payload。
  2.2 发起调用，并在 `<Session_State>` 中更新返回值。

Phase 3. 拦截与输出封装
  3.1 触发 `<Permission_Control>` 校验。
  3.2 确认无误后，严格按照 `<Output_Format>` 输出包。

## [Module B] 资产与规则字典

<!-- 按需添加各类数据标签，如： -->

<Style_Library>
1. [风格名称] — [描述]
</Style_Library>

<Skeleton_Library>
1. [骨架名称] — [描述]
</Skeleton_Library>

<Rules_Summary>
- [规则速查]
</Rules_Summary>

<Error_Trace_Format>
# Fatal Error Report
- Root_Cause: [技术级根因]
- Deviated_Node: [故障发生的 Phase/Step]
- Context_Dump: [故障前的变量状态]
</Error_Trace_Format>

<Output_Format>
<!-- 强制锁定的输出数据结构格式 -->
</Output_Format>
```

### 轻量版（简单 Skill）

```markdown
<Skill_Meta>
- Name: 翻译助手
- Version: 1.0
</Skill_Meta>

<Global_Config>
1. 保留原文格式，只翻译内容
2. 专业术语优先使用行业标准译法
</Global_Config>

## [Module A] 执行流

Phase 1. 分析原文
  1.1 识别语言和领域
  1.2 标记专业术语

Phase 2. 翻译输出
  2.1 逐段翻译
  2.2 输出对照格式

## [Module B] 术语库

<Glossary>
- AI: 人工智能
- API: 应用程序接口
</Glossary>
```

## 完整示例参考

参见 `Skills/工作效率类/W5-图片设计/amazon-skincare/skill_副本.md`，该文件为按本规范编写的完整示例。
