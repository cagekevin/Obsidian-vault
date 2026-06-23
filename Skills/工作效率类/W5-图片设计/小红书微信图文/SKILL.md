---
name: 社交卡片
description: 生成小红书图文、微信公众号封面等社交卡片，支持 Editorial 杂志风和 Swiss 国际风双视觉系统。Use when 用户需要小红书图文, Rednote/Xiaohongshu images, social cards, carousel, 3:4 covers, 微信公众号封面, WeChat 21:9+1:1 covers, Swiss Style, 杂志风 social images.
---

# Guizang Social Card Skill

Create polished social card packages for Xiaohongshu/Rednote, WeChat Official Account, article covers, and platform thumbnails.

This skill is self-contained. It borrows visual principles from the Guizang PPT style system, but it must not edit the original PPT skill, its templates, or its references. If the original PPT skill is available, you may read it for reference only. Put all generated work in the current project or in the user-requested output folder.

**依赖**：`playwright` 统一安装在 `skills-main/` 根目录的 `node_modules` 中。如需首次安装 playwright 的 Chromium 浏览器：
```bash
npx playwright install chromium
```

## What To Produce

Use this skill for:

- Social card / carousel image sets: cover plus content pages, especially Xiaohongshu/Rednote 3:4.
- WeChat Official Account cover pairs: one `21:9` main cover plus one `1:1` square cover, composed together in the same HTML for visual checking.
- Screenshot-heavy product posts, article covers, tutorial carousels, outdoor/lifestyle notes, AI/product update explainers.
- Social images that need Guizang-style Swiss or editorial magazine layouts.

Do not use this skill for:

- Full slide decks or horizontal PPT websites. Use the PPT skill for that.
- Long-form video generation. Use a video skill for that.
- Pure image editing with no layout or article extraction requirement.

### Rednote Category Capability (capability circle)

The 11 most-common Rednote (小红书) categories fall into three buckets. See `references/category-cookbook.md` for the recipe-by-recipe routing.

**Strong end-to-end** (text, structure, and image story all in scope):

- 旅行 (Travel), 职场 (Workplace), 推荐 (Recommended, after specifying a subtype).

**Strong on text & structure; image needs to come from the user or a sourced library:**

- 游戏 (Game), 影视 (Film/TV), 美食 食谱方向 (Food — recipes only), 彩妆 教程方向 (Makeup — tutorials only), 健身 (Fitness), 家居 (Home), 穿搭 精选方向 (Outfit — capsule/essay only).

**Outside scope — push back honestly rather than promise a result:**

- 美食 菜品大片摆盘 (food-photography showcase).
- 穿搭 日常 OOTD 全身 (daily OOTD body shots; we cannot generate or simulate).
- 情感 梦核 / 氛围感装饰风 (dreamcore / aesthetic-light styling — clashes with both Editorial and Swiss).
- Y2K / 千禧辣妹 / 哥特萝莉 / kawaii decorated aesthetics.
- Pure photography showcase posts where the image is the entire deliverable.

When a request falls in the third bucket, name what we cannot do at intake — do not silently retrofit a layout that misses the user's intent.

## Core Principle

Expression comes first. The goal is not to squeeze text into posters; it is to turn the source into a clear visual argument.

For each page, decide:

- What should the viewer understand in one glance?
- What evidence, screenshot, or image supports it?
- Which words must be large, and which can become captions or metadata?
- What can be removed because it belongs in the post body, not the image?

## Required References

Read these files as needed:

