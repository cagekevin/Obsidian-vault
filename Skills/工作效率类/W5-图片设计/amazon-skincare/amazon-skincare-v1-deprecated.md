---
name: 亚马逊护肤品主图提示词（已废弃）
description: ⚠️ 已废弃 - 请使用 amazon-skincare.md（v2）。旧版 v1，基于 25 个预置模板生成 Amazon 护肤品主图提示词。不再维护。
deprecated: true
---

# Amazon Skincare Main Image Prompt Generator

Generates 8-9 professional English prompts for Amazon skincare product main images. Auto-selects from 25 templates based on product selling points, adapts visuals to target body area, and outputs ready-to-use prompts for gpt-image2 plus text hierarchy specs for post-processing.

**🚨 TRIGGER RULES (双模触发引擎):**
* **MODE A [TEXT INPUT]:** Activate `[PROMPT GENERATION MODE]` — generate prompts from selling point texts using 25 templates.
* **MODE B [IMAGE INPUT]:** Activate `[TEMPLATE REVERSE-ENGINEERING MODE]` — extract a new reusable template from a reference image.

<what-to-do>

## Workflow

1. **Collect user input**: product category, background choice, brand, font pairing, and selling point texts (image count = number of texts provided)
2. **Generate Mapping Plan** (MANDATORY — do NOT skip): for each selling point, match to the best template via keywords, then check Diversity & Balance before finalizing. Output a plan table first so the user can review before prompts are generated.
3. **Fill variables**: replace all `{variable}` placeholders in prompt and text hierarchy
4. **Output & Save**: English prompt + text hierarchy spec for post-processing. Save to `output/<Brand>-<Product>-Prompts.md`

### Mapping Plan (Step 2 detail — Decision Loop)

Before outputting any prompts, execute this step-by-step **Decision Loop** for each selling point and output a **Mapping Plan table**:

**1. Match:** List ALL templates whose keywords match this selling point (even loosely).

**2. Candidate List:** From matches, pick the Top 3 by priority level (High > Medium > Low). If fewer than 3 matched, take all.

**3. Balance Filter:** From the Top 3 candidates, select the one that fills the most under-represented **Balance Category** in the current set.

**4. Commit:** Write the final choice into the table and recalculate balance counts before moving to the next selling point.

Output the plan as a table with these columns:

| Image # | Selling Point (original) | Matched Template | Priority Level | Balance Category |
|---|---|---|---|---|

Then verify:
- **Diversity**: no duplicate template IDs. If collision, resolve via collision rules below.
- **Balance**: check category distribution against target — `1 product hero + 1-2 proof/data + 1-2 ingredient + 1 model + 1 usage + 1-2 comparison/benefit`. If a category is over/under-represented, adjust by swapping to a next-best template in the under-represented category.

Once the user confirms the plan (or if auto-approved), proceed to fill variables and generate full prompts.

---

## Confirmation Checklist (Skill MUST ask before generating)

When invoked, the Skill asks the user to confirm these items. Use defaults if user skips.

| # | Item | Options | Default |
|---|---|---|---|
| 1 | **Product category** | anti_aging_face / eye_care / shoulder_care / body_firming / custom (describe) | — (required) |
| 2 | **Background** | white / warm_beige / soft_pink | warm_beige |
| 3 | **Brand** | HKH / custom | HKH |
| 4 | **Font pairing** | elegant (Didot + Montserrat) / modern (Cormorant + Lato) / bold (Playfair + Raleway) / custom | elegant |
| 5 | **Count** | images to generate（张数 = 文本条数，不用问） | — (required) |
| 6 | **Selling point texts** | one text block per image | — (required) |

### Custom category handling
If the user describes a category not in the predefined 4 (e.g., "背部祛痘", "手部护理"):

**Step A — Match closest anchor:** Map to the most visually similar existing category (e.g., 手部 → body_firming) to inherit layout proportions and template compatibility.

**Step B — Auto-generate 6 dimensions:** Imitate the structure of **Target Area Visual Map** to generate each variable:
1. `{closeup}` — Describe the specific skin texture closeup for this body part (e.g., "back skin texture with acne marks")
2. `{model_focus}` — Describe the ideal model visual for this area (e.g., "woman's smooth, clear back")
3. `{problem_visual}` — Describe the problem state the user wants to solve (e.g., "woman with back acne and red inflammation")
4. `{improvement_visual}` — Describe the improved result after using the product (e.g., "woman with clear, smooth, acne-free back")
5. `{application_area}` — Name the target body area plainly (e.g., "back")
6. `{application_verb}` — Describe the application action naturally (e.g., "smooth onto back")
7. `{problem_terms}` — List 5-7 problem-specific keywords (e.g., "back acne, body breakouts, dark spots, rough skin, redness, clogged pores, uneven texture")

**Step C — Confirm with user:** Present the auto-generated variables and ask: "These are AI-generated based on `[closest category]`. Revise any that don't match your product."

---

## Global Variables

**Default Settings & Overrides:**
- 默认品牌为 HKH，配色为 gold/dark red-brown，字体搭配为 elegant。
- 若用户有特殊指定，必须优先尊重用户的覆盖指令 (User overrides take precedence).

### Brand & style (user can override)
| Variable | Default |
|---|---|
| `{brand}` | HKH |
| `{aesthetic}` | luxury, professional, clinical, trustworthy |
| `{lighting}` | soft studio lighting |

### Background (per-image rule)
| Image | Background | Rule |
|---|---|---|
| **#1** (product_main) | `pure white background` | **强制白底**，Amazon 主图合规 |
| **#2–#N** | user's selected background (`warm_beige` / `white` / `soft_pink`) | 按用户确认清单的选项 |

### Product form (per-template, NOT global)
Each template describes its own product appearance. Common options:
| Option | Visual description |
|---|---|
| `{packaging_jar}` | transparent glass jar filled with golden capsules, golden cap |
| `{capsule_form}` | single golden capsule |
| `{capsule_cut_open}` | single golden capsule cut open revealing light golden oil texture |
| `{no_product}` | no product in frame (texture closeups, lifestyle scenes) |

> Templates pick the form that fits their purpose. Do NOT uniformly apply one form across all images.

### Font Pairing Options (user picks ONE)

POST-PROCESSING specs for Photoshop/Canva. Do NOT include in AI prompts.

