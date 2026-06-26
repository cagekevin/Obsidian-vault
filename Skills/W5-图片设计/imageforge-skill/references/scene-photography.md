# 商业摄影/写实

## 判定条件

路由到此场景的信号：
- 关键词：摄影/photo/写真/人像portrait/产品摄影/product photography/商业/commercial/写实/realistic/修复/增强/换背景/compositing/静物
- 场景特征：写实是默认审美方向但也是偏见的重灾区——需要"阻止模型自作聪明"
- 典型请求："写实人像不要油腻感"/"产品图白底商业摄影"/"修复这张图但别上色"/"换背景保持光照一致"

核心难点（为什么要路由到这里）：
- 皮肤油腻——训练数据"好人像"=磨皮→光滑反光=好皮肤的错误映射
- 训练偏见——亚洲人单眼皮变双眼皮、深肤色被提亮，系统性数据不平衡
- 修复/增强陷阱——"增加细节"可能擅自上色，"修复"可能产生蜡像感
- 产品一致性——商业产品图需要统一视觉标准，不同批次不能漂移
- 换背景光线不匹配——只换像素不调光照→融合度低

---

## Prompt组装

### 模板A：写实人像（通用）

```
a [年龄段] [性别] with [发色发型], [瞳色] eyes,
natural skin texture, visible pores, matte finish,
[服装], [姿态],
[场景], [光影描述],
shot on [相机+镜头], shallow depth of field
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 年龄段+性别 | ✅ | 基本身份 | Flux中不写"one girl"（触发汪格尔综合症→出动漫风），写"girl"或具体自然语言 | a young woman / a middle-aged man |
| 发色发型 | ✅ | 不可变特征 | 越具体越好 | long wavy auburn hair |
| 瞳色 | 选填 | 不可变特征 | 亚洲角色显式指定`monolid eyes`对抗训练偏见 | hazel eyes / monolid brown eyes |
| 皮肤质感词 | ✅ | 对抗油腻感 | 必加——这不是"加个词"，是在提示词中显式定义"好皮肤=有毛孔的哑光质感"来覆盖模型默认映射 | natural skin texture, visible pores, matte finish |
| 服装 | 选填 | 可变特征 | 按场景搭配 | wearing black turtleneck |
| 姿态 | 选填 | 动作 | | looking slightly to the left, subtle smile |
| 场景 | 选填 | 环境 | | in a dimly lit café |
| 光影描述 | 选填 | 光照三要素 | 类型+方向+色温（见下表） | Rembrandt lighting, warm 3200K key light from 45° left |
| 相机+镜头 | 选填 | 增加写实感 | 模型见过带EXIF的专业照片 | Canon EOS R5, 85mm f/1.4 |

**写实摄影常用光源配置**：

| 场景 | 光源配置 | 提示词 |
|------|---------|--------|
| 标准人像 | 主光+辅光 | `key light from 45° left, soft fill from right` |
| 戏剧性人像 | 伦勃朗光 | `Rembrandt lighting, triangle of light on cheek` |
| 逆光人像 | 轮廓光 | `rim light from behind, hair light, dark background` |
| 美妆特写 | 蝴蝶光/环形光 | `butterfly lighting, shadow under nose` / `ring light, catchlight in eyes` |
| 户外人像 | 黄金时刻 | `golden hour, warm directional light, long shadows` |
| 产品摄影 | 柔光箱 | `soft diffused key light from upper left, subtle fill from right` |

**相机/镜头参数速查**：

| 关键词 | 效果 | 最佳场景 |
|--------|------|---------|
| Hasselblad X2D | 中画幅极度锐利 | 高端产品/静物 |
| Canon EOS R5 | 全画幅自然 | 通用商业 |
| Fujifilm X-T5 | 复古色彩科学 | 生活方式 |
| 85mm f/1.4 | 压缩+浅景深 | 人像/产品特写 |
| 50mm | 自然视角 | 环境人像 |
| 100mm macro | 极限特写 | 产品细节 |
| Kodak Portra 400 | 暖调胶片质感 | 生活方式/纪实 |

#### 示例

用户："写实人像，亚洲女性，不要油腻"
→ `a young woman with long straight black hair, monolid brown eyes, natural skin texture, visible pores, matte finish, wearing white linen shirt, looking at camera with gentle expression, in a sunlit studio, soft diffused key light from overhead, shot on Canon EOS R5, 85mm f/1.4, shallow depth of field`

---

### 模板B：MJ商业摄影

```
[主体], [光影], [场景], [相机参数],
professional photography, editorial style,
--ar 3:4 --s 250 --style raw --v 7
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 主体 | ✅ | 画谁/画什么 | | a woman in her 30s with auburn hair |
| 光影 | ✅ | 光照三要素 | | Rembrandt lighting from 45° left |
| 场景 | 选填 | 环境 | | in a modern studio |
| 相机参数 | 选填 | 相机+镜头 | | shot on Hasselblad X2D, 85mm f/1.4 |
| MJ参数 | ✅ | MJ专用 | `--style raw`关闭美化是商业摄影关键 | --ar 3:4 --s 250 --style raw --v 7 |