- `references/platform-specs.md` for exact ratios, output sizes, and naming.
- `references/style-system.md` for Guizang editorial and Swiss visual rules.
- `references/theme-presets.md` when choosing electronic-magazine palettes or Swiss accent palettes.
- `references/layout-recipes.md` when selecting carousel/social-card/WeChat page structures.
- `references/components.md` for the shared component spec: font stacks, type scale, minimum readable sizes, Chinese title length bands, Swiss card-fill mutual-exclusion rule, image-container ratio classes, spacing tokens, and Lucide icon rules.
- `references/background-systems.md` when building electronic-magazine WebGL/ink/paper backgrounds.
- `references/portrait-fill.md` when adapting layouts to 3:4 and avoiding under-filled vertical space.
- `references/content-planning.md` for cover hooks, page breakdown, and copy compression.
- `references/production-workflow.md` for HTML/CSS rendering and image handling.
- `references/image-overlay.md` whenever text sits on top of a photo: photo qualification, localized tint fallback, and face / subject avoidance via multimodal subject mapping.
- `references/screenshot-treatment.md` when the user supplies an app / web / code / dashboard screenshot — picks `.frame-shot` over `.frame-img`, sets corners/shadow/bg/inset, decides on `.device-browser` or `.device-phone` chrome.
- `references/map-component.md` when the content has spatial relationships (travel route, store locations, walking tour) — real routes default to Mapbox Static or OSM static tiles; schematic SVG is only for conceptual / illustrative maps. Pins are HTML overlays; never use live JS maps.
- `references/title-shortener.md` when the task is a WeChat 21:9+1:1 cover pair, or any cross-platform reuse — derives the 1:1 short title from the long one (5-step extraction, 4 patterns, anti-patterns, sizing on `.poster.square`).
- `references/category-cookbook.md` to route a user-named Rednote category (旅行 / 职场 / 游戏 / 影视 / 彩妆 / 美食 / 穿搭 / 家居 / 健身 / 情感 / 推荐) to applicable recipes and to confirm scope.
- `references/qa-checklist.md` before delivering final images.

## Workflow — State Machine (MANDATORY)

**每次加载本 skill 后，必须先输出当前状态清单，逐项执行，不可跳步。**

```
═══════════════════════════════════════════════
社交卡片执行状态
═══════════════════════════════════════════════

▶ STEP 0: Project Init        [TODO]
▶ STEP 1: Intake              [TODO]
▶ STEP 2: Extract The Story   [TODO]
▶ STEP 3: Choose Style Mode   [TODO]
▶ STEP 4: Plan Pages          [TODO]
▶ STEP 4.5: Copy Seed Template[TODO]
▶ STEP 5: Build And Render    [TODO] — 自检 [TODO] 渲染 [TODO]
▶ STEP 6: Image Handling      [TODO]
▶ STEP 7: Deliver             [TODO] — 自检 [TODO] 交付 [TODO]

当前步骤: STEP 0
```

**执行规则**：
1. 每次输出完整状态表（9 个步骤，标注 TODO/DONE/SKIP/REVISE/PENDING）
2. 按步骤序号推进，不可跳步。每完成一步更新状态表，再进下一步
3. 修改循环：用户意见 → 判断归属步骤 → 标 REVISE，后续标 PENDING → 回退执行
4. **先展示、等确认、再执行**。任何外部操作（生成、渲染、写文件）都必须先展示计划，等用户说"做"再动手。如果用户只说方向没给具体，也必须确认后再执行
5. **不要信自己的审美**。template 内置 class 默认值是最优的，不要为了"我觉得好看"去改。只有用户明确要求时才改，用 CSS override 不用内联 style
6. **自检**：STEP 5 和 STEP 7 前输出自检清单，FAIL 项修正后才推进：

```
━━━ 自检 — STEP 5 ━━━                    ━━━ 自检 — STEP 7 ━━━
[PASS] 只改了 POSTERS_HERE 区域            [PASS] 用了模板内置 class
[PASS] 只用内置 class，无 task-scoped CSS  [PASS] 无多余 inline style
[PASS] 无多余 inline style                 [PASS] 如选 C，图已生成
━━━ 全部通过 ━━━                          ━━ 交核查工具验尺寸/密度 ━━
```

### 0. Project Init

**创建项目目录前必须先询问用户：当前项目放哪里？**