| Pairing | Title (Serif, bold) | Subtitle (Serif) | Body (Sans-serif) | Use case |
|---|---|---|---|---|
| **elegant** (default) | Didot | Didot, regular | Montserrat | Classic luxury, matches HKH style |
| **modern** | Cormorant Garamond | Cormorant, regular | Lato | Cleaner, more contemporary |
| **bold** | Playfair Display | Playfair, regular | Raleway | Stronger presence, younger audience |

### Global Text Colors (applies to ALL font pairings)

| Element | Color | Hex |
|---|---|---|
| Title / Subtitle / Body | dark red-brown | #4A1A1A |
| Data numbers (large %) | gold | #C8A45C |
| Data arrows (↑↓) | gold | #C8A45C |
| Section labels (e.g., "Top Note") | gold | #C8A45C |
| Disclaimer / fine print | grey | #999999 |
| Certification badge | SGS logo, bottom corner | — |
| Brand logo | HKH, gold, serif | #C8A45C |


### Quality Constraints (专业摄影约束逻辑)

Applied to prompts that involve the relevant element. These are mandatory triggers.

| Constraint | Apply when | Wording (High-End Photographic) |
|---|---|---|
| **Model** | image contains a person | "Editorial lifestyle photography, refined skin texture, natural expression, shot on 85mm prime lens, high-end skincare model" |
| **Photorealism** | all images | "Masterpiece, Phase One IQ4 clarity, intricate texture details, cinematic composition, premium skincare aesthetic" |
| **Edge highlights** | products visible | "Crisp rim lighting, defined glossy specular highlights, volumetric contours" |
| **Lighting match** | all images | "Cohesive studio environment, global illumination, unified light temperature, seamless product-environment integration" |

> Do NOT force a model into images that don't need one (e.g., texture closeups, data charts, ingredient diagrams).

### Target Area Visual Map (drives all body-part-specific visual descriptions)

| Variable | anti_aging_face | eye_care | shoulder_care | body_firming |
|---|---|---|---|---|
| `{closeup}` | facial skin texture | eye area skin texture | shoulder and décolletage skin texture | body skin texture |
| `{model_focus}` | woman's face with radiant skin | close-up of beautiful blue eye | woman with elegant, smooth shoulders | woman with toned, smooth body |
| `{problem_visual}` | woman with wrinkles and fine lines | woman with puffy, tired eyes | woman with tense, sagging shoulder and neck area | woman with loose, sagging skin |
| `{improvement_visual}` | woman with smooth, youthful skin | woman with radiant, refreshed eyes | woman with firm, lifted shoulders and neck | woman with firm, tightened skin |
| `{application_area}` | face | eye contour | shoulder and neck | body |
| `{application_verb}` | massage onto face | gently pat around eye area | massage onto shoulder and neck area | massage onto target body area |
| `{problem_terms}` | wrinkles, fine lines, crow's feet, forehead lines, nasolabial folds, neck lines | puffy eyes, dark circles, crow's feet, eye bags, eye wrinkles | sagging shoulders, neck lines, décolletage wrinkles, rough shoulder skin, uneven texture | sagging skin, cellulite, stretch marks, loss of firmness, uneven texture |

> **For custom categories** (hair, hands, lips, acne, whitening, etc.): At confirmation time, ask the user to describe `{closeup}`, `{model_focus}`, `{problem_visual}`, `{improvement_visual}`, `{application_area}`, `{application_verb}` in their own words, or AI auto-generates from the closest existing category.

---

## 🔵 MODE B: TEMPLATE REVERSE-ENGINEERING MODE (智能查重与提取)

当用户上传参考图时，**严禁直接提取**，必须按以下逻辑闭环执行：

**Step 1: 模板库对比门禁 (Conflict Detection)**
1. **语义特征提取**: 分析用户上传图片的视觉类型（如：Before/After 对比、成分连线、临床数据图等）。
2. **已有库比对**: 将此类型与现有的 25 个模板（`<templates>` 区域）进行强匹配。
3. **决策树**:
    * **若存在功能相似的模板 (Collision Found)**: 
        - 必须停止提取。
        - 告知用户："检测到库中已存在功能相似的模板（例如：#3 before_after_two_panel）。是否要升级现有模板以适配新风格？(Y/N)" 若选 Y，则进行更新，不新增 ID。
    * **若属于完全全新的功能类别或用户确认继续**: 
        - 输出一个可以直接追加到 `<templates>` 库的代码块：

> **✅ 已识别：新风格！已为你提取亚马逊模板：**
> 
> `### #{新编号} — {英文类别名}`
> `**Match**: {提取关键词，如：absorption, penetrate, tech}`
> `**Layout**: {描述产品与文字的空间位置关系}`
> `**Text hierarchy**:`
> `Layer 1 ({位置}, {字号}, {颜色}): {文字变量}`
> `Layer 2 ({位置}, {字号}, {颜色}): {文字变量}`
> `...`
> `**AI prompt**:`
> `{标准化 Prompt，保留 {variable} 占位符}`

</what-to-do>

<supporting-info>

## Template Selection Rules

For each selling point text, match keywords to template. Apply in priority order:

| Priority | If text contains... | Use template |
|---|---|---|
| Always | product/产品/包装/set/box/accessories | #1 product_main |
| High | `%` + clinical/improvement/SGS/proven | #6 clinical_data_showcase |
| High | `%` + agree/satisfaction/participants/survey | #7 user_satisfaction_stats |
| High | Before/After/对比/results/transformation/改善/前后 | #3 before_after_two_panel |
| High | 28/56/week/天/周/timeline/progressive/day | #4 before_after_three_panel |
| High | day 1/day 28/clinical/grid/四格 | #5 clinical_four_panel_grid |
| Medium | ingredient/成分/配方/formula/contains/squalane/oil/extract | #8 ingredient_connection_diagram |
| Medium | botanical/plant/植物/花/seed/petri/培养皿/天然/natural | #9 botanical_ingredient_cards |
| Medium | benefit/功效/作用/icon/图标/dermatologist tested | #10 ingredient_benefit_icons |
| Medium | rare/cold-pressed/virgin/稀有/冷压/植物油/seed oil/jojoba/baobab | #11 rare_plant_oils |
| Medium | source/origin/harvested/来源/产地/野生/wild/Mediterranean | #12 plant_source_origin |
| Medium | fragrance/scent/香调/note/前调/中调/后调/aroma | #13 fragrance_notes |
| Medium | model/woman/模特/beautiful/elegant/portrait/人像/lifestyle | #14 model_with_product |
| Medium | sensitive/敏感/dermatologist approved/non-irritating/gentle/温和/safe | #15 sensitive_skin_certification |
| Medium | non-greasy/不油腻/fresh/清爽/lightweight/吸收快/absorb | #16 non_greasy_formula |
| Medium | step/步骤/how to/使用方法/twist/squeeze/apply/涂抹/按摩 | #17 three_step_usage |
| Low | massage tool/按摩工具/wand/棒/roller/刮痧 | #18 massage_tool_demo |
| Low | layer/搭配/routine/add to/foundation/moisturizer/mix/混合 | #19 skincare_layering_guide |
| Low | vs/versus/对比/比较/traditional/ordinary/better than/优于 | #20 product_comparison_table |
| Low | botox/injection/needle/肉毒/注射/针剂/non-invasive/无创 | #21 botox_injection_alternative |
| Low | doctor/dermatologist/医生/专家/皮肤科/recommended/推荐 | #22 doctor_endorsement |
| Low | absorption/penetrate/dermis/吸收/渗透/深层/skin layer/tech | #23 technology_skin_layer |
| Low | patent/专利/certificate/证书 | #24 patent_certificate |
| Low | scenario/场景/lifestyle/travel/spa/night/morning/旅行 | #25 lifestyle_scenarios |
| Low | pour/liquid/golden/drop/倒/液体/concentration | #2 floating_product_pour |
| Fallback | none of the above | #14 model_with_product |

**Diversity rule**: Avoid two very similar templates in one set. If duplicate match, pick next-best.

**Balance target per 8-9 image set**: 1 product hero + 1-2 proof/data + 1-2 ingredient + 1 model + 1 usage + 1-2 comparison/benefit.

**Keyword collision resolution** (when one selling point hits multiple same-priority templates):
1. Map all matching templates for that selling point.
2. Cross-check against the current Mapping Plan: which matching template fills an under-represented balance category?
3. If still tied, prefer the template with the **most specific** keyword match (e.g., an exact "前调" match beats a generic "fragrance" match).
4. If none of the above resolves it, pick the first matching template in table order.

**Template category mapping** (for balance tracking):

| Balance Category | Templates |
|---|---|
| Product Hero | #1, #2 |
| Proof / Data | #3, #4, #5, #6, #7 |
| Ingredient / Fragrance | #8, #9, #10, #11, #12, #13 |
| Model / Lifestyle | #14, #25 |
| Usage / How-to | #17, #18, #19 |
| Comparison / Benefit | #15, #16, #20, #21, #22, #23, #24 |

---

## 25 Templates

Each template includes: match keywords, layout description, text hierarchy (for post-processing), and AI prompt (for gpt-image2).

### #1 — product_main (产品主图)

**Match**: product, 产品, 主图, 包装, 全套, set, box, accessories

**Layout**: product centered, surrounded by accessories (box, massage tool, scissors, flower, serum smear)

**Text hierarchy** (post-processing):
```
Layer 1 (top, small, gold sans-serif)      : top_label (e.g., "4VA")
Layer 2 (center, medium, dark red-brown serif bold): brand_name (e.g., "HKH")
Layer 3 (center below, large, dark red-brown serif): product_name
Layer 4 (bottom, small, dark red-brown sans-serif) : package_description
```

**AI prompt**:
```
luxury skincare {form} set, {packaging}, product box, golden massage tool, small scissors, white flower, serum smear with bubbles, {background}, professional product photography, {lighting}, {aesthetic}
```

---

### #2 — floating_product_pour (漂浮倒液图)

**Match**: pour, liquid, golden, 倒, 液体, 滴落, drop, 高浓度, concentration

**Layout**: tilted product bottle with golden liquid pouring from top, serum drop falling from bottom

**Text hierarchy** (post-processing):
```
Layer 1 (top, small, dark red-brown sans-serif)   : top_label
Layer 2 (mid-top, large, caps, dark red-brown serif bold): title (e.g., "ANTI-AGING")
Layer 3 (below title, medium, dark red-brown serif): subtitle
Layer 4 (mid, small, dark red-brown sans-serif)    : body_description
Layer 5 (bottom, small, dark red-brown sans-serif) : benefits_list with + marks
```

**AI prompt**:
```
tilted {packaging}, golden liquid pouring from top, a single serum drop falling from bottom with subtle golden splashes, {background}, professional product photography, {lighting}, {aesthetic}, dynamic liquid motion
```

---

### #3 — before_after_two_panel (Before/After两格对比)

**Match**: before, after, 对比, 前后, results, 效果, visible, transformation, 改善

**Layout**: two-panel side-by-side comparison with SGS logo and percentage data

**Text hierarchy** (post-processing):
```
Layer 1 (top center, large, dark red-brown serif bold): title
Layer 2 (below title, medium, dark red-brown serif)    : subtitle
Layer 3 (left panel, medium, dark red-brown sans-serif) : left_label (e.g., "Before")
Layer 4 (right panel, medium, dark red-brown sans-serif): right_label (e.g., "After")
Layer 5 (between panels, large numbers, gold, bold)     : data_points with ↑↓ arrows
Layer 6 (bottom corner, small)                          : SGS certification logo
```

**AI prompt**:
```
two-panel before and after comparison, left side: {problem_visual}, right side: {improvement_visual}, SGS certification logo, percentage improvement data with golden arrows, {background}, professional cosmetic photography, {lighting}, {aesthetic}
```

---

### #4 — before_after_three_panel (Before/After三格时间线)

**Match**: 28, 56, week, 天, 周, timeline, progressive, 逐渐, 时间, day

**Layout**: three vertical panels showing progression over time

**Text hierarchy** (post-processing):
```
Layer 1 (panel 1, medium, dark red-brown sans-serif): "Before"
Layer 2 (panel 2, medium, dark red-brown sans-serif): "After 28 Days"
Layer 3 (panel 3, medium, dark red-brown sans-serif): "After 56 Days"
```

**AI prompt**:
```
three-panel vertical before and after timeline, panel 1: {problem_visual} labeled "Before", panel 2: woman with visibly improved skin holding product labeled "After 28 Days", panel 3: woman with glowing transformed skin smiling confidently labeled "After 56 Days", {background}, professional cosmetic photography, {lighting}, {aesthetic}
```

---

### #5 — clinical_four_panel_grid (四格临床对比)

**Match**: day 1, day 28, clinical, 临床, before after, grid, 四格, 对比区域

