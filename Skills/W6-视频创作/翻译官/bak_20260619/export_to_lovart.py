#!/usr/bin/env python3
"""
转换脚本：export.py 的 output/ 提示词 → Lovart 图片生成 JSON。

用法:
    python3 export_to_lovart.py /path/to/项目 --type refs
    python3 export_to_lovart.py /path/to/项目 --type shots
    python3 export_to_lovart.py /path/to/项目 --type storyboard

--type refs:       扫描 output/ 下的 ref_*.txt，输出 output/lovart_refs.json
--type shots:      扫描 output/ 下的 image_*.txt + 读取 manifest 解析垫图，
                   输出 output/lovart_shots.json
--type storyboard: 从 project.json 的 storyboard_groups 读取 element_refs，
                   扫描 output/ 下的 *_storyboard_*.txt，输出 output/lovart_storyboard.json
"""

import json, os, sys, re

LOVART_MODELS = [
    "generate_image_gpt_image_2", "generate_image_gpt_image_2_low",
    "generate_image_gpt_image_2_medium", "generate_image_gpt_image_2_high",
    "generate_image_nano_banana_pro", "generate_image_nano_banana_2",
    "generate_image_seedream_v5", "generate_image_nano_banana",
    "generate_image_midjourney",
]


def fatal(msg):
    print(f"  ❌ {msg}")
    sys.exit(1)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_txt(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def resolve_manifest_ref(asset_key, manifest, project_dir):
    """从 manifest 解析 asset_key 的 latest 路径，找不到返回 None"""
    ext = os.path.splitext(asset_key)[0]
    clean = os.path.splitext(os.path.basename(asset_key))[0]
    for name in [clean, ext]:
        entry = manifest.get(name, {})
        for field in ("latest", "default"):
            rel = entry.get(field, "")
            if rel:
                full = os.path.join(project_dir, rel.replace("\\", "/"))
                if os.path.exists(full):
                    return full
    return None


def scan_asset_refs(ref_key, project_dir, assets_dir_name="assets"):
    """扫描 assets/ 下匹配 ref_key 前缀的所有文件（含 _v1, _v2 等），返回最新版本路径"""
    ad = os.path.join(project_dir, assets_dir_name)
    if not os.path.isdir(ad):
        return None
    # 统一转小写匹配（文件名可能大小写不一致）
    prefix = ref_key.lower()
    candidates = []
    for f in os.listdir(ad):
        if f.lower().startswith(prefix) and f.lower().endswith((".png", ".jpg", ".jpeg")):
            candidates.append(f)
    if not candidates:
        return None
    # 按 _v 版本号排序，取最新的
    def version_key(name):
        m = re.search(r'_v(\d+)', name)
        return int(m.group(1)) if m else 0
    best = max(candidates, key=version_key)
    return os.path.join(project_dir, assets_dir_name, best).replace("\\", "/")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    output_type = sys.argv[2].replace("--type=", "").replace("--type ", "")
    if output_type not in ("refs", "shots", "storyboard"):
        fatal("--type 必须是 refs, shots 或 storyboard")

    # ── 读取配置 ──
    config_path = os.path.join(project_dir, "lovart_config.json")
    if not os.path.exists(config_path):
        fatal(f"找不到 {config_path}，请先运行 init_project.py")
    config = load_json(config_path)

    project_id = config.get("project_id", "")
    if not project_id:
        fatal("lovart_config.json 缺少 project_id")

    skip_existing = config.get("skip_existing", False)
    output_dir = os.path.join(project_dir, "output")

    if not os.path.isdir(output_dir):
        fatal(f"output/ 目录不存在: {output_dir}")

    prompts = []

    if output_type == "refs":
        # ── 扫描 ref_*.txt ──
        ref_cfg = config.get("refs", {})
        ar = ref_cfg.get("aspect_ratio", "4:3")
        res = ref_cfg.get("resolution", "1K")
        model = ref_cfg.get("model", "generate_image_gpt_image_2_medium")
        assets_dir = config.get("output", {}).get("assets_dir", "assets")

        files = sorted(os.listdir(output_dir))
        ref_files = [f for f in files if f.startswith("ref_") and f.endswith(".txt")]
        if not ref_files:
            fatal("output/ 下没有 ref_*.txt，请先跑 export.py")

        for fname in ref_files:
            name = os.path.splitext(fname)[0]
            prompt = read_txt(os.path.join(output_dir, fname))

            out_path = os.path.join(project_dir, assets_dir, f"{name}.png")

            # skip_existing: 检查 manifest 中是否已有 latest
            if skip_existing:
                manifest_path = os.path.join(project_dir, "assets_manifest.json")
                if os.path.exists(manifest_path):
                    manifest = load_json(manifest_path)
                    existing = resolve_manifest_ref(name, manifest, project_dir)
                    if existing:
                        print(f"  ⏭️ {name} 已存在 ({existing})，跳过")
                        continue

            prompts.append({
                "name": name,
                "project_id": project_id,
                "prompt": prompt,
                "aspect_ratio": ar,
                "resolution": res,
                "model": model,
                "output_dir": out_path.replace("\\", "/"),
                "reference_image_paths": [],
            })

    elif output_type == "shots":
        # ── 扫描 image_*.txt ──
        shot_cfg = config.get("shots", {})
        ar = shot_cfg.get("aspect_ratio", "16:9")
        res = shot_cfg.get("resolution", "2K")
        model = shot_cfg.get("model", "generate_image_gpt_image_2_medium")
        images_dir = config.get("output", {}).get("images_dir", "images")
        assets_dir = config.get("output", {}).get("assets_dir", "assets")

        # 读取 manifest 解析垫图 latest
        manifest_path = os.path.join(project_dir, "assets_manifest.json")
        manifest = {}
        if os.path.exists(manifest_path):
            manifest = load_json(manifest_path)

        # 读取 project.json 获取 element 映射关系
        project_json = os.path.join(project_dir, "project.json")
        elements = []
        groups = []
        if os.path.exists(project_json):
            pj = load_json(project_json)
            elements = pj.get("elements", [])
            groups = pj.get("storyboard_groups", [])
        else:
            print("  ⚠️ 没有 project.json，垫图引用将使用文件名匹配")

        # 建立 element name → ref 文件名映射
        element_to_ref = {}
        for el in elements:
            en = el.get("name", "")
            ref_file = f"ref_{en.replace(' ', '_')}" if not el.get("is_background") else f"ref_bg_{en.replace(' ', '_')}"
            element_to_ref[en] = ref_file

        # 建立 scene_num → 所在 group 的 element_refs 映射
        scene_refs = {}
        for g in groups:
            refs = g.get("element_refs", [])
            for s in g.get("scenes", []):
                sn = s.get("scene_num", 0)
                scene_refs[sn] = refs

        files = sorted(os.listdir(output_dir))
        image_files = [f for f in files if f.startswith("image_") and f.endswith(".txt")]
        if not image_files:
            fatal("output/ 下没有 image_*.txt，请先跑 export.py")

        for fname in image_files:
            name = os.path.splitext(fname)[0]
            prompt = read_txt(os.path.join(output_dir, fname))
            # 截断：去掉分隔线后的说明文字（"以上 prompt 已完整"等）
            sep = "-" * 100
            if sep in prompt:
                prompt = prompt.split(sep)[0].strip()
            out_path = os.path.join(project_dir, images_dir, f"{name}.png")

            # skip_existing
            if skip_existing:
                existing = resolve_manifest_ref(name, manifest, project_dir)
                if existing:
                    print(f"  ⏭️ {name} 已存在 ({existing})，跳过")
                    continue

            # 解析 scene_num 从文件名（image_01_xxx → 01）
            sn_match = re.match(r"image_(\d+)_", fname)
            sn = int(sn_match.group(1)) if sn_match else 0

            # 根据 scene_refs + element_to_ref 推断垫图
            ref_paths = []
            if sn in scene_refs:
                for el_name in scene_refs[sn]:
                    ref_key = element_to_ref.get(el_name, "")
                    if ref_key:
                        resolved = resolve_manifest_ref(ref_key, manifest, project_dir)
                        if resolved:
                            ref_paths.append(resolved)
                        else:
                            scanned = scan_asset_refs(ref_key, project_dir, assets_dir)
                            if scanned:
                                ref_paths.append(scanned)

            prompts.append({
                "name": name,
                "project_id": project_id,
                "prompt": prompt,
                "aspect_ratio": ar,
                "resolution": res,
                "model": model,
                "output_dir": out_path.replace("\\", "/"),
                "reference_image_paths": ref_paths,
            })

    elif output_type == "storyboard":
        # ── 从 project.json 的 storyboard_groups 构造 prompt ──
        sb_cfg = config.get("storyboard", {})
        ar = sb_cfg.get("aspect_ratio", "16:9")
        res = sb_cfg.get("resolution", "2K")
        model = sb_cfg.get("model", "generate_image_gpt_image_2_medium")
        layout_prefix = sb_cfg.get("layout_prefix", "").strip()
        assets_dir = config.get("output", {}).get("assets_dir", "assets")
        images_dir = config.get("output", {}).get("images_dir", "images")

        manifest_path = os.path.join(project_dir, "assets_manifest.json")
        manifest = {}
        if os.path.exists(manifest_path):
            manifest = load_json(manifest_path)

        # 读取 project.json
        project_json = os.path.join(project_dir, "project.json")
        groups = []
        elements = []
        vs = ""
        ac = ""
        if os.path.exists(project_json):
            pj = load_json(project_json)
            elements = pj.get("elements", [])
            groups = pj.get("storyboard_groups", [])
            vs = pj.get("visual_style", "")
            ac = pj.get("accent_color", "")
        else:
            fatal(f"找不到 {project_json}，storyboard 类型需要 project.json")

        # 建立 element name → ref 文件名映射
        element_to_ref = {}
        for el in elements:
            en = el.get("name", "")
            ref_file = f"ref_{en.replace(' ', '_')}" if not el.get("is_background") else f"ref_bg_{en.replace(' ', '_')}"
            element_to_ref[en] = ref_file

        if not groups:
            fatal("project.json 的 storyboard_groups 为空")

        for idx, g in enumerate(groups):
            name = f"{idx+1:02d}_storyboard_{g.get('label', '')}"
            out_path = os.path.join(project_dir, images_dir, f"{name}.png")
            scenes = g.get("scenes", [])
            label = g.get("label", "")

            # 构造 prompt
            parts = []
            if layout_prefix:
                parts.append(layout_prefix)
                parts.append("")
            parts.append(vs)
            parts.append("")
            parts.append("STORYBOARD FRAMES (main area, grid layout, largest section):")
            for s in scenes:
                sn = s.get("scene_num", 0)
                title = s.get("title", "")
                sb_desc = s.get("storyboard_desc", "")
                parts.append(f"Frame {sn:02d}: '{title}. {sb_desc}'")
            parts.append("Each frame box should be 16:9 portrait aspect ratio (vertical rectangle, not square, not landscape).")
            parts.append("Each frame box has white thin border, small text label at bottom with shot number.")
            parts.append("")
            parts.append(f"TOP BAR: '{idx+1}镜：{label}'")
            parts.append("")
            parts.append("SECTION 3 - SCENE DESIGN (below character panel, compact):")
            parts.append("Top-down floor plan view of camera path.")
            for s in scenes:
                title = s.get("title", "")
                cam = s.get("camera", "")
                if cam:
                    parts.append(f"Camera arc: '{title}'")
                    parts.append("Dotted line with directional arrows connecting shot positions.")
                    break
            parts.append("Shot numbers labeled at each camera position.")
            parts.append("")
            parts.append("Overall layout: cohesive animation pre-production board, all text in clean sans-serif font, white or very light cream background, thin grid lines separating sections.")
            parts.append("")

            # 元素列表（只写名称，不嵌完整 appearance）
            el_names = [el_name for el_name in g.get("element_refs", [])]
            if el_names:
                parts.append("ELEMENTS IN THIS SCENE: " + ", ".join(el_names))
                parts.append("")

            prompt = "\n".join(parts)

            # 推导垫图
            ref_paths = []
            for el_name in g.get("element_refs", []):
                ref_key = element_to_ref.get(el_name, "")
                if ref_key:
                    resolved = resolve_manifest_ref(ref_key, manifest, project_dir)
                    if resolved:
                        ref_paths.append(resolved)
                    else:
                        scanned = scan_asset_refs(ref_key, project_dir, assets_dir)
                        if scanned:
                            ref_paths.append(scanned)

            prompts.append({
                "name": name,
                "project_id": project_id,
                "prompt": prompt,
                "aspect_ratio": ar,
                "resolution": res,
                "model": model,
                "output_dir": out_path.replace("\\", "/"),
                "reference_image_paths": ref_paths,
            })

    if not prompts:
        print("  ⚠️ 没有需要生成的条目（可能已被 skip_existing 跳过）")
        sys.exit(0)

    # ── 输出 JSON（完整文件） ──
    batch = {"prompts": prompts}
    out_json = os.path.join(output_dir, f"lovart_{output_type}.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(batch, f, indent=2, ensure_ascii=False)
    print(f"  ✅ {out_json} ({len(prompts)} 项)")

    # ── 同时拆分单文件 ──
    single_dir = os.path.join(output_dir, f"{output_type}_single")
    os.makedirs(single_dir, exist_ok=True)
    for p in prompts:
        safe = p["name"].replace("/", "_").replace(" ", "_")
        single_path = os.path.join(single_dir, safe + ".json")
        with open(single_path, "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {single_dir}/ ({len(prompts)} 个单文件)")

    print()
    print(f"  ── 后续命令 ──")
    print(f"  python3 run_image_generator.py {out_json}")
    print(f"  画布: https://www.lovart.ai/canvas?projectId={project_id}")


if __name__ == "__main__":
    main()
