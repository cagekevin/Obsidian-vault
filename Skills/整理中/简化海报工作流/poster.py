#!/usr/bin/env python3
"""
海报生成 2 层管线 + 图像反推 CLI

三层能力:
  1. 直接生成提示词        python poster.py --auto "<需求>"
  2. 双层模式（先分析再生成） python poster.py --two-pass --auto "<需求>"
  3. 图像反推              python poster.py --reverse <图片路径> [--style 详细]

环境变量:
  LLM_API_KEY    API 密钥（必填）
  LLM_API_URL    API 地址（默认 https://api.apimart.ai/v1/responses）
  LLM_MODEL      模型名（默认 gpt-5.4-mini）
"""
import os, sys, json, re, base64, argparse
from pathlib import Path

try: import requests
except: sys.exit("请先安装: pip install requests")

HERE = Path(__file__).parent

# ── 加载提示词模板 ─
_PROMPT_DIR = HERE.parent / "prompt"
_PROMPT_STYLES = {}
if _PROMPT_DIR.is_dir():
    for f in sorted(_PROMPT_DIR.glob("*.txt")):
        for enc in ("utf-8", "gbk", "utf-16"):
            try:
                text = f.read_text(encoding=enc).strip()
                if text:
                    _PROMPT_STYLES[f.stem] = text
                break
            except: continue

# ═══════════════════════════════════════════
# 第1层：需求理解与重构器
# ═══════════════════════════════════════════
LAYER1_SYSTEM = """任务说明
你的任务不是直接生成最终海报提示词，而是先对用户输入的自然语言需求进行理解、整理、纠偏、补全与结构化重写，把用户原始需求转换成一份适合后续海报提示词生成系统使用的标准需求稿。

你的核心目标是：
准确理解用户原始表达
自动识别用户真正想要的海报目标
识别参考图角色与信息层级
澄清模糊表达并做合理结构化补全
输出一份清晰、可执行、适合下游模型处理的需求稿

你输出的重点必须放在："帮后续系统更好理解用户输入"，而不是直接写最终英文 Prompt。

一、你的职责边界
你负责的是：理解用户需求、整理用户需求、补全用户需求结构、提炼传播主题、标准化图像角色定义、标准化视觉任务目标、输出结构化需求稿。
你不负责：直接生成最终海报 Prompt、直接替代后续海报提示词生成器、过早决定所有视觉细节。
你是一个需求理解与重构器，不是最终出图器。

二、适用场景
- 一句话口语化描述
- 多个要求混在一起的自然语言
- 图像角色说得不清楚
- 风格、姿势、构图、产品、文案要求混在同一句中
- 用户表达大意明确但细节不规范
- 用户有"词不达意""跳跃表达""信息不完整"的情况

三、核心任务 — 必须从用户输入中拆出以下信息：

1. 参考图角色：识别每张图角色（产品/模特/姿势/构图/风格/排版/场景），说不清时合理推断并标注"推测"

2. 任务目标：产品宣传海报/电商转化海报/品牌形象海报/模特手持产品海报等

3. 视觉风格：温馨家居/高级商业/科技感/杂志风/情绪氛围/自然生活方式/极简品牌等

4. 构图与姿势要求：姿势参考、构图参考、景别、手持关系、产品与人物互动、画面站位

5. 文案传播目标：识别真正想表达的主题而不只是表面文案
   - 例："女性也能自己修家具"→传播主张、情绪方向、文案语气

6. 约束条件：电商平台/品牌宣传/高还原/严格参考/中文文案/双语/促销感控制/产品外观保留

7. 用户没说全但下游需要的内容：合理默认补全，标注"默认补全项""推测项"

四、输出格式（必须严格遵守）

必须按以下结构输出：

【原始需求理解】
用简洁语言概括对用户需求的理解。

【参考图角色识别】
图1：[角色]
图2：[角色]
图3：[角色]
图4：[角色]
（双重用途标注"主角色+辅助角色"，不确定标注"推测角色"）

【任务目标重构】
目标明确、用途明确、产品/人物/姿势/构图/风格关系明确

【核心传播主题】
提炼海报真正要传达的核心主题

【视觉与风格方向】
海报类型、风格方向、氛围方向、商业目标

【高优先级要求】
如产品一致性、模特身份一致性、姿势迁移、构图迁移、文案主题表达

【需要下游重点处理的内容】
最容易跑偏、最需要重点控制的部分

【结构化需求稿】
可直接给下游使用的标准需求稿

五、重写原则
1. 忠于用户原意
2. 可以补结构，不能乱补意图
3. 区分"用户明确要求"和"系统推测补全"
4. 优先解决"词不达意"
5. 不直接生成最终 Prompt
6. 重点突出真正关键项

六、最终执行原则
你不是最终出图的 Prompt 生成器。你是用户自然语言需求的前置优化器。
你的价值在于：把用户说乱的话整理清楚、把用户没说清的重点提炼出来、
把图像角色关系梳理清楚、把传播主题翻译成后续模型能理解的语言。"""

