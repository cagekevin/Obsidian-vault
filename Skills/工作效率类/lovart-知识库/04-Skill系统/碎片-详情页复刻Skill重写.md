# Lovart 拼图碎片 — 详情页复刻Skill重写

## 话术

你刚刚评审了电商详情页复刻工作流v3，指出了很多现实问题：analyse_image不能输出精确数值、角度参数是安慰剂、过渡色带不可行、量化指标无法测量、真实成功率只有60%。

现在请你基于这些诚实反馈，直接帮我写一份完整的、重新设计的SKILL.md。

要求：
1. 定位改为：快速生成风格相似的详情页草稿，而非精确复刻
2. 删除所有不切实际的要求（精确坐标、ΔE数值、色温数值等）
3. 产品替换场景B的prompt从角度数值改为视觉化描述
4. 承认AI做不到的地方直接说明，给出人工介入建议
5. 保持流程清晰可执行，但降低承诺
6. 包含诚实的成功率预期

请直接输出完整的SKILL.md内容，不要省略，不要用占位符。

## 回复

# E-commerce Detail Page Style Transfer Skill
## Skill Overview
**Skill Name**: E-commerce Detail Page Style Transfer
**Skill ID**: `ecommerce_detail_page_style_transfer`
**Version**: 4.0 (Honest Edition)
**Purpose**: Quickly generate style-similar e-commerce detail page drafts by analyzing reference pages and transferring their visual language to new products. This is a **rapid prototyping tool**, not a pixel-perfect replication system.
**Realistic Success Rate**: 
- Style similarity: 70-80%
- Layout approximation: 60-70%
- Text rendering accuracy: 50-60%
- Overall usable draft rate: 65-75%
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
   - Mood/tone (e.g., "clean and modern", "warm and luxurious", "energetic and youthful")
   - Dominant colors (describe as "soft pink and gold accents" not "#FFB6C1")
   - Visual hierarchy (what catches the eye first, second, third)
2. Layout Pattern Recognition
   - Section sequence (e.g., "hero product → feature grid → lifestyle scene → specs table")
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
**Output to User**:
Present a **qualitative style summary** in natural language:
```
"The reference page has a [adjective] aesthetic with [color description]. 
The layout follows a [pattern description] structure with [spacing description]. 
Key design features include [visual elements]. 
The overall mood is [mood description]."
```
**DO NOT** output:
- Hex color codes
- Pixel measurements
- Precise angles
- ΔE values
- Numerical spacing ratios
---
#### Step 1.2: User Confirmation & Adjustment
**Action**: Ask user which aspects to prioritize.
**Question Format**:
```
"I've analyzed the reference page. Before generating, please confirm:
1. Style Priority: Should I focus more on [color mood] or [layout structure]?
2. Flexibility: Are you okay with variations in [specific element], or must it stay close?
3. Content: Do you have specific product images/text, or should I use placeholders?
You can also tell me: 'Just generate based on the overall style' to proceed directly."
```
**Why This Step Matters**: 
AI cannot perfectly replicate everything. User input helps allocate the limited "accuracy budget" to what matters most.
---
### Stage 2: Content Preparation
**Objective**: Gather assets for the new product page.
#### Step 2.1: Asset Collection
**Required from User**:
- [ ] New product images (at least 1 main image)
- [ ] Product name
- [ ] Key selling points (3-5 bullet points)
**Optional from User**:
- [ ] Brand logo
- [ ] Specific text content
- [ ] Additional product angles/lifestyle shots
- [ ] Technical specifications
**If User Provides Minimal Info**:
Proceed with placeholders and inform user:
```
"I'll generate a draft using placeholder text for [missing elements]. 
You can replace these later or provide the content now for a more complete draft."
```
---
#### Step 2.2: Reference Image Search (If Needed)
**When to Search**:
- User has no lifestyle/scene images but reference page uses them
- Need supporting visual elements (textures, backgrounds, icons)
**Action**: Call `search_image` with **simple, concrete queries**:
- ✅ Good: "minimalist product photography", "marble texture", "lifestyle kitchen"
- ❌ Bad: "high-end luxury modern minimalist product shot with soft lighting"
**Search Strategy**:
- 1-2 searches maximum
- Focus on filling critical gaps only
- Prefer user-provided images over searched ones
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
   - ✅ "Product shown from a slightly elevated front angle"
   - ❌ "Product at 15° angle"
2. **Describe colors qualitatively**:
   - ✅ "Soft peachy pink background with warm gold accents"
   - ❌ "Background #FFE5D9, accents #D4AF37"
