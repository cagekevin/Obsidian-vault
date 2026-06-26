---
name: 详情页复刻
description: '快速生成风格相似的电商详情页草稿（Style Transfer），非精确复刻。基于参考图分析视觉DNA → 迁移到新产品 → 诚实评估输出。Use when user wants to recreate a product detail page, clone an e-commerce design, replicate a product page, or generate a detail page from a reference. 适合出初稿/草稿/灵感参考，不适合像素级复刻。'
metadata:
  pattern: generator
---

# E-commerce Detail Page Style Transfer

<what-to-do>

**Purpose**: Quickly generate style-similar e-commerce detail page drafts by analyzing reference pages and transferring their visual language to new products. This is a **rapid prototyping tool**, not a pixel-perfect replication system.

**Realistic Success Rate**: Style similarity 70-80% | Layout approximation 60-70% | Text rendering accuracy 50-60% | Overall usable draft rate 65-75%

**What This Skill CAN Do**:
- Capture overall visual style (color palette, mood, composition patterns)
- Generate similar layout structures
- Transfer design language (modern/luxury/minimalist/energetic)
- Create quick drafts for iteration

**What This Skill CANNOT Do**:
- Pixel-perfect replication of layouts
- Exact color matching (expect ±10-20% variance)
- Precise text rendering in specific fonts
- Guaranteed element positioning
- Maintain exact proportions across all sections

---

## Workflow

### Stage 1: Reference Analysis & Style Extraction

**Objective**: Understand the visual DNA of the reference page, not measure it precisely.

#### Step 1.1: Initial Image Analysis

**Action**: Call `analyse_image` on the reference detail page.

**Analysis Focus** (qualitative, not quantitative):
```
1. Overall Visual Impression
   - Mood/tone (e.g., clean and modern, warm and luxurious, energetic and youthful)
   - Dominant colors (describe as soft pink and gold accents, not #HEX)
   - Visual hierarchy (what catches the eye first, second, third)

2. Layout Pattern Recognition
   - Section sequence (hero product → feature grid → lifestyle scene → specs table)
   - Composition style (centered/asymmetric/magazine-style/minimal)
   - Spacing feel (tight and compact vs. airy and spacious)

3. Design Elements
   - Typography style (bold headlines, elegant serifs, playful sans-serif)
   - Graphic treatments (rounded corners, shadows, borders, badges)
   - Image style (studio shots, lifestyle, illustrated, 3D renders)
   - Decorative elements (patterns, dividers, icons)

4. Content Structure
   - Key messaging themes
   - Information density (text-heavy vs. visual-focused)
   - Call-to-action patterns
```

**Output to User**: Present a qualitative style summary in natural language.
```
"The reference page has a [adjective] aesthetic with [color description]. 
The layout follows a [pattern description] structure with [spacing description]. 
Key design features include [visual elements]. 
The overall mood is [mood description]."
```

**DO NOT** output: hex color codes, pixel measurements, precise angles, Delta E values, numerical spacing ratios.

#### Step 1.2: User Confirmation & Adjustment

**Action**: Ask user which aspects to prioritize.
```
"I've analyzed the reference page. Before generating, please confirm:
1. Style Priority: Should I focus more on [color mood] or [layout structure]?
2. Flexibility: Are you okay with variations in [specific element], or must it stay close?
3. Content: Do you have specific product images/text, or should I use placeholders?
You can also tell me: 'Just generate based on the overall style' to proceed directly."
```

**Why This Step Matters**: AI cannot perfectly replicate everything. User input helps allocate the limited accuracy budget to what matters most.

---

### Stage 2: Content Preparation

**Objective**: Gather assets for the new product page.

#### Step 2.1: Asset Collection

**Required from User**:
- New product images (at least 1 main image)
- Product name
- Key selling points (3-5 bullet points)

**Optional from User**:
- Brand logo
- Specific text content
- Additional product angles/lifestyle shots
- Technical specifications

**If User Provides Minimal Info**: Proceed with placeholders and inform user:
```
"I will generate a draft using placeholder text for [missing elements]. 
You can replace these later or provide the content now for a more complete draft."
```