# ═══════════════════════════════════════════
# 第2层：电商视觉策划大师
# ═══════════════════════════════════════════
LAYER2_SYSTEM = """你是一个专业的电商视觉策划大师。你的任务是根据用户提供的产品信息和参考图，生成一系列用于AI绘画（如Midjourney/Stable Diffusion）的详细提示词，用于制作电商详情页。

请遵循以下规则：
1. **多图参考一致性**：如果提供了参考图，请仔细分析产品的主体特征（颜色、材质、形状），并在生成的提示词中保持主体一致性。
2. **场景构建**：根据场景偏好构建场景
3. **设计风格**：严格遵循指定的视觉风格。
4. **输出格式（严格遵守）**：
   - 必须且仅输出一个纯 JSON 字符串列表 ["prompt 1", "prompt 2", ...]
   - 严禁使用 Markdown 代码块标记（如 ```json 或 ```）
   - 严禁包含任何其他解释性文字、前缀或后缀
   - 确保 JSON 格式合法，字符串内双引号需转义
5. **语言**：根据输出语言输出。
6. **数量**：必须生成指定数量的提示词。

**核心规则：卖点可视化（Visual Translation）**
用户提供的卖点包含核心营销信息（如品牌名、Slogan、抽象卖点）。你绝不能忽略这些信息，必须将其转化为具体的视觉元素：
- **品牌/文字信息**：如果卖点包含具体的品牌名或短语，请尝试将其设计为画面中的 Logotype、包装文字、霓虹灯牌或杂志标题。
- **抽象卖点转化**：将抽象形容词转化为物理特征：
  - "水润" → 水珠、液态飞溅、湿润光泽感
  - "轻薄" → 羽毛、漂浮感、透气织物
  - "遮瑕" → 对比图构图、无瑕肌肤特写
- 请务必在 Prompt 中体现这些转化后的视觉细节。"""

# ── 工具函数 ─

