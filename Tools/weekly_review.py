#!/usr/bin/env python3
"""周复盘工具。扫最近 N 天 Daily Notes + Git log。"""
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

def gitlog(days=7):
    s = (datetime.now()-timedelta(days=days)).strftime("%Y-%m-%d")
    try:
        o = subprocess.run(["git","log",f"--since={s}","--oneline","--stat"],
                           capture_output=True,text=True,cwd=VAULT).stdout.strip()
        return o
    except: return ""

def main():
    import argparse
    a = argparse.ArgumentParser()
    a.add_argument("--days", type=int, default=7, help="扫最近 N 天")
    a.add_argument("--output")
    a.add_argument("--exclude-today", action="store_true", help="不包含今天")
    args = a.parse_args()
    offset = 1 if args.exclude_today else 0
    lines = [f"# 周复盘 — {datetime.now():%Y-%m-%d}\n---\n"]
    for d,p in recent(args.days, offset):
        with open(p) as f: lines.append(f"## {d}\n{f.read().strip()[:500]}\n")
    g = gitlog(args.days)
    if g: lines.append(f"## 变更\n```\n{g}\n```")
    lines.append("---\n*AI 分析待填写*")
    t = "\n".join(lines)
    if args.output:
        with open(args.output,"w") as f: f.write(t)
        print(f"✅ {args.output}")
    else: print(t)

if __name__ == "__main__": main()
