# Antigravity Tools 支持的模型

> 来源：反重力工具（Antigravity Tools.exe v1.2.2）本地 API 代理
> 地址：`http://127.0.0.1:8002/v1`
> 底层上游：`https://copilot.tencent.com/v2`（腾讯云 Copilot）

## DeepSeek 系列

| 模型名 | 说明 |
|--------|------|
| `deepseek-v4-pro` | DeepSeek V4 Pro（最强） |
| `deepseek-v4-flash` | DeepSeek V4 Flash（快速版） |
| `deepseek-v3-2-volc` | DeepSeek V3 火山引擎版 |
| `deepseek-v3-1` | DeepSeek V3-1 |
| `deepseek-v3-0324` | DeepSeek V3 0324 版 |
| `deepseek-r1` | DeepSeek R1（推理模型） |

## GLM 系列（智谱）

| 模型名 | 说明 |
|--------|------|
| `glm-5.2` | 智谱 GLM-5.2 |
| `glm-5.1` | 智谱 GLM-5.1 |
| `glm-5.0` | 智谱 GLM-5.0 |
| `glm-5.0-turbo` | 智谱 GLM-5.0 Turbo |
| `glm-5v-turbo` | 智谱 GLM-5V（视觉版）Turbo |
| `glm-4.7` | 智谱 GLM-4.7 |
| `glm-4.6` | 智谱 GLM-4.6 |

## Kimi 系列

| 模型名 | 说明 |
|--------|------|
| `kimi-k2.6` | Kimi K2.6 |

## MiniMax 系列

| 模型名 | 说明 |
|--------|------|
| `minimax-m2.5` | MiniMax M2.5 |
| `minimax-m2.7` | MiniMax M2.7 |
| `minimax-m3` | MiniMax M3 |

---

**总计：15 个模型，4 个厂商**

## 代理策略

- Key 管理：上游 Key 池（顺序耗尽策略，一个 Key 用完再切下一个）
- 鉴权：子 API Key 管理与鉴权
- 接口：OpenAI 兼容（`/v1/chat/completions`、`/v1/models` 等）
- 限流：支持限流与自动切换耗尽 Key

---

## 使用方法

任何支持 OpenAI API 格式的软件/客户端均可使用。

### 通用配置

| 字段 | 值 |
|------|-----|
| **API 地址** | `http://127.0.0.1:8002/v1` |
| **API Key** | 在 Antigravity Tools 界面中创建的子 API Key |
| **模型** | 从上方列表中选择，如 `deepseek-v4-flash` |

### 推荐客户端

#### 1. ChatBox（桌面端，最简单）
- 下载：https://chatboxai.app
- 设置 → 选择 **OpenAI API** 或 **自定义提供商**
- API 地址填 `http://127.0.0.1:8002/v1`
- API Key 填子 Key
- 模型名填 `deepseek-v4-flash`

#### 2. NextChat（ChatGPT-Next-Web）
- 部署后设置 → 自定义接口
- 接口地址：`http://127.0.0.1:8002`
- API Key：子 Key
- 模型：`deepseek-v4-flash`

#### 3. Open WebUI
- 管理员面板 → 设置 → 外部连接
- OpenAI API 地址：`http://127.0.0.1:8002/v1`
- 密钥：子 Key

#### 4. CodeBuddy / WorkBuddy（IDE 内使用）
- 在 Antigravity Tools 的 API 代理页面点击「一键配置 CodeBuddy 的 models.json」或「一键配置 WorkBuddy 的 models.json」
- 会自动写入 `%USERPROFILE%\.codebuddy\models.json` 或 `%USERPROFILE%\.workbuddy\models.json`

#### 5. 编程调用（Python）

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8002/v1",
    api_key="你的子Key"
)

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

#### 6. 直接 curl 测试

```bash
curl http://127.0.0.1:8002/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 你的子Key" \
  -d '{"model": "deepseek-v4-flash", "messages": [{"role": "user", "content": "你好"}]}'
```
