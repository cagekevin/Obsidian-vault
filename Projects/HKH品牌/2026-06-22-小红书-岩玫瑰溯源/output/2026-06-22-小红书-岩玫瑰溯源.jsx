/**
 * Social Card - Layered PSD Generator
 * PS: File > Scripts > Browse > select this file
 * Fonts matched dynamically from local app.fonts at runtime.
 */

function resolvePSFont(targetFamily, targetWeight, isItalic) {
  var alias = { "notoserifsc":"SourceHanSerifCN", "notosanssc":"SourceHanSansCN",
    "notoserif":"SourceHanSerif", "notosans":"SourceHanSans" };
  var tryFamilies = [targetFamily];
  var cleanOrig = targetFamily.toLowerCase().replace(/[\s\-_]/g, "");
  if (alias[cleanOrig]) tryFamilies.push(alias[cleanOrig]);
  var weightNum = parseInt(targetWeight) || 400;

  var keywords = [];
  if (isItalic) keywords.push("italic");
  if (weightNum <= 200) keywords.push("extralight");
  else if (weightNum <= 300) keywords.push("light");
  else if (weightNum >= 700) keywords.push("bold");
  else if (weightNum >= 500) keywords.push("medium");
  else keywords.push("regular");

  var localFonts = app.fonts;
  var firstFamilyMatch = null;

  for (var t = 0; t < tryFamilies.length; t++) {
    var tf = tryFamilies[t];
    var cleanFamily = tf.toLowerCase().replace(/[\s\-_]/g, "");
    for (var i = 0; i < localFonts.length; i++) {
      var f = localFonts[i];
      var localFam = f.family.toLowerCase().replace(/[\s\-_]/g, "");
      var localStyle = f.style.toLowerCase();

      if (localFam === cleanFamily || f.family.toLowerCase().replace(/[\s\-_]/g, "") === tf.toLowerCase().replace(/[\s\-_]/g, "")) {
        if (!firstFamilyMatch) firstFamilyMatch = f.postScriptName;
        var isStyleMatch = true;
        for (var k = 0; k < keywords.length; k++) {
          if (localStyle.indexOf(keywords[k]) === -1) { isStyleMatch = false; break; }
        }
        if (isStyleMatch) return f.postScriptName;
      }
    }
  }
  if (firstFamilyMatch) return firstFamilyMatch;
  // 智能回退：按字体类别选最接近的本地字体
  var origName = tryFamilies[0];
  var isSerif = /serif|song|ming|kai|fang|times|playfair|georgia|garamond/i.test(origName);
  var isMono = /mono|consolas|courier|code/i.test(origName);
  var isChinese = /song|hei|ming|kai|fang|noto|pingfang|microsoft.*yahei|simsun|simhei|思源|SourceHan/i.test(origName);
  if ($.os.indexOf("Mac") > -1) {
    return isMono ? "Menlo-Regular" : isSerif ? "TimesNewRomanPSMT" : "Helvetica";
  }
  if (isMono) return "Consolas";
  if (isChinese) return isSerif ? "SourceHanSerifCN-Regular" : "SourceHanSansCN-Regular";
  return isSerif ? "TimesNewRomanPSMT" : "ArialMT";
}

