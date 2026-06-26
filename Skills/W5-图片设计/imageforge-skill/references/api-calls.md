# 模型 API 调用指南

> Agent 执行层参考——当需要调用外部生图 API 时，按本文件操作。API Key 统一存 SECRET.md，一次提供长期使用。

---

## API Key 存储约定

所有生图 API Key 存入 `SECRET.md`，格式：

```markdown
## 生图模型 API Keys
- OPENAI_API_KEY: sk-xxx
- VOLCENGINE_API_KEY: xxx
- RECRAFT_API_KEY: sk-xxx
- IDEOGRAM_API_KEY: xxx
- FAL_API_KEY: sk-xxx
```

**读取规则**：agent 启动生图任务时，先读取 SECRET.md 对应 key。key 不存在 → 告知用户需要提供，并给出获取指引（见下方各模型"获取 Key"章节）。

**场景→模型→Key 映射**：

| 场景 | 首选模型 | 需要 Key | 备选模型 | 需要 Key |
|------|---------|---------|---------|---------|
| 角色/人物 | GPT Image 2 | OPENAI_API_KEY | Seedream 5.0 | VOLCENGINE_API_KEY |
| 风景/场景 | Flux 2 Pro | FAL_API_KEY | GPT Image 2 | OPENAI_API_KEY |
| 游戏素材/图标 | Recraft V4.1 | RECRAFT_API_KEY | GPT Image 2 | OPENAI_API_KEY |
| 文字海报/排版 | Ideogram v3 | IDEOGRAM_API_KEY | Seedream 5.0(中文) | VOLCENGINE_API_KEY |
| 风格化/艺术 | GPT Image 2 | OPENAI_API_KEY | Flux 2 Pro | FAL_API_KEY |
| 商业摄影 | Flux 2 Pro | FAL_API_KEY | GPT Image 2 | OPENAI_API_KEY |

**降级链**：首选模型无 Key → 备选模型 → 任何有 Key 的可用模型 → 告知用户"当前场景无可用模型，请提供 [Key名]"

---

## 1. OpenAI GPT Image 2

### 获取 Key
1. 访问 https://platform.openai.com/api-keys
2. 创建 API Key（以 `sk-` 开头）
3. 存入 SECRET.md → `OPENAI_API_KEY`
4. 需要充值余额（预付费）

### API 调用

**端点**: `POST https://api.openai.com/v1/images/generations`

**认证**: `Authorization: Bearer sk-xxx`

**Python 调用**:
```python
from openai import OpenAI
import base64

client = OpenAI()  # 自动读取 OPENAI_API_KEY 环境变量

result = client.images.generate(
    model="gpt-image-2",
    prompt="你的prompt",
    size="1024x1024",        # 支持: 1024x1024, 1536x1024, 1024x1536, auto
    quality="high",          # low / medium / high / auto
    n=1,                     # 1-10
    output_format="png",     # png / jpeg / webp
    background="auto",       # transparent / opaque / auto（transparent需png/webp）
)

# 获取图片
image_b64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_b64)
with open("output.png", "wb") as f:
    f.write(image_bytes)
```

**curl 调用**:
```bash
curl -X POST https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image-2",
    "prompt": "你的prompt",
    "size": "1024x1024",
    "quality": "high",
    "n": 1
  }'
```

**图片编辑端点**: `POST https://api.openai.com/v1/images/edits`
```python
result = client.images.edit(
    model="gpt-image-2",
    image=open("input.png", "rb"),
    prompt="把背景换成XX",
)
```

### 价格
- low: ~$0.006/张 | medium: ~$0.038/张 | high: ~$0.211/张（1024×1024）
- 输入参考图额外计费

### 限制
- prompt 最长 32000 字符
- 自定义尺寸：长边≤3840px，宽高均为16倍数，宽高比1:3~3:1
- 内容审核较严格

### 第三方中转站接入（已验证可用）

如果无法直连 OpenAI（网络/支付限制），可用中转站，base_url 替换即可：

```python
client = OpenAI(
    api_key="你的中转站Key",
    base_url="https://www.packyapi.com/v1",  # 中转站endpoint
)
# 其余调用代码完全相同
result = client.images.generate(
    model="gpt-image-2",
    prompt="你的prompt",
    size="1024x1024",
    quality="high",
    n=1,
)
```

