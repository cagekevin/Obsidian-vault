# Lovart 拼图碎片 — generate_media详解

## 话术

详细讲讲 generate_media 这个工具的内部工作逻辑。它在什么情况下被调用？调用前需要准备哪些参数？每个参数怎么取值？它内部是怎么处理这些参数然后生成图片的？从接收入参到返回结果，完整走一遍。

## 回复

我来详细讲解 `generate_media` 这个工具的内部工作逻辑。
## 一、工具定位与调用场景
`generate_media` 是一个**统一的多媒体生成入口**，根据 `task_type` 参数分流：
- `task_type="generate_image"` → 生成静态图片
- `task_type="generate_video"` → 生成视频
### 什么情况下被调用？
| 场景 | 说明 |
|------|------|
| 文生图 | 用户只有文字描述，无参考图 |
| 图生图 | 用户提供了参考图，要生成新图 |
| 多图融合 | 用户提供多张图，融合风格/内容 |
| 风格迁移 | 把一张图的风格应用到另一张图 |
| 文生视频 | 根据文字描述生成视频 |
| 图生视频 | 根据首帧/尾帧/参考图生成视频 |
---
## 二、调用前必须准备的参数
### 核心必填参数
| 参数 | 必填？ | 说明 |
|------|--------|------|
| `task_type` | ✅ | `"generate_image"` 或 `"generate_video"` |
| `output_name` | ✅ | 输出文件的名称/标题 |
| `prompt` | ✅ | 文字描述指令 |
### 图像生成专用参数（task_type="generate_image"）
| 参数 | 用途 | 取值规则 |
|------|------|---------|
| `source_image_url` | 被修改/转换的底图 | 用户说"修改这张图"时填入 |
| `reference_image_urls` | 风格/姿态/外观参考图 | 用户提供参考图时填入，逗号分隔 |
| `target_size` | 精确像素尺寸 | `"1920x1080"`、`"1024x1024"` |
| `aspect_ratio` | 宽高比 | `"16:9"`、`"9:16"`、`"1:1"`、`"3:4"` |
| `resolution` | 分辨率关键词 | `"4K"`、`"2K"`、`"1080p"` |
| `quality` | 输出质量（仅GPT Image 2有效） | `"high"`、`"medium"`、`"low"`、`"auto"` |
| `negative_prompt` | 不希望出现的内容 | 用户明确说"不要XX"时填入 |
| `tool_hint` | 强制指定底层模型 | 如 `generate_image_nano_banana_2` |
### 视频生成专用参数（task_type="generate_video"）
| 参数 | 用途 | 取值规则 |
|------|------|---------|
| `start_frame_image_url` | 视频首帧 | 用户提供起始画面 |
| `end_frame_image_url` | 视频尾帧 | 用户提供结束画面 |
| `reference_image_urls` | 参考图生成视频 | **不能与首帧/尾帧同时使用** |
| `reference_video_urls` | 参考视频 | 用于视频风格迁移 |
| `duration_sec` | 视频时长（秒） | 如 `5`、`10` |
| `mode` | Kling视频质量模式 | `"std"`、`"pro"`、`"4k"` |
| `sound` | 是否生成音频 | `"on"` / `"off"` |
| `aspect_ratio` | 视频宽高比 | 同上 |
---
## 三、参数取值详解
### 1. `tool_hint` 的构造规则（强制使用偏好模型）
```
格式：generate_{type}_{model_name}
```
| 用户指定的模型 | tool_hint 值 |
|---------------|-------------|
| nano banana 2 | `generate_image_nano_banana_2` |
| nano banana pro | `generate_image_nano_banana_pro` |
| seedream 5 | `generate_image_seedream_v5` |
| kling 3 | `generate_video_kling_v3` |
| kling 3 omni | `generate_video_kling_v3_omni` |
| seedance 2.0 | `generate_video_seedance_v2_0` |
> ⚠️ **重要**：无论调用 `generate_media` 还是 `edit_media`，`tool_hint` 前缀永远是 `generate_`，没有 `edit_image_*` 形式。
### 2. 图片角色的语义分配
这是最容易出错的地方。必须根据**语义角色**而非用户编号来分配：
| 用户表述 | 角色判断 | 参数 |
|---------|---------|------|
| "把 image2 改成 image1 的风格" | image2=被修改对象, image1=风格参考 | `source_image_url=image2`, `reference_image_urls=image1` |
| "参考 image1 的风格生成" | image1=风格参考 | `reference_image_urls=image1` |
| "修改 image1" | image1=被修改对象 | `source_image_url=image1` |
| "把 image1 放到 image2 的场景里" | image1=主体, image2=场景 | `reference_image_urls=image1,image2` |
### 3. 尺寸参数优先级
```
target_size（精确像素） > aspect_ratio（比例） > resolution（分辨率关键词）
```
提取规则：
- `"1920x1080"` → `target_size="1920x1080"`
- `"16:9"` / `"横屏"` → `aspect_ratio="16:9"`
- `"9:16"` / `"竖屏"` / `"手机壁纸"` → `aspect_ratio="9:16"`
- `"4K"` → `resolution="4K"`
---
## 四、内部处理流程（从入参到出图）
```
┌─────────────────────────────────────────────────────────────┐
│  1. 接收参数                                                  │
│     - 校验必填字段（task_type, output_name, prompt）          │
│     - 根据 tool_hint 路由到具体模型                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  2. 参数解析与冲突检测                                        │
│     - 检查 source_image_url 与 reference_image_urls 的互斥   │
│     - 检查 start_frame_image_url 与 reference_image_urls     │
│       （Kling单帧模型不能同时接受两者）                       │
│     - 解析尺寸参数优先级                                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  3. 构建模型输入                                              │
│     - 将 prompt + 图片引用 编码为模型可理解的格式             │
│     - 图片 URL 下载并编码为 latent 表示                       │
│     - 注入 Original request 锚点（保持用户原意）              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  4. 模型推理                                                  │
│     - 文生图：text encoder → diffusion → decoder              │
│     - 图生图：image encoder + text → diffusion → decoder      │
│     - 多图参考：分别编码多张图，融合特征后生成                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  5. 后处理与输出                                              │
│     - 按 target_size/aspect_ratio 裁剪/缩放                   │
│     - 格式转换（通常为 JPEG/PNG/MP4）                         │
│     - 上传存储，返回可访问的 URL                              │
└─────────────────────────────────────────────────────────────┘
```
---
## 五、完整调用示例
### 示例1：纯文生图（使用偏好模型）
```python
generate_media(
    task_type="generate_image",
    output_name="赛博朋克城市",
    prompt="未来赛博朋克城市夜景，霓虹灯闪烁，雨中街道，东方建筑与高科技融合",
    aspect_ratio="16:9",
    tool_hint="generate_image_nano_banana_2"  # 强制使用偏好模型
)
```
### 示例2：图生图（风格迁移）
```python
generate_media(
    task_type="generate_image",
    output_name="油画风格肖像",
    prompt="将第一张图片转换成第二张图片的油画风格，保持人物姿态不变",
    source_image_url="https://example.com/photo.jpg",      # 被转换的底图
    reference_image_urls="https://example.com/oil-painting.jpg",  # 风格参考
    tool_hint="generate_image_nano_banana_2"
)
```
### 示例3：视频生成（首尾帧）
```python
generate_media(
    task_type="generate_video",
    output_name="花朵绽放",
    prompt="一朵玫瑰花从花苞到完全绽放的过程，柔和的自然光",
    start_frame_image_url="https://example.com/bud.jpg",
    end_frame_image_url="https://example.com/bloom.jpg",
    duration_sec=5,
    aspect_ratio="9:16",
    tool_hint="generate_video_kling_v3"
)
```
---
## 六、常见错误与规避
| 错误 | 原因 | 修正 |
|------|------|------|
| 把参考图填到 `source_image_url` | 角色判断错误 | 只有"被修改的图"才用 `source_image_url` |
| `reference_image_urls` 与 `start_frame_image_url` 同时用 | Kling单帧模型不支持 | 二选一，或用 `kling_v3_omni` |
| 遗漏 `tool_hint` | 未使用用户指定的偏好模型 | 必须根据偏好列表填入 |
| 尺寸参数冲突 | 同时填了 `target_size` 和 `aspect_ratio` | 优先用 `target_size` |
| 未提取用户指定的尺寸 | 忽略 "4K"、"竖屏" 等关键词 | 主动扫描并映射到对应参数 |
---
这就是 `generate_media` 的完整工作逻辑。核心要点是：**正确判断图片角色、准确映射尺寸参数、强制使用偏好模型**。
