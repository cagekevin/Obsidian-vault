#!/usr/bin/env python3
"""
文件信息查询 — 代替 shell ls/wc/stat 等，一次调用多查

用法:
    python3 tools/list-stat-check-find-files.py ls tools/                          # 列出目录
    python3 tools/list-stat-check-find-files.py check tools/compress-image.py      # 检查文件是否存在
    python3 tools/list-stat-check-find-files.py stat tools/compress-image.py       # 详细信息
    python3 tools/list-stat-check-find-files.py find . "*.py"                      # 递归查找
"""

import sys
import os
from pathlib import Path


def cmd_ls(args):
    path = args[0] if args else "."
    p = Path(path)
    if not p.is_dir():
        print(f"❌ 不是目录: {path}")
        return
    items = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name))
    for item in items:
        size = item.stat().st_size if item.is_file() else 0
        icon = "📄" if item.is_file() else "📁" if item.is_dir() else "🔗"
        size_str = f"{size//1024}KB" if size > 0 else ""
        print(f"  {icon} {item.name}  {size_str}")


def cmd_check(args):
    """检查文件/目录是否存在，支持通配符"""
    if not args:
        print("❌ 用法: file-info check <路径>")
        return
    path = args[0]
    p = Path(path)
    if p.exists():
        kind = "目录" if p.is_dir() else "文件"
        print(f"✅ {kind}存在: {path}")
    else:
        print(f"❌ 不存在: {path}")
        # 检查父目录
        parent = p.parent
        if parent.exists():
            similar = [x.name for x in parent.iterdir() if path.lower() in x.name.lower() or x.name.lower() in path.lower()]
            if similar:
                print(f"   是否指: {', '.join(similar[:5])}")


def cmd_stat(args):
    if not args:
        return
    p = Path(args[0])
    if not p.exists():
        print(f"❌ 不存在: {args[0]}")
        return
    s = p.stat()
    print(f"📄 {p.name}")
    print(f"  大小: {s.st_size} 字节 ({s.st_size//1024}KB)")
    print(f"  修改: {_fmt_time(s.st_mtime)}")
    print(f"  创建: {_fmt_time(s.st_ctime)}")
    if p.is_file():
        text = p.read_text(encoding="utf-8", errors="ignore")
        print(f"  行数: {text.count(chr(10)) + 1}")
        print(f"  字符: {len(text)}")


def cmd_find(args):
    if len(args) < 1:
        return
    path = args[0]
    pattern = args[1] if len(args) > 1 else "*"
    root = Path(path)
    if not root.is_dir():
        print(f"❌ 不是目录: {path}")
        return
    count = 0
    for f in sorted(root.rglob(pattern)):
        if f.is_file():
            print(f"  {f.relative_to(root)}")
            count += 1
    print(f"共 {count} 个文件")


def _fmt_time(ts):
    from datetime import datetime
    return datetime.fromtimestamp(ts).strftime("%m-%d %H:%M")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    cmds = {
        "ls": cmd_ls,
        "check": cmd_check,
        "stat": cmd_stat,
        "find": cmd_find,
    }

    if cmd not in cmds:
        print(f"❌ 未知: {cmd} (可用: ls/check/stat/find)")
        sys.exit(1)

    cmds[cmd](args)


if __name__ == "__main__":
    main()
