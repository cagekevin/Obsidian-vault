"""
导出脚本：project.json → output/ 提示词文件
默认全量生成：分组分镜板 + 全片总览 + 图片单帧 + 参考图
用法：
    python3 export.py [项目目录]
    python3 export.py [项目目录] --html
    python3 export.py [项目目录] --input project_pixar.json
    python3 export.py [项目目录] --input project_pixar.json --html
"""

import json, os, sys, argparse, re, webbrowser, platform

parser = argparse.ArgumentParser()
parser.add_argument("project_dir", nargs="?", default=".", help="项目目录")
parser.add_argument("--html", action="store_true", help="额外生成 HTML")
parser.add_argument("--input", default="project.json", help="输入的 JSON 文件名，默认 project.json")
args = parser.parse_args()

project_dir = args.project_dir
input_name = args.input
INPUT = os.path.join(project_dir, input_name)

# 检查输入文件是否存在
if not os.path.isfile(INPUT):
    print(f"❌ 错误：找不到输入文件 {INPUT}")
    print(f"   当前项目目录：{os.path.abspath(project_dir)}")
    sys.exit(1)

# 读取并解析 JSON
try:
    with open(INPUT, 'r', encoding='utf-8') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"❌ 错误：JSON 解析失败 — {e}")
    print(f"   文件：{INPUT}")
    print(f"   行 {e.lineno}，列 {e.colno}：{e.msg}")
    sys.exit(1)
except FileNotFoundError:
    print(f"❌ 错误：找不到文件 {INPUT}")
    sys.exit(1)

# 按输入文件名确定输出目录和风格标签
base = os.path.splitext(input_name)[0]
if base == "project":
    OUTPUT_DIR = os.path.join(project_dir, "output")
    style_tag = "original"
else:
    style_tag = base.replace("project_", "")
    OUTPUT_DIR = os.path.join(project_dir, f"output_{style_tag}")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 清理输出目录（仅限已知导出文件类型）
ALLOWED_EXTENSIONS = {".txt", ".md", ".html"}
for f in os.listdir(OUTPUT_DIR):
    fp = os.path.join(OUTPUT_DIR, f)
    ext = os.path.splitext(f)[1].lower()
    if os.path.isfile(fp) and ext in ALLOWED_EXTENSIONS:
        os.remove(fp)

project_name = os.path.basename(os.path.abspath(project_dir))

vs = data.get("visual_style", "")
frame_aspect = data.get("frame_aspect_ratio", "")
elements = data.get("elements", [])
groups = data.get("storyboard_groups", [])

file_seq = 0
storyboard_count = 0
ref_count = 0

all_scenes = []
for g in groups:
    all_scenes.extend(g.get("scenes", []))

def safe_name(name):
    text = str(name or "").strip().lower().replace(" ", "-")
    text = re.sub(r'[\\/:"*?<>|]+', "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "element"

def reference_file_name(el):
    name = el.get("name", "element")
    if el.get("is_background"):
        return f"ref_bg_{safe_name(name)}.txt"
    return f"ref_{safe_name(name)}.txt"

# 判断元素是否出参考图（默认 true）
def is_reference(el):
    return el.get("reference", True) is not False

def write_board(scenes, label, is_overview=False):
    global file_seq, storyboard_count
    file_seq += 1
    lines = []
    lines.append("IMPORTANT: Generate exactly ONE single image containing an animation pre-production board layout, full grid layout with clearly labeled sections. Do NOT generate separate images.")
    lines.append("")
    lines.append("VISUAL HIERARCHY: Storyboard frames are PRIMARY — allocate the largest and most detailed area to these narrative panels. Character reference is SECONDARY — compact sidebar thumbnails. Scene diagram and direction bar are SUPPLEMENTARY — small minimal elements. Let the visual weight naturally reflect this priority order.")
    lines.append("")
    lines.append(f"Director style: {vs}")
    lines.append("")
    lines.append("STORYBOARD FRAMES (main area, grid layout, largest section):")
    for si, s in enumerate(scenes):
        desc = (s.get("storyboard_desc") or s.get("description", "")).replace('\n', ' ')
        title = s.get("title", "")
        if title:
            lines.append(f"Frame {str(si+1).zfill(2)}: 'Shot {str(si+1).zfill(2)} — {title}. {desc}'")
        else:
            lines.append(f"Frame {str(si+1).zfill(2)}: '{desc}'")
    if frame_aspect:
        lines.append(f"Each frame box should be {frame_aspect} portrait aspect ratio (vertical rectangle, not square, not landscape).")
    lines.append("Each frame box has white thin border, small text label at bottom with shot number.")
    lines.append("")
    scene_nums = [s.get("scene_num", i+1) for i, s in enumerate(scenes)]
    titles = [s.get("title", "") for s in scenes]
    if all(titles):
        title_chain = "→".join(titles)
        lines.append(f"TOP BAR: '{len(scenes)}镜：{label}（{title_chain}）'")
    else:
        lines.append(f"TOP BAR: '{len(scenes)}镜：{label}（镜头 {scene_nums[0]}-{scene_nums[-1]}）'")
    lines.append("")
    lines.append("SECTION 3 - SCENE DESIGN (below character panel, compact):")
    if is_overview:
        cam_parts = []
        for g in groups:
            tag = g.get("label", "")
            cam_parts.append(tag)
        cam_arc = " → ".join(cam_parts)
    else:
        if all(titles):
            cam_arc = " → ".join(titles)
        else:
            cam_arc = f"{label}"
    lines.append("Top-down floor plan view of camera path.")
    lines.append(f"Camera arc: '{cam_arc}'")
    lines.append("Dotted line with directional arrows connecting shot positions.")
    lines.append("Shot numbers labeled at each camera position.")
    lines.append("")
    lines.append("Overall layout: cohesive animation pre-production board, all text in clean sans-serif font, white or very light cream background, thin grid lines separating sections.")
    lines.append("")
    # 确定本组出镜元素列表（全片总览显示全部）
    group_refs = None
    if not is_overview:
        for sg in groups:
            if sg.get("scenes") == scenes:
                group_refs = sg.get("element_refs", None)
                break
    if group_refs is not None:
        all_shown = [e for e in elements if e.get("name") in group_refs]
    else:
        all_shown = [e for e in elements]
    # 按是否出参考图分开
    shown = [e for e in all_shown if not e.get("is_background") and is_reference(e)]
    bg_shown = [e for e in all_shown if e.get("is_background") and is_reference(e)]
    # 仅标注不出参考图的元素（纯说明）
    shown_brief = [e for e in all_shown if not is_reference(e)]
    if shown:
        lines.append("CHARACTER REFERENCE (compact sidebar):")
        for el in shown:
            en = el.get("english_name") or el.get("name", "")
            a = el.get("appearance", "")
            lines.append(f"-- {en}: {a}")
        lines.append("")
    if bg_shown:
        lines.append("ENVIRONMENT REFERENCE (compact sidebar):")
        for el in bg_shown:
            en = el.get("english_name") or el.get("name", "")
            a = el.get("appearance", "")
            lines.append(f"-- {en}: {a}")
        lines.append("")
    lines.append("CONSISTENCY RULE: ALL visual elements in the storyboard frames below MUST match the corresponding reference images EXACTLY. The same element must look IDENTICAL across every frame — same color, shape, material, proportions.")
    lines.append("")
    if all_shown:
        lines.append("----------------------------------------------------------------------------------------------------")
        lines.append("以上 prompt 已完整，直接复制即可生图。")
        ref_els = [e for e in all_shown if is_reference(e)]
        if ref_els:
            lines.append("")
            lines.append("⚠️ 如需跨分镜板视觉一致，用参考图锁定风格：")
            for el in ref_els:
                lines.append(f"  → 生图后拖入上传区域：{reference_file_name(el)}（{el['name']}）")
            lines.append("（不传也不影响出图）")
        brief_els = [e for e in all_shown if not is_reference(e)]
        if brief_els:
            lines.append("")
            lines.append(f"本组出现：{'、'.join(e['name'] for e in brief_els)}（外观已内嵌在 prompt 中，无需额外参考图）")
    fname = f"{str(storyboard_count+1).zfill(2)}_storyboard_{label.replace(' ', '-')}.txt"
    out = os.path.join(OUTPUT_DIR, fname)
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"{os.path.abspath(out)}\n")
    storyboard_count += 1