def image_to_base64(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    ext = Path(path).suffix.lower().lstrip(".")
    if ext in ("jpg", "jpeg"): mime = "image/jpeg"
    elif ext == "png": mime = "image/png"
    elif ext == "webp": mime = "image/webp"
    else: mime = "image/jpeg"
    return f"data:{mime};base64,{b64}"

def call_llm(system_prompt, user_input, api_key, api_url, model, image_path=None):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # 构建 input
    input_msgs = [
        {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]}
    ]

    user_content = [{"type": "input_text", "text": user_input}]
    if image_path:
        user_content.append({"type": "input_image", "image_url": image_to_base64(image_path)})

    input_msgs.append({"role": "user", "content": user_content})

    payload = {
        "model": model,
        "input": input_msgs,
        "temperature": 0.7,
        "max_output_tokens": 8192,
    }

    resp = requests.post(api_url, headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    data = resp.json()

    for item in data.get("output", []):
        for c in item.get("content", []):
            if c.get("text"): return c["text"]
    choices = data.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return json.dumps(data, ensure_ascii=False)

def extract_json_list(text):
    m = re.search(r'\[.*?\]', text, re.DOTALL)
    if m: return json.loads(m.group())
    return None

def list_styles():
    names = list(_PROMPT_STYLES.keys())
    print(f"\n  可用风格 ({len(names)}种):")
    for i, n in enumerate(names, 1):
        print(f"    {i}. {n}")

# ── 子命令 ─

def cmd_reverse(args):
    """图像反推：分析图片，输出详细描述"""
    api_key = os.environ.get("LLM_API_KEY") or sys.exit("请设置 LLM_API_KEY")
    api_url = os.environ.get("LLM_API_URL", "https://api.apimart.ai/v1/responses")
    model   = os.environ.get("LLM_MODEL", "gpt-5.4-mini")

    style = args.style or list(_PROMPT_STYLES.keys())[0]
    instruction = _PROMPT_STYLES.get(style, "")

    if args.list_styles:
        list_styles()
        return

    if not args.image:
        print("请指定图片路径或使用 --list-styles 查看可用风格")
        return

    img_path = Path(args.image)
    if not img_path.is_file():
        print(f"文件不存在: {img_path}")
        return

    print(f"\n  ⏳ 正在分析: {img_path.name}")
    print(f"  使用风格: {style}")
    result = call_llm(instruction, "请根据以上指令分析这张图片", api_key, api_url, model, image_path=str(img_path))
    print(f"\n  ✅ 反推结果:\n{result}")

    out = HERE / f"output_reverse_{img_path.stem}.md"
    out.write_text(result, encoding="utf-8")
    print(f"\n  💾 已保存到 {out}")

def cmd_generate(args):
    """生成提示词"""
    api_key = os.environ.get("LLM_API_KEY") or sys.exit("请设置 LLM_API_KEY")
    api_url = os.environ.get("LLM_API_URL", "https://api.apimart.ai/v1/responses")
    model   = os.environ.get("LLM_MODEL", "gpt-5.4-mini")

    raw = args.auto or _interactive_input()

    if args.two_pass:
        print("\n  ── 第1层：需求理解与重构 ──")
        structured = call_llm(LAYER1_SYSTEM, raw, api_key, api_url, model)
        out1 = HERE / "output_1_需求分析.md"
        out1.write_text(structured, encoding="utf-8")
        print(f"     ✅ 已保存到 {out1}")
        print("\n  ── 第2层：生成最终提示词 ──")
        result = call_llm(LAYER2_SYSTEM, structured, api_key, api_url, model)
    else:
        print("\n  ── 直接生成提示词 ──")
        result = call_llm(LAYER2_SYSTEM, raw, api_key, api_url, model)

    prompts = extract_json_list(result)
    if prompts:
        out2 = HERE / "output_prompts.json"
        with open(out2, "w", encoding="utf-8") as f:
            json.dump(prompts, f, ensure_ascii=False, indent=2)
        print(f"\n  ✅ 生成 {len(prompts)} 个提示词，已保存到 {out2}")
        for i, p in enumerate(prompts, 1):
            print(f"  [{i}] {p[:120]}...")
    else:
        print(f"\n  ⚠️  原始返回:\n{result[:1500]}")

def _interactive_input():
    print("\n" + "=" * 56)
    print("  海报提示词生成器")
    print("=" * 56)
    return (
        f"产品类型：{input('  产品类型: ') or '美妆粉底液'}\n"
        f"核心卖点：{input('  核心卖点: ') or '遮瑕持久，水润服帖'}\n"
        f"设计风格：{input('  设计风格: ') or '简约 Ins 风'}\n"
        f"场景偏好：{input('  场景偏好: ') or '混合（以使用场景为主）'}\n"
        f"输出语言：{input('  输出语言 [中文/英文]: ') or '中文'}\n"
        f"生成数量：{input('  数量 [1-20]: ') or '5'}"
    )

# ── 主入口 ─

def main():
    parser = argparse.ArgumentParser(description="海报生成 2 层管线 + 图像反推")
    sub = parser.add_subparsers(dest="mode")

    # generate
    g = sub.add_parser("generate", help="生成海报提示词")
    g.add_argument("--auto", type=str, help="快捷输入")
    g.add_argument("--two-pass", action="store_true", help="双层模式（先分析需求，再生产提示词）")

    # reverse
    r = sub.add_parser("reverse", help="图像反推分析")
    r.add_argument("image", nargs="?", type=str, help="图片路径")
    r.add_argument("--style", type=str, default="", help="提示词风格（默认第一个）")
    r.add_argument("--list-styles", action="store_true", help="列出可用风格")

    args = parser.parse_args()
    if args.mode == "reverse":
        cmd_reverse(args)
    else:
        cmd_generate(args if hasattr(args, 'auto') else argparse.Namespace(auto=None, two_pass=False))

if __name__ == "__main__":
    main()
