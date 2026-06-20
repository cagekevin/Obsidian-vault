#!/usr/bin/env python3
"""
Studio CLI — 影视全流程一键执行器
位置: screenplay-to-video/studio.py

用法:
  studio.py                       交互菜单（先选项目）
  studio.py <项目名>              交互菜单（锁定项目）
  studio.py <项目名> <命令号> <组>  跳过菜单直接执行

命令号:
  1=视频  2=故事板大图  3=逐镜图  4=定妆照/产品
  5=一键装配(board_to_video)  6=单步拼装(storyboard)
  7=切换模式  8=切换项目
"""
import os, sys, glob, json, subprocess, time
import platform
from manifest_resolver import load_manifest, resolve as resolve_single

# ── 路径 ──
if platform.system() == "Darwin":
    BASE = "/Users/kevin/Documents/AgentSpace/1_Active"
else:
    BASE = "G:/AgentSpace/1_Active"
BASE = os.environ.get("AGENT_SPACE", BASE)
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LOVART = os.path.join(os.path.dirname(os.path.dirname(SKILL_DIR)), "../W7-API链接/lovart-skill")
LOVART = os.path.normpath(LOVART)
STATE_FILE = os.path.join(SKILL_DIR, ".studio_state.json")

W = 55  # 菜单宽度
YES = False  # --yes 时跳过所有确认和按回车

# ── 帮助函数 ──

def load_state():
    try:
        with open(STATE_FILE) as f: return json.load(f)
    except: return {"project": "", "mode": "fast"}

def save_state(s):
    with open(STATE_FILE, "w") as f: json.dump(s, f, indent=2)

def list_projects():
    dirs = sorted(glob.glob(os.path.join(BASE, "*")))
    return [os.path.basename(d) for d in dirs if os.path.isdir(d)]

def project_path(name): return os.path.join(BASE, name)

def query_mode():
    """返回 (unlimited, ul_enable, days_str)"""
    try:
        r = json.loads(subprocess.check_output(
            [sys.executable, os.path.join(LOVART, "agent_skill.py"), "query-mode"],
            cwd=LOVART, timeout=15))
        d = r.get("detail", {})
        ul = d.get("unlimited", False)
        enable = d.get("unlimited_enable", False)
        lst = d.get("unlimited_list", [])
        days = lst[0].get("remaining_days", "") if lst else ""
        return (ul, enable, str(days))
    except: return (False, False, "?")

def set_mode(unlimited: bool):
    subprocess.run([sys.executable, os.path.join(LOVART, "agent_skill.py"),
                    "set-mode", "--unlimited" if unlimited else "--fast"],
                   cwd=LOVART, timeout=15)

def load_json(path):
    try:
        with open(path, encoding="utf-8") as f: return json.load(f)
    except: return None



def preview(prj, config_path, desc):
    """预览 config 内容，返回是否确认执行"""
    global YES
    if YES:
        return True
    cfg = load_json(config_path)
    if not cfg:
        print(f"\n  ❌ 无法读取配置文件: {config_path}")
        return False

    print(f"\n  {'='*50}")
    print(f"  {desc}")
    print(f"  {'='*50}")
    print(f"  配置: {config_path}")

    # 基本信息
    for k in ("name", "model", "aspect_ratio", "resolution", "duration"):
        v = cfg.get(k)
        if v: print(f"  {k}: {v}")

    # 垫图
    refs = cfg.get("reference_image_paths") or ( [cfg["reference_path"]] if cfg.get("reference_path") else [])
    if refs:
        print(f"\n  ── 垫图 ──")
        prj_path = project_path(prj)
        _manifest = load_manifest(prj_path)
        for orig in refs:
            resolved = resolve_single(orig, _manifest, prj_path)
            if resolved:
                rbase, obase = os.path.basename(resolved), os.path.basename(orig)
                if rbase != obase:
                    print(f"  ✅ {obase} → {rbase}")
                else:
                    print(f"  ✅ {rbase}")
            else:
                print(f"  ❌ {orig}  文件不存在")

    # prompt 摘要
    prompt = cfg.get("prompt", "")
    if prompt:
        short = prompt[:200].replace('\n', ' ')
        print(f"\n  ── 提示词（摘要）──")
        print(f"  {short}...")
        if len(prompt) > 200:
            print(f"  ...省略 {len(prompt)-200} 字符")

    print(f"\n  {'='*50}")
    confirm = input("  确认执行？[y/N]: ").strip().lower()
    return confirm == "y"

