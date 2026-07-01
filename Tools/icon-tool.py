#!/usr/bin/env python3
"""图标搜索下载工具 — 支持 Lucide / Heroicons / Phosphor 三个图标库，统一 stroke-width=1, 128×128"""

import os, sys, glob, re


def print_help():
    print("""
用法:
  python icon-tool.py search <关键词>      搜索图标
  python icon-tool.py download <图标名1> [图标名2 ...]  下载图标

示例:
  python icon-tool.py search heart
  python icon-tool.py download heart star moon

说明:
  - 搜索 Lucide / Heroicons / Phosphor（thin 风格）三个库
  - 下载统一 stroke-width=1, 尺寸 128×128
  - 文件保存到: C:\\Users\\xinye\\Downloads\\
""")


# ===== 配置 =====
ICON_DIRS = {
    "Lucide":   r"g:\Obsidian-vault\node_modules\lucide-static\icons",
    "Heroicons": r"g:\Obsidian-vault\node_modules\@heroicons\svg",
    "Phosphor": r"g:\Obsidian-vault\node_modules\@phosphor-icons\core\assets\thin",
}
OUTPUT_DIR = r"C:\Users\xinye\Downloads"

# 默认下载参数
STROKE_WIDTH = "1"
ICON_SIZE = "128"


def search_icons(keyword):
    """在三个图标库中搜索匹配的图标，精确匹配优先"""
    kw = keyword.lower()
    results = []
    seen_heroicons = {}  # Heroicons 同名去重
    for lib, path in ICON_DIRS.items():
        if not os.path.exists(path):
            continue
        pattern = os.path.join(path, "**", "*.svg") if lib == "Heroicons" else os.path.join(path, "*.svg")
        for f in glob.glob(pattern, recursive=True):
            name = os.path.splitext(os.path.basename(f))[0]
            if kw in name.lower():
                if lib == "Heroicons":
                    # Heroicons 同名只保留一条，附上子目录信息
                    if name not in seen_heroicons:
                        rel = os.path.relpath(os.path.dirname(f), path)
                        seen_heroicons[name] = f"{name} ({rel})"
                        results.append((lib, seen_heroicons[name], f))
                else:
                    results.append((lib, name, f))

    # 精确匹配排最前，其余字母序
    results.sort(key=lambda x: (0 if x[1].startswith(kw) and (len(x[1]) == len(kw) or x[1][len(kw)] in ('-', ' ', '(')) else 1, x[1]))
    return results


def download_icons(names):
    """下载图标，统一 stroke-width 和尺寸"""
    downloaded = []
    not_found = []

    # 先在所有库中建立名称→路径索引
    name_to_path = {}
    for lib, path in ICON_DIRS.items():
        if not os.path.exists(path):
            continue
        pattern = os.path.join(path, "**", "*.svg") if lib == "Heroicons" else os.path.join(path, "*.svg")
        for f in glob.glob(pattern, recursive=True):
            n = os.path.splitext(os.path.basename(f))[0]
            if n not in name_to_path:
                name_to_path[n] = f

    for name in names:
        if name in name_to_path:
            src = name_to_path[name]
            with open(src, "r", encoding="utf-8") as f:
                svg = f.read()
            # 统一参数
            # 先替换 stroke-width
            svg = re.sub(r'stroke-width="\d+(\.\d+)?"', f'stroke-width="{STROKE_WIDTH}"', svg)
            # 再替换独立的 width/height（前面带空格或换行，避免匹配 stroke-width 里残留的数字）
            svg = re.sub(r'(?<![-\w])width="\d+(\.\d+)?"', f'width="{ICON_SIZE}"', svg)
            svg = re.sub(r'(?<![-\w])height="\d+(\.\d+)?"', f'height="{ICON_SIZE}"', svg)
            out = os.path.join(OUTPUT_DIR, f"{name}.svg")
            with open(out, "w", encoding="utf-8") as f:
                f.write(svg)
            downloaded.append(f"{name}.svg")
        else:
            not_found.append(name)

    return downloaded, not_found


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "search":
        if len(sys.argv) < 3:
            print("请指定搜索关键词，例如: python icon-tool.py search heart")
            sys.exit(1)
        keyword = sys.argv[2]
        results = search_icons(keyword)
        if not results:
            print(f'未找到匹配 "{keyword}" 的图标')
            sys.exit(0)
        print(f'\n搜索 "{keyword}" 结果 ({len(results)} 个):\n')
        for lib, name, path in results:
            print(f"  [{lib:10s}] {name}")
        print(f'\n共 {len(results)} 个匹配\n提示: 用 "python icon-tool.py download <图标名>" 下载')

    elif cmd == "download":
        if len(sys.argv) < 3:
            print("请指定要下载的图标名，例如: python icon-tool.py download heart")
            sys.exit(1)
        names = sys.argv[2:]
        downloaded, not_found = download_icons(names)
        if downloaded:
            print(f"\n✓ 已下载 ({len(downloaded)} 个):")
            for f in downloaded:
                print(f"  {OUTPUT_DIR}\\{f}")
            print(f"  参数: stroke-width={STROKE_WIDTH}, size={ICON_SIZE}×{ICON_SIZE}")
        if not_found:
            print(f"\n✗ 未找到 ({len(not_found)} 个):")
            for n in not_found:
                print(f"  {n}")
            print("提示: 先用 search 搜索确认图标名是否正确")

    else:
        print(f'未知命令: {cmd}')
        print_help()
