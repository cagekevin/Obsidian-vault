#!/usr/bin/env python3
"""
Lovart 项目图片批量同步 — 按项目拉取所有线程图片，按 topic 命名下载。

用法:
  # 通过 --project 指定项目名（从 projects.json 查 UUID）
  python sync_lovart_images.py --project "婷美面霜" --output-dir /项目/output

  # 通过 --config 读取 JSON 中的 project_id（更推荐，不会跑错项目）
  python sync_lovart_images.py --config /项目/prompts/group1_video.json --output-dir /项目/images

功能:
  - 从 projects.json 查 UUID，拉取该项目所有线程
  - 按 topic 命名文件（如 collagen_detail.png）
  - 自动确认 pending_confirmation（--confirm）
  - 记录 CDN URL 到 output-dir 同级的 cdn_urls.json
  - 幂等：已有文件跳过不重复下载
"""
import argparse, json, os, re, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lovart_project import resolve_id, load_projects

AGENT = os.path.join(os.path.dirname(__file__), "agent_skill.py")


def agent(*args, timeout=120):
    r = subprocess.run(
        [sys.executable, AGENT] + list(args),
        capture_output=True, text=True, timeout=timeout
    )
    if r.returncode != 0:
        print(f"  ❌ agent_skill: {r.stderr[:200]}", file=sys.stderr)
        return None
    return r.stdout.strip()


def topic_name(topic: str) -> str:
    """从 topic 提取文件名，去掉 asset- 前缀，空格变下划线"""
    if not topic:
        return None
    name = topic.replace("asset-", "").replace(" ", "_")[:40]
    return name if name else None


def confirm_thread(project_id: str, thread_id: str):
    sys.path.insert(0, os.path.dirname(AGENT))
    import agent_skill as m
    skill = m.AgentSkill(
        base_url=os.environ.get("LOVART_BASE_URL", "https://lgw.lovart.ai"),
        access_key=os.environ.get("LOVART_ACCESS_KEY", ""),
        secret_key=os.environ.get("LOVART_SECRET_KEY", "")
    )
    try:
        r = skill.confirm(thread_id)
        return r.get("status") in ("ok", "done", "processing")
    except Exception as e:
        print(f"  ⚠️ confirm 失败: {e}")
        return False


def poll_until_done(thread_id: str, timeout: int = 60):
    deadline = time.time() + timeout
    while time.time() < deadline:
        raw = agent("status", "--thread-id", thread_id)
        if not raw:
            continue
        try:
            st = json.loads(raw).get("status", "")
        except json.JSONDecodeError:
            st = ""
        if st == "done":
            return True
        if st in ("abort", "error", "failed"):
            return False
        time.sleep(5)
    return False