**Layout**: four-panel grid showing different areas before and after

**Text hierarchy** (post-processing):
```
Layer 1 (each panel top, small, dark red-brown sans-serif): "DAY 1" / "DAY 28"
Layer 2 (each panel, large numbers, gold bold)             : percentage_change
Layer 3 (bottom, small)                                    : SGS logo
```

**AI prompt**:
```
four-panel grid of clinical before and after comparisons, each panel showing skin texture closeup with DAY 1 and DAY 28 labels, SGS logo, {background}, professional medical photography, {lighting}, clinical precision, {aesthetic}
```

---

### #6 — clinical_data_showcase (临床数据特写)

**Match**: %, SGS, clinically, proven, 临床, 数据, improvement, increase, reduction, decrease, test, 测试

**Layout**: skin texture closeup with data overlay

**Text hierarchy** (post-processing):
```
Layer 1 (top, large, dark red-brown serif bold)  : title (e.g., "SGS CLINICALLY PROVEN")
Layer 2 (below, medium, dark red-brown serif)     : subtitle
Layer 3 (scattered, large numbers, gold bold)      : data_values with ↑↓ arrows
Layer 4 (below each number, small, dark red-brown sans-serif): data_labels
Layer 5 (bottom corner)                            : SGS logo
```

**AI prompt**:
```
extreme close-up of {closeup} with moisturizing serum drops on skin surface, SGS certification logo, large percentage improvement numbers with golden arrows, {background}, professional medical photography, {lighting}, clinical grade detail, {aesthetic}
```

---

### #7 — user_satisfaction_stats (用户满意度统计)

**Match**: %, agree, satisfaction, participants, 满意度, 用户, 测试者, survey, consumer

**Layout**: product on right, large percentage stats on left

**Text hierarchy** (post-processing):
```
Layer 1 (left, very large, gold bold numbers)      : percentage_values (e.g., "96.9%")
Layer 2 (below each number, small, dark red-brown sans-serif): description_text
Layer 3 (small icons)                               : day/night icons (sun and moon)
```

**AI prompt**:
```
product placed on elegant marble surface on the right side, day and night icons (sun and moon), large bold percentage statistics on the left, {background}, professional product photography, {lighting}, {aesthetic}
```

---

### #8 — ingredient_connection_diagram (成分连线图)

**Match**: ingredient, 成分, 连线, 配方, formula, contains, 含有, squalane, oil, extract

**Layout**: product with serum smear on right, ingredient labels with connecting lines on left

**Text hierarchy** (post-processing):
```
Layer 1 (top left, large, dark red-brown serif bold): title_top
Layer 2 (below, large, dark red-brown serif)         : title_main
Layer 3 (left side, medium, dark red-brown sans-serif): ingredient_names (connected by lines)
Layer 4 (below each name, small, dark red-brown sans-serif): ingredient_descriptions
```

**AI prompt**:
```
skincare ingredient composition diagram, {capsule_form} with serum texture smear on the right, connecting line indicators to ingredient labels on the left, floating serum bubbles, {background}, professional cosmetic photography, {lighting}, clean infographic style, {aesthetic}
```

---

### #9 — botanical_ingredient_cards (植物配料卡片)

**Match**: botanical, plant, 植物, 花, seed, petri, 培养皿, 天然, natural, extract

**Layout**: three petri dishes with botanicals on left, four ingredient cards on right

**Text hierarchy** (post-processing):
```
Layer 1 (top, large, dark red-brown serif bold)   : title_top
Layer 2 (below, large, dark red-brown serif)       : title_main
Layer 3 (each card, medium, dark red-brown sans-serif bold): ingredient_name
Layer 4 (below name, small, dark red-brown sans-serif)     : ingredient_description
Layer 5 (each card, small)                                 : ingredient_icon
```

**AI prompt**:
```
botanical ingredients display, three glass petri dishes with delicate flowers and seeds on the left, four elegant ingredient information cards on the right with small icons, {background}, professional cosmetic photography, {lighting}, scientific botanical aesthetic, {aesthetic}
```

---

### #10 — ingredient_benefit_icons (成分功效图标)

**Match**: benefit, 功效, 作用, 效果, icon, 图标, dermatologist, tested, ingredient list, 成分列表

**Layout**: text on left, golden liquid texture on right, benefit icons

**Text hierarchy** (post-processing):
```
Layer 1 (top, large, dark red-brown serif bold)   : title
Layer 2 (left, medium, dark red-brown sans-serif)  : benefit_texts (each with an icon)
Layer 3 (left bottom, small)                       : ingredient badges
```

**AI prompt**:
```
skincare ingredient benefit information, golden liquid serum texture flowing on the right side, elegant benefit icons with labels on the left, {background}, professional cosmetic photography, {lighting}, clean information design, {aesthetic}
```

---

### #11 — rare_plant_oils (稀有植物油)

**Match**: rare, cold-pressed, virgin, 稀有, 冷压, 植物油, plant oil, seed oil, jojoba, baobab, macadamia

**Layout**: golden liquid texture background with ingredient illustrations in bubbles

**Text hierarchy** (post-processing):
```
Layer 1 (top, large, dark red-brown serif bold)   : title
Layer 2 (each bubble, medium, dark red-brown sans-serif bold): ingredient_name
Layer 3 (below name in bubble, small)                        : ingredient_description
```

**AI prompt**:
```
luxurious golden liquid texture background, rare plant oil ingredient illustrations floating in translucent bubbles with connecting labels, {background}, professional cosmetic photography, {lighting}, premium natural aesthetic, {aesthetic}
```

---

### #12 — plant_source_origin (植物来源图)

**Match**: source, origin, harvested, 来源, 产地, 野生, wild, Mediterranean, 天然来源, natural source, plant photo

**Layout**: white-framed plant photograph on left, text area on right

**Text hierarchy** (post-processing):
```
Layer 1 (right top, large, dark red-brown serif bold): title
Layer 2 (right, medium, dark red-brown serif)         : section1_title
Layer 3 (below, small, dark red-brown sans-serif)     : section1_body
Layer 4 (right, medium, dark red-brown serif)         : section2_title
Layer 5 (below, small, dark red-brown sans-serif)     : section2_body
```

**AI prompt**:
```
elegant white-framed photograph of the source plant growing in its pristine natural habitat on the left side, text description area on the right, {background}, professional editorial photography, {lighting}, natural botanical aesthetic, {aesthetic}
```

