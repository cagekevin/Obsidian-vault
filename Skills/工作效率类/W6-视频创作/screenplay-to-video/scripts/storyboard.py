#!/usr/bin/env python3
"""
故事板 JSON 拼装脚本：读取 storyboard_data_N.json → 组装 8 段式 prompt → 输出 configs/storyboard_N.json

核心原则：Agent 做创作决策，脚本做机械拼装。
用法: python storyboard.py <项目路径> --data prompts/storyboard_data_N.json
"""

import json, os, sys, re
from manifest_resolver import load_manifest, resolve as resolve_ref

PROMPT_LEAD = (
    "IMPORTANT: Generate exactly ONE single image containing an animation "
    "pre-production board layout, full grid layout with clearly labeled sections. "
    "Do NOT generate separate images."
)

CLOSING = (
    "Overall layout: cohesive animation pre-production board, all text in "
    "clean sans-serif font, white or very light cream background, thin grid lines "
    "separating sections."
)

REF_CATEGORIES = {
    "char_":    "CHARACTER appearance — copy face, hair, body, and outfit from this image into ALL character frames",
    "product_": "PRODUCT reference — copy the exact shape, color, and appearance into relevant frames",
    "scene_":   "SCENE/ENVIRONMENT reference — use as background and environment design guide",
}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fatal(msg):
    print(f"  ❌ {msg}")
    sys.exit(1)


TOKEN_ALIASES = {
    "token_director": ["token_director", "--token-vibe", "--token-director", "token_vibe"],
    "token_lighting": ["token_lighting", "--token-light", "--token-lighting", "token_light"],
    "token_camera":   ["token_camera",   "--token-camera", "token_cam"],
}

DEFAULT_TOKENS = {
    "token_director": "Pixar 3D animation style",
    "token_lighting": "Subsurface Scattering, warm studio lighting",
    "token_camera": "medium shot, eye-level, 35mm lens",
}


def get_style_tokens(project_dir):
    """从 global_vars.json 读取风格令牌，优先 style_tokens，回退到 tokens 的 alias 映射"""
    path = os.path.join(project_dir, "prompts", "global_vars.json")
    if not os.path.exists(path):
        print("  ⚠️ prompts/global_vars.json 不存在，使用兜底令牌")
        return dict(DEFAULT_TOKENS)
    gv = load_json(path)
    # 优先用标准化的 style_tokens（Phase 2 输出规范要求写入）
    st = gv.get("style_tokens", {})
    if st.get("token_director") and st.get("token_lighting") and st.get("token_camera"):
        return {
            "token_director": st["token_director"],
            "token_lighting": st["token_lighting"],
            "token_camera":   st["token_camera"],
        }
    # 回退：从 tokens 的 --token-* 做 alias 映射
    t = gv.get("tokens", {})
    result = {}
    for out_key, aliases in TOKEN_ALIASES.items():
        val = None
        for a in aliases:
            if a in t:
                val = t[a]
                break
        result[out_key] = val or DEFAULT_TOKENS[out_key]
    return result


def infer_char_descriptions(project_dir, refs):
    """从配置前缀为 char_ 的 ref 自动查找对应的 config 并提取描述"""
    descs = []
    for key in refs:
        clean = os.path.splitext(os.path.basename(key))[0]
        if not clean.startswith("char_"):
            continue
        config_path = os.path.join(project_dir, "configs", f"{clean}.json")
        if not os.path.exists(config_path):
            # 试试剥后缀后匹配
            base = re.sub(r"_(ar\d+x\d+_\d+[kK]|ar\d+x\d+|\d+[pPkK]|v\d+)$", "", clean)
            if base != clean:
                config_path = os.path.join(project_dir, "configs", f"{base}.json")
        if os.path.exists(config_path):
            cfg = load_json(config_path)
            prompt = cfg.get("prompt", "")
            parts = prompt.split("Clean grid layout")
            desc = parts[0].strip() if parts else prompt[:200]
            if desc:
                descs.append(desc)
    return descs


