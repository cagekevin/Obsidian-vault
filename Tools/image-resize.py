#!/usr/bin/env python3
"""
通用图片缩放 — 按指定宽高或比例缩放图片

用法:
    python3 tools/image-resize.py 图片.png --width 800              # 指定宽度，等比缩放
    python3 tools/image-resize.py 图片.png --size 1920x1080         # 指定宽高
    python3 tools/image-resize.py 图片.png --scale 2                # 2x 放大
    python3 tools/image-resize.py 图片.png -o 输出.jpg --width 800  # 指定输出
依赖: pip install Pillow
"""

import sys
from pathlib import Path
from PIL import Image


def main():
    args = sys.argv[1:]
    if not args or "-h" in args:
        print(__doc__)
        sys.exit(1)

    filepath = args[0]
    width = None
    height = None
    scale = None
    output = None

    i = 1
    while i < len(args):
        if args[i] == "--width" and i + 1 < len(args):
            i += 1
            width = int(args[i])
        elif args[i] in ("-o", "--output") and i + 1 < len(args):
            i += 1
            output = args[i]
        elif args[i] == "--scale" and i + 1 < len(args):
            i += 1
            scale = float(args[i])
        elif args[i] == "--size" and i + 1 < len(args):
            i += 1
            parts = args[i].split("x")
            if len(parts) == 2:
                width, height = int(parts[0]), int(parts[1])
        i += 1

    img = Image.open(filepath)
    ow, oh = img.size

    if scale:
        w, h = int(ow * scale), int(oh * scale)
    elif width and height:
        w, h = width, height
    elif width:
        ratio = width / ow
        w, h = width, int(oh * ratio)
    else:
        print("⚠️ 未指定尺寸，输出原图信息")
        print(f"  原图: {ow}x{oh}")
        return

    img = img.resize((w, h), Image.LANCZOS)

    if not output:
        stem = Path(filepath).stem
        output = f"{stem}_{w}x{h}{Path(filepath).suffix}"

    img.save(output)
    print(f"✅ {ow}x{oh} → {w}x{h}  ({Path(filepath).name} → {output})")


if __name__ == "__main__":
    main()
