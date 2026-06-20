#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import glob
import os
import sys
from pathlib import Path

try:
    from rembg import remove, new_session
except ImportError:
    print("Missing dependency: rembg", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Missing dependency: Pillow", file=sys.stderr)
    sys.exit(1)

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

def clean_mask_noise(mask_img: Image.Image, area_threshold_ratio=0.05) -> Image.Image:
    """用 OpenCV 清理黑白蒙版上的孤立杂色碎片"""
    arr = np.array(mask_img)
    _, binary = cv2.threshold(arr, 10, 255, cv2.THRESH_BINARY)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
    
    if num_labels <= 1: return mask_img
        
    areas = stats[1:, cv2.CC_STAT_AREA] 
    max_area = np.max(areas) 
    
    clean_mask = np.zeros_like(arr)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] >= max_area * area_threshold_ratio:
            clean_mask[labels == i] = arr[labels == i]
            
    return Image.fromarray(clean_mask)

def process_file(input_path: str, output_path: str, session, use_matting: bool = False):
    img = Image.open(input_path)

    # 💡 核心：only_mask=True，让 AI 只吐出黑白蒙版，不破坏原图！
    result = remove(
        img,
        session=session,
        alpha_matting=use_matting,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10,
        post_process_mask=True, 
        only_mask=True 
    )

    if HAS_CV2:
        result = clean_mask_noise(result)

    result.save(output_path, optimize=True)
    return result.size

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="+")
    parser.add_argument("-o", "--output")
    parser.add_argument("--matting", action="store_true")
    parser.add_argument("--product", action="store_true") 
    parser.add_argument("--model", default="bria-rmbg") # 💡 默认升级为电商顶流模型
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    files = []
    for pattern in args.input:
        matched = glob.glob(pattern, recursive=False)
        if matched: files.extend(matched)

    if not files: sys.exit(1)

    # 如果是人像，依然用最好的人像专模；如果是产品，直接上 BRIA 大模型
    model_name = "u2net_human_seg" if args.matting else args.model

    if not args.quiet:
        print(f"⏳ 加载神级模型 {model_name}...")
    
    session = new_session(model_name)
    
    for i, f in enumerate(files, 1):
        out_path = args.output if args.output else str(Path(f).with_name(f"{Path(f).stem}_nobg.png").resolve())
        try:
            process_file(f, out_path, session, use_matting=args.matting)
        except Exception as e:
            if not args.quiet: print(f"❌ 失败: {e}")

if __name__ == "__main__":
    main()
