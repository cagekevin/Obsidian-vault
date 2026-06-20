#!/usr/bin/env python3
"""
TTS 配音 — AnaNeural 可爱卡通 · 1.2倍速
用法:
  python tools/tts/run.py "Hello" -o out.mp3
  python tools/tts/run.py -f 台词.txt -o 配音.mp3
  python tools/tts/run.py --list-voices
"""
import sys, subprocess, os, re, tempfile

VOICE = "en-US-AnaNeural"
RATE  = "+20%"

def main():
    args = sys.argv[1:]
    if not args or "-h" in args or "--help" in args:
        print(__doc__); return
    if "--list-voices" in args:
        subprocess.run([sys.executable, "-m", "edge_tts", "--list-voices"])
        return

    text = None
    output = "output.mp3"
    voice, rate = VOICE, RATE
    i = 0
    while i < len(args):
        if args[i] == "-o" and i+1 < len(args):          i += 1; output = args[i]
        elif args[i] == "--voice" and i+1 < len(args):   i += 1; voice = args[i]
        elif args[i] == "--rate" and i+1 < len(args):    i += 1; rate = args[i]
        elif args[i] == "-f" and i+1 < len(args):
            i += 1
            p = args[i]
            if os.path.isfile(p):
                txt = open(p, encoding="utf-8").read()
                text = re.sub(r'\n\s*\n', ' ', txt).replace('\n', ' ').strip()
            else:
                print(f"❌ 找不到文件: {p}"); return
        elif text is None:
            text = args[i]
        i += 1

    if not text:
        print("❌ 未指定文字内容"); return

    # 写临时文件，避免命令行特殊字符问题
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8")
    tmp.write(text)
    tmp.close()

    cmd = [sys.executable, "-m", "edge_tts",
           "--voice", voice, "--rate", rate,
           "-f", tmp.name,
           "--write-media", output]
    print(f"🎤 {voice}  1.2x ({rate})")
    r = subprocess.run(cmd, capture_output=True, text=True)
    os.unlink(tmp.name)

    if os.path.exists(output) and os.path.getsize(output) > 0:
        print(f"✅ {output}  ({os.path.getsize(output)/1024:.0f}KB)")
    else:
        err = (r.stderr or "").strip()
        print(f"❌ 失败: {err[:200] if err else '未知错误'}")

if __name__ == "__main__":
    main()