---

### #13 — fragrance_notes (香调说明图)

**Match**: fragrance, scent, 香调, 香味, note, 前调, 中调, 后调, top note, middle note, base note, aroma

**Layout**: product with large flower on left, fragrance notes on right

**Text hierarchy** (post-processing):
```
Layer 1 (top, large, dark red-brown serif bold)    : title
Layer 2 (right, medium, gold sans-serif bold)       : "Top Note"
Layer 3 (below, small, dark red-brown sans-serif)   : top_note_items
Layer 4 (right, medium, gold sans-serif bold)       : "Middle Note"
Layer 5 (below, small, dark red-brown sans-serif)   : middle_note_items
Layer 6 (right, medium, gold sans-serif bold)       : "Base Note"
Layer 7 (below, small, dark red-brown sans-serif)   : base_note_items
```

**AI prompt**:
```
{packaging} with a large blooming flower beside it on the left, floating petals scattered elegantly, fragrance notes structure on the right, {background}, professional product photography, {lighting}, romantic luxurious aesthetic, {aesthetic}
```

---

### #14 — model_with_product (模特+产品)

**Match**: model, woman, 模特, 女性, beautiful, elegant, portrait, 人像, lifestyle

**Layout**: model on one side, product on the other

**Text hierarchy** (post-processing):
```
Layer 1 (opposite model, large, dark red-brown serif bold) : title
Layer 2 (below, medium, dark red-brown serif)               : subtitle
Layer 3 (below, small, dark red-brown sans-serif)           : feature_list (with checkmark bullets)
```

**AI prompt**:
```
beautiful woman, {model_focus}, elegant pose looking at camera, {packaging} placed beside her with scattered golden capsules, {background}, professional cosmetic photography, {lighting}, aspirational lifestyle aesthetic, {aesthetic}
```

---

### #15 — sensitive_skin_certification (敏感肌认证)

**Match**: sensitive, 敏感, dermatologist, approved, non-irritating, 无刺激, gentle, 温和, safe, 安全, allergy

**Layout**: model holding product on right, four certification icon cards on left

**Text hierarchy** (post-processing):
```
Layer 1 (top left, small, dark red-brown sans-serif)       : top_label
Layer 2 (below, large, dark red-brown serif bold)           : title
Layer 3 (each card, medium, dark red-brown sans-serif bold) : claim_title
Layer 4 (below each title, small, dark red-brown sans-serif): claim_description
Layer 5 (each card, small)                                  : icon (water-drop, skin, shield, prohibition)
```

**AI prompt**:
```
blonde woman in white blazer holding product on the right, four elegant certification icon cards on the left (water drop, skin shield, checkmark, prohibition symbol), {background}, professional cosmetic photography, {lighting}, clean medical aesthetic, {aesthetic}
```

---

### #16 — non_greasy_formula (不油腻配方)

**Match**: non-greasy, 不油腻, fresh, 清爽, lightweight, 轻透, absorption, absorb, 吸收快

**Layout**: model applying product, floating capsules and stats

**Text hierarchy** (post-processing):
```
Layer 1 (top left, large, dark red-brown serif bold): title
Layer 2 (left, very large, gold bold numbers)        : percentage_stats
Layer 3 (below numbers, small, dark red-brown sans-serif): stat_descriptions
Layer 4 (bottom, very small, grey sans-serif)         : disclaimer
```

**AI prompt**:
```
woman gracefully applying serum to her {application_area} on the right, three golden capsules floating on the left, large percentage satisfaction data displayed, {background}, professional cosmetic photography, {lighting}, fresh luxurious aesthetic, {aesthetic}
```

---

### #17 — three_step_usage (三步使用法)

**Match**: step, 步骤, how to, 使用方法, twist, squeeze, apply, 打开, 涂抹, 按摩, massage

**Layout**: three horizontal panels showing sequential steps

**Text hierarchy** (post-processing):
```
Layer 1 (each panel, large, gold bold numbers)          : "01" / "02" / "03"
Layer 2 (each panel below number, medium, dark red-brown sans-serif): step_description
```

**AI prompt**:
```
three-step usage demonstration in horizontal panels, step 1: hands twisting open golden capsule, step 2: hand squeezing serum into palm, step 3: hands gently massaging onto {application_area}, {background}, professional cosmetic photography, {lighting}, instructional clean aesthetic, {aesthetic}
```

---

### #18 — massage_tool_demo (按摩工具演示)

**Match**: massage, tool, 按摩, 工具, wand, 棒, roller, 刮痧, guasha

**Layout**: four-panel grid showing massage tool on different areas

**Text hierarchy** (post-processing):
```
Layer 1 (each panel, small, dark red-brown sans-serif): area_label (cheekbone, jawline, under-eye, forehead)
```

**AI prompt**:
```
four-panel grid showing golden facial massage wand being used on different facial areas (cheekbone, jawline, under-eye, forehead), {background}, professional cosmetic photography, {lighting}, instructional aesthetic, {aesthetic}
```

---

### #19 — skincare_layering_guide (护肤品搭配指南)

**Match**: layer, 搭配, routine, add to, foundation, moisturizer, mix, 混合, 叠加, 日常

**Layout**: three-panel grid showing product combination methods

**Text hierarchy** (post-processing):
```
Layer 1 (top, small, dark red-brown sans-serif)     : top_label
Layer 2 (below, large, dark red-brown serif bold)    : title
Layer 3 (each panel, medium, dark red-brown sans-serif bold): panel_title
Layer 4 (below title, small, dark red-brown sans-serif)     : panel_description
```

**AI prompt**:
```
three-panel grid showing skincare layering methods, panel 1: hand mixing serum with foundation, panel 2: hand adding serum to moisturizer bottles, panel 3: woman using rose quartz facial roller, {background}, professional cosmetic photography, {lighting}, lifestyle beauty aesthetic, {aesthetic}
```

---

### #20 — product_comparison_table (产品对比表)

**Match**: vs, versus, 对比, 比较, traditional, ordinary, 普通, 传统, better than, 优于, 替代, alternative, competitor

**Layout**: two-column or three-column comparison layout

