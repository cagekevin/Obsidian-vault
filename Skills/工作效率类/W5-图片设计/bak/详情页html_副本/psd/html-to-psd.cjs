#!/usr/bin/env node
/**
 * html-to-psd.cjs (三模式版)
 *
 * 用法 1 (合并长图):  node html-to-psd.cjs <task-dir>
 * 用法 2 (全部分屏):  node html-to-psd.cjs <task-dir> --split
 * 用法 3 (指定第N屏): node html-to-psd.cjs <task-dir> --split --index=3
 */
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
const isSplitMode = args.includes('--split');
const indexArg = args.find(arg => arg.startsWith('--index='));
const targetIndex = indexArg ? parseInt(indexArg.split('=')[1], 10) : null;
const taskDirArg = args.find(arg => !arg.startsWith('--'));
const taskDir = path.resolve(taskDirArg || '.');

var searchPaths = [path.join(taskDir, 'node_modules'), path.join(__dirname, 'node_modules')];
searchPaths.forEach(function(p) { if (fs.existsSync(p)) module.paths.unshift(p); });
const { chromium } = require('playwright');

function cssColorToPS(cssColor) {
  let r = 10, g = 10, b = 10, a = 100;
  if (cssColor.startsWith('#')) {
    const h = cssColor.slice(1);
    r = parseInt(h.slice(0,2), 16) || 0; g = parseInt(h.slice(2,4), 16) || 0; b = parseInt(h.slice(4,6), 16) || 0;
  } else if (cssColor.startsWith('rgba')) {
    const m = cssColor.match(/\d+(\.\d+)?/g);
    if (m && m.length >= 4) { r = +m[0]; g = +m[1]; b = +m[2]; a = Math.round(+m[3] * 100); }
  } else { const m = cssColor.match(/\d+/g); if (m) { r = +m[0]; g = +m[1]; b = +m[2]; } }
  return 'var c = new SolidColor(); c.rgb.red=' + r + '; c.rgb.green=' + g + '; c.rgb.blue=' + b + '; c; var _oa=' + a + '; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;';
}

function extractRGB(cssColor) {
  let r = 200, g = 200, b = 200, a = 255;
  if (!cssColor || cssColor === 'transparent') return [0, 0, 0, 0];
  if (cssColor.startsWith('#')) {
    const h = cssColor.slice(1);
    r = parseInt(h.slice(0,2), 16) || 0; g = parseInt(h.slice(2,4), 16) || 0; b = parseInt(h.slice(4,6), 16) || 0;
  } else if (cssColor.startsWith('rgba')) {
    const m = cssColor.match(/\d+(\.\d+)?/g);
    if (m && m.length >= 4) { r = +m[0]; g = +m[1]; b = +m[2]; a = Math.round(+m[3] * 255); }
  } else { const m = cssColor.match(/\d+/g); if (m && m.length >= 3) { r = +m[0]; g = +m[1]; b = +m[2]; } }
  return [r, g, b, a];
}