// ===== 原生 PS Fill Layer 引擎 (ActionManager) =====
function createColorLayer(name, r, g, b, opacity) {
  if (opacity === undefined) opacity = 100;
  var desc = new ActionDescriptor(), ref = new ActionReference();
  ref.putClass(stringIDToTypeID("contentLayer"));
  desc.putReference(charIDToTypeID("null"), ref);
  var desc2 = new ActionDescriptor(), desc3 = new ActionDescriptor();
  desc3.putDouble(charIDToTypeID("Rd  "), r);
  desc3.putDouble(charIDToTypeID("Grn "), g);
  desc3.putDouble(charIDToTypeID("Bl  "), b);
  var desc4 = new ActionDescriptor();
  desc4.putObject(charIDToTypeID("Clr "), charIDToTypeID("RGBC"), desc3);
  desc2.putObject(charIDToTypeID("Type"), stringIDToTypeID("solidColorLayer"), desc4);
  desc.putObject(charIDToTypeID("Usng"), stringIDToTypeID("contentLayer"), desc2);
  executeAction(charIDToTypeID("Mk  "), desc, DialogModes.NO);
  app.activeDocument.activeLayer.name = name;
  if (opacity < 100) app.activeDocument.activeLayer.opacity = opacity;
}
function selectEllipse(x, y, w, h) {
  var desc = new ActionDescriptor(), ref = new ActionReference();
  ref.putProperty(charIDToTypeID("Chnl"), charIDToTypeID("fsel"));
  desc.putReference(charIDToTypeID("null"), ref);
  var desc2 = new ActionDescriptor();
  desc2.putUnitDouble(charIDToTypeID("Top "), charIDToTypeID("#Pxl"), y);
  desc2.putUnitDouble(charIDToTypeID("Left"), charIDToTypeID("#Pxl"), x);
  desc2.putUnitDouble(charIDToTypeID("Btom"), charIDToTypeID("#Pxl"), y+h);
  desc2.putUnitDouble(charIDToTypeID("Rght"), charIDToTypeID("#Pxl"), x+w);
  desc.putObject(charIDToTypeID("T   "), charIDToTypeID("Elps"), desc2);
  desc.putBoolean(charIDToTypeID("AntA"), true);
  executeAction(charIDToTypeID("setd"), desc, DialogModes.NO);
}

// ===== xhs-01 =====
var doc = app.documents.add(2160, 2880, 72, "2026-06-22-小红书-岩玫瑰溯源_01", NewDocumentMode.RGB);
app.preferences.rulerUnits = Units.PIXELS;

var groupBg = doc.layerSets.add();
groupBg.name = "背景与形状 (Backgrounds & Shapes)";
var groupText = doc.layerSets.add();
groupText.name = "排版文字 (Typography)";

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[0,0],[2160,0],[2160,2880],[0,2880]]);
createColorLayer("Rect Fill", 240, 230, 210, 100);
doc.selection.deselect();

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[176,1012],[1984,1012],[1984,2284],[176,2284]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// "盛夏绽放"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L3 = groupText.artLayers.add();
L3.name = "盛夏绽放";
L3.kind = LayerKind.TEXT;
var ti = L3.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 216;
ti.height = 94;
ti.contents = '盛夏绽放';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "岩玫瑰溯源"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L4 = groupText.artLayers.add();
L4.name = "岩玫瑰溯源";
L4.kind = LayerKind.TEXT;
var ti = L4.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 260;
ti.height = 94;
ti.contents = '岩玫瑰溯源';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(432, 192);

// "天光眷顾"
var c = new SolidColor(); c.rgb.red=31; c.rgb.green=26; c.rgb.blue=20; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L5 = groupText.artLayers.add();
L5.name = "天光眷顾";
L5.kind = LayerKind.TEXT;
var ti = L5.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1181;
ti.height = 604;
ti.contents = '天光眷顾';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 248;
ti.color = c;
ti.leading = 263;
ti.tracking = 496;
ti.justification = Justification.LEFT;
ti.position = Array(176, 294);

// "源起之地"
var c = new SolidColor(); c.rgb.red=31; c.rgb.green=26; c.rgb.blue=20; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L6 = groupText.artLayers.add();
L6.name = "源起之地";
L6.kind = LayerKind.TEXT;
var ti = L6.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1181;
ti.height = 604;
ti.contents = '源起之地';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 248;
ti.color = c;
ti.leading = 263;
ti.tracking = 496;
ti.justification = Justification.LEFT;
ti.position = Array(176, 556);

// "地中海沿岸的盛夏，炽热阳光和滚烫的碎石，绝大多数植物选择"
var c = new SolidColor(); c.rgb.red=31; c.rgb.green=26; c.rgb.blue=20; c; var _oa=82; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L7 = groupText.artLayers.add();
L7.name = "地中海沿岸的盛夏，炽热阳光和滚烫的碎石，绝大多数植物选择";
L7.kind = LayerKind.TEXT;
var ti = L7.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1852;
ti.height = 310;
ti.contents = '地中海沿岸的盛夏，炽热阳光和滚烫的碎石，绝大多数植物选择干枯和休眠，而这里的岩玫瑰却将灼热的日光视作赏赐，默默储蓄整个夏天充沛的疗愈能量。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 87;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2382);

