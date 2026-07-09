#!/usr/bin/env python3
"""chat_rerank.py — 语义重排序，对 BM25 结果做相似度排序。

使用 Ollama 的 nomic-embed-text 对搜索结果做语义重排序。
如果 Ollama 不可用则返回 BM25 原始顺序。

用法:
  # 标准重排（从 BM25 结果重排）
  python chat_rerank.py "漫步丨港股打新群" "Momenta 新股" --candidates results.json

  # 查看当前策略
  python chat_rerank.py --peek "test query"
"""

import argparse
import hashlib
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CHATS_DIR = Path("G:\\xwechat_files\\聊天记录\\chats")

DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "nomic-embed-text"
OLLAMA_TIMEOUT_SEC = 3
EMBED_TIMEOUT_SEC = 30
MAX_RESPONSE_BYTES = 4 * 1024 * 1024

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_CANDIDATES = 3


def log(msg):
    print(msg, file=sys.stderr)


def cosine(a, b):
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


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


def ollama_alive(url):
    try:
        req = urllib.request.Request(f"{url}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT_SEC) as resp:
            data = json.loads(resp.read(MAX_RESPONSE_BYTES))
            models = [m.get("name", "").split(":")[0] for m in data.get("models", [])]
            return True, models
    except (urllib.error.URLError, json.JSONDecodeError, OSError):
        return False, []


def embed_one(url, model, text):
    payload = json.dumps({"model": model, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        f"{url}/api/embeddings",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=EMBED_TIMEOUT_SEC) as resp:
        data = json.loads(resp.read(MAX_RESPONSE_BYTES))
        return data.get("embedding") or []


def get_cache_dir(filepath):
    return filepath.parent / (filepath.stem + ".bm25")


def get_cache_path(filepath):
    return get_cache_dir(filepath) / "embed_cache.json"


def load_cache(filepath):
    p = get_cache_path(filepath)
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(cache, filepath):
    p = get_cache_path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(f".{os.getpid()}.tmp")
    try:
        tmp.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, p)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)


def rerank(filepath, query, candidates, top_k=5, allow_remote=False):
    """对候选消息做语义重排序"""
    url = os.environ.get("OLLAMA_URL", DEFAULT_OLLAMA_URL).rstrip("/")

    if not allow_remote:
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname or ""
        if host not in ("127.0.0.1", "localhost", "::1"):
            log(f"OLLAMA_URL={url} 指向非本地地址，请设置 --allow-remote-ollama")
            for c in candidates:
                c["rerank_score"] = float(c.get("score", 0.0))
                c["rerank_source"] = "noop-remote"
            return candidates[:top_k]

    alive, models = ollama_alive(url)
    if not alive:
        log("Ollama 不可用 — 返回 BM25 原始顺序")
        for c in candidates:
            c["rerank_score"] = float(c.get("score", 0.0))
            c["rerank_source"] = "noop-no-ollama"
        return candidates[:top_k]

    if DEFAULT_MODEL not in models:
        log(f"模型 {DEFAULT_MODEL} 未下载 — 返回 BM25 原始顺序")
        for c in candidates:
            c["rerank_score"] = float(c.get("score", 0.0))
            c["rerank_source"] = "noop-no-model"
        return candidates[:top_k]

    cache = load_cache(filepath)
    cache_dirty = False

    try:
        q_emb = embed_one(url, DEFAULT_MODEL, query)
    except Exception as e:
        log(f"查询嵌入失败: {e}")
        for c in candidates:
            c["rerank_score"] = float(c.get("score", 0.0))
            c["rerank_source"] = "noop-embed-error"
        return candidates[:top_k]

    for c in candidates:
        content = c.get("content", "")
        body_hash = hashlib.md5(content.encode("utf-8")).hexdigest()
        cache_key = f"{DEFAULT_MODEL}:{body_hash}"
        emb = cache.get(cache_key)

        if not emb:
            try:
                emb = embed_one(url, DEFAULT_MODEL, content)
            except Exception as e:
                log(f"嵌入失败: {e}")
                c["rerank_score"] = float(c.get("score", 0.0))
                c["rerank_source"] = "embed-error"
                continue
            cache[cache_key] = emb
            cache_dirty = True

        c["rerank_score"] = cosine(q_emb, emb)
        c["rerank_source"] = f"cosine:{DEFAULT_MODEL}"

    if cache_dirty:
        save_cache(cache, filepath)

    ranked = sorted(candidates, key=lambda x: x.get("rerank_score", 0.0), reverse=True)
    return ranked[:top_k]


def main():
    parser = argparse.ArgumentParser(description="聊天记录语义重排序")
    parser.add_argument("chat", nargs="?", help="群名称或 JSON 文件")
    parser.add_argument("query", nargs="?", help="搜索查询")
    parser.add_argument("--candidates", help="候选结果 JSON 文件或 `-` 从 stdin 读")
    parser.add_argument("--top", type=int, default=5, help="返回结果数")
    parser.add_argument("--peek", action="store_true", help="查看重排策略")
    parser.add_argument("--allow-remote-ollama", action="store_true")

    args = parser.parse_args()

    if args.peek:
        url = os.environ.get("OLLAMA_URL", DEFAULT_OLLAMA_URL).rstrip("/")
        alive, models = ollama_alive(url)
        strategy = "noop-no-ollama"
        if alive:
            strategy = f"cosine:{DEFAULT_MODEL}" if DEFAULT_MODEL in models else "noop-no-model"
        print(json.dumps({
            "query": args.query,
            "strategy": strategy,
            "ollama_url": url,
            "ollama_alive": alive,
            "model_present": DEFAULT_MODEL in models,
        }, indent=2, ensure_ascii=False))
        return EXIT_OK

    if not args.chat or not args.query or args.candidates is None:
        log("用法: chat_rerank.py <chat> <query> --candidates <path|-> [--top N]")
        return EXIT_USAGE

    filepath = resolve_chat(args.chat)

    if args.candidates == "-":
        cand_text = sys.stdin.read()
    else:
        cand_text = Path(args.candidates).read_text(encoding="utf-8")
    try:
        candidates = json.loads(cand_text)
        if not isinstance(candidates, list):
            raise ValueError("candidates must be a JSON list")
    except (json.JSONDecodeError, ValueError) as e:
        log(f"错误: 候选结果格式错误: {e}")
        return EXIT_CANDIDATES

    result = rerank(filepath, args.query, candidates, top_k=args.top,
                    allow_remote=args.allow_remote_ollama)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