# 分组分镜板
for gi, g in enumerate(groups):
    write_board(g.get("scenes", []), g.get("label", f"group-{gi+1}"))

# 全片总览
write_board(all_scenes, "全片总览", is_overview=True)

# 图片单帧
image_shot_count = 0
for s in all_scenes:
    num = s.get("scene_num", 0)
    lines = []
    lines.append(f"Director style: {vs}")
    lines.append("")
    lines.append("DESCRIPTION:")
    lines.append(s.get("description", "").replace('\n', ' '))
    lines.append("")
    lines.append(f"CAMERA: {s.get('camera', '')}")
    lines.append("")
    lines.append("Generate exactly ONE single image of this scene.")
    title_part = s.get("title", "")
    fname = f"image_{str(num).zfill(2)}_{safe_name(title_part) if title_part else str(num).zfill(2)}.txt"
    out = os.path.join(OUTPUT_DIR, fname)
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"{os.path.abspath(out)}\n")
    image_shot_count += 1

# 视频镜头
video_shot_count = 0
for s in all_scenes:
    num = s.get("scene_num", 0)
    desc = s.get("description", "").replace('\n', ' ')
    cam = s.get("camera", "")
    title = s.get("title", "")
    lines = []
    lines.append("REFERENCE:")
    s_groups = [g for g in groups if s in g.get("scenes", [])]
    s_elems = []
    if s_groups:
        refs = s_groups[0].get("element_refs", [])
        s_elems = [e for e in elements if e.get("name") in refs]
    if s_elems:
        for el in s_elems:
            name = el.get("name", "")
            lines.append(f"Use @{name} as reference.")
    lines.append(f"Use the matching image_{str(num).zfill(2)}_*.txt for visual lock.")
    lines.append("")
    lines.append("FIRST FRAME:")
    lines.append(desc)
    lines.append("")
    lines.append("ACTION:")
    # 从 description 提取动作词（动词 + 后续上下文，最长 20 词）
    action_verbs = ["floating", "drifting", "rising", "falling", "rotating", "spinning",
                    "glowing", "pulsing", "expanding", "contracting", "moving", "walking",
                    "running", "flying", "jumping", "turning", "reaching", "touching",
                    "climbing", "sliding", "swinging", "bouncing", "flowing", "melting",
                    "fading", "emerging", "dissolving", "transforming", "opening", "closing"]
    desc_words = desc.split()
    action_parts = []
    for i, w in enumerate(desc_words):
        w_lower = w.lower().strip(".,;:!?")
        if w_lower in action_verbs:
            chunk = " ".join(desc_words[i:min(i+15, len(desc_words))])
            action_parts.append(chunk)
            break
    if action_parts:
        lines.append(action_parts[0])
    else:
        lines.append("[Motion and transformation to unfold over this shot]")
    lines.append("")
    lines.append(f"CAMERA MOTION: {cam}")
    lines.append("")
    lines.append("CONTINUITY:")
    lines.append("Keep all recurring characters, objects, wardrobe, colors, proportions, and environments consistent with the reference sheets and previous shots.")
    lines.append("")
    lines.append("DURATION: 3 seconds")
    lines.append("")
    lines.append("AVOID:")
    lines.append("no text, no logo, no subtitles, no character redesign, no sudden scene change, no extra limbs, no flickering identity")
    title_part = s.get("title", "")
    fname = f"video_{str(num).zfill(2)}_{safe_name(title_part) if title_part else str(num).zfill(2)}.txt"
    out = os.path.join(OUTPUT_DIR, fname)
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"{os.path.abspath(out)}\n")
    video_shot_count += 1

