"""
一键生图工具：读取 config.json，批量提交并下载图片。
用法: python run_image_generator.py <config.json路径>
特点：
  - 纯净执行器，不做任何 prompt 二次拼装
  - 非阻塞 send + 每10秒轮询状态
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
    except: return "?"


def poll_until_done(skill, tid, timeout=600, interval=10):
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

    MODEL_ALIASES = {
        "medium": "generate_image_gpt_image_2_medium",
        "low": "generate_image_gpt_image_2_low",
        "high": "generate_image_gpt_image_2_high",
        "gpt2":  "generate_image_gpt_image_2",
        "gpt15": "generate_image_gpt_image_1_5",
        "nb2":   "generate_image_nano_banana_2",
        "nb":    "generate_image_nano_banana",
        "nbp":   "generate_image_nano_banana_pro",
        "mj":    "generate_image_midjourney",
        "sd4":   "generate_image_seedream_v4",
        "sd45":  "generate_image_seedream_v4_5",
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("config", nargs="?", default=None, help="config.json 路径")
    parser.add_argument("--ar", default=None, help="覆盖比例，如 --ar 3:4")
    parser.add_argument("--res", default=None, help="覆盖分辨率，如 --res 2K")
    parser.add_argument("--model", default=None, help="覆盖模型: low / medium / high 或全名")
    # 支持 -- 3:4 2K 快捷覆盖（位置参数: 比例 分辨率 模型）
    parser.add_argument("--project", default=None, help="项目名（从 projects.json 查 UUID）")
    parser.add_argument("overrides", nargs="*", help="快捷覆盖: 比例 分辨率 模型，如 -- 3:4 2K low")
    args = parser.parse_args()

    config_path = args.config
    if not config_path:
        config_path = os.path.join(SKILL_DIR, "config.json")
    if not os.path.exists(config_path):
        print(f" ❌ 找不到配置文件: {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8-sig") as f:
        config = json.load(f)

    # 确定项目根目录
    _project_dir = os.path.dirname(os.path.abspath(config_path))
    if os.path.basename(_project_dir) == "configs":
        _project_dir = os.path.dirname(_project_dir)
    _manifest_path = os.path.join(_project_dir, "assets_manifest.json")
    try:
        with open(_manifest_path, "r", encoding="utf-8") as f:
            _manifest = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        _manifest = {}

    # 解析快捷覆盖: -- 3:4 2K low 或 -- low 或 -- 3:4 low（任意顺序）
    if args.overrides:
        import re
        for val in args.overrides:
            if val in MODEL_ALIASES or val.startswith("generate_image"):
                args.model = val
            elif re.match(r'^\d+[kK]$', val):
                args.res = val.upper()
            elif re.match(r'^\d+:\d+$', val) or re.match(r'^\d+x\d+$', val):
                args.ar = val

    # CLI 参数覆盖配置值
    overrides = []
    if args.ar:
        config["aspect_ratio"] = args.ar.replace("x", ":").replace("X", ":")
        overrides.append(f"ar{args.ar}".replace(":", "x"))
    if args.res:
        config["resolution"] = args.res
        overrides.append(f"{args.res}")
    if args.model:
        raw = args.model
        config["model"] = MODEL_ALIASES.get(raw, raw)
        tag = MODEL_ALIASES.get(raw, raw).split("_")[-1] if "_" in raw else raw
        overrides.append(tag)
    # 修改 output_dir 防止覆盖原文件
    if overrides and "output_dir" in config and isinstance(config, dict) and "prompts" not in config:
        base, ext = os.path.splitext(config["output_dir"])
        tag = "_".join(overrides)
        config["output_dir"] = f"{base}_{tag}{ext}"

    skill = AgentSkill(
        base_url=os.environ.get("LOVART_BASE_URL", "https://lgw.lovart.ai"),
        access_key=ak,
        secret_key=sk,
        timeout=600,
    )
    state = LocalState()

    project_id = args.project if args.project else None
    if project_id:
        project_id = resolve_id(project_id)
    else:
        project_id = config.get("project_id") or state.get_project_id()
    if not project_id:
        project_id = skill.create_project()
        state.add_project(project_id, "AI_Project")

    if "prompts" in config:
        items = config["prompts"]
    else:
        items = [config]

    print()
    print(" ╭──────────────────────────────────────────────╮")
    print(" │       HKH · Lovart 生图工具                   │")
    print(" ╰──────────────────────────────────────────────╯")
    print()
    print(f"  项目ID : {project_id}")
    print(f"  配置档 : {os.path.basename(os.path.dirname(config_path))}/{os.path.basename(config_path)}")
    print(f"  本次任务: {len(items)} 项")
    print()

    # manifest 解析函数 — 自动升级到 latest 版本（复用项目已加载的 _manifest）
    import re as _re
    def _resolve_ref_path(path):
        if not path:
            return path
        asset_name = os.path.splitext(os.path.basename(path))[0]
        candidates = [asset_name]
        # 去掉比例后缀 _ar3x4_2K、_9x16、_480p 等
        s = _re.sub(r'_(ar\d+x\d+_\d+[kK]|ar\d+x\d+|\d+[pPkK])$', '', asset_name)
        if s != asset_name:
            candidates.append(s)
        s2 = _re.sub(r'_v\d+$', '', asset_name)
        if s2 != asset_name:
            candidates.append(s2)
        s3 = _re.sub(r'_v\d+$', '', s) if s != asset_name else ""
        if s3 and s3 != s:
            candidates.append(s3)
        for name in candidates:
            entry = _manifest.get(name, {})
            latest = entry.get("latest", "")
            if latest:
                resolved = os.path.join(_project_dir, latest.replace('\\', '/'))
                if os.path.exists(resolved):
                    if name != asset_name:
                        print(f"    📌 {name}: {os.path.basename(path)} → {latest}")
                    return resolved.replace('\\', '/')
        return path

    results = []
    _output_paths = []
    for idx, item in enumerate(items, 1):
        name = item["name"]
        print(f" ── [{idx}/{len(items)}] {name}  ".ljust(50, "─"))

        # 垫图 — 通过 manifest 解析 latest + 文件不存在则打印警告
        attachments = []
        raw_refs = item.get("reference_image_paths")
        if raw_refs is None:
            raw_refs = [item["reference_image_path"]] if item.get("reference_image_path") else []
        ref_ok = 0
        ref_fail = 0
        for rp in raw_refs:
            if rp.startswith("http://") or rp.startswith("https://"):
                print(f"    垫图 (CDN) {rp}")
                attachments.append(rp)
                ref_ok += 1
                continue
            rp = _resolve_ref_path(rp)
            if os.path.exists(rp):
                print(f"    垫图 + {rp} ({hsize(rp)})")
                cdn_url = skill.upload_file(rp)
                print(f"      ↳ {cdn_url}")
                attachments.append(cdn_url)
                ref_ok += 1
            else:
                print(f"    ❌ 垫图文件不存在: {rp}")
                ref_fail += 1
        if ref_fail > 0:
            print(f"    ⚠️ {ref_fail} 张垫图缺失，仅 {ref_ok} 张生效")
        print(f"    模型   {item['model']}")
        ar = item.get('aspect_ratio', '1:1')
        res = item.get('resolution', '1K')
        print(f"    比例   {ar} / {res}")

        prompt = item['prompt'].rstrip()

        # ── 垫图说明：自动拼入 prompt 开头（参考 run_video_generator.py）──
        ref_guide_parts = []
        for i, rp in enumerate(item.get("reference_image_paths", []), 1):
            fn_short = os.path.basename(rp)
            fn_lower = fn_short.lower()
            if 'char_' in fn_lower or 'female' in fn_lower or 'doctor' in fn_lower:
                desc = "Character appearance reference — match the face, hair, body, and outfit"
            elif 'product' in fn_lower or 'bottle' in fn_lower or 'capsule' in fn_lower:
                desc = "PRODUCT reference — copy the exact shape, color, and packaging design. DO NOT invent the product appearance"
            elif 'scene' in fn_lower:
                desc = "Scene environment reference — match the lighting, space layout, and color palette"
            elif 'storyboard' in fn_lower:
                desc = "Scene composition guide — use this storyboard for layout and framing"
            else:
                continue
            ref_guide_parts.append(f"Attachment #{i} ({fn_short}): {desc}")
        if ref_guide_parts:
            guide = "REFERENCE IMAGES GUIDE: " + " | ".join(ref_guide_parts) + ". "
            if guide not in prompt:
                prompt = guide + prompt
            for line in ref_guide_parts:
                print(f"    📌 {line}")

        # 拼接关键参数到 prompt 开头（Agent 优先读前面内容）
        prefix = f'{ar}, {res} resolution, using {item["model"]}. '
        if not prompt.startswith(prefix):
            prompt = prefix + prompt

        if attachments:
            print(f"    垫图   {len(attachments)} 张")
        print()

        # 【纯净执行器】prompt 原封不动传给 API，不含任何二次拼装（仅追加比例/分辨率参数）
        try:
            tid = skill.send(
                prompt=prompt,
                project_id=project_id,
                attachments=attachments if attachments else None,
                prefer_models={"IMAGE": [item["model"]]},
            )
            print(f"    thread: {tid}")
            state.upsert_thread(tid, f"asset-{name}")

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

            asset_name = item.get("name", "")
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
                    _output_paths.append(f"    ✅ 下载完成 → {target} ({hsize(target)})")
                    # 自动更新 assets_manifest.json 的 latest
                    if _manifest and _manifest_path and asset_name:
                        rel = os.path.relpath(target, _project_dir).replace('\\', '/')
                        if asset_name in _manifest:
                            old = _manifest[asset_name].get("latest", "")
                            _manifest[asset_name]["latest"] = rel
                            print(f"    📌 manifest: {asset_name}.latest → {rel}" + (f" (之前: {old})" if old else ""))
                        else:
                            _manifest[asset_name] = {"config": "", "default": rel, "latest": rel}
                            print(f"    📌 manifest: 新增 {asset_name} → {rel}")
                        with open(_manifest_path, "w", encoding="utf-8") as f:
                            json.dump(_manifest, f, indent=2, ensure_ascii=False)
                    # 自动记录 CDN URL 到 cdn_urls.json
                    cdn_url = dl.get("url", "")
                    if cdn_url and asset_name:
                        _cdn_path = os.path.join(_project_dir, "cdn_urls.json")
                        _cdn_data = {}
                        if os.path.exists(_cdn_path):
                            with open(_cdn_path, "r", encoding="utf-8") as f:
                                _cdn_data = json.load(f)
                        if _cdn_data.get(asset_name) != cdn_url:
                            _cdn_data[asset_name] = cdn_url
                            with open(_cdn_path, "w", encoding="utf-8") as f:
                                json.dump(_cdn_data, f, indent=2, ensure_ascii=False)
                            print(f"    📌 CDN: {asset_name} → saved")
                else:
                    _output_paths.append(f"    ✅ 下载完成 → {dl_path}")
                results.append({"name": name, "status": "done"})
            else:
                print(f"    ⚠️ 生成无产出")
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

    if _output_paths:
        print()
        for line in _output_paths:
            print(line)

    print()


if __name__ == "__main__":
    main()
