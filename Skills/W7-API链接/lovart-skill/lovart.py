#!/usr/bin/env python3
"""
Lovart 对话引擎 — 统一入口，所有模式由 JSON 配置控制。

用法:
  python lovart.py projects/xxx.json

支持 4 种模式（由 JSON 的 mode 字段决定）:

  1. ask     — 单次纯文本对话
  2. analyze — 单次带图分析
  3. batch   — 批量钓鱼（读 tasks 数组，自动跳过已有/去重/追问）
  4. pipeline — 多步管线（逐步执行，自动传 thread_id）

所有模式共享 lovart_client.call() 的追问/去重/拒绝重试/续期逻辑。

JSON 公共字段: mode, output_dir, follow_ups
"""
import sys, os, json, time, re, glob as glob_mod
from pathlib import Path

# lovart_client.py 同目录
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lovart_client import call, CallContext

# ── 默认值（全局统一，不再散落各处）─────────────────────────
# lovart-skill/ → W7-API链接/ → 工作效率类/ → skills/ → skills-main/
_MAIN_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
_DEFAULT_OUTPUT = os.path.join(os.path.dirname(_MAIN_DIR), "Temp")
_DEFAULT_FOLLOW_UPS = 3
_DEFAULT_STEP_DELAY = 8

# 占位符正则：匹配 [项目UUID] [项目路径] 等
_PLACEHOLDER_RE = re.compile(r'\[.*?\]')


def load_config(path):
    p = Path(path)
    if not p.exists():
        print(f"❌ 找不到 {path}")
        sys.exit(1)
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式错误: {e}")
        sys.exit(1)


def _resolve(cfg: dict, key: str, default):
    """解析配置中的占位符，遇到 [项目UUID] [项目路径] 等返回默认值"""
    val = cfg.get(key)
    if not val or (isinstance(val, str) and _PLACEHOLDER_RE.match(val)):
        return default
    return val


def save_step(text, name, output_dir, pipeline_prefix=""):
    os.makedirs(output_dir, exist_ok=True)
    safe = name.replace(" ", "_").replace("/", "_")
    prefix = f"{pipeline_prefix}_" if pipeline_prefix else ""
    fpath = os.path.join(output_dir, f"{prefix}{safe}.md")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(text)
    preview = text[:120].replace("\n", " ").strip()
    print(f"   💾 {fpath} ({len(text)} 字)")
    if preview:
        print(f"   📄 {preview}...")


# ══════════════════════════════════════════════════════════
#  Mode: ask — 单次纯文本
# ══════════════════════════════════════════════════════════

def mode_ask(cfg):
    text, tid, _, _ = call(
        cfg["prompt"],
        label="Lovart",
        thread_id=cfg.get("thread_id"),
        follow_ups=cfg.get("follow_ups", _DEFAULT_FOLLOW_UPS),
        project_id=_resolve(cfg, "project_id", None),
        ctx=CallContext(mode=cfg.get("mode", "thinking")),
    )
    output_dir = _resolve(cfg, "output_dir", _DEFAULT_OUTPUT)
    if text:
        save_step(text, "output", output_dir)
    return text, tid


# ══════════════════════════════════════════════════════════
#  Mode: analyze — 单次带图
# ══════════════════════════════════════════════════════════

def mode_analyze(cfg):
    img = cfg.get("image")
    imgs = cfg.get("images")
    text, tid, _, _ = call(
        cfg["prompt"],
        label="Lovart",
        thread_id=cfg.get("thread_id"),
        image_path=img,
        image_paths=imgs if imgs and len(imgs) > 1 else None,
        follow_ups=cfg.get("follow_ups", _DEFAULT_FOLLOW_UPS),
        project_id=_resolve(cfg, "project_id", None),
        ctx=CallContext(mode=cfg.get("mode", "thinking")),
    )
    output_dir = _resolve(cfg, "output_dir", _DEFAULT_OUTPUT)
    if text:
        save_step(text, "output", output_dir)
    return text, tid


