#!/usr/bin/env python3
"""
聊天记录概览分析工具

用法:
  python chat_overview.py overview <聊天记录.json>        # 话题概览
  python chat_overview.py info <聊天记录.json>             # 关键信息提取
  python chat_overview.py deepdive <聊天记录.json> <关键词>  # 深入分析

输入格式: WeFlow 导出的 JSON 格式
输出: 终端打印结构化分析结果
"""

import re
import sys
import json
import math
from collections import defaultdict, Counter
from datetime import datetime, timedelta

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

URL_PATTERN = re.compile(r'https?://[^\s,，。、；;）\)\]]+')
REPLY_PATTERN = re.compile(r'^↩ .+?：')


def load_chat(filepath):
    """加载 WeFlow JSON 格式的聊天记录"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    group_name = data.get('displayName', '未知群')
    messages = []
    for msg in data.get('messages', []):
        if msg.get('typeName') in ('system', 'unknown'):
            continue
        try:
            ts = datetime.strptime(msg['datetime'], '%Y-%m-%d %H:%M:%S')
        except:
            continue
        
        content = msg.get('content', '').strip()
        # 过滤纯媒体/系统消息
        if content in ('[表情]', '[图片]', '[语音]', '[视频]', '[动画表情]'):
            continue
        if content.startswith('"') and ('拍了拍' in content or '撤回' in content):
            continue
        if content == '当前微信版本不支持展示该内容，请升级至最新版本。':
            continue
        
        # 去掉回复前缀 "↩ xxx："
        clean_content = REPLY_PATTERN.sub('', content).strip()
        
        messages.append({
            'time': ts,
            'date': ts.strftime('%Y-%m-%d'),
            'weekday': ts.weekday(),
            'hour': ts.hour,
            'speaker': msg.get('senderName') or msg.get('senderWxid') or '未知',
            'content': clean_content,
            'raw_content': content,
        })
    
    return group_name, messages


def extract_urls(text):
    return URL_PATTERN.findall(text)


def build_daily_summary(messages):
    """按天统计"""
    daily = defaultdict(lambda: {
        'count': 0, 'speakers': set(), 'texts': [], 'urls': [], 'all_content': ''
    })
    for msg in messages:
        day = msg['date']
        daily[day]['count'] += 1
        daily[day]['speakers'].add(msg['speaker'])
        daily[day]['texts'].append(msg['content'])
        daily[day]['all_content'] += ' ' + msg['content']
        urls = extract_urls(msg['content'])
        daily[day]['urls'].extend(urls)
    return daily


def cmd_overview(filepath):
    """话题概览"""
    group_name, messages = load_chat(filepath)
    if not messages:
        print("❌ 未解析到有效消息")
        return
    
    total_days = len(set(m['date'] for m in messages))
    date_range = f"{messages[0]['date']} ~ {messages[-1]['date']}"
    
    speaker_counter = Counter(m['speaker'] for m in messages)
    top_speakers = speaker_counter.most_common(10)
    
    daily = build_daily_summary(messages)
    sorted_days = sorted(daily.keys())
    
    # 总链接
    all_urls = []
    for d in daily.values():
        all_urls.extend(d['urls'])
    url_counter = Counter(all_urls)
    
    print(f"\n{'='*60}")
    print(f"  📊 {group_name}")
    print(f"{'='*60}")
    print(f"  时间跨度: {date_range}  ({total_days}天)")
    print(f"  总消息数: {len(messages)}")
    print(f"  日均消息: {len(messages)//max(total_days,1)}")
    print(f"{'='*60}")
    
    print(f"\n  👥 活跃成员 TOP10")
    print(f"  {'─'*40}")
    for name, count in top_speakers:
        bar = '█' * min(count // max(top_speakers[0][1], 1) * 20, 20)
        pct = count * 100 // len(messages)
        print(f"  {name:<20} {bar} {count} ({pct}%)")
    
    print(f"\n  📅 每日话题")
    print(f"  {'─'*60}")
    for day in sorted_days[-30:]:  # 最近30天
        info = daily[day]
        wd = datetime.strptime(day, '%Y-%m-%d').weekday()
        wd_name = ['一','二','三','四','五','六','日'][wd]
        
        # 提取该日关键词（简单词频）
        words = re.findall(r'[\u4e00-\u9fff\w]+', info['all_content'])
        word_freq = Counter(w.lower() for w in words if len(w) > 1)
        # 过滤常见词
        stopwords = {'的','了','在','是','我','有','和','就','不','人','都','一','一个',
                     '上','也','很','到','说','要','去','你','会','着','没有','看','好',
                     '自己','这','他','她','它','们','那','这个','那个','什么','怎么',
                     '可以','但是','因为','所以','如果','还是','不是','吗','啊','呢',
                     '吧','哦','嗯','哈','哈哈','ok','OK','em','emmm'}
        for sw in stopwords:
            word_freq.pop(sw, None)
        
        top_words = word_freq.most_common(5)
        keywords = ' '.join(f'{w}' for w, c in top_words if c >= 2)
        if not keywords:
            keywords = '(闲聊/媒体)'
        
        url_count = len(info['urls'])
        url_info = f' 🔗{url_count}' if url_count > 0 else ''
        
        print(f"  {day} 周{wd_name}  {info['count']}条{url_info}")
        print(f"      {len(info['speakers'])}人参与 · 关键词: {keywords}")
    
    if url_counter:
        print(f"\n  🔗 出现最多的链接")
        print(f"  {'─'*60}")
        for url, count in url_counter.most_common(10):
            short = url if len(url) < 70 else url[:67] + '...'
            print(f"  ({count}x) {short}")


def cmd_info(filepath):
    """关键信息提取：链接、活动、工具"""
    group_name, messages = load_chat(filepath)
    if not messages:
        print("❌ 未解析到有效消息")
        return
    
    # 提取所有链接
    all_links = []
    for msg in messages:
        urls = extract_urls(msg['content'])
        for url in urls:
            all_links.append((msg['date'], msg['speaker'], url))
    
    print(f"\n{'='*60}")
    print(f"  🔗 {group_name} - 关键信息")
    print(f"{'='*60}")
    
    if all_links:
        print(f"\n  链接 ({len(all_links)}个)")
        print(f"  {'─'*60}")
        # 按域名归类
        by_domain = defaultdict(list)
        for date, speaker, url in all_links:
            domain = re.findall(r'https?://([^/]+)', url)
            domain_name = domain[0] if domain else '未知'
            by_domain[domain_name].append((date, speaker, url))
        
        for domain, items in sorted(by_domain.items(), key=lambda x: -len(x[1])):
            print(f"\n  [{domain}] ({len(items)}次)")
            for date, speaker, url in items[:5]:  # 每个域名最多5条
                short = url if len(url) < 80 else url[:77] + '...'
                print(f"    {date} {speaker}: {short}")
            if len(items) > 5:
                print(f"    ...还有{len(items)-5}条")
    else:
        print("\n  未发现链接")


def cmd_deepdive(filepath, keyword):
    """深入分析某个话题"""
    group_name, messages = load_chat(filepath)
    if not messages:
        print("❌ 未解析到有效消息")
        return
    
    keyword_lower = keyword.lower()
    related = []
    for msg in messages:
        if keyword_lower in msg['content'].lower():
            related.append(msg)
    
    if not related:
        print(f"\n未找到包含「{keyword}」的消息")
        return
    
    # 按天分组
    by_day = defaultdict(list)
    for msg in related:
        by_day[msg['date']].append(msg)
    
    print(f"\n{'='*60}")
    print(f"  🔍 「{keyword}」相关讨论 ({len(related)}条)")
    print(f"{'='*60}")
    
    # 统计谁在聊
    speaker_counter = Counter(m['speaker'] for m in related)
    print(f"\n  参与讨论: {', '.join(f'{n}({c})' for n, c in speaker_counter.most_common())}")
    print()
    
    # 按时间线输出
    for date in sorted(by_day.keys(), reverse=True):
        msgs = by_day[date]
        print(f"  [{date}] ({len(msgs)}条)")
        for msg in msgs:
            content = msg['content']
            if len(content) > 120:
                content = content[:117] + '...'
            print(f"    {msg['time'].strftime('%H:%M')} {msg['speaker']}: {content}")
        print()


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  python chat_overview.py overview <聊天记录.json>")
        print("  python chat_overview.py info <聊天记录.json>")
        print("  python chat_overview.py deepdive <聊天记录.json> <关键词>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    filepath = sys.argv[2]
    
    if cmd == 'overview':
        cmd_overview(filepath)
    elif cmd == 'info':
        cmd_info(filepath)
    elif cmd == 'deepdive' and len(sys.argv) >= 4:
        cmd_deepdive(filepath, sys.argv[3])
    else:
        print(f"未知命令: {cmd}")


if __name__ == '__main__':
    main()