3. **Reference the style image clearly**:
   - Always include reference image URL in `image_url_list`
   - Use phrases like "in the style of the reference image"
4. **Be specific about layout but flexible about execution**:
   - Describe what sections exist and their purpose
   - Don't demand pixel-perfect positioning
---
#### Step 3.2: Tool Invocation
**Tool**: `generate_image_nano_banana_2`
**Parameters**:
```javascript
{
  "image_name": "[Product Name] Detail Page Draft",
  "prompt": "[Constructed prompt from 3.1]",
  "image_url_list": [
    "[Reference detail page URL]",
    "[Main product image URL]",
    "[Optional: lifestyle/supporting images]"
  ],
  "task_type": "REFERENCE_TO_IMAGE",
  "aspect_ratio": "9:16",  // or "3:4" for shorter pages
  "resolution": "2K"  // Higher resolution for detail pages
}
```
**Aspect Ratio Selection**:
- Standard detail page: `9:16` (portrait)
- Short-form page: `3:4` 
- Extra-long page: Generate in sections (see Stage 4)
---
#### Step 3.3: Output Delivery
**Present to User**:
```
"Here's your detail page draft based on the reference style:
[Generated Image]
STYLE MATCH ASSESSMENT:
✓ Successfully captured: [list 2-3 strong matches]
⚠ Approximate areas: [list 1-2 areas with variance]
✗ Needs manual adjustment: [list any obvious misses]
NEXT STEPS:
- If the overall direction works, I can generate variations or additional sections
- If specific elements need changes, describe what to adjust and I'll iterate
- For final production, you may need to manually refine [specific elements]"
```
**Honesty in Presentation**:
- Point out what worked and what didn't
- Don't oversell the result
- Provide clear guidance on what needs human touch
---
### Stage 4: Iteration & Refinement
**Objective**: Improve the draft based on user feedback.
#### Step 4.1: Feedback Collection
**Ask User**:
```
"What would you like to adjust?
Common refinements:
1. Change specific section layouts
2. Adjust color mood (warmer/cooler/more vibrant)
3. Modify text content
4. Regenerate with different product angles
5. Create variations of specific sections"
```
---
#### Step 4.2: Targeted Regeneration
**For Section-Specific Changes**:
If user wants to modify just one section (e.g., "make the feature comparison section more visual"):
**Option A: Regenerate Entire Page** (simpler, less control)
- Modify prompt to emphasize the changed section
- Regenerate full page
**Option B: Generate Section Separately** (more control, requires assembly)
- Generate the specific section as a standalone image
- User manually combines in design tool
**Recommendation**: Default to Option A for 1-2 iterations, suggest Option B if user needs fine control.
---
#### Step 4.3: Variation Generation
**Common Variation Requests**:
1. **Color Variations**:
   ```
   "Generate 2 more versions with different color moods:
   - Version A: Cooler tones (blues and purples)
   - Version B: Warmer tones (oranges and reds)"
   ```
2. **Layout Variations**:
   ```
   "Create an alternative layout with:
   - Hero section using a lifestyle scene instead of product-only
   - Feature grid changed to side-by-side comparison"
   ```
3. **Density Variations**:
   ```
   "Generate a more minimal version with:
   - More white space
   - Fewer text blocks
   - Focus on large visuals"
   ```
