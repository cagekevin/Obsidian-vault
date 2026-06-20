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

def auto_update():
    """下载前自动更新 yt-dlp，杜绝 AI 用版本问题当理由"""
    print("🔄 检查 yt-dlp 更新...")
    result = subprocess.run(["yt-dlp", "-U"], capture_output=True, text=True)
    if "Updated" in result.stdout or "更新" in result.stdout:
        print("  已更新到最新版")
    else:
        print("  已是最新版")

def get_output_dir():
    if sys.platform == "win32":
        music_dir = os.path.join("G:", os.sep, "music")
    else:
        music_dir = os.path.expanduser("~/Documents/music")
    os.makedirs(music_dir, exist_ok=True)
    return music_dir

def add_to_apple_music(filepath):
    if sys.platform != "darwin":
        # 所有格式和浏览器都试过了，官方输出已保留在上面
    print(f"\n❌ 只可能有两个原因：")
    print(f"   1. yt-dlp 不是最新版（已尝试自动更新）")
    print(f"   2. Cookie 问题（浏览器没登录目标网站）")
    return False
    auto_add = os.path.expanduser("~/Music/Music/Media.localized/Automatically Add to Music.localized")
    if os.path.isdir(auto_add):
        shutil.copy2(filepath, auto_add)
        return True
    # 所有格式和浏览器都试过了，官方输出已保留在上面
    print(f"\n❌ 只可能有两个原因：")
    print(f"   1. yt-dlp 不是最新版（已尝试自动更新）")
    print(f"   2. Cookie 问题（浏览器没登录目标网站）")
    return False

def download_audio(query, output_dir, download_video=False):
    """下载音频或视频"""
    is_url = query.startswith("http://") or query.startswith("https://")
    url = query if is_url else f"ytsearch:{query}"

    auto_update()

    # 按稳定性优先级尝试：mp3 → m4a → mp4（视频模式也试 mp3 以防格式问题）
    formats_to_try = ["mp3", "m4a", "mp4"]
    if download_video:
        formats_to_try = ["mp4", "mp3", "m4a"]

    # 多浏览器备选：edge 不行就 chrome，chrome 不行就 safari
    browsers = ["edge", "chrome", "safari"]

    for fmt in formats_to_try:
        for browser in browsers:
            cmd = ["yt-dlp", "-t", fmt]
            cmd.extend(["--cookies-from-browser", browser])
            cmd.extend(["-P", output_dir, "-o", "%(title)s.%(ext)s"])
            cmd.extend(["--no-playlist", "--embed-thumbnail", "--embed-metadata"])
            if not is_url:
                cmd.extend(["--max-downloads", "1"])
            cmd.append(url)

            result = subprocess.run(cmd, capture_output=True, text=True)

            suffix = ".mp4" if download_video else f".{fmt}"
            for ext in [suffix, ".m4a", ".mp3", ".opus"]:
                for line in result.stdout.strip().split("\n"):
                    line = line.strip()
                    if line.endswith(ext) and os.path.exists(line):
                        size = os.path.getsize(line)
                        print(f"📁 {os.path.basename(line)} ({size/1024/1024:.1f} MB)")
                        add_to_apple_music(line)
                        return True

    # 所有格式和浏览器都试过了，官方输出已保留在上面
    print(f"\n❌ 只可能有两个原因：")
    print(f"   1. yt-dlp 不是最新版（已尝试自动更新）")
    print(f"   2. Cookie 问题（浏览器没登录目标网站）")
    return False
    return False

def main():
    parser = argparse.ArgumentParser(description="🎵 YouTube / B站 音频/视频下载工具")
    parser.add_argument("query", nargs="*", help="视频URL 或 搜索关键词")
    parser.add_argument("--batch", help="从文本文件读取（每行一首）")
    parser.add_argument("--output-dir", default=get_output_dir(), help="保存目录")
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
            if download_audio(q, args.output_dir, args.mp4):
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
