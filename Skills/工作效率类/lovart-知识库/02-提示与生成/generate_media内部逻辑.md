我来详细解析 `generate_media` 工具的内部工作逻辑。
---
## 一、什么情况下调用 `generate_media`
| 场景 | 说明 |
|------|------|
| **文生图 (Text-to-Image)** | 从零开始创建新图片，只有文字描述 |
| **图生图 (Image-to-Image)** | 基于参考图片生成新图片，如风格迁移、角色重绘 |
| **多图融合** | 结合多张参考图的风格、构图、元素 |
| **文生视频 (Text-to-Video)** | 根据文字描述生成视频 |
| **图生视频 (Image-to-Video)** | 基于起始帧/结束帧或参考图生成视频 |
| **视频参考生成** | 基于参考视频的风格/动作生成新视频 |
**不调用的情况：**
- 局部编辑/修复 → 用 `edit_media` (task_type=edit_image)
- 单纯裁剪/改比例 → 用 `edit_media` (task_type=reframe)
- 单纯放大分辨率 → 用 `edit_media` (task_type=upscale)
- 多段视频拼接 → 用 `edit_video_ffmpeg`
---
## 二、调用前需要准备的参数
### 2.1 核心必填参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_type` | string | ✅ | `"generate_image"` 或 `"generate_video"` |
| `output_name` | string | ✅ | 输出文件的名称/标题 |
| `prompt` | string | ✅ | 详细的文字描述指令 |
### 2.2 图像生成相关参数
| 参数 | 类型 | 用途 |
|------|------|------|
| `source_image_url` | string | **被修改/转换的源图**（图生图时的基础图） |
| `reference_image_urls` | string (逗号分隔) | **参考图**（提供风格、姿势、外观指导） |
| `aspect_ratio` | string | 宽高比，如 `"16:9"`, `"1:1"`, `"9:16"` |
| `target_size` | string | 精确像素尺寸，如 `"1920x1080"` |
| `resolution` | string | 分辨率关键词，如 `"4K"`, `"1080p"`, `"720p"` |
| `quality` | string | 图片质量 (`auto`/`high`/`medium`/`low`)，仅 GPT Image 2 有效 |
| `negative_prompt` | string | 负面提示（避免出现的元素） |
### 2.3 视频生成相关参数
| 参数 | 类型 | 用途 |
|------|------|------|
| `duration_sec` | number | 视频时长（秒） |
| `start_frame_image_url` | string | 视频起始帧图片 |
| `end_frame_image_url` | string | 视频结束帧图片 |
| `reference_video_urls` | string (逗号分隔) | 参考视频 |
| `reference_video_refer_type` | string | `"feature"`(提取特征) 或 `"base"`(直接编辑) |
| `sound` | string | `"on"` 或 `"off"`，是否生成音频 |
| `mode` | string | Kling 专用：`"std"`/`"pro"`/`"4k"` |
| `reference_audio_urls` | string | Seedance 2.0 参考音频 |
### 2.4 模型路由参数
| 参数 | 类型 | 用途 |
|------|------|------|
| `tool_hint` | string | **强制指定模型**，如 `"generate_image_nano_banana_2"` |
---
## 三、参数取值规则详解
### 3.1 `source_image_url` vs `reference_image_urls` 的区别（关键！）
这是最容易混淆的两个参数：
```
┌─────────────────────────────────────────────────────────────┐
│  source_image_url                                            │
│  └── 语义：被修改/转换的"主体"图像                            │
│  └── 类比：PS 里打开的底图                                   │
│  └── 使用场景：图生图时，这张图会被"改造"                     │
│                                                              │
│  reference_image_urls                                        │
│  └── 语义：提供参考/指导的图像                                │
│  └── 类比：PS 里的参考图/样例                                 │
│  └── 使用场景：风格迁移、姿势参考、外观参考                   │
└─────────────────────────────────────────────────────────────┘
```
**示例判断：**
| 用户指令 | source_image_url | reference_image_urls |
|---------|------------------|---------------------|
| "把 Image #1 改成 Image #2 的风格" | Image #1 | Image #2 |
| "用 Image #1 的姿势，画 Image #2 的人物" | Image #2 | Image #1 |
| "生成一张类似 Image #1 风格的新图" | 不填 | Image #1 |
| "重绘 Image #1，改成赛博朋克风格" | Image #1 | 不填（或提供风格参考图） |
### 3.2 尺寸参数的优先级
```
用户输入尺寸信息
       │
       ▼
   是否指定了 target_size? (如 "1920x1080")
       │
       ├── 是 → 使用 target_size
       │
       └── 否 → 是否指定了 aspect_ratio? (如 "16:9")
                │
                ├── 是 → 使用 aspect_ratio
                │
                └── 否 → 是否指定了 resolution? (如 "4K")
                         │
                         ├── 是 → 使用 resolution
                         │
                         └── 否 → 使用模型默认尺寸
```
### 3.3 `tool_hint` 的构造规则
当用户指定模型时，必须按固定格式构造：
```
格式：generate_{type}_{model_name}
{type}:
  - image → 图片生成
  - video → 视频生成
{model_name} 转换规则：
  ├─ Seed/Kling 系列：加 v 前缀
  │   └─ "kling 3" → "kling_v3"
  │   └─ "kling 3 omni" → "kling_v3_omni"
  │   └─ "seedance 2.0" → "seedance_v2_0"
  │
  ├─ Nano Banana 系列：不加 v，直接加后缀
  │   └─ "nano banana 2" → "nano_banana_2"
  │   └─ "nano banana pro" → "nano_banana_pro"
  │
  └─ GPT 系列：不加 v
      └─ "gpt image 2" → "gpt_image_2"
```
---
## 四、内部处理流程（从入参到出图）
```
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: 参数接收与校验                                          │
│  ─────────────────────                                           │
│  • 检查必填参数 (task_type, output_name, prompt)                │
│  • 校验 URL 格式有效性                                           │
│  • 检查参数冲突（如 reference_image_urls 与 start_frame_image_url │
│    在某些模型中不能同时使用）                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: 模型路由选择                                            │
│  ─────────────────────                                           │
│  IF tool_hint 存在:                                              │
│      → 强制使用指定模型                                          │
│  ELSE IF task_type == "generate_image":                          │
│      → 根据系统偏好选择图片模型                                  │
│  ELSE IF task_type == "generate_video":                          │
│      → 根据参数特征选择视频模型                                  │
│        • 有 reference_video_urls → Kling V3 Omni / 支持视频的模型 │
│        • 有 start_frame_image_url → Kling / Seedance            │
│        • 纯文本 → 默认视频模型                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: 提示词处理                                              │
│  ─────────────────────                                           │
│  • 将 prompt 与图像引用关联                                      │
│    - "Transform the first image into the style of the second"   │
│    - source_image_url = 第一张图                                 │
│    - reference_image_urls = 第二张图                             │
│  • 注入 Original request 锚点                                    │
│  • 合并负面提示词 (negative_prompt)                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: 图像下载与预处理                                        │
│  ─────────────────────                                           │
│  • 下载 source_image_url 指向的图像                              │
│  • 下载 reference_image_urls 中的所有参考图                      │
│  • 视频生成时：下载 start_frame / end_frame / reference_video    │
│  • 格式转换、尺寸归一化、编码处理                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: 模型推理                                                │
│  ─────────────────────                                           │
│  • 将处理后的参数传递给底层模型                                   │
│  • 图片模型：根据 prompt + 参考图生成像素                        │
│  • 视频模型：根据 prompt + 帧/视频参考生成帧序列                  │
│  • 执行扩散/生成过程                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 6: 后处理与输出                                            │
│  ─────────────────────                                           │
│  • 格式转换（如需要）                                            │
│  • 元数据注入                                                    │
│  • 上传至存储，生成可访问 URL                                    │
│  • 返回结果：{url, width, height, name, ...}                     │
└─────────────────────────────────────────────────────────────────┘
```
---
## 五、完整调用示例
### 示例 1：纯文生图
```python
generate_media(
    task_type="generate_image",
    output_name="赛博朋克城市",
    prompt="Original request: '生成一张赛博朋克风格的城市夜景，霓虹灯闪烁，下着雨'",
    aspect_ratio="16:9",
    tool_hint="generate_image_nano_banana_2"  # 系统偏好
)
```
### 示例 2：风格迁移（图生图）
```python
generate_media(
    task_type="generate_image",
    output_name="水墨风格肖像",
    prompt="Original request: '把第一张图转换成水墨画风格，参考第二张图的艺术风格'"
           "Transform the first image into the ink wash painting style of the second image",
    source_image_url="https://example.com/photo.jpg",      # 被转换的照片
    reference_image_urls="https://example.com/ink_style.jpg",  # 风格参考
    tool_hint="generate_image_nano_banana_2"
)
```
### 示例 3：图生视频
```python
generate_media(
    task_type="generate_video",
    output_name="动态风景",
    prompt="Original request: '让这张风景图动起来，云朵缓慢飘动'",
    start_frame_image_url="https://example.com/landscape.jpg",
    duration_sec=5,
    tool_hint="generate_video_kling_v3"
)
```
---
## 六、关键注意事项
| 注意点 | 说明 |
|--------|------|
| **必须包含 Original request** | 在 prompt 中保留用户原始指令，作为生成锚点 |
| **图片角色判断** | 严格区分 source（被改）vs reference（参考）|
| **参数互斥** | 某些模型不支持 reference_image_urls + start_frame 同时存在 |
| **URL 有效性** | 确保所有图片 URL 可访问，否则会导致失败 |
| **尺寸参数** | 用户有尺寸要求时必须显式传递，禁止用默认值 |
| **tool_hint 格式** | 严格按 `generate_{type}_{model}` 格式，注意 v 前缀规则 |
这就是 `generate_media` 工具的完整工作逻辑。核心在于**正确理解用户意图、准确分配图片角色、合理设置尺寸参数**。