#### Step 2.2: Reference Image Search (If Needed)

**When to Search**:
- User has no lifestyle/scene images but reference page uses them
- Need supporting visual elements (textures, backgrounds, icons)

**Action**: Call `search_image` with simple, concrete queries.
- Good: "minimalist product photography", "marble texture", "lifestyle kitchen"
- Bad: "high-end luxury modern minimalist product shot with soft lighting"

**Search Strategy**: 1-2 searches maximum. Focus on filling critical gaps. Prefer user-provided images.

---

### Stage 3: Draft Generation

**Objective**: Generate a style-similar detail page draft in one shot.

#### Step 3.1: Prompt Construction

**Prompt Structure** (for `generate_image_nano_banana_2`):
```
Create an e-commerce product detail page for [PRODUCT_NAME] in the style of the reference image.

VISUAL STYLE TO MATCH:
- Overall mood: [mood from analysis]
- Color palette: [color description from analysis]
- Design language: [style keywords from analysis]

LAYOUT STRUCTURE:
[Describe section-by-section in visual terms, e.g.:]
- Top section: Large hero product image on [left/right/center] with [background description]
- Second section: [Grid of 3 feature callouts / Side-by-side comparison / etc.]
- Third section: [Lifestyle scene showing product in use]
- Bottom section: [Specifications table / Trust badges / etc.]

PRODUCT CONTENT:
- Product: [product name and brief description]
- Key features: [bullet points]
- [Any specific text to include]

DESIGN DETAILS:
- Typography: [bold/elegant/playful] headlines, [clean/serif/rounded] body text
- Spacing: [tight/moderate/airy]
- Graphic elements: [rounded corners/shadows/borders/badges as seen in reference]
Keep the overall visual language consistent with the reference while adapting to the new product.
```

**Critical Prompt Rules**:
1. **Use visual descriptions, not numbers**: 
   - Good: "Product shown from a slightly elevated front angle"
   - Bad: "Product at 15 degree angle"
2. **Describe colors qualitatively**:
   - Good: "Soft peachy pink background with warm gold accents"
   - Bad: "Background #FFE5D9, accents #D4AF37"
3. **Reference the style image clearly**: Always include reference image URL in image_url_list. Use phrases like "in the style of the reference image".
4. **Be specific about layout but flexible about execution**: Describe what sections exist and their purpose. Do not demand pixel-perfect positioning.

#### Step 3.2: Tool Invocation

**Tool**: `generate_image_nano_banana_2`

**Parameters**:
```javascript
{
  "task_type": "REFERENCE_TO_IMAGE",
  "image_url_list": [
    "[Reference detail page URL]",
    "[Main product image URL]",
    "[Optional: lifestyle/supporting images]"
  ],
  "aspect_ratio": "9:16",   // Standard detail page
  "resolution": "2K"        // Higher resolution for detail pages
}
```

**Aspect Ratio Selection**:
- Standard detail page: 9:16 (portrait)
- Short-form page: 3:4
- Extra-long page: Generate in sections (see Stage 5)

#### Step 3.3: Output Delivery

**Present to User**:
```
"Here is your detail page draft based on the reference style:

STYLE MATCH ASSESSMENT:
✓ Successfully captured: [list 2-3 strong matches]
⚠ Approximate areas: [list 1-2 areas with variance]
✗ Needs manual adjustment: [list any obvious misses]

NEXT STEPS:
- If the overall direction works, I can generate variations or additional sections
- If specific elements need changes, describe what to adjust and I will iterate
- For final production, you may need to manually refine [specific elements]"
```

**Honesty in Presentation**: Point out what worked and what did not. Do not oversell the result. Provide clear guidance on what needs human touch.

---

### Stage 4: Iteration & Refinement

**Objective**: Improve the draft based on user feedback.

#### Step 4.1: Feedback Collection
```
"What would you like to adjust? Common refinements:
1. Change specific section layouts
2. Adjust color mood (warmer/cooler/more vibrant)
3. Modify text content
4. Regenerate with different product angles
5. Create variations of specific sections"
```