---

### 模板C：产品摄影（五要素）

```
[产品描述] on [表面材质],
[光源类型+方向] creating [光效],
shot on [相机+镜头] [光圈],
[风格/后处理], commercial product photography
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 产品描述 | ✅ | 产品+位置姿态 | 包含材质和视觉特征 | A frosted glass perfume bottle with gold cap, standing upright |
| 表面材质 | ✅ | 摆在什么上 | 影响反射和氛围 | on a white marble slab / on a dark walnut surface |
| 光源类型+方向 | ✅ | 光从哪来怎么照 | 创造产品的视觉高光 | soft diffused side lighting from the left |
| 光效 | 选填 | 光在产品上产生什么 | | creating a subtle highlight along the cap edge |
| 相机+镜头+光圈 | 选填 | 设备参数 | 产品摄影常用macro | shot on Hasselblad X2D with 100mm macro lens at f/5.6 |
| 风格/后处理 | 选填 | 整体风格 | | clean minimal aesthetic / luxury editorial |
| commercial product photography | ✅ | 类型锚定 | 触发商业摄影视觉模式 | |

**色彩锁定**（防止模型用"产品摄影平均配色"→通常是灰/白/蓝）：
```
[产品+材质], color palette strictly limited to [颜色1], [颜色2], [颜色3]
```

**参考图锚定**（图生图模式）：上传产品参考图→提示词只描述环境和光照→模型注意力集中在场景构建而非产品重建→减少产品变形。

#### 示例

→ `A frosted glass perfume bottle with gold cap, standing upright on a white marble slab, soft diffused side lighting from the left creating a subtle highlight along the cap edge, shot on Hasselblad X2D with 100mm macro lens at f/5.6, commercial product photography, clean minimal aesthetic`

---

### 模板D：人像修复/增强

```
preserve original color tone, enhance texture sharpness,
reduce noise artifacts, natural skin texture,
maintain original facial features and expression,
[具体修复目标如 remove blemishes / smooth skin slightly]
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| preserve original color tone | ✅ | 防止色调漂移 | 修复后色调可能漂移 | |
| enhance texture sharpness | ✅ | 锐化方向 | 不说"增加细节/4K/高清"——可能导致擅自上色 | |
| reduce noise artifacts | ✅ | 降噪方向 | 不说"修复"——编码为"更光滑"→蜡像感 | |
| natural skin texture | ✅ | 保持皮肤质感 | 修复不能丢皮肤真实感 | |
| maintain original features | ✅ | 保持面部特征 | | |
| 具体修复目标 | 选填 | 要修什么 | 具体而非笼统 | remove blemishes / smooth skin slightly / fix lighting on left side |

**修复/增强核心原则：指定方向，不笼统增强**：
1. 不说"增加细节"——说"enhance texture sharpness, reduce noise artifacts"
2. 不说"修复"——说"preserve original features, remove [具体缺陷]"
3. 不说"4K/高清"——说"maintain resolution, enhance edge clarity"
4. 重绘幅度0.3-0.5——保留原貌+修复损伤，过高会偏离原图
5. 颜色匹配——修复后色调可能漂移，加颜色匹配节点（ComfyUI）强制参考原图
6. 局部修复优于全局——Inpaint只改有问题的区域，不做全局重绘

---

### 模板E：商业合成（换背景）

```
[人物描述] standing in [新场景],
[新场景光线如 golden sunset light from the right],
[人物在新环境中的状态如 warm light casting on face, soft shadows on ground],
[新环境氛围如 lake reflections, distant mountains],
seamless compositing, consistent lighting throughout
```

#### 填充规则

