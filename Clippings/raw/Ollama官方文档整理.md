# Ollama 官方文档整理

> 来源：Ollama 官方文档 https://docs.ollama.com
> 下载日期：2026-06-21

---

## 一、Modelfile 参考

### 格式

```
# 注释
INSTRUCTION 参数
```

| 指令 | 描述 |
|------|------|
| **FROM（必需）** | 定义基础模型 |
| **PARAMETER** | 设置运行参数 |
| **TEMPLATE** | 完整提示模板 |
| **SYSTEM** | 系统消息 |
| **ADAPTER** | LoRA 适配器 |
| **LICENSE** | 许可证 |
| **MESSAGE** | 消息历史 |
| **REQUIRES** | 最低 Ollama 版本 |

### 示例

```
FROM llama3.2
PARAMETER temperature 1
PARAMETER num_ctx 4096
SYSTEM You are Mario from super mario bros, acting as an assistant.
```

使用：
```bash
ollama create choose-a-model-name -f ./Modelfile
ollama run choose-a-model-name
```

查看已有模型的 Modelfile：
```bash
ollama show --modelfile llama3.2
```

### FROM（必需）

**从已有模型构建：**
```
FROM llama3.2
```

**从 Safetensors 模型构建：**
```
FROM <model directory>
```
支持架构：Llama, Mistral, Gemma, Phi3

**从 GGUF 文件构建：**
```
FROM ./ollama-model.gguf
```
路径可以是绝对路径或相对于 Modelfile 的路径。

### PARAMETER

| 参数 | 描述 | 类型 | 默认值 |
|------|------|------|--------|
| `num_ctx` | 上下文窗口大小 | int | 2048 |
| `repeat_last_n` | 防止重复的回看距离 | int | 64 |
| `repeat_penalty` | 重复惩罚强度 | float | 1.1 |
| `temperature` | 温度（创造性） | float | 0.8 |
| `seed` | 随机种子 | int | 0 |
| `stop` | 停止序列 | string | — |
| `num_predict` | 最大预测 token 数 | int | -1 |
| `top_k` | 保留最高概率 token 数 | int | 40 |
| `top_p` | 核采样概率阈值 | float | 0.9 |
| `min_p` | 最小概率阈值 | float | 0.0 |

### TEMPLATE

使用 Go 模板语法：

| 变量 | 描述 |
|------|------|
| `{{ .System }}` | 系统消息 |
| `{{ .Prompt }}` | 用户提示消息 |
| `{{ .Response }}` | 模型响应 |

**ChatML 格式示例（Qwen 模型用）：**
```
TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
"""
```

### SYSTEM

```
SYSTEM """<system message>"""
```

### MESSAGE

```
MESSAGE <role> <message>
```
角色：`system`、`user`、`assistant`

---

## 二、Anthropic 兼容 API（Claudian 连接用）

### 环境变量

```bash
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_BASE_URL=http://localhost:11434
```

**注意：** URL 不带 `/v1`，API Key 用 `ANTHROPIC_AUTH_TOKEN`。

### Python 示例

```python
import anthropic
client = anthropic.Anthropic(
    base_url='http://localhost:11434',
    api_key='ollama',  # required but ignored
)
message = client.messages.create(
    model='qwen3-coder',
    max_tokens=1024,
    messages=[{'role': 'user', 'content': 'Hello, how are you?'}]
)
```

### 与 Claude Code 配合

```bash
# 快速启动
ollama launch claude

# 手动配置
ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_BASE_URL=http://localhost:11434 claude --model qwen3-coder
```

### 支持的功能

- ✅ Messages / Streaming / System prompts
- ✅ Multi-turn conversations
- ✅ Vision (images) - 仅支持 base64
- ✅ Tools (function calling)
- ✅ Thinking/extended thinking
- ❌ 不支持：tool_choice、metadata、prompt caching、PDF

---

## 三、Claude Code 集成

### 安装 Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### 与 Ollama 配合使用

```bash
# 快速启动
ollama launch claude

# 指定模型
ollama launch claude --model qwen3.5
```

### 推荐模型

| 模型 | 说明 |
|------|------|
| `kimi-k2.5:cloud` | 推荐（云端） |
| `glm-5:cloud` | 推荐（云端） |
| `qwen3.5` | 可用（本地） |
| `qwen3-coder` | 编码专用（30B，需24GB VRAM） |

### 手动配置环境变量

```bash
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
export ANTHROPIC_BASE_URL=http://localhost:11434

claude --model qwen3.5
```

**注意：** 官方推荐至少 64k tokens 上下文窗口。

---

## 四、CLI 命令参考

| 命令 | 说明 |
|------|------|
| `ollama run <model>` | 运行模型（交互模式） |
| `ollama run <model> "prompt"` | 一次性问答 |
| `ollama launch claude` | 启动 Claude Code 集成 |
| `ollama pull <model>` | 下载模型 |
| `ollama rm <model>` | 删除模型 |
| `ollama ls` | 列出已下载模型 |
| `ollama ps` | 列出运行中的模型 |
| `ollama stop <model>` | 停止模型 |
| `ollama serve` | 启动服务 |
| `ollama create -f Modelfile` | 创建自定义模型 |
| `ollama show --modelfile <model>` | 查看模型 Modelfile |
| `ollama cp <src> <dst>` | 复制/重命名模型 |

---

## 五、FAQ 要点

### 上下文窗口
- 默认 4096 tokens
- 通过 `OLLAMA_CONTEXT_LENGTH` 环境变量或 `num_ctx` 参数设置

### Flash Attention
设置环境变量 `OLLAMA_FLASH_ATTENTION=1`

### K/V 缓存量化
通过 `OLLAMA_KV_CACHE_TYPE` 设置：`f16`、`q8_0`、`q4_0`

### 模型存储位置
macOS: `~/.ollama/models`

### 修改存储位置
设置 `OLLAMA_MODELS` 环境变量

### 禁用云功能
`OLLAMA_NO_CLOUD=1`
