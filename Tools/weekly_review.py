#!/usr/bin/env python3
"""周复盘工具。扫最近 N 天 Daily Notes + Git log 统计 + 目标检查。"""
import os, subprocess
from datetime import datetime, timedelta
VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAILY = os.path.join(VAULT, "Daily Notes")

def recent(days=7, offset=0):
    r = []
    for i in range(offset, offset+days):
        d = (datetime.now()-timedelta(days=i)).strftime("%Y-%m-%d")
        p = os.path.join(DAILY, f"{d}.md")
        if os.path.exists(p): r.append((d, p))
    return sorted(r)

def git_stats(days=7):
    """返回文件变更统计，不输出完整 log"""
    s = (datetime.now()-timedelta(days=days)).strftime("%Y-%m-%d")
    try:
        o = subprocess.run(["git","log",f"--since={s}","--name-only","--format=","--diff-filter=AM"],
                           capture_output=True,text=True,cwd=VAULT).stdout.strip()
        files = [l for l in o.split("\n") if l.strip()]
        counts = {}
        for f in files:
            ext = os.path.splitext(f)[1] or "(无后缀)"
            counts[ext] = counts.get(ext, 0) + 1
        total = len(files)
        unique = len(set(files))
        return f"修改文件：{total} 次 / {unique} 个唯一文件\n" + \
               "\n".join(f"  {k}: {v}" for k,v in sorted(counts.items(), key=lambda x:-x[1]))
    except:
        return ""

def read_goals():
    p = os.path.join(VAULT, "Context", "goals.md")
    if os.path.exists(p):
        with open(p) as f: return f.read().strip()
    return ""

def full_audit(days=7):
    """完整输出校准日志内容"""
    mem_dir = os.path.join(VAULT, ".codebuddy", "memory")
    parts = []
    for i in range(days):
        d = (datetime.now()-timedelta(days=i+1)).strftime("%Y-%m-%d.md")
        p = os.path.join(mem_dir, d)
        if os.path.exists(p):
            with open(p) as f:
                parts.append(f"### {d}\n{f.read().strip()}")
    return "\n\n".join(parts)

def main():
    import argparse
    a = argparse.ArgumentParser()
    a.add_argument("--days", type=int, default=7)
    a.add_argument("--output")
    a.add_argument("--exclude-today", action="store_true")
    a.add_argument("--audit", action="store_true", help="包含校准日志审计")
    args = a.parse_args()
    offset = 1 if args.exclude_today else 0

    now = datetime.now()
    lines = [f"# 周复盘 — {now:%Y} 第 {now.isocalendar()[1]} 周\n---\n"]

    # Daily Notes 摘要
    for d,p in recent(args.days, offset):
        with open(p) as f: lines.append(f"## {d}\n{f.read().strip()[:500]}\n")

    # 文件变更统计
    g = git_stats(args.days)
    if g: lines.append(f"## 文件变更\n```\n{g}\n```")

    # 目标检查
    goals = read_goals()
    if goals:
        lines.append(f"## 目标检查\n当前目标：\n```\n{goals[:500]}\n```\n")

    # 校准日志审计（完整版）
    if args.audit:
        audit = full_audit(args.days)
        if audit:
            lines.append(f"## 校准日志审计\n\n{audit}\n")

    # AI 分析空位（按顺序填写，最后做文件体检）
    lines.append("---\n## AI 分析\n\n### 1. 本周重点\n\n### 2. 与目标对比\n\n### 3. 目标是否需要更新？\n\n### 4. 本期最值得追踪的问题\n\n### 5. 校准日志沉淀建议\n\n---\n\n### 6. 文件体检\n检查以下文件有无矛盾或过时内容（列出清单，不直接改）：\n\n- `Context/goals.md`：\n- `Context/style.md`：\n- `Context/profile.md`：\n- `Context/brand.md`：\n- `CLAUDE.md` 核心规则：\n- 校准日志已解决的问题 → 对应规则可删除？：\n")

    t = "\n".join(lines)
    if args.output:
        with open(args.output,"w") as f: f.write(t)
        print(f"✅ {args.output}")
    else: print(t)

if __name__ == "__main__": main()
