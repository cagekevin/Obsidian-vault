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

Pipeline 节点名: convert_to_lovart
"""

import json, os, sys, re

from utils import (
    load_json, read_txt, fatal, safe_name,
    resolve_manifest_ref, scan_asset_refs,
    output_dir, get_all_scenes, get_elements, load_config,
    log, setup_logger,
)
from pipeline import Pipeline, register

log = setup_logger("lovart_convert")

LOVART_MODELS = [
    "generate_image_gpt_image_2", "generate_image_gpt_image_2_low",
    "generate_image_gpt_image_2_medium", "generate_image_gpt_image_2_high",
    "generate_image_nano_banana_pro", "generate_image_nano_banana_2",
    "generate_image_seedream_v5", "generate_image_nano_banana",
    "generate_image_midjourney",
]

# ══════════════════════════════════════
# 注册到 Pipeline
# ══════════════════════════════════════

pipe = Pipeline()


@register(pipe, dependencies=["export_main"])
def convert_to_lovart(ctx):
    """入口：根据 ctx 中的 type 转换对应文件"""
    project_dir = ctx["project_dir"]
    output_type = ctx.get("lovart_type", "refs")

    if not os.path.isdir(os.path.join(project_dir, "output")):
        fatal("output/ 目录不存在，请先运行 export.py")

    config = load_config(project_dir)
    project_id = config.get("project_id", "")
    if not project_id:
        fatal("lovart_config.json 缺少 project_id")

    if output_type == "refs":
        result = _convert_refs(project_dir, project_id, config)
    elif output_type == "shots":
        result = _convert_shots(project_dir, project_id, config)
    elif output_type == "storyboard":
        result = _convert_storyboard(project_dir, project_id, config)
    else:
        fatal(f"未知类型: {output_type}")

    ctx["lovart_result"] = result
    log.info(f"转换完成: {output_type} → {result}")
    return ctx


# ══════════════════════════════════════
# refs 转换
# ══════════════════════════════════════

def _convert_refs(project_dir, project_id, config):
    out_dir = output_dir(project_dir)
    refs_config = config.get("refs", {})

    tasks = []
    for fn in sorted(os.listdir(out_dir)):
        if not fn.startswith("ref_"):
            continue
        fpath = os.path.join(out_dir, fn)
        prompt = read_txt(fpath)
        # 垫图：按文件名找 assets/ 下匹配的图片
        ref_key = os.path.splitext(fn)[0]
        manifest_path = os.path.join(project_dir, "assets_manifest.json")
        if os.path.exists(manifest_path):
            manifest = load_json(manifest_path)
            ref_image = resolve_manifest_ref(ref_key, manifest, project_dir)
        else:
            ref_image = scan_asset_refs(ref_key, project_dir)

        task = {
            "project_id": project_id,
            "type": "ref",
            "title": fn,
            "prompt": prompt,
            "resolution": refs_config.get("resolution", "1K"),
            "aspect_ratio": refs_config.get("aspect_ratio", "4:3"),
            "model": refs_config.get("model", "generate_image_gpt_image_2_medium"),
        }
        if ref_image:
            task["ref_image"] = ref_image
        tasks.append(task)

    out_path = os.path.join(out_dir, "lovart_refs.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"tasks": tasks}, f, indent=2, ensure_ascii=False)
    log.info(f"  {os.path.abspath(out_path)} ({len(tasks)} tasks)")
    return out_path


# ══════════════════════════════════════
# shots 转换
# ══════════════════════════════════════

def _convert_shots(project_dir, project_id, config):
    out_dir = output_dir(project_dir)
    shots_config = config.get("shots", {})

    manifest_path = os.path.join(project_dir, "assets_manifest.json")
    manifest = load_json(manifest_path) if os.path.exists(manifest_path) else {}

    tasks = []
    for fn in sorted(os.listdir(out_dir)):
        if not fn.startswith("image_"):
            continue
        fpath = os.path.join(out_dir, fn)
        prompt = read_txt(fpath)

        # 垫图：从 manifest 解析同名 key
        ref_key = os.path.splitext(fn)[0]
        ref_image = resolve_manifest_ref(ref_key, manifest, project_dir)
        if not ref_image:
            ref_image = scan_asset_refs(ref_key, project_dir)

        task = {
            "project_id": project_id,
            "type": "shot",
            "title": fn,
            "prompt": prompt,
            "resolution": shots_config.get("resolution", "2K"),
            "aspect_ratio": shots_config.get("aspect_ratio", "16:9"),
            "model": shots_config.get("model", "generate_image_gpt_image_2_medium"),
        }
        if ref_image:
            task["ref_image"] = ref_image
        tasks.append(task)

    out_path = os.path.join(out_dir, "lovart_shots.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"tasks": tasks}, f, indent=2, ensure_ascii=False)
    log.info(f"  {os.path.abspath(out_path)} ({len(tasks)} tasks)")
    return out_path


# ══════════════════════════════════════
# storyboard 转换
# ══════════════════════════════════════

def _convert_storyboard(project_dir, project_id, config):
    out_dir = output_dir(project_dir)
    # 读 project.json 取 element_refs
    pj_path = os.path.join(project_dir, "project.json")
    if not os.path.exists(pj_path):
        fatal(f"找不到 {pj_path}")
    data = load_json(pj_path)
    elements = get_elements(data)
    groups = data.get("storyboard_groups", [])
    vs = data.get("visual_style", "")
    refs_config = config.get("refs", {})

    tasks = []
    for fn in sorted(os.listdir(out_dir)):
        if not fn.endswith("_storyboard_.txt") and "_storyboard_" not in fn:
            continue
        if "全片总览" in fn:
            continue
        fpath = os.path.join(out_dir, fn)
        prompt = read_txt(fpath)

        # 从文件名提取 label 以匹配 group
        label_match = re.search(r'_storyboard_(.+)\.txt', fn)
        label = label_match.group(1).replace('-', ' ') if label_match else ""

        # 找该组对应的 element_refs
        group_refs = []
        for g in groups:
            if g.get("label", "").lower().replace(' ', '-') == label.lower().replace(' ', '-'):
                group_refs = g.get("element_refs", [])
                break
        if not group_refs:
            group_refs = [g.get("element_refs", []) for g in groups if g.get("element_refs")]

        # 垫图
        ref_images = []
        for ref_name in (group_refs if isinstance(group_refs, list) else []):
            el = next((e for e in elements if e.get("name") == ref_name), None)
            if el and el.get("reference", True) is not False:
                ref_key = safe_name(el.get("name", ""))
                manifest_path = os.path.join(project_dir, "assets_manifest.json")
                if os.path.exists(manifest_path):
                    manifest = load_json(manifest_path)
                    img = resolve_manifest_ref(ref_key, manifest, project_dir)
                else:
                    img = scan_asset_refs(ref_key, project_dir)
                if img:
                    ref_images.append(img)

        task = {
            "project_id": project_id,
            "type": "storyboard",
            "title": fn,
            "prompt": prompt,
            "resolution": refs_config.get("resolution", "1K"),
            "aspect_ratio": refs_config.get("aspect_ratio", "4:3"),
            "model": refs_config.get("model", "generate_image_gpt_image_2_medium"),
        }
        if ref_images:
            task["ref_images"] = ref_images
        tasks.append(task)

    out_path = os.path.join(out_dir, "lovart_storyboard.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"tasks": tasks}, f, indent=2, ensure_ascii=False)
    log.info(f"  {os.path.abspath(out_path)} ({len(tasks)} tasks)")
    return out_path


# ══════════════════════════════════════
# 命令行入口
# ══════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    output_type = sys.argv[2].replace("--type=", "").replace("--type ", "")
    if output_type not in ("refs", "shots", "storyboard"):
        fatal("--type 必须是 refs, shots 或 storyboard")

    ctx = {
        "project_dir": project_dir,
        "lovart_type": output_type,
    }

    pipe.run("convert_to_lovart", ctx=ctx)