def load_cdn_db(output_dir: str) -> dict:
    path = os.path.join(os.path.dirname(output_dir), "cdn_urls.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def save_cdn_db(output_dir: str, cdn: dict):
    path = os.path.join(os.path.dirname(output_dir), "cdn_urls.json")
    with open(path, "w") as f:
        json.dump(cdn, f, indent=2, ensure_ascii=False)


def download_thread(thread_id: str, name: str, output_dir: str, cdn_db: dict):
    target = os.path.join(output_dir, f"{name}.png")
    if os.path.exists(target):
        # 幂等：同名 topic 已有文件则跳过（同一线程重跑不重复下载）
        print(f"  ✅ {name}.png 已存在，跳过")
        return True

    raw = agent("result", "--thread-id", thread_id, "--download", "--output-dir", output_dir)
    if not raw:
        return False
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print(f"  ❌ {name} JSON 解析失败")
        return False

    dl = data.get("downloaded", [])
    if not dl:
        print(f"  ⚠️ {name} 无产物")
        return False

    src = dl[0].get("local_path", "")
    url = dl[0].get("url", "")
    if not src or not os.path.exists(src):
        print(f"  ❌ {name} 文件不存在: {src}")
        return False

    os.rename(src, target)
    size_mb = os.path.getsize(target) / 1024 / 1024

    cdn_db[name] = {
        "default": f"images/{name}.png",
        "cdn_url": url,
        "version": 1
    }
    print(f"  ✅ {name}.png ({size_mb:.1f}MB)")
    return True


def main():
    p = argparse.ArgumentParser(description="Lovart 项目图片批量同步")
    p.add_argument("--project", default=None, help="项目名（projects.json 中的 key）")
    p.add_argument("--config", default=None, help="从 JSON 文件读取 project_id（与 --project 二选一）")
    p.add_argument("--output-dir", required=True, help="本地图片输出目录")
    p.add_argument("--confirm", action="store_true", help="自动确认 pending 线程")
    p.add_argument("--poll", action="store_true", help="等待 running 线程完成")
    p.add_argument("--dry-run", action="store_true", help="只列出，不下载")
    args = p.parse_args()

    # 确定 project_id
    project_id = None
    project_name = args.project
    if args.config:
        with open(args.config, encoding="utf-8") as f:
            cfg = json.load(f)
        pid = cfg.get("project_id")
        if pid:
            project_id = pid
            # 反向查项目名（仅用于展示）
            projects = load_projects()
            for name, uuid in projects.items():
                if uuid == pid:
                    project_name = name
                    break
    if not project_id and args.project:
        project_id = resolve_id(args.project)
    if not project_id:
        print("❌ 请提供 --project 或 --config")
        sys.exit(1)

    print(f"📦 项目: {project_name or project_id[:12]}... ({project_id})")

    raw = agent("threads", "--project-id", project_id, "--json")
    if not raw:
        print("❌ 无法获取线程列表")
        sys.exit(1)

    threads = json.loads(raw)
    if not threads:
        print("该项目下无线程")
        return

    cdn_db = load_cdn_db(args.output_dir)
    stats = {"downloaded": 0, "skipped": 0, "pending": 0, "failed": 0}

    for t in threads:
        tid = t["id"]
        name = topic_name(t.get("topic", ""))
        if not name:
            continue

        target = os.path.join(args.output_dir, f"{name}.png")
        if os.path.exists(target):
            stats["skipped"] += 1
            continue

        raw_st = agent("status", "--thread-id", tid)
        if not raw_st:
            stats["failed"] += 1
            continue
        try:
            status = json.loads(raw_st).get("status", "")
        except json.JSONDecodeError:
            stats["failed"] += 1
            continue

        has_pending = "pending_confirmation" in raw_st

        if status == "done" and not has_pending:
            if args.dry_run:
                print(f"  📋 {name} 待下载")
                stats["pending"] += 1
            elif download_thread(tid, name, args.output_dir, cdn_db):
                stats["downloaded"] += 1
            else:
                stats["failed"] += 1

        elif has_pending and args.confirm:
            print(f"  🔑 {name} 待确认扣费")
            if args.dry_run:
                stats["pending"] += 1
                continue
            if confirm_thread(project_id, tid):
                print(f"  ⏳ {name} 已确认，等待完成...")
                if poll_until_done(tid):
                    if download_thread(tid, name, args.output_dir, cdn_db):
                        stats["downloaded"] += 1
                    else:
                        stats["failed"] += 1
                else:
                    stats["pending"] += 1
            else:
                stats["failed"] += 1

        elif status in ("running", "processing") and args.poll:
            print(f"  ⏳ {name} 正在生成，等待...")
            if args.dry_run:
                stats["pending"] += 1
            elif poll_until_done(tid):
                if download_thread(tid, name, args.output_dir, cdn_db):
                    stats["downloaded"] += 1
                else:
                    stats["failed"] += 1
            else:
                stats["pending"] += 1

        else:
            label = f"状态={status}" + (" (--confirm 确认扣费)" if has_pending else "")
            print(f"  ⏳ {name} {label}")
            stats["pending"] += 1

    save_cdn_db(args.output_dir, cdn_db)
    cdn_path = os.path.join(os.path.dirname(args.output_dir), "cdn_urls.json")
    print(f"\n📦 CDN: {cdn_path}")
    print(f"{'='*40}")
    print(f"✅ 已下载: {stats['downloaded']}  ➡️ 已跳过: {stats['skipped']}")
    print(f"⏳ 待处理: {stats['pending']}  ❌ 失败: {stats['failed']}")


if __name__ == "__main__":
    main()
