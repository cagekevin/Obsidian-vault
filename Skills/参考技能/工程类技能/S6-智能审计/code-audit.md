---
name: 代码审计
description: Deep code review covering security, robustness, performance, and clean code standards. Use when user wants to review code for enterprise-grade quality.
---

# 代码质量审计 (Code Audit)

<what-to-do>
作为资深技术专家，按照企业级 Code Review 标准对代码进行深度扫描：

1. **安全性审查 (Security)**：
   - 扫描常见的注入漏洞（SQLi, XSS, CSRF 等）。
   - 检查密码、API Key、Token 等敏感信息是否被硬编码。
   - 权限越权隐患及输入消毒（Sanitization）验证。
2. **健壮性与异常兜底 (Robustness)**：
   - try-catch 或错误捕获是否覆盖全面？
   - 空指针、数组越界、并发竞争等边界条件是否被妥善处理？
   - 是否有"吞咽异常"（Silent Failures）的行为？
3. **性能与复杂度分析 (Performance)**：
   - 识别高时间复杂度的代码（如死循环、多层嵌套遍历、N+1 数据库查询）。
   - 数据结构选择是否最优？是否可以利用哈希表、缓存机制优化性能？
4. **可维护性与整洁度 (Clean Code)**：
   - 变量与函数命名是否"见名知意"？
   - 函数是否符合单一职责原则（SRP）？是否存在"上帝类（God Class）"？

**执行输出**：
- 按照严重等级分块：🚨 致命漏洞、🔴 逻辑错误、🟡 性能警告、💡 最佳实践建议。
- 每一个指出的问题，**必须**附带具体的行号（或代码段），并直接提供【重构对比代码】。
</what-to-do>

<supporting-info>
- 审计时，自动加载目标语言的最佳实践标准（如 Python PEP8, Java 阿里巴巴规范, ESLint 标准）。
- 不要给出模糊的建议（如"优化这段代码"），必须给出具体的代码实现。
</supporting-info>
