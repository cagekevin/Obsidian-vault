"""
一键视频生成工具：读取 config，将比例/分辨率/时长拼入 prompt，send + 轮询。
用法: python run_video_generator.py <config.json路径>
"""
import json
import os
import sys
import time
import argparse

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)
from agent_skill import AgentSkill, LocalState, AgentSkillError
from lovart_project import resolve_id


def hsize(path):
    try:
        b = os.path.getsize(path)
        for u in ('B','KB','MB','GB'):
            if b < 1024: return f"{b:.0f}{u}"
            b /= 1024
    except:
        return "?"


def poll_until_done(skill, tid, timeout=1800, interval=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        status = skill.get_status(tid)
        st = status.get("status", "unknown")
        elapsed = int(time.time() - (deadline - timeout))
        dots = "." * ((elapsed // 10) % 5)
        print(f"    [{elapsed}s] {st}{dots}", flush=True)

        if st == "done":
            r = skill.get_result(tid)
            if r.get("pending_confirmation"):
                cost = r["pending_confirmation"].get("estimated_cost", "?")
                print(f"    ⏳ 扣费 {cost} 积分，自动确认中...", flush=True)
                skill.confirm(tid)
                time.sleep(3)
                continue
            r["final_status"] = "done"
            return r
        elif st == "abort":
            return {"thread_id": tid, "final_status": "abort"}
        time.sleep(interval)
    return {"thread_id": tid, "final_status": "timeout"}


def main():
    ak = os.environ.get("LOVART_ACCESS_KEY")
    sk = os.environ.get("LOVART_SECRET_KEY")
    if not ak or not sk:
        print(" ❌ 请设置环境变量 LOVART_ACCESS_KEY 和 LOVART_SECRET_KEY")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("config", nargs="?", default=None, help="config 路径")
    parser.add_argument("--ar", default=None, help="覆盖比例，如 --ar 9:16")
    parser.add_argument("--res", default=None, help="覆盖分辨率，如 --res 720p")
    parser.add_argument("--dur", "--duration", default=None, help="覆盖时长（秒），如 --dur 10 或 --duration 5")
    parser.add_argument("--model", default=None, help="覆盖视频模型全名")
    parser.add_argument("--project-dir", default=None, help="项目根目录（查找 .video_approved）")
    # 支持 -- 9:16 480p 5 快捷覆盖（位置参数: 比例 分辨率 时长）
    parser.add_argument("--project", default=None, help="项目名（从 projects.json 查 UUID）")
    parser.add_argument("overrides", nargs="*", help="快捷覆盖: 比例 分辨率 时长，如 -- 9:16 480p 5 或 -- 480p 5")
    args = parser.parse_args()

    config_path = args.config
    if not config_path:
        config_path = os.path.join(SKILL_DIR, "config_video.json")
    if not os.path.exists(config_path):
        print(f" ❌ 找不到配置文件: {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 解析快捷覆盖: -- 9:16 480p 5 或 -- 720p 6s 或 -- low（任意顺序）
    if args.overrides:
        import re
        for val in args.overrides:
            if val.startswith("generate_video") or val.startswith("generate_image"):
                args.model = val
            elif re.match(r'^\d+:\d+$', val) or re.match(r'^\d+x\d+$', val):
                args.ar = val
            elif re.match(r'^\d+[pPkK]$', val):
                args.res = val.upper()
            elif re.match(r'^\d+s?$', val):
                args.dur = val.rstrip('s')
            else:
                args.model = val

    # CLI 参数覆盖配置值
    overrides = []
    if args.ar:
        config["aspect_ratio"] = args.ar.replace("x", ":").replace("X", ":")
        overrides.append(f"ar{args.ar}".replace(":", "x"))
    if args.res:
        config["resolution"] = args.res
        overrides.append(f"{args.res}")
    if args.dur:
        config["duration"] = int(args.dur)
        overrides.append(f"{args.dur}s")
    if args.model:
        config["model"] = args.model
        tag = args.model.split("_")[-1] if "_" in args.model else args.model
        overrides.append(tag)
    # 修改 output_dir 防止覆盖原文件（仅单配置时）
    if overrides and isinstance(config, dict) and "prompts" not in config and "output_dir" in config:
        base, ext = os.path.splitext(config["output_dir"])
        tag = "_".join(overrides)
        config["output_dir"] = f"{base}_{tag}{ext}"

    skill = AgentSkill(
        base_url=os.environ.get("LOVART_BASE_URL", "https://lgw.lovart.ai"),
        access_key=ak,
        secret_key=sk,
    )
    state = LocalState()

    project_id = args.project if args.project else None
    if project_id:
        project_id = resolve_id(project_id)
    else:
        project_id = config.get("project_id") or state.get_project_id()
    if not project_id:
        project_id = skill.create_project()
        state.add_project(project_id, "HKH-Video")

    # ══ 熔断检查（注释：容器无shell时跳过，用户可自行 touch .video_approved） ══
    # project_dir = args.project_dir
    # if not project_dir:
    #     config_dir = os.path.dirname(os.path.abspath(config_path))
    #     project_dir = os.path.dirname(config_dir) if os.path.basename(config_dir) == 'configs' else config_dir
    # approved_file = os.path.join(project_dir, '.video_approved')
    # if not os.path.exists(approved_file):
    #     print()
    #     print(" ╔══════════════════════════════════════════════╗")
    #     print(" ║  🔒 强制熔断拦截                              ║")
    #     print(" ║  未检测到视频授权文件 .video_approved           ║")
    #     print(" ║  拒绝执行高耗时视频生成任务                    ║")
    #     print(" ║  (touch 项目/.video_approved 以解锁)            ║")
    #     print(" ╚══════════════════════════════════════════════╝")
    #     print()
    #     sys.exit(1)
    if args.project_dir:
        project_dir = args.project_dir
    else:
        cfg_dir = os.path.dirname(os.path.abspath(config_path))
        project_dir = os.path.dirname(cfg_dir) if os.path.basename(cfg_dir) == 'configs' else cfg_dir

    # ══ 通过 assets_manifest.json 解析垫图路径 ══
    manifest_path = os.path.join(project_dir, "assets_manifest.json")
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        manifest = {}

    def resolve_ref_path(path):
        """通过 manifest 将 default 路径解析为 latest 版本
           自动剥离文件名中的比例/分辨率后缀（_ar3x4_2K, _9x16 等）再查 manifest"""
        if not path:
            return path
        import re
        asset_name = os.path.splitext(os.path.basename(path))[0]
        # 尝试各种去后缀策略直到命中 manifest
        candidates = [asset_name]
        # 去掉 _ar3x4_2K、_9x16、_480p 等比例/分辨率后缀
        stripped = re.sub(r'_(ar\d+x\d+_\d+[kK]|ar\d+x\d+|\d+[pPkK])$', '', asset_name)
        if stripped != asset_name:
            candidates.append(stripped)
        # 去掉 _v数字 后缀（兼容旧文件）
        stripped2 = re.sub(r'_v\d+$', '', asset_name)
        if stripped2 != asset_name:
            candidates.append(stripped2)
        # 去掉比例后再去 v 后缀
        stripped3 = re.sub(r'_v\d+$', '', stripped) if stripped != asset_name else ""
        if stripped3 and stripped3 != stripped:
            candidates.append(stripped3)
        for name in candidates:
            entry = manifest.get(name, {})
            latest = entry.get("latest", "")
            if latest:
                resolved = os.path.join(project_dir, latest.replace('\\', '/'))
                if os.path.exists(resolved):
                    if name != asset_name:
                        print(f"  📌 {name}: {os.path.basename(path)} → {latest}")
                    return resolved.replace('\\', '/')
        return path

    items = config if isinstance(config, list) else [config]

    print()
    print(" ╭──────────────────────────────────────────────╮")
    print(" │       HKH · Lovart 视频生成工具              │")
    print(" ╰──────────────────────────────────────────────╯")
    print()
    print(f"  项目ID : {project_id}")
    print(f"  配置档 : {os.path.basename(config_path)}")
    print(f"  本次任务: {len(items)} 项")
    print()

    VIDEO_GUIDE = "Generate a single continuous video. Do NOT generate any images, static frames, multi-panel layouts, or storyboard grids. This must be ONE moving video with smooth transitions. (Exclusions): No text, No watermarks,  No camera shake, No flickering, No distortions. Characters, products, and scenes must match the reference images exactly. Sound effects only, no background music, ambient natural sound only. "
    VIDEO_GUIDE_TAG = "Generate a single continuous video."
    results = []
    for idx, item in enumerate(items, 1):
        name = item["name"]
        print(f" ── [{idx}/{len(items)}] {name}  ".ljust(50, "─"))

        # ── 参数拼入 prompt（API 不直接接受这些参数，通过描述控制）──
        prompt = item['prompt'].rstrip()
        if not prompt.startswith(VIDEO_GUIDE_TAG):
            prompt = VIDEO_GUIDE + prompt
        ar = item.get('aspect_ratio', '9:16')
        res = item.get('resolution', '480p')
        dur = item.get('duration', 15)
        prefix = f'{ar}, {res} resolution, {dur}-second video, using {item["model"]}. '
        if not prompt.startswith(prefix):
            prompt = prefix + prompt
        print(f"    比例   {ar}")
        print(f"    分辨率 {res}")
        print(f"    时长   {dur}s")

        prefer_models = {"VIDEO": [item["model"]]}

        # ── 垫图：解析 latest → 按附件编号上传 → 生成说明 ──
        attachments = []
        raw_refs = item.get("reference_image_paths")
        if raw_refs is None:
            raw_refs = [item["reference_path"]] if item.get("reference_path") else []
        # 先全部解析（resolve_ref_path 可能改变文件名如 v4），用解析后的路径做后续所有事
        resolved_refs = []
        for rp in raw_refs:
            resolved_refs.append(resolve_ref_path(rp))
        ref_guide_parts = []
        for i, rp in enumerate(resolved_refs, 1):
            if not rp:
                continue
            if rp.startswith("http://") or rp.startswith("https://"):
                print(f"    Attachment #{i} (CDN) {rp}")
                attachments.append(rp)
                fn_short = rp.split("/")[-1]
            elif os.path.exists(rp):
                fn_short = os.path.basename(rp)
                print(f"    Attachment #{i} + {rp} ({hsize(rp)})")
                cdn_url = skill.upload_file(rp)
                attachments.append(cdn_url)
            else:
                print(f"    ❌ Attachment #{i} 垫图文件不存在: {rp}")
                continue
            # 根据文件名判断用途
            fn_lower = fn_short.lower()
            if 'storyboard' in fn_lower:
                desc = "Scene composition guide — use this storyboard for overall timing, camera movement, and frame transitions"
            elif 'hkh_capsule' in fn_lower or 'capsule' in fn_lower:
                desc = "PRODUCT reference — copy the exact shape, color, and golden translucent appearance of this HKH capsule. DO NOT invent the product design"
            elif 'char_' in fn_lower or 'female' in fn_lower or 'doctor' in fn_lower:
                desc = "Character appearance reference — match the face, hair, body, and outfit"
            else:
                continue
            ref_guide_parts.append(f"Attachment #{i} ({fn_short}): {desc}")
        if ref_guide_parts:
            guide = "REFERENCE IMAGES GUIDE: " + " | ".join(ref_guide_parts) + ". "
            if guide not in prompt:
                prompt = guide + prompt
            for line in ref_guide_parts:
                print(f"    📌 {line}")

        print(f"    模型   {item['model']}")
        if attachments:
            print(f"    垫图   {len(attachments)} 张")
        print()

        try:
            tid = skill.send(
                prompt=prompt,
                project_id=project_id,
                attachments=attachments if attachments else None,
                prefer_models=prefer_models,
                include_tools=[item["model"]],
                mode="fast",
            )
            print(f"    thread: {tid}")
            state.upsert_thread(tid, f"video-{name}")

            result = poll_until_done(skill, tid)

            if result.get("final_status") == "timeout":
                print(f"    ⏳ 超时，请稍后手动拉取: python agent_skill.py result --thread-id {tid} --json --download")
                results.append({"name": name, "status": "timeout"})
                continue
            elif result.get("final_status") == "abort":
                print(f"    ❌ 已中止")
                results.append({"name": name, "status": "abort"})
                continue

            if result.get("generation_succeeded", True) is False:
                print(f"    ⚠️ 失败: {result.get('warning')}")
                results.append({"name": name, "status": "failed"})
                continue

            if result.get("agent_message"):
                print(f"    📝 {result.get('agent_message')[:150]}")

            output_path = item.get("output_dir", "")
            out_dir = os.path.dirname(output_path) if output_path else SKILL_DIR
            downloaded = skill.download_artifacts(result, output_dir=out_dir)

            if downloaded:
                dl = downloaded[0]
                dl_path = dl.get("local_path", "")
                if output_path and dl_path and os.path.exists(dl_path):
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    base, ext = os.path.splitext(output_path)
                    v = 1
                    while os.path.exists(f"{base}_v{v}{ext}"):
                        v += 1
                    target = f"{base}_v{v}{ext}"
                    os.rename(dl_path, target)
                    print(f"    ✅ 下载完成 → {target} ({hsize(target)})")
                    # 自动更新 assets_manifest.json 的 latest
                    asset_name = item.get("name", "")
                    if manifest and asset_name:
                        rel = os.path.relpath(target, project_dir).replace('\\', '/')
                        if asset_name in manifest:
                            old = manifest[asset_name].get("latest", "")
                            manifest[asset_name]["latest"] = rel
                            print(f"    📌 manifest: {asset_name}.latest → {rel}" + (f" (之前: {old})" if old else ""))
                        else:
                            manifest[asset_name] = {"config": "", "default": rel, "latest": rel}
                            print(f"    📌 manifest: 新增 {asset_name} → {rel}")
                        with open(manifest_path, "w", encoding="utf-8") as f:
                            json.dump(manifest, f, indent=2, ensure_ascii=False)
                else:
                    print(f"    ✅ 下载完成 → {dl_path}")
                results.append({"name": name, "status": "done"})
            else:
                print(f"    ⚠️ 无视频产出")
                results.append({"name": name, "status": "no_artifact"})

        except AgentSkillError as e:
            print(f"    ❌ API错误: {e.message}")
            results.append({"name": name, "status": "error"})
        except Exception as e:
            print(f"    ❌ {e}")
            results.append({"name": name, "status": "error"})

        time.sleep(1)

    ok = sum(1 for r in results if r["status"] == "done")
    fail = len(results) - ok
    print(f"\n ── 汇总  ".ljust(50, "─"))
    for r in results:
        icon = "✅" if r["status"] == "done" else "❌"
        print(f"  {icon} {r['name']}  {r['status']}")
    print(f"\n  ✅ {ok}/{len(results)} 完成" + (f"  ❌ {fail} 失败" if fail else ""))
    print(f"  🔗 https://www.lovart.ai/canvas?projectId={project_id}")
    print()


if __name__ == "__main__":
    main()