# ══════════════════════════════════════════════════════════
#  Mode: batch — 批量钓鱼
# ══════════════════════════════════════════════════════════

def mode_batch(cfg):
    tasks = cfg.get("tasks", [])
    follow_ups = cfg.get("follow_ups", 5)
    output_dir = _resolve(cfg, "output_dir", _DEFAULT_OUTPUT)
    mark_done = cfg.get("mark_done", False)
    config_path = cfg.get("_config_path")

    if not tasks:
        print("✅ 无待处理任务")
        return

    print(f"\n   📋 {len(tasks)} 个任务")
    for i, m in enumerate(tasks):
        label = m["label"]
        fpath = os.path.join(output_dir, f"{label}.md")

        # 跳过已有
        if os.path.isfile(fpath) and os.path.getsize(fpath) > 100:
            print(f"\n[{i+1}/{len(tasks)}] {label} ⏭️  已有")
            m["_done"] = True
            continue

        print(f"\n[{i+1}/{len(tasks)}] 📤 {label}...")
        text, tid, _, _ = call(m["prompt"], label="Lovart", follow_ups=follow_ups, project_id=_resolve(cfg, "project_id", None))

        if not text:
            print("   ⚠️  无回复，跳过")
            continue

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(f"# {label}\n\n## 话术\n\n{m['prompt']}\n\n## 回复\n\n{text}\n")
        print(f"   💾 {label}.md ({len(text)} 字)")
        m["_done"] = True
        time.sleep(3)

    # mark_done: 从 JSON 移除已完成任务
    if mark_done and config_path and os.path.exists(config_path):
        remaining = [t for t in tasks if not t.get("_done")]
        if len(remaining) < len(tasks):
            cfg["tasks"] = remaining
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2, ensure_ascii=False)
            print(f"\n   🗑️  已从 JSON 移除 {len(tasks) - len(remaining)} 个已完成任务")

    print("\n✅ 批量完成")


# ══════════════════════════════════════════════════════════
#  Mode: pipeline — 多步管线
# ══════════════════════════════════════════════════════════