**已验证**：packyapi.com + gpt-image-2 → 1024×1024 low quality 成功，图片质量与直连一致。
**注意**：中转站价格和限额可能与 OpenAI 官方不同，以中转站页面为准。

---

## 2. 火山引擎 Seedream 5.0

### 获取 Key
1. 访问 https://console.volcengine.com/ark
2. 创建 API Key
3. 存入 SECRET.md → `VOLCENGINE_API_KEY`
4. 国内平台，支持支付宝充值

### API 调用（火山引擎原生）

**端点**: `POST https://ark.cn-beijing.volces.com/api/v3/images/generations`

**认证**: `Authorization: Bearer {API_KEY}`

**Python 调用（requests，推荐）**:
```python
import requests

resp = requests.post(
    "https://ark.cn-beijing.volces.com/api/v3/images/generations",
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer 你的VOLCENGINE_API_KEY",
    },
    json={
        "model": "doubao-seedream-5-0-260128",     # 5.0-lite
        "prompt": "一只赛博朋克风格的猫",
        "sequential_image_generation": "disabled",  # disabled=单图 | enabled=多图序列
        "response_format": "url",                    # url(24h有效) / b64_json
        "size": "2K",                                # 见下方尺寸预设
        "stream": False,
        "watermark": True,
    },
    timeout=120,
)
data = resp.json()
image_url = data["data"][0]["url"]
```

**参考图生成**（图生图）:
```python
resp = requests.post(
    "https://ark.cn-beijing.volces.com/api/v3/images/generations",
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer 你的VOLCENGINE_API_KEY",
    },
    json={
        "model": "doubao-seedream-5-0-260128",
        "prompt": "将图1的服装换为图2的服装",
        "image": [                                      # 最多14张参考图URL
            "https://example.com/ref1.png",
            "https://example.com/ref2.png",
        ],
        "sequential_image_generation": "disabled",
        "response_format": "url",
        "size": "2K",
        "stream": False,
        "watermark": True,
    },
    timeout=120,
)
```

**OpenAI 兼容模式**（也可用，但参数名不同）:
```python
from openai import OpenAI

client = OpenAI(
    api_key="你的VOLCENGINE_API_KEY",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

result = client.images.generate(
    model="doubao-seedream-5-0-260128",
    prompt="一只赛博朋克风格的猫",
    size="1024x1024",
    n=1,
    response_format="url",
)
image_url = result.data[0].url
```

**尺寸预设**:
| 值 | 含义 | 最小像素要求 |
|----|------|------------|
| `"2K"` | 自动2K分辨率 | 3,686,400 (≈1920×1920) |
| `"3K"` | 自动3K分辨率 | — |
| `"4K"` | 自动4K分辨率 | — |
| `"1024x1024"` 等 | 自定义 | ≥3,686,400像素 |
| `auto_2K` / `auto_3K` / `auto_4K` | OpenAI兼容模式 | — |

⚠️ **注意**：5.0-lite 最小像素要求 3,686,400（≈1920×1920），1024×1024 会报 400 错误。务必使用 `"2K"` 或更大尺寸。

**模型 ID 对照**:
| 版本 | Model ID | 特点 |
|------|----------|------|
| 5.0-lite | doubao-seedream-5-0-260128 | CoT推理+联网检索+多图参考(14张)，PNG输出 |
| 4.5 | doubao-seedream-4-5-251128 | 最高画质上限，人像/美观度强 |
| 4.0 | doubao-seedream-4-0-250828 | 极速低成本 |

### 价格
- 5.0-lite: ~¥0.25/张 (~$0.035)
- 4.5: ~¥0.20/张
- 4.0: ~¥0.04/张

### 特殊能力
- **联网检索**（仅5.0-lite）: prompt中加 `tools: [{"type": "web_search"}]`
- **多图参考**: image字段传URL列表，最多14张
- **中文强**: 直接用中文prompt效果优于英文
- **速率**: 500 IPM

