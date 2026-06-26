# Lovart 拼图碎片 — 详情页复刻-产品替换Prompt

## 话术

电商主图复刻中SKU替换（产品替换）的最佳Prompt怎么写？请给出：1) 标准模板结构 2) 不同品类（美妆/3C/食品/服装）的案例各一个 3) 多步替换策略（简单替换/复杂替换/批量替换的区别） 4) 垫图顺序和配置。用中英文双语回答。

## 回复

# 电商主图SKU替换最佳实践指南 | E-commerce Product Replacement Best Practices
## 1. 标准Prompt模板结构 | Standard Prompt Template Structure
### 🎯 核心模板 | Core Template
```
[操作指令] Replace the [原产品描述] in the first image with the [新产品描述] from the second image, while preserving all other elements including [保留元素列表: background, lighting, composition, props, layout, shadows, reflections, perspective].
[细节要求] The new [产品] should:
- Match the exact position, size, and angle of the original product
- Integrate naturally with the existing lighting and shadows
- Maintain the same visual style and quality
- Preserve all background elements, text, and decorative items unchanged
[质量控制] Keep the overall composition, color scheme, and professional e-commerce photography style consistent.
```
### 📋 关键要素拆解 | Key Components
| 要素 Element | 作用 Purpose | 示例 Example |
|-------------|-------------|--------------|
| **操作动词** Operation Verb | 明确替换动作 | Replace / Swap / Substitute |
| **图片顺序说明** Image Order | 指定哪张是底图/参考图 | "the first image" (base), "the second image" (reference) |
| **产品精确描述** Product Description | 避免混淆 | "the red lipstick" → "the pink lipstick" |
| **保留清单** Preservation List | 防止过度编辑 | background, lighting, props, text, layout |
| **融合要求** Integration Requirements | 确保自然 | match position/size/angle, natural lighting integration |
---
## 2. 不同品类案例 | Category-Specific Examples
### 💄 美妆类 | Beauty & Cosmetics
**场景**: 口红色号替换 | Lipstick Shade Replacement
```
Replace the lipstick in the first image with the lipstick from the second image, while preserving all other elements including the marble background, rose petals, golden cap, product box, shadows, and reflections.
The new lipstick should:
- Match the exact position and angle (45-degree tilt) of the original lipstick
- Maintain the same luxury lighting with soft highlights on the tube
- Keep the same size and proportions
- Integrate naturally with the existing shadows on the marble surface
- Preserve the brand logo position on the tube
Keep all background props (rose petals, perfume bottle, jewelry), text overlays, and the overall elegant beauty photography style unchanged.
```
**垫图配置** | Image Setup:
- 第一张 Image 1: 原主图(底图) Original hero image (base)
- 第二张 Image 2: 新SKU产品图(白底或纯色背景) New SKU product shot (white/clean background)
---
### 📱 3C数码类 | Electronics & Tech
**场景**: 手机颜色替换 | Phone Color Variant Replacement
```
Replace the smartphone in the first image with the smartphone from the second image, while preserving all other elements including the wooden desk background, coffee cup, notebook, wireless earbuds, plant, lighting setup, and composition.
The new phone should:
- Match the exact position (vertical standing with slight tilt) and size of the original phone
- Display the same screen content and interface
- Integrate naturally with the existing studio lighting and reflections on the glass surface
- Maintain the same perspective and depth of field
- Keep the same shadow cast on the wooden desk
Preserve all lifestyle props, ambient lighting, color grading, and the modern tech lifestyle photography style completely unchanged.
```
**垫图配置** | Image Setup:
- 第一张 Image 1: 原场景图(底图) Original lifestyle scene (base)
- 第二张 Image 2: 新颜色手机正面图(官方渲染图或白底图) New color phone front view (official render/white background)
---
### 🍫 食品类 | Food & Beverage
**场景**: 包装口味替换 | Packaging Flavor Replacement
```
Replace the chocolate bar package in the first image with the chocolate bar package from the second image, while preserving all other elements including the rustic wooden table, scattered cocoa beans, cinnamon sticks, coffee cup, fabric texture, and natural lighting.
The new package should:
- Match the exact position (centered, slightly angled) and size of the original package
- Maintain the same lighting with natural shadows from the window light
- Integrate seamlessly with the surrounding cocoa beans and props
- Keep the same depth and perspective in the composition
- Preserve any existing reflections or highlights on the package surface
Keep all food styling elements (cocoa beans arrangement, cinnamon sticks, coffee steam), background texture, warm color tone, and artisanal food photography aesthetic unchanged.
```
**垫图配置** | Image Setup:
- 第一张 Image 1: 原美食场景图(底图) Original food styling scene (base)
- 第二张 Image 2: 新口味包装正面图(干净背景) New flavor package front view (clean background)
---
### 👗 服装类 | Fashion & Apparel
**场景**: 服装款式替换 | Garment Style Replacement
```
Replace the dress worn by the model in the first image with the dress from the second image, while preserving all other elements including the model's pose, body position, facial expression, hairstyle, background setting, lighting, and all accessories (shoes, jewelry, bag).
The new dress should:
- Fit naturally on the model's body following the same pose and body contours
- Match the fabric draping and movement suggested by the pose
- Integrate with the existing studio lighting and shadows on the fabric
- Maintain the same garment length and silhouette proportion
- Preserve the color harmony with existing accessories
Keep the model's appearance, pose, background (studio/outdoor setting), all styling elements, and the overall fashion editorial photography style completely unchanged.
```
**垫图配置** | Image Setup:
- 第一张 Image 1: 原模特穿搭图(底图) Original model wearing scene (base)
- 第二张 Image 2: 新款服装平铺图或模特正面图(白底) New garment flat lay or front model shot (white background)
---
## 3. 多步替换策略 | Multi-Step Replacement Strategies
### 🟢 简单替换 | Simple Replacement
**适用场景** | Use Cases: 产品位置居中、背景简洁、光影简单 | Centered product, clean background, simple lighting
**策略** | Strategy:
- **单次调用** One-shot call
- **2张图** 2 images: 底图 + 新SKU图 | Base + New SKU
- **Prompt重点** Focus: 强调位置和尺寸匹配 | Emphasize position & size matching
```
Replace the [product] in the first image with the [product] from the second image, keeping the same position, size, and background unchanged.
```
---
### 🟡 复杂替换 | Complex Replacement
**适用场景** | Use Cases: 多个道具、复杂光影、特殊角度、反射/阴影明显 | Multiple props, complex lighting, special angles, prominent reflections/shadows
**策略** | Strategy:
- **单次调用(详细Prompt)** One-shot with detailed prompt
- **2-3张图** 2-3 images: 底图 + 新SKU图 + (可选)光影参考图 | Base + New SKU + (Optional) lighting reference
- **Prompt重点** Focus: 详细列出保留元素,明确光影融合要求 | List all preserved elements, specify lighting integration
```
Replace the [product] in the first image with the [product] from the second image, while preserving all other elements including [detailed list: specific props, text, shadows, reflections, background texture].
The new product should:
- Match the exact [specific angle/position description]
- Integrate naturally with [specific lighting description: direction, softness, color temperature]
- Maintain [specific shadow/reflection details]
- Preserve [specific compositional elements]
Keep [specific style elements] unchanged.
```
**可选增强** | Optional Enhancement:
- 如果首次结果不理想,可进行二次微调 | If first result unsatisfactory, perform secondary refinement
- 使用首次生成图作为新底图,调整Prompt聚焦问题区域 | Use first generation as new base, adjust prompt to focus on problem areas
---
### 🔴 批量替换 | Batch Replacement
**适用场景** | Use Cases: 同一场景需替换多个SKU(5+个变体) | Same scene, multiple SKUs (5+ variants)
**策略** | Strategy:
- **模板化流程** Templated workflow
- **标准化垫图** Standardized image setup: 统一底图 + 标准化SKU图(相同角度/光照) | Unified base + standardized SKU shots (same angle/lighting)
- **Prompt模板** Prompt template: 固定结构,仅替换产品描述变量 | Fixed structure, only swap product description variables
**批量Prompt模板** | Batch Prompt Template:
```
Replace the [PRODUCT_CATEGORY] in the first image with the [PRODUCT_VARIANT_DESCRIPTION] from the second image, while preserving all other elements including [FIXED_PRESERVATION_LIST].
The new [PRODUCT_CATEGORY] should:
- Match the exact position [FIXED_POSITION_DESCRIPTION]
- Integrate naturally with [FIXED_LIGHTING_DESCRIPTION]
- Maintain [FIXED_SIZE_PROPORTION]
Keep [FIXED_STYLE_ELEMENTS] unchanged.
```
**变量替换示例** | Variable Replacement Example:
- `[PRODUCT_VARIANT_DESCRIPTION]`: "red lipstick" → "pink lipstick" → "nude lipstick"
- 其他部分保持不变 | All other parts remain constant
**执行方式** | Execution:
- 逐个调用工具,每次替换一个SKU | Sequential tool calls, one SKU per call
- 或使用循环结构批量处理 | Or use loop structure for batch processing
---
## 4. 垫图顺序和配置 | Image Order & Configuration
### 📐 标准配置 | Standard Configuration
#### **双图模式 (最常用)** | Two-Image Mode (Most Common)
```
image_url_list: [
  "底图URL - 原完整场景图",        // Image 1: Base - Original complete scene
  "参考图URL - 新SKU产品图"        // Image 2: Reference - New SKU product shot
]
```
**Prompt中的引用方式** | Reference in Prompt:
- "the first image" = 底图(要被编辑的图) | Base image (to be edited)
- "the second image" = 参考图(新产品来源) | Reference image (new product source)
---
#### **三图模式 (复杂场景)** | Three-Image Mode (Complex Scenes)
```
image_url_list: [
  "底图URL - 原完整场景图",        // Image 1: Base - Original complete scene
  "参考图1 URL - 新SKU产品图",     // Image 2: Reference 1 - New SKU product shot
  "参考图2 URL - 光影/角度参考"    // Image 3: Reference 2 - Lighting/angle reference
]
```
**使用场景** | Use Cases:
- 新SKU图角度不完全匹配,需要额外角度参考 | New SKU angle doesn't match, need additional angle reference
- 需要特定光影效果参考 | Need specific lighting effect reference
- 产品材质/纹理需要额外参考 | Product material/texture needs additional reference
**Prompt示例** | Prompt Example:
```
Replace the product in the first image with the product from the second image, matching the angle and perspective shown in the third image. Preserve all background elements...
```
---
### 🎨 垫图质量要求 | Image Quality Requirements
| 图片类型 | 分辨率要求 | 背景要求 | 角度要求 | 光照要求 |
|---------|-----------|---------|---------|---------|
| **底图** Base | ≥1500px长边 | 完整场景 | 实际使用角度 | 实际光照 |
| **新SKU图** New SKU | ≥1000px长边 | 纯色/白底(推荐) | 尽量正面或与底图一致 | 均匀/柔和 |
| **光影参考** Lighting Ref | ≥1000px长边 | 不限 | 与目标一致 | 与目标一致 |
---
### ⚙️ 配置优化建议 | Configuration Optimization Tips
1. **底图选择** | Base Image Selection:
   - ✅ 选择光线均匀、构图清晰的主图 | Choose well-lit, clearly composed hero images
   - ✅ 避免过度后期、滤镜过重的图片 | Avoid over-edited, heavily filtered images
   - ✅ 确保原产品边缘清晰 | Ensure original product edges are clear