def run_script(script, args, prj, desc):
    global YES
    p = project_path(prj)
    # 找 config 路径：args 里第一个是 json 文件路径
    config_path = None
    for a in args:
        if a.endswith(".json") and os.path.exists(a):
            config_path = a
            break
    if config_path and not preview(prj, config_path, desc):
        print("  已取消")
        if not YES:
            input("  按回车返回菜单...")
        return

    sdir = LOVART if script in ("run_image_generator.py","run_video_generator.py") else SKILL_DIR
    cmd = [sys.executable, os.path.join(sdir, script)] + args
    print(f"\n  $ {' '.join(cmd)}\n")
    sys.stdout.flush()
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"\n  ❌ 异常退出 (code={r.returncode})")
    if not YES:
        input("\n  按回车返回菜单...")

# ── 执行函数 ──

def do_video(prj, g):
    p = project_path(prj)
    run_script("run_video_generator.py", [os.path.join(p, f"prompts/group{g}_prompt_video.json"), "--project-dir", p],
               prj, f"🎬 视频 组{g}")

def do_image(prj, g):
    p = project_path(prj)
    run_script("run_image_generator.py", [os.path.join(p, f"configs/storyboard_{g}.json"), "--", "3:4", "2K"],
               prj, f"🖼️ 故事板大图 组{g}")

def do_shot(prj, n):
    p = project_path(prj)
    run_script("run_image_generator.py", [os.path.join(p, f"configs/{n}.json"), "--", "9:16", "2K"],
               prj, f"📷 逐镜 {n}")

def do_product(prj, n):
    p = project_path(prj)
    run_script("run_image_generator.py", [os.path.join(p, f"configs/product_{n}.json"), "--", "3:4", "2K"],
               prj, f"📦 产品 {n}")

def do_build(prj, g):
    p = project_path(prj)
    run_script("storyboard.py", [p, "--data", f"prompts/storyboard_data_{g}.json"],
               prj, f"🔧 拼装故事板 组{g}")

def do_board_to_video(prj, g):
    """一键装配：storyboard.py + 垫图校验 + 视频提示词补填"""
    SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(SKILL_DIR, "board_to_video.py")
    cmd = [sys.executable, script, project_path(prj), str(g)]
    print(f"\n  🔧 一键装配(故事板+视频) 组{g}\n")
    print(f"  $ {' '.join(cmd)}\n")
    sys.stdout.flush()
    subprocess.run(cmd)
    if not YES:
        input("\n  按回车返回菜单...")

# ── 菜单 ──

def line(text=""):
    print(f"│  {text:<{W-4}s}│")

def title(text):
    print(f"│  {'─'*3} {text} {'─'*(W-10-len(text))}│")

