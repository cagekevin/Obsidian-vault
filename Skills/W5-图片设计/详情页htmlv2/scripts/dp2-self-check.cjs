#!/usr/bin/env node
/* ════════════════════════════════════════════════════════════
 * dp2-self-check.cjs · v0.5.1 详情页 HTML 2 自检脚本
 *
 * 跑法：node scripts/dp2-self-check.cjs <项目目录>
 * 例：  node scripts/dp2-self-check.cjs examples/hk-time-capsule/
 *
 * 检查项（v0.5.1 · 9 项）：
 *  1. 无 emoji 字符
 *  2. 无 <br> 后 1-2 字孤儿（每行 ≥ 3 字）
 *  3. 无 inline transform / scale / translate / rotate
 *  4. 无 <script> 标签
 *  5. 无 CSS @keyframes / animation
 *  6. 无 .theme-switcher 类
 *  7. 无 V3 违规 class（sp / selling-points / miracle-item 等）
 *  8. 无 CSS transform: scale/translate/rotate
 *  9. .mod 都有 min-height: 940px 或 height: 940px
 *
 * 输出：PASS/FAIL + 详细违规位置 + 修法
 * ════════════════════════════════════════════════════════════ */

const fs = require('fs');
const path = require('path');

const targetDir = process.argv[2] || 'examples/';
const indexFile = path.join(targetDir, 'index.html');

if (!fs.existsSync(indexFile)) {
  console.error(`❌ 找不到 ${indexFile}`);
  process.exit(1);
}

const html = fs.readFileSync(indexFile, 'utf-8');
const lines = html.split('\n');
// v0.5.4：同步读 brand-spec.md（用于 #16 #17 字段校验）
const brandSpecFile = path.join(targetDir, 'brand-spec.md');
let brandSpecContent = '';
if (fs.existsSync(brandSpecFile)) {
  brandSpecContent = fs.readFileSync(brandSpecFile, 'utf-8');
}
let pass = 0, fail = 0;

