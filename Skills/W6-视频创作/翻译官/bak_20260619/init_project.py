#!/usr/bin/env python3
"""
项目初始化脚本：创建目录结构 + Lovart 画布 + 配置文件。

用法:
    python3 init_project.py /path/to/项目目录

流程:
    1. 创建 assets/ images/ videos/ output/ 目录
    2. 创建空的 assets_manifest.json
    3. 调 lovart_project.py 创建 Lovart 画布 → 获取 UUID
    4. 创建 lovart_config.json（含 project_id + 默认参数）
"""

import json, os, subprocess, sys

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LOVART_PROJECT_PY = os.path.join(
    SKILL_DIR, "../../W7-API链接/lovart-skill/lovart_project.py"
)


def fatal(msg):
    print(f"  ❌ {msg}")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    project_name = os.path.basename(project_dir)

    # ── 1) 创建目录结构 ──
    dirs = ["assets", "images", "videos", "output"]
    for d in dirs:
        os.makedirs(os.path.join(project_dir, d), exist_ok=True)
    print(f"  ✅ 目录结构已创建: {' '.join(dirs)}")

    # ── 2) 创建空的 assets_manifest.json ──
    manifest_path = os.path.join(project_dir, "assets_manifest.json")
    if not os.path.exists(manifest_path):
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2, ensure_ascii=False)
        print(f"  ✅ assets_manifest.json 已创建")
    else:
        print(f"  ⚠️ assets_manifest.json 已存在，跳过")

    # ── 3) 创建 Lovart 画布 ──
    lovart_py = os.path.normpath(LOVART_PROJECT_PY)
    if not os.path.exists(lovart_py):
        fatal(f"找不到 lovart_project.py: {lovart_py}")

    print(f"  🔧 创建 Lovart 画布: {project_name}")
    result = subprocess.run(
        [sys.executable, lovart_py, "init", project_name],
        capture_output=True, text=True, cwd=os.path.dirname(lovart_py),
    )
    if result.returncode != 0:
        print(f"  stderr: {result.stderr}")
        fatal(f"Lovart 项目创建失败: {result.stdout.strip()}")
    print(f"  ✅ {result.stdout.strip()}")

    # 从 projects.json 读取刚创建的 UUID
    projects_json = os.path.join(os.path.dirname(lovart_py), "projects.json")
    project_id = ""
    if os.path.exists(projects_json):
        with open(projects_json, "r", encoding="utf-8") as f:
            projects = json.load(f)
        entry = projects.get(project_name, {})
        if isinstance(entry, dict):
            project_id = entry.get("uuid", "")
        elif isinstance(entry, str):
            project_id = entry
    if not project_id:
        fatal("无法获取 Lovart 项目 UUID")

    # ── 4) 创建 lovart_config.json ──
    config_path = os.path.join(project_dir, "lovart_config.json")
    if not os.path.exists(config_path):
        config = {
            "project_id": project_id,
            "refs": {
                "resolution": "1K",
                "aspect_ratio": "4:3",
                "model": "generate_image_gpt_image_2_medium"
            },
            "shots": {
                "resolution": "2K",
                "aspect_ratio": "16:9",
                "model": "generate_image_gpt_image_2_medium"
            },
            "output": {
                "assets_dir": "assets",
                "images_dir": "images",
                "videos_dir": "videos"
            },
            "skip_existing": False
        }
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"  ✅ lovart_config.json 已创建（含 project_id）")
    else:
        print(f"  ⚠️ lovart_config.json 已存在，跳过")

    # ── 5) 创建空的 project.json ──
    project_json_path = os.path.join(project_dir, "project.json")
    if not os.path.exists(project_json_path):
        template = {
            "visual_style": "",
            "elements": [],
            "storyboard_groups": []
        }
        with open(project_json_path, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        print(f"  ✅ project.json 已创建（空模板，等待 AI 填充）")
    else:
        print(f"  ⚠️ project.json 已存在，跳过")

    print(f"\n  ── 初始化完成 ──")
    print(f"  项目: {project_name}")
    print(f"  UUID: {project_id}")
    print(f"  画布: https://www.lovart.ai/canvas?projectId={project_id}")
    print(f"\n  lovart_config.json 中的参数可自行修改（分辨率/模型/比例）")


if __name__ == "__main__":
    main()
