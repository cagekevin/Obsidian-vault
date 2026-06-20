// scripts/render.cjs
const fs = require('fs');
const path = require('path');

// 用法：
//   node scripts/render.cjs <ProjectName>                  (默认：项目在 <root>/Temp/<ProjectName>/，JSON 在 <root>/specs/brand-spec.json)
//   node scripts/render.cjs <ProjectName> <ProjectRootDir> (项目目录指向任意位置，JSON 在 <ProjectRootDir>/specs/brand-spec.json)
const projectName = process.argv[2];
const projectRootArg = process.argv[3];
if (!projectName) {
    console.error('❌ Fail Fast: 请提供项目名称。用法: node scripts/render.cjs <ProjectName> [ProjectRootDir]');
    process.exit(1);
}

const PROJECT_DIR = projectRootArg
    ? path.resolve(projectRootArg)
    : path.join(__dirname, '..', 'Temp', projectName);
const HTML_PATH = path.join(PROJECT_DIR, 'index.html');
const OUTPUT_DIR = path.join(PROJECT_DIR, 'output');

// JSON 在项目根目录下
const JSON_PATH = path.join(PROJECT_DIR, 'brand-spec.json');


if (!fs.existsSync(JSON_PATH)) {
    console.error(`❌ Fail Fast: 找不到 brand-spec.json (已查 specs/ 和根目录): ${JSON_PATH}`);
    process.exit(1);
}
const spec = JSON.parse(fs.readFileSync(JSON_PATH, 'utf-8'));

// ==========================================
// 主题自动注入：JSON 里指定 theme，脚本自动复制对应 CSS
// ==========================================
const THEME_MAP = {
    'pilgrim-dawn': 'theme-pilgrim-dawn.css',
    'dark-nexus': 'theme-dark-nexus.css',
    'swiss-industrial': 'theme-swiss-industrial.css',
    'apothecary-folio': 'theme-apothecary-folio.css',
    'data-ink': 'theme-data-ink.css',
    'brutalist': 'theme-brutalist.css',
    'mid-century': 'theme-mid-century.css',
    'cupertino': 'theme-cupertino.css',
    'data-terminal': 'theme-data-terminal.css',
    'lyrical-ocean': 'theme-lyrical-ocean.css',
    'parisian-chic': 'theme-parisian-chic.css',
};

if (spec.theme) {
    const themeFile = THEME_MAP[spec.theme];
    if (!themeFile) {
        console.error(`❌ Fail Fast: 未知主题 "${spec.theme}"。可选: ${Object.keys(THEME_MAP).join(', ')}`);
        process.exit(1);
    }
    const SOURCE_THEMES_DIR = path.join(__dirname, '..', 'tokens');
    const SOURCE_THEME = path.join(SOURCE_THEMES_DIR, themeFile);
    if (!fs.existsSync(SOURCE_THEME)) {
        console.error(`❌ Fail Fast: 主题源文件不存在: ${SOURCE_THEME}`);
        process.exit(1);
    }
    const PROJECT_TOKENS_DIR = path.join(PROJECT_DIR, 'tokens');
    if (!fs.existsSync(PROJECT_TOKENS_DIR)) fs.mkdirSync(PROJECT_TOKENS_DIR, { recursive: true });
    fs.copyFileSync(SOURCE_THEME, path.join(PROJECT_TOKENS_DIR, 'theme.css'));
    console.log(`🎨 主题已注入: ${spec.theme} → ${themeFile}`);
}

const allowedRatios = ['9:21', '9:16'];
if (!allowedRatios.includes(spec.style.ratio)) {
    console.error(`❌ Fail Fast: style.ratio 必须为 9:21 或 9:16，当前: "${spec.style.ratio}"`);
    process.exit(1);
}

if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

// ==========================================
// 工具函数：视觉字数计算 (用于动态字号推断)
// ==========================================
function getVisualLength(str) {
    if (!str) return 0;
    let len = 0;
    for (let i = 0; i < str.length; i++) {
        len += str.charCodeAt(i) > 255 ? 1 : 0.5;
    }
    return Math.ceil(len);
}