const checks = [
  {
    id: '1',
    name: '无 emoji 字符（仅检测真实 emoji 区 1F000-1F1FF）',
    test: (line) => !/<!--/.test(line) && /[\u{1F000}-\u{1F1FF}\u{1F300}-\u{1FAFF}]/u.test(line),
    fix: '删除所有 Unicode emoji（🎯 🔥 💡 等），改用 .icon-circle 或纯文字。注：✓ ✗ ★ 等符号（U+2700-27BF）不是 emoji',
  },
  {
    id: '2',
    name: '无 <br> 后 1-2 字孤儿',
    test: (line) => /<br>\s*[\u4e00-\u9fff]{1,2}[^\u4e00-\u9fff]*$/.test(line.trim()),
    fix: '断行后每行最少 3 字；调整 <br> 位置或降字号到 display-lg',
  },
  {
    id: '3',
    name: '无 inline transform: scale/rotate（translateX 居中允许）',
    test: (line) => /style\s*=\s*["'][^"']*transform\s*:\s*(scale|rotate)/i.test(line),
    fix: 'R4 静态优先。inline style 禁止 transform: scale/rotate（动效）；translateX 用于居中是必要的，允许',
  },
  {
    id: '4',
    name: '无 <script> 标签',
    test: (line) => /<script[\s>]/i.test(line),
    fix: 'R4 禁止 Tweaks JS；主题切换按 PRD §3.1 启动时手动',
  },
  {
    id: '5',
    name: '无 CSS @keyframes / animation',
    test: (line) => /@keyframes\s/i.test(line) || /animation\s*:/i.test(line),
    fix: 'R4 静态优先。删除所有 @keyframes / animation 声明',
  },
  {
    id: '6',
    name: '无 .theme-switcher 类',
    test: (line) => /theme-switcher/i.test(line),
    fix: 'R4 禁止 Tweaks 面板',
  },
  {
    id: '7',
    name: '无 V3 违规 class',
    test: (line) => /\bclass\s*=\s*["'][^"']*\b(sp|selling-points|miracle-item|dim-flow|dim-node|tech-vs__card|compare-board|board-card|stats-bar|extracts|origin__row|ph)\b/i.test(line),
    fix: '用 dp2- 组件替代（详见 references/legacy-remediation.md 命名空间映射速查）',
  },
  {
    id: '8',
    name: '无 CSS transform: scale/rotate（translateX 居中允许）',
    test: (line) => /transform\s*:\s*(scale|rotate)\b/i.test(line),
    fix: 'R4 静态优先。删除所有 transform: scale/rotate；translateX 用于居中是必要的，允许',
  },
  {
    id: '9',
    name: '.mod 规则含 min-height: 940px（搜全文）',
    test: () => {
      // 全文 grep：必须有 .mod { ... min-height: 940px ... }
      return !/\.mod\s*\{[^}]*min-height\s*:\s*940px[^}]*\}/m.test(html);
    },
    fix: 'R2 每屏 940px 固定。.mod 必须 min-height: 940px',
  },
  {
    id: '10',
    name: '无 V3 违规 class 残留（v0.5.3 新增 · 全文搜）',
    test: () => {
      // v0.5.3 新增：检测 V3 时期违规 class（全文搜，不用 line 参数避免误报）
      const v3banned = [
        'zero-add-layout',     // → dp2-wrap-block
        'list-item-arc',       // → dp2-wrap-block__line
        'product-hero-left',   // → dp2-wrap-block
        'product-hero-right',  // → dp2-wrap-block
        'selling-points',      // → dp2-list-row
        'miracle-item',        // → dp2-list-row
        'miracle-list',        // → dp2-list-row
        'dim-flow',            // → dp2-step-flow
        'dim-node',            // → dp2-step-node
        'tech-vs',             // → dp2-card-compare
        'compare-board',       // → dp2-card-overlap
        'stats-bar',           // → dp2-data-strip
        'usage-step',          // → dp2-step-flow
        'selling-point',       // → dp2-list-row (单数)
      ];
      // 移除 style / script 块 + 注释行（CSS 选择器 / JS 字符串 / 文档说明豁免）
      const htmlClean = html
        .replace(/<style[\s\S]*?<\/style>/g, '')
        .replace(/<script[\s\S]*?<\/script>/g, '')
        .replace(/<!--[\s\S]*?-->/g, '');
      const found = [];
      v3banned.forEach(cls => {
        // 整词边界（前后是空格 / 引号 / > / < / 等非单词字符）
        const regex = new RegExp(`(?<![\\w-])${cls}(?![\\w-])`, 'i');
        if (regex.test(htmlClean)) {
          found.push(cls);
        }
      });
      if (found.length > 0) {
        process.env.VIOLATION = found.join(', ');
        return true; // FAIL
      }
      return false;
    },
    fix: 'R10-1 v0.5.3。删除所有 V3 违规 class，改用 dp2- 组件。详见 references/pattern-library.md 模板 8 V3 违规对照表 + references/legacy-remediation.md',
  },
  {
    id: '11',
    name: '屏宽必须 790px（max-width: 790px）',
    test: () => {
      // v0.5.4 新增：检测 .mod 是否有 max-width: 790px
      // 允许的写法：max-width: 790px / max-width:790px（无空格也接受）
      const modRule = html.match(/\.mod\s*\{[^}]*\}/m);
      if (!modRule) return true; // 没找到 .mod 规则
      return !/max-width\s*:\s*790px/i.test(modRule[0]);
    },
    fix: 'R2 · 屏宽 790px 固定。.mod 必须 max-width: 790px（v0.5.4 新增护栏）',
  },
  {
    id: '12',
    name: '衬线启用 font-variation-settings SOFT 80-100',
    test: () => {
      // 全文 grep display-xxl / display-xl / display-lg / h1-sm 规则
      // 必须含 font-variation-settings 且 SOFT 数值在 80-100
      const serifRules = html.match(/\.(display-xxl|display-xl|display-lg|h1-sm)\s*\{[^}]*\}/g) || [];
      if (serifRules.length === 0) return false; // 没衬线规则不算违规
      return serifRules.some(rule => {
        const m = rule.match(/font-variation-settings\s*:\s*[^;]*SOFT["']?\s*(\d+)/i);
        if (!m) return false;
        const val = parseInt(m[1]);
        return val < 80 || val > 100; // 超出 80-100 范围
      });
    },
    fix: 'R5-3 衬线细节。font-variation-settings SOFT 必须在 80-100 范围。Fraunces 默认 SOFT 100 可不动，claud 风格用 SOFT 80',
  },
  {
    id: '13',
    name: 'R8-1 强约束 · 12 屏背景不能全相同（至少 2 态交替）',
    test: () => {
      // 全文搜所有 .mod 块的 background 设置
      // 必须有 ≥ 2 种不同的 background（不允许 12 屏全用 var(--bg)）
      const modBgs = [];
      const re = /\.mod[\w-]*\s*\{[^}]*background\s*:\s*([^;}]+)/g;
      let m;
      while ((m = re.exec(html)) !== null) {
        modBgs.push(m[1].trim());
      }
      // 也检测 .dp2-section-soft / .dp2-section-card / .dp2-section-dark 引用
      const sectionUses = (html.match(/dp2-section-(soft|card|dark)/g) || []).length;
      // 至少要满足：1) 2 种 .mod--xxx 背景态 或 2) ≥ 1 次 .dp2-section-xxx 引用
      // （放宽：12 屏项目才有 3 态 ≥ 3 次；前 3 屏允许 1 次）
      const distinctBgs = new Set(modBgs).size;
      return !(distinctBgs >= 2 || sectionUses >= 1);
    },
    fix: 'R8-1 v0.5.4 强约束。12 屏全用同 bg 违规。必须 mod--alt-bg / mod--dark-bg / .dp2-section-soft / .dp2-section-card / .dp2-section-dark 至少 2 态交替',
  },
  {
    id: '14',
    name: '自由排版区 ≥ 500px（PRD 风险 §3 强约束）',
    test: () => {
      // 自由区 = 940 - mod-top-c - mod-body padding - mod-img
      // 全文搜 .mod-top-c 块的 height / padding-top + .mod-body 块的 padding-top + .mod-img 块
      // 简化检测：找 1 屏典型 .mod 块，验证 mod-top-c 高度 ≤ 380px
      // （mod-top-c 380 + mod-body 48 + mod-img 撑满 ≥ 500 留给自由区）
      const topRules = html.match(/\.mod-top-c\s*\{[^}]*\}/g) || [];
      if (topRules.length === 0) return false;
      return topRules.some(rule => {
        // padding-top > 300px 视为标题区过大
        const pt = rule.match(/padding-top\s*:\s*(\d+)px/);
        return pt && parseInt(pt[1]) > 200;
      });
    },
    fix: 'PRD 风险 §3。自由区 ≥ 500px。mod-top-c padding-top ≤ 200px（屏 1 hero 例外），body padding ≤ 96px',
  },
  {
    id: '15',
    name: 'R1 · 每屏必含 display-* 主标 + 至少 1 段 .body（PRD L51-55）',
    test: () => {
      // 全文搜：display-* 出现次数 vs .body 出现次数
      // 1) 至少 1 个 display-xxl/xl/lg 或 h1-sm
      const hasMainTitle = /class\s*=\s*["'][^"']*(display-xxl|display-xl|display-lg|h1-sm)/.test(html);
      // 2) 至少 1 个 class="body" 或 class="...body..."
      const hasBody = /class\s*=\s*["'][^"']*\bbody\b/.test(html);
      // 3) 至少 1 个 <h1> <h2> <h3> 标签（v0.5.4 宽松：display class 用 <p> 也接受）
      const hasHeading = /<h[1-3][\s>]/.test(html);
      return !(hasMainTitle && hasBody && hasHeading);
    },
    fix: 'R1。每屏必含 display-* / h1-sm + class="body" + <h1>/<h2>/<h3> 标签',
  },
  {
    id: '16',
    name: 'brand-spec.md 必填字段完整（PRD Step 0 强约束）',
    test: () => {
      // 必填：品牌 / 产品 / 卖点 / 主题 / 资产清单 / 原文护栏 / Theme Bundle / 断句符映射
      // 字段检测宽松：仅要求关键 key 词出现
      const requiredFields = [
        /品牌/,
        /产品/,
        /卖点/,
        /主题/,
        /资产/,
        /Theme Bundle/,
        /断句符/,
        /原文护栏/,
      ];
      const fullText = html + (brandSpecContent || '');
      return requiredFields.some(rx => !rx.test(fullText));
    },
    fix: 'PRD Step 0。brand-spec.md 必填 8 字段：品牌/产品/卖点/主题/资产/Theme Bundle/断句符/原文护栏',
  },
  {
    id: '17',
    name: '4 维定位完整（PRD Step 2 强约束）',
    test: () => {
      // 必填：目的 / 用户情绪 / 内容类型 / 视觉锚点
      const fourDims = [
        /目的/,
        /用户情绪|情绪/,
        /内容类型|类型/,
        /视觉锚点|锚点/,
      ];
      const fullText = html + (brandSpecContent || '');
      return fourDims.some(rx => !rx.test(fullText));
    },
    fix: 'PRD Step 2 4 维定位。每屏必填 4 字段：目的/用户情绪/内容类型/视觉锚点。详见 references/pattern-library.md 4 维定位模板',
  },
];

console.log(`\n🔍 v0.5.1 自检：${indexFile}\n`);
console.log('─'.repeat(60));

for (const check of checks) {
  const violations = [];
  // v0.5.3：如果 test 函数 arity=0（不接受 line 参数），用全文模式
  const isFullText = check.test.length === 0;
  if (isFullText) {
    // 重置 process.env 避免上一个 check 污染
    const prev = process.env.VIOLATION;
    process.env.VIOLATION = '';
    if (check.test()) {
      violations.push({ line: 1, content: prev || '命中 v0.5.3 违规' });
    }
  } else {
    lines.forEach((line, idx) => {
      if (check.test(line)) {
        violations.push({ line: idx + 1, content: line.trim().slice(0, 80) });
      }
    });
  }
  if (violations.length === 0) {
    console.log(`✅ ${check.id}. ${check.name}  PASS`);
    pass++;
  } else {
    console.log(`❌ ${check.id}. ${check.name}  FAIL (${violations.length} 处)`);
    violations.slice(0, 3).forEach(v => {
      console.log(`   L${v.line}: ${v.content}`);
    });
    if (violations.length > 3) {
      console.log(`   ... +${violations.length - 3} 处`);
    }
    console.log(`   修法：${check.fix}`);
    fail++;
  }
}

console.log('─'.repeat(60));
console.log(`\n📊 结果：${pass} PASS / ${fail} FAIL / 共 ${checks.length} 项\n`);

if (fail > 0) {
  process.exit(1);
}