**Text hierarchy** (post-processing):
```
Layer 1 (left column top, medium, grey sans-serif bold)    : competitor_product_name
Layer 2 (left column, small, grey sans-serif)              : competitor_points (with X marks)
Layer 3 (middle column, large, gold serif bold)            : "VS"
Layer 4 (middle column, small, dark red-brown sans-serif) : comparison_criteria
Layer 5 (right column top, medium, dark red-brown serif bold): hero_product_name
Layer 6 (right column, small, dark red-brown sans-serif)   : hero_product_points (with checkmarks)
Layer 7 (right column, small, gold sans-serif)             : hero_subtitle
```

**AI prompt**:
```
product comparison layout, left side: competitor product on grey background with X marks, right side: {packaging} on golden pedestal with warm beige background and check marks, {background}, professional product photography, {lighting}, comparison infographic style, {aesthetic}
```

---

### #21 — botox_injection_alternative (注射替代方案)

**Match**: botox, injection, needle, 肉毒, 注射, 针剂, fillers, 整形, non-invasive, 无创

**Layout**: split comparison - injections vs natural serum, with model face

**Text hierarchy** (post-processing):
```
Layer 1 (left side, medium, grey sans-serif bold)       : injection_label
Layer 2 (left side, small, grey sans-serif)             : injection_warnings
Layer 3 (right side, medium, dark red-brown serif bold) : serum_label
Layer 4 (right side, small, dark red-brown sans-serif)  : serum_benefits
Layer 5 (scattered, large, gold numbers)                : percentage_data
Layer 6 (bottom)                                        : SGS logo
```

**AI prompt**:
```
split comparison layout, left side: syringe with warning triangle on dark background representing injections, right side: {capsule_form} on golden pedestal with warm background, model face with serum droplets evenly distributed on skin, SGS logo, {background}, professional cosmetic photography, {lighting}, {aesthetic}
```

---

### #22 — doctor_endorsement (医生推荐)

**Match**: doctor, dermatologist, ophthalmologist, 医生, 专家, 皮肤科, recommended, 推荐, endorsed, white coat

**Layout**: doctor on one side, product claims on the other

**Text hierarchy** (post-processing):
```
Layer 1 (opposite doctor, large, dark red-brown serif bold): title
Layer 2 (below, medium, dark red-brown sans-serif)          : endorsement_claims (with checkmark bullets)
Layer 3 (below, large, gold bold numbers)                   : percentage_data
Layer 4 (bottom, small)                                     : doctor_signature
```

**AI prompt**:
```
professional doctor in white coat with arms crossed and confident expression on one side, {packaging} with percentage efficacy data and signature on the other side, {background}, clinical photography style, professional medical aesthetic, {lighting}, {aesthetic}
```

---

### #23 — technology_skin_layer (技术皮肤层说明)

**Match**: absorption, penetrate, dermis, 吸收, 渗透, 深层, layer, skin layer, 技术, tech, delivery, 表皮

**Layout**: capsule on left, skin layer diagram and absorption chart on right

**Text hierarchy** (post-processing):
```
Layer 1 (right diagram, small, dark red-brown sans-serif): skin_layer_labels
Layer 2 (right chart, small, dark red-brown sans-serif)  : chart_annotations
Layer 3 (right chart, medium, gold numbers)              : percentage_data
```

**AI prompt**:
```
{capsule_form} with visible absorption effect on the left, cross-section skin layer diagram showing deep dermis penetration on the right with absorption rate chart, {background}, clinical infographic style, professional medical illustration, {lighting}, {aesthetic}
```

---

### #24 — patent_certificate (专利证书展示)

**Match**: patent, 专利, certificate, 证书, 认证, registered, 专利技术

**Layout**: patent certificate on display stand with product

**Text hierarchy** (post-processing):
```
Layer 1 (certificate, small, dark red-brown serif): patent_details
Layer 2 (around product, small, dark red-brown sans-serif): benefit_icon_labels
```

**AI prompt**:
```
official patent certificate on elegant display stand, {capsule_form} placed beside it with circular benefit icons, {background}, professional product photography, {lighting}, authoritative aesthetic, {aesthetic}
```

---

### #25 — lifestyle_scenarios (生活场景)

**Match**: scenario, 场景, lifestyle, travel, spa, night, morning, 旅行, 夜间, 日常, daily, 随身

**Layout**: three-panel vertical grid showing usage occasions

**Text hierarchy** (post-processing):
```
Layer 1 (each panel, medium, dark red-brown sans-serif): scenario_label
```

**AI prompt**:
```
three-panel vertical grid of lifestyle scenarios, panel 1: overnight repair with soft bedroom lighting, panel 2: travel with product in elegant travel bag, panel 3: spa relaxation with candles and white towel, {background}, warm lifestyle photography, {lighting}, {aesthetic}
```

---

## Variable Reference

| Placeholder | Source | Example value |
|---|---|---|
| `{background}` | user's background choice | warm beige to light brown gradient background |
| `{form}` | product form | serum / cream / balm |
| `{packaging}` | product packaging | transparent glass jar with golden cap |
| `{capsule_form}` | capsule description | golden capsule |
| `{capsule_cut_open}` | capsule cut open | single golden capsule cut open revealing light golden oil texture |
| `{no_product}` | no product in frame | no product (texture closeups, lifestyle scenes) |
| `{lighting}` | fixed global | soft studio lighting |
| `{aesthetic}` | fixed global | luxury, professional, clinical, trustworthy |
| `{closeup}` | target area map | facial skin texture |
| `{model_focus}` | target area map | woman's face with radiant skin |
| `{problem_visual}` | target area map | woman with wrinkles and fine lines |
| `{improvement_visual}` | target area map | woman with smooth, youthful skin |
| `{application_area}` | target area map | face |
| `{application_verb}` | target area map | massage onto face |
| `{problem_terms}` | target area map | wrinkles, fine lines, crow's feet |

---

## Output Format

For each image, output:

```
**Image #N | Template: {name_cn} (#{id})**

**Prompt:** {filled prompt in English}

**Text layers:** {filled text hierarchy with user's actual text placed in each layer}

---
```

---

## Important Rules

