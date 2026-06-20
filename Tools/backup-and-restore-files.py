#!/usr/bin/env python3
"""
文件备份器 — AI 做高风险修改前自动备份到文件同级 .backups/，带时间戳

用法:
    python3 tools/backup-and-restore-files.py 文件.md                              # 备份
    python3 tools/backup-and-restore-files.py 文件.md --restore                     # 恢复最近
    python3 tools/backup-and-restore-files.py 文件.md --list                        # 列出备份
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime


def backup_dir(p):
    """备份目录 = 文件同级 .backups/"""
    return p.parent / ".backups"


def backup_single(p):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak_dir = backup_dir(p)
    bak_dir.mkdir(parents=True, exist_ok=True)
    bak_path = bak_dir / f"{p.name}.{ts}.bak"
    shutil.copy2(str(p), str(bak_path))
    print(f"💾 已备份: {bak_path}")
    return bak_path


def list_backups(p):
    bak_dir = backup_dir(p)
    if not bak_dir.exists():
        print("  没有备份记录")
        return []
    backups = sorted(bak_dir.glob(f"{p.name}.*.bak"), reverse=True)
    for b in backups:
        ts = b.suffixes[-2].lstrip(".") if len(b.suffixes) >= 2 else "??"
        size = b.stat().st_size // 1024
        print(f"  {ts}  {size}KB  {b.name}")
    return backups


def restore_single(p, bak_path=None):
    if not bak_path:
        bak_dir = backup_dir(p)
        backups = sorted(bak_dir.glob(f"{p.name}.*.bak"), reverse=True)
        if not backups:
            print(f"❌ 没有找到 {p.name} 的备份")
            return
        bak_path = backups[0]

    shutil.copy2(str(bak_path), str(p))
    print(f"♻️  已恢复: {bak_path} → {p}")


def main():
    args = sys.argv[1:]
    if not args or "-h" in args:
        print(__doc__)
        sys.exit(1)

    path = Path(args[0])
    if not path.exists():
        print(f"❌ 不存在: {path}")
        sys.exit(1)

    if "--list" in args:
        if path.is_file():
            list_backups(path)
        return

    if "--restore" in args:
        if path.is_file():
            restore_single(path)
        return

    if path.is_file():
        backup_single(path)


if __name__ == "__main__":
    main()
