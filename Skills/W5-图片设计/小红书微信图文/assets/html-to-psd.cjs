#!/usr/bin/env node
/**
 * html-to-psd.cjs
 *
 * 读取社交卡片 index.html → 生成 Photoshop ExtendScript (.jsx)
 * 在 PS 中运行 .jsx 即可得到可编辑文字图层 + 装饰形状层的分层 PSD。
 *
 * 用法:
 *   node html-to-psd.cjs <task-dir>
 *
 * 输出:
 *   <task-dir>/output/layered.jsx
 */
const path = require('path');
const fs = require('fs');

const taskDir = path.resolve(process.argv[2] || '.');
// 从 taskDir 向上搜索 node_modules（允许父目录共享安装）
(function findNM(dir) {
  var nm = path.join(dir, 'node_modules');
  if (fs.existsSync(nm)) module.paths.unshift(nm);
  var parent = path.dirname(dir);
  if (parent !== dir) findNM(parent);
})(taskDir);
const { chromium } = require('playwright');

// 字体映射已移至 JSX 运行时动态匹配 (resolvePSFont)
function cssColorToPS(cssColor) {
  let r = 10, g = 10, b = 10, a = 100;
  if (cssColor.startsWith('#')) {
    const h = cssColor.slice(1);
    r = parseInt(h.slice(0,2), 16) || 0;
    g = parseInt(h.slice(2,4), 16) || 0;
    b = parseInt(h.slice(4,6), 16) || 0;
  } else if (cssColor.startsWith('rgba')) {
    const m = cssColor.match(/\d+(\.\d+)?/g);
    if (m && m.length >= 4) { r = +m[0]; g = +m[1]; b = +m[2]; a = Math.round(+m[3] * 100); }
  } else {
    const m = cssColor.match(/\d+/g);
    if (m) { r = +m[0]; g = +m[1]; b = +m[2]; }
  }
  return 'var c = new SolidColor(); c.rgb.red=' + r + '; c.rgb.green=' + g + '; c.rgb.blue=' + b + '; c; var _oa=' + a + '; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;';
}

function extractRGB(cssColor) {
  let r = 200, g = 200, b = 200, a = 255;
  if (!cssColor || cssColor === 'transparent') return [0, 0, 0, 0];
  if (cssColor.startsWith('#')) {
    const h = cssColor.slice(1);
    r = parseInt(h.slice(0,2), 16) || 0;
    g = parseInt(h.slice(2,4), 16) || 0;
    b = parseInt(h.slice(4,6), 16) || 0;
  } else if (cssColor.startsWith('rgba')) {
    const m = cssColor.match(/\d+(\.\d+)?/g);
    if (m && m.length >= 4) { r = +m[0]; g = +m[1]; b = +m[2]; a = Math.round(+m[3] * 255); }
  } else {
    const m = cssColor.match(/\d+/g);
    if (m && m.length >= 3) { r = +m[0]; g = +m[1]; b = +m[2]; }
  }
  return [r, g, b, a];
}

