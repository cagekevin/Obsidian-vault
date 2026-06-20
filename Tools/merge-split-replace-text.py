#!/usr/bin/env python3
"""
批量替换工具 — AI 跨文件精准替换，不支持的操作不要硬来

一次性在多个文件中执行精确/正则替换，支持预览确认和备份回滚。
不需要手动逐文件编辑。

用法:
    # 基本替换
    text-tool replace 文件.md "旧文本" "新文本"

    # 正则替换（! 确保正则只匹配目标，不误伤）
    text-tool replace 文件.md "pattern" "替换为" --regex

    # 批量替换所有 .md 文件
    text-tool replace "旧文本" "新文本" --glob "*.md"

    # 预览模式（不改，只看差异）
    text-tool replace "旧" "新" --glob "*.md" --preview

    # 忽略大小写
    text-tool replace "old" "new" --glob "*.py" -i

    # 备份后替换 + 失败恢复
    text-tool replace "旧" "新" --glob "*.json" --backup
    text-tool undo 文件.json           # 恢复备份

    # 仅替换特定行号范围（精确控制）
    text-tool replace 文件.md "旧" "新" --lines 5-20

参数:
    <文件或模式>         文件路径 或 --glob 匹配模式
    <旧文本>             要替换的文本（精确或正则）
    <新文本>             替换后的文本
    --regex / -r         启用正则模式
    --preview / -p       只显示差异，不写入
    --backup / -b        替换前创建 .bak 备份
    --glob / -g <模式>   文件匹配模式（如 "*.md" "src/**/*.py"）
    --lines / -l <范围>  行号范围 "5-20"，仅在该范围内替换
    -i                   忽略大小写

关键词: 批量替换, 正则替换, 跨文件替换, 文本替换, 代码批量修改
"""
import os, re, sys, glob as glob_mod
from pathlib import Path


def _backup(path):
    bak = str(path) + ".bak"
    if not Path(bak).exists():
        Path(bak).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")


def _restore(path):
    bak = str(path) + ".bak"
    if Path(bak).exists():
        path.write_text(Path(bak).read_text(encoding="utf-8"), encoding="utf-8")
        Path(bak).unlink()
        print(f"↩️  已恢复: {path}")
    else:
        print(f"⚠️  没有备份: {path}.bak")


def _resolve_files(pattern):
    files = sorted(glob_mod.glob(pattern, recursive=True))
    return [f for f in files if os.path.isfile(f)]


def _do_replace(text, old, new, flags, is_regex):
    if is_regex:
        return re.sub(old, new, text, flags=flags)
    return text.replace(old, new)


def _count_matches(text, old, flags, is_regex):
    if is_regex:
        return len(re.findall(old, text, flags=flags))
    return text.count(old)


def _show_preview(path, old, new, is_regex, ignore_case, lines_range):
    content = Path(path).read_text(encoding="utf-8")
    flags = re.IGNORECASE if ignore_case else 0
    lines = content.split("\n")
    if lines_range:
        start, end = lines_range
        lines = lines[start-1:end]
        offset = start
    else:
        lines = lines[:]
        offset = 1
    found = False
    for i, line in enumerate(lines, offset):
        if is_regex and re.search(old, line, flags):
            new_line = re.sub(old, new, line, flags=flags)
            print(f"  -{i:>4}: {line}")
            print(f"  +{i:>4}: {new_line}")
            found = True
        elif not is_regex and old in line:
            new_line = line.replace(old, new)
            if ignore_case:
                # case-insensitive: find actual match preserving case
                idx = line.lower().index(old.lower())
                actual = line[idx:idx+len(old)]
                new_line = line.replace(actual, new)
            else:
                new_line = line.replace(old, new)
            print(f"  -{i:>4}: {line}")
            print(f"  +{i:>4}: {new_line}")
            found = True
    if not found:
        print(f"  (当前范围内无匹配)")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    # ── undo 命令 ──
    if cmd == "undo":
        if not args:
            print("❌ 用法: undo <文件>")
            return
        _restore(Path(args[0]))
        return

    # ── replace 命令 ──
    if cmd != "replace":
        print(f"❌ 未知命令: {cmd}")
        print(f"   唯一可用命令: replace")
        return

    # 解析参数
    glob_pattern = None
    is_regex = False
    preview = False
    backup = False
    ignore_case = False
    lines_range = None
    positional = []

    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--glob", "-g") and i + 1 < len(args):
            i += 1
            glob_pattern = args[i]
        elif a in ("--regex", "-r"):
            is_regex = True
        elif a in ("--preview", "-p"):
            preview = True
        elif a in ("--backup", "-b"):
            backup = True
        elif a == "-i":
            ignore_case = True
        elif a in ("--lines", "-l") and i + 1 < len(args):
            i += 1
            parts = args[i].split("-")
            start, end = int(parts[0]), int(parts[1]) if len(parts) > 1 else int(parts[0])
            lines_range = (start, end)
        elif a.startswith("-"):
            pass
        else:
            positional.append(a)
        i += 1

    if len(positional) < 2:
        print("❌ 用法: replace <旧文本/文件> <新文本> [选项]")
        return

    # 第一个位置参数可能是文件路径或旧文本
    # 判断：如果无 --glob 且第一个参数是文件 → 单文件模式
    first_arg = positional[0]
    if not glob_pattern and not _resolve_files(first_arg):
        # 普通替换：待替换文件放最后面或由 --glob 指定
        if len(positional) < 3:
            print("❌ 需要指定文件: replace 文件.md '旧' '新'")
            return
        filepath, old, new = positional[0], positional[1], positional[2]
        files = [filepath]
    elif not glob_pattern:
        # 单文件，第一个参数就是文件路径
        old = positional[1]
        new = " ".join(positional[2:]) if len(positional) > 2 else ""
        files = [first_arg]
    else:
        # 批量模式
        old = positional[0]
        new = " ".join(positional[1:])
        files = _resolve_files(glob_pattern)

    if not files:
        print("❌ 没有匹配的文件")
        return

    flags = re.IGNORECASE if ignore_case else 0
    total_changes = 0

    for fp in files:
        p = Path(fp)
        if not p.exists():
            print(f"  ⚠️  跳过: {fp}（不存在）")
            continue
        content = p.read_text(encoding="utf-8")
        if lines_range:
            start, end = lines_range
            lines = content.split("\n")
            target = "\n".join(lines[start-1:end])
            count = _count_matches(target, old, flags, is_regex)
        else:
            count = _count_matches(content, old, flags, is_regex)
        if count == 0:
            continue
        total_changes += count

        if preview:
            print(f"\n📄 {p} ({count} 处):")
            _show_preview(fp, old, new, is_regex, ignore_case, lines_range)
        else:
            if backup:
                _backup(p)
            if lines_range:
                start, end = lines_range
                lines = content.split("\n")
                lines[start-1:end] = [_do_replace("\n".join(lines[start-1:end]), old, new, flags, is_regex)].pop().split("\n")
                new_content = "\n".join(lines)
            else:
                new_content = _do_replace(content, old, new, flags, is_regex)
            p.write_text(new_content, encoding="utf-8")
            print(f"  ✅ {p}: {count} 处替换")

    if total_changes == 0:
        print(f"⚠️ 未找到匹配: {old}")
    else:
        print(f"\n✅ 总计: {total_changes} 处替换" + ("（预览模式，未写入）" if preview else ""))


if __name__ == "__main__":
    main()