(async () => {
  const htmlPath = path.join(taskDir, 'index.html');
  if (!fs.existsSync(htmlPath)) { console.error('ERROR: index.html not found'); process.exit(1); }

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 790, height: 1080, deviceScaleFactor: 2 } });
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);

  const elements = await page.evaluate((opts) => {
    const isSplit = opts.isSplit;
    const targetIdx = opts.targetIndex;
    const results = [];
    const containerSelector = isSplit ? '.mod, .mod-auto, .section-sand, .poster.xhs' : '.page, .poster.xhs';
    const containers = document.querySelectorAll(containerSelector);

    function skipTag(tag) { return ['canvas','script','style','link','meta','head'].includes(tag); }
    function skipCls(c) { return c.contains('grain') || c.contains('paper-wash') || c.contains('mag-bg') || c.contains('dot-mat') || c.contains('ring-mat'); }
    
    containers.forEach(function(container, index) {
      if (targetIdx !== null && index + 1 !== targetIdx) return;
      var pr = container.getBoundingClientRect();
      var pid = isSplit ? (container.id || ('M' + String(index + 1).padStart(2, '0'))) : 'FullPage';
      results.push({ pid: pid, t: 'meta_size', w: pr.width, h: pr.height });

      (function walkShape(el) {
        if (!el || el.nodeType !== 1) return;
        if (skipTag(el.tagName.toLowerCase()) || skipCls(el.classList)) return;
        var s = getComputedStyle(el);
        var r = el.getBoundingClientRect();
        if (r.width === 0) return;
        var x = r.left - pr.left, y = r.top - pr.top, w = r.width, h = r.height;

        if (el.tagName === 'HR') {
          results.push({pid:pid, t:'shape', sh:'rect', x:x, y:y, w:w, h:h, bg:s.backgroundColor || s.borderTopColor});
        } else if (el.classList.contains('card-fill') || el.classList.contains('card-ink') || el.classList.contains('card-accent')) {
          var bw = parseFloat(s.borderLeftWidth);
          if (bw > 0) results.push({pid:pid, t:'shape', sh:'rect', x:x, y:y, w:bw, h:h, bg:s.borderLeftColor});
          results.push({pid:pid, t:'shape', sh:'rect', x:x+bw, y:y, w:w-bw, h:h, bg:s.backgroundColor});
        } else if (el.classList.contains('marker-dot') || el.classList.contains('check')) {
          results.push({pid:pid, t:'shape', sh:'circle', x:x, y:y, w:w, h:h, bg:s.backgroundColor});
        } else if (['IMG', 'SVG'].includes(el.tagName)) {
          var isCircle = s.borderRadius.indexOf('50%') !== -1 || (parseFloat(s.borderRadius) || 0) >= w / 2;
          results.push({ pid:pid, t:'shape', sh: isCircle ? 'circle' : 'rect', x:x, y:y, w:w, h:h, bg:'#E2E8F0', placeholderName: '🖼️ Image Placeholder' });
        } else if (['DIV','SECTION','ARTICLE','HEADER','FOOTER'].includes(el.tagName)) {
          var bg = s.backgroundColor;
          if (bg && bg !== 'transparent' && bg !== 'rgba(0, 0, 0, 0)') {
            results.push({pid:pid, t:'shape', sh:'rect', x:x, y:y, w:w, h:h, bg:bg});
          }
        }
        for (var ci = 0; ci < el.children.length; ci++) walkShape(el.children[ci]);
      })(container);

      var seen = [];
      var walker = document.createTreeWalker(container, 4, {
        acceptNode: function(node) {
          if (!node.textContent.replace(/\s+/g, '').trim()) return NodeFilter.FILTER_REJECT;
          var p = node.parentElement;
          if (!p) return NodeFilter.FILTER_REJECT;
          if (skipTag(p.tagName.toLowerCase()) || skipCls(p.classList)) return NodeFilter.FILTER_REJECT;
          var st = getComputedStyle(p);
          if (st.display === 'none' || st.visibility === 'hidden') return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        }
      });
      while (walker.nextNode()) {
        var raw = walker.currentNode.textContent;
        var txt = raw.replace(/\s+/g, ' ').trim();
        if (!txt) continue;
        var p = walker.currentNode.parentElement;
        if (!p) continue;
        var ws = ''; if (/^\s/.test(raw)) ws += 'L'; if (/\s$/.test(raw)) ws += 'R';
        var range = document.createRange();
        range.selectNodeContents(walker.currentNode);
        var rect = range.getBoundingClientRect();
        range.detach();
        if (rect.width === 0 || rect.height === 0) continue;
        var px = Math.round(rect.left - pr.left);
        var py = Math.round(rect.top - pr.top);
        var dup = seen.some(function(s) { return Math.abs(s[0] - px) < 3 && Math.abs(s[1] - py) < 3 && s[2] === p; });
        if (dup) continue;
        seen.push([px, py, p]);
        var st = getComputedStyle(p);
        results.push({
          pid: pid, t: 'text', text: txt, x: px, y: py, w: Math.round(rect.width), h: Math.round(rect.height),
          ff: st.fontFamily.split(',')[0].replace(/["']/g, '').trim() || 'PingFang SC',
          fw: st.fontWeight, fs: st.fontStyle, sz: st.fontSize, lh: st.lineHeight,
          clr: st.color, align: st.textAlign || 'left', ls: st.letterSpacing, ws: ws
        });
      }
    });
    return results;
  }, { isSplit: isSplitMode, targetIndex: targetIndex });

  if (!fs.existsSync(path.join(taskDir, 'output'))) fs.mkdirSync(path.join(taskDir, 'output'), { recursive: true });
  var slug = path.basename(taskDir);
  var containerSelector = isSplitMode ? '.mod, .mod-auto, .section-sand, .poster.xhs' : '.page, .poster.xhs';
  var posterEls = await page.$$(containerSelector);
  
  for (var pi = 0; pi < posterEls.length; pi++) {
    if (targetIndex !== null && pi + 1 !== targetIndex) continue;
    var pe = posterEls[pi];
    var pid = isSplitMode
      ? await pe.evaluate((el, i) => el.id || ('M' + String(i + 1).padStart(2, '0')), pi)
      : 'FullPage';
    var box = await pe.boundingBox();
    if (isSplitMode) {
      await pe.screenshot({ path: path.join(taskDir, 'output', slug + '-' + pid + '.png') });
      await pe.screenshot({ path: path.join(taskDir, 'output', slug + '-' + pid + '-alpha.png'), omitBackground: true });
    } else {
      await page.screenshot({ path: path.join(taskDir, 'output', slug + '.png'), fullPage: true });
    }
    console.log('   ' + pid + '  ' + Math.round(box.width) + 'x' + Math.round(box.height));
  }
  await browser.close();

  // 去重 + 融合
  var modSizes = {};
  var deduped = [];
  for (var i = 0; i < elements.length; i++) {
    var el = elements[i];
    if (el.t === 'meta_size') { modSizes[el.pid] = { w: el.w, h: el.h }; continue; }
    if (el.t === 'shape') {
      var overlap = deduped.some(function(e) { return e.pid === el.pid && e.t === 'shape' && Math.abs(e.x - el.x) < 10 && Math.abs(e.y - el.y) < 10 && Math.abs(e.w - el.w) < 10 && Math.abs(e.h - el.h) < 10; });
      if (!overlap) deduped.push(el);
    } else { deduped.push(el); }
  }
  var shapes = deduped.filter(function(e) { return e.t === 'shape'; });
  var texts = deduped.filter(function(e) { return e.t === 'text'; });
  texts.sort(function(a, b) {
    if (a.pid !== b.pid) return a.pid < b.pid ? -1 : 1;
    if (Math.abs(a.y - b.y) > 8) return a.y - b.y;
    return a.x - b.x;
  });
  var fusedTexts = [];
  var current = null;
  for (var i = 0; i < texts.length; i++) {
    var t = texts[i];
    if (!current) { current = { pid: t.pid, t: 'text', text: t.text, x: t.x, y: t.y, w: t.w, h: t.h, ff: t.ff, fw: t.fw, fs: t.fs, sz: t.sz, lh: t.lh, clr: t.clr, align: t.align, ls: t.ls, _ws: t.ws }; continue; }
    var samePid = current.pid === t.pid;
    var sameLine = Math.abs(current.y - t.y) <= 8;
    var gapX = t.x - (current.x + current.w);
    if (samePid && sameLine && gapX >= -5 && gapX <= 35) {
      var sp = ''; if (current._ws && current._ws.indexOf('R') >= 0) sp = ' '; else if (t._ws && t._ws.indexOf('L') >= 0) sp = ' '; else if (gapX > 6) sp = ' ';
      current.text += sp + t.text; current.w = (t.x + t.w) - current.x;
    } else { fusedTexts.push(current); current = { pid: t.pid, t: 'text', text: t.text, x: t.x, y: t.y, w: t.w, h: t.h, ff: t.ff, fw: t.fw, fs: t.fs, sz: t.sz, lh: t.lh, clr: t.clr, align: t.align, ls: t.ls, _ws: t.ws }; }
  }
  if (current) fusedTexts.push(current);
  var finalElements = shapes.concat(fusedTexts);

  var groups = {};
  for (var i = 0; i < finalElements.length; i++) {
    var el = finalElements[i];
    if (!groups[el.pid]) groups[el.pid] = [];
    groups[el.pid].push(el);
  }

  // 生成 JSX
  var outDir = path.join(taskDir, 'output');
  var jsxPath = path.join(outDir, slug + (isSplitMode ? '-Split' : '') + '.jsx');
  var lines = [];

  lines.push('/** Detail Page PSD (' + (isSplitMode ? 'SPLIT' : 'MERGED') + ') */');
  lines.push('app.preferences.rulerUnits = Units.PIXELS;');
  lines.push('');
  lines.push('var _fontCache={};function resolvePSFont(tf,tg,ii){var key=tf+"|"+tg+"|"+ii;if(_fontCache[key])return _fontCache[key];var cf=tf.toLowerCase().replace(/[\\s\\-_]/g,"");var wn=parseInt(tg)||400;var kw=[];if(ii)kw.push("italic");if(wn<=200)kw.push("extralight");else if(wn<=300)kw.push("light");else if(wn>=700)kw.push("bold");else if(wn>=500)kw.push("medium");else kw.push("regular");var lf=app.fonts;var ffm=null;for(var i=0;i<lf.length;i++){var f=lf[i];var lcl=f.family.toLowerCase().replace(/[\\s\\-_]/g,"");var ls=f.style.toLowerCase();if(lcl===cf||f.family.toLowerCase()===tf.toLowerCase()){if(!ffm)ffm=f.postScriptName;var sm=true;for(var k=0;k<kw.length;k++){if(ls.indexOf(kw[k])===-1){sm=false;break;}}if(sm){_fontCache[key]=f.postScriptName;return f.postScriptName;}}}if(ffm){_fontCache[key]=ffm;return ffm;}var fallback=$.os.indexOf("Mac")>-1?"PingFangSC-Regular":"ArialMT";_fontCache[key]=fallback;return fallback;}');
  lines.push('function createColorLayer(n,r,g,b,o){if(o===undefined)o=100;var d=new ActionDescriptor(),ref=new ActionReference();ref.putClass(stringIDToTypeID("contentLayer"));d.putReference(charIDToTypeID("null"),ref);var d2=new ActionDescriptor(),d3=new ActionDescriptor();d3.putDouble(charIDToTypeID("Rd  "),r);d3.putDouble(charIDToTypeID("Grn "),g);d3.putDouble(charIDToTypeID("Bl  "),b);var d4=new ActionDescriptor();d4.putObject(charIDToTypeID("Clr "),charIDToTypeID("RGBC"),d3);d2.putObject(charIDToTypeID("Type"),stringIDToTypeID("solidColorLayer"),d4);d.putObject(charIDToTypeID("Usng"),stringIDToTypeID("contentLayer"),d2);executeAction(charIDToTypeID("Mk  "),d,DialogModes.NO);app.activeDocument.activeLayer.name=n;if(o<100)app.activeDocument.activeLayer.opacity=o;}');
  lines.push('function selectEllipse(x,y,w,h){var d=new ActionDescriptor(),ref=new ActionReference();ref.putProperty(charIDToTypeID("Chnl"),charIDToTypeID("fsel"));d.putReference(charIDToTypeID("null"),ref);var d2=new ActionDescriptor();d2.putUnitDouble(charIDToTypeID("Top "),charIDToTypeID("#Pxl"),y);d2.putUnitDouble(charIDToTypeID("Left"),charIDToTypeID("#Pxl"),x);d2.putUnitDouble(charIDToTypeID("Btom"),charIDToTypeID("#Pxl"),y+h);d2.putUnitDouble(charIDToTypeID("Rght"),charIDToTypeID("#Pxl"),x+w);d.putObject(charIDToTypeID("T   "),charIDToTypeID("Elps"),d2);d.putBoolean(charIDToTypeID("AntA"),true);executeAction(charIDToTypeID("setd"),d,DialogModes.NO);}');
  lines.push('');

  for (var pid in groups) {
    var els = groups[pid];
    var modW = modSizes[pid] ? Math.round(modSizes[pid].w) : 790;
    var modH = modSizes[pid] ? Math.round(modSizes[pid].h) : 1000;

    lines.push('// ===== ' + pid + ' =====');
    lines.push('var doc = app.documents.add(' + modW + ', ' + modH + ', 72, "' + slug + '-' + pid + '", NewDocumentMode.RGB);');
    lines.push('doc.suspendHistory("' + slug + '-' + pid + '", function(){');
    lines.push('var groupBg = doc.layerSets.add(); groupBg.name = "背景与形状";');
    lines.push('var groupText = doc.layerSets.add(); groupText.name = "排版文字";');
    lines.push('');

    els.sort(function(a, b) {
      if (a.t !== b.t) return a.t === 'shape' ? -1 : 1;
      if (Math.abs(a.y - b.y) > 10) return a.y - b.y;
      return a.x - b.x;
    });

    for (var j = 0; j < els.length; j++) {
      var el = els[j];
      if (el.t === 'shape') {
        var rgb = extractRGB(el.bg);
        var alphaPct = Math.round((rgb[3] || 255) / 255 * 100);
        if (alphaPct === 0) continue;
        var rx = Math.round(el.x), ry = Math.round(el.y), rw = Math.round(el.w), rh = Math.round(el.h);
        var shName = el.placeholderName || (el.sh === 'circle' ? 'Circle' : 'Rect');
        lines.push('app.activeDocument.activeLayer = groupBg;');
        if (el.sh === 'circle') { lines.push('selectEllipse(' + rx + ', ' + ry + ', ' + rw + ', ' + rh + ');'); }
        else { lines.push('doc.selection.select([[' + rx + ',' + ry + '],[' + (rx+rw) + ',' + ry + '],[' + (rx+rw) + ',' + (ry+rh) + '],[' + rx + ',' + (ry+rh) + ']]);'); }
        lines.push('createColorLayer("' + shName + '", ' + rgb[0] + ', ' + rgb[1] + ', ' + rgb[2] + ', ' + alphaPct + ');');
        lines.push('doc.selection.deselect();');
        continue;
      }
      if (el.t === 'text') {
        var sz = parseFloat(el.sz) || 24;
        var lh = el.lh !== 'normal' ? parseFloat(el.lh) : sz * 1.4;
        var ls = el.ls !== 'normal' ? (parseFloat(el.ls) || 0) * 100 : 0;
        var safe = el.text.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/\n/g, '\\n');
        var nm = safe.replace(/['"\\]/g, '').replace(/\s+/g, ' ').slice(0, 28);
        lines.push(cssColorToPS(el.clr) + ';');
        lines.push('var L = groupText.artLayers.add(); L.name = "' + nm + '"; L.kind = LayerKind.TEXT;');
        // 段落文本框宽度：serif 字体 + 大字号需要更多右留白，防止最后一个字被裁切
        var pad = (el.ff && el.ff.toLowerCase().indexOf('serif') !== -1) ? Math.max(30, sz * 0.6) : Math.max(18, sz * 0.4);
        lines.push('var ti = L.textItem; ti.kind = TextType.PARAGRAPHTEXT; ti.width = ' + Math.round(el.w + pad) + '; ti.height = ' + Math.round(el.h + sz) + ';');
        lines.push("ti.contents = '" + safe + "';");
        lines.push('ti.font = resolvePSFont("' + el.ff + '", "' + el.fw + '", ' + (el.fs === 'italic' ? 'true' : 'false') + ');');
        lines.push('ti.size = ' + sz + '; ti.color = c; ti.leading = ' + Math.round(lh) + '; ti.tracking = ' + Math.round(ls) + ';');
        var al = 'Justification.LEFT';
        if (el.align === 'center') al = 'Justification.CENTER';
        else if (el.align === 'right') al = 'Justification.RIGHT';
        lines.push('ti.justification = ' + al + '; ti.position = Array(' + Math.round(el.x) + ', ' + Math.round(el.y) + ');');
      }
    }

    lines.push('}); // end suspendHistory');
    lines.push('var sf = new File(Folder.desktop + "/' + slug + '-' + pid + '.psd"); doc.saveAs(sf);');
    if (isSplitMode) lines.push('doc.close(SaveOptions.DONOTSAVECHANGES);');
    lines.push('');
  }

  lines.push('alert("✅ ' + (isSplitMode ? '分屏' : '合并长图') + '生成完成！PSD 已存入桌面。");');
  fs.writeFileSync(jsxPath, '\uFEFF' + lines.join('\r\n'), 'utf-8');
  var tc = 0, sc = 0;
  finalElements.forEach(function(e) { if (e.t === 'text') tc++; else sc++; });
  console.log('OK: ' + jsxPath);
  console.log('Mode: ' + (isSplitMode ? 'Split' : 'Merged') + ' | Elements: ' + deduped.length + ' (' + tc + ' text, ' + sc + ' shapes)');
})();
