#!/usr/bin/env python3
"""
Pixiv 风格插画增强工具 — 支持超分辨率放大、智能锐化、批量处理，专为二次元/数字插画优化。
"""
import os, sys, argparse, glob
from PIL import Image, ImageFilter, ImageEnhance

# ───── 参数 ─────
parser = argparse.ArgumentParser(description="插画增强工具 — 超分 + 锐化 + 批量")
parser.add_argument("input", help="输入图片或目录")
parser.add_argument("-o", "--output", default=None, help="输出路径（目录时自动命名）")
parser.add_argument("-s", "--scale", type=float, default=2.0, help="放大倍数 (默认: 2)")
parser.add_argument("--max-size", type=int, default=4096, help="最大边长限制 (默认: 4096)")
parser.add_argument("--sharpness", type=float, default=1.3, help="锐化强度 0.5-2.0 (默认: 1.3)")
parser.add_argument("--denoise", type=float, default=0.3, help="降噪强度 0-1.0 (默认: 0.3)")
parser.add_argument("--format", choices=["png", "jpg", "webp"], default="png", help="输出格式")
parser.add_argument("--jpg-quality", type=int, default=92, help="JPG/WebP 质量 (默认: 92)")
parser.add_argument("--overwrite", action="store_true", help="覆盖原文件")
args = parser.parse_args()


# ───── 核心处理 ─────
def enhance_image(img: Image.Image, name: str) -> Image.Image:
    """对一张插画执行增强流水线"""
    w, h = img.size


    # ─ 分步放大（质量更好）─
    current = img
    steps = max(1, int(args.scale * 2))
    for i in range(steps):
        ratio = (i + 1) / steps
        sw = min(int(w * args.scale * ratio), args.max_size)
        sh = min(int(h * args.scale * ratio), args.max_size)
        current = current.resize((sw, sh), Image.LANCZOS)

    # ─ 插画锐化 ─
    if args.sharpness > 0:
        # 保留 alpha 通道（如有）
        alpha = None
        if current.mode == "RGBA":
            alpha = current.split()[-1]
            current = current.convert("RGB")

        # 转为 HSV，只锐化明度通道（保留色相纯度）
        hsv = current.convert("HSV")
        h, s, v = hsv.split()
        v_sharp = v.filter(ImageFilter.UnsharpMask(
            radius=min(1.5, args.sharpness * 0.8),
            percent=int(100 * args.sharpness),
            threshold=3
        ))
        v_mixed = Image.blend(v, v_sharp, 0.35 * (args.sharpness - 0.3))
        hsv_sharp = Image.merge("HSV", (h, s, v_mixed))
        current = hsv_sharp.convert("RGB")

        # 还原 alpha
        if alpha:
            current.putalpha(alpha)

    # ─ 轻微降噪（清理压缩伪影）─
    if args.denoise > 0:
        strength = int(args.denoise * 3)
        if strength > 0:
            current = current.filter(ImageFilter.MedianFilter(size=strength))

    # ─ 微对比度提升（让颜色更通透）─
    enh = ImageEnhance.Contrast(current)
    current = enh.enhance(1.05)

    return current


def process_img(path: str):
    """处理单张图片"""
    try:
        img = Image.open(path)
    except Exception as e:
        print(f"  ⚠ 无法打开: {path} — {e}")
        return

    # 确定输出路径
    ext_map = {"png": "png", "jpg": "jpg", "jpeg": "jpg", "webp": "webp"}
    out_ext = ext_map.get(args.format.lower(), args.format.lower())

    if args.overwrite:
        out = path
    elif args.output and os.path.isdir(args.output):
        base = os.path.splitext(os.path.basename(path))[0]
        out = os.path.join(args.output, f"{base}_enhanced.{out_ext}")
    elif args.output and not os.path.isdir(args.output):
        out = args.output
    else:
        base = os.path.splitext(path)[0]
        out = f"{base}_enhanced.{out_ext}"

    print(f"  📐 {img.size[0]}x{img.size[1]} → ", end="")

    result = enhance_image(img, path)

    # 保存
    save_kw = {}
    if out_ext in ("jpg", "jpeg"):
        save_kw["quality"] = args.jpg_quality
        if result.mode == "RGBA":
            result = result.convert("RGB")
    elif out_ext == "webp":
        save_kw["quality"] = args.jpg_quality
    elif out_ext == "png":
        save_kw["optimize"] = True

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    result.save(out, **save_kw)

    print(f"{result.size[0]}x{result.size[1]}  ✅ {out}")


# ───── 主流程 ─────
def main():
    input_path = args.input

    if os.path.isfile(input_path):
        files = [input_path]
    elif os.path.isdir(input_path):
        exts = ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.bmp", "*.tiff")
        files = []
        for ext in exts:
            files.extend(glob.glob(os.path.join(input_path, ext)))
            files.extend(glob.glob(os.path.join(input_path, ext.upper())))
        files = sorted(set(files))
        if not files:
            print(f"❌ {input_path} 下没有找到图片文件")
            sys.exit(1)
    else:
        print(f"❌ 路径不存在: {input_path}")
        sys.exit(1)

    print(f"🎨 Pixiv 插画增强器 — {len(files)} 张")
    print(f"   放大 {args.scale}x | 锐化 {args.sharpness} | 降噪 {args.denoise}")
    print()

    for f in files:
        process_img(f)

    print(f"\n✅ 完成！共处理 {len(files)} 张")


if __name__ == "__main__":
    main()