# 分组视频 prompt（整组一起生成视频）
group_video_count = 0
for gi, g in enumerate(groups):
    scenes = g.get("scenes", [])
    label = g.get("label", f"group-{gi+1}")
    if not scenes:
        continue
    lines = []
    lines.append(f"VIDEO — {label}")
    lines.append("")
    lines.append(f"Duration: ~9 seconds total ({len(scenes)} continuous shots)")
    lines.append("")
    for si, s in enumerate(scenes):
        num = s.get("scene_num", 0)
        title = s.get("title", "")
        desc = s.get("description", "").replace('\n', ' ')
        cam = s.get("camera", "")
        lines.append(f"Shot {str(si+1).zfill(2)}: {title}" if title else f"Shot {str(si+1).zfill(2)}:")
        lines.append(f"  {desc}")
        if cam:
            lines.append(f"  Camera: {cam}")
        lines.append("")
        # 镜头间过渡
        if si < len(scenes) - 1:
            next_desc = scenes[si+1].get("description", "")
            next_cam = scenes[si+1].get("camera", "")
            if next_desc.lower().startswith("same"):
                lines.append("  → same frame, state transitions (e.g. redness heals)")
            elif "pull" in cam.lower() and "fixed" in next_cam.lower():
                lines.append("  → movement settles into static frame")
            else:
                lines.append("  → cut to next shot")
            lines.append("")
        else:
            if any(kw in desc.lower() for kw in ["frozen", "idle", "breathing", "stays", "slow motion"]):
                lines.append("  → gentle fade to end")
                lines.append("")
    # CONTINUITY: 保持通用 + 加入该组 element 提及
    lines.append("CONTINUITY:")
    refs = g.get("element_refs", [])
    if refs:
        for r in refs:
            el = next((e for e in elements if e.get("name") == r), None)
            if el:
                en = el.get("english_name") or r
                lines.append(f"  - {en}: consistent across all shots in this group")
        lines.append("")
    lines.append("  Keep visual style, color palette, and lighting consistent across all shots. Transitions should be seamless.")
    lines.append("")
    lines.append("CONSTRAINT: no text, no logo, no subtitle, no brand watermark, no sudden scene breaks between shots")
    fname = f"video_group_{str(gi+1).zfill(2)}_{label.replace(' ', '-')}.txt"
    out = os.path.join(OUTPUT_DIR, fname)
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"{os.path.abspath(out)}\n")
    group_video_count += 1


# 参考图
for idx, el in enumerate(elements):
    if not is_reference(el):
        continue
    name = el.get("name", f"element-{idx}")
    en_name = el.get("english_name") or name
    appearance = el.get("appearance", "")
    is_bg = el.get("is_background", False)
    if is_bg:
        prompt = f"""Generate exactly ONE single image containing an ENVIRONMENT CONCEPT SHEET for 3D animation reference.
This is a scene design reference.
STYLE: {vs}
ENVIRONMENT:
{appearance}
LAYOUT — multiple views on one canvas, arranged by visual priority:
- PRIMARY (largest area): main camera angle, full atmospheric shot
- FLOOR PLAN (compact inset): top-down view
- TERTIARY VIEWS (1-2 small insets): side or reverse angle
- Clean white background, thin grid lines between views
Generate exactly ONE environment concept sheet with multiple views.

Positive constraint: empty environment, no people, no characters, no human figures — environment only."""
        fname = f"ref_bg_{safe_name(name)}.txt"
    else:
        label = "MAIN CHARACTER" if idx == 0 else "SECONDARY CHARACTER"
        prompt = f"""Generate exactly ONE single image containing a CHARACTER CONCEPT SHEET for 3D animation reference — {label}.
STYLE: {vs}
CHARACTER: {en_name}
APPEARANCE:
{appearance}
LAYOUT — multiple views on one canvas:
- PRIMARY VIEW (largest area): front-facing, best-lit, showing all details
- PORTRAIT INSET (compact): face close-up
- ALTERNATE ANGLES (2-3 smaller): side profile, 3/4 view, back view
- EXPRESSION VARIANTS (3-4 small panels): neutral, happy, surprised, intense
- Clean white background, thin grid lines between panels
- All views must show the same character — consistent color, shape, proportions
Generate exactly ONE character concept sheet with multiple views and expressions.

Positive constraint: pure white seamless background, only the character, clothing and personal accessories — no environmental objects, no background setting."""
        fname = f"ref_{safe_name(name)}.txt"
    # 垫图说明（横线分隔，不干扰复制按钮的 split 逻辑）
    role_type = "场景" if is_bg else "角色"
    # appearance 本身末尾已有标点，不再追加句号
    ref_note = f"\n\n----------------------------------------------------------------------------------------------------\n\n我上传的第__张图是故事里的{name}{role_type}，{appearance} Please generate the video strictly following my reference image."
    full_content = prompt.strip() + ref_note
    out = os.path.join(OUTPUT_DIR, fname)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(full_content)
    print(f"{os.path.abspath(out)}\n")
    ref_count += 1

# QC Report
qc_warnings = []
qc_notes = []
qc_errors = []
# 1. visual_style
if not vs or vs == "[]":
    qc_warnings.append("visual_style is empty.")
# 2. elements 完整性检查
element_names = set()
for el in elements:
    en = el.get("name", "")
    ename = el.get("english_name", "")
    app = el.get("appearance", "")
    ib = el.get("is_background")
    element_names.add(en)
    if not en:
        qc_errors.append(f"Element missing name: {el}")
    if not ename:
        qc_errors.append(f"Element '{en}' missing english_name.")
    elif ename:
        # 检查 english_name 是否符合 M 姐资产命名规范
        allowed_prefixes = ("char_", "scene_", "product_", "prop_", "fx_", "other_")
        if not ename.lower().startswith(allowed_prefixes):
            qc_errors.append(
                f"Element '{en}' english_name ('{ename}') 不符合资产命名规范。"
                f" 必须以下列前缀开头：{', '.join(allowed_prefixes)}"
                f" （char_=角色, scene_=场景, product_=产品, prop_=道具, fx_=特效, other_=其他）"
            )
    if not app:
        qc_notes.append(f"Element '{en}' appearance is empty (non-reference element, no reference image needed).")
    if ib is None:
        qc_warnings.append(f"Element '{en}' is_background is not set.")
# 4. element_refs 引用检查
for gi, g in enumerate(groups):
    refs = g.get("element_refs", [])
    for r in refs:
        if r not in element_names:
            qc_errors.append(f"Group {gi+1} references missing element: '{r}'")
    if not refs:
        qc_warnings.append(f"Group {gi+1} ({g.get('label', '')}) has no element_refs.")
# 5. scene 编号连续性
all_nums = [s.get("scene_num", 0) for s in all_scenes]
for i in range(1, len(all_nums)):
    if all_nums[i] != all_nums[i-1] + 1:
        qc_warnings.append(f"Scene numbering jump: {all_nums[i-1]} → {all_nums[i]}")
        break