def mode_pipeline(cfg):
    steps = cfg.get("steps", [])
    output_dir = _resolve(cfg, "output_dir", _DEFAULT_OUTPUT)
    state_path = os.path.join(output_dir, ".lovart_state.json")

    # 加载项目状态（线程ID、步骤进度）
    # 注意：state 仅用于跳过已有步骤时恢复线程，新 pipeline 第一步始终用新线程
    state = {}
    if os.path.isfile(state_path):
        try:
            state = json.loads(Path(state_path).read_text(encoding="utf-8"))
        except Exception:
            pass
    main_tid = cfg.get("thread_id")  # 仅在 JSON 显式指定时使用，不取自 state
    current_tid = main_tid  # None → 第一步开新线程，不同 pipeline 互不干扰
    last_generated_images = []
    last_urls = []
    step_outputs = {}

    def resolve_refs(text):
        """解析 prompt 中的 $step[name] 和 $file[path] 引用"""
        if not isinstance(text, str):
            return text
        # $step[name]
        def step_replacer(m):
            ref_name = m.group(1)
            if ref_name in step_outputs:
                content = step_outputs[ref_name]
                print(f"   📝 $step[{ref_name}] -> {len(content)} 字")
                return content
            print(f"   ⚠️  $step[{ref_name}] 未找到")
            return m.group(0)
        text = re.sub(r'\$step\[(.+?)\]', step_replacer, text)
        # $file[path] — 加载外部文件，解决新线程引用前置产出的问题
        def file_replacer(m):
            path = m.group(1)
            if os.path.isfile(path):
                try:
                    content = Path(path).read_text(encoding="utf-8")
                    print(f"   📄 $file[{os.path.basename(path)}] -> {len(content)} 字")
                    return content
                except Exception as e:
                    print(f"   ⚠️  $file[{path}] 读取失败: {e}")
            else:
                print(f"   ⚠️  $file[{path}] 文件不存在")
            return m.group(0)
        return re.sub(r'\$file\[(.+?)\]', file_replacer, text)

    step_delay = cfg.get("step_delay", _DEFAULT_STEP_DELAY)
    pipeline_name_slug = re.sub(r'[<>:"/\\|?*\s]', '_', cfg.get("name", "pipeline"))[:20]

    print(f"\n   📋 {len(steps)} 步")
    for step in steps:
        name = step["name"]
        step_type = step.get("type", "ask")
        prompt = resolve_refs(step["prompt"])
        fups = step.get("follow_ups", _DEFAULT_FOLLOW_UPS)
        img = step.get("image")
        imgs = step.get("images")  # 多图列表，优先级低于 image
        thread_mode = step.get("thread")  # "main" / "new" / None(默认顺延)

        # 将结构化参数转为自然语言注入 prompt，让 Lovart AI 能理解
        STEP_MODEL_NAMES = {
            "nb2": "Nano Banana 2",
            "gpt2 low": "GPT Image 2 Low",
            "gpt2 medium": "GPT Image 2 Medium",
            "gpt2 high": "GPT Image 2 High",
            "seedance_v2_0": "Seedance 2.0",
        }
        nl_parts = []
        if step.get("model"):
            m = STEP_MODEL_NAMES.get(step["model"], step["model"])
            nl_parts.append(f"使用{m}模型")
        if step.get("resolution"):
            nl_parts.append(f"{step['resolution']}画质")
        if step.get("aspect_ratio"):
            nl_parts.append(f"{step['aspect_ratio']}比例")
        if nl_parts:
            prompt = "，".join(nl_parts) + "生成图片。" + prompt

        # 解析 image 字段：$last 优先用 CDN URL，避免重复上传
        reuse_urls = []
        if isinstance(img, str) and img.startswith("$last"):
            if img == "$last":
                reuse_urls = [last_urls[0]] if last_urls else []
            else:
                try:
                    idx = int(img[6:-1])
                    if 0 <= idx < len(last_urls):
                        reuse_urls = [last_urls[idx]]
                    else:
                        print(f"   ⚠️  $last[{idx}] 超出范围 (共{len(last_urls)}张)")
                except ValueError:
                    print(f"   ⚠️  无法解析 {img}")
            img = None  # $last 语法由 reuse_urls 接管，不再走上传

        # 决定本步使用的 thread_id
        if thread_mode == "new":
            step_tid = None          # 开新对话
        elif thread_mode == "main":
            step_tid = main_tid      # 回到主线
        else:
            step_tid = current_tid   # 默认：顺延上一步的线程

        mode_label = f"🆕" if thread_mode == "new" else (f"🔙" if thread_mode == "main" else "🔄")
        print(f"\n  — {mode_label} {name} —")

        # 跳过已完成：md 文件存在 或 图片已生成（用管线前缀+步骤前缀全名匹配）
        safe_name = name.replace(" ", "_").replace("/", "_")
        fname_md = f"{pipeline_name_slug}_{safe_name}.md" if pipeline_name_slug else f"{safe_name}.md"
        fpath = os.path.join(output_dir, fname_md)
        step_prefix = re.sub(r'[<>:"/\\|?*\s]', '_', name)[:20]
        full_prefix = f"{pipeline_name_slug}_{step_prefix}" if pipeline_name_slug else step_prefix
        exts = (".png", ".jpg", ".mp4")
        has_images = any(
            f == f"{full_prefix}{ext}" or re.match(rf"^{re.escape(full_prefix)}_v\d+{re.escape(ext)}$", f)
            for f in (os.listdir(output_dir) if os.path.isdir(output_dir) else [])
            for ext in exts
        )
        if (os.path.isfile(fpath) and os.path.getsize(fpath) > 100) or has_images:
            reason = "文字+图" if has_images else "已有输出"
            print(f"   ⏭️  {reason}，跳过")
            try:
                step_outputs[name] = Path(fpath).read_text(encoding="utf-8") if os.path.isfile(fpath) else ""
            except Exception:
                pass
            # 恢复线程 ID，让后续步骤能续上
            saved_tid = state.get("threads", {}).get(name)
            if saved_tid:
                current_tid = saved_tid
                if main_tid is None:
                    main_tid = saved_tid
            continue

        # call() 内部已通过 status 轮询等线程空闲，无需在此重试
        _img_prefix = re.sub(r'[<>:\"/\\|?*\s]', '_', name)[:16]
        text, result_tid, downloaded, cdn_urls = call(
            prompt,
            thread_id=step_tid,
            image_path=img if img else None,
            image_paths=imgs if imgs else None,
            attachment_urls=reuse_urls if reuse_urls else None,
            follow_ups=fups,
            project_id=_resolve(cfg, "project_id", None),
            ctx=CallContext(
                output_dir=output_dir,
                prefix=f"{pipeline_name_slug}_{_img_prefix}",
                label=name,
                follow_ups=fups,
                mode=step.get("mode", "thinking"),
            ),
        )

        if not text:
            print(f"   ⚠️ [{name}] 未收到回复，跳过（详情见上方错误信息）")
            continue

        # 存储本步输出
        step_outputs[name] = text

        # 记录图片（去重，同时保存本地路径和 CDN URL）
        seen = set()
        last_generated_images = []
        last_urls = []
        for d in downloaded:
            if d and d not in seen:
                seen.add(d)
                last_generated_images.append(d)
        for u in cdn_urls:
            if u and u not in last_urls:
                last_urls.append(u)

        if last_generated_images:
            count = len(last_generated_images)
            print(f"   🖼️  {count} 张")
            for d in last_generated_images:
                print(f"      {d}")

        current_tid = result_tid
        if main_tid is None:
            main_tid = result_tid   # 第一个步骤自动成为主线
        elif thread_mode == "main":
            current_tid = main_tid

        save_step(text, name, output_dir, pipeline_name_slug)

        # 保存项目状态：记录线程ID和进度
        state.setdefault("threads", {})[name] = result_tid
        state["main_tid"] = main_tid
        state["current_tid"] = current_tid
        state["updated"] = time.strftime("%Y-%m-%d %H:%M")
        try:
            Path(state_path).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

        print(f"   🔗 线程: {result_tid}")

        time.sleep(step_delay)

    # 管线结束：打印输出汇总
    # 输出汇总
    abs_output = os.path.abspath(output_dir)
    print(f"\n{'─'*60}")
    print(f"✅ {cfg.get('name', '未命名')}  —  {abs_output}")
    for name in step_outputs:
        safe = name.replace(" ", "_").replace("/", "_")
        size = len(step_outputs[name])
        fname = f"{pipeline_name_slug}_{safe}.md" if pipeline_name_slug else f"{safe}.md"
        print(f"  {fname}  {size} 字")
    if last_generated_images:
        for i, d in enumerate(last_generated_images):
            print(f"  🖼️  {os.path.basename(d)}  →  {d}")
    print(f"{'─'*60}")

    # 返回最后一个线程 ID（供交互模式使用）
    return current_tid