// ==========================================
// Phase 1: 渲染 HTML (内容感知型自适应引擎)
// ==========================================
function generateHTML() {
    console.log(`[1/3] 正在启动内容感知引擎，构建动态大牌 DOM 树...`);
    // 每次都从干净模板重新读取，避免历史注入累积污染
    const TEMPLATE_PATH = path.join(__dirname, '..', 'templates', 'template.html');
    let htmlContent = fs.readFileSync(TEMPLATE_PATH, 'utf-8');

    // 注入情绪手写体
    const fontLink = `<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;600&display=swap" rel="stylesheet">\n</head>`;
    htmlContent = htmlContent.replace('</head>', fontLink);

    const p = spec.style.palette || {};
    const viewportHeight = spec.style.ratio === '9:16' ? '1280px' : '1680px';
    
    const cssVars = `
        :root {
            --color-accent: ${p.accent || '#C5A26B'};
            --color-gold: ${p.accent || '#C5A26B'};
            --color-bg-alt: ${p.bg_alt || '#F4EFE3'};
            --color-cream: ${p.bg_alt || '#F4EFE3'};
            --color-text: ${p.text || '#2A1F1A'};
            --color-sub: ${p.sub || '#7A6E67'};
        }
        .mod { ${spec.style.height_mode === 'auto' ? 'min-height: auto; height: auto;' : `min-height: ${viewportHeight};`} }
        ${spec.style.height_mode === 'auto' ? '.mod--hero { display: flex; flex-direction: column; } .mod--hero .mod-hero-bg { position: relative; min-height: 50vh; } .mod--hero .mod-hero-overlay { margin-top: 0; padding-top: 0; }' : ''}
        .mod-hero-bg { position: absolute; inset: 0; z-index: 0; }
        .mod-hero-overlay { position: relative; z-index: 10; }
    `;
    htmlContent = htmlContent.replace('/* CSS_VARS_INJECTION */', cssVars);

    let screensHtml = '';
    const screens = Object.keys(spec.screens).sort();

    screens.forEach(id => {
        const s = spec.screens[id];
        const bgClass = s.background === 'default' ? '' : (s.background || '');
        const text = s.text_exact || {};
        
        // 动态字号感应：根据标题长短决定字号，绝对防爆
        const titleLen = getVisualLength(text.headline);
        let titleClass = 'display-xl'; // 默认安全字号
        if (titleLen <= 8) titleClass = 'display-xxl'; // 极简短标，放大震撼
        else if (titleLen > 16) titleClass = 'display-lg'; // 超长标题，自动降级防破版
        
        screensHtml += `\n\n<div class="mod ${bgClass}" id="screen-${id}">`;
        
        // ------------------------------------------------
        // 模板 A：Hero 满铺主视觉
        // ------------------------------------------------
        if (s.template === 'hero') {
            screensHtml += `
            <div class="mod-hero-bg">
                <div class="dp2-mock dp2-mock--hero" style="height: 100%; border:none;"><span>[Asset: Screen ${id} - 沉浸式主视觉底图]</span></div>
                <div style="position:absolute; inset:0; background: linear-gradient(to bottom, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 40%, rgba(255,255,255,0.85) 100%); z-index:1;"></div>
            </div>`;
            
            screensHtml += `<div class="mod-top-c mod-hero-overlay" style="padding-top: var(--sp-10); margin-top: auto; margin-bottom: var(--sp-6);">`;
            if (text.kicker) screensHtml += `<span class="kicker">${text.kicker}</span>`;
            if (text.headline) screensHtml += `<h1 class="${titleClass}">${text.headline}</h1>`;
            if (text.deco_en) {
                screensHtml += `<div class="deco-line"></div>`;
                screensHtml += `<span class="deco-en">${text.deco_en}</span>`;
            }
            if (text.subheadline) screensHtml += `<p class="h1-sm" style="margin-top: 12px;">${text.subheadline}</p>`;
            
            if (text.tags) {
                screensHtml += `<div style="margin-top: 48px; display:flex; flex-wrap:wrap; justify-content:center; gap: 12px; max-width: 90%;">`;
                text.tags.forEach(tag => screensHtml += `<span class="tag-item" style="background:rgba(255,255,255,0.6); backdrop-filter:blur(4px);">${tag}</span>`);
                screensHtml += `</div>`;
            }
            screensHtml += `</div>`;
        } 
        // ------------------------------------------------
        // 模板 B：List 智能多态图文引擎
        // ------------------------------------------------
        else if (s.template === 'list') {
            screensHtml += `<div class="mod-top-c">`;
            if (text.kicker) screensHtml += `<span class="kicker">${text.kicker}</span>`;
            if (text.headline) screensHtml += `<h2 class="${titleClass}">${text.headline}</h2>`;
            if (text.deco_en) {
                screensHtml += `<div class="deco-line"></div>`;
                screensHtml += `<span class="deco-en">${text.deco_en}</span>`;
            }
            if (text.body) screensHtml += `<p class="body" style="margin-top: var(--sp-2); opacity:0.8;">${text.body}</p>`;
            screensHtml += `</div>`;

            screensHtml += `<div class="mod-body" style="justify-content: center;">`;
            
            if (text.items) {
                // 【智能分支 1：4项数据 -> 错落网格】
                if (text.items.length === 4) {
                    screensHtml += `<div class="grid-2x2">`;
                    text.items.forEach((item, i) => {
                        screensHtml += `<div class="grid-2x2-item">
                            <div class="dp2-mock dp2-mock--square" style="margin-bottom:20px;"><span>[Asset: Fragment ${i+1}]</span></div>
                            <strong style="font-size:14.5px; text-align:center; color:var(--color-text);">${item.label || item.title || item.name}</strong>
                        </div>`;
                    });
                    screensHtml += `</div>`;
                } 
                // 【智能分支 2：3项无贴士数据 -> Z字形交错瀑布流】(例如核心机制)
                else if (text.items.length === 3 && !text.tip && !text.texture) {
                    screensHtml += `<div class="stack gap-2">`;
                    text.items.forEach((item, i) => {
                        // 偶数行图在右，奇数行图在左，形成 Z 字流向
                        const isReversed = i % 2 !== 0;
                        const flexDir = isReversed ? 'row-reverse' : 'row';
                        const markStr = item.initial || item.num || String(i+1);
                        
                        screensHtml += `<div style="display:flex; flex-direction:${flexDir}; align-items:center; gap:32px; margin-bottom: 24px;">
                            <div class="dp2-mock dp2-mock--square" style="flex:1;"><span>[Asset: Node ${i+1}]</span></div>
                            <div style="flex:1.2; display:flex; flex-direction:column; align-items:${isReversed ? 'flex-end' : 'flex-start'}; text-align:${isReversed ? 'right' : 'left'};">
                                <span class="num" style="opacity:0.4; margin-bottom:12px;">${markStr}</span>
                                <strong style="font-size:18px; color:var(--color-text); margin-bottom:8px; font-family:var(--font-serif);">${item.name || item.title}</strong>
                                <span style="font-size:13px; color:var(--color-sub); line-height:1.6;">${item.desc || item.role || ''}</span>
                            </div>
                        </div>`;
                    });
                    screensHtml += `</div>`;
                }
                // 【智能分支 3：带补充贴士的长列表 -> 横向对冲卡片流】(例如使用场景)
                else {
                    screensHtml += `<div class="stack gap-2">`;
                    text.items.forEach((item, i) => {
                        const markStr = item.time || item.initial || item.num || item.mark || '•';
                        screensHtml += `<div class="callout-box" style="padding:24px;">
                            <div style="min-width: 60px; border-right: 1px solid rgba(197,162,107,0.2); padding-right:16px; margin-right:16px;">
                                <span style="font-family:var(--font-serif); font-size:24px; color:var(--color-gold); font-style:italic;">${markStr}</span>
                            </div>
                            <div style="flex:1;">
                                <strong style="font-size:15px; color:var(--color-text); display:block; margin-bottom:6px;">${item.name || item.title || item.caption || ''}</strong>
                                <span style="font-size:13px; color:var(--color-sub); line-height:1.5; display:block;">${item.desc || item.role || ''}</span>
                            </div>
                        </div>`;
                    });
                    screensHtml += `</div>`;
                    
                    // 嗅探挂载补充贴士
                    if (text.tip || text.texture) {
                        screensHtml += `<div style="margin-top:40px; padding-top:24px; border-top:1px dashed var(--color-line); text-align:center;">`;
                        if (text.texture) screensHtml += `<p style="font-size:13px; color:var(--color-gold); margin-bottom:8px;">${text.texture}</p>`;
                        if (text.tip) screensHtml += `<p style="font-size:12px; color:var(--color-sub);">💡 ${text.tip}</p>`;
                        screensHtml += `</div>`;
                    }
                }
            }

            // 嗅探挂载零添加横条
            if (text.zero_strip) {
                screensHtml += `<div class="dp2-data-strip">`;
                text.zero_strip.forEach((z, i) => {
                    screensHtml += `<span style="font-weight:600; letter-spacing:1px;">${z}</span>`;
                    if (i < text.zero_strip.length - 1) screensHtml += `<span style="color:var(--color-gold); opacity:0.3;">|</span>`;
                });
                screensHtml += `</div>`;
            }

            // 【智能手写体探针】list 屏内容块收尾，signature 错落装饰
            if (text.signature) {
                screensHtml += `<div style="text-align: center; margin-top: 32px; width: 100%;">`;
                screensHtml += `<span class="deco-script">${text.signature}</span>`;
                screensHtml += `</div>`;
            }
            screensHtml += `</div>`;
        }
        // ------------------------------------------------
        // 模板 C：Compare 空间错层卡片 (智能嗅探)
        // ------------------------------------------------
        else if (s.template === 'compare') {
            screensHtml += `<div class="mod-top-c">`;
            if (text.kicker) screensHtml += `<span class="kicker">${text.kicker}</span>`;
            if (text.headline) screensHtml += `<h2 class="${titleClass}">${text.headline}</h2>`;
            if (text.deco_en) {
                screensHtml += `<div class="deco-line"></div>`;
                screensHtml += `<span class="deco-en">${text.deco_en}</span>`;
            }
            screensHtml += `</div>`;

            screensHtml += `<div class="mod-body" style="justify-content: center;">`;
            if (text.rows) {
                screensHtml += `<div class="dp2-card-overlap">
                    <div class="dp2-card-overlap__card--them">
                        <div style="text-align:center; font-size:12px; font-weight:600; color:var(--color-sub); margin-bottom:24px; letter-spacing:1px;">其他产品</div>
                        <ul class="body" style="list-style:none; padding:0; font-size:13px; opacity:0.6; display:flex; flex-direction:column; gap:14px;">`;
                text.rows.forEach(r => screensHtml += `<li style="display:flex; gap:8px;"><span style="font-family:var(--font-serif);">×</span><span>${r.label}: ${r.them}</span></li>`);
                screensHtml += `</ul></div>
                    <div class="dp2-card-overlap__card--us">
                        <div style="text-align:center; font-size:12px; font-weight:bold; color:var(--color-gold); margin-bottom:24px; letter-spacing:1px;">HKH 稳态配方</div>
                        <ul class="body" style="list-style:none; padding:0; font-size:14px; font-weight:500; color:var(--color-text); display:flex; flex-direction:column; gap:14px;">`;
                text.rows.forEach(r => screensHtml += `<li style="display:flex; gap:8px;"><span style="color:var(--color-gold); font-weight:bold; font-size:16px; margin-top:-2px;">✓</span><span>${r.label}: ${r.us}</span></li>`);
                screensHtml += `</ul></div></div>`;
            }
            
            // 嗅探挂载徽章
            if (text.badges) {
                screensHtml += `<div style="margin-top:64px; display:flex; flex-wrap:wrap; gap:10px; justify-content:center;">`;
                text.badges.forEach(b => screensHtml += `<span class="tag-item" style="border-color:rgba(197,162,107,0.3); background:rgba(255,255,255,0.4);">${b}</span>`);
                screensHtml += `</div>`;
            }
            screensHtml += `</div>`;
        }
        // ------------------------------------------------
        // 模板 D：Closing 情绪展览（拱门遮罩图 + 手写体）
        // ------------------------------------------------
        else if (s.template === 'closing') {
            screensHtml += `<div class="mod-top-c">`;
            if (text.kicker) screensHtml += `<span class="kicker">${text.kicker}</span>`;
            if (text.headline) screensHtml += `<h2 class="${titleClass}">${text.headline}</h2>`;
            if (text.deco_en) {
                screensHtml += `<div class="deco-line"></div>`;
                screensHtml += `<span class="deco-en">${text.deco_en}</span>`;
            }
            screensHtml += `</div>`;

            screensHtml += `<div class="mod-body" style="align-items: center; justify-content: center; gap: 48px;">`;
            
            if (text.quote) {
                screensHtml += `<div class="deco-script" style="width:90%; text-align:center;">“ ${text.quote} ”</div>`;
            }
            
            // 嗅探香调结构：如果有香调，缩小主图，在旁边错落摆放香调标签
            if (text.notes) {
                screensHtml += `<div style="display:flex; align-items:center; gap:32px; width:100%;">
                    <div class="dp2-mock dp2-mock--arch" style="flex:1;"><span>[Asset: 情绪图]</span></div>
                    <div style="flex:1; display:flex; flex-direction:column; gap:24px;">`;
                text.notes.forEach(n => {
                    screensHtml += `<div>
                        <span style="font-family:var(--font-serif); font-size:12px; color:var(--color-gold); text-transform:uppercase; letter-spacing:2px; display:block; margin-bottom:4px;">${n.label}</span>
                        <strong style="font-size:15px; color:var(--color-text);">${n.text}</strong>
                    </div>`;
                });
                screensHtml += `</div></div>`;
            } else {
                // 默认居中大拱门
                screensHtml += `<div class="dp2-mock dp2-mock--arch" style="width: 75%;"><span>[Asset: Screen ${id} - 拱门形情绪美学海报]</span></div>`;
            }

            if (text.qa) {
                screensHtml += `<div class="stack gap-2" style="width: 100%;">`;
                text.qa.forEach(q => {
                    screensHtml += `<div style="border-bottom:1px solid rgba(197,162,107,0.1); padding-bottom:16px;">
                        <strong style="color:var(--color-text); font-size:15px; display:block; margin-bottom:8px; font-family:var(--font-serif);">Q: ${q.q}</strong>
                        <span style="color:var(--color-sub); font-size:13.5px; line-height:1.6; display:block;">A: ${q.a}</span>
                    </div>`;
                });
                screensHtml += `</div>`;
            }

            // 【智能手写体探针】closing 收尾
            if (text.closing) {
                screensHtml += `<div class="deco-script" style="opacity:0.85; transform:none; text-align:center;">${text.closing}</div>`;
            }
            screensHtml += `</div>`;
        }
        // ------------------------------------------------
        // 模板 E：Editorial (编辑视角/深度阅读) - 提取自 Monocle & NYT
        // ------------------------------------------------
        else if (s.template === 'editorial') {
            // NYT / Monocle 招牌：左对齐，严谨的三段阶梯式标题
            screensHtml += `<div class="mod-top-c editorial-overlay" style="align-items: flex-start; text-align: left;">`;
            if (text.kicker) screensHtml += `<span class="muji-label" style="color:var(--color-gold); margin-bottom:12px;">${text.kicker}</span>`;
            if (text.headline) screensHtml += `<h2 class="${titleClass}">${text.headline}</h2>`;
            // 倾斜的 Standfirst (副标题)
            if (text.subheadline) screensHtml += `<p class="display-lg" style="font-size:22px; font-style:italic; margin-top:20px; color:var(--color-sub); line-height:1.4;">${text.subheadline}</p>`;
            screensHtml += `</div>`;

            screensHtml += `<div class="mod-body editorial-overlay">`;
            // 插入 Monocle 式上下拉线的巨大引语
            if (text.quote) screensHtml += `<div class="monocle-pullquote">${text.quote}</div>`;

            // 插入杂志双栏排版正文
            if (text.body) {
                screensHtml += `<div class="layout-editorial-cols">
                    <p class="body" style="text-align:justify;">${text.body}</p>
                </div>`;
            }

            // Tufte 式数据边注
            if (text.notes) {
                screensHtml += `<div style="display:flex; flex-direction:column; gap:8px; margin-top:32px;">`;
                text.notes.forEach(n => {
                    screensHtml += `<div class="tufte-sidenote"><strong>${n.label}</strong>: ${n.text}</div>`;
                });
                screensHtml += `</div>`;
            }

            // 宽幅相片新闻感配图
            screensHtml += `<div class="dp2-mock dp2-mock--wide" style="margin-top: 48px; border-radius:0;"><span>[Asset: Editorial Photojournalism]</span></div>`;
            screensHtml += `</div>`;
        }
        // ------------------------------------------------
        // 模板 F：Focus (极致留白/实体凝视) - 提取自 MUJI & Stripe Press
        // ------------------------------------------------
        else if (s.template === 'focus') {
            // MUJI 式排版：取消明显的区块分割，居中，大量留白
            screensHtml += `<div class="mod-body editorial-overlay" style="align-items: center; justify-content: center; padding: 120px 0;">`;

            if (text.kicker) screensHtml += `<div class="muji-label" style="margin-bottom: 64px;">[ ${text.kicker} ]</div>`;

            // Stripe Press 式的实体物品阴影 (让产品看起来像一本精装书)
            screensHtml += `<div class="dp2-mock stripe-shadow" style="width: 55%; aspect-ratio: 3/4; background: #FFFFFF; border:none;"><span>[Asset: Product as Object]</span></div>`;

            if (text.headline) screensHtml += `<h2 class="${titleClass}" style="margin-top: 64px; text-align:center;">${text.headline}</h2>`;
            if (text.body) screensHtml += `<p class="body" style="margin-top: 24px; text-align:center; max-width: 80%;">${text.body}</p>`;

            screensHtml += `</div>`;
        }
        
        screensHtml += `</div>\n`;
    });

    htmlContent = htmlContent.replace(/(<title>).*?(<\/title>)/, `$1${spec.brand?.name || 'Brand Showcase'} - Showcase$2`);
    htmlContent = htmlContent.replace('<!-- SCREENS_INJECTION -->', screensHtml);
    fs.writeFileSync(HTML_PATH, htmlContent);
    console.log(`✅ 内容感知渲染完毕！(根据字数与数据量实现了: Z字排版/错落网格/动态字号/结构嗅探)`);
}