# 6. scene 字段缺失
for s in all_scenes:
    sn = s.get("scene_num", "?")
    if not s.get("description", "").strip():
        qc_errors.append(f"Scene {sn} description is empty.")
    if not s.get("camera", "").strip():
        qc_warnings.append(f"Scene {sn} camera is empty.")
    # 检查跨镜引用是否缺失 storyboard_desc
    desc = s.get("description", "")
    if re.search(r'scene\s+\d+', desc, re.IGNORECASE) and not s.get("storyboard_desc", "").strip():
        qc_errors.append(
            f"Scene {sn} description references 'scene {sn}' but has no 'storyboard_desc' field. "
            f"Storyboard frames are generated independently — they cannot reference other scenes. "
            f"Add a 'storyboard_desc' with a self-contained description for storyboard use."
        )
# 7. 中文残留检查
for s in all_scenes:
    sn = s.get("scene_num", "?")
    desc = s.get("description", "")
    if re.search(r'[\u4e00-\u9fff]', desc):
        qc_warnings.append(f"Scene {sn} description contains Chinese characters.")
# 8. 高风险品牌名检查
brand_words = ["Inside Out", "Kurzgesagt", "Apple Keynote", "Nintendo", "Disney",
               "Marvel", "Star Wars", "Pokemon"]
for s in all_scenes:
    sn = s.get("scene_num", "?")
    desc = s.get("description", "")
    for bw in brand_words:
        if bw.lower() in desc.lower():
            qc_errors.append(f"Scene {sn} contains brand name: '{bw}'")
# 9. 背景元素未被引用检查
for el in elements:
    if el.get("is_background"):
        en = el.get("name", "")
        used = False
        for g in groups:
            if en in g.get("element_refs", []):
                used = True
                break
        if not used:
            qc_warnings.append(f"Background element '{en}' is not referenced by any group.")
# 10. 描述长度波动检查
    desc_word_counts = [(s.get("scene_num", "?"), len(s.get("description", "").split())) for s in all_scenes]
    if len(desc_word_counts) >= 3:
        valid_counts = [c for _, c in desc_word_counts if c > 0]
        if valid_counts:
            avg_len = sum(valid_counts) / len(valid_counts)
            for sn, wc in desc_word_counts:
                if wc > 0 and wc < avg_len * 0.3:
                    qc_warnings.append(f"Scene {sn} description is notably short ({wc} words vs {avg_len:.0f} average). Possible detail loss.")
                    break

# 11. 术语一致性检查（跨 Scene 同一 element 叫法一致性）
    consistency_warnings = []
    for el in elements:
        if el.get("is_background"):
            continue
        ename = el.get("english_name", "")
        if not ename:
            continue
        ename_lower = ename.lower()
        # 提取出该元素的几个核心词
        core_words = set(ename_lower.split())
        # 扫描所有 scene description，找对该 element 的引用
        aliases = {}
        for s in all_scenes:
            sn = s.get("scene_num", 0)
            desc = s.get("description", "").lower()
            # 检查是否包含 core_words 中的 ≥ 1 个词
            found_words = [w for w in core_words if w in desc and len(w) > 2]
            if not found_words:
                continue
            # 取出该 Scene 中这组词附近的简短引用
            for w in found_words:
                idx = desc.find(w)
                if idx >= 0:
                    # 提取以该词为中心的 10 词片段作为"引用方式"
                    snippet_words = desc.split()
                    ref = ""
                    for si, sw in enumerate(snippet_words):
                        if w in sw.lower():
                            start = max(0, si - 1)
                            end = min(len(snippet_words), si + 2)
                            ref = " ".join(snippet_words[start:end])
                            break
                    if sn not in aliases:
                        aliases[sn] = set()
                    aliases[sn].add(ref)
        # 检查不同 Scene 之间是否使用了显著不同的引用词
        all_refs = []
        for sn, refs in aliases.items():
            for r in refs:
                all_refs.append((sn, r))
        if len(all_refs) >= 3:
            # 把引用方式按 Scene 分组
            ref_by_scene = {}
            for sn, r in all_refs:
                if sn not in ref_by_scene:
                    ref_by_scene[sn] = []
                ref_by_scene[sn].append(r)
            # 检查每个 Scene 的引用是否包含 core_words 中的词
            scene_missing_core = []
            for sn, refs in ref_by_scene.items():
                ref_text = " ".join(refs)
                has_core = any(w in ref_text for w in core_words if len(w) > 2)
                if not has_core:
                    scene_missing_core.append(sn)
            # 检查是否有引用核心词以外的叫法
            if scene_missing_core:
                consistency_warnings.append(
                    f"Element '{el.get('name', '')}' (english_name: '{ename}') "
                    f"referenced differently in Scene(s) {', '.join(map(str, scene_missing_core))}. "
                    f"Description there may use synonyms instead of the english_name's core terms."
                )

    for cw in consistency_warnings:
        qc_warnings.append(cw)

# 12. 描述压缩率检测（对比中文 storyboard 与英文 project.json 的细节密度）
    # 读取 storyboard.md（如存在）
    storyboard_path = os.path.join(project_dir, "storyboard.md")
    chinese_scenes = {}  # {scene_num: chinese_text}
    if os.path.isfile(storyboard_path):
        with open(storyboard_path, 'r', encoding='utf-8') as f:
            sb_content = f.read()
        # 用正则提取 Scene N 的中文描述段落
        scene_blocks = re.split(r'\n(?=##? Scene\s+\d)', sb_content)
        for block in scene_blocks:
            # 提取 Scene 编号
            sn_match = re.search(r'Scene\s+(\d+)', block, re.IGNORECASE)
            if not sn_match:
                continue
            sn = int(sn_match.group(1))
            # 提取中文文字（去除#标题、镜头行、英文标记）
            cn_lines = []
            for line in block.split('\n'):
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('>') or line.startswith('---'):
                    continue
                # 跳过"镜头："行（这些不是画面描述）
                if '镜头' in line or 'camera' in line.lower() or 'Camera' in line:
                    continue
                # 保留含中文的行
                if re.search(r'[一-鿿]', line):
                    cn_lines.append(line)
            cn_text = ' '.join(cn_lines)
            if cn_text.strip():
                chinese_scenes[sn] = cn_text

    # 如果找到了中文描述，对比每个 Scene 的中英文长度
    if chinese_scenes:
        for s in all_scenes:
            sn = s.get("scene_num", 0)
            en_desc = s.get("description", "").strip()
            cn_desc = chinese_scenes.get(sn, "")
            if not cn_desc or not en_desc:
                continue
            cn_words = len(cn_desc)
            en_words = len(en_desc.split())
            # 英文单词数 vs 中文字数：按 1 中文≈1.8 英文词折算
            expected_en = cn_words * 1.8
            ratio = en_words / expected_en if expected_en > 0 else 1
            if ratio < 0.5:
                # 仅有 1 个中文标点或纯标点的跳过
                cn_chars = len(re.sub(r'[\s，。、？！：；""''（）【】《》——…·　]', '', cn_desc))
                if cn_chars < 5:
                    continue
                qc_warnings.append(
                    f"Scene {sn} English description may have lost visual details "
                    f"({en_words} English words vs ~{int(expected_en)} expected from {cn_chars} Chinese chars, "
                    f"density ratio {ratio:.0%}). Check if visual detail was preserved."
                )

