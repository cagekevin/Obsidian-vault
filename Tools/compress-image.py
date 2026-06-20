#!/usr/bin/env python3
"""
图片压缩工具 — 优先 pngquant/oxipng/jpegoptim，无依赖时自动用 Pillow 兜底。

用法：
    python3 compress-image.py 图片.png                     ← 默认压缩（macOS有损/Windows无损）
    python3 compress-image.py 图片.png --lossless           ← 强制无损模式
    python3 compress-image.py input.jpg -q 70               ← 指定质量
    python3 compress-image.py *.png --out-dir compressed    ← 批量输出到目录
    python3 compress-image.py input.png --format webp       ← 转 WebP
    python3 compress-image.py "\\nas\share\folder\*.png"    ← 网络路径

平台说明：
    - macOS 默认 pngquant 256色量化（有损，画质可接受）
    - Windows 默认走无损（Pillow 量化效果差，跳过）
    - 都支持 --lossless 强制无损

依赖（可选）：
    brew install pngquant oxipng jpegoptim  (macOS，有则用，无则 Pillow)
    pip install Pillow                      (Windows 必需，macOS 格式转换也需要)
"""
import sys, os, subprocess, json, glob
from pathlib import Path

# 检查外部工具可用性
_HAS_PNGQUANT = subprocess.run(["which", "pngquant"], capture_output=True).returncode == 0 if sys.platform != "win32" else False
_HAS_JPEGOPTIM = subprocess.run(["which", "jpegoptim"], capture_output=True).returncode == 0 if sys.platform != "win32" else False
_HAS_OXIPNG = subprocess.run(["which", "oxipng"], capture_output=True).returncode == 0 if sys.platform != "win32" else False


def has_pillow():
    try:
        from PIL import Image
        return True
    except ImportError:
        return False


def compress_png(path, quality_min=75, quality_max=90, output=None, lossless=False):
    """用 pngquant（有）或 Pillow（无）压缩 PNG。
    lossless=True 时跳过量化，仅 oxipng/Pillow optimize 无损优化。
    Windows 默认走 lossless（无 pngquant/oxipng，Pillow 量化效果差）"""
    out = output or path
    is_win = sys.platform == "win32"

    if lossless or is_win:
        if _HAS_OXIPNG:
            subprocess.run(["oxipng", "-o", "4", "--strip", "safe", "--out", str(out), str(path)], capture_output=True)
            return out
        else:
            return _compress_png_pillow(path, out, lossless=True)

    if _HAS_PNGQUANT:
        temp = path.parent / f"__q_{path.name}"
        r = subprocess.run([
            "pngquant", f"--quality={quality_min}-{quality_max}",
            "--speed=1", "--force", "--output", str(temp), str(path)
        ], capture_output=True)
        if r.returncode != 0:
            print(f"  ⚠️  pngquant 失败: {path.name}")
            return None
        if _HAS_OXIPNG:
            subprocess.run(["oxipng", "-o", "4", "--strip", "safe", "--out", str(out), str(temp)], capture_output=True)
            temp.unlink(missing_ok=True)
        else:
            if out != temp:
                temp.rename(out)
        return out
    else:
        return _compress_png_pillow(path, out)


def _compress_png_pillow(path, output, lossless=False):
    """Pillow 压缩：lossless=True 仅 optimize，否则量化到 256 色"""
    if not has_pillow():
        print("  ⚠️  无 oxipng 也无 Pillow，跳过")
        return None
    try:
        from PIL import Image
        img = Image.open(path)
        if lossless:
            img.save(output, "PNG", optimize=True)
        else:
            if img.mode == "RGBA":
                r, g, b, a = img.split()
                rgb = Image.merge("RGB", (r, g, b))
                pal = rgb.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
                pal_rgba = pal.convert("RGBA")
                pal_rgba.putalpha(a)
                pal_rgba.save(output, optimize=True)
            else:
                img.quantize(colors=256, method=Image.Quantize.MEDIANCUT).save(output, optimize=True)
        return Path(output)
    except Exception as e:
        print(f"  ⚠️  Pillow 压缩失败: {e}")
        return None


def compress_jpeg(path, quality=80, output=None):
    """用 jpegoptim（有）或 Pillow（无）压缩 JPEG"""
    out = output or path

    if _HAS_JPEGOPTIM:
        if out == path:
            r = subprocess.run(["jpegoptim", f"-m{quality}", "--strip-all", "--preserve", str(path)], capture_output=True)
        else:
            import shutil
            shutil.copy2(path, out)
            r = subprocess.run(["jpegoptim", f"-m{quality}", "--strip-all", "--preserve", str(out)], capture_output=True)
        if r.returncode == 0:
            return out
        return None
    else:
        return _compress_jpeg_pillow(path, quality, out)


