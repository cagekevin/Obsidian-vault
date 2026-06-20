#!/usr/bin/env python3
"""
Lovart 项目管理 — 项目名↔UUID 映射，供 W7 内部使用。

用法:
  python lovart_project.py init "项目名"               # 新建 Lovart 项目
  python lovart_project.py init "项目名" --output H:/路径  # 新建+创建本地目录
  python lovart_project.py list                         # 列出所有项目
  python lovart_project.py id "项目名"                   # 查 UUID
  python lovart_project.py path "项目名"                 # 查本地路径
  python lovart_project.py info "项目名"                 # 查项目完整信息
  python lovart_project.py switch "项目名"              # 切换 active project
projects.json 位置：本脚本同目录。
"""
import json, os, sys, subprocess, uuid as _uuid

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECTS_JSON = os.path.join(_SCRIPT_DIR, "projects.json")
_AGENT = os.path.join(_SCRIPT_DIR, "agent_skill.py")


def load_projects() -> dict:
    if not os.path.exists(_PROJECTS_JSON):
        return {}
    with open(_PROJECTS_JSON, encoding="utf-8") as f:
        return json.load(f)


def save_projects(data: dict):
    with open(_PROJECTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _get_info(project_name: str) -> dict:
    """取项目信息，兼容旧格式（UUID 字符串）和新格式（{uuid, path}）。"""
    projects = load_projects()
    raw = projects.get(project_name)
    if not raw:
        return None
    if isinstance(raw, str):
        return {"uuid": raw, "path": ""}
    return {"uuid": raw.get("uuid", ""), "path": raw.get("path", "")}


def resolve_id(project_name: str) -> str:
    info = _get_info(project_name)
    if not info or not info["uuid"] or info["uuid"].startswith("aaaa"):
        print(f"❌ 未找到项目 '{project_name}'，请先: python lovart_project.py init \"{project_name}\"")
        sys.exit(1)
    return info["uuid"]


def run_agent(*args):
    r = subprocess.run(
        [sys.executable, _AGENT] + list(args),
        capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print(f"❌ agent_skill 出错: {r.stderr[:200]}")
        sys.exit(1)
    return r.stdout.strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python lovart_project.py <init|list|id|switch> [项目名]")
        sys.exit(1)

    cmd = sys.argv[1]
    projects = load_projects()

    if cmd == "init":
        if len(sys.argv) < 3:
            print("用法: python lovart_project.py init \"项目名\" [--output H:/路径]")
            sys.exit(1)
        name = sys.argv[2]
        output_dir = None
        if "--output" in sys.argv:
            idx = sys.argv.index("--output")
            if idx + 1 < len(sys.argv):
                output_dir = sys.argv[idx + 1]

        if name in projects and not projects[name].startswith("aaaa"):
            print(f"⚠️ 项目 '{name}' 已存在: {projects[name]}")
        else:
            # 先让云端创建项目，获取真实 UUID
            import json as _json
            try:
                out = run_agent("create-project")
                new_id = _json.loads(out)["project_id"]
            except Exception as e:
                print(f"❌ 云端项目创建失败: {e}")
                sys.exit(1)
            # 改名为用户指定的项目名
            run_agent("project-rename", "--project-id", new_id, "--name", name)
            projects[name] = new_id
            # 如果有路径，升级为对象格式
            if output_dir:
                project_dir = os.path.join(output_dir, name)
                projects[name] = {"uuid": new_id, "path": project_dir}
            save_projects(projects)
            print(f"✅ Lovart 项目已创建: {new_id}")
            print(f"   画布: https://www.lovart.ai/canvas?projectId={new_id}")
            print(f"   active project 已自动切换到: {name}")

        if output_dir:
            project_dir = os.path.join(output_dir, name)
            for sub in ["products", "references", "briefs", "assets"]:
                os.makedirs(os.path.join(project_dir, "input", sub), exist_ok=True)
            os.makedirs(os.path.join(project_dir, "output"), exist_ok=True)
            # 复制管线编排工具到 input/
            import shutil
            marker_src = os.path.join(_SCRIPT_DIR, "../workflow/pipeline-marker.html")
            marker_dst = os.path.join(project_dir, "input", "pipeline-marker.html")
            if os.path.exists(marker_src) and not os.path.exists(marker_dst):
                shutil.copy2(marker_src, marker_dst)
            print(f"📁 本地目录: {project_dir}/")
            print(f"   ├─ input/")
            print(f"   │   ├─ products/   ← 产品实拍图")
            print(f"   │   ├─ references/ ← 竞品参考图/风格参考")
            print(f"   │   ├─ briefs/     ← 需求(从看板导出的JSON)")
            print(f"   │   ├─ assets/     ← 其他素材(logo/背景等)")
            print(f"   │   └─ pipeline-marker.html ← 管线编排工具(双击打开)")
            print(f"   └─ output/         ← 管线产出(.md + 图片)")

    elif cmd == "list":
        if not projects:
            print("暂无项目")
        else:
            active_pid = ""
            state_threads = {}
            try:
                state = json.loads(run_agent("config", "--json"))
                active_pid = state.get("active_project", "")
                for t in state.get("threads", []):
                    pid = t.get("project_id", "")
                    state_threads[pid] = state_threads.get(pid, 0) + 1
            except Exception:
                pass
            for name, raw in projects.items():
                if name.startswith("_"):
                    continue
                info = _get_info(name)
                pid = info["uuid"] if info else ""
                path = info["path"] if info else ""
                marker = " (占位)" if pid.startswith("aaaa") else ""
                active = " *" if pid == active_pid else "  "
                threads = state_threads.get(pid, 0)
                path_info = f"  📁 {path}" if path else ""
                thr_info = f"  🧵 {threads}" if threads else ""
                print(f"{active} {name:20s} → {pid[:12]}...{marker}{path_info}{thr_info}")

    elif cmd == "id":
        if len(sys.argv) < 3:
            print("用法: python lovart_project.py id \"项目名\"")
            sys.exit(1)
        print(resolve_id(sys.argv[2]))

    elif cmd == "path":
        if len(sys.argv) < 3:
            print("用法: python lovart_project.py path \"项目名\"")
            sys.exit(1)
        info = _get_info(sys.argv[2])
        if not info:
            print(f"❌ 未找到项目 '{sys.argv[2]}'")
            sys.exit(1)
        if not info["path"]:
            print(f"⚠️ 项目 '{sys.argv[2]}' 未记录本地路径 (init 时未传 --output)")
            sys.exit(1)
        print(info["path"])

    elif cmd == "info":
        if len(sys.argv) < 3:
            print("用法: python lovart_project.py info \"项目名\"")
            sys.exit(1)
        info = _get_info(sys.argv[2])
        if not info:
            print(f"❌ 未找到项目 '{sys.argv[2]}'")
            sys.exit(1)
        # 从官方 state.json 读取名称和线程数
        active = ""
        threads = 0
        try:
            state = json.loads(run_agent("config", "--json"))
            for pid, pdata in state.get("projects", {}).items():
                if pid == info["uuid"]:
                    active = " (活跃)" if state.get("active_project") == pid else ""
                    threads = sum(1 for t in state.get("threads", []) if t.get("project_id") == pid)
                    break
        except Exception:
            pass
        print(f"  UUID: {info['uuid']}{active}")
        print(f"  画布: https://www.lovart.ai/canvas?projectId={info['uuid']}")
        if info["path"]:
            print(f"  路径: {info['path']}")
            print(f"  产品图: {info['path']}\\input\\products")
            print(f"  产出: {info['path']}\\output")
        else:
            print("  路径: 未记录")
        if threads:
            print(f"  线程: {threads} 条")

    elif cmd == "switch":
        if len(sys.argv) < 3:
            print("用法: python lovart_project.py switch \"项目名\"")
            sys.exit(1)
        name = sys.argv[2]
        pid = resolve_id(name)
        run_agent("project-switch", "--project-id", pid)
        print(f"🔄 active project 已切换到: {name} ({pid[:12]}...)")

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