(async () => {
  const htmlPath = path.join(taskDir, 'index.html');
  if (!fs.existsSync(htmlPath)) { console.error('ERROR: index.html not found'); process.exit(1); }

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);

  // 用函数替代字符串，避免转义问题
  const elements = await page.evaluate(() => {
    const results = [];
    const posters = document.querySelectorAll('.poster');

    function skipTag(tag) {
      return ['canvas','script','style','link','meta','head'].includes(tag);
    }
    function skipCls(c) {
      return c.contains('grain') || c.contains('paper-wash') || c.contains('mag-bg') ||
             c.contains('dot-mat') || c.contains('ring-mat') || c.contains('cross-mat') ||
             c.contains('hero-bleed') || c.contains('map-block');
    }
    posters.forEach(function(poster) {
      var pr = poster.getBoundingClientRect();
      var pid = poster.id || 'poster';
      results.push({ pid: pid, t: 'meta_size', w: pr.width, h: pr.height });

      // --- 形状收集 ---
      (function walkShape(el) {
        if (!el || el.nodeType !== 1) return;
        if (skipTag(el.tagName.toLowerCase()) || skipCls(el.classList)) return;
        var s = getComputedStyle(el);
        var r = el.getBoundingClientRect();
        if (r.width === 0) return;
        var x = r.left - pr.left, y = r.top - pr.top, w = r.width, h = r.height;

        // hr
        if (el.tagName === 'HR') {
          results.push({pid:pid, t:'shape', sh:'rect', x:x, y:y, w:w, h:h, bg:s.backgroundColor || s.borderTopColor});
        }
        // card fill
        else if (el.classList.contains('card-fill') || el.classList.contains('card-ink') || el.classList.contains('card-accent')) {
          // border-left as accent stripe
          var bw = parseFloat(s.borderLeftWidth);
          if (bw > 0) results.push({pid:pid, t:'shape', sh:'rect', x:x, y:y, w:bw, h:h, bg:s.borderLeftColor});
          results.push({pid:pid, t:'shape', sh:'rect', x:x+bw, y:y, w:w-bw, h:h, bg:s.backgroundColor});
        }
        // marker dot
        else if (el.classList.contains('marker-dot')) {
          results.push({pid:pid, t:'shape', sh:'circle', x:x, y:y, w:w, h:h, bg:s.backgroundColor});
        }
        // check circle
        else if (el.classList.contains('check')) {
          results.push({pid:pid, t:'shape', sh:'circle', x:x, y:y, w:w, h:h, bg:s.backgroundColor});
        }
        // img / svg placeholder
        else if (['IMG', 'SVG'].includes(el.tagName)) {
          var isCircle = s.borderRadius.indexOf('50%') !== -1 || (parseFloat(s.borderRadius) || 0) >= w / 2;
          results.push({ pid:pid, t:'shape', sh: isCircle ? 'circle' : 'rect', x:x, y:y, w:w, h:h, bg:'#E2E8F0', placeholderName: 'Image Placeholder' });
        }
        // background div
        else if (['DIV','SECTION','ARTICLE','HEADER','FOOTER'].includes(el.tagName)) {
          var bg = s.backgroundColor;
          if (bg && bg !== 'transparent' && bg !== 'rgba(0, 0, 0, 0)') {
            results.push({pid:pid, t:'shape', sh:'rect', x:x, y:y, w:w, h:h, bg:bg});
          }
        }
        for (var ci = 0; ci < el.children.length; ci++) walkShape(el.children[ci]);
      })(poster);

      // --- 文字收集 (TreeWalker) ---
      var seen = [];

      // NodeFilter.SHOW_TEXT = 4
      var walker = document.createTreeWalker(poster, 4, {
        acceptNode: function(node) {
          if (!node.textContent.replace(/\s+/g, '').trim()) return NodeFilter.FILTER_REJECT;
          var p = node.parentElement;
          if (!p) return NodeFilter.FILTER_REJECT;
          // 跳过 canvas/script/style/img 内的文字
          if (skipTag(p.tagName.toLowerCase()) || skipCls(p.classList)) return NodeFilter.FILTER_REJECT;
          // 跳过隐藏文字
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

        // 检测原始文本是否有前后空白（inline 元素间的自然间距）
        var ws = '';
        if (/^\s/.test(raw)) ws += 'L';
        if (/\s$/.test(raw)) ws += 'R';

        // 用 Range API 取文本节点自身精确包围盒
        var range = document.createRange();
        range.selectNodeContents(walker.currentNode);
        var rect = range.getBoundingClientRect();
        range.detach();

        if (rect.width === 0 || rect.height === 0) continue;

        var px = Math.round(rect.left - pr.left);
        var py = Math.round(rect.top - pr.top);

        // 防抖：同标签下多个文本节点取最左最上
        var dup = seen.some(function(s) {
          return Math.abs(s[0] - px) < 3 && Math.abs(s[1] - py) < 3 && s[2] === p;
        });
        if (dup) continue;

        seen.push([px, py, p]);
        var st = getComputedStyle(p);

        results.push({
          pid: pid, t: 'text', text: txt,
          x: px, y: py, w: Math.round(rect.width), h: Math.round(rect.height),
          ff: st.fontFamily.split(',')[0].replace(/["']/g, '').trim() || 'PingFang SC',
          fw: st.fontWeight, fs: st.fontStyle,
          sz: st.fontSize, lh: st.lineHeight,
          clr: st.color, align: st.textAlign || 'left',
          ls: st.letterSpacing,
          ws: ws   // 原始 HTML 中的空白标记 "L"/"R"/"LR"/""
        });
      }
    });

    return results;
  });

  await browser.close();

  // ===== 去重 (只去重形状，TreeWalker 已保证文字唯一) =====
  var modSizes = {};
  var deduped = [];
  for (var i = 0; i < elements.length; i++) {
    var el = elements[i];
    if (el.t === 'meta_size') { modSizes[el.pid] = { w: el.w, h: el.h }; continue; }
    if (el.t === 'shape') {
      var overlap = deduped.some(function(e) {
        return e.pid === el.pid && e.t === 'shape' &&
          Math.abs(e.x - el.x) < 10 && Math.abs(e.y - el.y) < 10 &&
          Math.abs(e.w - el.w) < 10 && Math.abs(e.h - el.h) < 10;
      });
      if (!overlap) deduped.push(el);
    } else {
      deduped.push(el);
    }
  }

  // ===== 文本节点智能融合 (Text Node Fusion) =====
  var shapes = deduped.filter(function(e) { return e.t === 'shape'; });
  var texts = deduped.filter(function(e) { return e.t === 'text'; });

  // 按海报 + 空间坐标排序
  texts.sort(function(a, b) {
    if (a.pid !== b.pid) return a.pid < b.pid ? -1 : 1;
    if (Math.abs(a.y - b.y) > 8) return a.y - b.y;
    return a.x - b.x;
  });

  var fusedTexts = [];
  var current = null;

  for (var i = 0; i < texts.length; i++) {
    var t = texts[i];
    if (!current) {
      current = { pid: t.pid, t: 'text', text: t.text, x: t.x, y: t.y, w: t.w, h: t.h, ff: t.ff, fw: t.fw, fs: t.fs, sz: t.sz, lh: t.lh, clr: t.clr, align: t.align, ls: t.ls, _ws: t.ws };
      continue;
    }

    var samePid = current.pid === t.pid;
    var sameLine = Math.abs(current.y - t.y) <= 8;
    var gapX = t.x - (current.x + current.w);

    if (samePid && sameLine && gapX >= -5 && gapX <= 35) {
      // 用原始 HTML 的空白标记决定是否加空格，比用 gapX 更准
      var space = '';
      if (current._ws && current._ws.indexOf('R') >= 0) space = ' ';
      else if (t._ws && t._ws.indexOf('L') >= 0) space = ' ';
      else if (gapX > 6) space = ' ';  // 兜底：物理距离大时强加
      current.text += space + t.text;
      current.w = (t.x + t.w) - current.x;
      // 合并后的 ws 继承左节点（左边界不变）
    } else {
      fusedTexts.push(current);
      current = { pid: t.pid, t: 'text', text: t.text, x: t.x, y: t.y, w: t.w, h: t.h, ff: t.ff, fw: t.fw, fs: t.fs, sz: t.sz, lh: t.lh, clr: t.clr, align: t.align, ls: t.ls, _ws: t.ws };
    }
  }
  if (current) fusedTexts.push(current);

  var finalElements = shapes.concat(fusedTexts);

  // ===== 分组 + 排序 =====
  var groups = {};
  for (var i = 0; i < finalElements.length; i++) {
    var el = finalElements[i];
    if (!groups[el.pid]) groups[el.pid] = [];
    groups[el.pid].push(el);
  }

  // ===== 生成 .jsx =====
  var outDir = path.join(taskDir, 'output');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  var slug = path.basename(taskDir);
  var jsxPath = path.join(outDir, slug + '.jsx');
  var lines = [];

  lines.push('/**');
  lines.push(' * Social Card - Layered PSD Generator');
  lines.push(' * PS: File > Scripts > Browse > select this file');
  lines.push(' * Fonts matched dynamically from local app.fonts at runtime.');
  lines.push(' */');
  lines.push('');
  // ===== 注入 PS 运行时字体模糊匹配引擎 =====
  lines.push('function resolvePSFont(targetFamily, targetWeight, isItalic) {');
  lines.push('  var alias = { "notoserifsc":"SourceHanSerifCN", "notosanssc":"SourceHanSansCN",');
  lines.push('    "notoserif":"SourceHanSerif", "notosans":"SourceHanSans" };');
  lines.push('  var tryFamilies = [targetFamily];');
  lines.push('  var cleanOrig = targetFamily.toLowerCase().replace(/[\\s\\-_]/g, "");');
  lines.push('  if (alias[cleanOrig]) tryFamilies.push(alias[cleanOrig]);');
  lines.push('  var weightNum = parseInt(targetWeight) || 400;');
  lines.push('');
  lines.push('  var keywords = [];');
  lines.push('  if (isItalic) keywords.push("italic");');
  lines.push('  if (weightNum <= 200) keywords.push("extralight");');
  lines.push('  else if (weightNum <= 300) keywords.push("light");');
  lines.push('  else if (weightNum >= 700) keywords.push("bold");');
  lines.push('  else if (weightNum >= 500) keywords.push("medium");');
  lines.push('  else keywords.push("regular");');
  lines.push('');
  lines.push('  var localFonts = app.fonts;');
  lines.push('  var firstFamilyMatch = null;');
  lines.push('');
  lines.push('  for (var t = 0; t < tryFamilies.length; t++) {');
  lines.push('    var tf = tryFamilies[t];');
  lines.push('    var cleanFamily = tf.toLowerCase().replace(/[\\s\\-_]/g, "");');
  lines.push('    for (var i = 0; i < localFonts.length; i++) {');
  lines.push('      var f = localFonts[i];');
  lines.push('      var localFam = f.family.toLowerCase().replace(/[\\s\\-_]/g, "");');
  lines.push('      var localStyle = f.style.toLowerCase();');
  lines.push('');
  lines.push('      if (localFam === cleanFamily || f.family.toLowerCase().replace(/[\\s\\-_]/g, "") === tf.toLowerCase().replace(/[\\s\\-_]/g, "")) {');
  lines.push('        if (!firstFamilyMatch) firstFamilyMatch = f.postScriptName;');
  lines.push('        var isStyleMatch = true;');
  lines.push('        for (var k = 0; k < keywords.length; k++) {');
  lines.push('          if (localStyle.indexOf(keywords[k]) === -1) { isStyleMatch = false; break; }');
  lines.push('        }');
  lines.push('        if (isStyleMatch) return f.postScriptName;');
  lines.push('      }');
  lines.push('    }');
  lines.push('  }');
  lines.push('  if (firstFamilyMatch) return firstFamilyMatch;');
  lines.push('  // 智能回退：按字体类别选最接近的本地字体');
  lines.push('  var origName = tryFamilies[0];');
  lines.push('  var isSerif = /serif|song|ming|kai|fang|times|playfair|georgia|garamond/i.test(origName);');
  lines.push('  var isMono = /mono|consolas|courier|code/i.test(origName);');
  lines.push('  var isChinese = /song|hei|ming|kai|fang|noto|pingfang|microsoft.*yahei|simsun|simhei|思源|SourceHan/i.test(origName);');
  lines.push('  if ($.os.indexOf("Mac") > -1) {');
  lines.push('    return isMono ? "Menlo-Regular" : isSerif ? "TimesNewRomanPSMT" : "Helvetica";');
  lines.push('  }');
  lines.push('  if (isMono) return "Consolas";');
  lines.push('  if (isChinese) return isSerif ? "SourceHanSerifCN-Regular" : "SourceHanSansCN-Regular";');
  lines.push('  return isSerif ? "TimesNewRomanPSMT" : "ArialMT";');
  lines.push('}');
  lines.push('');
  lines.push('// ===== 原生 PS Fill Layer 引擎 (ActionManager) =====');
  lines.push('function createColorLayer(name, r, g, b, opacity) {');
  lines.push('  if (opacity === undefined) opacity = 100;');
  lines.push('  var desc = new ActionDescriptor(), ref = new ActionReference();');
  lines.push('  ref.putClass(stringIDToTypeID("contentLayer"));');
  lines.push('  desc.putReference(charIDToTypeID("null"), ref);');
  lines.push('  var desc2 = new ActionDescriptor(), desc3 = new ActionDescriptor();');
  lines.push('  desc3.putDouble(charIDToTypeID("Rd  "), r);');
  lines.push('  desc3.putDouble(charIDToTypeID("Grn "), g);');
  lines.push('  desc3.putDouble(charIDToTypeID("Bl  "), b);');
  lines.push('  var desc4 = new ActionDescriptor();');
  lines.push('  desc4.putObject(charIDToTypeID("Clr "), charIDToTypeID("RGBC"), desc3);');
  lines.push('  desc2.putObject(charIDToTypeID("Type"), stringIDToTypeID("solidColorLayer"), desc4);');
  lines.push('  desc.putObject(charIDToTypeID("Usng"), stringIDToTypeID("contentLayer"), desc2);');
  lines.push('  executeAction(charIDToTypeID("Mk  "), desc, DialogModes.NO);');
  lines.push('  app.activeDocument.activeLayer.name = name;');
  lines.push('  if (opacity < 100) app.activeDocument.activeLayer.opacity = opacity;');
  lines.push('}');
  lines.push('function selectEllipse(x, y, w, h) {');
  lines.push('  var desc = new ActionDescriptor(), ref = new ActionReference();');
  lines.push('  ref.putProperty(charIDToTypeID("Chnl"), charIDToTypeID("fsel"));');
  lines.push('  desc.putReference(charIDToTypeID("null"), ref);');
  lines.push('  var desc2 = new ActionDescriptor();');
  lines.push('  desc2.putUnitDouble(charIDToTypeID("Top "), charIDToTypeID("#Pxl"), y);');
  lines.push('  desc2.putUnitDouble(charIDToTypeID("Left"), charIDToTypeID("#Pxl"), x);');
  lines.push('  desc2.putUnitDouble(charIDToTypeID("Btom"), charIDToTypeID("#Pxl"), y+h);');
  lines.push('  desc2.putUnitDouble(charIDToTypeID("Rght"), charIDToTypeID("#Pxl"), x+w);');
  lines.push('  desc.putObject(charIDToTypeID("T   "), charIDToTypeID("Elps"), desc2);');
  lines.push('  desc.putBoolean(charIDToTypeID("AntA"), true);');
  lines.push('  executeAction(charIDToTypeID("setd"), desc, DialogModes.NO);');
  lines.push('}');
  lines.push('');

  var SCALE = 2;
  var ln = 0;

  // ===== 遍历海报生成图层 =====
  var posterIndex = 0;
  for (var pid in groups) {
    posterIndex++;
    var num = String(posterIndex).padStart(2, '0');
    var els = groups[pid];
    lines.push('// ===== ' + pid + ' =====');
    var modW = modSizes[pid] ? Math.round(modSizes[pid].w * SCALE) : 2160;
    var modH = modSizes[pid] ? Math.round(modSizes[pid].h * SCALE) : 2880;
    lines.push('var doc = app.documents.add(' + modW + ', ' + modH + ', 72, "' + slug + '_' + num + '", NewDocumentMode.RGB);');
    lines.push('app.preferences.rulerUnits = Units.PIXELS;');
    lines.push('');

    // 创建图层编组
    lines.push('var groupBg = doc.layerSets.add();');
    lines.push('groupBg.name = "背景与形状 (Backgrounds & Shapes)";');
    lines.push('var groupText = doc.layerSets.add();');
    lines.push('groupText.name = "排版文字 (Typography)";');
    lines.push('');

    // 排序：形状在底，文字在上
    els.sort(function(a, b) {
      if (a.t !== b.t) return a.t === 'shape' ? -1 : 1;
      if (Math.abs(a.y - b.y) > 10) return a.y - b.y;
      return a.x - b.x;
    });

    for (var j = 0; j < els.length; j++) {
      var el = els[j];
      ln++;
      var vn = 'L' + ln;

      if (el.t === 'shape') {
        var rgb = extractRGB(el.bg);
        var alphaPct = Math.round((rgb[3] || 255) / 255 * 100);
        if (alphaPct === 0) continue;

        var rx = Math.round(el.x * SCALE), ry = Math.round(el.y * SCALE), rw = Math.round(el.w * SCALE), rh = Math.round(el.h * SCALE);
        var shName = el.sh === 'circle' ? 'Circle Fill' : 'Rect Fill';

        lines.push('// ' + shName);
        lines.push('app.activeDocument.activeLayer = groupBg;');
        if (el.sh === 'circle') {
          lines.push('selectEllipse(' + rx + ', ' + ry + ', ' + rw + ', ' + rh + ');');
        } else {
          lines.push('doc.selection.select([[' + rx + ',' + ry + '],[' + (rx+rw) + ',' + ry + '],[' + (rx+rw) + ',' + (ry+rh) + '],[' + rx + ',' + (ry+rh) + ']]);');
        }
        lines.push('createColorLayer("' + shName + '", ' + rgb[0] + ', ' + rgb[1] + ', ' + rgb[2] + ', ' + alphaPct + ');');
        lines.push('doc.selection.deselect();');
        lines.push('');
        continue;
      }

      if (el.t === 'text') {
        var psColor = cssColorToPS(el.clr);
        var sz = (parseFloat(el.sz) || 24) * SCALE;
        var lh = el.lh !== 'normal' ? parseFloat(el.lh) * SCALE : sz * 1.4;
        var ls = el.ls !== 'normal' ? (parseFloat(el.ls) || 0) * 100 : 0;
        var safe = el.text.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/\n/g, '\\n');
        var nm = safe.replace(/['"\\]/g, '').replace(/\s+/g, ' ').slice(0, 28);

        lines.push('// "' + nm + '"');
        lines.push(psColor + ';');
        lines.push('var ' + vn + ' = groupText.artLayers.add();');
        lines.push(vn + '.name = "' + nm + '";');
        lines.push(vn + '.kind = LayerKind.TEXT;');

        lines.push('var ti = ' + vn + '.textItem;');

        // 段落文本 (Paragraph Text) 代替点文本
        lines.push('ti.kind = TextType.PARAGRAPHTEXT;');
        var pad = (el.ff && el.ff.toLowerCase().indexOf('serif') !== -1) ? Math.max(30 * SCALE, sz * 0.6) : Math.max(18 * SCALE, sz * 0.4);
        lines.push('ti.width = ' + Math.round(el.w * SCALE + pad) + ';');
        lines.push('ti.height = ' + Math.round(el.h * SCALE + sz) + ';');

        lines.push("ti.contents = '" + safe + "';");
        lines.push('ti.font = resolvePSFont("' + el.ff + '", "' + el.fw + '", ' + (el.fs === 'italic' ? 'true' : 'false') + ');');
        lines.push('ti.size = ' + sz + ';');
        lines.push('ti.color = c;');
        lines.push('ti.leading = ' + Math.round(lh) + ';');
        lines.push('ti.tracking = ' + Math.round(ls) + ';');

        // 对齐方式
        var al = 'Justification.LEFT';
        if (el.align === 'center') al = 'Justification.CENTER';
        else if (el.align === 'right') al = 'Justification.RIGHT';
        lines.push('ti.justification = ' + al + ';');

        // 段落文本的 position 取左上角原点
        lines.push('ti.position = Array(' + Math.round(el.x * SCALE) + ', ' + Math.round(el.y * SCALE) + ');');
        lines.push('');
      }
    }
    // 每个 poster 独立保存 + 关闭
    lines.push('var sf = new File(Folder.desktop + "/' + slug + '_' + num + '.psd");');
    lines.push('doc.saveAs(sf);');
    lines.push('doc.close(SaveOptions.DONOTSAVECHANGES);');
    lines.push('');
  }

  lines.push('alert("✅ PSD 已存入桌面！共 ' + Object.keys(groups).length + ' 个文件。");');

  fs.writeFileSync(jsxPath, '\uFEFF' + lines.join('\r\n'), 'utf-8');

  var tc = 0, sc = 0;
  finalElements.forEach(function(e) { if (e.t === 'text') tc++; else sc++; });
  console.log('OK: ' + jsxPath);
  console.log('   ' + deduped.length + ' elements (' + tc + ' text, ' + sc + ' shapes)');
  console.log('   Run in Photoshop to get layered PSD');
})();
