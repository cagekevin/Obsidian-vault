#!/bin/bash
# 外部AI审查自动化脚本
# 用法: bash scripts/auto_review.sh <产品文案文件路径>
#
# 前提条件:
#   1. Chrome 已在 9222 端口运行远程调试
#   2. 目标 AI 网站已登录
#   3. 三个源文件路径正确

set -e

PRODUCT_COPY_FILE="$1"
TEMPLATE_FILE="/Users/kevin/Nutstore Files/我的坚果云/skills-main/skills/工作效率类/W5-图片设计/详情页html/template.html"
REFERENCE_FILE="/Users/kevin/Nutstore Files/我的坚果云/skills-main/skills/工作效率类/W5-图片设计/详情页html/设计系统_reference.md"
SKILL_FILE="/Users/kevin/Nutstore Files/我的坚果云/skills-main/skills/工作效率类/W5-图片设计/详情页html/SKILL.md"
CDP="--cdp 9222"
AI_URL="https://yiyan.baidu.com"

if [ ! -f "$PRODUCT_COPY_FILE" ]; then
  echo "❌ 产品文案文件不存在: $PRODUCT_COPY_FILE"
  exit 1
fi

echo "🚀 开始自动化审查流程..."
echo "目标 AI: $AI_URL"
echo "产品文案: $PRODUCT_COPY_FILE"
echo ""

# 打开目标 AI 网站
agent-browser $CDP open "$AI_URL"
sleep 3

# 点击"新对话"（如果有）
echo "📩 消息 1: 打招呼 + 要求读文件"
agent-browser $CDP type @e130 "我接下来要和你做一次设计系统的迭代审查。请先读完以下三个文件，读完回复【已读完】，不要做任何分析。"

# 发送 template.html
FILES_CONTENT="文件1 — 基础模板（template.html）："
FILES_CONTENT+="\n\`\`\`\n$(cat $TEMPLATE_FILE)\n\`\`\`"
FILES_CONTENT+="\n\n文件2 — 组件手册（设计系统_reference.md）："
FILES_CONTENT+="\n\`\`\`\n$(cat $REFERENCE_FILE)\n\`\`\`"
FILES_CONTENT+="\n\n文件3 — 操作流程（SKILL.md）："
FILES_CONTENT+="\n\`\`\`\n$(cat $SKILL_FILE)\n\`\`\`"
FILES_CONTENT+="\n\n读完直接回复：已读完"

# 这里需要分多次发送因为文件很大
echo "⏳ 正在发送文件内容..."
agent-browser $CDP keyboard inserttext "$FILES_CONTENT"
sleep 2
agent-browser $CDP press "Enter"

echo "⏳ 等待对方读取文件..."
sleep 30

echo "📩 消息 2: 发送产品文案 + 要求生成"
COPY_TEXT=$(cat "$PRODUCT_COPY_FILE")
MSG2="好。现在用这套系统帮我生成一个产品的详情页。\n\n产品：智能充电器\n风格：冷峻硬核（默认风格，删除<link>行）\n\n文案如下：\n$COPY_TEXT\n\n规则重申：\n- 零内联样式，仅对比栏color:var(--text-muted)允许\n- 核心数据必须用.num+.gold\n- 多组内容用rule分割\n- 连续均分网格不超过3屏\n- 内容不足时增加真实描述，不用占位图填充\n- 首屏第一个.mod加page-hero class\n\n做完直接输出完整HTML。"
agent-browser $CDP keyboard inserttext "$MSG2"
sleep 2
agent-browser $CDP press "Enter"

echo "⏳ 等待生成页面..."
sleep 60

echo "📩 消息 3: 切换视角 + 审查系统"
MSG3='好，页面生成了。\n\n现在请你切换到设计师/架构师视角，不要看刚才生成的页面内容好不好卖，而是审视我发给你的那三个文件本身。\n\n【不可触碰的根基】\n1. CSS变量体系\n2. 字体隔离\n3. 字号铁律\n4. 模块高度940px\n5. 布局骨架\n6. 间距常量\n7. 填充率75%\n8. 内联样式禁令\n\n【问题清单】\n1. 模板的演示屏和预制区块在版式节奏上有什么可改进的？\n2. reference.md的规则哪里写得太抽象？\n3. 预制区块缺什么高频场景？\n4. 组件组合范式缺什么常见搭配？\n5. 这套体系在设计层面最大的弱项是什么？\n\n【输出格式】\n建议#N\n目标文件：\n具体位置：\n修改类型：\n修改内容：\n理由：'
agent-browser $CDP keyboard inserttext "$MSG3"
sleep 2
agent-browser $CDP press "Enter"

echo "⏳ 等待审查结果（可能需要2-3分钟）..."
sleep 120

echo "📩 消息 5: 收尾确认"
agent-browser $CDP keyboard inserttext "收到，感谢。"
sleep 1
agent-browser $CDP press "Enter"

echo ""
echo "✅ 自动化审查流程完成！"
echo "请手动查看浏览器中的对话历史，获取外部AI的全部反馈。"
