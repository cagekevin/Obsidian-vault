#!/usr/bin/env python3
"""chat_lib.py — 聊天记录分析底层库"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

CHATS_DIR = Path("G:\\xwechat_files\\聊天记录\\chats")
DEFAULT_BACKEND_URL = "http://localhost:11434/v1"
BACKEND_URL = os.environ.get("WA_BACKEND_URL", DEFAULT_BACKEND_URL).rstrip("/")
DEFAULT_MODEL = os.environ.get("WA_ANALYSIS_MODEL", "qwen3.5:9b")

REPLY_PATTERN = re.compile(r'^↩ .+?：')


def log(msg):
    print(msg, file=sys.stderr)


def resolve_chat(chat_name_or_file):
    p = Path(chat_name_or_file)
    if p.exists() and p.suffix == ".json":
        return p
    files = sorted(CHATS_DIR.glob("*.json"))
    for f in files:
        if f.stem == chat_name_or_file or f.name == chat_name_or_file:
            return f
    matches = []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            name = data.get("displayName", "")
            if chat_name_or_file.lower() in name.lower() or chat_name_or_file.lower() in f.stem.lower():
                matches.append((f, name))
        except Exception:
            continue
    if not matches:
        sys.exit(f"错误: 未找到匹配 '{chat_name_or_file}' 的聊天记录。")
    if len(matches) > 1:
        log(f"'{chat_name_or_file}' 匹配到多个结果: {[m[1] for m in matches]}")
        sys.exit("请缩小搜索范围或使用精确文件名。")
    return matches[0][0]


def load_messages(filepath, since=None, until=None, max_messages=0):
    data = json.loads(filepath.read_text(encoding="utf-8"))
    group_name = data.get("displayName", filepath.stem)
    raw_msgs = data.get("messages", [])

    messages = []
    for msg in raw_msgs:
        if msg.get("typeName") in ("system", "unknown"):
            continue
        content = (msg.get("content") or "").strip()
        if content in ("[表情]", "[图片]", "[语音]", "[视频]", "[动画表情]"):
            continue
        if content == "当前微信版本不支持展示该内容，请升级至最新版本。":
            continue
        try:
            ts = datetime.strptime(msg["datetime"], "%Y-%m-%d %H:%M:%S")
        except (ValueError, KeyError):
            continue
        if since and ts < datetime.strptime(since, "%Y-%m-%d"):
            continue
        if until and ts > datetime.strptime(until + " 23:59:59", "%Y-%m-%d %H:%M:%S"):
            continue

        clean_content = REPLY_PATTERN.sub("", content).strip()
        messages.append({
            "timestamp": msg["datetime"],
            "sender": msg.get("senderName") or msg.get("senderWxid") or "未知",
            "is_from_me": msg.get("isSelf", False),
            "content": clean_content,
        })

    truncated = False
    if max_messages and len(messages) > max_messages:
        truncated = True
        messages = messages[-max_messages:]

    return group_name, messages, truncated


def format_line(msg) -> str:
    ts = msg["timestamp"]
    who = "我" if msg["is_from_me"] else msg["sender"]
    return f"[{ts[:16]}] {who}: {msg['content']}"


def format_transcript(messages) -> str:
    return "\n".join(format_line(m) for m in messages)


def call_chat(model, system, user, temperature=0.2, label=""):
    prefix = f"  [{label}] " if label else ""
    url = f"{BACKEND_URL}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "temperature": temperature,
    }
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"})
    sys.stderr.write(f"{prefix}请求已发送，等待模型响应...\n")
    sys.stderr.flush()
    try:
        with urllib.request.urlopen(req, timeout=900) as resp:
            data = json.load(resp)
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"无法连接 Ollama ({url}): {e.reason}。"
            f"请确保 Ollama 已启动并加载了模型。")
    try:
        result = data["choices"][0]["message"]["content"]
        sys.stderr.write(f"{prefix}完成\n")
        sys.stderr.flush()
        return result
    except (KeyError, TypeError, IndexError):
        raise RuntimeError(f"Ollama 返回异常: {json.dumps(data)[:500]}")


def list_chats():
    files = sorted(CHATS_DIR.glob("*.json"))
    if not files:
        log(f"错误: {CHATS_DIR} 下没有找到 JSON 文件")
        sys.exit(1)
    print(f"{'消息数':>8}  {'群名称':40}  文件名")
    print(f"{'─'*8}  {'─'*40}  {'─'*30}")
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            name = data.get("displayName", f.stem)
            count = len([m for m in data.get("messages", [])
                         if m.get("typeName") not in ("system", "unknown")])
            print(f"{count:>8}  {name[:40]:40}  {f.name}")
        except Exception as e:
            print(f"{'ERR':>8}  {f.name} — {e}")
