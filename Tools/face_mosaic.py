#!/usr/bin/env python3
"""
人脸打码工具 — 提取自 FACE-MOSAIC-VIDEO (幽浮喵)
用法: python face_mosaic.py 图片1.jpg 图片2.jpg ...
"""

import cv2
import numpy as np
from pathlib import Path
import sys

SUPPORTED = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


class FaceMosaic:
    def __init__(self, size=15):
        self.size = size
        self.cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def imread(self, path):
        arr = np.fromfile(str(path), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"无法读取: {path}")
        return img

    def imwrite(self, path, img):
        ok, buf = cv2.imencode(".jpg", img)
        if not ok:
            raise ValueError("编码失败")
        buf.tofile(str(path))

    def process(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        result = img.copy()
        for x, y, w, h in faces:
            roi = result[y:y+h, x:x+w]
            block = max(2, self.size)
            small = cv2.resize(roi, None, fx=1/block, fy=1/block, interpolation=cv2.INTER_NEAREST)
            result[y:y+h, x:x+w] = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
        return result, len(faces)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python face_mosaic.py 图片1.jpg 图片2.jpg ...")
        sys.exit(1)

    mosaic = FaceMosaic(size=15)

    for path_str in sys.argv[1:]:
        p = Path(path_str)
        if not p.exists() or p.suffix.lower() not in SUPPORTED:
            print(f"跳过: {p.name} (不支持或不存在)")
            continue
        try:
            img = mosaic.imread(p)
            result, fc = mosaic.process(img)
            output_dir = p.parent / "output"
            output_dir.mkdir(exist_ok=True)
            out_path = output_dir / f"mosaic_{p.name}"
            mosaic.imwrite(out_path, result)
            print(f"{p.name} → {out_path}  (检测到 {fc} 个人脸)")
        except Exception as e:
            print(f"{p.name} 失败: {e}")