### 替代接入方式（ofox.ai 聚合）
如果火山引擎原生API接入困难（签名鉴权），可用 ofox.ai 聚合平台：
```python
client = OpenAI(
    api_key="你的OFOX_API_KEY",
    base_url="https://api.ofox.ai/v1",
)
result = client.images.generate(
    model="volcengine/doubao-seedream-5.0-lite",
    prompt="你的prompt",
    size="1024x1024",
)
```

---

## 3. Ideogram v3

### 获取 Key
1. 访问 https://developer.ideogram.ai/
2. 注册开发者账号，获取 API Key
3. 存入 SECRET.md → `IDEOGRAM_API_KEY`

### API 调用

**端点**: `POST https://api.ideogram.ai/api/ideogram/v3/generate`

**认证**: `Api-Key: {API_KEY}`

**Python 调用**:
```python
import requests

response = requests.post(
    "https://api.ideogram.ai/api/ideogram/v3/generate",
    headers={
        "Api-Key": "你的IDEOGRAM_API_KEY",
        "Content-Type": "application/json",
    },
    json={
        "prompt": "你的prompt",
        "rendering_speed": "QUALITY",    # TURBO / BALANCED / QUALITY
        "image_size": "ASPECT_3_4",      # 预设比例
        "style_type": "AUTO",            # AUTO / GENERAL / REALISTIC / DESIGN
        "num_images": 1,                 # 1-4
        "seed": None,                    # 可选，0-2147483647
    },
)

result = response.json()
image_url = result["data"][0]["url"]     # 24h有效
```

**图片尺寸预设**:
- `ASPECT_1_1` (1024×1024)
- `ASPECT_3_4` / `ASPECT_4_3`
- `ASPECT_16_9` / `ASPECT_9_16`
- `ASPECT_4_5` / `ASPECT_5_4`

**编辑端点**: `POST https://api.ideogram.ai/api/ideogram/v3/edit`
- 支持图片编辑（multipart/form-data）
- 支持 mask 局部重绘

### 价格
| 档位 | 价格/张 | 适用 |
|------|---------|------|
| TURBO | $0.0375 | 快速迭代/批量 |
| BALANCED | $0.075 | 日常生产 |
| QUALITY | $0.1125 | 最终交付 |

### 替代接入方式
- **fal.ai**: model=`ideogram-v3`，统一 fal key
- **Atlas Cloud**: model=`ideogram/ideogram-v3/text-to-image`
- **FairStack**: model=`ideogram-v3`，$0.036/张

---

## 4. Recraft V4.1

### 获取 Key
1. 访问 https://www.recraft.ai/ → 注册 → Settings → API Keys
2. 创建 API Key（以 `sk-` 开头）
3. 存入 SECRET.md → `RECRAFT_API_KEY`

### API 调用

**端点**: `POST https://external.api.recraft.ai/v1/images/generations`

**认证**: `Authorization: Bearer sk-xxx`

**Python 调用（OpenAI 兼容）**:
```python
from openai import OpenAI

client = OpenAI(
    api_key="你的RECRAFT_API_KEY",
    base_url="https://external.api.recraft.ai/v1",
)

result = client.images.generate(
    prompt="Minimalist logo for a coffee shop",
    extra_body={
        "style": "vector_illustration",    # realistic_image / digital_illustration / vector_illustration / icon
        "image_size": "1024x1024",         # 或 1792x1024 / 1024x1792
        "model": "recraftv4",              # recraftv4 / recraftv4_pro / recraftv4_vector / recraftv4_pro_vector
    }
)

print(result.data[0].url)
```

**SVG 矢量输出**:
```python
result = client.images.generate(
    prompt="A game icon of a sword",
    extra_body={
        "style": "icon",
        "model": "recraftv4_vector",
        "response_format": "svg",
    }
)
```

**自定义品牌风格**:
```python
# 1. 创建风格
response = requests.post(
    "https://external.api.recraft.ai/v1/styles",
    headers={"Authorization": "Bearer sk-xxx"},
    files={"style": "digital_illustration", "image": open("ref.png", "rb")}
)
style_id = response.json()["style_id"]

# 2. 使用风格生成
result = client.images.generate(
    prompt="你的prompt",
    extra_body={"style_id": style_id}
)
```