- 如果用户有指定位置 → 使用用户指定的位置
- 如果用户说"默认"/"随便" → 询问用户要放哪个项目目录
- 如果用户说了其他路径 → 使用该路径

**目录命名规则：** 遵循项目所在目录的命名规范。
- 如在 `Projects/HKH品牌/` 下 → `YYYY-MM-DD-项目名/`
- 如在其他位置 → 按用户要求

**STEP 0.5: 保存用户文案**

将用户提供的原始文案写入项目目录的 `01-输入/文案.txt`（UTF-8 编码），作为后续步骤的参考底本。

**创建目录结构（以 HKH 品牌项目为例）：**
```text
Projects/HKH品牌/
├── 参考/                    ← 共用：别人的素材
├── 资产/                    ← 共用：品牌资产
└── YYYY-MM-DD-项目名/       ← 具体项目
    ├── 01-输入/             ← 原始需求/brief/素材
    ├── 02-中间过程/         ← 生图过程的产物
    ├── 03-输出/             ← 最终成品
    ├── index.html           ← 种子模板复制过来
    ├── assets/              ← 图片素材放这里
    └── output/              ← 导出文件输出到这里
```

**playwright / canvas / ag-psd 已在技能根目录安装**，子项目不需要 `npm install`。Node.js 会自动向上搜索 `node_modules`，直接运行即可。

**导出方式（需要用户确认后再执行）：**

两个流程职责不同，根据需求选用：

**主流程（推荐）：`render.cjs` + `psd-composer.cjs`**

| 步骤 | 脚本 | 输出 | 说明 |
|------|------|------|------|
| ① 截图 | `assets/render.cjs <project>` | `output/项目名_01.png` | 正常版交付图 |
| | | `output/alpha/项目名_01.png` | 透明背景版 |
| | | `output/psd_layers/` | 自动拆层碎片（中间产物） |
| ② 合PSD | `assets/psd-composer.cjs <project>` | `output/项目名_01.psd` | 碎片合成PSD，各元素独立图层 |

拆层规则通过 `AUTO_LAYER_SELECTOR` 自动匹配（`.content > *` 直接子元素、`.frame-img` 图片容器、`.pipeline-v .step-*` 步骤元素、`.marginalia > div / .mg-col > *` 边栏子元素、`.callout / .lead / .body / .pullquote` 独立文本块、`.issue-strip` 底部标签条、`[class^="corner-"]` 角落修饰），无需手动标记 `.layer-item`。

**备选方案（需文字可编辑图层时用）：`html-to-psd.cjs`**

| 步骤 | 脚本 | 输出 | 说明 |
|------|------|------|------|
| ① 生成JSX | `assets/html-to-psd.cjs <project>` | `output/项目名.jsx` | PS脚本 |
| ② 跑脚本 | PS中运行该JSX | 桌面生成 `项目名_01.psd` 等 | 文字图层可双击编辑，但排版可能丢失 |

### 1. Intake

Gather only the missing information that changes the output:

- Target platforms and ratios.
- Source text, subtitles, article, or title.
- **Rednote category** — if the user names one of the 11 common types (旅行 / 职场 / 游戏 / 影视 / 美食 / 彩妆 / 穿搭 / 家居 / 健身 / 情感 / 推荐), route via `references/category-cookbook.md` to find the right recipes and to confirm the request is inside the capability circle (see "Rednote Category Capability" above). If a request lands in the outside-scope bucket, surface that to the user **before** designing, do not silently retrofit.
- Supplied images/screenshots and where each should appear. **For News / Tutorial / Data / Review content, actively prompt for screenshots or photos** — they are the evidence layer. A poster with no real artifact tends to read as filler.
- **If the user supplies only text (no images at all), ask once before designing:**

  ```
  这篇我需要 1-2 张图。三种走法：
  A. 你自己有照片 / 截图，传给我（推荐——最不"AI 感"）
  B. 我去 Pexels / Unsplash / Flickr 帮你找
  C. 用 AI 生成
  ```

  Recommend A in one line — your own photo is what makes a poster not look AI-generated. Accept whatever the user picks (including "都行你看着办") and proceed. **Do not re-prompt later, do not keep nudging toward A across multiple turns.** This question is one-shot.

  **If the user picks C (AI-generated):** write a draft prompt that matches the page's visual role (atmosphere / product / scene / concept), show it to the user for confirmation, then generate only after they approve. Do not generate without showing the prompt first. Example:

  ```
  我打算生成的图：editorial 风格，浅景深微距，金色精油液滴落在湿润绿叶上，暖自然光，柔和的鼠尾草绿与奶油色调，无文字，3:4
  这个方向可以吗？
  ```