def show_menu(prj, ul, ul_enable, days):
    os.system("cls" if os.name == "nt" else "clear")
    mode_icon = "⏳" if ul else "⚡"
    mode_name = "UNLIMITED (排队)" if ul else "FAST (消耗积分)"
    mode_line = f"{mode_icon}  {mode_name}"
    if ul and days:
        mode_line += f"  剩余 {days}天"

    print("┌" + "─"*(W-2) + "┐")
    print(f"│{'':^{(W-2)//2-9}}  Studio 影视工作台{'':^{(W-2)//2-9}}│")
    print("├" + "─"*(W-2) + "┤")
    print(f"│  📁  项目: {prj:<{W-13}}│")
    print(f"│  {mode_line:<{W-4}}│")
    print("├" + "─"*(W-2) + "┤")

    # ── 工具类 ──
    title("工具类")
    line("5)  🔧  一键装配     board_to_video.py (故事板+视频)")
    line("6)  🔧  拼装故事板   单步 storyboard.py 调试用")
    line()

    # ── 生成类 ──
    title("生成类")
    line("1)  🎬  视频          15s  480p  seedance_v2_0")
    line("2)  🖼️  故事板大图    3:4  2K    gpt_image_2_medium")
    line("3)  📷  逐镜图        9:16 2K    gpt_image_2_medium")
    line("4)  📦  定妆照/产品   3:4  2K    gpt_image_2_medium")
    line()

    # ── 系统 ──
    title("系统")
    mode_target = "UNLIMITED (排队免费)" if not ul else "FAST (消耗积分)"
    line(f"7)  ⚡  切换生成模式  → {mode_target}")
    line("8)  🚪  切换项目")
    line("0)  ❌  退出")
    print("└" + "─"*(W-2) + "┘")

def direct_run(prj, cmd, arg):
    pp = project_path(prj)
    if not os.path.isdir(pp):
        print(f"❌ 项目不存在: {prj}")
        return
    print(f"\n  项目: {prj}  命令: {cmd}  参数: {arg}")
    if   cmd=="1": do_video(prj, arg)
    elif cmd=="2": do_image(prj, arg)
    elif cmd=="3": do_shot(prj, arg)
    elif cmd=="4": do_product(prj, arg)
    elif cmd=="5": do_board_to_video(prj, arg)
    elif cmd=="6": do_build(prj, arg)
    else: print("  未知命令: 1=视频 2=故事板 3=逐镜 4=产品 5=一键装配 6=单步拼装")

# ── 主 ──

def main():
    global YES
    state = load_state()
    argv = sys.argv[1:]

    YES = "--yes" in argv or "-y" in argv
    argv = [a for a in argv if a not in ("--yes", "-y")]

    prj = state.get("project", "")
    if argv:
        prj = argv[0]
        if not os.path.isdir(project_path(prj)):
            print(f"❌ 不存在项目: {prj}"); prj = ""

    unlimited, ul_enable, days = query_mode()
    state["mode"] = "unlimited" if unlimited else "fast"
    save_state(state)

    # 快捷模式
    if len(argv) >= 2:
        direct_run(prj or state["project"], argv[1], argv[2] if len(argv) >= 3 else "")
        return

    # 交互模式
    while True:
        if not prj:
            projects = list_projects()
            if not projects:
                print("❌ G:\\AgentSpace\\1_Active\\ 下没有项目")
                return
            print("\n  可选项目:\n")
            for i, p in enumerate(projects, 1):
                print(f"    {i}. {p}")
            try:
                sel = int(input("\n  选择项目编号: ").strip())
                prj = projects[sel - 1]
            except:
                print("  输入无效")
                continue
            state["project"] = prj
            save_state(state)

        unlimited, ul_enable, days = query_mode()
        show_menu(prj, unlimited, ul_enable, days)
        sel = input("\n  请选择 [0-8]: ").strip()

        if sel == "0":
            print("\n  再见！\n")
            break

        elif sel == "5":
            do_board_to_video(prj, input("  组号: ").strip())

        elif sel == "6":
            do_build(prj, input("  组号: ").strip())

        elif sel in ("1", "2", "3", "4"):
            direct_run(prj, sel, input("  组号/名称: ").strip())

        elif sel == "7":
            new_mode = not unlimited
            set_mode(new_mode)
            time.sleep(1)
            unlimited, ul_enable, days = query_mode()
            state["mode"] = "unlimited" if unlimited else "fast"
            save_state(state)
            print(f"\n  ✅ 已切换到 {'UNLIMITED (排队)' if unlimited else 'FAST (消耗积分)'}")
            input("  按回车继续...")

        elif sel == "8":
            prj = ""

if __name__ == "__main__":
    main()
