#!/usr/bin/env python3
"""chat.py — 聊天记录分析：汇总 → 深入探索

用法:
  # 汇总最近 3 天所有群的动态
  python chat.py

  # 汇总最近 7 天
  python chat.py --days 7

  # 深入探索某个群的话题
  python chat.py deep "漫步丨港股打新群" --topic "Momenta"

  # 查看某个群近期所有话题
  python chat.py deep "漫步丨港股打新群" --since 2026-07-01
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import chat_lib

SCAN_SUMMARY_SYSTEM = "你是一个聊天记录分析师。用 3-5 句话概括这个群最近在聊什么，列出核心话题和关键讨论点。直接说内容，不要前缀。"

DEEP_SYSTEM = "你是一个聊天记录分析师。严格基于提供的聊天记录分析，不要编造。回答使用中文。"
DEEP_USER = """下面是「{group}」群中与「{topic}」相关的讨论记录（{count} 条）。
请按时间线梳理该话题的来龙去脉：

1. 话题最早什么时候出现、由谁提起
2. 中间有哪些关键转折和重要信息
3. 当前状态（有结论还是仍在讨论）
4. 谁在主导这个话题

使用 Markdown 格式。

聊天记录:
{transcript}"""


def detect_active_chats(days=3):
    """检测最近 days 天内有消息的群"""
    cutoff = datetime.now() - timedelta(days=days)
    active = []

    for f in sorted(chat_lib.CHATS_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue

        name = data.get("displayName", f.stem)
        recent = 0
        last_time = None
        for msg in data.get("messages", []):
            if msg.get("typeName") in ("system", "unknown"):
                continue
            try:
                ts = datetime.strptime(msg["datetime"], "%Y-%m-%d %H:%M:%S")
            except (ValueError, KeyError):
                continue
            if ts >= cutoff:
                recent += 1
                if last_time is None or ts > last_time:
                    last_time = ts

        if recent > 0:
            active.append({
                "filepath": f,
                "name": name,
                "recent_msgs": recent,
                "last_time": last_time,
            })

    active.sort(key=lambda x: x["last_time"] or datetime.min, reverse=True)
    return active


def cmd_scan(days=3):
    active = detect_active_chats(days)

    if not active:
        print(f"最近 {days} 天内没有活跃的群聊记录。")
        return

    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    print(f"\n{'='*60}")
    print(f"  聊天记录扫描 — 最近 {days} 天（{since_date} ~ 今天）")
    print(f"{'='*60}\n")

    for idx, group in enumerate(active, 1):
        name = group["name"]
        recent = group["recent_msgs"]
        last_time = group["last_time"].strftime("%m-%d %H:%M") if group["last_time"] else "?"
        filepath = group["filepath"]

        print(f"── [{idx}] {name} ──")
        print(f"   {recent} 条消息 · 最后活跃 {last_time}")

        _, messages, _ = chat_lib.load_messages(
            filepath, since=since_date, max_messages=200)
        if not messages:
            print()
            continue

        # LLM 一句话摘要
        try:
            transcript = chat_lib.format_transcript(messages[-60:] if len(messages) > 60 else messages)
            summary = chat_lib.call_chat(
                chat_lib.DEFAULT_MODEL,
                SCAN_SUMMARY_SYSTEM,
                f"群名: {name}\n最近聊天:\n{transcript}",
                temperature=0.3,
                label=name,
            ).strip()
            print(f"   {summary}")
        except RuntimeError as e:
            print(f"   (LLM 不可用: {e})")
        print()

    print(f"{'='*60}")
    print(f"  共 {len(active)} 个活跃群")
    print(f"  深入探索: python chat.py deep <群名> --topic <话题>")
    print(f"{'='*60}\n")


def cmd_deep(chat_name, topic=None, since=None):
    filepath = chat_lib.resolve_chat(chat_name)
    group_name, messages, _ = chat_lib.load_messages(
        filepath, since=since, max_messages=500)

    if not messages:
        sys.exit(f"在 '{group_name}' 中未找到符合条件的消息。")

    window = since or "全部"

    if topic:
        # 按话题过滤消息
        topic_lower = topic.lower()
        related = [m for m in messages if topic_lower in m["content"].lower()]
        if not related:
            sys.exit(f"在 '{group_name}' 中未找到与「{topic}」相关的消息。")

        print(f"\n{'='*60}")
        print(f"  深入探索: {group_name} → {topic}")
        print(f"  时间范围: {window} · 相关消息: {len(related)} 条")
        print(f"{'='*60}\n")

        # 消息时间线
        print(f"相关消息时间线:\n")
        for m in related:
            print(f"  [{m['timestamp'][:16]}] {m['sender']}: {m['content'][:200]}")

        # LLM 分析
        print(f"\n{'─'*40}")
        print(f"话题分析:\n")
        transcript = chat_lib.format_transcript(related)
        try:
            analysis = chat_lib.call_chat(
                chat_lib.DEFAULT_MODEL,
                DEEP_SYSTEM,
                DEEP_USER.format(group=group_name, topic=topic,
                                 count=len(related), transcript=transcript),
                temperature=0.3,
            )
            print(analysis)
        except RuntimeError as e:
            print(f"(LLM 不可用: {e})")
    else:
        # 没有指定话题，做 themes 分析
        print(f"\n{'='*60}")
        print(f"  {group_name} — 话题分析")
        print(f"  时间范围: {window} · 消息数: {len(messages)}")
        print(f"{'='*60}\n")

        # 直接调 chat_analyze 的 themes 模式
        try:
            import chat_analyze
            analysis = chat_analyze.run_analysis(
                chat_lib.DEFAULT_MODEL, "themes", group_name, window,
                messages, 0.3)
            print(analysis)
        except RuntimeError as e:
            print(f"(LLM 不可用: {e})")

        print(f"\n{'─'*40}")
        print(f"  深入特定话题: python chat.py deep \"{chat_name}\" --topic <话题>")
        print(f"{'─'*40}\n")


def main():
    ap = argparse.ArgumentParser(description="聊天记录分析")
    ap.add_argument("mode", nargs="?", default="scan",
                    choices=["scan", "deep"],
                    help="scan=汇总, deep=深入")
    ap.add_argument("chat", nargs="?", help="群名称（deep 模式必需）")
    ap.add_argument("--days", type=int, default=3, help="最近 N 天（默认 3）")
    ap.add_argument("--topic", help="深入探索的话题关键词")
    ap.add_argument("--since", help="起始日期 YYYY-MM-DD")
    ap.add_argument("--model", default=chat_lib.DEFAULT_MODEL)
    args = ap.parse_args()

    chat_lib.DEFAULT_MODEL = args.model

    if args.mode == "scan":
        cmd_scan(days=args.days)
    elif args.mode == "deep":
        if not args.chat:
            ap.print_help()
            sys.exit(1)
        since = args.since or (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
        cmd_deep(args.chat, topic=args.topic, since=since)


if __name__ == "__main__":
    main()