def build_prompt(data, project_dir, tokens, char_descs, resolved_refs):
    """精简版故事板 prompt — 只保留视觉必需段，技术信息移入 production_notes.md"""
    # S1 — 顶部方向栏（压缩为一行）
    s1 = (
        f"TOP BAR: '{data.get('shots_total', 'N/A')}' | "
        f"Palette: {data.get('palette', 'N/A')} | "
        f"Environment: {data.get('environment', 'N/A')}."
    )

    # 垫图说明段（有垫图才写，无垫图跳过）
    if resolved_refs:
        ref_lines = [
            "⭐ REFERENCE IMAGES — YOU MUST USE THEM when drawing characters and "
            "products in the storyboard frames below. DO NOT invent appearances "
            "that differ from these references."
        ]
        for i, (key, path) in enumerate(resolved_refs, 1):
            label = "Reference image"
            for prefix, desc in REF_CATEGORIES.items():
                if key.startswith(prefix):
                    label = desc
                    break
            ref_lines.append(f"  Attachment #{i} ({os.path.basename(path)}) → {label}")
        ref_guide = " ".join(ref_lines)
    else:
        ref_guide = ""

    # S2 — 角色参考（仅当有 char_ 垫图时才生成）
    if char_descs:
        s2 = (
            f"CHARACTER REFERENCE (compact sidebar): "
            f"{' Also shown: '.join(char_descs)} "
            f"Shown in multiple poses: front view, back view, side profile, close-up portrait."
        )
    else:
        s2 = ""

    # S3 — 场景平面图（改为极小占位图标，不占文字空间）
    camera_path = data.get("camera_path", "")
    s3 = (
        f"SCENE TOP-DOWN MINI DIAGRAM (small corner inset): "
        f"Camera path '{camera_path}'." if camera_path else ""
    )

    # S4 — 故事板网格（主力区域，尽量宽松）
    shots = data.get("shots", [])
    if not shots:
        fatal("shots 数组为空，无法生成故事板")
    frames = []
    for i, s in enumerate(shots):
        title = s.get("title", f"Shot {i+1}")
        en = s.get("en", "").strip()
        if not en:
            fatal(f"Shot {i+1} ('{title}') 缺少 'en' 字段")
        frames.append(f"Frame {i+1:02d}: 'Shot {i+1:02d} — {title}. {en}'")
    s4 = (
        "STORYBOARD FRAMES (main area, grid layout, largest section): "
        f"{' '.join(frames)} "
        "Each frame box has white thin border, small text label at bottom with shot number."
    )

    # 风格令牌行（动态注入）
    token_line = (
        f"Director style: {tokens['token_director']}. "
        f"Lighting: {tokens['token_lighting']}. "
        f"Camera: {tokens['token_camera']}."
    )

    # 只拼非空的辅助段
    auxiliary = " ".join(seg for seg in [s1, s2, s3] if seg)
    hierarchy_parts = [
        "Storyboard frames are PRIMARY — allocate the largest area",
    ]
    if char_descs:
        hierarchy_parts.append("Character reference is SECONDARY — compact sidebar")
    hierarchy_parts.append("Top bar and scene diagram are SUPPLEMENTARY — minimal elements")

    full = (
        f"{PROMPT_LEAD}. VISUAL HIERARCHY: {'; '.join(hierarchy_parts)}. "
        f"Let the visual weight naturally reflect this priority order. "
        f"{ref_guide} {token_line} "
        f"{s4} "
        f"{auxiliary} {CLOSING}"
    )
    return " ".join(full.split())


def main():
    if len(sys.argv) < 2:
        print("用法: python storyboard.py <项目路径> --data prompts/storyboard_data_N.json")
        sys.exit(1)

    project_dir = sys.argv[1]
    data_path = next(
        (sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--data"),
        None,
    )
    if not data_path:
        fatal("需要 --data 参数指定 storyboard_data JSON 路径")

    data_path = data_path if os.path.isabs(data_path) else os.path.join(project_dir, data_path)
    if not os.path.exists(data_path):
        fatal(f"数据文件不存在: {data_path}")

    data = load_json(data_path)
    group = data.get("group", 1)
    print(f"  📦 组 {group}")

    # 1) 读取风格令牌
    tokens = get_style_tokens(project_dir)
    print(f"  令牌: {tokens['token_director'][:50]}...")

    # 2) 解析垫图路径（manifest 版本追踪）
    manifest = load_manifest(project_dir)
    ref_keys = data.get("refs", [])
    resolved_refs = [(k, p) for k in ref_keys if (p := resolve_ref(k, manifest, project_dir))]
    print(f"  垫图: {len(resolved_refs)}/{len(ref_keys)} 已解析")

    # 3) 自动推断角色描述（从 char_ 前缀的 ref 反查 config）
    char_descs = infer_char_descriptions(project_dir, ref_keys)
    print(f"  角色描述: {len(char_descs)} 个")

    # 4) 拼装 8 段式 prompt
    prompt = build_prompt(data, project_dir, tokens, char_descs, resolved_refs)

    # 5) 写 config JSON
    config = {
        "name": f"storyboard_{group}",
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "resolution": "1K",
        "model": "generate_image_gpt_image_2_medium",
        "output_dir": os.path.join(project_dir, "images", f"storyboard_{group}.png").replace("\\", "/"),
        "reference_image_paths": [p for _, p in resolved_refs],
    }

    out_dir = os.path.join(project_dir, "configs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"storyboard_{group}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"  ✅ configs/storyboard_{group}.json ({len(data.get('shots', []))}镜, {len(resolved_refs)}垫图)")
    if resolved_refs:
        missing = sum(1 for _, p in resolved_refs if not os.path.exists(p))
        print(f"     垫图状态: {'全部存在 ✅' if missing == 0 else f'{missing} 个缺失 ⚠️'}")
    print(f"  ⚠️  确认后执行:")
    print(f'     python run_image_generator.py "{out_path}"')


if __name__ == "__main__":
    main()