// "源起 · Origin"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L8 = groupText.artLayers.add();
L8.name = "源起 · Origin";
L8.kind = LayerKind.TEXT;
var ti = L8.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 350;
ti.height = 82;
ti.contents = '源起 · Origin';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "—"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L9 = groupText.artLayers.add();
L9.name = "—";
L9.kind = LayerKind.TEXT;
var ti = L9.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 62;
ti.height = 82;
ti.contents = '—';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1160, 2722);

// "1 / 4"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L10 = groupText.artLayers.add();
L10.name = "1 / 4";
L10.kind = LayerKind.TEXT;
var ti = L10.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 166;
ti.height = 82;
ti.contents = '1 / 4';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1854, 2722);

var sf = new File(Folder.desktop + "/2026-06-22-小红书-岩玫瑰溯源_01.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

// ===== xhs-02 =====
var doc = app.documents.add(2160, 2880, 72, "2026-06-22-小红书-岩玫瑰溯源_02", NewDocumentMode.RGB);
app.preferences.rulerUnits = Units.PIXELS;

var groupBg = doc.layerSets.add();
groupBg.name = "背景与形状 (Backgrounds & Shapes)";
var groupText = doc.layerSets.add();
groupText.name = "排版文字 (Typography)";

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[0,0],[2160,0],[2160,2880],[0,2880]]);
createColorLayer("Rect Fill", 240, 230, 210, 100);
doc.selection.deselect();

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[176,1012],[1984,1012],[1984,2284],[176,2284]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// "盛夏绽放"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L13 = groupText.artLayers.add();
L13.name = "盛夏绽放";
L13.kind = LayerKind.TEXT;
var ti = L13.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 216;
ti.height = 94;
ti.contents = '盛夏绽放';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "岩玫瑰溯源"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L14 = groupText.artLayers.add();
L14.name = "岩玫瑰溯源";
L14.kind = LayerKind.TEXT;
var ti = L14.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 260;
ti.height = 94;
ti.contents = '岩玫瑰溯源';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(432, 192);

// "循光而生"
var c = new SolidColor(); c.rgb.red=31; c.rgb.green=26; c.rgb.blue=20; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L15 = groupText.artLayers.add();
L15.name = "循光而生";
L15.kind = LayerKind.TEXT;
var ti = L15.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1181;
ti.height = 604;
ti.contents = '循光而生';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 248;
ti.color = c;
ti.leading = 263;
ti.tracking = 496;
ti.justification = Justification.LEFT;
ti.position = Array(176, 294);

// "自成光芒"
var c = new SolidColor(); c.rgb.red=31; c.rgb.green=26; c.rgb.blue=20; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L16 = groupText.artLayers.add();
L16.name = "自成光芒";
L16.kind = LayerKind.TEXT;
var ti = L16.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1181;
ti.height = 604;
ti.contents = '自成光芒';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 248;
ti.color = c;
ti.leading = 263;
ti.tracking = 496;
ti.justification = Justification.LEFT;
ti.position = Array(176, 556);

// "日光越是炽烈、毒辣，岩玫瑰便越是肆意地交织出生存的哲学。"
var c = new SolidColor(); c.rgb.red=31; c.rgb.green=26; c.rgb.blue=20; c; var _oa=82; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L17 = groupText.artLayers.add();
L17.name = "日光越是炽烈、毒辣，岩玫瑰便越是肆意地交织出生存的哲学。";
L17.kind = LayerKind.TEXT;
var ti = L17.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1852;
ti.height = 310;
ti.contents = '日光越是炽烈、毒辣，岩玫瑰便越是肆意地交织出生存的哲学。从枝梢间缓缓渗出的琥珀般金色油脂，是天地淬炼的"浓缩养分库"，治愈自我，也治愈肌肤。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 87;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2382);