# 13. element_refs 交叉校验——检查元素在该组 description 中是否被实际提到
for gi, g in enumerate(groups):
    refs = g.get("element_refs", [])
    gname = g.get("label", f"group-{gi+1}")
    for r in refs:
        el = next((e for e in elements if e.get("name") == r), None)
        if not el:
            continue
        ename = el.get("english_name") or el.get("name", "")
        # 拆成单词，长度≥5才算（避免 "skin"、"face" 等短词误匹配）
        ename_words = [w.lower().strip(".,;:!?()") for w in ename.split() if len(w) >= 5]
        mentioned = False
        for s in g.get("scenes", []):
            desc = s.get("description", "").lower()
            for w in ename_words:
                if w in desc:
                    mentioned = True
                    break
            if mentioned:
                break
        if not mentioned:
            if is_reference(el):
                # 检查是否在其他组的描述中能匹配到（是的话说明只是本组描述用词问题）
                found_elsewhere = False
                for ogi, og in enumerate(groups):
                    if ogi == gi:
                        continue
                    for s in og.get("scenes", []):
                        desc = s.get("description", "").lower()
                        for w in ename_words:
                            if w in desc:
                                found_elsewhere = True
                                break
                        if found_elsewhere:
                            break
                    if found_elsewhere:
                        break
                msg = (
                    f"Group '{gname}' element_refs 含参考元素 '{r}'（{ename}），"
                    f"但该组所有场景的 description 均未明确提及"
                )
                if found_elsewhere:
                    qc_notes.append(f"{msg}（该元素在其他组中有匹配，可能仅为本组描述用语问题）")
                else:
                    qc_warnings.append(f"{msg}——如该元素确实不出现在本组画面中，请从 element_refs 移除，否则参考图锁定会错误")

# 14. 过锐/堆料词检查
sharp_words = ["HDR", "8K", "超高清", "高细节", "锐利", "ultra sharp", "hyper-detailed",
               "intricate", "繁复", "浓郁", "8k", "Ultra HD", "超高细节"]
for el in elements:
    en = el.get("name", "")
    app = el.get("appearance", "")
    for sw in sharp_words:
        if sw.lower() in app.lower():
            qc_warnings.append(f"Element '{en}' appearance 含过锐词 '{sw}'——替换为柔和描述（清晰/柔和/克制/干净通透）")
            break
for s in all_scenes:
    sn = s.get("scene_num", "?")
    desc = s.get("description", "")
    for sw in sharp_words:
        if sw.lower() in desc.lower():
            qc_warnings.append(f"Scene {sn} description 含过锐词 '{sw}'")
            break

# 确定状态
if qc_errors:
    status = "FAIL"
elif qc_warnings:
    status = "WARNING"
else:
    status = "PASS"
# 写出 qc-report.md
qc_lines = []
status_icon = {"PASS": "🟢", "WARNING": "🟡", "FAIL": "🔴"}
qc_lines.append(f"# QC Report")
qc_lines.append("")
qc_lines.append(f"{status_icon.get(status, '')} Status: **{status}**")
qc_lines.append("")
qc_lines.append("## Summary")
qc_lines.append(f"- Scenes: {len(all_scenes)}")
qc_lines.append(f"- Groups: {len(groups)}")
qc_lines.append(f"- Elements: {len(elements)}")
qc_lines.append(f"- Warnings: {len(qc_warnings)}")
qc_lines.append(f"- Errors: {len(qc_errors)}")
if qc_errors:
    qc_lines.append("")
    qc_lines.append("## Errors")
    for e in qc_errors:
        qc_lines.append(f"- {e}")
if qc_warnings:
    qc_lines.append("")
    qc_lines.append("## Warnings")
    for w in qc_warnings:
        qc_lines.append(f"- {w}")
if qc_notes:
    qc_lines.append("")
    qc_lines.append("## Notes")
    for n in qc_notes:
        qc_lines.append(f"- {n}")
qc_path = os.path.join(OUTPUT_DIR, "qc-report.md")
with open(qc_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(qc_lines))
print(f"{os.path.abspath(qc_path)}\n")

# Asset Index
asset_lines = []
asset_lines.append("# Asset Index")
asset_lines.append("")
asset_lines.append("## Characters / Objects")
asset_lines.append("")
for el in elements:
    if el.get("is_background"):
        continue
    en = el.get("name", "")
    ename = el.get("english_name", "")
    # 找对应的 ref 文件
    ref_file = ""
    for rfn in sorted(os.listdir(OUTPUT_DIR)):
        target = f"ref_{safe_name(en)}.txt"
        if rfn == target:
            ref_file = rfn
            break
    # 找出现在哪些 scene：优先用 element_refs，fallback 到英文名匹配
    appear_scenes = set()
    appear_groups = []
    for gi, g in enumerate(groups):
        if en in g.get("element_refs", []):
            appear_groups.append(g.get("label", ""))
            for s in g.get("scenes", []):
                appear_scenes.add(s.get("scene_num", 0))
    # 如果 element_refs 没覆盖到，用英文名在描述中匹配作为补充
    if not appear_scenes:
        for s in all_scenes:
            sn = s.get("scene_num", 0)
            desc = s.get("description", "")
            if ename and ename.lower() in desc.lower():
                appear_scenes.add(sn)
    appear_scenes = sorted(appear_scenes)
    asset_lines.append(f"### {en}")
    asset_lines.append(f"- English name: {ename or '(none)'}")
    if not is_reference(el):
        asset_lines.append("- Reference file: (无需参考图，描述已嵌入 prompt)")
    else:
        asset_lines.append(f"- Reference file: {ref_file or '(none)'}")
    asset_lines.append(f"- Appears in scenes: {', '.join(map(str, appear_scenes)) if appear_scenes else '(none)'}")
    asset_lines.append(f"- Appears in groups: {', '.join(appear_groups) if appear_groups else '(none)'}")
    asset_lines.append("")