### 价格
- recraftv4: ~$0.04/张
- recraftv4_pro: ~$0.08/张
- 矢量输出同价

### 核心优势
- **唯一原生SVG矢量输出**——游戏图标/Logo的最佳选择
- **100+内置风格**——icon / realistic_image / digital_illustration / vector_illustration
- **自定义品牌色彩**——锁定hex色板跨图一致
- HuggingFace Logo生成排行#1

---

## 5. Flux 2 Pro (via fal.ai)

### 获取 Key
1. 访问 https://fal.ai/ → 注册 → Keys
2. 创建 API Key
3. 存入 SECRET.md → `FAL_API_KEY`

### API 调用

**fal.ai 端点**: `POST https://queue.fal.run/black-forest-labs/flux-2-pro`

**Python 调用（fal 客户端）**:
```python
import fal_client

# 设置环境变量 FAL_KEY
result = fal_client.submit(
    "black-forest-labs/flux-2-pro",
    arguments={
        "prompt": "你的prompt",
        "image_size": "landscape_16_9",   # square / portrait_4_3 / landscape_16_9 等
        "num_images": 1,
        "seed": None,
    },
)

# 异步等待结果
for event in result.iter_events():
    pass  # 处理进度事件

output = result.get()
image_url = output["images"][0]["url"]
```

**Python 调用（REST）**:
```python
import requests

response = requests.post(
    "https://queue.fal.run/black-forest-labs/flux-2-pro",
    headers={
        "Authorization": "Key 你的FAL_API_KEY",
        "Content-Type": "application/json",
    },
    json={
        "prompt": "你的prompt",
        "image_size": "landscape_16_9",
    },
)

request_id = response.json()["request_id"]

# 轮询结果
import time
while True:
    status = requests.get(
        f"https://queue.fal.run/black-forest-labs/flux-2-pro/requests/{request_id}",
        headers={"Authorization": "Key 你的FAL_API_KEY"},
    ).json()
    if status["status"] == "COMPLETED":
        image_url = status["images"][0]["url"]
        break
    time.sleep(2)
```

### 价格
- Flux 2 Pro: ~$0.03/张（fal.ai 按 megapixel 计费 $0.03/MP）
- Flux 2 Schnell: ~$0.01/张
- Flux 2 Dev: ~$0.025/张

### 替代接入方式
| 平台 | 模型ID | 价格 | 特点 |
|------|--------|------|------|
| Replicate | black-forest-labs/flux-2-pro | ~$0.03/张 | 简单REST |
| Atlas Cloud | black-forest-labs/flux-2-pro/text-to-image | ~$0.03/张 | 聚合多模型 |
| BFL 直连 | flux-2-pro | ~$0.03/张 | 原厂 |

### 核心优势
- **写实标杆**——LM Arena Elo 1265（Pro v1.1）
- **长prompt遵循**——最复杂的空间指令也能执行
- **极速**——~3秒出图
- **性价比**——同品质下 GPT Image 2 的 1/7 价格

---

## 聚合平台备选

如果不想逐个注册多家 API，可以用聚合平台一个 Key 访问多模型：

| 平台 | 支持模型 | 优势 | 价格加成 |
|------|---------|------|---------|
| fal.ai | 600+模型含Flux/Recraft/Ideogram | 冷启动5-10秒 | ~0% |
| Atlas Cloud | Flux/Imagen/Ideogram/Seedream | 中文文档好 | ~0% |
| ofox.ai | Seedream/GPT Image/Flux等 | 国内友好 | ~20% |
| FairStack | Ideogram/Flux/Seedream | 透明定价 | ~20% |

---

## 错误处理速查

| HTTP码 | 含义 | 处理 |
|--------|------|------|
| 401 | Key无效/过期 | 提醒用户更新SECRET.md中的Key |
| 402 | 余额不足 | 提醒用户充值 |
| 429 | 速率限制 | 等待 Retry-After 头指定秒数后重试 |
| 400 | 请求格式错误 | 检查prompt/参数格式 |
| 500 | 服务端错误 | 重试1次，仍失败换备选模型 |

---

> v1.0 — 2026-06-14。基于各模型官方文档和社区验证。价格可能变动，以官方为准。