| Slot | 必填? | 填什么 | 关键点 | 示例 |
|------|-------|--------|--------|------|
| 人物描述 | ✅ | 保留的人物 | | a woman in a red dress |
| 新场景 | ✅ | 新背景环境 | | standing by a lake at sunset |
| 新场景光线 | ✅ | 新环境的光线 | 关键！描述新场景光线+人物在新环境中的状态→模型重建整个光照→融合度高 | golden sunset light from the right |
| 人物在新环境中的状态 | ✅ | 光线如何影响人物 | ❌只说"换背景到日落湖边"只换像素不调光；✅描述光线如何打在人物身上 | warm light casting on face, soft shadows on ground |
| 新环境氛围 | 选填 | 环境细节 | | lake reflections, distant mountains |
| seamless compositing | ✅ | 合成标记 | | |

**换背景关键**：直接说"更换背景"只换背景不动光线→融合度低。描述"人物在新场景中的状态+新场景的光线氛围"→模型重建整个光照→融合度更高。

---

### 模板F：产品摄影速成食谱

**二段式**（最快）：
```
on [表面/位置], [背景元素和颜色]
```

**三段式**（更多控制）：
```
on [表面/位置], [光照和氛围], [背景风格]
```

**输入图质量要求**：
- 锐利、光线充足，产品完整可见
- 边缘不裁切，Logo/纹理对焦清晰
- 正面角度+均匀照明+简洁背景=最佳起点

---

## 诊断路由

| 观察到 | 可能原因 | 修复动作 | 规则 |
|--------|---------|---------|------|
| 写实人像油腻 | 磨皮数据→光滑=好皮肤 | 加"natural skin texture, visible pores, matte finish" | P02 |
| Flux出动漫风 | "one girl"与动漫数据共现 | 写"girl"而非"one girl"（汪格尔综合症） | R12 |
| 手部崩坏 | 手部训练不足+空间定位弱 | 局部修复工具（SD: ADetailer+负向词） | P03 |
| 亚洲人偏见 | 训练数据不平衡 | 显式指定"monolid eyes"等特征；严重时需针对性LoRA | P02 |
| "4K"擅自上色 | "增加细节"编码为"更多元素" | 指定增强方向："preserve original color, enhance texture sharpness" | R11 |
| 修复产生蜡像感 | "修复"编码为"更光滑" | "maintain original features, reduce noise"而非"修复/增强" | R11 |
| 换背景光线不匹配 | 只改像素不调光照 | 描述新场景光线+人物在新环境中的状态 | R05 |
| 修复色调漂移 | 去噪过程重定色温 | 加颜色匹配节点（ComfyUI），或"preserve original color tone" | R11 |
| 产品变形 | 模型猜产品形状 | 用参考图图生图，提示词只描述环境 | R06 |
| 产品配色Generic | 未指定色彩 | 用色彩锁定："color palette strictly limited to [色1], [色2]" | R05 |

---

## 场景必检项

```
□ 写实人像：皮肤质感词已加？（natural skin texture, visible pores, matte finish）
□ 写实人像：有无训练偏见风险？（亚洲人→显式指定monolid eyes；深肤色→显式指定肤色）
□ 写实人像：Flux环境→不写"one girl"
□ 产品摄影：五要素齐了？（产品/表面/光源+光效/相机/风格）
□ 产品摄影：色彩锁定了？（不锁定→模型用"平均配色"）
□ 修复/增强：指定方向而非笼统增强？（不说"增加细节/4K/修复"）
□ 修复/增强：重绘幅度0.3-0.5？（过高偏离原图）
□ 换背景：光线+人物状态一起描述了？（不能只换像素不调光照）
□ 修复色调漂移：preserve original color tone写了？
```

---

## 模型注意

- **Imagen 4**：写实天花板——盲测最难辨；但国内难用需VPN
- **MJ + --style raw**：审美加工顶级+关闭美化→商业摄影经典参数`--ar 3:4 --s 250 --style raw`
- **Flux**：人像油腻需抗油腻词；写实图写"girl"不写"one girl"；CFG 2.5-3.5
- **Gemini Flash**：免费写实标杆——日常场景性价比最高
- **GPT Image 2**：对话式迭代适合逐步调整——"把光线改成侧光"、"把背景换成暗色"
- **SD**：需画质词+负向词；ADetailer修复手部；ControlNet光照图精确控制明暗
