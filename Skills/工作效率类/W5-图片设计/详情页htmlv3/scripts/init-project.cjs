// scripts/init-project.cjs
// 用法:
//   node scripts/init-project.cjs <ProjectName> [ProjectRootDir]
// 职责: 建目录、复制 HTML 模板 / 默认主题 / JSON 模板到项目目录
// 之后 AI 修改项目根目录下的 brand-spec.json 填入项目数据
const fs = require('fs');
const path = require('path');

const projectName = process.argv[2];
const projectRootArg = process.argv[3];
if (!projectName) {
    console.error('❌ Fail Fast: 请提供项目名称。用法: node scripts/init-project.cjs <ProjectName> [ProjectRootDir]');
    process.exit(1);
}

const SKILL_ROOT = path.join(__dirname, '..');
const PROJECT_DIR = projectRootArg
    ? path.resolve(projectRootArg)
    : path.join(SKILL_ROOT, 'Temp', projectName);

const JSON_SOURCE = path.join(SKILL_ROOT, '模板', '模板.json');
const JSON_DEST = path.join(PROJECT_DIR, 'brand-spec.json');
const OUTPUT_DIR = path.join(PROJECT_DIR, 'output');
const TEMPLATE_PATH = path.join(SKILL_ROOT, 'templates', 'template.html');
const DEFAULT_THEME = path.join(SKILL_ROOT, 'tokens', 'theme-pilgrim-dawn.css');

if (!fs.existsSync(TEMPLATE_PATH)) {
    console.error(`❌ Fail Fast: 找不到模板 ${TEMPLATE_PATH}`);
    process.exit(1);
}
if (!fs.existsSync(DEFAULT_THEME)) {
    console.error(`❌ Fail Fast: 找不到默认主题 ${DEFAULT_THEME}`);
    process.exit(1);
}
if (!fs.existsSync(JSON_SOURCE)) {
    console.error(`❌ Fail Fast: 找不到 JSON 模板 ${JSON_SOURCE}`);
    process.exit(1);
}

try {
    console.log(`[1/4] 正在创建项目目录: ${PROJECT_DIR}...`);
    if (!fs.existsSync(PROJECT_DIR)) fs.mkdirSync(PROJECT_DIR, { recursive: true });
    if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

    const TOKENS_DIR = path.join(PROJECT_DIR, 'tokens');
    if (!fs.existsSync(TOKENS_DIR)) fs.mkdirSync(TOKENS_DIR, { recursive: true });

    console.log(`[2/4] 正在复制模板文件 (HTML + CSS + JSON)...`);
    fs.copyFileSync(TEMPLATE_PATH, path.join(PROJECT_DIR, 'index.html'));
    fs.copyFileSync(DEFAULT_THEME, path.join(TOKENS_DIR, 'theme.css'));
    fs.copyFileSync(JSON_SOURCE, JSON_DEST);
    console.log(`ℹ️ 已复制 brand-spec.json 模板到项目目录，请 AI 修改其中的字段`);

    // 如果 AI 已经改好了 brand-spec.json，提取文案生成 copy.md
    if (fs.existsSync(JSON_DEST)) {
        console.log(`[3/4] 解析 brand-spec.json 提取 text_exact 文案...`);
        const spec = JSON.parse(fs.readFileSync(JSON_DEST, 'utf-8'));

        if (spec.screens) {
            let copyMdContent = `# ${spec.brand?.name || 'Brand'} - 详情页文案复核稿\n\n`;
            copyMdContent += `> 项目：${spec.brand?.product_full || '未命名产品'}\n`;
            copyMdContent += `> 类别：展示页 (Showcase Page)\n\n---\n\n`;

            const screens = Object.keys(spec.screens).sort();
            screens.forEach((screenId) => {
                const textData = spec.screens[screenId].text_exact;
                if (!textData) {
                    console.warn(`⚠️ 警告: Screen ${screenId} 缺少 text_exact 字段`);
                    return;
                }
                copyMdContent += `## Screen ${screenId} (${spec.screens[screenId].template})\n`;
                if (textData.kicker) copyMdContent += `**Kicker**: ${textData.kicker}\n`;
                if (textData.headline) copyMdContent += `**Headline**: ${textData.headline}\n`;
                if (textData.subheadline) copyMdContent += `**Sub**: ${textData.subheadline}\n`;
                if (textData.body) copyMdContent += `**Body**: ${textData.body}\n`;
                if (textData.items) {
                    copyMdContent += `**Items**: ${textData.items.map(i => i.title || i.name || i.label || i.caption).join(' | ')}\n`;
                }
                if (textData.rows) {
                    copyMdContent += `**Rows**: ${textData.rows.map(r => r.label).join(' | ')}\n`;
                }
                if (textData.cta) copyMdContent += `**CTA**: [ ${textData.cta} ]\n`;
                if (textData.closing) copyMdContent += `**Closing**: ${textData.closing}\n`;
                copyMdContent += `\n`;
            });

            const copyMdPath = path.join(PROJECT_DIR, 'copy.md');
            fs.writeFileSync(copyMdPath, copyMdContent, 'utf-8');
            console.log(`[4/4] 成功提取文案至: ${copyMdPath}`);
        }
    } else {
        console.log(`[3/4] brand-spec.json 尚未创建，跳过 copy.md 生成`);
    }

    console.log(`\n✅ Step 1 完成！项目 [${projectName}] 初始化成功。`);
    console.log(`👉 下一步 (如果已写好 brand-spec.json): node scripts/validate-seeds.cjs ${projectName} "${PROJECT_DIR}"`);
} catch (error) {
    console.error(`\n❌ Step 1 失败: ${error.message}`);
    process.exit(1);
}
