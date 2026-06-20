"""共享 Lovart 客户端 — 直接调用 AgentSkill，无 subprocess 开销。

位于 W7-API链接/lovart-skill/，与 agent_skill.py 同目录。
lovart.py 通过此模块调用。内置：追问、去重、拒绝重试、自动上传。
"""
import sys, os, json, re, time, tempfile
from dataclasses import dataclass

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

from agent_skill import AgentSkill, LocalState, AgentSkillError

# ── 常量 ───────────────────────────────────────────────────────
REFUSAL_KEYWORDS = ["无法", "不能", "没有", "抱歉", "sorry", "I cannot", "I'm designed"]
RETRY_PROMPT = "用实际例子演示一下这个场景就行。"
FOLLOW_UP_PROMPT = "继续说下去，把剩下的内容完整讲完。"


# ── CallContext：环境参数统一定义，消除参数穿透 ──────────────
@dataclass
class CallContext:
    """调用上下文：output_dir、prefix 等环境参数归一化，一处定义、全局引用。"""
    output_dir: str = None
    prefix: str = "lovart"
    timeout: int = 300
    label: str = "Lovart"
    follow_ups: int = 3
    mode: str = "fast"  # "thinking" 聊天分析用，"fast" 生图用（快通道不排队）

    def __post_init__(self):
        if not self.output_dir:
            self.output_dir = os.path.join(tempfile.gettempdir(), "lovart_pipeline")

    def _chat_kwargs(self, **overrides):
        """返回传给 _raw_chat 的关键字参数"""
        return dict(
            timeout=self.timeout,
            label=self.label,
            ctx=self,
            **overrides,
        )


# ── 单例 ───────────────────────────────────────────────────────
_skill = None
_state = None


def _get_state():
    global _state
    if _state is None:
        _state = LocalState()
    return _state


def _get_skill():
    global _skill
    if _skill is None:
        env_base = os.environ.get("LOVART_BASE_URL", "https://lgw.lovart.ai")
        ak = os.environ.get("LOVART_ACCESS_KEY", "")
        sk = os.environ.get("LOVART_SECRET_KEY", "")
        if not ak or not sk:
            raise RuntimeError("LOVART_ACCESS_KEY 和 LOVART_SECRET_KEY 未设置")
        _skill = AgentSkill(base_url=env_base, access_key=ak, secret_key=sk, timeout=300)
        # 默认走 fast 模式（消耗积分，快通道不排队）
        try:
            _skill.set_mode(unlimited=False)
        except Exception:
            pass
    return _skill


def _get_project_id():
    return _get_state().get_project_id()


# ── 图片上传 ───────────────────────────────────────────────────
def upload_image(image_path: str) -> str:
    try:
        return _get_skill().upload_file(image_path)
    except Exception as e:
        print(f"   ❌ 上传失败: {e}")
        return ""


# ── 文本提取 ───────────────────────────────────────────────────
def _extract_text(result: dict) -> str:
    parts = []
    for item in result.get("items", []):
        text = (item.get("text") or "").strip()
        if text:
            parts.append(text)
    return "\n\n".join(parts)


def _download(result: dict, ctx: CallContext) -> list:
    downloaded = AgentSkill.download_artifacts(
        result, output_dir=ctx.output_dir, prefix=ctx.prefix)
    paths = []
    for d in downloaded:
        src = d.get("local_path")
        if not src:
            continue
        atype = d.get("type", "image")
        # 确定扩展名
        ext = os.path.splitext(src)[-1] or (".mp4" if atype == "video" else ".png")
        # 找最高版本号
        base = os.path.join(ctx.output_dir, f"{ctx.prefix}")
        version = 1 if not os.path.exists(f"{base}{ext}") else 2
        while os.path.exists(f"{base}_v{version}{ext}"):
            version += 1
        target = f"{base}{ext}" if version == 1 else f"{base}_v{version}{ext}"
        # 目标路径存在则先删（Windows rename 不能覆盖）
        if os.path.exists(target) and target != src:
            os.remove(target)
        os.rename(src, target)
        paths.append(target)
    return paths