2. **新SKU图准备** | New SKU Image Preparation:
   - ✅ 白底或纯色背景最佳 | White or solid color background optimal
   - ✅ 产品居中、无遮挡 | Product centered, unobstructed
   - ✅ 角度尽量与底图一致(正面/侧面/45度等) | Angle matches base image (front/side/45° etc.)
   - ⚠️ 避免带水印、标签、不相关元素 | Avoid watermarks, labels, irrelevant elements
3. **顺序重要性** | Order Importance:
   - 🔴 **第一张永远是底图** | First image is ALWAYS the base
   - 🔴 Prompt中必须明确"the first image"和"the second image" | Must explicitly state "the first image" and "the second image" in prompt
   - 🔴 顺序错误会导致完全错误的结果 | Wrong order leads to completely wrong results
---
## 5. 实战检查清单 | Practical Checklist
### ✅ Prompt编写检查 | Prompt Writing Checklist
- [ ] 明确指定了"Replace...in the first image...with...from the second image" | Clearly specified "Replace...in the first image...with...from the second image"
- [ ] 列出了所有需要保留的元素(背景/道具/文字/光影) | Listed all elements to preserve (background/props/text/lighting)
- [ ] 描述了新产品的位置/尺寸/角度要求 | Described new product position/size/angle requirements
- [ ] 强调了光影/阴影/反射的自然融合 | Emphasized natural integration of lighting/shadows/reflections
- [ ] 指定了保持整体风格不变 | Specified maintaining overall style unchanged
### ✅ 垫图准备检查 | Image Preparation Checklist
- [ ] 底图分辨率足够(≥1500px) | Base image resolution sufficient (≥1500px)
- [ ] 新SKU图背景干净 | New SKU image background clean
- [ ] 图片顺序正确(底图在前) | Image order correct (base first)
- [ ] 产品角度尽量匹配 | Product angles match as much as possible
- [ ] 图片格式支持(JPG/PNG) | Image format supported (JPG/PNG)
---
## 💡 高级技巧 | Advanced Tips
1. **渐进式替换** | Progressive Replacement:
   - 复杂场景先做简化版测试 | Test simplified version first for complex scenes
   - 根据结果逐步增加细节要求 | Gradually add detail requirements based on results
2. **描述性语言** | Descriptive Language:
   - 用具体描述替代模糊词汇 | Use specific descriptions instead of vague terms
   - ❌ "好看的背景" | ❌ "nice background"
   - ✅ "木质纹理桌面,带有自然光影" | ✅ "wooden texture tabletop with natural lighting"
3. **一致性维护** | Consistency Maintenance:
   - 批量替换时保存首次成功的Prompt模板 | Save successful prompt template for batch replacements
   - 标准化新SKU图的拍摄角度和光照 | Standardize shooting angles and lighting for new SKU images
---
需要我针对您的具体产品类别生成定制化的Prompt模板吗?或者您有具体的替换案例需要优化?
Would you like me to generate a customized prompt template for your specific product category? Or do you have a specific replacement case that needs optimization?