#### Step 4.2: Targeted Regeneration

For section-specific changes:

**Option A: Regenerate Entire Page** (simpler, less control)
- Modify prompt to emphasize the changed section
- Regenerate full page

**Option B: Generate Section Separately** (more control, requires assembly)
- Generate the specific section as a standalone image
- User manually combines in design tool

**Recommendation**: Default to Option A for 1-2 iterations, suggest Option B if user needs fine control.

#### Step 4.3: Variation Generation

**Common Variation Requests**:
1. **Color Variations**:
   "Generate 2 more versions with different color moods: Version A: Cooler tones (blues and purples), Version B: Warmer tones (oranges and reds)"

2. **Layout Variations**:
   "Create an alternative layout with hero section using a lifestyle scene instead of product-only, feature grid changed to side-by-side comparison"

3. **Density Variations**:
   "Generate a more minimal version with more white space, fewer text blocks, focus on large visuals"

**Batch Generation**: If user wants multiple variations, generate them in one call to image sub-agent with all variations listed in project context.

---

### Stage 5: Multi-Section Pages (Advanced)

**When to Use**: Reference page is extremely long (equivalent to 3+ screen heights).

**Challenge**: Single image generation has practical limits on length and detail density.

**Solution**: Section-by-section generation with style consistency.

#### Step 5.1: Section Planning

**Action**: Divide the page into logical sections.

**Example Breakdown**:
```
Section 1: Hero (product + headline)
Section 2: Key Features (3-column grid)
Section 3: Lifestyle Scene (product in use)
Section 4: Technical Specs (table/infographic)
Section 5: Trust Signals (badges, testimonials)
```

**Present to User**:
```
"This reference page is quite long. I recommend generating it in [X] sections. I will generate them with consistent styling. You will need to assemble them in a design tool. Alternatively, I can create a condensed single-page version. Which do you prefer?"
```

#### Step 5.2: Sequential Generation

**Process**:
1. Generate Section 1 with full style reference
2. Generate Section 2 using both: Original reference page + Generated Section 1 (for style consistency)
3. Repeat for remaining sections

**Prompt Pattern for Section 2+**:
```
"Create section [N] of an e-commerce detail page, maintaining visual consistency with the previous section.
STYLE CONSISTENCY:
- Match the color palette, typography, and design language from the first image
- Use similar spacing and graphic treatments
SECTION CONTENT:
[Specific content for this section]
This section should feel like a natural continuation of the page."
```

**Tool Call for Section 2+**:
```javascript
{
  "image_url_list": [
    "[Original reference page]",
    "[Previously generated Section 1]",
    "[Product/content images for this section]"
  ],
  "aspect_ratio": "16:9",   // Shorter ratio for individual sections
}
```

#### Step 5.3: Assembly Guidance
```
"All sections are complete! Here is how to assemble them:
MANUAL ASSEMBLY (Recommended):
1. Open in Figma/Photoshop/Canva
2. Stack sections vertically
3. Adjust overlaps/spacing between sections
4. Ensure color consistency (may need minor tweaks)
AUTOMATED ASSEMBLY (Experimental): I can attempt to generate a combined version, but quality may degrade."
```

**Reality Check**: Automated assembly often produces worse results than manual combination. Be honest about this.

---

## Scenario-Specific Guidance

### Scenario A: Same Product Category, Different Product
**Example**: Reference is a skincare cream page, user wants to create a page for their serum.
**Approach**: High style transfer fidelity expected. Focus on swapping product images while keeping layout. Adjust text content.
**Success Rate**: 75-85% (highest success scenario)
**Prompt Emphasis**:
```
"Create a detail page for [NEW_PRODUCT] using the exact same layout structure and visual style as the reference [OLD_PRODUCT] page. Maintain the section sequence, color palette, and design treatments. Only swap the product images and update the text content."
```

