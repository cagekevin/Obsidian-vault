#!/usr/bin/env python3
"""
Lovart Web UI — 项目出图面板

用法:
    python3 skills/工作效率类/W6-视频创作/翻译官/lovart-web.py --dir /path/to/项目 --port 5678

替换终端命令出图流程：查看 prompt / 检查垫图 / 编辑 appearance / 一键出图。

流程定位（翻译官三件套）：
    ① export.py          → 导出提示词 + HTML + QC + 资产索引
    ② export_to_lovart.py → 拆分为单文件 JSON（refs_single / shots_single）
    ③ lovart-web.py       → 本文件：Web 面板，浏览 + 编辑 + 出图
"""

import json
import os
import re
import sys
import argparse
import subprocess
import time
import threading

from flask import Flask, request, jsonify, send_file, send_from_directory, render_template

from utils import (
    load_json, read_txt, output_dir as _utils_output_dir,
    safe_name, extract_appearance, json_filename_to_element_name,
    check_asset_exists, list_all_ref_versions, log, setup_logger,
)

log = setup_logger("lovart_web")

# ── Flask app ──
app = Flask(__name__)

# ── 全局状态 ──
PROJECT_DIR = ""
SKILLS_MAIN_DIR = ""   # skills-main 根目录（用于定位脚本）
TASKS = {}              # {task_id: {"status": "running"|"done"|"error", "log": [...], "result": ...}}


# ── 便捷封装 ──

def _output_dir():
    return _utils_output_dir(PROJECT_DIR)


def _assets_dir():
    return os.path.join(PROJECT_DIR, "assets")


def read_txt_content(path):
    return read_txt(path)


def build_ref_images(jdata):
    images = []
    for rp in jdata.get("reference_image_paths", []):
        exists, disp = check_asset_exists(rp, _assets_dir())
        images.append({
            "originalPath": rp,
            "displayName": os.path.basename(rp),
            "exists": exists,
            "displayPath": disp,
        })
    return images


# ══════════════════════════════════════
# API 路由（与备份版保持一致）
# ══════════════════════════════════════

