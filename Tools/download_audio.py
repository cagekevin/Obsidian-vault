#!/usr/bin/env python3
"""
YouTube / B站 音频下载工具
依赖: yt-dlp, ffmpeg (遇到问题先确保是最新版本，有没有使用cookie，只有这两个原因，禁止其他任何行为)
安装: brew install yt-dlp ffmpeg (Mac) / choco install yt-dlp ffmpeg (Win)

用法:
  python3 download_audio.py "视频URL或搜索关键词"
  python3 download_audio.py "I'm Just Your Type"          # 搜索并下载
  python3 download_audio.py "https://youtu.be/xxx"         # 直接下载URL
  python3 download_audio.py "https://www.bilibili.com/xxx" # 下载B站视频

批量下载（传多个歌名，自动排队）:
  python3 download_audio.py "歌名1" "歌名2" "歌名3"
  python3 download_audio.py --batch songs.txt   # 从文本文件读取歌名，每行一首

可选参数:
  --output-dir DIR    保存目录 (默认: ~/Documents/music 或 G:\\music)
  --format FORMAT     音频格式 mp3/m4a/opus (默认: mp3)
"""

import subprocess
import sys
import os
import shutil
import argparse
import time
import shlex

def check_dependencies():
    """检查 yt-dlp 和 ffmpeg 是否已安装"""
    missing = []
    if not shutil.which("yt-dlp"):
        missing.append("yt-dlp")
    if not shutil.which("ffmpeg"):
        missing.append("ffmpeg")
    
    if missing:
        print(f"❌ 缺少依赖: {', '.join(missing)}")
        print("Mac 请运行: brew install yt-dlp ffmpeg")
        print("Win 请运行: pip install yt-dlp / choco install ffmpeg")
        sys.exit(1)

def get_output_dir():
    """根据平台确定默认输出目录
    Mac 默认 ~/Documents/music（下载音乐用）。
    如需转文字，指定 --output-dir ~/Documents/Obsidian\ vault/Temp"""
    if sys.platform == "win32":
        music_dir = os.path.join("G:", os.sep, "music")
    else:
        music_dir = os.path.expanduser("~/Documents/music")
    os.makedirs(music_dir, exist_ok=True)
    return music_dir

def get_ytdl_extra_args(source="youtube", is_url=False):
    """返回特定平台的额外参数"""
    args = []
    if sys.platform == "win32":
        cookie = os.path.join(os.path.expanduser("~"), ".config", "yt-dlp", "youtube_cookies.txt")
        if os.path.exists(cookie):
            args.extend(["--cookies", cookie])
    elif sys.platform == "darwin":
        # Mac: 从 Edge 浏览器读取 cookie（绕过 YouTube bot 检测）
        args.extend(["--cookies-from-browser", "edge"])
        
    return args

def add_to_apple_music(filepath):
    """macOS: 复制 MP3 到 Apple Music 自动添加目录"""
    if sys.platform != "darwin":
        return False
    auto_add = os.path.expanduser("~/Music/Music/Media.localized/Automatically Add to Music.localized")
    if os.path.isdir(auto_add):
        shutil.copy2(filepath, auto_add)
        return True
    return False

