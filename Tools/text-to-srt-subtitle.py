#!/usr/bin/env python3
"""
将纯文本字幕文件转换为 SRT 格式，智能分配每条字幕时长。

一句话用法：
    python text-to-srt-subtitle.py 字幕.txt --total 秒数

唯一必填参数：字幕文件路径。
最常用参数：--total 视频总秒数（自动按文本长短分配时长并精准对齐总时长）。

示例：
    # 1分钟视频，自动分配时长
    python text-to-srt-subtitle.py 旁白.txt --total 60

    # 30秒视频
    python text-to-srt-subtitle.py 旁白.txt --total 30

    # 自定义阅读速度（数字越小越慢，默认自动推算）
    python text-to-srt-subtitle.py 旁白.txt --total 60 --speed 4

    # 自定义每条固定时长（不智能，不推荐）
    python text-to-srt-subtitle.py 旁白.txt --duration 3

    # 输出到指定路径
    python text-to-srt-subtitle.py 旁白.txt --total 60 -o 输出.srt

输入格式：每行一条字幕，无时间标记，纯文本。

智能时长规则（AI 无需读代码，看这里即可）：
- 中文字：每个算 1 单位
- 英文词：每个算 1 单位
- 逗号顿号破折号：各 +0.5 单位（意群停顿）
- 句号感叹号问号省略号：各 +1.0 单位（语句结束停顿）
- 超短句不低于 1.5 秒，长句不低于 2.5 秒
- 指定 --total 后自动等比缩放对齐总时长
"""

import sys, math
from pathlib import Path
import re


def parse_time(t):
    t = t.strip()
    m = re.match(r'^(\d+):(\d+):(\d+)$', t)
    if m: return int(m.group(1))*3600 + int(m.group(2))*60 + int(m.group(3))
    m = re.match(r'^(\d+):(\d+)$', t)
    if m: return int(m.group(1))*60 + int(m.group(2))
    try: return float(t)
    except: return None


def to_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def estimate_duration(text, speed):
    """
    智能时长估算：
    - 中文字每个 1 单位
    - 英文单词每个 0.5 单位（阅读速度更快）
    - 逗号/顿号/破折号 各 +0.5 单位（意群停顿）
    - 句号/感叹号/问号/省略号 各 +1.0 单位（语句结束停顿）
    - 最短 1.5s，最长由 speed 倒推确保不超
    """
    if not speed:
        return None

    # 基础：中文字 + 英文词（每个英文词 ≈ 1 个中文字阅读时间）
    cn = len(re.findall(r"[\u4e00-\u9fff]", text))
    en_words = len(re.findall(r"[a-zA-Z]+", text))
    base_unit = cn + en_words * 1.0

    # 标点停顿加权
    pauses = len(re.findall(r"[，、—]", text)) * 0.5
    stops = len(re.findall(r"[。！？…]", text)) * 1.0

    total_unit = base_unit + pauses + stops
    raw = total_unit / speed if speed else 3.0

    # 智能上下限: 短句不低于 1.5s，长句不赶
    # 根据总字数动态决定上限
    total_chars = len(text)
    if total_chars <= 8:
        minimum = 1.5
    elif total_chars <= 15:
        minimum = 2.0
    else:
        minimum = 2.5

    dur = max(minimum, raw)
    return dur


def main():
    args = sys.argv[1:]
    if not args or "-h" in args:
        print(__doc__)
        sys.exit(1)

    duration = 3.0      # 默认每条3秒
    max_duration = 8.0  # 默认最长8秒
    speed = None        # 默认不启动自适应
    offset = 0.0
    total = None        # 视频总长
    content = None
    content_source = None
    output = None

    i = 0
    while i < len(args):
        if args[i] == "--duration" and i + 1 < len(args):
            i += 1; duration = float(args[i])
        elif args[i] == "--max-duration" and i + 1 < len(args):
            i += 1; max_duration = float(args[i])
        elif args[i] == "--speed" and i + 1 < len(args):
            i += 1; speed = float(args[i])
        elif args[i] == "--total" and i + 1 < len(args):
            i += 1; total = float(args[i])
        elif args[i] == "--offset" and i + 1 < len(args):
            i += 1; offset = float(args[i])
        elif args[i] == "-o" and i + 1 < len(args):
            i += 1; output = args[i]
        elif args[i] == "--stdin":
            content = sys.stdin.read()
        elif content is None:
            p = Path(args[i])
            if p.exists():
                content_source = str(p)
                content = p.read_text(encoding="utf-8")
            else:
                content = args[i]
        i += 1

    if not content:
        print("❌ 未指定输入"); sys.exit(1)

    lines = [l.strip() for l in content.strip().split("\n") if l.strip()]

    # 解析行: 有时间标记的 / 纯文本
    items = []
    for line in lines:
        m = re.match(r'^([\d:\.]+)\s+(.+)$', line)
        if m:
            t = parse_time(m.group(1))
            if t is not None:
                items.append((t, m.group(2)))
                continue
        items.append((None, line))

    # --- 第一轮：计算每条字幕的原始时长 ---
    raw_durations = []
    for t, text in items:
        if t is not None:
            raw_durations.append(duration)
        elif speed:
            est = estimate_duration(text, speed)
            raw_durations.append(min(est, max_duration) if max_duration else est)
        else:
            # 未指定 speed 时，按内容估算（默认阅读速度 ≈ 5 单位/秒）
            est = estimate_duration(text, 5)
            raw_durations.append(min(est, max_duration) if max_duration else est)

    # --- 方案1：--total 等比缩放 ---
    # 当指定了 total 且没给显式时间标记时，将所有字幕等比缩放对齐总时长
    if total is not None and not any(t is not None for t, _ in items):
        raw_total = sum(raw_durations)
        if raw_total > 0 and abs(raw_total - total) > 0.1:
            scale = total / raw_total
            raw_durations = [d * scale for d in raw_durations]

    # --- 第二轮：生成 SRT ---
    srt_parts = []
    current_time = offset

    for idx, ((t, text), dur) in enumerate(zip(items, raw_durations), 1):
        if t is not None:
            start = t + offset
            # 如果有下一条时间标记，防重叠
            if idx < len(items) and items[idx][0] is not None:
                next_start = items[idx][0] + offset
                max_end = next_start - 0.001
                if start + dur > max_end:
                    dur = max(1.0, max_end - start)
        else:
            start = current_time

        end = start + dur
        srt_parts.append(f"{idx}\n{to_srt_time(start)} --> {to_srt_time(end)}\n{text}\n")
        current_time = end

    srt_content = "\n".join(srt_parts)

    if not output:
        if content_source and Path(content_source).suffix != ".srt":
            output = str(Path(content_source).with_suffix(".srt"))
        else:
            output = "output.srt"

    Path(output).write_text(srt_content, encoding="utf-8")

    # 输出汇总
    total_sec = current_time - offset
    print(f"✅ 已生成: {output}")
    print(f"   {len(items)} 条字幕 | 总时长 {total_sec:.1f}s ({int(total_sec//60)}分{int(total_sec%60)}秒)")
    min_dur = min(raw_durations)
    max_dur = max(raw_durations)
    print(f"   最短 {min_dur:.1f}s | 最长 {max_dur:.1f}s (基于文本长度+标点停顿)")
    if speed:
        print(f"   基准速度: {speed} 单位/秒 (含标点加权)")
    if total is not None:
        print(f"   目标时长: {total}s")


if __name__ == "__main__":
    main()
