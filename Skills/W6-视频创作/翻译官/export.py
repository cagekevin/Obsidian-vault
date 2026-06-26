"""
导出脚本：project.json → output/ 提示词文件
默认全量生成：分组分镜板 + 全片总览 + 图片单帧 + 参考图
用法：
    python3 export.py [项目目录]
    python3 export.py [项目目录] --html
    python3 export.py [项目目录] --input project_pixar.json
    python3 export.py [项目目录] --input project_pixar.json --html

Pipeline 节点名: export_main
"""

import json, os, sys, argparse, re, webbrowser, platform

from utils import (
    load_json, read_txt, fatal, safe_name, reference_file_name,
    is_reference, output_dir, style_tag_from_input,
    get_all_scenes, get_elements, log, setup_logger,
)
from pipeline import Pipeline, register

log = setup_logger("export")


# ══════════════════════════════════════
# 注册到 Pipeline
# ══════════════════════════════════════

pipe = Pipeline()


@register(pipe)
def export_main(ctx):
    """入口：读取 project.json → 导出所有提示词文件"""
    project_dir = ctx["project_dir"]
    input_name = ctx.get("input_name", "project.json")
    html_flag = ctx.get("html", False)

    INPUT = os.path.join(project_dir, input_name)
    if not os.path.isfile(INPUT):
        fatal(f"找不到输入文件 {INPUT}")

    data = load_json(INPUT)

    out_dir = output_dir(project_dir, input_name)
    os.makedirs(out_dir, exist_ok=True)
    _clean_output_dir(out_dir)

    style_tag = style_tag_from_input(input_name)
    vs = data.get("visual_style", "")
    frame_aspect = data.get("frame_aspect_ratio", "")
    elements = get_elements(data)
    all_scenes, groups = get_all_scenes(data)

    ctx["out_dir"] = out_dir
    ctx["style_tag"] = style_tag
    ctx["vs"] = vs
    ctx["frame_aspect"] = frame_aspect
    ctx["elements"] = elements
    ctx["all_scenes"] = all_scenes
    ctx["groups"] = groups

    # 执行各子步骤（内联调用，不经过 pipeline 依赖图，因为它们在同一个入口下）
    n_storyboard = export_storyboards(ctx)
    n_shots = export_image_shots(ctx)
    n_videos = export_video_shots(ctx)
    n_group_videos = export_group_videos(ctx)
    n_refs = export_refs(ctx)

    # QC + Asset Index
    qc_warnings, qc_errors, qc_notes = run_qc(ctx)
    _write_qc_report(out_dir, all_scenes, groups, elements, qc_warnings, qc_errors, qc_notes)
    _write_asset_index(out_dir, all_scenes, groups, elements)

    # 统计
    total = n_storyboard + n_shots + n_videos + n_group_videos + n_refs
    log.info(f"完成！共 {n_storyboard} 个故事板/总览 + {n_shots} 个图片单帧 + "
             f"{n_videos} 个单镜视频 + {n_group_videos} 个分组视频 + {n_refs} 个参考图 + QC + 资产索引")
    log.info(f"输出目录: {os.path.abspath(out_dir)}")

    # HTML
    if html_flag:
        _generate_html(project_dir, out_dir, style_tag, data, all_scenes, groups, elements,
                        qc_warnings, qc_errors, qc_notes)

    return ctx


# ══════════════════════════════════════
# 清理
# ══════════════════════════════════════

def _clean_output_dir(out_dir):
    ALLOWED_EXTENSIONS = {".txt", ".md", ".html"}
    for f in os.listdir(out_dir):
        fp = os.path.join(out_dir, f)
        ext = os.path.splitext(f)[1].lower()
        if os.path.isfile(fp) and ext in ALLOWED_EXTENSIONS:
            os.remove(fp)


# ══════════════════════════════════════
# 故事板
# ══════════════════════════════════════

file_seq = 0