- Preferred style if specified: Swiss Style, magazine/editorial, tech, outdoor, etc.
- Hard constraints: title text, no image on 1:1 cover, must include a hardware photo, keep screenshot readable, and so on.

If the user has already supplied enough context, proceed with reasonable assumptions.

If the content involves current product releases, policies, prices, claims, or news, verify unstable facts with browsing and cite sources in the final response.

**If the user provides a custom color palette:** create a new `[data-theme="custom-xxx"]` block with the user's colors mapped to `--paper` (base bg), `--paper-2` (secondary bg), `--ink` (text), `--muted` (secondary text), `--accent` (highlight), `--accent-soft` (soft highlight), `--line` (borders). Set `--ink-rgb`, `--paper-rgb`, `--accent-rgb` as comma-separated RGB values for CSS `rgba()` use. Any color not provided by the user: use the closest match from ink-classic theme. Set `--grain-opacity: .55` for light paper (`#` luminosity > 200), `.35` for medium paper, `.25` for dark paper.

### 2. Extract The Story

Turn the source into a page plan before designing.

For Rednote:

- Page 1 is the cover hook.
- Pages 2-N each carry one idea only.
- Use 5-9 pages for most posts. Compress or combine pages when lower areas become empty.
- Keep the post body for nuance; images should carry hooks, comparisons, checklists, and sharp takeaways.

For WeChat:

- Always produce a paired system: `21:9` main cover and `1:1` square cover.
- Build both covers in the same HTML file and add a combined preview section so their visual relationship can be checked together.
- `21:9` keeps the full or near-full title, subtitle, and one strong visual relation.
- `1:1` uses a simplified short title derived from the long title: big centered type, no image by default, no cramped subtitles.

### 3. Choose Style Mode

Pick one mode per package. **The two systems are not bound to specific content types** — what changes is the visual stance, not which topic you can talk about. A workplace essay can be Editorial; a travel ledger can be Swiss. Pick by the feeling you want, not by category lookup.

**Editorial Magazine x E-ink** brings:

- Serif/Songti display + quiet sans body, paper + ink palette.
- Atmosphere layer (paper grain / ink wash / WebGL canvas) over a warm paper base.
- Ledger rows, marginalia, pull quotes, large photo wells — magazine-feature feel.
- Best when you want the page to feel slow, considered, hand-set.

**Swiss International** brings:

- Inter / Helvetica feel, very light display at large sizes, mono labels at small.
- Strict left-aligned grid, hairline rules, one high-saturation accent.
- Card-fill matrices, KPI towers, h-bar charts, numbered statements — system / data feel.
- Best when you want the page to feel engineered, quantified, decisive.

If both feel viable for a piece of content, the question becomes editorial intent: "is this a feature story or a release note?" That decides the mode, not the topic itself.

Do not mix the two visual systems inside the same image set unless the user explicitly asks for a hybrid.

Then pick one theme:

- Editorial Magazine x E-ink uses one of 6 magazine palettes: Ink Classic, Indigo Porcelain, Forest Ink, Kraft Paper, Dune, or Midnight Ink (the only dark variant; reserved for game key art / night photography / cinematic covers).
- Swiss International uses one of 4 accent palettes: IKB Blue, Lemon Yellow, Lemon Green, or Safety Orange.