# ══════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════

# ── 交互模式 ──────────────────────────────────────────────────

def interactive_chat(tid: str = None, output_dir: str = None):
    """交互式 REPL：管线跑完后不退出，继续接受输入"""
    print(f"\n{'─'*60}")
    print(f"  💬 交互模式已开启")
    if tid:
        print(f"  线程: {tid}")
    print(f"  直接输入内容继续对话，输入 exit 退出")
    print(f"  也可以输入 .json 文件路径跑新管线")
    print(f"{'─'*60}\n")

    current_tid = tid
    ctx = CallContext(output_dir=output_dir) if output_dir else None

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.rstrip("\n\r ")
            if not line:
                continue
            if line.lower() in ("exit", "quit"):
                print("  再见 👋")
                break

            # 如果输入的是 JSON 文件名，跑管线
            if line.endswith(".json") and os.path.isfile(line):
                cfg = load_config(line)
                cfg["_config_path"] = line
                new_tid = mode_pipeline(cfg)
                if new_tid:
                    current_tid = new_tid
                continue

            # 否则当作消息发送到当前线程
            text, new_tid, downloaded, cdn_urls = call(
                line, thread_id=current_tid, ctx=ctx, retry=False,
                project_id=None,
            )
            if new_tid:
                current_tid = new_tid

            if text:
                print(f"\n{text}\n")
            if downloaded:
                for d in downloaded:
                    print(f"  🖼️  {d}")

        except KeyboardInterrupt:
            print("\n  再见 👋")
            break
        except EOFError:
            break


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return

    # 检查交互模式
    interactive = "-i" in sys.argv or "--interactive" in sys.argv
    auto_sync = "--auto-sync" in sys.argv
    args = [a for a in sys.argv[1:] if a not in ("-i", "--interactive", "--auto-sync")]

    # init：创建标准项目目录结构
    if args and args[0] in ("init", "--init"):
        root = args[1] if len(args) > 1 else "."
        for d in ["input", "output", "pipelines"]:
            os.makedirs(os.path.join(root, d), exist_ok=True)
        print(f"✅ 项目已初始化：{os.path.abspath(root)}")
        print(f"   input/     ← 放参考图和产品图")
        print(f"   output/    ← 产出（md + 图片 + .lovart_state.json）")
        print(f"   pipelines/ ← 放 JSON 配置文件")
        if interactive:
            interactive_chat(output_dir=os.path.join(root, "output"))
        return

    if not args:
        if interactive:
            interactive_chat()
        else:
            print("❌ 请指定 JSON 配置文件")
            sys.exit(1)
        return

    config_path = args[0]
    cfg = load_config(config_path)
    cfg["_config_path"] = config_path  # 供 batch 模式的 mark_done 用

    mode = cfg.get("mode", "ask")
    name = cfg.get("name", "未命名")

    print(f"\n📋 {name}")
    print(f"   模式: {mode}")

    modes = {
        "ask": mode_ask,
        "analyze": mode_analyze,
        "batch": mode_batch,
        "pipeline": mode_pipeline,
    }

    if mode not in modes:
        print(f"❌ 未知模式: {mode} (可用: {', '.join(modes)})")
        sys.exit(1)

    result = modes[mode](cfg)

    # 提取线程 ID（ask/analyze 返回 (text, tid)，pipeline 返回 tid）
    last_tid = None
    if mode in ("ask", "analyze"):
        text, tid = result
        last_tid = tid
        if text:
            print(f"\n{'='*60}")
            if len(text) < 5000:
                print(text)
            else:
                print(text[:3000] + f"\n\n... (截断，共 {len(text)} 字)")
            print(f"{'='*60}")
            print(f"\n✅ 完成 ({len(text)} 字) | 线程: {tid}")
        else:
            print("\n⚠️  无回复")
    elif mode == "pipeline":
        last_tid = result

    print(f"\n{'='*60}")
    print(f"  ✅ 完成！")
    print(f"{'='*60}")

    # 自动 sync（仅 pipeline 模式 + --auto-sync 标志）
    if auto_sync and mode == "pipeline":
        output_dir = _resolve(cfg, "output_dir", None)
        project_id = _resolve(cfg, "project_id", None)
        if output_dir and project_id and not (isinstance(project_id, str) and project_id.startswith("[")):
            print(f"\n  ☁️  自动同步图片到 {output_dir}...")
            try:
                import subprocess as _sp
                sync_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync_lovart_images.py")
                _sp.run([sys.executable, sync_script,
                        "--config", config_path,
                        "--output-dir", output_dir,
                        "--confirm"], timeout=300)
            except Exception as e:
                print(f"  ⚠️  自动同步失败: {e}")

    # 交互模式：进入 REPL
    if interactive:
        output_dir = cfg.get("output_dir")
        interactive_chat(tid=last_tid, output_dir=output_dir)


if __name__ == "__main__":
    main()