def export_storyboards(ctx):
    global file_seq
    out_dir = ctx["out_dir"]
    vs = ctx["vs"]
    frame_aspect = ctx["frame_aspect"]
    groups = ctx["groups"]
    elements = ctx["elements"]
    all_scenes = ctx["all_scenes"]
    count = 0

    def write_board(scenes, label, is_overview=False):
        global file_seq
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
            cam_parts = [g.get("label", "") for g in groups]
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
        # 确定本组出镜元素列表
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
        shown = [e for e in all_shown if not e.get("is_background") and is_reference(e)]
        bg_shown = [e for e in all_shown if e.get("is_background") and is_reference(e)]
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
        lines.append("CONSISTENCY RULE: ALL visual elements in the storyboard frames below MUST match the corresponding reference images EXACTLY.")
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
        fname = f"{count+1:02d}_storyboard_{label.replace(' ', '-')}.txt"
        out = os.path.join(out_dir, fname)
        with open(out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        log.info(f"  {os.path.abspath(out)}")

    # 分组分镜板
    for gi, g in enumerate(groups):
        write_board(g.get("scenes", []), g.get("label", f"group-{gi+1}"))
        count += 1
    # 全片总览
    write_board(all_scenes, "全片总览", is_overview=True)
    count += 1

    ctx["storyboard_count"] = count
    return count


# ══════════════════════════════════════
# 图片单帧
# ══════════════════════════════════════

def export_image_shots(ctx):
    out_dir = ctx["out_dir"]
    vs = ctx["vs"]
    all_scenes = ctx["all_scenes"]
    count = 0

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
        out = os.path.join(out_dir, fname)
        with open(out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        log.info(f"  {os.path.abspath(out)}")
        count += 1

    return count


# ══════════════════════════════════════
# 单镜视频
# ══════════════════════════════════════

def export_video_shots(ctx):
    out_dir = ctx["out_dir"]
    elements = ctx["elements"]
    all_scenes = ctx["all_scenes"]
    groups = ctx["groups"]
    count = 0

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
        out = os.path.join(out_dir, fname)
        with open(out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        log.info(f"  {os.path.abspath(out)}")
        count += 1

    return count


# ══════════════════════════════════════
# 分组视频
# ══════════════════════════════════════

def export_group_videos(ctx):
    out_dir = ctx["out_dir"]
    groups = ctx["groups"]
    elements = ctx["elements"]
    count = 0

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
        out = os.path.join(out_dir, fname)
        with open(out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        log.info(f"  {os.path.abspath(out)}")
        count += 1

    return count


# ══════════════════════════════════════
# 参考图
# ══════════════════════════════════════

def export_refs(ctx):
    out_dir = ctx["out_dir"]
    vs = ctx["vs"]
    elements = ctx["elements"]
    count = 0

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
        role_type = "场景" if is_bg else "角色"
        ref_note = f"\n\n----------------------------------------------------------------------------------------------------\n\n我上传的第__张图是故事里的{name}{role_type}，{appearance} Please generate the video strictly following my reference image."
        full_content = prompt.strip() + ref_note
        out = os.path.join(out_dir, fname)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(full_content)
        log.info(f"  {os.path.abspath(out)}")
        count += 1

    return count


# ══════════════════════════════════════
# QC
# ══════════════════════════════════════

def run_qc(ctx):
    """运行所有 QC 检查，返回 (warnings, errors, notes)"""
    vs = ctx["vs"]
    elements = ctx["elements"]
    groups = ctx["groups"]
    all_scenes = ctx["all_scenes"]
    project_dir = ctx.get("project_dir", ".")

    qc_warnings = []
    qc_notes = []
    qc_errors = []

    # 1. visual_style
    if not vs or vs == "[]":
        qc_warnings.append("visual_style is empty.")

    # 2. elements 完整性
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
            allowed_prefixes = ("char_", "scene_", "product_", "prop_", "fx_", "other_")
            if not ename.lower().startswith(allowed_prefixes):
                qc_errors.append(
                    f"Element '{en}' english_name ('{ename}') 不符合资产命名规范。"
                    f" 必须以下列前缀开头：{', '.join(allowed_prefixes)}"
                )
        if not app:
            qc_notes.append(f"Element '{en}' appearance is empty (non-reference element, no reference image needed).")
        if ib is None:
            qc_warnings.append(f"Element '{en}' is_background is not set.")

    # 3. element_refs
    for gi, g in enumerate(groups):
        refs = g.get("element_refs", [])
        for r in refs:
            if r not in element_names:
                qc_errors.append(f"Group {gi+1} references missing element: '{r}'")
        if not refs:
            qc_warnings.append(f"Group {gi+1} ({g.get('label', '')}) has no element_refs.")

    # 4. scene 编号连续性
    all_nums = [s.get("scene_num", 0) for s in all_scenes]
    for i in range(1, len(all_nums)):
        if all_nums[i] != all_nums[i-1] + 1:
            qc_warnings.append(f"Scene numbering jump: {all_nums[i-1]} → {all_nums[i]}")
            break

    # 5. scene 字段缺失
    for s in all_scenes:
        sn = s.get("scene_num", "?")
        if not s.get("description", "").strip():
            qc_errors.append(f"Scene {sn} description is empty.")
        if not s.get("camera", "").strip():
            qc_warnings.append(f"Scene {sn} camera is empty.")
        desc = s.get("description", "")
        if re.search(r'scene\s+\d+', desc, re.IGNORECASE) and not s.get("storyboard_desc", "").strip():
            qc_errors.append(
                f"Scene {sn} description references 'scene {sn}' but has no 'storyboard_desc' field."
            )

    # 6. 中文残留
    for s in all_scenes:
        sn = s.get("scene_num", "?")
        desc = s.get("description", "")
        if re.search(r'[\u4e00-\u9fff]', desc):
            qc_warnings.append(f"Scene {sn} description contains Chinese characters.")

    # 7. 品牌名检查
    brand_words = ["Inside Out", "Kurzgesagt", "Apple Keynote", "Nintendo", "Disney",
                   "Marvel", "Star Wars", "Pokemon"]
    for s in all_scenes:
        sn = s.get("scene_num", "?")
        desc = s.get("description", "")
        for bw in brand_words:
            if bw.lower() in desc.lower():
                qc_errors.append(f"Scene {sn} contains brand name: '{bw}'")

    # 8. 背景元素未被引用
    for el in elements:
        if el.get("is_background"):
            en = el.get("name", "")
            used = any(en in g.get("element_refs", []) for g in groups)
            if not used:
                qc_warnings.append(f"Background element '{en}' is not referenced by any group.")

    # 9. 描述长度波动
    desc_word_counts = [(s.get("scene_num", "?"), len(s.get("description", "").split())) for s in all_scenes]
    if len(desc_word_counts) >= 3:
        valid_counts = [c for _, c in desc_word_counts if c > 0]
        if valid_counts:
            avg_len = sum(valid_counts) / len(valid_counts)
            for sn, wc in desc_word_counts:
                if wc > 0 and wc < avg_len * 0.3:
                    qc_warnings.append(f"Scene {sn} description is notably short ({wc} words vs {avg_len:.0f} average).")
                    break

    # 10. element_refs 交叉校验
    for gi, g in enumerate(groups):
        refs = g.get("element_refs", [])
        gname = g.get("label", f"group-{gi+1}")
        for r in refs:
            el = next((e for e in elements if e.get("name") == r), None)
            if not el:
                continue
            ename = el.get("english_name") or el.get("name", "")
            ename_words = [w.lower().strip(".,;:!?()") for w in ename.split() if len(w) >= 5]
            mentioned = False
            for s in g.get("scenes", []):
                desc = s.get("description", "").lower()
                if any(w in desc for w in ename_words):
                    mentioned = True
                    break
            if not mentioned and is_reference(el):
                found_elsewhere = any(
                    any(w in s.get("description", "").lower() for w in ename_words)
                    for og in groups if og != g
                    for s in og.get("scenes", [])
                )
                msg = f"Group '{gname}' element_refs 含参考元素 '{r}'（{ename}），但该组所有场景的 description 均未明确提及"
                if found_elsewhere:
                    qc_notes.append(f"{msg}（该元素在其他组中有匹配）")
                else:
                    qc_warnings.append(f"{msg}——如该元素确实不出现在本组画面中，请从 element_refs 移除")

    # 11. 过锐词检查
    sharp_words = ["HDR", "8K", "超高清", "高细节", "锐利", "ultra sharp", "hyper-detailed",
                   "intricate", "繁复", "浓郁", "8k", "Ultra HD", "超高细节"]
    for el in elements:
        en = el.get("name", "")
        app = el.get("appearance", "")
        if any(sw.lower() in app.lower() for sw in sharp_words):
            qc_warnings.append(f"Element '{en}' appearance 含过锐词——替换为柔和描述（清晰/柔和/克制/干净通透）")
            break
    for s in all_scenes:
        sn = s.get("scene_num", "?")
        desc = s.get("description", "")
        if any(sw.lower() in desc.lower() for sw in sharp_words):
            qc_warnings.append(f"Scene {sn} description 含过锐词")
            break

    ctx["qc_warnings"] = qc_warnings
    ctx["qc_errors"] = qc_errors
    ctx["qc_notes"] = qc_notes
    return qc_warnings, qc_errors, qc_notes


# ══════════════════════════════════════
# 写 QC 报告
# ══════════════════════════════════════

def _write_qc_report(out_dir, all_scenes, groups, elements, qc_warnings, qc_errors, qc_notes):
    if qc_errors:
        status = "FAIL"
    elif qc_warnings:
        status = "WARNING"
    else:
        status = "PASS"
    status_icon = {"PASS": "🟢", "WARNING": "🟡", "FAIL": "🔴"}
    lines = []
    lines.append(f"# QC Report\n")
    lines.append(f"{status_icon.get(status, '')} Status: **{status}**\n")
    lines.append("## Summary")
    lines.append(f"- Scenes: {len(all_scenes)}")
    lines.append(f"- Groups: {len(groups)}")
    lines.append(f"- Elements: {len(elements)}")
    lines.append(f"- Warnings: {len(qc_warnings)}")
    lines.append(f"- Errors: {len(qc_errors)}")
    if qc_errors:
        lines.append("\n## Errors")
        for e in qc_errors:
            lines.append(f"- {e}")
    if qc_warnings:
        lines.append("\n## Warnings")
        for w in qc_warnings:
            lines.append(f"- {w}")
    if qc_notes:
        lines.append("\n## Notes")
        for n in qc_notes:
            lines.append(f"- {n}")
    qc_path = os.path.join(out_dir, "qc-report.md")
    with open(qc_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    log.info(f"  {os.path.abspath(qc_path)}")


# ══════════════════════════════════════
# 资产索引
# ══════════════════════════════════════

def _write_asset_index(out_dir, all_scenes, groups, elements):
    lines = []
    lines.append("# Asset Index\n")
    lines.append("## Characters / Objects\n")
    for el in elements:
        if el.get("is_background"):
            continue
        en = el.get("name", "")
        ename = el.get("english_name", "")
        ref_file = ""
        for rfn in sorted(os.listdir(out_dir)):
            if rfn == f"ref_{safe_name(en)}.txt":
                ref_file = rfn
                break
        appear_scenes = set()
        appear_groups = []
        for gi, g in enumerate(groups):
            if en in g.get("element_refs", []):
                appear_groups.append(g.get("label", ""))
                for s in g.get("scenes", []):
                    appear_scenes.add(s.get("scene_num", 0))
        if not appear_scenes:
            for s in all_scenes:
                sn = s.get("scene_num", 0)
                desc = s.get("description", "")
                if ename and ename.lower() in desc.lower():
                    appear_scenes.add(sn)
        appear_scenes = sorted(appear_scenes)
        lines.append(f"### {en}")
        lines.append(f"- English name: {ename or '(none)'}")
        if not is_reference(el):
            lines.append("- Reference file: (无需参考图，描述已嵌入 prompt)")
        else:
            lines.append(f"- Reference file: {ref_file or '(none)'}")
        lines.append(f"- Appears in scenes: {', '.join(map(str, appear_scenes)) if appear_scenes else '(none)'}")
        lines.append(f"- Appears in groups: {', '.join(appear_groups) if appear_groups else '(none)'}")
        lines.append("")

    lines.append("## Environments\n")
    for el in elements:
        if not el.get("is_background"):
            continue
        en = el.get("name", "")
        ename = el.get("english_name", "")
        appear_scenes = set()
        appear_groups = []
        for gi, g in enumerate(groups):
            if en in g.get("element_refs", []):
                appear_groups.append(g.get("label", ""))
                for s in g.get("scenes", []):
                    appear_scenes.add(s.get("scene_num", 0))
        if not appear_scenes:
            for s in all_scenes:
                sn = s.get("scene_num", 0)
                desc = s.get("description", "")
                if ename and ename.lower() in desc.lower():
                    appear_scenes.add(sn)
        appear_scenes = sorted(appear_scenes)
        bg_ref_name = ""
        target = f"ref_bg_{safe_name(en)}.txt"
        for bfn in sorted(os.listdir(out_dir)):
            if bfn == target:
                bg_ref_name = bfn
                break
        if not bg_ref_name:
            for bfn in sorted(os.listdir(out_dir)):
                if bfn.startswith("ref_bg_"):
                    bg_ref_name = bfn
                    break
        lines.append(f"### {en}")
        lines.append(f"- English name: {ename or '(none)'}")
        if not is_reference(el):
            lines.append("- Reference file: (无需参考图，描述已嵌入 prompt)")
        else:
            lines.append(f"- Reference file: {bg_ref_name or '(none)'}")
        lines.append(f"- Appears in scenes: {', '.join(map(str, appear_scenes)) if appear_scenes else '(none)'}")
        lines.append(f"- Appears in groups: {', '.join(appear_groups) if appear_groups else '(none)'}")
        lines.append("")

    asset_path = os.path.join(out_dir, "asset-index.md")
    with open(asset_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    log.info(f"  {os.path.abspath(asset_path)}")


# ══════════════════════════════════════
# HTML 生成（原样保留）
# ══════════════════════════════════════

def md_to_html(text):
    """简单 Markdown → 带样式 HTML"""
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    lines = safe.split('\n')
    html_parts = []
    in_list = False
    for line in lines:
        if line.startswith('### '):
            if in_list: html_parts.append('</ul>'); in_list = False
            html_parts.append(f'<h3 style="font-family:Outfit;font-size:16px;font-weight:600;margin:20px 0 8px;">{line[4:]}</h3>')
        elif line.startswith('## '):
            if in_list: html_parts.append('</ul>'); in_list = False
            html_parts.append(f'<h2 style="font-family:Outfit;font-size:18px;font-weight:600;margin:20px 0 8px;">{line[3:]}</h2>')
        elif line.startswith('# '):
            if in_list: html_parts.append('</ul>'); in_list = False
            html_parts.append(f'<h1 style="font-family:Outfit;font-size:22px;font-weight:600;margin:20px 0 8px;">{line[2:]}</h1>')
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
        elif not line.strip():
            if in_list: html_parts.append('</ul>'); in_list = False
            html_parts.append('')
        else:
            if in_list: html_parts.append('</ul>'); in_list = False
            html_parts.append(f'<div style="line-height:1.8;margin:4px 0;">{line}</div>')
    if in_list:
        html_parts.append('</ul>')
    result = '\n'.join(html_parts)
    result = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', result)
    return result


def _generate_html(project_dir, out_dir, style_tag, data, all_scenes, groups, elements,
                    qc_warnings, qc_errors, qc_notes):
    """生成 HTML 预览页面"""
    vs = data.get("visual_style", "")
    project_name = os.path.basename(os.path.abspath(project_dir))

    files = sorted(os.listdir(out_dir))
    tabs = {"group": "", "all": "", "shot": "", "video": "", "groupvideo": "", "ref": "", "qc": "", "asset": "", "img": ""}
    counts = {"group": 0, "all": 0, "shot": 0, "video": 0, "groupvideo": 0, "ref": 0, "qc": 0, "asset": 0, "img": 0}

    if qc_errors:
        status = "FAIL"
    elif qc_warnings:
        status = "WARNING"
    else:
        status = "PASS"
    status_icon = {"PASS": "🟢", "WARNING": "🟡", "FAIL": "🔴"}

    asset_index_content = ""
    for fn in files:
        if fn == "asset-index.md":
            with open(os.path.join(out_dir, fn)) as f:
                asset_index_content = f.read()

    for fn in files:
        if fn.endswith(".txt"):
            with open(os.path.join(out_dir, fn)) as f:
                content = f.read()
            safe = content.replace("<", "&lt;").replace(">", "&gt;")
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
            with open(os.path.join(out_dir, fn)) as f:
                content = f.read()
            safe = content.replace("<", "&lt;").replace(">", "&gt;")
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

    img_tab_btn = f'<button class="ns-tab" onclick="switchTab(\'img\')">已生成图片 <span class="ns-count">{counts["img"]}</span></button>' if counts["img"] else ''
    img_tab_panel = f'<div id="panel-img" class="ns-panel">{tabs["img"]}</div>' if counts["img"] else ''
    video_tab_btn = f'<button class="ns-tab" onclick="switchTab(\'video\')">单镜视频 <span class="ns-count">{counts["video"]}</span></button>' if counts["video"] else ''
    video_tab_panel = f'<div id="panel-video" class="ns-panel">{tabs["video"]}</div>' if counts["video"] else ''
    groupvideo_tab_btn = f'<button class="ns-tab" onclick="switchTab(\'groupvideo\')">故事板视频 <span class="ns-count">{counts["groupvideo"]}</span></button>' if counts["groupvideo"] else ''
    groupvideo_tab_panel = f'<div id="panel-groupvideo" class="ns-panel">{tabs["groupvideo"]}</div>' if counts["groupvideo"] else ''
    qc_tab_btn = f'<button class="ns-tab" onclick="switchTab(\'qc\')">质检报告 <span class="ns-count">{counts["qc"]}</span></button>' if counts["qc"] else ''
    qc_tab_panel = f'<div id="panel-qc" class="ns-panel">{tabs["qc"]}</div>' if counts["qc"] else ''
    asset_tab_btn = f'<button class="ns-tab" onclick="switchTab(\'asset\')">资产索引 <span class="ns-count">{counts["asset"]}</span></button>' if counts["asset"] else ''
    asset_tab_panel = f'<div id="panel-asset" class="ns-panel">{tabs["asset"]}</div>' if counts["asset"] else ''

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{project_name} — {style_tag}</title>
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
    .ns-tab:hover {{ background: #F3F4F6; color: var(--c-text-main); }}
    .ns-tab.active {{ background: var(--c-surface); color: var(--c-accent); border: 1px solid var(--c-border); font-weight: 600; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }}
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
    .ns-card-title {{ font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 14px; color: var(--c-text-main); }}
    .ns-copy-btn {{ background: var(--c-text-main); color: var(--c-surface); border: none; padding: var(--sp-8) var(--sp-16); font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; border-radius: 4px; cursor: pointer; transition: background 0.1s; }}
    .ns-copy-btn:hover {{ background: var(--c-accent); }}
    .ns-copy-btn.copied {{ background: #27C93F; pointer-events: none; }}
    .ns-card-body {{ padding: var(--sp-24); }}
    pre {{ font-family: 'Space Grotesk', monospace; font-size: 13px; line-height: 1.6; color: #374151; white-space: pre-wrap; word-break: break-word; }}
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
                <button class="ns-tab active" onclick="switchTab('all')">全片总览 <span class="ns-count">{counts["all"]}</span></button>
                <button class="ns-tab" onclick="switchTab('group')">故事板图片 <span class="ns-count">{counts["group"]}</span></button>
                {groupvideo_tab_btn}
                <button class="ns-tab" onclick="switchTab('shot')">图片单帧 <span class="ns-count">{counts["shot"]}</span></button>
                {video_tab_btn}
                <button class="ns-tab" onclick="switchTab('ref')">角色和场景 <span class="ns-count">{counts["ref"]}</span></button>
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
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(finalPrompt).then(() => {{
                    btn.textContent = '[ COPIED ]';
                    btn.classList.add('copied');
                    setTimeout(() => {{ btn.textContent = originalText; btn.classList.remove('copied'); }}, 2000);
                }}).catch(function() {{ fallbackCopy(btn, finalPrompt, originalText); }});
            }} else {{ fallbackCopy(btn, finalPrompt, originalText); }}
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
                setTimeout(() => {{ btn.textContent = originalText; btn.classList.remove('copied'); }}, 2000);
            }} catch (e) {{ btn.textContent = '[ COPY FAILED ]'; setTimeout(() => {{ btn.textContent = originalText; }}, 2000); }}
            document.body.removeChild(ta);
        }},
        switchTab: function(targetId) {{
            document.querySelectorAll('.ns-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.ns-panel').forEach(p => p.classList.remove('active'));
            document.querySelector(`.ns-tab[onclick$="'{targetId}')"]`).classList.add('active');
            document.getElementById('panel-' + targetId).classList.add('active');
        }}
    }});
</script>
</body>
</html>"""

    html_name = f"{project_name}.html"
    hp = os.path.join(out_dir, html_name)
    with open(hp, 'w', encoding='utf-8') as f:
        f.write(html)
    log.info(f"  🌐 {os.path.abspath(hp)}")

    # 跨平台打开
    sys_name = platform.system()
    if sys_name == "Windows":
        os.system(f'start "" "{hp}"')
    elif sys_name == "Darwin":
        os.system(f'open "{hp}"')
    else:
        webbrowser.open(f"file://{hp}")


# ══════════════════════════════════════
# 命令行入口
# ══════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", nargs="?", default=".", help="项目目录")
    parser.add_argument("--html", action="store_true", help="额外生成 HTML")
    parser.add_argument("--input", default="project.json", help="输入的 JSON 文件名，默认 project.json")
    args = parser.parse_args()

    ctx = {
        "project_dir": args.project_dir,
        "input_name": args.input,
        "html": args.html,
    }

    pipe.run("export_main", ctx=ctx)