Read `references/theme-presets.md` for exact CSS tokens. Do not invent arbitrary colors unless the user has a strict brand requirement.

**Cover recipe selection by content type:**
- **M09 Atmospheric Thesis** — no photo, pure text + WebGL atmosphere. Best when user has no cover image.
- **M01 Magazine Issue Cover** — title + photo well (35-55%) + bottom strip. Best when user has a product shot, scene photo, or wants an image on cover.
- **M16 Image-Led Full-Bleed** — photo fills canvas, title floats on image. Best for lifestyle/atmosphere photos. Requires photo to pass quiet-zone and light tests (see `references/image-overlay.md`). Do not use as default.

### 4. Plan Pages

Create a concise internal plan:

```text
Page 01 / cover / hook / image source / layout intent
Page 02 / point / key copy / visual evidence / layout intent
...
```

When the user asks for approval, show this plan before rendering. Otherwise use it internally and proceed.

**Each page plan must specify image slots:** which page needs images, how many (1 per page typically), where in the layout they go (above title / between text / behind text), and what ratio (`.r-3x2` for landscape, `.r-3x4` for portrait, `.r-1x1` for square). If the user hasn't provided images and chose option C (AI-generated), note the image role in the plan (atmosphere / product / scene / evidence).

Use `references/layout-recipes.md` to choose page structures. Avoid making every page a repeated title-plus-card layout.

For 3:4 images, check `references/portrait-fill.md` before coding. A short table or ledger must be expanded into a full portrait composition with a quote column, image evidence, marginalia, larger rows, or a background hero zone.

### 4.5. Copy The Seed Template

Do not write HTML from scratch. Pick one seed template based on the style mode chosen in Step 3:

- Editorial Magazine × E-ink → copy `assets/template-editorial-card.html` into the task folder as `index.html`.
- Swiss International → copy `assets/template-swiss-card.html` into the task folder as `index.html`.

The task folder is the project directory created in STEP 0 (e.g. `Projects/HKH品牌/YYYY-MM-DD-项目名/`).

The seed already wires up: font loading, theme tokens, all three poster sizes (`.poster.xhs` / `.poster.square` / `.poster.wide`), the pair-preview frame, grain/background layers, and all class definitions referenced by the layout recipes.

Set the theme/accent on the `<html>` element:

- Editorial: `<html data-theme="ink-classic | indigo-porcelain | forest-ink | kraft-paper | dune | midnight-ink">`.
- Swiss: `<html data-accent="ikb | lemon-yellow | lemon-green | safety-orange">`.

Replace the single placeholder poster after `<!-- POSTERS_HERE -->` with one `<section class="poster ...">` block per page, each carrying the HTML skeleton from a chosen Layout Recipe (M01-M16 for Editorial, S01-S12 for Swiss). Never load the wrong template's class system: Editorial recipes assume serif display + ledger/marginalia/pipeline-v; Swiss recipes assume Inter + card-fills + matrix/h-bar/kpi-tower. Mixing them silently breaks the layout.

### 5. Build And Render

Default implementation pattern:

- Create a task folder (STEP 0 already did this), for example `2026-06-22-小红书-岩玫瑰溯源/`.
- Put source images in `assets/`.
- Start from the seed template copied in Step 4.5, not a blank file. Change only the `<!-- POSTERS_HERE -->` region. Use built-in template classes (`.ledger`, `.pipeline-v`, `.callout`, `.pullquote`, `.issue-row`, `.issue-strip`, etc.) unless the required layout genuinely cannot be expressed with them. If built-in classes suffice — and they almost always do — no custom CSS is allowed. Only add a small task-scoped block when all built-in options are exhausted, and keep it minimal.
- **Playwright 已在技能根目录安装**，子项目无需再装。
- 渲染命令（用户确认后再执行）。PSD 图层碎片自动根据语义选择器拆分，无需手动标记。

  ```bash
  # ─── 主流程：截图 → 合成 PSD ───
  node <skill-assets>/render.cjs <project-dir>
  # 输出: project_01.png + alpha/ + psd_layers/

  node <skill-assets>/psd-composer.cjs <project-dir>
  # 输出: project_01.psd（各元素独立图层）

  # ─── 备选：DOM 提取 PSD（文字可编辑）───
  node <skill-assets>/html-to-psd.cjs <project-dir>
  # 输出: project.jsx → PS 运行 → 桌面生成 project_01.psd
  ```