@app.route("/api/project")
def api_project():
    pj = load_json(os.path.join(PROJECT_DIR, "project.json"))
    od = _output_dir()
    ad = _assets_dir()

    elements = pj.get("elements", [])
    groups = pj.get("storyboard_groups", [])
    all_scenes = []
    for g in groups:
        all_scenes.extend(g.get("scenes", []))
    project_name = os.path.basename(os.path.abspath(PROJECT_DIR))

    result = {
        "projectName": project_name,
        "visualStyle": pj.get("visual_style", ""),
        "accentColor": pj.get("accent_color", ""),
        "tabs": {},
    }

    files = []
    if os.path.isdir(od):
        files = sorted(os.listdir(od))

    # 全片总览
    overview_items = []
    for f in files:
        if "全片总览" in f and f.endswith(".txt"):
            overview_items.append({"filename": f, "content": read_txt_content(os.path.join(od, f))})
    result["tabs"]["all"] = overview_items

    # 故事板图片
    storyboard_single_dir = os.path.join(od, "storyboard_single")
    group_items = []
    if os.path.isdir(storyboard_single_dir):
        for f in sorted(os.listdir(storyboard_single_dir)):
            if f.endswith(".json"):
                sp = os.path.join(storyboard_single_dir, f)
                jdata = load_json(sp)
                ref_images = build_ref_images(jdata)
                sn_match = re.match(r'(\d+)_', f)
                idx = int(sn_match.group(1)) - 1 if sn_match else -1
                scenes = []
                if 0 <= idx < len(groups):
                    scenes = groups[idx].get("scenes", [])
                all_refs = []
                if 0 <= idx < len(groups):
                    for el_name in groups[idx].get("element_refs", []):
                        all_refs.extend(list_all_ref_versions(el_name, None, _assets_dir()))
                seen = set()
                all_refs_uniq = []
                for r in all_refs:
                    if r not in seen:
                        seen.add(r)
                        all_refs_uniq.append(r)
                group_items.append({
                    "filename": f, "name": jdata.get("name", f), "prompt": jdata.get("prompt", ""),
                    "appearance": "", "aspectRatio": jdata.get("aspect_ratio", ""),
                    "resolution": jdata.get("resolution", ""), "model": jdata.get("model", ""),
                    "referenceImages": ref_images, "allRefImages": all_refs_uniq,
                    "outputDir": jdata.get("output_dir", ""), "scenes": scenes, "groupId": idx,
                })
    if not group_items:
        for f in files:
            if re.match(r'\d+_storyboard_.*\.txt$', f) and "全片总览" not in f:
                group_items.append({"filename": f, "content": read_txt_content(os.path.join(od, f))})
    result["tabs"]["group"] = group_items

    # 故事板视频
    groupvideo_items = []
    for f in files:
        if f.startswith("video_group_") and f.endswith(".txt"):
            groupvideo_items.append({"filename": f, "content": read_txt_content(os.path.join(od, f))})
    result["tabs"]["groupvideo"] = groupvideo_items

    # 图片单帧
    shots_single_dir = os.path.join(od, "shots_single")
    shot_items = []
    if os.path.isdir(shots_single_dir):
        for f in sorted(os.listdir(shots_single_dir)):
            if f.endswith(".json"):
                sp = os.path.join(shots_single_dir, f)
                jdata = load_json(sp)
                ref_images = build_ref_images(jdata)
                sn_match = re.match(r'image_(\d+)_', f)
                sn = int(sn_match.group(1)) if sn_match else 0
                matched_scenes = []
                for s in all_scenes:
                    if s.get("scene_num") == sn:
                        matched_scenes.append(s)
                        break
                all_refs = []
                if matched_scenes:
                    for g in groups:
                        for s in g.get("scenes", []):
                            if s.get("scene_num") == sn:
                                for el_name in g.get("element_refs", []):
                                    all_refs.extend(list_all_ref_versions(el_name, None, _assets_dir()))
                                break
                        if all_refs:
                            break
                seen = set()
                all_refs_uniq = []
                for r in all_refs:
                    if r not in seen:
                        seen.add(r)
                        all_refs_uniq.append(r)
                shot_items.append({
                    "filename": f, "name": jdata.get("name", f), "prompt": jdata.get("prompt", ""),
                    "appearance": "", "aspectRatio": jdata.get("aspect_ratio", ""),
                    "resolution": jdata.get("resolution", ""), "model": jdata.get("model", ""),
                    "referenceImages": ref_images, "allRefImages": all_refs_uniq,
                    "outputDir": jdata.get("output_dir", ""), "scenes": matched_scenes, "sceneNum": sn,
                })
    result["tabs"]["shot"] = shot_items

    # 单镜视频
    video_items = []
    for f in files:
        if re.match(r'video_\d+.*\.txt$', f) and not f.startswith("video_group_"):
            video_items.append({"filename": f, "content": read_txt_content(os.path.join(od, f))})
    result["tabs"]["video"] = video_items

    # 角色和场景
    refs_single_dir = os.path.join(od, "refs_single")
    ref_items = []
    if os.path.isdir(refs_single_dir):
        for f in sorted(os.listdir(refs_single_dir)):
            if f.endswith(".json"):
                sp = os.path.join(refs_single_dir, f)
                jdata = load_json(sp)
                appearance = extract_appearance(jdata.get("prompt", ""))
                ref_images = build_ref_images(jdata)
                el_name = json_filename_to_element_name(f)
                matched_el = None
                for el in elements:
                    if el.get("name") == el_name:
                        matched_el = el
                        break
                ref_items.append({
                    "filename": f, "name": jdata.get("name", f), "elementName": el_name,
                    "appearance": appearance, "aspectRatio": jdata.get("aspect_ratio", ""),
                    "resolution": jdata.get("resolution", ""), "model": jdata.get("model", ""),
                    "referenceImages": ref_images, "allRefImages": list_all_ref_versions(el_name, f, _assets_dir()),
                    "outputDir": jdata.get("output_dir", ""),
                    "elementIsBackground": matched_el.get("is_background", False) if matched_el else False,
                })
    result["tabs"]["ref"] = ref_items

    result["tabs"]["asset"] = {"content": read_txt_content(os.path.join(od, "asset-index.md"))}
    result["tabs"]["qc"] = {"content": read_txt_content(os.path.join(od, "qc-report.md"))}
    img_files = []
    if os.path.isdir(ad):
        for f in sorted(os.listdir(ad)):
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                img_files.append(f)
    result["tabs"]["img"] = img_files

    all_assets = []
    if os.path.isdir(ad):
        for f in sorted(os.listdir(ad)):
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                all_assets.append(f)
    result["allAssets"] = all_assets

    return jsonify(result)