- **Confirmation first**: Always go through the 6-item checklist before generating any prompts
- **Mapping Plan first**: Before outputting any prompts, output a Mapping Plan table (see Workflow Step 2). Never skip this step.
- **AI prompt covers only VISUAL elements** — what the camera captures (products, models, backgrounds, props, lighting). See Boundary Principle below for enforcement.
- **Text hierarchy covers POST-PROCESSING elements** — fonts, colors, layer order for Photoshop/Canva. See Boundary Principle below for enforcement.
- **AI prompts MUST be in English** (image generation models perform better with English)
- **Text layers MUST preserve the user's original language** — do NOT translate the user's selling points unless the user explicitly requests it
- **Text layers MUST contain extracted real text, NOT variable names** — extract specific wording from the user's selling points and fill into each layer (e.g., replace `percentage_data` with `"30%"`, replace `ingredient_names` with actual ingredient names). Never leave placeholder variable names in the output.
- If product form is `capsule` (not jar), exclude templates #2 (floating_pour) and #13 (fragrance_notes)
- For custom categories: follow the three-step process in **Custom Category Handling** (Step A → Step B → Step C). Do NOT skip directly to variable filling.
- Always output exactly the number of prompts the user requested (typically 8-9)
- **绝对不允许"缩水"：** 无论用户请求生成多少张图片（如 8-9 张），**每一张图的 Prompt 必须拥有完全一致的详细程度和专业摄影参数描述**。
- **禁止懒惰策略：** 严禁使用"同上"、"详见上文"或缩减 Prompt 描述等偷懒策略。即便到了第 9 张图，也必须完整输出完整的摄影术语、布光描述和材质约束。
- **强制一致性：** 模型必须将每一个 Prompt 视为一次独立的"高质量创作"，不允许在输出序列的末端降低生成质量。

### 🚨 零占位符准则 (Zero-Placeholder Rule)
在最终输出的 Prompt 和 Text layers 中，**严禁出现任何 `{}` 占位符**。如果 AI 无法从用户输入中提取到特定信息，则必须使用逻辑通顺的通用描述进行替代，而不能保留变量名。在输出每条 Prompt 前，必须进行最后检查：**是否存在 `{` 符号**。若存在，说明变量填充失败，必须重写。

### 🧱 边界准则 (Boundary Principle)
- **AI Prompt 必须是纯视觉描述** — 严禁包含任何文字内容、引号、字符、品牌名或文案。只能描述相机能拍到的东西。
- **Text Hierarchy 必须只包含文案和排版规则** — 严禁包含任何光影、构图、道具等视觉描述。只负责字体、颜色、层级顺序。
- 若不遵守此边界准则，视为指令违规，必须重写。

---

## End-to-End Example

### User says:
> 帮我做一套肩部护理的图，8张。背景用暖米色。产品是装满胶囊的玻璃罐。
> 
> 1. 4VA肩颈胶囊精华 — 专为肩颈松弛设计
> 2. 2周改善肩颈皱纹30%
> 3. 天然植物来源，地中海野生植物萃取
> 4. 前调玫瑰，中调茉莉，后调檀香
> 5. 5种活性肽协同作用
> 6. 纳米微囊技术，3秒渗透至真皮层
> 7. SGS认证，14天临床实测
> 8. 居家SPA级肩颈护理体验

### Skill confirms:
| # | Item | User choice |
|---|---|---|
| 1 | Category | shoulder_care |
| 2 | Background | warm_beige |
| 3 | Brand | HKH |
| 4 | Font | elegant (Didot + Montserrat) |
| 5 | Count | 8 |
| 6 | Texts | (8 texts above) |

### Skill outputs Mapping Plan:

| Image # | Selling Point (original) | Matched Template | Priority | Balance Category |
|---|---|---|---|---|
| 1 | 4VA肩颈胶囊精华 — 专为肩颈松弛设计 | #1 product_main | Always | Product Hero |
| 2 | 2周改善肩颈皱纹30% | #3 before_after_two_panel | High (改善/前后) | Proof / Data |
| 3 | 天然植物来源，地中海野生植物萃取 | #12 plant_source_origin | Medium (来源/产地/野生/Mediterranean) | Ingredient / Fragrance |
| 4 | 前调玫瑰，中调茉莉，后调檀香 | #13 fragrance_notes | Medium (前调/中调/后调) | Ingredient / Fragrance |
| 5 | 5种活性肽协同作用 | #8 ingredient_connection_diagram | Medium (成分/配方) | Ingredient / Fragrance |
| 6 | 纳米微囊技术，3秒渗透至真皮层 | #23 technology_skin_layer | Low (渗透/深层/skin layer) | Comparison / Benefit |
| 7 | SGS认证，14天临床实测 | #6 clinical_data_showcase | High (SGS/临床/测试) | Proof / Data |
| 8 | 居家SPA级肩颈护理体验 | #25 lifestyle_scenarios | Low (spa/场景) | Model / Lifestyle |

**Balance check**: Product Hero (1) ✓ | Proof/Data (2) ✓ | Ingredient/Fragrance (3) ✓ | Model/Lifestyle (1) ✓ | Comparison/Benefit (1) ✓
**Diversity check**: All 8 templates are unique — no duplicates. ✓

### Skill generates prompts:

**Image #1 | Template: product_main (#1)**

**Prompt:**
```
luxury skincare serum set, transparent glass jar filled with golden capsules, golden cap, product box, golden massage tool, small scissors, white flower, serum smear with bubbles, warm beige to light brown gradient background, professional product photography, soft studio lighting, luxury, professional, clinical, trustworthy
```

**Text layers:**
```
Layer 1 (top, small, gold sans-serif)      : "4VA"
Layer 2 (center, medium, dark red-brown serif bold): "HKH"
Layer 3 (center below, large, dark red-brown serif): "肩颈胶囊精华"
Layer 4 (bottom, small, dark red-brown sans-serif) : "专为肩颈松弛设计"
```
  Font pairing: elegant — Title: Didot Bold, Subtitle: Didot Regular, Body: Montserrat Regular

---

**Image #2 | Template: before_after_two_panel (#3)**

**Prompt:**
```
two-panel before and after comparison, left side: woman with tense, sagging shoulder and neck area, right side: woman with firm, lifted shoulders and neck, SGS certification logo, percentage improvement data "30%" with golden arrows, warm beige to light brown gradient background, professional cosmetic photography, soft studio lighting, luxury, professional, clinical, trustworthy
```

**Text layers:**
```
Layer 1 (top center, large, dark red-brown serif bold): "2周改善肩颈皱纹"
Layer 2 (below title, medium, dark red-brown serif)    : "临床实测对比"
Layer 3 (left panel, medium, dark red-brown sans-serif) : "使用前"
Layer 4 (right panel, medium, dark red-brown sans-serif): "使用后"
Layer 5 (between panels, large numbers, gold, bold)     : "30%↓"
Layer 6 (below data, small, dark red-brown sans-serif)  : "肩颈皱纹改善率"
Layer 7 (bottom corner, small)                          : SGS certification logo
```
  Font pairing: elegant — Title: Didot Bold, Subtitle: Didot Regular, Body: Montserrat Regular