def _compress_jpeg_pillow(path, quality, output):
    """Pillow JPEG 再压缩"""
    if not has_pillow():
        print("  ⚠️  无 jpegoptim 也无 Pillow，跳过")
        return None
    try:
        from PIL import Image
        img = Image.open(path)
        img.save(output, "JPEG", quality=quality, optimize=True)
        return Path(output)
    except Exception as e:
        print(f"  ⚠️  Pillow 压缩失败: {e}")
        return None


def convert_format(path, target_fmt, output):
    """转格式（用 Pillow）"""
    if not has_pillow():
        print("  ⚠️  需要 Pillow 才能转格式: pip install Pillow")
        return None
    from PIL import Image
    fmt_map = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WebP"}
    pil_fmt = fmt_map.get(target_fmt.lower())
    if not pil_fmt:
        print(f"  ⚠️  不支持的格式: {target_fmt}")
        return None
    img = Image.open(path)
    kw = {"optimize": True}
    if pil_fmt in ("JPEG", "WebP"):
        kw["quality"] = 85
    img.save(output, pil_fmt, **kw)
    return output


def fmt_size(b):
    if b < 1024:
        return f"{b}B"
    elif b < 1024 * 1024:
        return f"{b//1024}KB"
    else:
        return f"{b/(1024*1024):.1f}MB"


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return

    # 提示可用工具
    tools = []
    if _HAS_PNGQUANT: tools.append("pngquant")
    if _HAS_JPEGOPTIM: tools.append("jpegoptim")
    if _HAS_OXIPNG: tools.append("oxipng")
    pill = has_pillow()
    mode = f"  [{', '.join(tools)}]" if tools else "  [Pillow]" if pill else "  [⚠️  无压缩引擎]"
    print(mode)

    args = sys.argv[1:]
    inputs = []
    quality = 80
    quality_min = 75
    quality_max = 90
    lossless = False
    out_dir = None
    target_format = None

    i = 0
    while i < len(args):
        if args[i] in ("-q", "--quality"):
            i += 1
            quality = int(args[i])
        elif args[i] == "--quality-range":
            i += 1
            parts = args[i].split("-")
            quality_min = int(parts[0])
            quality_max = int(parts[1])
        elif args[i] == "--lossless":
            lossless = True
        elif args[i] in ("--out-dir",):
            i += 1
            out_dir = Path(args[i])
            out_dir.mkdir(parents=True, exist_ok=True)
        elif args[i] in ("--format",):
            i += 1
            target_format = args[i].lower().lstrip(".")
        else:
            if "*" in args[i]:
                inputs.extend(glob.glob(args[i]))
            else:
                inputs.append(args[i])
        i += 1

    if not inputs:
        print("❌ 未指定输入文件")
        return

    results = []
    for inp in inputs:
        path = Path(inp)
        if not path.exists():
            print(f"❌ 文件不存在: {inp}")
            continue

        suffix = path.suffix.lower()
        orig_size = path.stat().st_size

        if out_dir:
            stem = path.stem
            out_ext = f".{target_format}" if target_format else path.suffix
            output = out_dir / f"{stem}{out_ext}"
        else:
            output = None

        if target_format:
            temp = path.parent / f"__temp_{path.name}"
            if suffix in (".png",):
                result = compress_png(path, quality_min, quality_max, temp)
            elif suffix in (".jpg", ".jpeg"):
                result = compress_jpeg(path, quality, temp)
            else:
                print(f"  ⚠️  不支持格式: {suffix}")
                continue
            if result:
                final = convert_format(result, target_format, str(output or path.parent / f"{path.stem}.{target_format}"))
                result = Path(final)
                temp.unlink(missing_ok=True)
            else:
                temp.unlink(missing_ok=True)
                continue
        else:
            if suffix in (".png",):
                result = compress_png(path, quality_min, quality_max, output)
            elif suffix in (".jpg", ".jpeg"):
                result = compress_jpeg(path, quality, output)
            else:
                print(f"  ⚠️  不支持格式: {suffix}")
                continue

        if not result:
            continue

        new_size = result.stat().st_size
        ratio = (1 - new_size / orig_size) * 100
        print(f"  {path.name}  {fmt_size(orig_size)} → {fmt_size(new_size)}  (-{ratio:.0f}%)  →  {result}")
        results.append({"file": str(result), "original": orig_size, "compressed": new_size, "ratio": round(ratio, 1)})

    if results:
        total_orig = sum(r["original"] for r in results)
        total_new = sum(r["compressed"] for r in results)
        total_ratio = (1 - total_new / total_orig) * 100
        print(f"\n  总计: {fmt_size(total_orig)} → {fmt_size(total_new)}  (-{total_ratio:.0f}%)")
        print(json.dumps({"success": True, "total_ratio": round(total_ratio, 1)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