asset_lines.append("## Environments")
asset_lines.append("")
for el in elements:
    if not el.get("is_background"):
        continue
    en = el.get("name", "")
    ename = el.get("english_name", "")
    # 背景元素优先使用 element_refs 确定出现场景
    appear_scenes = set()
    appear_groups = []
    for gi, g in enumerate(groups):
        if en in g.get("element_refs", []):
            appear_groups.append(g.get("label", ""))
            for s in g.get("scenes", []):
                appear_scenes.add(s.get("scene_num", 0))
    # fallback：用英文名在描述中匹配
    if not appear_scenes:
        for s in all_scenes:
            sn = s.get("scene_num", 0)
            desc = s.get("description", "")
            if ename and ename.lower() in desc.lower():
                appear_scenes.add(sn)
    appear_scenes = sorted(appear_scenes)
    # 查找背景 ref 文件名
    bg_ref_name = ""
    target = f"ref_bg_{safe_name(en)}.txt"
    for bfn in sorted(os.listdir(OUTPUT_DIR)):
        if bfn == target:
            bg_ref_name = bfn
            break
    if not bg_ref_name:
        for bfn in sorted(os.listdir(OUTPUT_DIR)):
            if bfn.startswith("ref_bg_"):
                bg_ref_name = bfn
                break
    asset_lines.append(f"### {en}")
    asset_lines.append(f"- English name: {ename or '(none)'}")
    if not is_reference(el):
        asset_lines.append("- Reference file: (无需参考图，描述已嵌入 prompt)")
    else:
        asset_lines.append(f"- Reference file: {bg_ref_name or '(none)'}")
    asset_lines.append(f"- Appears in scenes: {', '.join(map(str, appear_scenes)) if appear_scenes else '(none)'}")
    asset_lines.append(f"- Appears in groups: {', '.join(appear_groups) if appear_groups else '(none)'}")
    asset_lines.append("")
asset_path = os.path.join(OUTPUT_DIR, "asset-index.md")
with open(asset_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(asset_lines))
print(f"{os.path.abspath(asset_path)}\n")

print(f"完成！共 {storyboard_count} 个故事版/总览 + {image_shot_count} 个图片单帧 + {video_shot_count} 个单镜视频 + {group_video_count} 个分组视频 + {ref_count} 个参考图 + 1 份QC报告 + 1 份资产索引")
print(f"\n{os.path.abspath(OUTPUT_DIR)}")

def md_to_html(text):
    """简单 Markdown → 带样式 HTML"""
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    lines = safe.split('\n')
    html_parts = []
    in_list = False
    for line in lines:
        # 标题
        if line.startswith('### '):
            if in_list: html_parts.append('</ul>'); in_list = False
            html_parts.append(f'<h3 style="font-family:Outfit;font-size:16px;font-weight:600;margin:20px 0 8px;">{line[4:]}</h3>')
        elif line.startswith('## '):
            if in_list: html_parts.append('</ul>'); in_list = False
            html_parts.append(f'<h2 style="font-family:Outfit;font-size:18px;font-weight:600;margin:20px 0 8px;">{line[3:]}</h2>')
        elif line.startswith('# '):
            if in_list: html_parts.append('</ul>'); in_list = False
            html_parts.append(f'<h1 style="font-family:Outfit;font-size:22px;font-weight:600;margin:20px 0 8px;">{line[2:]}</h1>')
        # 无序列表
        elif line.startswith('- '):
            if not in_list:
                html_parts.append('<ul style="margin:8px 0;padding-left:20px;line-height:1.8;">')
                in_list = True
            html_parts.append(f'<li style="list-style:disc;">{line[2:]}</li>')
        elif line.startswith('  - '):
            if not in_list:
                html_parts.append('<ul style="margin:8px 0;padding-left:20px;line-height:1.8;">')
                in_list = True
            html_parts.append(f'<li style="list-style:circle;margin-left:16px;">{line[4:]}</li>')
        # 空行
        elif not line.strip():
            if in_list: html_parts.append('</ul>'); in_list = False
            html_parts.append('')
        # 正文
        else:
            if in_list: html_parts.append('</ul>'); in_list = False
            html_parts.append(f'<div style="line-height:1.8;margin:4px 0;">{line}</div>')
    if in_list:
        html_parts.append('</ul>')
    result = '\n'.join(html_parts)
    # 加粗转换 **text** → <strong>text</strong>
    result = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', result)
    return result

