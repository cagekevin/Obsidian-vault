#!/usr/bin/env python3
"""chat_bm25.py — BM25 索引构建 + 查询，适配聊天记录。

从 WeFlow JSON 聊天记录构建 BM25 索引，支持中文语义搜索。
每条消息作为一个文档，索引字段为消息内容。

用法:
  # 构建索引（先指定聊天记录）
  python chat_bm25.py build "漫步丨港股打新群"

  # 查询
  python chat_bm25.py query "Momenta 新股" --top 10

  # 查看索引统计
  python chat_bm25.py stats

数据:
  索引文件保存在 {聊天记录文件名}.bm25/index.json 同级目录
"""

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

CHATS_DIR = Path("G:\\xwechat_files\\聊天记录\\chats")

K1 = 1.5
B = 0.75

# 中英文混合分词
TOKEN_RE = re.compile(r"\w[\w'\-]*", re.UNICODE)
CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+")

# 中文停用词
STOPWORDS = frozenset("""
的 了 在 是 我 有 和 就 不 人 都 一 一个 上 也 很 到 说 要 去 你
会 着 没有 看 好 自己 这 他 她 它 们 那 这个 那个 什么 怎么 可以
但是 因为 所以 如果 还是 不是 吗 啊 呢 吧 哦 嗯 哈 哈哈 啊 呀 啦
ok OK em emmm 嗯嗯 好的 是的 对 对呀 嗯呢 行 可以 了 哦哦
a an and are as at be by for from has have he her him his i if in is it its
of on or that the their them they this to was were will with you your
""".split())

REPLY_PATTERN = re.compile(r'^↩ .+?：')


def log(msg):
    print(msg, file=sys.stderr)


def tokenize(text):
    """分词：英文单词 + 中文二元组"""
    terms = []
    for t in TOKEN_RE.findall(text):
        t = t.lower()
        if t not in STOPWORDS and len(t) > 1:
            terms.append(t)
    for cjk_run in CJK_RE.findall(text):
        if len(cjk_run) == 1:
            terms.append(cjk_run)
        else:
            for i in range(len(cjk_run) - 1):
                terms.append(cjk_run[i:i+2])
    return terms


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
        sys.exit(f"未找到匹配 '{chat_name_or_file}' 的聊天记录。")
    if len(matches) > 1:
        log(f"'{chat_name_or_file}' 匹配到多个: {[m[1] for m in matches]}")
        sys.exit("请精确指定。")
    return matches[0][0]


def get_index_dir(filepath):
    """索引文件保存在聊天记录同级目录"""
    return filepath.parent / (filepath.stem + ".bm25")


def get_index_path(filepath):
    return get_index_dir(filepath) / "index.json"


def load_messages_for_index(filepath):
    """加载消息用于索引"""
    data = json.loads(filepath.read_text(encoding="utf-8"))
    group_name = data.get("displayName", filepath.stem)
    messages = []
    for msg in data.get("messages", []):
        if msg.get("typeName") in ("system", "unknown"):
            continue
        content = (msg.get("content") or "").strip()
        if content in ("[表情]", "[图片]", "[语音]", "[视频]", "[动画表情]"):
            continue
        if content == "当前微信版本不支持展示该内容，请升级至最新版本。":
            continue
        clean_content = REPLY_PATTERN.sub("", content).strip()
        if not clean_content:
            continue
        messages.append({
            "msg_id": msg["id"],
            "datetime": msg.get("datetime", ""),
            "sender": msg.get("senderName") or msg.get("senderWxid") or "未知",
            "content": clean_content,
        })
    return group_name, messages


def build_index(filepath):
    """构建 BM25 索引"""
    group_name, messages = load_messages_for_index(filepath)
    log(f"构建索引: {group_name} ({len(messages)} 条消息)")

    docs = {}
    df = Counter()
    postings = defaultdict(list)

    for msg in messages:
        tokens = tokenize(msg["content"])
        tf = Counter(tokens)
        doc_id = str(msg["msg_id"])
        docs[doc_id] = {
            "datetime": msg["datetime"],
            "sender": msg["sender"],
            "content": msg["content"],
            "dl": len(tokens),
        }
        for term, count in tf.items():
            df[term] += 1
            postings[term].append([doc_id, count])

    if not docs:
        log("没有可索引的消息。")
        return None

    avg_dl = sum(d["dl"] for d in docs.values()) / len(docs)
    vocab = {
        term: {"df": df[term], "postings": postings[term]}
        for term in sorted(df.keys())
    }

    return {
        "schema_version": 1,
        "group_name": group_name,
        "source_file": str(filepath),
        "params": {"k1": K1, "b": B},
        "doc_count": len(docs),
        "avg_dl": avg_dl,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "vocab": vocab,
        "docs": docs,
    }


