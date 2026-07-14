#!/usr/bin/env python3
"""
YouTube / B站 音频/视频下载工具
依赖: yt-dlp, ffmpeg
安装: brew install yt-dlp ffmpeg (Mac) / choco install yt-dlp ffmpeg (Win)
出错只有两个原因：1. 软件没更新  2. Cookie 问题（浏览器没登录）

禁止 AI 主动修改 PY 脚本
禁止 AI 主动修改 PY 脚本
禁止 AI 主动修改 PY 脚本！！！！

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
        print(f"\n❌ 只可能有两个原因：")
        print(f"   1. yt-dlp 不是最新版（已尝试自动更新）")
        print(f"   2. Cookie 问题（浏览器没登录目标网站）")
        return False
    auto_add = os.path.expanduser("~/Music/Music/Media.localized/Automatically Add to Music.localized")
    if os.path.isdir(auto_add):
        shutil.copy2(filepath, auto_add)
        return True
    print(f"\n❌ 只可能有两个原因：")
    print(f"   1. yt-dlp 不是最新版（已尝试自动更新）")
    print(f"   2. Cookie 问题（浏览器没登录目标网站）")
    return False

def download_audio(query, output_dir, download_video=False, cookie_file=""):
    """下载音频或视频"""
    is_url = query.startswith("http://") or query.startswith("https://")
    url = query if is_url else f"ytsearch:{query}"

    auto_update()

    # 如果提供了 cookie 文件，直接用文件（优先级最高）
    if cookie_file and os.path.isfile(cookie_file):
        fmt = "mp4" if download_video else "mp3"
        cmd = ["yt-dlp", "-t", fmt]
        cmd.extend(["--cookies", cookie_file, "--js-runtimes", "node"])
        cmd.extend(["-P", output_dir, "-o", "%(title)s.%(ext)s"])
        cmd.extend(["--no-playlist", "--embed-thumbnail", "--embed-metadata"])
        if not is_url:
            cmd.extend(["--max-downloads", "1"])
        cmd.append(url)

        print(f"  使用 Cookie 文件: {cookie_file}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"  yt-dlp RC={result.returncode}")
        if result.stderr.strip():
            for line in result.stderr.strip().split("\n")[-3:]:
                print(f"  [yt-dlp] {line}")

        # 检测方式：扫描输出目录找最新非空 mp4/mkv 文件
        if result.returncode == 0:
            suffix = ".mp4" if download_video else f".{fmt}"
            exts_to_check = [suffix, ".mkv", ".webm", ".m4a", ".mp3", ".opus"]
            # 取输出目录中修改时间最新的文件
            latest = None
            latest_mtime = 0
            for fname in os.listdir(output_dir):
                fpath = os.path.join(output_dir, fname)
                if os.path.isfile(fpath) and any(fname.lower().endswith(e) for e in exts_to_check):
                    mtime = os.path.getmtime(fpath)
                    if mtime > latest_mtime:
                        latest_mtime = mtime
                        latest = fpath
            if latest and os.path.getsize(latest) > 1024 * 1024:  # >1MB 排除封面图
                size_mb = os.path.getsize(latest) / 1024 / 1024
                print(f"📁 {os.path.basename(latest)} ({size_mb:.1f} MB)")
                add_to_apple_music(latest)
                return True
        # cookie 文件失败时 fallthrough 到浏览器模式

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

            if result.returncode == 0:
                suffix = ".mp4" if download_video else f".{fmt}"
                exts_to_check = [suffix, ".mkv", ".webm", ".m4a", ".mp3", ".opus"]
                latest = None
                latest_mtime = 0
                for fname in os.listdir(output_dir):
                    fpath = os.path.join(output_dir, fname)
                    if os.path.isfile(fpath) and any(fname.lower().endswith(e) for e in exts_to_check):
                        mtime = os.path.getmtime(fpath)
                        if mtime > latest_mtime:
                            latest_mtime = mtime
                            latest = fpath
                if latest and os.path.getsize(latest) > 1024 * 1024:
                    size_mb = os.path.getsize(latest) / 1024 / 1024
                    print(f"📁 {os.path.basename(latest)} ({size_mb:.1f} MB)")
                    add_to_apple_music(latest)
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
    parser.add_argument("--cookie-file", help="指定 Netscape 格式的 Cookie 文件路径")

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
            if download_audio(q, args.output_dir, args.mp4, args.cookie_file):
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
