#!/usr/bin/env python3
"""
【board_to_video.py】故事板到视频：装配 + 校验 + 填垫图

工作分工：
  Agent 负责创作（storyboard_data_N.json + groupN_prompt_video.json 草稿）
  本脚本负责机械（装配、校验、填写）

用法:
  # 默认：垫图从 assets_manifest.json 解析本地路径
  python3 board_to_video.py /path/to/project <组号>

  # 后补：故事板图生成后，把图作为视频垫图（CDN URL 方式）
  python3 board_to_video.py /path/to/project <组号> --board-cdn <CDN_URL>

流程:
  1. 校验 storyboard_data_N.json, groupN_prompt_video.json 存在
  2. 通过 assets_manifest.json 解析 refs 垫图路径
  3. 运行 storyboard.py 装配 configs/storyboard_N.json
  4. 读取 groupN_prompt_video.json，填入解析后的垫图路径（首次自动备份原稿）
"""

import json, os, sys, subprocess
from manifest_resolver import load_manifest, resolve as resolve_manifest_ref

# 硬闸门校验
import validate_project

STORY_DIR = os.path.dirname(os.path.abspath(__file__))
LOVART_DIR = os.path.join(STORY_DIR, "../../W7-API链接/lovart-skill")


def fatal(msg):
    print(f"  ❌ {msg}")
    sys.exit(1)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def backup_path(path):
    """首次覆盖前备份原稿：group1_prompt_video.json → group1_prompt_video.orig.json"""
    orig = path.replace(".json", ".orig.json")
    if not os.path.exists(orig):
        import shutil
        shutil.copy2(path, orig)
        print(f"  💾 原稿已备份: {os.path.basename(orig)}")
    return path





def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    group = int(sys.argv[2])
    board_cdn = None
    for i, a in enumerate(sys.argv):
        if a == "--board-cdn" and i + 1 < len(sys.argv):
            board_cdn = sys.argv[i + 1]

    if not os.path.isdir(project_dir):
        fatal(f"项目目录不存在: {project_dir}")

    print(f"\n ═══ Group {group} 准备 ═══\n")

    # ── 1) 校验 Agent 创作文件 ──
    data_path = os.path.join(project_dir, "prompts", f"storyboard_data_{group}.json")
    video_draft_path = os.path.join(project_dir, "prompts", f"group{group}_prompt_video.json")

    if not os.path.exists(data_path):
        fatal(f"找不到 storyboard_data_{group}.json —— Agent 你还没写吧？")

    data = load_json(data_path)
    print(f"  ✅ storyboard_data_{group}.json ({len(data.get('shots', []))} 镜)")

    if not os.path.exists(video_draft_path):
        fatal(f"找不到 group{group}_prompt_video.json —— Agent 你还没写视频描述吧？")

    video_draft = load_json(video_draft_path)
    if not video_draft.get("prompt", "").strip():
        fatal("video prompt 草稿的 prompt 字段为空")
    print(f"  ✅ group{group}_prompt_video.json (已有 Agent 写的视频描述)")

    # ── 🔒 硬闸门校验 ──
    print(f"  🔒 执行前置校验...")
    if not validate_project.run(project_dir, types=["data", "video", "storyboard"], group=group):
        fatal(f"校验未通过，请修复后重试")
    print(f"  🔒 校验全部通过\n")

    # ── 2) 通过 assets_manifest.json 解析 refs 垫图 ──
    manifest_path = os.path.join(project_dir, "assets_manifest.json")
    manifest = load_json(manifest_path) if os.path.exists(manifest_path) else {}
    refs = data.get("refs", [])
    resolved_paths = []
    for key in refs:
        p = resolve_manifest_ref(key, manifest, project_dir)
        if p:
            resolved_paths.append(p)
        else:
            print(f"  ⚠️ 资产 '{key}' 在 manifest/assets 中未找到，跳过")
    if resolved_paths:
        print(f"  ✅ 垫图: {len(resolved_paths)} 个本地路径已解析")
    else:
        print(f"  ⚠️ 无垫图解析，仅用 --board-cdn")

    # ── 3) 运行 storyboard.py 装配 ──
    storyboard_py = os.path.join(STORY_DIR, "storyboard.py")
    if not os.path.exists(storyboard_py):
        fatal(f"找不到 storyboard.py: {storyboard_py}")

    print(f"  🔧 装配故事板...")
    result = subprocess.run(
        [sys.executable, storyboard_py, project_dir, "--data", data_path],
        capture_output=True, text=True, cwd=STORY_DIR,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        fatal("故事板装配失败")

    # ── 4) 补视频垫图 + 存入新版本文件 ──
    # 视频垫图只需故事板图，不要角色/产品资产图（故事板图已包含这些细节）
    refs_list = []
    _board_path = resolve_manifest_ref(f"storyboard_{group}", manifest, project_dir)
    if _board_path:
        refs_list.append(_board_path)
        print(f"  📌 故事板图: {os.path.basename(_board_path)}")
    else:
        print(f"  ⚠️ 故事板图未生成，视频无垫图")
    if board_cdn:
        refs_list.append(board_cdn)

    updated = {
        "name": video_draft.get("name", f"group{group}_video"),
        "prompt": video_draft["prompt"].rstrip(),
        "model": video_draft.get("model", "generate_video_seedance_v2_0"),
        "aspect_ratio": video_draft.get("aspect_ratio", "16:9"),
        "resolution": video_draft.get("resolution", "720p"),
        "duration": video_draft.get("duration", 15),
        "reference_image_paths": refs_list,
        "output_dir": video_draft.get("output_dir", os.path.join(project_dir, "videos", f"group{group}_video.mp4")),
    }

    # 覆写原文件（首次自动备份 .orig.json）
    out_path = backup_path(video_draft_path)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)

    print(f"  ✅ 视频提示词已填入垫图: {os.path.basename(out_path)}")
    print(f"     垫图: {len(refs_list)} 个{' (含 CDN URL)' if board_cdn else ''}")

    # ── 5) 建议命令 ──
    print(f"\n ═══ 后续命令 ═══\n")
    print(f"  生图:")
    print(f"    python3 {LOVART_DIR}/run_image_generator.py \\")
    print(f"      {project_dir}/configs/storyboard_{group}.json")
    print(f"\n  跑视频:")
    print(f"    python3 {LOVART_DIR}/run_video_generator.py \\")
    print(f"      {out_path} --project-dir {project_dir}")
    if not board_cdn:
        print(f"\n  💡 故事板图已记录到 cdn_urls.json, 后补垫图:")
        print(f"    python3 {sys.argv[0]} {project_dir} {group} --board-cdn <URL>")
        print(f"    🔗 查看: cat {os.path.join(project_dir, 'cdn_urls.json')}")
    print()


if __name__ == "__main__":
    main()