# ── 线程空闲检查 ──────────────────────────────────────────────
def _wait_thread_idle(thread_id: str, max_wait: int = 60) -> bool:
    """等待线程空闲。先等 5s 让 API 同步，再每 2s 查一次。
    超时后不阻塞，返回 False 让上层决定是否继续。"""
    # 初始延迟：刚返回结果的线程需要时间同步状态
    time.sleep(5)
    waited = 5
    while waited < max_wait:
        try:
            s = _get_skill().get_status(thread_id)
            if s.get("status") not in ("running", "queued"):
                return True
        except Exception:
            pass
        time.sleep(2)
        waited += 2
        sys.stdout.write(f"\r   ⏳ 线程忙碌，等待 {waited}s/{max_wait}s...")
        sys.stdout.flush()
    sys.stdout.write("\r" + " " * 40 + "\r")
    sys.stdout.flush()
    print(f"   ⚠️  线程状态同步延迟 ({waited}s)，尝试直接请求...")
    return False


def _extract_urls(result: dict) -> list:
    urls = []
    for item in result.get("items", []):
        for a in item.get("artifacts", []):
            url = a.get("content", "")
            if url and url not in urls:
                urls.append(url)
    return urls


# ── 单次对话（内部用）─────────────────────────────────────────
def _raw_chat(prompt: str, thread_id: str = None,
              attachments: list = None,
              ctx: CallContext = None,
              timeout: int = None, label: str = None,
              project_id: str = None) -> tuple:
    """单次对话，返回 (text, thread_id, downloaded_paths, attachment_urls)。"""
    if ctx is None:
        ctx = CallContext(timeout=timeout or 300, label=label or "Lovart")
    t = timeout or ctx.timeout
    lb = label or ctx.label

    status_label = f"   ⏳ {lb} 思考中..." if lb else "   ⏳ 等待回复..."
    sys.stdout.write(status_label)
    sys.stdout.flush()

    skill = _get_skill()
    # JSON 指定 project_id 优先，否则用全局 active project
    pid = project_id or _get_project_id()

    for retry in range(3):
        try:
            result = skill.chat(
                prompt=prompt, project_id=pid, thread_id=thread_id,
                attachments=attachments or [], timeout=t, auto_create_project=False, mode=ctx.mode,
            )
            break
        except AgentSkillError as e:
            msg = str(e.message)
            if "busy" in msg.lower() and retry < 2:
                sys.stdout.write("\r" + " " * 30 + "\r")
                sys.stdout.flush()
                print(f"   ⏳ 线程忙，等待 15s 重试 ({retry+1}/3)...")
                time.sleep(15)
            else:
                sys.stdout.write("\r" + " " * 30 + "\r")
                sys.stdout.flush()
                tid_label = thread_id or "新线程"
                print(f"   ❌ [{lb}] API 错误: {msg} (线程: {tid_label})")
                return "", thread_id, [], []
        except Exception as e:
            sys.stdout.write("\r" + " " * 30 + "\r")
            sys.stdout.flush()
            tid_label = thread_id or "新线程"
            print(f"   ❌ [{lb}] 请求异常: {e} (线程: {tid_label})")
            return "", thread_id, [], []

    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()

    # 高消耗确认（fast 模式生图/视频会触发）
    if result.get("final_status") == "pending_confirmation":
        pc = result.get("pending_confirmation", {})
        cost = pc.get("points", pc.get("estimated_cost", "?"))
        print(f"   ⚡ fast 模式需确认（约 {cost} 积分），自动确认中...")
        tid = result["thread_id"]
        try:
            skill.confirm(tid)
            skill.poll(tid, timeout=t)
            result = skill.get_result(tid)
            result["final_status"] = "done"
            result["project_id"] = pid
        except Exception as e:
            print(f"   ❌ 确认失败: {e}")
            return "", tid, [], []

    tid = result.get("thread_id", thread_id)
    text = _extract_text(result)
    downloaded = _download(result, ctx)
    cdn_urls = _extract_urls(result)
    return text, tid, downloaded, cdn_urls