---

**Image #3 | Template: plant_source_origin (#12)**

**Prompt:**
```
elegant white-framed photograph of wild Mediterranean plants growing in their pristine natural habitat on the left side, text description area on the right, warm beige to light brown gradient background, professional editorial photography, soft studio lighting, natural botanical aesthetic, luxury, professional, clinical, trustworthy
```

**Text layers:**
```
Layer 1 (right top, large, dark red-brown serif bold): "天然植物来源"
Layer 2 (right, medium, dark red-brown serif)         : "地中海野生植物萃取"
Layer 3 (below, small, dark red-brown sans-serif)     : "源自地中海沿岸的野生植物，手工采摘"
Layer 4 (right, medium, dark red-brown serif)         : "纯净萃取工艺"
Layer 5 (below, small, dark red-brown sans-serif)     : "先进萃取技术保留活性成分"
```
  Font pairing: elegant — Title: Didot Bold, Subtitle: Didot Regular, Body: Montserrat Regular

---

**Image #4 | Template: fragrance_notes (#13)**

**Prompt:**
```
transparent glass jar filled with golden capsules, golden cap with large blooming rose flower beside it on the left, floating petals scattered elegantly, fragrance notes structure on the right, warm beige to light brown gradient background, professional product photography, soft studio lighting, romantic luxurious aesthetic, luxury, professional, clinical, trustworthy
```

**Text layers:**
```
Layer 1 (top, large, dark red-brown serif bold)    : "香调说明"
Layer 2 (right, medium, gold sans-serif bold)       : "前调"
Layer 3 (below, small, dark red-brown sans-serif)   : "玫瑰"
Layer 4 (right, medium, gold sans-serif bold)       : "中调"
Layer 5 (below, small, dark red-brown sans-serif)   : "茉莉"
Layer 6 (right, medium, gold sans-serif bold)       : "后调"
Layer 7 (below, small, dark red-brown sans-serif)   : "檀香"
```
  Font pairing: elegant — Title: Didot Bold, Subtitle: Didot Regular, Body: Montserrat Regular

---

**Image #5 | Template: ingredient_connection_diagram (#8)**

**Prompt:**
```
skincare ingredient composition diagram, golden capsule with serum texture smear on the right, connecting line indicators to 5 peptide ingredient labels on the left, floating serum bubbles, warm beige to light brown gradient background, professional cosmetic photography, soft studio lighting, clean infographic style, luxury, professional, clinical, trustworthy
```

**Text layers:**
```
Layer 1 (top left, large, dark red-brown serif bold): "5种活性肽"
Layer 2 (below, large, dark red-brown serif)         : "协同作用配方"
Layer 3 (left side, medium, dark red-brown sans-serif): "肽-1" / "肽-2" / "肽-3" / "肽-4" / "肽-5"（连线标注）
Layer 4 (below each name, small, dark red-brown sans-serif): "紧致提升" / "淡化皱纹" / "深层修护" / "增强弹性" / "锁水保湿"
```
  Font pairing: elegant — Title: Didot Bold, Subtitle: Didot Regular, Body: Montserrat Regular

---

**Image #6 | Template: technology_skin_layer (#23)**

**Prompt:**
```
golden capsule with visible absorption effect on the left, cross-section skin layer diagram showing deep dermis penetration on the right with absorption rate chart, warm beige to light brown gradient background, clinical infographic style, professional medical illustration, soft studio lighting, luxury, professional, clinical, trustworthy
```

**Text layers:**
```
Layer 1 (right diagram, medium, dark red-brown sans-serif bold): "纳米微囊技术"
Layer 2 (right chart, large, gold bold numbers)                : "3秒"
Layer 3 (right chart, small, dark red-brown sans-serif)        : "微囊渗透至真皮层"
Layer 4 (right chart, small, dark red-brown sans-serif)        : "表皮层 → 真皮层"
```
  Font pairing: elegant — Title: Didot Bold, Subtitle: Didot Regular, Body: Montserrat Regular

---

**Image #7 | Template: clinical_data_showcase (#6)**

**Prompt:**
```
extreme close-up of shoulder and décolletage skin texture with moisturizing serum drops on skin surface, SGS certification logo, large percentage improvement numbers with golden arrows, warm beige to light brown gradient background, professional medical photography, soft studio lighting, clinical grade detail, luxury, professional, clinical, trustworthy
```

**Text layers:**
```
Layer 1 (top, large, dark red-brown serif bold)  : "SGS认证"
Layer 2 (below, medium, dark red-brown serif)     : "14天临床实测"
Layer 3 (scattered, large numbers, gold bold)      : "14天" + "↑" 箭头
Layer 4 (below each number, small, dark red-brown sans-serif): "临床测试周期" / "皮肤改善数据"
Layer 5 (bottom corner)                            : SGS logo
```
  Font pairing: elegant — Title: Didot Bold, Subtitle: Didot Regular, Body: Montserrat Regular

---

**Image #8 | Template: lifestyle_scenarios (#25)**

**Prompt:**
```
three-panel vertical grid of lifestyle scenarios, panel 1: woman doing evening shoulder and neck massage with golden capsule serum in soft bedroom lighting, panel 2: product in elegant travel bag, panel 3: spa relaxation with candles, warm towel, and white flowers, warm beige to light brown gradient background, warm lifestyle photography, soft studio lighting, luxury, professional, clinical, trustworthy
```

**Text layers:**
```
Layer 1 (each panel, medium, dark red-brown sans-serif): "夜间修护" / "随身携带" / "居家SPA"
```
  Font pairing: elegant — Title: Didot Bold, Subtitle: Didot Regular, Body: Montserrat Regular

---

## Self-Correction Report (自动校验报告)

After outputting all prompts, append this report:

```
### Self-Correction Report
- Balance Category check: [OK / Adjustments made: ...]
- Placeholder check: [No {} found / {} found at Image #X, rewritten]
- Language check: AI Prompts → English [OK / Issues: ...], Text Layers → Original Language [OK / Issues: ...]
- Boundary check: AI Prompts (visual only) → [OK], Text Hierarchy (text+typography only) → [OK]
```

If any check fails, fix the issue and re-output the affected prompt(s) before presenting the final result.

</supporting-info>
