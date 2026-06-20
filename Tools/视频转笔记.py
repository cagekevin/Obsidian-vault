#!/usr/bin/env python3
"""
极简本地音视频转文字工具 (whisper-cpp 版)
依赖: whisper-cli (已装: brew install whisper-cpp)
      模型: ~/.whisper-models/ggml-small.bin

用法:
  python3 视频转笔记.py /路径/到/音频.mp3
"""

import subprocess
import sys
import argparse
import tempfile
import os
from pathlib import Path

MODEL = os.path.expanduser("~/.whisper-models/ggml-small.bin")
WHISPER = "/opt/homebrew/bin/whisper-cli"

def main():
    parser = argparse.ArgumentParser(description="一键本地音视频转文字")
    parser.add_argument("filepath", help="本地音频或视频文件的路径")
    args = parser.parse_args()

    input_path = Path(args.filepath).expanduser().resolve()
    if not input_path.exists():
        print(f"❌ 找不到指定文件: {input_path}")
        sys.exit(1)

    if not os.path.exists(MODEL):
        print(f"❌ 模型文件不存在: {MODEL}")
        sys.exit(1)

    output_dir = input_path.parent
    expected_txt = output_dir / f"{input_path.stem}.txt"

    print(f"\n📝 目标文件: {input_path.name}")
    print(f"⚡ 正在转码音频...")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        temp_wav = f.name

    subprocess.run([
        "ffmpeg", "-y", "-i", str(input_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        temp_wav
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"📥 开始转录文字...\n")

    result = subprocess.run([
        WHISPER, "-m", MODEL, "-f", temp_wav,
        "-l", "zh", "-otxt", "-of", str(output_dir / input_path.stem)
    ])

    if os.path.exists(temp_wav):
        os.remove(temp_wav)

    if result.returncode == 0 and expected_txt.exists():
        print(f"\n✅ 搞定！文字稿: {expected_txt}")
    else:
        print(f"\n❌ 转录异常中断 (退出码: {result.returncode})")

if __name__ == "__main__":
    main()