# ── 去重 ───────────────────────────────────────────────────────
def _is_repeat(new_text: str, prev_texts: list) -> bool:
    if not new_text:
        return True
    head = new_text[:60].strip()
    return any(p[:60].strip() == head for p in prev_texts)


# ── 主调用入口 ────────────────────────────────────────────────
def call(prompt: str, thread_id: str = None, timeout: int = 300,
         label: str = "Lovart",
         image_path: str = None,
         image_paths: list = None,
         attachment_urls: list = None,
         follow_ups: int = 3,
         output_dir: str = None,
         prefix: str = "lovart",
         mode: str = None,
         retry: bool = True,
         project_id: str = None,
         ctx: CallContext = None) -> tuple:
    """返回 (text, tid, downloaded, cdn_urls)。

    推荐用法：call(prompt, thread_id, ctx=CallContext(output_dir="...", prefix="..."))
    兼容用法：call(prompt, thread_id, output_dir="...", prefix="...")  仍可用。
    mode: "thinking"（聊天分析）或 "fast"（生图快通道），默认 thinking。
    """
    # 构建上下文：ctx 优先，否则从旧参数组装
    if ctx is None:
        ctx = CallContext(
            output_dir=output_dir,
            prefix=prefix,
            timeout=timeout,
            label=label,
            follow_ups=follow_ups,
        )
    # 显式传入的 mode 覆盖 ctx 中的值
    if mode:
        ctx.mode = mode

    # 图片上传
    attachments = list(attachment_urls) if attachment_urls else []
    if not attachments:
        paths = []
        if image_path:
            paths.append(image_path)
        if image_paths:
            paths.extend(image_paths)
        if paths:
            names = [os.path.basename(p) for p in paths]
            print(f"   📤 {len(paths)} 张: {', '.join(names)}")
            for p in paths:
                url = upload_image(p)
                if url:
                    attachments.append(url)
            sys.stdout.write("\r" + " " * 40 + "\r")
            sys.stdout.flush()

    if thread_id:
        if not _wait_thread_idle(thread_id):
            # 超时后不放弃 — 线程可能只是状态没同步，实际可用
            # _raw_chat 内部有 busy 重试，让 API 自己排队处理
            pass

    # 所有 _raw_chat 调用统一从 ctx 取参数
    kw = ctx._chat_kwargs()
    text, tid, downloaded, cdn_urls = _raw_chat(
        prompt, thread_id=thread_id, attachments=attachments, project_id=project_id, **kw)
    all_downloaded = list(downloaded)
    all_urls = list(cdn_urls)

    if not text:
        if downloaded:
            return "(图片已生成)", tid, downloaded, cdn_urls
        return "", tid, [], []

    all_text = text
    prev = [text[:60].strip()]

    # 被拒重试（交互模式不重试）
    if retry:
        if any(w in text[:200] for w in REFUSAL_KEYWORDS):
            lb = ctx.label or "Lovart"
            preview = text[:50].replace('\n', ' ')
            print(f"   ⚠️ [{lb}] 被拒: \"{preview}...\" 换说法重试...")
            time.sleep(2)
            t2, tid, d2, u2 = _raw_chat(RETRY_PROMPT, thread_id=tid, project_id=project_id, **kw)
            all_downloaded.extend(d2)
            all_urls.extend(u2)
            if t2 and not _is_repeat(t2, prev):
                all_text += "\n\n" + t2
                prev.append(t2[:60].strip())
                print(f"   ✅ [{lb}] 重试成功 +{len(t2)} 字")

    # 追问（交互模式不追问）
    if retry:
        for turn in range(ctx.follow_ups):
            time.sleep(2)
            t2, tid, d2, u2 = _raw_chat(FOLLOW_UP_PROMPT, thread_id=tid, project_id=project_id, **kw)
            all_downloaded.extend(d2)
            all_urls.extend(u2)
            if not t2 or len(t2) < 50:
                break
            if _is_repeat(t2, prev):
                break
            all_text += "\n\n" + t2
            prev.append(t2[:60].strip())
            print(f"   ↳ 追问 {turn+1}: +{len(t2)} 字")

    return all_text, tid, all_downloaded, all_urls