### Scenario B: Different Product, Similar Style
**Example**: Reference is a tech gadget page, user wants fashion item page.
**Approach**: Transfer visual mood and design language. Adapt layout to suit different product type.
**Success Rate**: 60-70% (moderate success)
**Prompt Emphasis**:
```
"Create a detail page for [FASHION_PRODUCT] inspired by the visual style of the reference tech product page.
TRANSFER THESE ELEMENTS: Overall color mood, typography style, graphic treatments, spacing feel.
ADAPT THESE ELEMENTS: Layout structure to suit fashion product, content sections, image style."
```
**Visual Description for Product Presentation**: 
- "Show the dress on a model, full-body shot, centered"
- "Display the handbag from a front-facing view with slight elevation"
- "Present the shoes in a dynamic side angle showing the profile"
- NEITHER: "Product at 45 degree angle, 30 degree elevation"

### Scenario C: Competitor Analysis / Inspiration Transfer
**Example**: User likes a competitor page style and wants similar for their brand.
**Approach**: Extract style DNA without copying. Emphasize differentiation. Focus on inspired by not replica of.
**Success Rate**: 65-75%
**Prompt Emphasis**:
```
"Create a detail page for [BRAND] [PRODUCT] inspired by the reference design, but with distinct brand identity.
INSPIRATION ELEMENTS: [Specific style aspects to borrow], [Layout patterns that work well]
DIFFERENTIATION: Use [BRAND] colors, adapt tone to be more [adjective], include unique brand elements."
```
**Ethical Note**: Remind user this is for inspiration, not copying. Suggest adding unique brand elements.

---

## Limitations & Manual Intervention Points

### What AI Cannot Reliably Do

#### 1. Precise Text Rendering
- **Problem**: AI often generates garbled text, wrong fonts, or misaligned text blocks
- **Success Rate**: 50-60% for readable text
- **Solution**: Generate page with placeholder text areas. User adds real text in design tool. Or provide exact text in prompt and regenerate if garbled (may take 2-3 tries)

#### 2. Exact Color Matching
- **Problem**: AI interprets colors qualitatively, not numerically
- **Expected Variance**: +/- 10-20% in hue/saturation
- **Solution**: Accept close enough for drafts. Manual color correction in final production. Or provide brand color descriptions in prompt (e.g., use deep navy blue, not bright blue)

#### 3. Complex Data Visualizations
- **Problem**: Charts, graphs, detailed tables often generate incorrectly
- **Success Rate**: 30-40% for complex infographics
- **Solution**: Generate page with placeholder chart areas. Create actual charts in specialized tools (Excel, Figma). Composite manually.

#### 4. Pixel-Perfect Alignment
- **Problem**: AI does not understand grids and precise spacing
- **Reality**: Elements will be approximately positioned
- **Solution**: Use AI draft as a guide. Rebuild in design tool for production. Or accept good enough for quick campaigns.

#### 5. Brand Logo Integration
- **Problem**: Logos often get distorted or stylized incorrectly
- **Success Rate**: 40-50% for clean logo rendering
- **Solution**: Generate page without logo. Add real logo file in post-production. Or provide logo as reference image and emphasize keep logo unchanged.

### When to Stop Iterating with AI

**Diminishing Returns Point**: After 3-4 regenerations, you are likely fighting AI limitations rather than making progress.

**Signs to Move to Manual Editing**:
- Text keeps generating incorrectly after 3 tries
- Specific element positioning will not cooperate
- User needs pixel-perfect precision
- Color matching requires exact hex values

**Recommendation to User**:
```
"We have reached the point where manual refinement will be faster than more AI iterations. 
I recommend:
1. Use this draft as your foundation
2. Import into [Figma/Photoshop/Canva]
3. Manually adjust [specific elements]
4. Add final text and brand assets
This hybrid approach gives you the speed of AI drafting plus precision of manual control."
```

---

## Quality Expectations & Success Metrics

### Realistic Output Quality

**Draft Quality (First Generation)**:
- Style similarity: 70-80%
- Layout structure approximation: 60-70%
- Text accuracy: 50-60%
- Color precision: 60-70%
- Element positioning: 60-70%