def download_audio(query, output_dir, audio_format="mp3", source="youtube"):
    """下载音频"""
    is_url = query.startswith("http://") or query.startswith("https://")
    
    # 判断是 URL 还是搜索关键词
    if is_url:
        url = query
        print(f"🔗 URL: {url}")
        actual_source = "youtube" if "youtu" in query else source 
    else:
        if source == "bilibili":
            url = f"bilisearch:{query}"
            print(f"🔍 从 B站 搜索: {query}")
        else:
            url = f"ytsearch:{query}"
            print(f"🔍 从 YouTube 搜索: {query}")
        actual_source = source

    print(f"📂 保存到: {output_dir}")
    print("\n⏳ 正在下载，请稍候...\n")
    
    cmd = [
        "yt-dlp",
        *get_ytdl_extra_args(actual_source, is_url),
        "-x",
        "--audio-format", audio_format,
        "--audio-quality", "0",
        "-P", output_dir,
        "-o", "%(title)s.%(ext)s",
        "--no-playlist",
        "--embed-thumbnail",
        "--add-metadata",
        "--clean-infojson",
        "--print", "filename"
    ]
    
    # 搜索模式限制只下载第一个结果；URL 模式不需要
    if not is_url:
        cmd.extend(["--max-downloads", "1"])
    
    # B站防 412 拦截的核心参数：带上浏览器身份
    # （如果你用的是 Safari，请把下面这行的 chrome 改成 safari）
    if actual_source == "bilibili" or (is_url and "bilibili.com" in url):
        pass  # cookie 已在 get_ytdl_extra_args 中统一添加

    cmd.append(url)
    
    # 打印底层执行命令，方便你直接复制去终端排错
    safe_cmd = shlex.join(cmd)
    print(f"🛠️  [底层命令] {safe_cmd}\n")
    print(f"📥 开始传输...\n")
    
    # 核心修改：不捕获任何输出！
    # 直接运行，yt-dlp 原始的进度条和真实报错会原封不动地砸在你的终端屏幕上
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # 从 --print filename 的输出获取实际生成的文件路径
    # yt-dlp 可能先输出中间格式（如 .m4a），再转成目标格式（如 .mp3）
    # 所以同时检查目标格式和常见中间格式
    output_lines = result.stdout.strip().split("\n")
    downloaded_file = None
    for line in output_lines:
        line = line.strip()
        if line.endswith(f".{audio_format}") and os.path.exists(line):
            downloaded_file = line
            break
    # 如果目标格式没找到，检查中间格式（如 .m4a）
    if not downloaded_file:
        for ext in ["m4a", "opus"]:
            if ext == audio_format:
                continue
            for line in output_lines:
                line = line.strip()
                if line.endswith(f".{ext}") and os.path.exists(line):
                    downloaded_file = line
                    break
            if downloaded_file:
                break
    
    if downloaded_file:
        size = os.path.getsize(downloaded_file)
        print(f"\n📁 成功生成: {os.path.basename(downloaded_file)}")
        print(f"📏 文件大小: {size / 1024 / 1024:.1f} MB")
        if add_to_apple_music(downloaded_file):
            print(f"🎵 已自动添加到 Apple Music")
        return True
            
    return False

def main():
    parser = argparse.ArgumentParser(
        description="🎵 YouTube / B站 音频下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s "I'm Just Your Type"           # 搜索并下载
  %(prog)s "https://youtu.be/xxx"          # 直接下载URL
  %(prog)s "https://www.bilibili.com/xxx"  # 下载B站视频
  %(prog)s "歌名1" "歌名2" "歌名3"         # 批量下载
  %(prog)s --batch songs.txt               # 从文件读取歌名
  %(prog)s "歌名" --format m4a             # 下载 m4a 格式
  %(prog)s "歌名" --source bilibili        # 从B站搜索
  %(prog)s "歌名" --output-dir ~/Music     # 保存到指定目录
        """
    )
    parser.add_argument("query", nargs="*", help="视频URL 或 搜索关键词（支持多个）")
    parser.add_argument("--batch", help="从文本文件读取歌名列表（每行一首）")
    parser.add_argument("--output-dir", default=get_output_dir(),
                       help=f"保存目录 (默认: 自动判断系统目录)")
    parser.add_argument("--source", default="youtube",
                       choices=["youtube", "bilibili"],
                       help="搜索来源 (默认: youtube)")
    parser.add_argument("--format", default="mp3",
                       choices=["mp3", "m4a", "opus"],
                       help="音频格式 (默认: mp3)")
    
    args = parser.parse_args()
    
    check_dependencies()

    # 收集所有待下载的歌曲名
    queries = []
    if args.batch:
        with open(args.batch, "r", encoding="utf-8") as f:
            queries = [line.strip() for line in f if line.strip()]
        print(f"📋 从文件读取了 {len(queries)} 首歌")
    elif args.query:
        queries = args.query
    else:
        parser.print_help()
        sys.exit(1)

    # 逐个下载
    total = len(queries)
    for i, q in enumerate(queries, 1):
        print(f"\n{'='*50}")
        print(f"[{i}/{total}] 正在处理: {q}")
        print(f"{'='*50}")
        try:
            success = download_audio(q, args.output_dir, args.format, args.source)
            if not success:
                print(f"⚠️  [{i}/{total}] '{q}' 抓取失败。")
        except KeyboardInterrupt:
            print(f"\n🛑 用户强行中断。")
            break
        except SystemExit:
            print(f"⚠️  [{i}/{total}] '{q}' 下载遇到系统退出信号，跳过...")
        except Exception as e:
            print(f"💥 未知异常: {e}")
    
    print(f"\n{'='*50}")
    print(f"🎉 队列处理完成！")
    print(f"📂 保存目录: {args.output_dir}")

if __name__ == "__main__":
    main()