# HTML 生成
if args.html:
    files = sorted(os.listdir(OUTPUT_DIR))
    tabs = {"group": "", "all": "", "shot": "", "video": "", "groupvideo": "", "ref": "", "qc": "", "asset": "", "img": ""}
    counts = {"group": 0, "all": 0, "shot": 0, "video": 0, "groupvideo": 0, "ref": 0, "qc": 0, "asset": 0, "img": 0}

    # 构建 asset-index 内容的 HTML
    asset_index_content = ""
    for fn in files:
        if fn == "asset-index.md":
            with open(os.path.join(OUTPUT_DIR, fn)) as f:
                asset_index_content = f.read()

    for fn in files:
        if fn.endswith(".txt"):
            with open(os.path.join(OUTPUT_DIR, fn)) as f:
                content = f.read()
            safe = content.replace("<", "&lt;").replace(">", "&gt;")
            # 根据文件类型确定复制按钮文案
            copy_label = "[ COPY ]"
            if fn.startswith("video_group_"):
                copy_label = "[ COPY GROUP VIDEO ]"
            elif fn.startswith("video_"):
                copy_label = "[ COPY VIDEO PROMPT ]"
            elif fn.startswith("ref_"):
                copy_label = "[ COPY REF PROMPT ]"
            elif fn.startswith("image_"):
                copy_label = "[ COPY IMAGE PROMPT ]"
            card = f'''
            <div class="ns-card">
                <div class="ns-card-header">
                    <span class="ns-card-title">{fn}</span>
                    <button class="ns-copy-btn" onclick="copyPrompt(this)">{copy_label}</button>
                </div>
                <div class="ns-card-body">
                    <pre>{safe}</pre>
                </div>
            </div>
            '''
            if "全片总览" in fn:
                tabs["all"] += card; counts["all"] += 1
            elif fn.startswith("video_group_"):
                tabs["groupvideo"] += card; counts["groupvideo"] += 1
            elif fn.startswith("video_"):
                tabs["video"] += card; counts["video"] += 1
            elif fn.startswith("image_"):
                tabs["shot"] += card; counts["shot"] += 1
            elif fn.startswith("ref_"):
                tabs["ref"] += card; counts["ref"] += 1
            else:
                tabs["group"] += card; counts["group"] += 1
        elif fn.lower().endswith((".png", ".jpg", ".jpeg")):
            card = f'''
            <div class="ns-card">
                <div class="ns-card-header">
                    <span class="ns-card-title">{fn}</span>
                </div>
                <div class="ns-card-body" style="padding:8px;text-align:center;">
                    <img src="{fn}" style="max-width:100%;border-radius:4px;" />
                </div>
            </div>
            '''
            tabs["img"] += card; counts["img"] += 1
        elif fn == "qc-report.md":
            with open(os.path.join(OUTPUT_DIR, fn)) as f:
                content = f.read()
            safe = content.replace("<", "&lt;").replace(">", "&gt;")
            # Markdown 渲染为格式化 HTML
            md_html = safe
            for line in md_html.split('\n'):
                if line.startswith('# '):
                    md_html = md_html.replace(line, f'<h1 style="font-family:Outfit;font-size:24px;margin:16px 0 8px;">{line[2:]}</h1>')
                elif line.startswith('## '):
                    md_html = md_html.replace(line, f'<h2 style="font-family:Outfit;font-size:18px;margin:16px 0 8px;">{line[3:]}</h2>')
            tabs["qc"] += f'''
            <div class="ns-card">
                <div class="ns-card-header">
                    <span class="ns-card-title">{status_icon.get(status, '')} QC Report — Status: {status}</span>
                </div>
                <div class="ns-card-body" style="font-family:'Space Grotesk';font-size:14px;line-height:1.8;">
                    <pre style="white-space:pre-wrap;">{safe}</pre>
                </div>
            </div>
            '''
            counts["qc"] += 1
        elif fn == "asset-index.md" and asset_index_content:
            safe = asset_index_content.replace("<", "&lt;").replace(">", "&gt;")
            tabs["asset"] += f'''
            <div class="ns-card">
                <div class="ns-card-header">
                    <span class="ns-card-title">Asset Index</span>
                </div>
                <div class="ns-card-body">
                    <pre style="white-space:pre-wrap;">{safe}</pre>
                </div>
            </div>
            '''
            counts["asset"] += 1

    img_tab_btn = '<button class="ns-tab" onclick="switchTab(\'img\')">已生成图片 <span class="ns-count">' + str(counts["img"]) + '</span></button>' if counts["img"] else ''
    img_tab_panel = '<div id="panel-img" class="ns-panel">' + tabs["img"] + '</div>' if counts["img"] else ''
    video_tab_btn = '<button class="ns-tab" onclick="switchTab(\'video\')">单镜视频 <span class="ns-count">' + str(counts["video"]) + '</span></button>' if counts["video"] else ''
    video_tab_panel = '<div id="panel-video" class="ns-panel">' + tabs["video"] + '</div>' if counts["video"] else ''
    groupvideo_tab_btn = '<button class="ns-tab" onclick="switchTab(\'groupvideo\')">故事板视频 <span class="ns-count">' + str(counts["groupvideo"]) + '</span></button>' if counts["groupvideo"] else ''
    groupvideo_tab_panel = '<div id="panel-groupvideo" class="ns-panel">' + tabs["groupvideo"] + '</div>' if counts["groupvideo"] else ''
    qc_tab_btn = '<button class="ns-tab" onclick="switchTab(\'qc\')">质检报告 <span class="ns-count">' + str(counts["qc"]) + '</span></button>' if counts["qc"] else ''
    qc_tab_panel = '<div id="panel-qc" class="ns-panel">' + tabs["qc"] + '</div>' if counts["qc"] else ''
    asset_tab_btn = '<button class="ns-tab" onclick="switchTab(\'asset\')">资产索引 <span class="ns-count">' + str(counts["asset"]) + '</span></button>' if counts["asset"] else ''
    asset_tab_panel = '<div id="panel-asset" class="ns-panel">' + tabs["asset"] + '</div>' if counts["asset"] else ''
    html_title = f"{project_name} — {style_tag}"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{html_title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600&family=Space+Grotesk:wght@400;600&display=swap" rel="stylesheet">
<style>
    :root {{
        --c-accent: oklch(0.50 0.15 200);
        --c-bg: #F3F4F6;
        --c-surface: #FFFFFF;
        --c-text-main: #111827;
        --c-text-mut: #6B7280;
        --c-border: #E5E7EB;
        --sp-8: 8px; --sp-16: 16px; --sp-24: 24px; --sp-32: 32px; --sp-64: 64px;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        background: var(--c-bg);
        font-family: 'Space Grotesk', sans-serif;
        color: var(--c-text-main);
        padding: var(--sp-16);
        display: flex;
        justify-content: center;
        min-height: 100vh;
    }}
    .ns-device-frame {{
        width: 100%;
        max-width: 90vw;
        background: var(--c-surface);
        border-radius: 12px;
        box-shadow: 0 32px 64px rgba(0,0,0,0.06);
        border: 1px solid var(--c-border);
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }}
    .ns-frame-header {{
        height: 48px;
        background: #FAFAFA;
        border-bottom: 1px solid var(--c-border);
        display: flex;
        align-items: center;
        padding: 0 var(--sp-24);
        gap: var(--sp-8);
    }}
    .ns-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
    .ns-dot.red {{ background: #FF5F56; }}
    .ns-dot.yellow {{ background: #FFBD2E; }}
    .ns-dot.green {{ background: #27C93F; }}
    .ns-layout {{
        display: grid;
        grid-template-columns: 220px 1fr;
        flex: 1;
        height: 100%;
        background: var(--c-surface);
    }}
    .ns-sidebar {{
        padding: var(--sp-24);
        border-right: 1px solid var(--c-border);
        background: #FAFAFA;
    }}
    .ns-sidebar-title {{
        font-family: 'Outfit', sans-serif;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 4px;
        letter-spacing: -0.3px;
    }}
    .ns-sidebar-style {{
        font-family: 'Outfit', sans-serif;
        font-size: 14px;
        font-weight: 400;
        color: var(--c-text-mut);
        margin-bottom: 24px;
    }}
    .ns-tabs {{
        display: flex;
        flex-direction: column;
        gap: var(--sp-8);
    }}
    .ns-tab {{
        text-align: left;
        padding: var(--sp-16);
        font-family: 'Outfit', sans-serif;
        font-size: 15px;
        background: transparent;
        border: 1px solid transparent;
        color: var(--c-text-mut);
        cursor: pointer;
        border-radius: 6px;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .ns-tab:hover {{
        background: #F3F4F6;
        color: var(--c-text-main);
    }}
    .ns-tab.active {{
        background: var(--c-surface);
        color: var(--c-accent);
        border: 1px solid var(--c-border);
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }}
    .ns-count {{ float: right; font-family: 'Space Grotesk'; font-size: 13px; color: #9CA3AF; }}
    .ns-tab.active .ns-count {{ color: var(--c-accent); }}
    .ns-content {{
        padding: var(--sp-24) var(--sp-16);
        overflow-y: auto;
        max-height: calc(100vh - 48px - 48px);
        background: var(--c-surface);
    }}
    .ns-panel {{ display: none; }}
    .ns-panel.active {{ display: block; }}
    .ns-card {{
        border: 1px solid var(--c-border);
        border-radius: 8px;
        margin-bottom: var(--sp-24);
        background: var(--c-surface);
    }}
    .ns-card-header {{
        padding: var(--sp-16) var(--sp-24);
        border-bottom: 1px solid var(--c-border);
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FAFAFA;
    }}
    .ns-card-title {{
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 14px;
        color: var(--c-text-main);
    }}
    .ns-copy-btn {{
        background: var(--c-text-main);
        color: var(--c-surface);
        border: none;
        padding: var(--sp-8) var(--sp-16);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 12px;
        font-weight: 600;
        border-radius: 4px;
        cursor: pointer;
        transition: background 0.1s;
    }}
    .ns-copy-btn:hover {{ background: var(--c-accent); }}
    .ns-copy-btn.copied {{ background: #27C93F; pointer-events: none; }}
    .ns-card-body {{ padding: var(--sp-24); }}
    pre {{
        font-family: 'Space Grotesk', monospace;
        font-size: 13px;
        line-height: 1.6;
        color: #374151;
        white-space: pre-wrap;
        word-break: break-word;
    }}
</style>
</head>
<body>

<div class="ns-device-frame">
    <div class="ns-frame-header">
        <div class="ns-dot red"></div>
        <div class="ns-dot yellow"></div>
        <div class="ns-dot green"></div>
    </div>
    <div class="ns-layout">
        <div class="ns-sidebar">
            <div class="ns-sidebar-title">{project_name}</div>
            <div class="ns-sidebar-style">{style_tag}</div>
            <div class="ns-tabs">
                <button class="ns-tab active" onclick="switchTab('all')">
                    全片总览 <span class="ns-count">{counts["all"]}</span>
                </button>
                <button class="ns-tab" onclick="switchTab('group')">
                    故事板图片 <span class="ns-count">{counts["group"]}</span>
                </button>
                {groupvideo_tab_btn}
                <button class="ns-tab" onclick="switchTab('shot')">
                    图片单帧 <span class="ns-count">{counts["shot"]}</span>
                </button>
                {video_tab_btn}
                <button class="ns-tab" onclick="switchTab('ref')">
                    角色和场景 <span class="ns-count">{counts["ref"]}</span>
                </button>
                {asset_tab_btn}
                {qc_tab_btn}
                {img_tab_btn}
            </div>
        </div>
        <div class="ns-content">
            <div id="panel-all" class="ns-panel active">{tabs["all"]}</div>
            <div id="panel-group" class="ns-panel">{tabs["group"]}</div>
            {groupvideo_tab_panel}
            <div id="panel-shot" class="ns-panel">{tabs["shot"]}</div>
            {video_tab_panel}
            <div id="panel-ref" class="ns-panel">{tabs["ref"]}</div>
            {asset_tab_panel}
            {qc_tab_panel}
            {img_tab_panel}
        </div>
    </div>
</div>

<script>
    Object.assign(window, {{
        copyPrompt: function(btn) {{
            const originalText = btn.dataset.originalText || btn.textContent;
            btn.dataset.originalText = originalText;
            const textContent = btn.parentElement.nextElementSibling.textContent;
            const finalPrompt = textContent.split('-----------------------------')[0].trim();
            // 优先使用 Clipboard API（需要 HTTPS/localhost）
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(finalPrompt).then(() => {{
                    btn.textContent = '[ COPIED ]';
                    btn.classList.add('copied');
                    setTimeout(() => {{
                        btn.textContent = originalText;
                        btn.classList.remove('copied');
                    }}, 2000);
                }}).catch(function() {{
                    // Clipboard API 失败时 fallback 到 execCommand
                    fallbackCopy(btn, finalPrompt, originalText);
                }});
            }} else {{
                fallbackCopy(btn, finalPrompt, originalText);
            }}
        }},
        fallbackCopy: function(btn, text, originalText) {{
            const ta = document.createElement('textarea');
            ta.value = text;
            ta.style.position = 'fixed';
            ta.style.opacity = '0';
            document.body.appendChild(ta);
            ta.select();
            try {{
                document.execCommand('copy');
                btn.textContent = '[ COPIED ]';
                btn.classList.add('copied');
                setTimeout(() => {{
                    btn.textContent = originalText;
                    btn.classList.remove('copied');
                }}, 2000);
            }} catch (e) {{
                btn.textContent = '[ COPY FAILED ]';
                setTimeout(() => {{ btn.textContent = originalText; }}, 2000);
            }}
            document.body.removeChild(ta);
        }},
        switchTab: function(targetId) {{
            document.querySelectorAll('.ns-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.ns-panel').forEach(p => p.classList.remove('active'));
            document.querySelector(`.ns-tab[onclick$="'${{targetId}}')"]`).classList.add('active');
            document.getElementById('panel-' + targetId).classList.add('active');
        }}
    }});
</script>
</body>
</html>"""

    html_name = f"{project_name}.html" if base == "project" else f"{project_name}_{style_tag}.html"
    hp = os.path.join(OUTPUT_DIR, html_name)
    with open(hp, 'w', encoding='utf-8') as f:
        f.write(html)
    # 跨平台打开 HTML
    sys_name = platform.system()
    if sys_name == "Windows":
        os.system(f'start "" "{hp}"')
    elif sys_name == "Darwin":
        os.system(f'open "{hp}"')
    else:
        webbrowser.open(f"file://{hp}")
    print(f"🌐 HTML: {os.path.abspath(hp)}")
