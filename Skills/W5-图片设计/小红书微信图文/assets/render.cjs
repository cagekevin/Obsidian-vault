#!/usr/bin/env node
/*
 * Social Card Renderer (Fully Smart Cropped - No Fullscreen Base Layer)
 */
const path = require('path');
const fs = require('fs');

const taskDir = path.resolve(process.argv[2] || '.');
(function findNM(dir) {
  var nm = path.join(dir, 'node_modules');
  if (fs.existsSync(nm)) module.paths.unshift(nm);
  var parent = path.dirname(dir);
  if (parent !== dir) findNM(parent);
})(taskDir);
const { chromium } = require('playwright');

const selectors = process.argv.slice(3);
const idMap = {
  xhs:    '.poster.xhs',
  square: '.poster.square',
  wide:   '.poster.wide',
};
const SCALE_FACTOR = 2; 

// 自动化图层拆分规则：逐层覆盖常见 Editorial/Swiss 容器结构
const AUTO_LAYER_SELECTOR = [
  // 顶层容器（content 直接子元素，排除需要递归拆分的容器）
  '.content > *:not(figure):not(.pipeline-v):not(.marginalia):not(.mg-col)',
  // 图片容器
  '.content figure.frame-img',
  // pipeline 步骤子元素
  '.pipeline-v .step-nb',
  '.pipeline-v .step-title',
  '.pipeline-v .step-desc',
  // marginalia：不拆容器层，直接拆到内部独立元素
  '.marginalia .h-xl',
  '.marginalia .lead',
  '.marginalia .callout',
  '.marginalia figure.frame-img',
  '.marginalia .mg-col > p',
  '.marginalia .mg-col > div',
  // callout / lead / body 等独立文本块
  '.callout',
  '.lead',
  '.body',
  '.pullquote',
  '.h-sub',
  // 底部标签条 + 角落修饰
  '.issue-strip',
  '[class^="corner-"]'
].join(', ');

