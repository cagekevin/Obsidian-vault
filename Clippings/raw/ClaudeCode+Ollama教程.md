# 教程：Claude Code + Ollama 本地模型免费跑

> 来源：微信公众号"GitHubStore"
> 作者：小G
> 链接：https://mp.weixin.qq.com/s/xhtVwnBJIpIGsMTCajDlcA

## 核心工具

- **Ollama** — 本地模型运行器
- **Claude Code** — AI 编程代理
- **推荐模型**：`qwen3-coder:7b`（低配） / `qwen3-coder:30b`（高配）

## 5 分钟上手

### 1. 安装 Ollama

访问 ollama.com 下载安装，验证：`ollama --version`

### 2. 拉取模型

```bash
ollama pull qwen3-coder:7b
```

### 3. 安装 Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | sh
```

### 4. 连接本地 Ollama

**方式一（推荐）：自动配置**
```bash
ollama launch claude --model qwen3-coder:7b
```

**方式二：手动设置环境变量**
```bash
export ANTHROPIC_BASE_URL="http://localhost:11434"
export ANTHROPIC_AUTH_TOKEN="ollama"
claude --model qwen3-coder:7b
```

## 模型推荐

| 配置 | 推荐模型 |
|------|----------|

<!-- processed: 2026-06-23 → Wiki/sources/Claude Code + Ollama Tutorial.md + Wiki/concepts/Ollama.md + Wiki/concepts/Claude Code Local Setup.md -->