**After 2-3 Iterations**:
- Style similarity: 80-85%
- Layout structure: 75-80%
- Text accuracy: 65-70%
- Color precision: 70-75%
- Element positioning: 70-75%

**Production-Ready (AI + Manual)**: 90%+ quality achievable with manual post-production.

### Success Criteria by Use Case

**Quick Campaign Drafts** (Speed Priority): AI alone sufficient. Accept 70-80% fidelity.
**Client Presentations** (Balance): AI draft + light manual touch-up. 80-85% fidelity. 1-2 hours manual refinement.
**Final Production** (Quality Priority): AI as foundation + full manual production. 95%+ fidelity. Treat AI output as wireframe/mockup.

---

## Workflow Decision Tree

```
START: User provides reference detail page
  ↓
[Analyze reference with analyse_image]
  ↓
Does user have all product assets?
  ├─ YES → Proceed to generation
  └─ NO → Request assets or use placeholders
       ↓
Is reference page extremely long?
  ├─ YES → Offer section-by-section generation
  └─ NO → Single-page generation
       ↓
[Generate draft with generate_image_nano_banana_2]
  ↓
Present draft with honest assessment
  ↓
User satisfied with direction?
  ├─ YES → Offer variations/refinements
  └─ NO → Iterate with specific feedback
       ↓
After 3 iterations, still not satisfied?
  ├─ YES → Recommend manual editing
  └─ NO → Continue refinement
       ↓
COMPLETE: Deliver final draft + assembly guidance
```

---

## Example Prompt Templates

### Template 1: Standard Product Page
```
Create an e-commerce product detail page for [PRODUCT_NAME] in the style of the reference image.

VISUAL STYLE:
- Mood: [Clean and modern / Luxurious and elegant / Energetic and youthful]
- Colors: [Soft pastels with gold accents / Bold primary colors / Muted earth tones]
- Design language: [Minimalist / Maximalist / Organic / Geometric]

LAYOUT STRUCTURE:
- Hero section: [Product image placement and background description]
- Feature section: [Grid/list/comparison format]
- Lifestyle section: [Scene description]
- Details section: [Specs/benefits presentation]

PRODUCT INFO:
- Name: [Product name]
- Key features: [Feature 1], [Feature 2], [Feature 3]

DESIGN DETAILS:
- Typography: [Bold sans-serif headlines, clean body text]
- Spacing: [Airy with generous margins]
- Graphics: [Rounded corners, subtle shadows, minimal borders]
```

### Template 2: Style Transfer Across Categories
```
Create a [NEW_CATEGORY] product detail page inspired by the visual style of the reference [OLD_CATEGORY] page.

STYLE ELEMENTS TO TRANSFER:
- Color palette: [Description from reference]
- Typography feel: [Bold/elegant/playful]
- Composition style: [Centered/asymmetric/grid-based]
- Graphic treatments: [Specific elements to keep]

ADAPTATIONS FOR NEW CATEGORY:
- Layout: [How to modify structure for new product type]
- Content focus: [What to emphasize for this category]
- Image style: [Lifestyle/studio/illustrated approach]
```

### Template 3: Competitor-Inspired (Differentiated)
```
Create a detail page for [BRAND] [PRODUCT] inspired by the reference design, but with distinct brand identity.

INSPIRATION FROM REFERENCE:
- [Specific layout patterns]
- [Design techniques that work well]

BRAND DIFFERENTIATION:
- Colors: Use [BRAND] palette - [description]
- Tone: More [adjective] than reference
- Unique elements: Include [brand-specific features]
```

---

## Communication Templates

### Initial Analysis Presentation
```
"I have analyzed the reference detail page. Here is what I found:
VISUAL STYLE: [Mood], [Colors], [Design language]
LAYOUT PATTERN: [Sections]
KEY DESIGN ELEMENTS: [Elements]
Before I generate your page, please provide:
1. Your product images (at least 1 main image)
2. Product name and key features
3. Any specific content you want included
Or tell me to proceed with placeholders for a quick draft."
```