@app.route("/api/assets/<path:filepath>")
def api_assets(filepath):
    ad = _assets_dir()
    safe_path = os.path.normpath(filepath)
    if safe_path.startswith("..") or os.path.isabs(safe_path):
        return jsonify({"error": "forbidden"}), 403
    full_path = os.path.join(ad, safe_path)
    if os.path.exists(full_path):
        return send_file(full_path)
    return jsonify({"error": "not found"}), 404


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(force=True)
    json_filename = data.get("name", "")
    new_appearance = data.get("appearance", "")

    if not json_filename:
        return jsonify({"error": "missing name"}), 400

    split_type = "refs" if json_filename.startswith("ref_") else "shots"
    el_name = json_filename_to_element_name(json_filename)
    pj_path = os.path.join(PROJECT_DIR, "project.json")
    pj = load_json(pj_path)

    found = False
    for el in pj.get("elements", []):
        if el.get("name") == el_name:
            el["appearance"] = new_appearance
            found = True
            break

    if not found:
        return jsonify({"error": f"element '{el_name}' not found in project.json"}), 404

    with open(pj_path, "w", encoding="utf-8") as f:
        json.dump(pj, f, indent=2, ensure_ascii=False)

    task_id = f"{int(time.time() * 1000)}"
    _trans_dir = os.path.dirname(os.path.abspath(__file__))

    def run_generation():
        log_lines = []
        try:
            log_lines.append(f"[1/4] 已更新 project.json: {el_name} appearance")
            export_script = os.path.join(_trans_dir, "export.py")
            log_lines.append(f"[2/4] running export.py...")
            r = subprocess.run([sys.executable, export_script, PROJECT_DIR, "--html"], capture_output=True, text=True, timeout=120, cwd=SKILLS_MAIN_DIR)
            if r.returncode != 0: TASKS[task_id] = {"status": "error", "log": log_lines + [f"export.py failed: {r.stderr}"]}; return
            log_lines.append(f"[2/4] export.py done")

            split_script = os.path.join(_trans_dir, "export_to_lovart.py")
            log_lines.append(f"[3/4] running export_to_lovart.py --type={split_type}...")
            r = subprocess.run([sys.executable, split_script, PROJECT_DIR, f"--type={split_type}"], capture_output=True, text=True, timeout=120, cwd=SKILLS_MAIN_DIR)
            if r.returncode != 0: TASKS[task_id] = {"status": "error", "log": log_lines + [f"export_to_lovart.py failed: {r.stderr}"]}; return
            log_lines.append(f"[3/4] export_to_lovart.py done")

            single_dir = os.path.join(_output_dir(), f"{split_type}_single")
            target_json = os.path.join(single_dir, json_filename)

            selected_refs = data.get("selectedRefs", [])
            if selected_refs and os.path.exists(target_json):
                ref_paths = []
                for sr in selected_refs:
                    full = os.path.join(_assets_dir(), sr)
                    if os.path.exists(full):
                        ref_paths.append(full)
                if ref_paths:
                    with open(target_json, "r", encoding="utf-8") as f:
                        jd = json.load(f)
                    jd["reference_image_paths"] = ref_paths
                    with open(target_json, "w", encoding="utf-8") as f:
                        json.dump(jd, f, indent=2, ensure_ascii=False)
                    log_lines.append(f"[3.5/4] 垫图覆盖为: {selected_refs}")

            if not os.path.exists(target_json):
                TASKS[task_id] = {"status": "error", "log": log_lines + [f"JSON not found: {target_json}"]}; return

            gen_script = os.path.join(SKILLS_MAIN_DIR, "skills/工作效率类/W7-API链接/lovart-skill/run_image_generator.py")
            log_lines.append(f"[4/4] running run_image_generator.py {json_filename}...")
            r = subprocess.run([sys.executable, gen_script, target_json], capture_output=True, text=True, timeout=900, cwd=SKILLS_MAIN_DIR)
            log_lines.append(f"[4/4] run_image_generator.py exit code: {r.returncode}")
            if r.stdout: log_lines.append(r.stdout)
            if r.stderr: log_lines.append(r.stderr)

            TASKS[task_id] = {"status": "done", "log": log_lines, "returnCode": r.returncode}

        except subprocess.TimeoutExpired:
            TASKS[task_id] = {"status": "error", "log": log_lines + ["Timeout exceeded"]}
        except Exception as e:
            TASKS[task_id] = {"status": "error", "log": log_lines + [str(e)]}

    t = threading.Thread(target=run_generation, daemon=True)
    t.start()
    return jsonify({"taskId": task_id, "status": "running", "elementName": el_name})