(async () => {
  const htmlPath = path.join(taskDir, 'index.html');
  if (!fs.existsSync(htmlPath)) {
    console.error('ERROR: index.html not found in ' + taskDir);
    process.exit(1);
  }

  const browser = await chromium.launch();
  const page = await browser.newPage({ 
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: SCALE_FACTOR 
  });
  
  await page.goto('file://' + htmlPath.replace(/\\/g, '/'), { waitUntil: 'networkidle' });
  await page.waitForTimeout(1200);

  let query = selectors.length === 0 ? '.poster.xhs, .poster.square, .poster.wide' : selectors.map(s => idMap[s] || '#' + s).join(', ');
  const els = await page.$$(query);
  if (els.length === 0) {
    console.error('ERROR: no elements matched: ' + query);
    await browser.close();
    process.exit(1);
  }

  const outDir = path.join(taskDir, 'output');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  
  const alphaDir = path.join(outDir, 'alpha');
  if (!fs.existsSync(alphaDir)) fs.mkdirSync(alphaDir, { recursive: true });
  
  const slug = path.basename(taskDir);

  let idx = 0;
  for (const el of els) {
    idx++;
    const box = await el.boundingBox();
    const fname = slug + '_' + String(idx).padStart(2, '0') + '.png';

    // 1. 正常导出
    await el.screenshot({ path: path.join(outDir, fname) });

    // 2. 准备 Alpha 环境
    await page.evaluate((node) => {
      if (!document.body.dataset.origBg) {
        document.body.dataset.origBg = document.body.style.background || '';
        document.body.style.setProperty('background', 'transparent', 'important');
      }
      node.dataset.origBg = node.style.background || '';
      node.style.setProperty('background', 'transparent', 'important');

      const hides = node.querySelectorAll('.grain, .paper-wash, .mag-bg, canvas, .dot-mat, .ring-mat, .cross-mat');
      hides.forEach(n => {
        n.dataset.origDisplay = n.style.display || '';
        n.style.setProperty('display', 'none', 'important');
      });

      const trans = node.querySelectorAll('.frame-img, .frame-shot');
      trans.forEach(n => {
        n.dataset.origBg = n.style.background || '';
        n.style.setProperty('background', 'transparent', 'important');
      });
    }, el);

    // 3. 整体 Alpha 导出
    await el.screenshot({ 
      path: path.join(alphaDir, fname), 
      omitBackground: true 
    });

    // 3.5 恢复 frame-img 背景（基底层需要显示灰色占位）
    await page.evaluate((node) => {
      const trans = node.querySelectorAll('.frame-img, .frame-shot');
      trans.forEach(n => { n.style.background = n.dataset.origBg || ''; });
    }, el);

    // 4. 自动化精细 PSD 图层碎片导出
    const layerItems = await el.$$(AUTO_LAYER_SELECTOR);
    if (layerItems.length > 0) {
      const psdLayersDir = path.join(outDir, 'psd_layers', slug + '_' + String(idx).padStart(2, '0'));
      if (!fs.existsSync(psdLayersDir)) fs.mkdirSync(psdLayersDir, { recursive: true });

      const metaData = {
        width: Math.round(box.width * SCALE_FACTOR),
        height: Math.round(box.height * SCALE_FACTOR),
        layers: []
      };

      // --- 基底图层 (layer_00.png)：保留装饰条、图片灰色背景等 ---
      await page.evaluate(({ poster, selector }) => {
        poster.querySelectorAll(selector).forEach(n => n.style.opacity = '0');
      }, { poster: el, selector: AUTO_LAYER_SELECTOR });
      await el.screenshot({
        path: path.join(psdLayersDir, 'layer_00.png'),
        omitBackground: true
      });
      metaData.layers.push({ file: 'layer_00.png', left: 0, top: 0 });

      let layerIdx = 0;
      for (const item of layerItems) {
        layerIdx++;
        const layerFname = `layer_${String(layerIdx).padStart(2, '0')}.png`;

        const rects = await page.evaluate(({ poster, target }) => {
          const pRect = poster.getBoundingClientRect();
          const tRect = target.getBoundingClientRect();
          return {
            px: pRect.left,
            py: pRect.top,
            tx: tRect.left,
            ty: tRect.top
          };
        }, { poster: el, target: item });

        const left = Math.round(rects.tx * SCALE_FACTOR) - Math.round(rects.px * SCALE_FACTOR);
        const top = Math.round(rects.ty * SCALE_FACTOR) - Math.round(rects.py * SCALE_FACTOR);

        await page.evaluate(({ poster, target }) => {
          const all = poster.querySelectorAll('*');
          all.forEach(n => {
            if (n === target || target.contains(n) || n.contains(target)) {
              n.style.opacity = '1';
            } else {
              n.style.opacity = '0'; 
            }
          });
        }, { poster: el, target: item });

        await item.screenshot({
          path: path.join(psdLayersDir, layerFname),
          omitBackground: true
        });
        
        metaData.layers.push({ file: layerFname, left, top });
      }

      fs.writeFileSync(path.join(psdLayersDir, 'meta.json'), JSON.stringify(metaData, null, 2));

      // 恢复透明度
      await page.evaluate((poster) => {
        poster.querySelectorAll('*').forEach(n => n.style.opacity = '');
      }, el);
    }

    // 5. 恢复节点状态
    await page.evaluate((node) => {
      node.style.background = node.dataset.origBg;

      const hides = node.querySelectorAll('.grain, .paper-wash, .mag-bg, canvas, .dot-mat, .ring-mat, .cross-mat');
      hides.forEach(n => { n.style.display = n.dataset.origDisplay; });

      const trans = node.querySelectorAll('.frame-img, .frame-shot');
      trans.forEach(n => { n.style.background = n.dataset.origBg; });

      if (document.body.dataset.origBg !== undefined) {
        document.body.style.background = document.body.dataset.origBg;
        delete document.body.dataset.origBg;
      }
    }, el);

    console.log(`${fname}  ${Math.round(box.width)}x${Math.round(box.height)} (Normal & Alpha${layerItems.length > 0 ? ' & Smart Layers' : ''})`);
  }

  await browser.close();
  console.log('Done — ' + els.length + ' image(s) in ' + outDir);
})();
