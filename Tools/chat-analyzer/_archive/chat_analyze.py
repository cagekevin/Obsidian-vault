#!/usr/bin/env python3
"""chat_analyze.py — LLM 话题分析（themes/timeline/extract/brief）

支持 map-reduce 策略处理超长聊天记录。

用法:
  python chat_analyze.py themes "漫步丨港股打新群" --since 2026-07-01
  python chat_analyze.py timeline "漫步丨港股打新群" --since 2026-07-01
  python chat_analyze.py brief "漫步丨港股打新群"
  python chat_analyze.py --list
"""

import argparse
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import chat_lib

NUM_CTX = int(os.environ.get("WA_NUM_CTX", "32768"))
OUTPUT_RESERVE = 2500
MAX_TOKENS = int(os.environ.get("WA_MAX_TOKENS", "0"))
OVERHEAD = 800
CHARS_PER_TOKEN = 2.5

_BASE = ("你是一个聊天记录分析师。严格基于提供的聊天记录内容分析，不要编造。"
         "引用具体日期和发言者。回答使用中文。\n\n")

PROMPTS = {
    "extract": _BASE + """请从聊天记录中提取以下信息，使用 Markdown 格式，没有内容的部分省略：

## 决策事项
## 承诺事项（谁承诺了什么）
## 行动项（待办任务及负责人）
## 争议 / 分歧
## 待解决问题（提出但未解决）

没有内容的章节直接省略，不要填充。""",

    "themes": _BASE + """请对聊天记录进行话题分析，使用 Markdown 格式：

## 概述
一段话概括该群聊的核心内容和定位。

## 主要话题
对于每个核心话题（4-8个）：标题加粗、说明讨论内容、如何演变的、
主要分歧点、谁在主导这个话题。引用代表性发言。

## 跨话题关联
涉及多个话题的冲突或联系。

## 未解决事项
截止到记录末尾仍未关闭的讨论。""",

    "timeline": _BASE + """请按时间线梳理关键事件，使用 Markdown 格式。
按日期分组（## 标题），每个日期下列出转折点、决策和重要讨论。
关注事件脉络，不要逐条复述消息。""",

    "brief": _BASE + """请为未关注该群的人写一份简报，使用 Markdown 格式：

## 这是什么群
## 当前状态
## 需要关注什么

三个简短段落，不填充，直击重点。""",
}

MAP_PROMPT = _BASE + """这是较长聊天记录的一部分，按时间顺序排列。
请以 CHRONOLOGICAL ORDER 输出精简笔记，按日期分组（**YYYY-MM-DD**）。
每个日期下，列出该时段的主题、决策、承诺、争议、重要事件和待解决问题。
每条笔记必须归属于对应日期。不要写引言和结论，只输出日期分组的笔记。
这些笔记会和其他部分的笔记合并做最终分析。"""


def transcript_budget_chars() -> int:
    return int((NUM_CTX - OUTPUT_RESERVE - OVERHEAD) * CHARS_PER_TOKEN)


def chunk_messages(messages, budget_chars):
    chunks, cur, size = [], [], 0
    for m in messages:
        ln = len(chat_lib.format_line(m)) + 1
        if cur and size + ln > budget_chars:
            chunks.append(cur)
            cur, size = [], 0
        cur.append(m)
        size += ln
    if cur:
        chunks.append(cur)
    return chunks


def run_analysis(model, mode, group_name, window, messages, temperature):
    budget = transcript_budget_chars()
    transcript = chat_lib.format_transcript(messages)

    if len(transcript) <= budget:
        user = f"群聊: {group_name}\n时间范围: {window}\n消息数: {len(messages)}\n\n聊天记录:\n{transcript}"
        return chat_lib.call_chat(model, PROMPTS[mode], user, temperature, label=group_name)

    chunks = chunk_messages(messages, budget)
    chat_lib.log(f"消息超出 context 限制，使用 map-reduce 分 {len(chunks)} 块处理...")
    notes = []
    for i, ch in enumerate(chunks, 1):
        chat_lib.log(f"  处理第 {i}/{len(chunks)} 块 ({len(ch)} 条消息)...")
        u = f"群聊: {group_name}\n第 {i} 部分 / 共 {len(chunks)} 部分\n\n聊天记录:\n{chat_lib.format_transcript(ch)}"
        notes.append(f"--- 第 {i} 部分笔记 ({ch[0]['timestamp'][:10]} ~ {ch[-1]['timestamp'][:10]}) ---\n"
                     + chat_lib.call_chat(model, MAP_PROMPT, u, temperature, label=f"{group_name} #{i}"))

    chat_lib.log("  合并笔记生成最终报告...")
    combined = "\n\n".join(notes)
    u = (f"群聊: {group_name}\n时间范围: {window}\n"
         f"以下是从完整聊天记录 ({len(chunks)} 部分) 中提炼的时间顺序笔记。"
         f"请仅基于这些笔记进行分析:\n\n{combined}")
    return chat_lib.call_chat(model, PROMPTS[mode], u, temperature)


def main():
    ap = argparse.ArgumentParser(description="聊天记录话题分析")
    ap.add_argument("mode", nargs="?", choices=list(PROMPTS),
                    help="themes | timeline | extract | brief")
    ap.add_argument("chat", nargs="?", help="群名称或 JSON 文件路径")
    ap.add_argument("--since", help="起始日期 YYYY-MM-DD")
    ap.add_argument("--until", help="结束日期 YYYY-MM-DD")
    ap.add_argument("--max-messages", type=int, default=0, help="消息数上限")
    ap.add_argument("--model", default=chat_lib.DEFAULT_MODEL)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--list", action="store_true", help="列出所有聊天记录")
    args = ap.parse_args()

    if args.list:
        chat_lib.list_chats()
        return

    if not args.mode or not args.chat:
        ap.print_help()
        sys.exit(1)

    filepath = chat_lib.resolve_chat(args.chat)
    group_name, messages, truncated = chat_lib.load_messages(
        filepath, args.since, args.until, args.max_messages)

    if not messages:
        sys.exit(f"在 '{group_name}' 中未找到符合条件的消息。")

    window = f"{args.since or '开始'} ~ {args.until or '结束'}"
    approx_tokens = int(len(chat_lib.format_transcript(messages)) / CHARS_PER_TOKEN)
    chat_lib.log(f"群聊: {group_name}")
    chat_lib.log(f"分析范围: {len(messages)} 条消息, {window}, ~{approx_tokens:,} tokens"
                 + (" [已达上限]" if truncated else ""))
    chat_lib.log(f"模式: {args.mode}. 使用模型 {args.model} 分析中...\n")

    try:
        print(run_analysis(args.model, args.mode, group_name, window,
                           messages, args.temperature))
    except RuntimeError as e:
        sys.exit(f"错误: {e}")


if __name__ == "__main__":
    main()
