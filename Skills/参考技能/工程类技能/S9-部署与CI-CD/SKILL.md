---
name: 部署与CI-CD
description: 构建与部署流水线指导——CI 设计原则、构建脚本规范、部署策略速查。当需要配置构建流程、设计 CI 流水线、或部署服务到服务器时使用。Use when user wants to set up CI/CD, write build scripts, configure deployment, or says "配一下CI" / "部署" / "构建脚本".
metadata:
  pattern: tool-wrapper
---

# 部署与 CI/CD

<what-to-do>

## CI 设计原则

1. **快速反馈** — 提交后 5 分钟内给出结果
2. **并行执行** — lint、test、build 互不阻塞
3. **可重现** — 同样的代码 + 同样的配置 = 同样的结果
4. **失败快速** — 先跑最快的检查，失败即终止

## 标准流水线阶段

```
提交代码 → Lint → 单元测试 → 构建 → 集成测试 → 部署
```

## 构建脚本规范

- 构建命令写在 `package.json` 或 `Makefile` 中
- 本地和 CI 用同一套脚本
- 版本号通过 Git Tag 或 CI 变量注入

## 部署策略

| 策略 | 适用场景 | 风险 |
|-----|---------|------|
| 直接部署 | 个人项目/原型 | 有停机时间 |
| 蓝绿部署 | 生产环境 | 需要双倍资源 |
| 滚动更新 | 集群部署 | 回滚慢 |

</what-to-do>
