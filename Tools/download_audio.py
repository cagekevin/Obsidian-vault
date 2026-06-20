#!/usr/bin/env python3
"""
YouTube / B站 音频/视频下载工具
依赖: yt-dlp, ffmpeg
安装: brew install yt-dlp ffmpeg (Mac) / choco install yt-dlp ffmpeg (Win)
出错只有两个原因：1. 软件没更新  2. Cookie 问题（浏览器没登录）

用法:
  python3 download_audio.py "https://youtu.be/xxx"              # 下载音频（默认 mp3）
  python3 download_audio.py "https://www.bilibili.com/xxx"      # 下载B站音频
  python3 download_audio.py "https://youtu.be/xxx" --mp4        # 下载视频（mp4）
  python3 download_audio.py "歌名"                               # 搜索YouTube音频
  python3 download_audio.py "歌名1" "歌名2"                      # 批量下载
  python3 download_audio.py --batch songs.txt                   # 从文件读取
  python3 download_audio.py "歌名" --format m4a                 # 指定格式
  python3 download_audio.py "歌名" --output-dir ~/Music         # 指定保存目录
"""
import subprocess
import sys
import os
import shutil
import argparse

def check_dependencies():
    missing = []
    if not shutil.which("yt-dlp"):
        missing.append("yt-dlp")
    if not shutil.which("ffmpeg"):
        missing.append("ffmpeg")
    if missing:
        print(f"❌ 缺少依赖: {', '.join(missing)}")
        print("Mac: brew install yt-dlp ffmpeg")
        sys.exit(1)

def get_output_dir():
    if sys.platform == "win32":
        music_dir = os.path.join("G:", os.sep, "music")
    else:
        music_dir = os.path.expanduser("~/Documents/music")
    os.makedirs(music_dir, exist_ok=True)
    return music_dir

def add_to_apple_music(filepath):
    if sys.platform != "darwin":
        return False
    auto_add = os.path.expanduser("~/Music/Music/Media.localized/Automatically Add to Music.localized")
    if os.path.isdir(auto_add):
        shutil.copy2(filepath, auto_add)
        return True
    return False

def download_audio(query, output_dir, audio_format="best", download_video=False):
    """下载音频或视频。音频按优先级自动降级：mp3 → m4a → best"""
    is_url = query.startswith("http://") or query.startswith("https://")

    if is_url:
        url = query
    else:
        url = f"ytsearch:{query}"

    if download_video:
        # 视频模式：下载 mp4，不需要降级
        cmd = ["yt-dlp"]
        cmd.extend(["--cookies-from-browser", "edge"])
        cmd.extend(["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"])
        cmd.extend(["-P", output_dir, "-o", "%(title)s.%(ext)s"])
        cmd.extend(["--no-playlist", "--embed-thumbnail", "--add-metadata", "--clean-infojson"])
        if not is_url:
            cmd.extend(["--max-downloads", "1"])
        cmd.append(url)

        result = subprocess.run(cmd, capture_output=True, text=True)
        output_lines = result.stdout.strip().split("\n")
        for line in output_lines:
            line = line.strip()
            if line.endswith(".mp4") and os.path.exists(line):
                size = os.path.getsize(line)
                print(f"📁 {os.path.basename(line)} ({size/1024/1024:.1f} MB)")
                return True
        return False

    # 音频模式：按优先级尝试格式
    formats_to_try = [audio_format]
    if audio_format == "best":
        formats_to_try = ["mp3", "m4a", "best"]
    elif audio_format == "m4a":
        formats_to_try = ["m4a", "mp3"]
    elif audio_format == "mp3":
        formats_to_try = ["mp3", "m4a"]

    for fmt in formats_to_try:
        cmd = ["yt-dlp"]
        cmd.extend(["--cookies-from-browser", "edge"])
        cmd.extend(["-x", "--audio-format", fmt, "--audio-quality", "0"])
        cmd.extend(["-P", output_dir, "-o", "%(title)s.%(ext)s"])
        cmd.extend(["--no-playlist", "--embed-thumbnail", "--add-metadata", "--clean-infojson"])
        if not is_url:
            cmd.extend(["--max-downloads", "1"])
        cmd.append(url)

        result = subprocess.run(cmd, capture_output=True, text=True)

        # 检查是否下载成功
        output_lines = result.stdout.strip().split("\n")
        for ext in [f".{fmt}", ".m4a", ".mp3", ".opus"]:
            for line in output_lines:
                line = line.strip()
                if line.endswith(ext) and os.path.exists(line):
                    size = os.path.getsize(line)
                    print(f"📁 {os.path.basename(line)} ({size/1024/1024:.1f} MB)")
                    add_to_apple_music(line)
                    return True

        # 失败则记录错误，继续尝试下一个格式
        last_error = result.stderr[:200] if result.stderr else "格式不支持"

    print(f"❌ 下载失败（尝试了 {', '.join(formats_to_try)} 格式）")
    return False

def main():
    parser = argparse.ArgumentParser(description="🎵 YouTube / B站 音频/视频下载工具")
    parser.add_argument("query", nargs="*", help="视频URL 或 搜索关键词")
    parser.add_argument("--batch", help="从文本文件读取（每行一首）")
    parser.add_argument("--output-dir", default=get_output_dir(), help="保存目录")
    parser.add_argument("--format", default="best", choices=["best", "aac", "flac", "m4a", "mp3", "opus", "wav"],
                        help="音频格式（默认 best，自动降级）")
    parser.add_argument("--mp4", action="store_true", help="下载视频（mp4 格式）")

    args = parser.parse_args()
    check_dependencies()

    queries = []
    if args.batch:
        with open(args.batch, "r", encoding="utf-8") as f:
            queries = [line.strip() for line in f if line.strip()]
    elif args.query:
        queries = args.query
    else:
        parser.print_help()
        sys.exit(1)

    total = len(queries)
    success_count = 0
    for i, q in enumerate(queries, 1):
        print(f"\n{'='*50}")
        print(f"[{i}/{total}] {q}")
        print(f"{'='*50}")
        try:
            if download_audio(q, args.output_dir, args.format, args.mp4):
                success_count += 1
            else:
                print(f"❌ 失败: {q}")
        except Exception as e:
            print(f"💥 异常: {e}")

    print(f"\n{'='*50}")
    print(f"🎉 完成！成功 {success_count}/{total}")
    print(f"📂 {args.output_dir}")

if __name__ == "__main__":
    main()