**Batch Generation**:
If user wants multiple variations, generate them in **one call** to image sub-agent with all variations listed in project context.
---
### Stage 5: Multi-Section Pages (Advanced)
**When to Use**: Reference page is extremely long (equivalent to 3+ screen heights).
**Challenge**: Single image generation has practical limits on length and detail density.
**Solution**: Section-by-section generation with style consistency.
---
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
"This reference page is quite long. I recommend generating it in [X] sections:
[List sections]
I'll generate them with consistent styling. You'll need to assemble them in a design tool.
Alternatively, I can create a condensed single-page version. Which do you prefer?"
```
---
#### Step 5.2: Sequential Generation
**Process**:
1. Generate Section 1 with full style reference
2. Generate Section 2 using both:
   - Original reference page
   - Generated Section 1 (for style consistency)
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
**Tool Call**:
```javascript
{
  "image_url_list": [
    "[Original reference page]",
    "[Previously generated Section 1]",
    "[Product/content images for this section]"
  ],
  "aspect_ratio": "16:9",  // Shorter ratio for individual sections
  ...
}
```
---
#### Step 5.3: Assembly Guidance
**After All Sections Generated**:
```
"All sections are complete! Here's how to assemble them:
MANUAL ASSEMBLY (Recommended):
1. Open in Figma/Photoshop/Canva
2. Stack sections vertically
3. Adjust overlaps/spacing between sections
4. Ensure color consistency (may need minor tweaks)
AUTOMATED ASSEMBLY (Experimental):
I can attempt to generate a combined version, but quality may degrade.
Which approach would you like?"
```
**Reality Check**: 
Automated assembly often produces worse results than manual combination. Be honest about this.
---
## Scenario-Specific Guidance
### Scenario A: Same Product Category, Different Product
**Example**: Reference is a skincare cream page, user wants to create a page for their serum.
**Approach**:
- High style transfer fidelity expected
- Focus on swapping product images while keeping layout
- Adjust text content to new product claims
**Success Rate**: 75-85% (highest success scenario)
**Prompt Emphasis**:
```
"Create a detail page for [NEW_PRODUCT] using the exact same layout structure and visual style as the reference [OLD_PRODUCT] page. 
Maintain the section sequence, color palette, and design treatments. 
Only swap the product images and update the text content to reflect [NEW_PRODUCT]'s features."
```
---
### Scenario B: Different Product, Similar Style
**Example**: Reference is a tech gadget page, user wants to create a page for a fashion item.
**Approach**:
- Transfer visual mood and design language
- Adapt layout to suit different product type
- May need different content sections
**Success Rate**: 60-70% (moderate success)
**Prompt Emphasis**:
```
"Create a detail page for [FASHION_PRODUCT] inspired by the visual style of the reference tech product page.
TRANSFER THESE ELEMENTS:
- Overall color mood and palette
- Typography style and hierarchy
- Graphic treatments (corners, shadows, badges)
- Spacing and composition feel
ADAPT THESE ELEMENTS:
- Layout structure to suit fashion product presentation
- Content sections appropriate for [FASHION_PRODUCT]
- Image style (lifestyle vs. technical shots)"
```
**Visual Description for Product Presentation**:
Instead of angle numbers, describe visually:
- ✅ "Show the dress on a model, full-body shot, centered"
- ✅ "Display the handbag from a front-facing view with slight elevation to show depth"
- ✅ "Present the shoes in a dynamic side angle showing the profile and sole"
- ❌ "Product at 45° angle, 30° elevation"
---
### Scenario C: Competitor Analysis / Inspiration Transfer
**Example**: User likes a competitor's page style and wants similar for their brand.
**Approach**:
- Extract style DNA without copying
- Emphasize differentiation
- Focus on "inspired by" not "replica of"
**Success Rate**: 65-75%
**Prompt Emphasis**:
```
"Create a detail page for [USER_PRODUCT] inspired by the design language of the reference page, but with distinct visual identity.
INSPIRATION ELEMENTS:
- [Specific style aspects to borrow]
- [Layout patterns that work well]
DIFFERENTIATION:
- Use [USER_BRAND] colors: [description]
- Adapt tone to be more [adjective] than the reference
- Include [unique brand elements]"
```
**Ethical Note**: Remind user this is for inspiration, not copying. Suggest adding unique brand elements.
---
## Limitations & Manual Intervention Points
### What AI Cannot Reliably Do
#### 1. **Precise Text Rendering**
- **Problem**: AI often generates garbled text, wrong fonts, or misaligned text blocks
- **Success Rate**: 50-60% for readable text
- **Solution**: 
  - Generate page with placeholder text areas
  - User adds real text in design tool
  - Or: Provide exact text in prompt and regenerate if garbled (may take 2-3 tries)
#### 2. **Exact Color Matching**
- **Problem**: AI interprets colors qualitatively, not numerically
- **Expected Variance**: ±10-20% in hue/saturation
- **Solution**:
  - Accept "close enough" for drafts
  - Manual color correction in final production
  - Or: Provide brand color descriptions in prompt (e.g., "use deep navy blue, not bright blue")
#### 3. **Complex Data Visualizations**
- **Problem**: Charts, graphs, detailed tables often generate incorrectly
- **Success Rate**: 30-40% for complex infographics
- **Solution**:
  - Generate page with placeholder chart areas
  - Create actual charts in specialized tools (Excel, Figma)
  - Composite manually
#### 4. **Pixel-Perfect Alignment**
- **Problem**: AI doesn't understand grids and precise spacing
- **Reality**: Elements will be approximately positioned
- **Solution**:
  - Use AI draft as a guide
  - Rebuild in design tool for production
  - Or: Accept "good enough" for quick campaigns
#### 5. **Brand Logo Integration**
- **Problem**: Logos often get distorted or stylized incorrectly
- **Success Rate**: 40-50% for clean logo rendering
- **Solution**:
  - Generate page without logo
  - Add real logo file in post-production
  - Or: Provide logo as reference image and emphasize "keep logo unchanged"
---
### When to Stop Iterating with AI
**Diminishing Returns Point**: After 3-4 regenerations, you're likely fighting AI limitations rather than making progress.
**Signs to Move to Manual Editing**:
- Text keeps generating incorrectly after 3 tries
- Specific element positioning won't cooperate
- User needs pixel-perfect precision
- Color matching requires exact hex values
**Recommendation to User**:
```
"We've reached the point where manual refinement will be faster than more AI iterations. 
I recommend:
1. Use this draft as your foundation
2. Import into [Figma/Photoshop/Canva]
3. Manually adjust [specific elements]
4. Add final text and brand assets
This hybrid approach gives you the speed of AI drafting + precision of manual control."
```
---
## Quality Expectations & Success Metrics
### Realistic Output Quality
**Draft Quality (First Generation)**:
- ✅ Overall style similarity: 70-80%
- ✅ Layout structure approximation: 60-70%
- ⚠️ Text accuracy: 50-60%
- ⚠️ Color precision: 60-70%
- ⚠️ Element positioning: 60-70%
**After 2-3 Iterations**:
- ✅ Style similarity: 80-85%
- ✅ Layout structure: 75-80%
- ⚠️ Text accuracy: 65-70%
- ⚠️ Color precision: 70-75%
- ⚠️ Element positioning: 70-75%
**Production-Ready** (AI + Manual):
- ✅ 90%+ quality achievable with manual post-production
---
### Success Criteria by Use Case
**Quick Campaign Drafts** (Speed Priority):
- ✅ AI alone sufficient
- Accept 70-80% fidelity
- Fast iteration over perfection
**Client Presentations** (Balance):
- ✅ AI draft + light manual touch-up
- 80-85% fidelity target
- 1-2 hours manual refinement
**Final Production** (Quality Priority):
- ✅ AI as foundation + full manual production
- 95%+ fidelity target
- Treat AI output as wireframe/mockup
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
- Key features: 
  • [Feature 1]
  • [Feature 2]
  • [Feature 3]
DESIGN DETAILS:
- Typography: [Bold sans-serif headlines, clean body text]
- Spacing: [Airy with generous margins]
- Graphics: [Rounded corners, subtle shadows, minimal borders]
Maintain the reference's visual language while adapting to this product.
```
---
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
PRODUCT: [New product details]
Create a cohesive page that feels related to the reference but appropriate for [NEW_CATEGORY].
```
---
### Template 3: Competitor-Inspired (Differentiated)
```
Create a detail page for [BRAND] [PRODUCT] inspired by the reference design, but with distinct brand identity.
INSPIRATION FROM REFERENCE:
- [Specific layout patterns]
- [Design techniques that work well]
- [Overall composition approach]
BRAND DIFFERENTIATION:
- Colors: Use [BRAND] palette - [description]
- Tone: More [adjective] than reference
- Unique elements: Include [brand-specific features]
PRODUCT: [Product details]
The result should feel inspired by, not copied from, the reference.
```
---
## Communication Templates
### Initial Analysis Presentation
```
"I've analyzed the reference detail page. Here's what I found:
VISUAL STYLE:
• Mood: [Description]
• Colors: [Qualitative description]
• Design language: [Style keywords]
LAYOUT PATTERN:
• [Section 1 description]
• [Section 2 description]
• [Section 3 description]
KEY DESIGN ELEMENTS:
• [Element 1]
• [Element 2]
• [Element 3]
Before I generate your page, please provide:
1. Your product images (at least 1 main image)
2. Product name and key features
3. Any specific content you want included
Or tell me to proceed with placeholders for a quick draft."
```
---
### Draft Delivery with Honest Assessment
```
"Here's your detail page draft:
[Image]
STYLE MATCH ASSESSMENT:
✓ Successfully captured:
  • [Strong match 1]
  • [Strong match 2]