def write_index(index, filepath):
    idx_dir = get_index_dir(filepath)
    idx_dir.mkdir(parents=True, exist_ok=True)
    idx_path = get_index_path(filepath)
    tmp = idx_path.with_suffix(f".{os.getpid()}.tmp")
    try:
        tmp.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, idx_path)
        log(f"索引已保存: {idx_path}  docs={index['doc_count']}  vocab={len(index['vocab'])}")
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)


def load_index(filepath):
    idx_path = get_index_path(filepath)
    if not idx_path.is_file():
        sys.exit(f"索引不存在: {idx_path}。请先运行 build。")
    try:
        return json.loads(idx_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        sys.exit(f"索引损坏: {e}")


def query(filepath, text, top_k=20):
    idx = load_index(filepath)
    vocab = idx["vocab"]
    docs = idx["docs"]
    params = idx["params"]
    avg_dl = idx["avg_dl"]
    N = idx["doc_count"]
    k1 = params["k1"]
    b = params["b"]

    qterms = tokenize(text)
    if not qterms:
        return []

    avg_dl_safe = avg_dl or 1.0
    scores = defaultdict(float)
    for term in qterms:
        v = vocab.get(term)
        if not v:
            continue
        df = v["df"]
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        for doc_id, cnt in v["postings"]:
            dl = docs[doc_id]["dl"]
            denom = cnt + k1 * (1 - b + b * dl / avg_dl_safe)
            scores[doc_id] += idf * (cnt * (k1 + 1)) / denom

    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    return [
        {
            "msg_id": doc_id,
            "score": round(score, 6),
            "datetime": docs[doc_id]["datetime"],
            "sender": docs[doc_id]["sender"],
            "content": docs[doc_id]["content"],
        }
        for doc_id, score in ranked
    ]


def cmd_build(chat_name):
    filepath = resolve_chat(chat_name)
    index = build_index(filepath)
    if index is None:
        return
    write_index(index, filepath)


def cmd_query(chat_name, text, top_k):
    filepath = resolve_chat(chat_name)
    results = query(filepath, text, top_k)
    if not results:
        print("未找到匹配结果。")
        return
    print(f"找到 {len(results)} 条相关消息:\n")
    for r in results:
        print(f"[{r['datetime']}] {r['sender']}: {r['content']}")
        print(f"   (score: {r['score']})\n")


def cmd_stats(chat_name):
    filepath = resolve_chat(chat_name)
    idx = load_index(filepath)
    print(json.dumps({
        "group_name": idx["group_name"],
        "doc_count": idx["doc_count"],
        "avg_dl": round(idx["avg_dl"], 2),
        "vocab_size": len(idx["vocab"]),
        "updated_at": idx["updated_at"],
    }, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="聊天记录 BM25 搜索")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sp_build = sub.add_parser("build", help="构建索引")
    sp_build.add_argument("chat", help="群名称或 JSON 文件")

    sp_query = sub.add_parser("query", help="搜索")
    sp_query.add_argument("chat", help="群名称或 JSON 文件")
    sp_query.add_argument("text", help="搜索关键词")
    sp_query.add_argument("--top", type=int, default=10, help="返回结果数")

    sp_stats = sub.add_parser("stats", help="索引统计")
    sp_stats.add_argument("chat", help="群名称或 JSON 文件")

    args = parser.parse_args()

    if args.cmd == "build":
        cmd_build(args.chat)
    elif args.cmd == "query":
        cmd_query(args.chat, args.text, args.top)
    elif args.cmd == "stats":
        cmd_stats(args.chat)


if __name__ == "__main__":
    main()
