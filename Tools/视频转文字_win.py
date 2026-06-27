#!/usr/bin/env python3
"""
极简视频/音频转文字工具 (faster-whisper 版 · Windows 专用)
============================================================
依赖: pip install faster-whisper  (已全局安装)

用法:
  python 视频转文字_win.py <文件路径>              单文件
  python 视频转文字_win.py <文件夹路径>            批量转整个文件夹
  python 视频转文字_win.py <路径> --model large-v3  指定模型（默认 small）

模型大小参考:
  tiny    ~75MB  最快，精度一般
  base   ~150MB
  small  ~500MB  推荐，平衡速度和精度
  medium ~1.5GB  更准，稍慢
  large-v3 ~3GB  最准，慢

首次运行会自动从 HuggingFace 下载模型到:
  C:\\Users\\<用户名>\\.cache\\huggingface\\hub\\
"""

import argparse
import os
import sys
import time
from pathlib import Path

# 支持的视频/音频格式
MEDIA_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm",
              ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma"}


def transcribe(file_path: Path, model_name: str = "small", language: str = "zh"):
    """转写单个文件，输出 .txt + .srt"""
    from faster_whisper import WhisperModel

    print(f"\n🎤 加载模型: {model_name} ...")
    # 用 CPU，Windows 上最兼容；有 NVIDIA 卡可加 device="cuda"
    model = WhisperModel(model_name, device="cpu", compute_type="int8")

    print(f"📂 正在转写: {file_path.name}")
    start = time.time()

    segments, info = model.transcribe(str(file_path), language=language, beam_size=5)

    # 收集结果
    texts = []
    srt_lines = []
    for i, seg in enumerate(segments, 1):
        texts.append(seg.text.strip())
        # SRT 格式
        start_s = _srt_time(seg.start)
        end_s = _srt_time(seg.end)
        srt_lines.append(f"{i}\n{start_s} --> {end_s}\n{seg.text.strip()}\n")

    duration = time.time() - start

    # 写入 .txt（纯文字稿）
    txt_path = file_path.with_suffix(".txt")
    txt_path.write_text("\n".join(texts), encoding="utf-8")

    # 写入 .srt（带时间轴的字幕）
    srt_path = file_path.with_suffix(".srt")
    srt_path.write_text("\n".join(srt_lines), encoding="utf-8")

    print(f"✅ 完成！耗时 {duration:.1f} 秒")
    print(f"   📄 文字稿: {txt_path}")
    print(f"   🎬 字幕:   {srt_path}")
    print(f"   📝 {len(texts)} 条 | 检测语言: {info.language} (概率 {info.language_probability:.0%})")


def _srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def main():
    parser = argparse.ArgumentParser(description="视频/音频转文字 (faster-whisper)")
    parser.add_argument("path", help="文件或文件夹路径")
    parser.add_argument("--model", default="small",
                        choices=["tiny", "base", "small", "medium", "large-v3"],
                        help="Whisper 模型大小 (默认 small)")
    parser.add_argument("--lang", default="zh",
                        help="语言代码，如 zh/en/ja (默认 zh)")
    args = parser.parse_args()

    input_path = Path(args.path)
    if not input_path.exists():
        print(f"❌ 找不到路径: {args.path}")
        sys.exit(1)

    if input_path.is_file():
        transcribe(input_path, args.model, args.lang)
    else:
        # 文件夹：批量处理
        files = sorted([f for f in input_path.iterdir()
                       if f.suffix.lower() in MEDIA_EXTS])
        if not files:
            print(f"❌ 文件夹中没有找到视频/音频文件")
            sys.exit(1)

        print(f"📁 找到 {len(files)} 个文件，开始批量转写...")
        for f in files:
            transcribe(f, args.model, args.lang)
        print(f"\n🎉 全部完成！共处理 {len(files)} 个文件")


if __name__ == "__main__":
    main()