// "生存 · Survival"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L18 = groupText.artLayers.add();
L18.name = "生存 · Survival";
L18.kind = LayerKind.TEXT;
var ti = L18.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 402;
ti.height = 82;
ti.contents = '生存 · Survival';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "—"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L19 = groupText.artLayers.add();
L19.name = "—";
L19.kind = LayerKind.TEXT;
var ti = L19.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 62;
ti.height = 82;
ti.contents = '—';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1186, 2722);

// "2 / 4"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L20 = groupText.artLayers.add();
L20.name = "2 / 4";
L20.kind = LayerKind.TEXT;
var ti = L20.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 166;
ti.height = 82;
ti.contents = '2 / 4';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1854, 2722);

var sf = new File(Folder.desktop + "/2026-06-22-小红书-岩玫瑰溯源_02.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

// ===== xhs-03 =====
var doc = app.documents.add(2160, 2880, 72, "2026-06-22-小红书-岩玫瑰溯源_03", NewDocumentMode.RGB);
app.preferences.rulerUnits = Units.PIXELS;

var groupBg = doc.layerSets.add();
groupBg.name = "背景与形状 (Backgrounds & Shapes)";
var groupText = doc.layerSets.add();
groupText.name = "排版文字 (Typography)";

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[0,0],[2160,0],[2160,2880],[0,2880]]);
createColorLayer("Rect Fill", 240, 230, 210, 100);
doc.selection.deselect();

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[176,1012],[1984,1012],[1984,2284],[176,2284]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// "盛夏绽放"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L23 = groupText.artLayers.add();
L23.name = "盛夏绽放";
L23.kind = LayerKind.TEXT;
var ti = L23.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 216;
ti.height = 94;
ti.contents = '盛夏绽放';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "岩玫瑰溯源"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L24 = groupText.artLayers.add();
L24.name = "岩玫瑰溯源";
L24.kind = LayerKind.TEXT;
var ti = L24.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 260;
ti.height = 94;
ti.contents = '岩玫瑰溯源';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(432, 192);

// "黄金时刻"
var c = new SolidColor(); c.rgb.red=31; c.rgb.green=26; c.rgb.blue=20; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L25 = groupText.artLayers.add();
L25.name = "黄金时刻";
L25.kind = LayerKind.TEXT;
var ti = L25.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1181;
ti.height = 604;
ti.contents = '黄金时刻';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 248;
ti.color = c;
ti.leading = 263;
ti.tracking = 496;
ti.justification = Justification.LEFT;
ti.position = Array(176, 294);

// "留住活性"
var c = new SolidColor(); c.rgb.red=31; c.rgb.green=26; c.rgb.blue=20; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L26 = groupText.artLayers.add();
L26.name = "留住活性";
L26.kind = LayerKind.TEXT;
var ti = L26.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1181;
ti.height = 604;
ti.contents = '留住活性';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 248;
ti.color = c;
ti.leading = 263;
ti.tracking = 496;
ti.justification = Justification.LEFT;
ti.position = Array(176, 556);

// "当地居民默默守护着古老的默契，不强求，不干预。何时开花何"
var c = new SolidColor(); c.rgb.red=31; c.rgb.green=26; c.rgb.blue=20; c; var _oa=82; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L27 = groupText.artLayers.add();
L27.name = "当地居民默默守护着古老的默契，不强求，不干预。何时开花何";
L27.kind = LayerKind.TEXT;
var ti = L27.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1852;
ti.height = 310;
ti.contents = '当地居民默默守护着古老的默契，不强求，不干预。何时开花何时采摘，自然早有答案。直到盛夏之巅，岩玫瑰活性最高、油脂最浓，即刻采收，只为在活性巅峰将它完整封存。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 87;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2382);

// "采收 · Harvest"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L28 = groupText.artLayers.add();
L28.name = "采收 · Harvest";
L28.kind = LayerKind.TEXT;
var ti = L28.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 376;
ti.height = 82;
ti.contents = '采收 · Harvest';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "—"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L29 = groupText.artLayers.add();
L29.name = "—";
L29.kind = LayerKind.TEXT;
var ti = L29.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 62;
ti.height = 82;
ti.contents = '—';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1172, 2722);

// "3 / 4"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L30 = groupText.artLayers.add();
L30.name = "3 / 4";
L30.kind = LayerKind.TEXT;
var ti = L30.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 166;
ti.height = 82;
ti.contents = '3 / 4';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1854, 2722);

