// scripts/check.cjs
// Step 3: 渲染完成后全面校验（叙事/合规/模板分配/输出物检测）
// 用法:
//   node scripts/check.cjs <ProjectName> [ProjectRootDir]
const fs = require('fs');
const path = require('path');

const projectName = process.argv[2];
const projectRootArg = process.argv[3];
if (!projectName) {
    console.error('❌ Fail Fast: 请提供项目名称。用法: node scripts/check.cjs <ProjectName> [ProjectRootDir]');
    process.exit(1);
}

const PROJECT_DIR = projectRootArg ? path.resolve(projectRootArg) : path.join(__dirname, '..');
const JSON_PATH = path.join(PROJECT_DIR, 'brand-spec.json');

if (!fs.existsSync(JSON_PATH)) {
    console.error(`❌ Fail Fast: 找不到 brand-spec.json (已查 ${JSON_PATH})`);
    process.exit(1);
}
const spec = JSON.parse(fs.readFileSync(JSON_PATH, 'utf-8'));

let failCount = 0;
function fail(ruleId, msg, fix) {
    console.error(`❌ FAIL #${ruleId}: ${msg}\n   👉 Fix: ${fix}`);
    failCount++;
}

const screens = Object.keys(spec.screens).sort();
const htmlPath = path.join(PROJECT_DIR, 'index.html');
const htmlContent = fs.existsSync(htmlPath) ? fs.readFileSync(htmlPath, 'utf-8') : '';
const ALLOWED_TEMPLATES = ['hero', 'list', 'compare', 'closing', 'editorial', 'focus'];
const CONVERSION_BANNED = [
    '立即购买','立即下单','立即查看','立即抢购','加购','加入购物车','加入车队',
    '领券','领红包','优惠券','满减','限时','限时特价','倒计时','错过等',
    '包邮','顺丰包邮','7天无理由','7 天无理由','7天退换','7 天退换',
    '库存','仅剩','即将售罄','疯抢','正品保证','假一赔十'
];

console.log(`========== 全面校验 ==========`);

// ── 1. JSON 完整性 ──
if (!spec.brand?.name) fail('1', 'brand.name 缺失', '补齐 brand-spec.json');
if (!spec.style) fail('1', 'style 缺失', '补齐 brand-spec.json');
if (!spec.claim_seeds || spec.claim_seeds.length < 2) fail('1', 'claim_seeds 不足 2 个', '至少写 2-4 个核心声明');

// ── 2. Claim Seeds 叙事追溯 ──
const rootSeeds = (spec.claim_seeds||[]).map(s => s.id);
let firstScreenSeeds = spec.screens[screens[0]]?.claim_seed_back || [];
const missing = rootSeeds.filter(s => !firstScreenSeeds.includes(s));
if (missing.length > 0) fail('2', `屏 01 缺少 seed: ${missing.join(',')}`, `补全 claim_seed_back`);

const seedCounts = {};
screens.forEach(id => {
    const s = spec.screens[id].claim_seed_back;
    if (!s || s.length === 0) fail('2', `屏 ${id} 缺 claim_seed_back`, '补全追溯');
    (s||[]).forEach(seed => seedCounts[seed] = (seedCounts[seed]||0) + 1);
});
if (!Object.values(seedCounts).some(c => c >= 3)) fail('2', '无主线 seed（≥3 屏）', '让至少 1 个 seed 贯穿 3 屏以上');

// ── 3. 转化词拦截 ──
screens.forEach(id => {
    const str = JSON.stringify(spec.screens[id].text_exact||{});
    CONVERSION_BANNED.forEach(w => {
        if (str.includes(w)) fail('3', `屏 ${id} 含转化词 [${w}]`, '改写为展示页语气');
    });
});

// ── 4. visual_description 解耦 ──
screens.forEach(id => {
    const vd = spec.screens[id].visual_description;
    if (!vd) fail('4', `屏 ${id} 缺 visual_description`, '补齐纯英文画面描述');
    else if (/[\u4e00-\u9fa5]/.test(vd)) fail('4', `屏 ${id} 的 visual_description 含中文`, '必须纯英文');
});

// ── 5. 模板分配 ──
let prev = null;
screens.forEach((id, i) => {
    const t = spec.screens[id].template;
    if (!ALLOWED_TEMPLATES.includes(t)) fail('5', `屏 ${id} 模板 [${t}] 非法`, `仅支持 ${ALLOWED_TEMPLATES.join(', ')}`);
    if (t === prev && t !== 'closing') fail('5', `屏 ${id} 与上屏同模板 [${t}]`, '换模板');
    if (i === 0 && t !== 'hero') fail('5', `屏 01 必须 hero`, `改为 hero`);
    if (i === screens.length-1 && t !== 'closing') fail('5', `末屏必须 closing`, `改为 closing`);
    prev = t;
});

// ── 6. HTML 输出检测 ──
if (htmlContent) {
    if (/[\u{1F300}-\u{1FAFF}]/u.test(htmlContent)) fail('6', 'HTML 含 Emoji', '删除 Emoji');
    if (/<script\b/i.test(htmlContent)) fail('6', 'HTML 含 <script>', '删除 JS');
    if (/@keyframes|animation:/i.test(htmlContent)) fail('6', 'HTML 含 CSS 动效', '删除 @keyframes');
    const bgSet = new Set(screens.map(id => spec.screens[id].background || 'default'));
    if (bgSet.size < 2) fail('6', '所有屏背景相同', '加 mod--alt-bg/dark-bg');
    const knownFonts = ['Fraunces','Playfair','Inter','Caveat','PT Serif','JetBrains Mono'];
    if (!knownFonts.some(f => htmlContent.includes(f))) fail('6', '未发现自定义字体引用', '检查 template.html 字体链接');
}

// ── 7. 截图产物检测 ──
screens.forEach(id => {
    const png = path.join(PROJECT_DIR, 'output', `screen_${id}.png`);
    if (!fs.existsSync(png)) fail('7', `screen_${id}.png 未生成`, '重跑 render.cjs');
    else {
        const size = fs.statSync(png).size;
        if (size < 2000) fail('7', `screen_${id}.png 过小 (${size}B)`, '内容可能为空，检查 JSON 数据');
    }
});

// ── 8. Prompt 产物检测 ──
screens.forEach(id => {
    const txt = path.join(PROJECT_DIR, 'output', `prompt_${id}.txt`);
    if (!fs.existsSync(txt)) fail('8', `prompt_${id}.txt 未生成`, '重跑 render.cjs');
    else {
        const content = fs.readFileSync(txt, 'utf-8').replace(/Banned:.*$/m, '');
        if (/[\u4e00-\u9fa5]/.test(content)) fail('8', `prompt_${id}.txt 含中文`, '检查 render.cjs 是否误读 text_exact');
    }
});

if (failCount === 0) {
    console.log(`✅ 全部 ${screens.length} 屏校验通过！`);
} else {
    console.error(`\n❌ ${failCount} 项失败，请按 Fix 提示修改后重跑 render.cjs + check.cjs`);
    process.exit(1);
}
