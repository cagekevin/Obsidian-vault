#!/usr/bin/env python3
"""
视频/音频转文字工具 (OpenAI Whisper · GPU 加速)
================================================
用已安装的 torch CUDA 跑 GPU 加速，不额外装任何包。

用法:
  python 视频转文字_win.py <文件路径>              单文件
  python 视频转文字_win.py <文件夹路径>            批量转整个文件夹

模型: tiny (~150MB) 最快，中文够用。首次运行自动下载。
"""

import argparse
import sys
import time
import torch
from pathlib import Path

MEDIA_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm",
              ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma"}


def transcribe(file_path: Path, model_name: str = "tiny", language: str = "zh"):
    import whisper

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n🎤 加载模型: {model_name} (设备: {device.upper()}) ...")
    model = whisper.load_model(model_name, device=device)

    print(f"📂 正在转写: {file_path.name}")
    start = time.time()
    result = model.transcribe(str(file_path), language=language)
    duration = time.time() - start

    # 写入 .txt
    txt_path = file_path.with_suffix(".txt")
    txt_path.write_text(result["text"].strip(), encoding="utf-8")

    # 写入 .srt
    srt_path = file_path.with_suffix(".srt")
    srt_lines = []
    for i, seg in enumerate(result["segments"], 1):
        s = _srt_time(seg["start"])
        e = _srt_time(seg["end"])
        srt_lines.append(f"{i}\n{s} --> {e}\n{seg['text'].strip()}\n")
    srt_path.write_text("\n".join(srt_lines), encoding="utf-8")

    print(f"✅ 完成！耗时 {duration:.1f} 秒")
    print(f"   📄 文字稿: {txt_path}")
    print(f"   🎬 字幕:   {srt_path}")
    print(f"   📝 {len(result['segments'])} 条")


def _srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def main():
    parser = argparse.ArgumentParser(description="视频/音频转文字 (OpenAI Whisper)")
    parser.add_argument("path", help="文件或文件夹路径")
    parser.add_argument("--model", default="tiny",
                        choices=["tiny", "base", "small"],
                        help="模型大小 (默认 tiny)")
    parser.add_argument("--lang", default="zh", help="语言代码 (默认 zh)")
    args = parser.parse_args()

    input_path = Path(args.path)
    if not input_path.exists():
        print(f"❌ 找不到路径: {args.path}")
        sys.exit(1)

    if input_path.is_file():
        transcribe(input_path, args.model, args.lang)
    else:
        files = sorted([f for f in input_path.iterdir()
                       if f.suffix.lower() in MEDIA_EXTS])
        if not files:
            print("❌ 文件夹中没有找到视频/音频文件")
            sys.exit(1)

        pending = [f for f in files if not f.with_suffix(".txt").exists()]
        skipped = len(files) - len(pending)
        if skipped:
            print(f"⏭️  跳过 {skipped} 个已处理的文件")
        if not pending:
            print("✅ 全部已完成，无需处理")
            return

        print(f"📁 待处理 {len(pending)} 个文件，开始批量转写...")
        for f in pending:
            transcribe(f, args.model, args.lang)
        print(f"\n🎉 全部完成！共处理 {len(pending)} 个文件")


if __name__ == "__main__":
    main()