### Draft Delivery with Honest Assessment
```
"Here is your detail page draft:
STYLE MATCH ASSESSMENT:
✓ Successfully captured: [Strong match 1], [Strong match 2]
⚠ Approximate areas: [Variance 1], [Variance 2]
✗ Needs manual adjustment: [Element that did not work]
OVERALL: This draft captures [X]% of the reference style.
Would you like me to: 1) Iterate on specific sections, 2) Generate variations, 3) Provide guidance for manual refinement"
```

### Iteration Limit Recommendation
```
"We have done [X] iterations. I am noticing we are hitting AI limitations on [specific element].
OPTION A: Accept current draft + manual refinement. Import into [design tool], manually adjust. Result: 95%+ quality.
OPTION B: Continue AI iteration. May take 3-5+ more tries, no guarantee. Diminishing returns likely.
My honest recommendation: Option A will get you to your goal faster."
```

---

## FAQ

**Q: Can AI perfectly replicate a detail page?** A: No. AI can create style-similar drafts with 70-85% fidelity. For production quality, expect to do manual refinement.

**Q: How many iterations should I try?** A: 2-3 iterations usually yield the best results. After that, diminishing returns set in. Switch to manual editing.

**Q: Why is the text garbled?** A: AI text rendering is unreliable (50-60% success rate). Generate with placeholder text and add real text manually, or regenerate 2-3 times.

**Q: The colors do not match exactly. Can you fix this?** A: AI interprets colors qualitatively, not numerically. Expect +/- 10-20% variance. For exact brand colors, do manual color correction in post-production.

**Q: Can I use this for final production?** A: Use AI output as a foundation/wireframe. Plan for manual refinement to achieve production quality (90%+ fidelity).

**Q: What if the layout is completely wrong?** A: Regenerate with more specific layout description. If it fails after 2-3 tries, the layout may be too complex for AI. Consider section-by-section generation or manual design.

**Q: How long does this process take?** A: Quick draft 5-10 minutes. Refined draft (2-3 iterations) 20-30 minutes. Production-ready (AI + manual) 2-4 hours.

---

## Tool Selection Logic

### Primary Tool: generate_image_nano_banana_2
**Advantages**: Good style transfer, handles multiple reference images, reasonable text rendering, fast.
**Use for**: All standard detail page generation, single-page outputs, section-by-section, iterations and variations.
**Parameters**: task_type always REFERENCE_TO_IMAGE, aspect_ratio 9:16 or 16:9 for sections, resolution 2K.

### When to Use Image Sub-Agent
**Scenario**: User requests multiple variations in one message (e.g., Generate 3 versions with different color schemes).
**Action**: Call subagent with all variations listed in one project_context, each with full prompt. Use generate_image_nano_banana_2 for all generations.

### When NOT to Use This Skill
- User wants pixel-perfect replication: Set expectations that AI cannot achieve this
- Reference is a complex interactive page: AI generates static images only
- User needs exact brand compliance: AI cannot guarantee brand guideline adherence
- Reference has heavy data visualization: Charts/graphs will likely fail

---

## Version History

### v4.0 (Current - Honest Edition)
- Removed all unrealistic precision requirements
- Changed to qualitative analysis approach
- Added honest success rate expectations
- Included manual intervention guidance
- Repositioned as draft generation not replication
- Added diminishing returns detection
- Improved communication templates with realistic assessments

### v3.0 (Previous - Overpromised)
- Claimed precise color/layout replication
- Used numerical parameters AI could not deliver
- Promised 90%+ success rates
- No guidance on when to stop iterating

---

## Best Use Cases

- Quick campaign drafts
- A/B testing concepts
- Client presentation mockups
- Foundation for manual design

**Success Formula**: AI Draft (70-85% quality) + Manual Refinement (15-30% effort) = Production-Ready Output (95%+ quality)

**Key Principle**: Be honest about AI limitations. Set realistic expectations. Deliver usable drafts quickly, and guide users on when to switch to manual editing.

</what-to-do>
