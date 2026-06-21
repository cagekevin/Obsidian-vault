# Ollama 官方文档完整整理

> 来源：https://docs.ollama.com
> 下载日期：2026-06-21
> 工具：browser_control.py 脱水清洗

---

## 目录

1. [Modelfile 参考](#1-modelfile-参考)
2. [CLI 命令参考](#2-cli-命令参考)
3. [Anthropic 兼容 API（Claudian 连接用）](#3-anthropic-兼容-apiclaudian-连接用)
4. [OpenAI 兼容 API](#4-openai-兼容-api)
5. [Claude Code 集成](#5-claude-code-集成)
6. [FAQ](#6-faq)

---

## 1. Modelfile 参考

### 1.1 格式

```
# 注释
INSTRUCTION 参数
```

| 指令 | 描述 | 必需 |
|------|------|------|
| **FROM** | 定义基础模型 | **是** |
| **PARAMETER** | 设置运行参数 | 否 |
| **TEMPLATE** | 完整提示模板 | 否 |
| **SYSTEM** | 系统消息 | 否 |
| **ADAPTER** | (Q)LoRA 适配器 | 否 |
| **LICENSE** | 许可证 | 否 |
| **MESSAGE** | 消息历史 | 否 |
| **REQUIRES** | 最低 Ollama 版本 | 否 |

### 1.2 基本示例

```dockerfile
FROM llama3.2
# 设置温度
PARAMETER temperature 1
# 设置上下文窗口大小
PARAMETER num_ctx 4096
# 设置系统消息
SYSTEM You are Mario from super mario bros, acting as an assistant.
```

**使用：**
```bash
# 创建模型
ollama create choose-a-model-name -f ./Modelfile

# 运行模型
ollama run choose-a-model-name
```

**查看已有模型的 Modelfile：**
```bash
ollama show --modelfile llama3.2
```

输出示例：
```
FROM /Users/pdevine/.ollama/models/blobs/sha256-xxx
TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

{{ .Response }}<|eot_id|>"""
PARAMETER stop "<|start_header_id|>"
PARAMETER stop "<|end_header_id|>"
PARAMETER stop "<|eot_id|>"
PARAMETER stop "<|reserved_special_token"
```

### 1.3 FROM（必需）

**从已有模型构建：**
```dockerfile
FROM llama3.2
```

**从 Safetensors 模型构建：**
```dockerfile
FROM <model directory>
```
支持架构：Llama (2, 3, 3.1, 3.2), Mistral (1, 2, Mixtral), Gemma (1, 2), Phi3

**从 GGUF 文件构建：**
```dockerfile
FROM ./ollama-model.gguf
```
路径可以是绝对路径或相对于 Modelfile 的路径。

### 1.4 PARAMETER

| 参数 | 描述 | 类型 | 默认值 | 示例 |
|------|------|------|--------|------|
| `num_ctx` | 上下文窗口大小 | int | 2048 | `num_ctx 4096` |
| `repeat_last_n` | 防止重复的回看距离 | int | 64 | `repeat_last_n 64` |
| `repeat_penalty` | 重复惩罚强度 | float | 1.1 | `repeat_penalty 1.1` |
| `temperature` | 温度，越高越有创意 | float | 0.8 | `temperature 0.7` |
| `seed` | 随机种子 | int | 0 | `seed 42` |
| `stop` | 停止序列 | string | — | `stop "AI assistant:"` |
| `num_predict` | 最大预测 token 数 | int | -1（无限） | `num_predict 42` |
| `top_k` | 保留最高概率 token 数 | int | 40 | `top_k 40` |
| `top_p` | 核采样概率阈值 | float | 0.9 | `top_p 0.9` |
| `min_p` | 最小概率阈值 | float | 0.0 | `min_p 0.05` |

### 1.5 TEMPLATE

使用 Go 模板语法。

**模板变量：**

| 变量 | 描述 |
|------|------|
| `{{ .System }}` | 系统消息 |
| `{{ .Prompt }}` | 用户提示消息 |
| `{{ .Response }}` | 模型响应（此变量后的内容被忽略） |

**ChatML 格式（Qwen 模型用）：**
```
TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
"""
```

### 1.6 SYSTEM

```
SYSTEM """<system message>"""
```

### 1.7 ADAPTER

**Safetensor 适配器：**
```
ADAPTER <path to safetensor adapter>
```
支持：Llama, Mistral, Gemma

**GGUF 适配器：**
```
ADAPTER ./ollama-lora.gguf
```

### 1.8 LICENSE

```
LICENSE """<license text>"""
```

### 1.9 MESSAGE

```
MESSAGE <role> <message>
```

有效角色：`system`、`user`、`assistant`

示例：
```
MESSAGE user Is Toronto in Canada?
MESSAGE assistant yes
MESSAGE user Is Sacramento in Canada?
MESSAGE assistant no
```

### 1.10 REQUIRES

```
REQUIRES 0.14.0
```

### 1.11 注意事项

- Modelfile **不区分大小写**
- 指令顺序可以任意
- 官方推荐 `FROM` 放在首位

---

## 2. CLI 命令参考

### 2.1 运行模型

```bash
ollama run gemma4              # 交互模式
ollama run gemma4 "你好"        # 一次性问答
```

### 2.2 多行输入

```bash
>>> """Hello,
... world!
... """
```

### 2.3 多模态模型（看图）

```bash
ollama run gemma4 "What's in this image? /path/to/image.png"
```

### 2.4 生成嵌入向量

```bash
ollama run nomic-embed-text "Hello world"
echo "Hello world" | ollama run nomic-embed-text
```

### 2.5 启动集成应用

```bash
ollama launch                    # 交互式启动
ollama launch claude             # 启动 Claude Code
ollama launch claude --model qwen3.5  # 指定模型
ollama launch droid --config     # 仅配置不启动
```

支持集成：OpenCode, Claude Code, Codex, VS Code, Droid

### 2.6 模型管理

```bash
ollama pull gemma4               # 下载模型
ollama rm gemma4                 # 删除模型
ollama ls                        # 列出已下载模型
ollama ps                        # 列出运行中模型
ollama stop gemma4               # 停止模型
ollama cp llama3.2 my-model      # 复制/重命名模型
```

### 2.7 创建自定义模型

```bash
# 先创建 Modelfile
FROM gemma4
SYSTEM """You are a happy cat."""

# 然后创建
ollama create -f Modelfile
```

### 2.8 服务管理

```bash
ollama serve                     # 启动服务
ollama serve --help              # 查看环境变量
```

### 2.9 登录/登出

```bash
ollama signin                    # 登录
ollama signout                   # 登出
```

---

## 3. Anthropic 兼容 API（Claudian 连接用）

### 3.1 环境变量

```bash
export ANTHROPIC_AUTH_TOKEN=ollama    # 必需但被忽略
export ANTHROPIC_BASE_URL=http://localhost:11434
```

**关键点：**
- URL **不要加 `/v1`**
- 用 `ANTHROPIC_AUTH_TOKEN` 而不是 `ANTHROPIC_API_KEY`

### 3.2 Python 示例

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
print(message.content[0].text)
```

### 3.3 流式示例

```python
import anthropic

client = anthropic.Anthropic(
    base_url='http://localhost:11434',
    api_key='ollama',
)

with client.messages.stream(
    model='qwen3-coder',
    max_tokens=1024,
    messages=[{'role': 'user', 'content': 'Count from 1 to 10'}]
) as stream:
    for text in stream.text_stream:
        print(text, end='', flush=True)
```

### 3.4 工具调用示例

```python
import anthropic

client = anthropic.Anthropic(
    base_url='http://localhost:11434',
    api_key='ollama',
)

message = client.messages.create(
    model='qwen3-coder',
    max_tokens=1024,
    tools=[{
        'name': 'get_weather',
        'description': 'Get the current weather in a location',
        'input_schema': {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string',
                    'description': 'The city and state, e.g. San Francisco, CA'
                }
            },
            'required': ['location']
        }
    }],
    messages=[{'role': 'user', 'content': "What's the weather in San Francisco?"}]
)

for block in message.content:
    if block.type == 'tool_use':
        print(f'Tool: {block.name}')
        print(f'Input: {block.input}')
```

### 3.5 与 Claude Code 配合

```bash
# 快速启动
ollama launch claude

# 手动配置
ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_BASE_URL=http://localhost:11434 claude --model qwen3-coder

# 或在 shell profile 中设置
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_BASE_URL=http://localhost:11434
claude --model qwen3-coder
```

### 3.6 推荐模型

| 模型 | 说明 |
|------|------|
| `qwen3-coder` | 编码专用（30B，需 ≥24GB VRAM） |
| `gpt-oss:20b` | 通用模型 |
| `glm-4.7:cloud` | 云端模型（无需下载） |
| `minimax-m2.1:cloud` | 快速云端模型 |

### 3.7 支持的功能

**✅ 支持：**
- Messages / Streaming / System prompts
- Multi-turn conversations
- Vision (images) - **仅支持 base64，不支持 URL**
- Tools (function calling) / Tool results
- Thinking/extended thinking（`budget_tokens` 接受但不强制执行）

**❌ 不支持：**
- `/v1/messages/count_tokens`（Token 计数）
- `tool_choice`（强制指定工具）
- `metadata`（请求元数据）
- Prompt caching（`cache_control`）
- Batches API（异步批处理）
- Citations（引用）
- PDF 支持
- 服务端错误事件

### 3.8 支持的消息端点

`/v1/messages`

**支持字段：**
- `model`, `max_tokens`, `messages`
- `content`: text, image(base64), tool_use, tool_result, thinking
- `system` (string or array)
- `stream`, `temperature`, `top_p`, `top_k`
- `stop_sequences`, `tools`, `thinking`

### 3.9 默认模型名

```bash
# 将模型复制为 Anthropic 默认名称
ollama cp qwen3-coder claude-3-5-sonnet

# 然后可以用新名称调用
curl http://localhost:11434/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## 4. OpenAI 兼容 API

### 4.1 基本配置

```
Base URL: http://localhost:11434/v1/
API Key: 'ollama'（必需但忽略）
```

### 4.2 Python 示例

**Chat Completions：**
```python
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)

chat_completion = client.chat.completions.create(
    messages=[{'role': 'user', 'content': 'Say this is a test'}],
    model='gpt-oss:20b',
)
print(chat_completion.choices[0].message.content)
```

**Responses API（v0.13.3+）：**
```python
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',
)

responses_result = client.responses.create(
    model='qwen3:8b',
    input='Write a short poem about the color blue',
)
print(responses_result.output_text)
```

**Vision（看图）：**
```python
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',
)

response = client.chat.completions.create(
    model='qwen3-vl:8b',
    messages=[{
        'role': 'user',
        'content': [
            {'type': 'text', 'text': "What's in this image?"},
            {'type': 'image_url', 'image_url': 'data:image/png;base64,...'}
        ]
    }],
    max_tokens=300,
)
print(response.choices[0].message.content)
```

### 4.3 支持端点

| 端点 | 状态 |
|------|------|
| `/v1/chat/completions` | ✅ 完整支持 |
| `/v1/completions` | ✅ 支持 |
| `/v1/models` | ✅ 支持 |
| `/v1/models/{model}` | ✅ 支持 |
| `/v1/embeddings` | ✅ 支持 |
| `/v1/images/generations` | ⚠️ 实验性 |
| `/v1/responses` | ✅ v0.13.3+ |

### 4.4 `/v1/chat/completions` 支持的功能

**✅ 支持：**
- Chat completions / Streaming / JSON mode
- Reproducible outputs / Vision / Tools (function calling)
- Reasoning/thinking control
- `model`, `messages`, `content`（文本/图像）
- `frequency_penalty`, `presence_penalty`
- `response_format`, `seed`, `stop`
- `stream`, `stream_options`, `include_usage`
- `temperature`, `top_p`, `max_tokens`
- `tools`
- `reasoning_effort` / `effort` (`"high"`, `"medium"`, `"low"`, `"none"`)

**❌ 不支持：**
- `tool_choice`, `logit_bias`, `user`, `n`
- 图像 URL（仅支持 base64）

### 4.5 默认模型名

```bash
ollama cp llama3.2 gpt-3.5-turbo

curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### 4.6 设置上下文大小

创建 Modelfile：
```dockerfile
FROM llama3.2
PARAMETER num_ctx 8192
```

创建并使用：
```bash
ollama create mymodel

curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mymodel",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## 5. Claude Code 集成

### 5.1 安装 Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### 5.2 与 Ollama 配合使用

```bash
# 快速启动（交互式选模型）
ollama launch claude

# 直接指定模型
ollama launch claude --model kimi-k2.5:cloud

# 非交互模式（用于 Docker/CI/CD）
ollama launch claude --model kimi-k2.5:cloud --yes -- -p "how does this repository work?"
```

### 5.3 推荐模型

| 模型 | 说明 |
|------|------|
| `kimi-k2.5:cloud` | ⭐ 推荐（云端） |
| `glm-5:cloud` | ⭐ 推荐（云端） |
| `minimax-m2.7:cloud` | 可用（云端） |
| `qwen3.5:cloud` | 可用（云端） |
| `glm-4.7-flash` | 可用（云端） |
| `qwen3.5` | 可用（本地） |

### 5.4 手动配置

```bash
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
export ANTHROPIC_BASE_URL=http://localhost:11434

claude --model qwen3.5
```

或内联：
```bash
ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_API_KEY="" claude --model glm-5:cloud
```

**注意：** 建议至少 64k tokens 上下文窗口。

### 5.5 定时任务（/loop）

```bash
/loop 30m Check my open PRs and summarize their status
/loop 1h Research the latest AI news and summarize key developments
/loop 15m Check for new GitHub issues and triage by priority
/loop 1h Remind me to review the deploy status
```

### 5.6 Telegram 集成

```bash
ollama launch claude -- --channels plugin:telegram@claude-plugins-official
```

---

## 6. FAQ

### 6.1 升级 Ollama

- macOS/Windows：自动更新，点击 "Restart to update"
- Linux：重新运行 `curl -fsSL https://ollama.com/install.sh | sh`

### 6.2 设置上下文窗口大小

```bash
# 环境变量
OLLAMA_CONTEXT_LENGTH=8192 ollama serve

# ollama run 中使用
/set parameter num_ctx 4096

# API 中使用
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?",
  "options": { "num_ctx": 4096 }
}'
```

默认 4096 tokens。

### 6.3 检查模型是否在 GPU 上运行

```bash
ollama ps
```

Processor 列显示：
- `100% GPU` → 完全在 GPU
- `100% CPU` → 完全在 CPU
- `48%/52% CPU/GPU` → 混合

### 6.4 配置环境变量（macOS）

```bash
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
# 重启 Ollama 应用
```

### 6.5 使用代理

```bash
# 只设置 HTTPS_PROXY，不要设 HTTP_PROXY
export HTTPS_PROXY=https://proxy.example.com
```

### 6.6 禁用云功能

```json
// ~/.ollama/server.json
{ "disable_ollama_cloud": true }
```

或环境变量：`OLLAMA_NO_CLOUD=1`

### 6.7 暴露到网络

```bash
OLLAMA_HOST="0.0.0.0:11434" ollama serve
```

### 6.8 模型存储位置

| 系统 | 路径 |
|------|------|
| macOS | `~/.ollama/models` |
| Linux | `/usr/share/ollama/.ollama/models` |
| Windows | `C:\Users\%username%\.ollama\models` |

修改：设置 `OLLAMA_MODELS` 环境变量

### 6.9 预加载模型

```bash
# API
curl http://localhost:11434/api/generate -d '{"model": "mistral"}'

# CLI
ollama run llama3.2 ""
```

### 6.10 保持模型在内存中

```bash
# 保持加载（keep_alive=-1）
curl http://localhost:11434/api/generate -d '{"model": "llama3.2", "keep_alive": -1}'

# 立即卸载
curl http://localhost:11434/api/generate -d '{"model": "llama3.2", "keep_alive": 0}'

# 或使用 CLI
ollama stop llama3.2
```

默认 5 分钟后卸载。可通过 `OLLAMA_KEEP_ALIVE` 环境变量修改。

### 6.11 启用 Flash Attention

```bash
OLLAMA_FLASH_ATTENTION=1 ollama serve
```

### 6.12 K/V 缓存量化

```bash
OLLAMA_KV_CACHE_TYPE=q8_0 ollama serve
```

可用类型：`f16`（默认）、`q8_0`（推荐，省一半内存）、`q4_0`

### 6.13 并发请求管理

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `OLLAMA_MAX_LOADED_MODELS` | 3 × GPU 数 | 最大并发加载模型数 |
| `OLLAMA_NUM_PARALLEL` | 1 | 每个模型的并行请求数 |
| `OLLAMA_MAX_QUEUE` | 512 | 最大排队请求数 |

### 6.14 Ollama 公钥位置

| 系统 | 路径 |
|------|------|
| macOS | `~/.ollama/id_ed25519.pub` |
| Linux | `/usr/share/ollama/.ollama/id_ed25519.pub` |
| Windows | `C:\Users\<username>\.ollama\id_ed25519.pub` |

### 6.15 禁止开机自启

- **Windows**：任务管理器 → 启动应用 → 禁用 ollama
- **macOS**：设置 → 登录项 → 找到 Ollama → 禁用

---

## 7. Thinking（思考模式）— 官方原文

> 来源：https://docs.ollama.com/capabilities/thinking
> 以下为页面原文脱水内容：

Thinking-capable models emit a thinking field that separates their reasoning trace from the final answer. Use this capability to audit model steps, animate the model thinking in a UI, or hide the trace entirely when you only need the final response.

### Supported models

- Qwen 3
- GPT-OSS (use think levels: low, medium, high — the trace cannot be fully disabled)
- DeepSeek-v3.1
- DeepSeek R1

### Enable thinking in API calls

Set the think field on chat or generate requests. Most models accept booleans (true/false). GPT-OSS instead expects one of low, medium, or high to tune the trace length. The message.thinking (chat endpoint) or thinking (generate endpoint) field contains the reasoning trace while message.content/response holds the final answer.

**cURL 示例：**
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3",
  "messages": [{
    "role": "user",
    "content": "How many letter r are in strawberry?"
  }],
  "think": true,
  "stream": false
}'
```

**Python 示例：**
```python
from ollama import chat

response = chat(
  model='qwen3',
  messages=[{'role': 'user', 'content': 'How many letter r are in strawberry?'}],
  think=True,
  stream=False,
)

print('Thinking:\n', response.message.thinking)
print('Answer:\n', response.message.content)
```

**JavaScript 示例：**
```javascript
import ollama from 'ollama'

const response = await ollama.chat({
  model: 'deepseek-r1',
  messages: [{ role: 'user', content: 'How many letter r are in strawberry?' }],
  think: true,
  stream: false,
})

console.log('Thinking:\n', response.message.thinking)
console.log('Answer:\n', response.message.content)
```

GPT-OSS requires think to be set to "low", "medium", or "high". Passing true/false is ignored for that model.

### CLI quick reference

| 命令 | 说明 |
|------|------|
| `ollama run deepseek-r1 --think "Where should I visit in Lisbon?"` | Enable thinking for a single run |
| `ollama run deepseek-r1 --think=false "Summarize this article"` | Disable thinking |
| `ollama run deepseek-r1 --hidethinking "Is 9.9 bigger or 9.11?"` | Hide the trace while still using a thinking model |
| `/set think` | Inside interactive sessions, toggle with /set think |
| `/set nothink` | Inside interactive sessions, toggle with /set nothink |
| `ollama run gpt-oss --think=low "Draft a headline"` | GPT-OSS only accepts levels (low/medium/high) |

**Thinking is enabled by default in the CLI and API for supported models.**