@app.route("/api/generate-scene", methods=["POST"])
def api_generate_scene():
    data = request.get_json(force=True)
    json_filename = data.get("name", "")
    new_scenes = data.get("scenes", [])
    scene_type = data.get("type", "storyboard")  # "storyboard" 或 "shot"

    if not json_filename or not new_scenes:
        return jsonify({"error": "missing name or scenes"}), 400

    pj_path = os.path.join(PROJECT_DIR, "project.json")
    pj = load_json(pj_path)
    groups = pj.get("storyboard_groups", [])

    if scene_type == "storyboard":
        sn_match = re.match(r"(\d+)_", json_filename)
        idx = int(sn_match.group(1)) - 1 if sn_match else -1
        if idx >= len(groups):
            return jsonify({"error": f"group index {idx} out of range"}), 404
        group = groups[idx]
        for si, desc in enumerate(new_scenes):
            if si < len(group.get("scenes", [])):
                group["scenes"][si]["storyboard_desc"] = desc
        export_type = "storyboard"
        log_label = f"group[{idx}] scenes"
    else:
        sn_match = re.match(r"image_(\d+)_", json_filename)
        sn = int(sn_match.group(1)) if sn_match else 0
        updated = False
        for g in groups:
            for s in g.get("scenes", []):
                if s.get("scene_num") == sn:
                    s["description"] = new_scenes[0] if new_scenes else s.get("description", "")
                    updated = True
                    break
            if updated:
                break
        if not updated:
            return jsonify({"error": f"scene num {sn} not found"}), 404
        export_type = "shots"
        log_label = f"scene {sn} description"

    with open(pj_path, "w", encoding="utf-8") as f:
        json.dump(pj, f, indent=2, ensure_ascii=False)

    task_id = f"{int(time.time() * 1000)}"

    def run_generation():
        log_lines = []
        try:
            log_lines.append(f"[1/4] 已更新 project.json: {log_label}")
            _trans_dir = os.path.dirname(os.path.abspath(__file__))

            export_script = os.path.join(_trans_dir, "export.py")
            log_lines.append(f"[2/4] running export.py...")
            r = subprocess.run([sys.executable, export_script, PROJECT_DIR, "--html"], capture_output=True, text=True, timeout=120, cwd=SKILLS_MAIN_DIR)
            if r.returncode != 0: TASKS[task_id] = {"status": "error", "log": log_lines + [f"export.py failed: {r.stderr}"]}; return

            split_script = os.path.join(_trans_dir, "export_to_lovart.py")
            log_lines.append(f"[3/4] running export_to_lovart.py --type={export_type}...")
            r = subprocess.run([sys.executable, split_script, PROJECT_DIR, f"--type={export_type}"], capture_output=True, text=True, timeout=120, cwd=SKILLS_MAIN_DIR)
            if r.returncode != 0: TASKS[task_id] = {"status": "error", "log": log_lines + [f"export_to_lovart.py failed: {r.stderr}"]}; return

            single_dir = "storyboard_single" if export_type == "storyboard" else "shots_single"
            target_json = os.path.join(_output_dir(), single_dir, json_filename)
            selected_refs = data.get("selectedRefs", [])
            if selected_refs and os.path.exists(target_json):
                ref_paths = []
                for sr in selected_refs:
                    full = os.path.join(_assets_dir(), sr)
                    if os.path.exists(full): ref_paths.append(full)
                if ref_paths:
                    with open(target_json, "r", encoding="utf-8") as f: jd = json.load(f)
                    jd["reference_image_paths"] = ref_paths
                    with open(target_json, "w", encoding="utf-8") as f: json.dump(jd, f, indent=2, ensure_ascii=False)

            if not os.path.exists(target_json): TASKS[task_id] = {"status": "error", "log": log_lines + [f"JSON not found: {target_json}"]}; return

            gen_script = os.path.join(SKILLS_MAIN_DIR, "skills/工作效率类/W7-API链接/lovart-skill/run_image_generator.py")
            r = subprocess.run([sys.executable, gen_script, target_json], capture_output=True, text=True, timeout=900, cwd=SKILLS_MAIN_DIR)
            TASKS[task_id] = {"status": "done", "log": log_lines + [r.stdout, r.stderr], "returnCode": r.returncode}

        except subprocess.TimeoutExpired: TASKS[task_id] = {"status": "error", "log": log_lines + ["Timeout exceeded"]}
        except Exception as e: TASKS[task_id] = {"status": "error", "log": log_lines + [str(e)]}

    threading.Thread(target=run_generation, daemon=True).start()
    return jsonify({"taskId": task_id, "status": "running"})


@app.route("/api/task/<task_id>")
def api_task_status(task_id):
    task = TASKS.get(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404
    return jsonify(task)


@app.route("/")
def index():
    return render_template("index.html")


# ══════════════════════════════════════
# 启动入口
# ══════════════════════════════════════

if __name__ == "__main__":
    _parser = argparse.ArgumentParser(description="Lovart Web UI")
    _parser.add_argument("--dir", required=True, help="项目目录路径")
    _parser.add_argument("--port", type=int, default=5678, help="端口号（默认5678）")
    _args = _parser.parse_args()

    PROJECT_DIR = os.path.abspath(_args.dir)
    SKILLS_MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))

    if not os.path.isfile(os.path.join(PROJECT_DIR, "project.json")):
        log.error(f"项目目录下找不到 project.json: {PROJECT_DIR}")
        sys.exit(1)

    log.info(f"Lovart Web UI")
    log.info(f"  项目: {PROJECT_DIR}")
    log.info(f"  skills-main: {SKILLS_MAIN_DIR}")
    log.info(f"  http://127.0.0.1:{_args.port}")

    app.run(host="127.0.0.1", port=_args.port, debug=False)