// ==========================================
// Phase 2: Prompt 引擎 (资产硬核隔离)
// ==========================================
function generatePrompts() {
    console.log(`[3/3] 正在生成受控生图 Prompt (流向级白名单)...`);
    
    const baseBanned = spec.banned || [];
    const themeBanned = (spec.theme_bundle && spec.theme_bundle.banned) ? spec.theme_bundle.banned : [];
    const GLOBAL_BANNED = [...new Set([...baseBanned, ...themeBanned])].join(', ');

    const st = spec.style;
    const paletteStr = st.palette ? `palette: ${Object.values(st.palette).join(' / ')}, ` : '';
    const typoStr = st.typography ? `typography: ${st.typography.header} for headers, ` : '';
    const ratioStr = st.ratio ? `ratio: ${st.ratio} vertical, ` : '';
    const stylePrefix = `Style: ${st.photography}, ${st.lighting}, ${st.lens}, mood: ${st.mood}, ${paletteStr}${typoStr}${ratioStr}modifiers: ${(st.modifiers||[]).join(', ')}.\n`;
    
    // 硬核护栏：防止大模型在环境描述中加人，或乱加漂浮粒子
    const ENGINE_CONSTRAINTS = `ASSET ISOLATION: When describing environments or backgrounds, strictly exclude any characters. When describing characters, strictly exclude complex backgrounds. CRITICAL ENVIRONMENTAL CONSTRAINT: No functional props or floating particles unless explicitly specified.`;

    const screens = Object.keys(spec.screens).sort();
    screens.forEach(id => {
        const s = spec.screens[id];
        
        if (!s.visual_description) {
            throw new Error(`Screen ${id} 缺少 visual_description！绝对禁止将 text_exact 喂给生图模型！`);
        }

        if (s.text_exact) {
            const exactValues = Object.values(s.text_exact).filter(v => typeof v === 'string' && v.length > 2);
            exactValues.forEach(val => {
                if (s.visual_description.includes(val)) {
                    throw new Error(`🚫 Prompt 污染警报: Screen ${id} 混入了营销修辞 ["${val}"]！`);
                }
            });
        }

        let promptContent = stylePrefix;
        promptContent += `Screen ${id} · ${s.template} · claim seed: ${(s.claim_seed_back||[]).join(', ')}\n`;
        promptContent += `${s.visual_description}\n`;
        promptContent += `${ENGINE_CONSTRAINTS}\n`;
        
        if (id === '01' || id === '1') {
            promptContent += `Primary product reference: ${spec.primary_image}\n`;
        }
        promptContent += `Banned: ${GLOBAL_BANNED}.\n`;

        fs.writeFileSync(path.join(OUTPUT_DIR, `prompt_${id}.txt`), promptContent);
    });
    console.log(`✅ 8 段受控的 Prompt 文本落盘完成！`);
}

(async () => {
    try {
        generateHTML();
        generatePrompts();
        console.log(`\n🎉 Render 引擎执行完毕！`);
        console.log(`👉 如需导出截图/PSD: node psd/html-to-psd.cjs "${projectName}" "${PROJECT_DIR}"`);
    } catch (err) {
        console.error(`\n❌ Render 引擎崩溃 (Fail Fast): ${err.message}`);
        process.exit(1);
    }
})();