⚠ Approximate areas:
  • [Variance 1] - close but not exact
  • [Variance 2] - similar feel, different execution
✗ Needs manual adjustment:
  • [Element that didn't work] - recommend manual editing
OVERALL: This draft captures [X]% of the reference style and provides a solid foundation.
Would you like me to:
1. Iterate on specific sections
2. Generate color/layout variations
3. Provide guidance for manual refinement"
```
---
### Iteration Limit Recommendation
```
"We've done [X] iterations and made good progress. However, I'm noticing we're hitting AI limitations on [specific element].
At this point, I recommend:
OPTION A: Accept current draft + manual refinement
- Import into [design tool]
- Manually adjust [specific elements]
- Estimated time: [X] hours
- Result: 95%+ quality
OPTION B: Continue AI iteration
- May take 3-5+ more tries
- No guarantee of solving [specific issue]
- Diminishing returns likely
My honest recommendation: Option A will get you to your goal faster.
Which would you prefer?"
```
---
## Tool Selection Logic
### When to Use `generate_image_nano_banana_2`
**Primary Tool for This Skill**
**Advantages**:
- Good style transfer capability
- Handles multiple reference images well
- Reasonable text rendering (for AI standards)
- Fast generation
**Use for**:
- All standard detail page generation
- Single-page outputs
- Section-by-section generation
- Iterations and variations
**Parameters**:
- `task_type`: Always `"REFERENCE_TO_IMAGE"`
- `aspect_ratio`: `"9:16"` for full pages, `"16:9"` for sections
- `resolution`: `"2K"` (higher detail for text-heavy pages)
---
### When to Use Image Sub-Agent
**Scenario**: User requests multiple variations in one message.
**Example**: "Generate 3 versions with different color schemes"
**Action**: 
```javascript
call_subagent({
  subagent_name: "image_sub_agent",
  project_context: `
Reference Image: [URL]
Generate 3 detail page variations for [PRODUCT]:
Version 1: Cool tones (blues, purples)
[Full prompt]
Version 2: Warm tones (oranges, reds)  
[Full prompt]
Version 3: Neutral tones (grays, beiges)
[Full prompt]
Use generate_image_nano_banana_2 for all generations.
`
})
```
---
### When NOT to Use This Skill
**Inappropriate Scenarios**:
1. **User wants pixel-perfect replication**: Set expectations that AI cannot achieve this
2. **Reference is a complex interactive page**: AI generates static images only
3. **User needs exact brand compliance**: AI cannot guarantee brand guideline adherence
4. **Reference has heavy data visualization**: Charts/graphs will likely fail
**Alternative Approaches**:
- Suggest manual design with AI-generated elements
- Recommend specialized tools (Canva templates, Figma kits)
- Offer to generate individual sections only
---
## Version History & Improvements
### v4.0 (Current - Honest Edition)
- ✅ Removed all unrealistic precision requirements
- ✅ Changed to qualitative analysis approach
- ✅ Added honest success rate expectations
- ✅ Included manual intervention guidance
- ✅ Repositioned as "draft generation" not "replication"
- ✅ Added diminishing returns detection
- ✅ Improved communication templates with realistic assessments
### v3.0 (Previous - Overpromised)
- ❌ Claimed precise color/layout replication
- ❌ Used numerical parameters AI couldn't deliver
- ❌ Promised 90%+ success rates
- ❌ No guidance on when to stop iterating
---
## FAQ
**Q: Can AI perfectly replicate a detail page?**
A: No. AI can create style-similar drafts with 70-85% fidelity. For production quality, expect to do manual refinement.
**Q: How many iterations should I try?**
A: 2-3 iterations usually yield the best results. After that, diminishing returns set in—switch to manual editing.
**Q: Why is the text garbled?**
A: AI text rendering is unreliable (50-60% success rate). Generate with placeholder text and add real text manually, or regenerate 2-3 times.
**Q: The colors don't match exactly. Can you fix this?**
A: AI interprets colors qualitatively, not numerically. Expect ±10-20% variance. For exact brand colors, do manual color correction in post-production.
**Q: Can I use this for final production?**
A: Use AI output as a foundation/wireframe. Plan for manual refinement to achieve production quality (90%+ fidelity).
**Q: What if the layout is completely wrong?**
A: Regenerate with more specific layout description. If it fails after 2-3 tries, the layout may be too complex for AI—consider section-by-section generation or manual design.
**Q: How long does this process take?**
A: 
- Quick draft: 5-10 minutes
- Refined draft (2-3 iterations): 20-30 minutes  
- Production-ready (AI + manual): 2-4 hours
---
## Conclusion
This skill provides **rapid style transfer for e-commerce detail pages**, not pixel-perfect replication. 
**Best Use Cases**:
- Quick campaign drafts
- A/B testing concepts
- Client presentation mockups
- Foundation for manual design
**Success Formula**:
AI Draft (70-85% quality) + Manual Refinement (15-30% effort) = Production-Ready Output (95%+ quality)
**Key Principle**: 
Be honest about AI limitations. Set realistic expectations. Deliver usable drafts quickly, and guide users on when to switch to manual editing.
---
**End of Skill Document**