- Save rendered images in `output/`.
- **Optional: generate layered PSD script** — `node html-to-psd.cjs <task-dir>` produces `output/<slug>.png`, `output/<slug>-alpha.png`, and `output/<slug>.jsx`. Run the `.jsx` in Photoshop (File → Scripts → Browse) to get a layered PSD with editable text and native fill layers.
- Verify dimensions and inspect the rendered PNGs.
- Keep `node validate-social-deck.mjs <task-dir>` available for auto-check passes. It checks overflow (R1), footer collision (R2), Swiss bold display (R3), minimum font size (R4), 4-band density (R5), `.h-xl` line caps (R6), and browser-default figure margin drift (R7). Exit code 1 on any FAIL — fix before final delivery when auto-check is requested. WARN is advisory but read it.

Do not place visible instructions, keyboard shortcuts, or usage explanations inside the images.

For Editorial Magazine x E-ink, use a layered background system. Prefer a subtle WebGL ink-flow canvas or a frozen procedural canvas plus paper grain. Read `references/background-systems.md`; do not rely on a flat beige background, and do not add page-wide grid/dot backgrounds.

### 6. Image And Screenshot Handling

When the user provides screenshots:

- Preserve screenshot content unless the user asks for redesign.
- Prefer programmatic framing: target-ratio canvas, safe padding, clean background, readable screenshot.
- Do not stretch screenshots.
- If screenshot clarity matters, enlarge the screenshot area and reduce nearby text.

#### Text-On-Image Composition

Whenever a poster places text on top of a photo (full-bleed cover, large image well, generated-image overlay), follow `references/image-overlay.md`:

- **Selection first, tint only if needed.** A photo covering ≥60% of the canvas must first pass the quiet-zone and light tests in `image-overlay.md`. Compose without a mask first; if the thumbnail check fails, add only a localized, image-toned tint around the title area. Do not default to full-canvas falloffs.
- **Subject mapping is mandatory.** Before placing the title, read the image with the Read tool, describe in plain language where the subject's face/focal feature sits, and record the subject map as an HTML comment next to the hero block. Place text only in the documented safe zones.
- **Crop discipline — set `object-position` inline on every photo.** The template default (`center 50%`) is a fallback, not a recommendation. For every `<img>`, decide based on subject location and write it inline: e.g. `style="object-position:center 62%"` for mid-body subjects, `center 30%` for sky-heavy landscapes with horizon-line subjects, `center 70%` for foreground gear. See the table in `references/components.md` for ranges and `image-overlay.md` for face-photo specifics. Skipping this silently crops subjects out of frame on tall ratios (`r-3x4`, `r-21x9`).
- **Thumbnail test.** Downscale the rendered PNG to 360 px wide and confirm the title is still legible. If the title fights the photo, move the title, swap the photo, or add a localized image-toned tint; if the photo looks dead, the tint is too heavy or the photo was wrong for text-on-image.

Editorial dark covers (e.g. game journals on key art) and Swiss covers with hero photos both require these checks. Skipping them is a known failure mode (see `style-system.md` Anti-Pattern D).

When the user has no images:

- This branch only runs if the Step 1 "三选一" gate landed on B (web-sourced) or C (AI-generated). Never silently fall into B or C — the user picked one.
- For C (AI-generated): use generated bitmaps only where they add real value, usually 1-2 pages. Generate images that match the page's visual role, not generic decoration. Keep generated images free of embedded titles, page numbers, logos, or fake UI labels unless explicitly needed.
- For B (web-sourced): see the Web-Sourced Images section below.

#### Web-Sourced Images (fallback when user has none)

When the user has no screenshots/photos and a generated bitmap would not fit the page's role (e.g. Editorial atmosphere shot, outdoor / lifestyle backdrop, game cover art, real-world product shot), fetch from the web instead of leaving the page thin.

Policy: **grab first, disclose after, let the user decide on attribution.** Do not pre-filter sources by guessed license — the user is the rights holder of the final composition and decides what is acceptable.

Recommended sources, in order of preference. **All five below are free-tier libraries with no required licensing fees**; we do not pull from paid stock sites (视觉中国 / Getty / 站酷海洛 etc.).

1. **Unsplash** — `https://unsplash.com/s/photos/<keyword>`. Strong for outdoor / lifestyle / atmospheric backdrops. English keywords work best. License is permissive but verify case by case.
2. **Pexels** — `https://www.pexels.com/search/<keyword>/` or `https://www.pexels.com/zh-cn/search/<keyword>/`. **Supports Chinese keyword search natively** — fills Unsplash's gap on 国内场景 (中文街景 / 国风物件 / 本地地名). Use this first when the subject is China-specific or the keyword is Chinese. Free under Pexels License.
3. **Flickr CC-licensed pool** — `https://www.flickr.com/search/?text=<keyword>&license=2%2C3%2C4%2C5%2C6%2C9`. The license filter (`license=2,3,4,5,6,9`) restricts to Creative Commons photos. Fills the "documentary realness" gap: street photography, people-in-context, real interiors, non-styled scenes that Unsplash/Pexels lack. Always preserve CC attribution if the user opts in.
4. **Wallhaven** — `https://wallhaven.cc/search?q=<keyword>`. Strong for game / anime / wallpaper themes. Content is user-uploaded, rights are unverified.
5. **Direct web search** — when a specific subject is needed (a product render, a game still, a historical photo). Use WebFetch / WebSearch to find a candidate URL.

Editorial-mode picking order: **Pexels (if keyword is Chinese / China-specific) → Unsplash → Flickr CC (if you need real-life feel) → direct search**. Swiss mode rarely needs any of these — product renders, UI screenshots, and keyshot-style images should be user-supplied or AI-generated, not stock.

How to fetch:

- Use WebFetch or `curl` to download the image into the task folder's `assets/` directory.
- Name the file by purpose, not by hash: `assets/hero-mountain.jpg`, `assets/ui-pulse-card.png`.
- Record the source URL in a `assets/SOURCES.md` file next to the images (one line per file: `hero-mountain.jpg ← <url>`). Always do this even if the user declines attribution in the final image — it preserves provenance for the human author.

After fetching, surface the provenance to the user **before** finalizing the design:

```
我从 <site> 取了这些图：
- assets/hero-mountain.jpg — <url>
- assets/ui-pulse-card.png — <url>

⚠️ 版权未经核实。请你判断是否可用。
是否需要在图文中标注来源？
- 要：我把 "Photo · <site> · @<author>" 加到对应页脚 / 角标。
- 不要：原样使用,不加注释。
```

If the user picks "标注" — add a small `mono` caption (Swiss: `.t-meta` 18-20px in corner; Editorial: `.label` next to the image well). Never crowd the caption into the layout's focal area.

If the user picks "不标注" — proceed silently. The provenance still lives in `assets/SOURCES.md` for the user's own records.

If an image is only one element among many in a composite (e.g. one of nine photos in a matrix), the user may reasonably skip attribution. Do not force a credit label that breaks the layout.

### 7. Deliver

**Show user first, validate on request.** Auto-running the validator after every render takes too long and delays the user from seeing results. Default flow:

1. After rendering completes, immediately show the user the rendered images inline (absolute paths) with a one-sentence summary of what was built.
2. Ask one question: **"先你自己看，还是我先自动核查一遍？"** (Do you want to review first, or should I run the auto-check?)
3. If the user says "我自己看" / "先给我" / "no need" — stop here, let them inspect, and respond to whatever they raise.
4. If the user says "你查吧" / "auto-check" / "yes" — only then run `node validate-social-deck.mjs <task-dir>`, fix any FAIL, and re-render before final delivery. Mention density/cap WARNs.

Never silently run the validator before showing the user — it costs minutes per pass and the user often spots issues faster.

Final response (after the user has reviewed or asked for auto-check) should include:

- Output folder path.
- Rendered images shown inline with absolute paths when useful.
- A short note on dimensions and verification (or "not yet validated, awaiting your review").
- For any image fetched from the web: source URL + site + the attribution decision the user made.
- Any unresolved risks, such as source images being low resolution.
- **Layered PSD available**: `output/<slug>.jsx` is ready — run in PS (File → Scripts → Browse) for editable text and native fill layers. Only mention if the user might need it.

**最终出图流程（用户确认定稿后执行）：**

1. 运行 `render.cjs` 生成正常图 + alpha + 逐层碎片（自动拆层，无需手动标记）
2. 运行 `psd-composer.cjs` 合成 PSD
3. 交付：正常 PNG / alpha 透明版 / PSD

**追加卡片子流程**（用户要求在已有套图中增加新卡片）：
1. 标记状态表：STEP 2 → [REVISE]，STEP 4 → [REVISE]，后续 → [PENDING]
2. 提取新卡片的内容（STEP 2）
3. 制定新卡片的页面计划，标注图片位（STEP 4）
4. 在 `<!-- POSTERS_HERE -->` 区域最后追加一个 `<section class="poster xhs">` 块（STEP 5）
5. 渲染全部卡片，验证全部通过后交付（STEP 7）

## Non-Negotiables

- Never edit the original Guizang PPT skill or any upstream skill copied from elsewhere.
- Do not create random decorative SVG ovals, blobs, rain drops, stickers, or meaningless circles.
- Do not use nested cards or generic SaaS card layouts as the default.
- Do not let text overflow, touch the edge, or collide with the footer band. Pin `.foot` with `margin-top: auto` inside a flex column, never with `position: absolute` over growing content.
- Do not let text become too small to read on mobile.
- Do not write inline `font-size` + `font-weight` on display titles in Swiss. Use the typed classes (`.h-hero` / `.h-statement` / `.h-xl` / `.num-mega`). A 80-120px headline at weight 700-900 is not Swiss; "the larger, the lighter" is a hard rule.
- Do not deliver Editorial posters with a flat paper background, mono labels on every row, and no atmosphere layer. Run the Editorial Identity Test in `references/style-system.md` — a serif title alone does not make a poster Editorial.
- Do not fake data, release details, or percentages.
- Do not crop faces, key UI text, or hardware/product details unless the user explicitly accepts it.
- Do not reuse a 21:9 cover by blindly cropping it into 1:1. Compose each ratio separately.
- **3:4 卡必须吃满画布**。Content (text + image + data) 必须覆盖 ≥75% 画布高度。任何 >15% 画布高度的纯空白带都需要"留白理由"：(a) hero image 自带呼吸、(b) 单句宣言式 hero statement、(c) 段落顶/底 leading & trailing whitespace（前后总和 ≤15%）。**禁止用 `<div style="flex: 1"></div>` 上下夹击把内容塞到中段**——杂志页留白逻辑不适用于社交卡（杂志靠对开页吸收留白，社交卡逐张独立刷，欠填看着像 PPT 漏排）。Recipe-by-recipe 最小密度见 `references/layout-recipes.md` 每条 recipe 的「Minimum density」段。Render 后必须跑 `qa-checklist.md` 的 4 横带密度检查。