var sf = new File(Folder.desktop + "/2026-06-22-小红书-岩玫瑰溯源_03.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

// ===== xhs-04 =====
var doc = app.documents.add(2160, 2880, 72, "2026-06-22-小红书-岩玫瑰溯源_04", NewDocumentMode.RGB);
app.preferences.rulerUnits = Units.PIXELS;

var groupBg = doc.layerSets.add();
groupBg.name = "背景与形状 (Backgrounds & Shapes)";
var groupText = doc.layerSets.add();
groupText.name = "排版文字 (Typography)";

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[0,0],[2160,0],[2160,2880],[0,2880]]);
createColorLayer("Rect Fill", 240, 230, 210, 100);
doc.selection.deselect();

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[176,1012],[1984,1012],[1984,2284],[176,2284]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// "盛夏绽放"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L33 = groupText.artLayers.add();
L33.name = "盛夏绽放";
L33.kind = LayerKind.TEXT;
var ti = L33.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 216;
ti.height = 94;
ti.contents = '盛夏绽放';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "岩玫瑰溯源"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L34 = groupText.artLayers.add();
L34.name = "岩玫瑰溯源";
L34.kind = LayerKind.TEXT;
var ti = L34.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 260;
ti.height = 94;
ti.contents = '岩玫瑰溯源';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(432, 192);

// "敬畏自然"
var c = new SolidColor(); c.rgb.red=31; c.rgb.green=26; c.rgb.blue=20; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L35 = groupText.artLayers.add();
L35.name = "敬畏自然";
L35.kind = LayerKind.TEXT;
var ti = L35.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1181;
ti.height = 604;
ti.contents = '敬畏自然';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 248;
ti.color = c;
ti.leading = 263;
ti.tracking = 496;
ti.justification = Justification.LEFT;
ti.position = Array(176, 294);

// "浴火重生"
var c = new SolidColor(); c.rgb.red=31; c.rgb.green=26; c.rgb.blue=20; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L36 = groupText.artLayers.add();
L36.name = "浴火重生";
L36.kind = LayerKind.TEXT;
var ti = L36.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1181;
ti.height = 604;
ti.contents = '浴火重生';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 248;
ti.color = c;
ti.leading = 263;
ti.tracking = 496;
ti.justification = Justification.LEFT;
ti.position = Array(176, 556);

// "采摘不是全部据为己有，而是克制和对自然的敬畏。保留一部分"
var c = new SolidColor(); c.rgb.red=31; c.rgb.green=26; c.rgb.blue=20; c; var _oa=82; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L37 = groupText.artLayers.add();
L37.name = "采摘不是全部据为己有，而是克制和对自然的敬畏。保留一部分";
L37.kind = LayerKind.TEXT;
var ti = L37.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1852;
ti.height = 310;
ti.contents = '采摘不是全部据为己有，而是克制和对自然的敬畏。保留一部分岩玫瑰的花朵与枝干，在烈日中凝练，在自燃的烈火中涅槃。当灰烬成为新生的温床，种子便能在寂灭里浴火重生。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 87;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2382);

// "涅槃 · Rebirth"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L38 = groupText.artLayers.add();
L38.name = "涅槃 · Rebirth";
L38.kind = LayerKind.TEXT;
var ti = L38.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 376;
ti.height = 82;
ti.contents = '涅槃 · Rebirth';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "—"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L39 = groupText.artLayers.add();
L39.name = "—";
L39.kind = LayerKind.TEXT;
var ti = L39.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 62;
ti.height = 82;
ti.contents = '—';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1172, 2722);

// "4 / 4"
var c = new SolidColor(); c.rgb.red=111; c.rgb.green=101; c.rgb.blue=87; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L40 = groupText.artLayers.add();
L40.name = "4 / 4";
L40.kind = LayerKind.TEXT;
var ti = L40.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 166;
ti.height = 82;
ti.contents = '4 / 4';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1854, 2722);

var sf = new File(Folder.desktop + "/2026-06-22-小红书-岩玫瑰溯源_04.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

alert("✅ PSD 已存入桌面！共 4 个文件。");