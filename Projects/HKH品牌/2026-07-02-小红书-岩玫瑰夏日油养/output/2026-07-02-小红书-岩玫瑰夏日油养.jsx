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
var doc = app.documents.add(2160, 2880, 72, "2026-07-02-小红书-岩玫瑰夏日油养_01", NewDocumentMode.RGB);
app.preferences.rulerUnits = Units.PIXELS;

var groupBg = doc.layerSets.add();
groupBg.name = "背景与形状 (Backgrounds & Shapes)";
var groupText = doc.layerSets.add();
groupText.name = "排版文字 (Typography)";

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[0,0],[2160,0],[2160,2880],[0,2880]]);
createColorLayer("Rect Fill", 245, 241, 232, 100);
doc.selection.deselect();

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[492,1033],[1667,1033],[1667,2370],[492,2370]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// "HKH"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L3 = groupText.artLayers.add();
L3.name = "HKH";
L3.kind = LayerKind.TEXT;
var ti = L3.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 122;
ti.height = 94;
ti.contents = 'HKH';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "岩玫瑰系列"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L4 = groupText.artLayers.add();
L4.name = "岩玫瑰系列";
L4.kind = LayerKind.TEXT;
var ti = L4.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 260;
ti.height = 94;
ti.contents = '岩玫瑰系列';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(338, 192);

// "夏日限定 · 清爽上市"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=55; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L5 = groupText.artLayers.add();
L5.name = "夏日限定 · 清爽上市";
L5.kind = LayerKind.TEXT;
var ti = L5.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 550;
ti.height = 98;
ti.contents = '夏日限定 · 清爽上市';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 42;
ti.color = c;
ti.leading = 59;
ti.tracking = 462;
ti.justification = Justification.LEFT;
ti.position = Array(176, 342);

// "夏日油养 清爽上市"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L6 = groupText.artLayers.add();
L6.name = "夏日油养 清爽上市";
L6.kind = LayerKind.TEXT;
var ti = L6.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1769;
ti.height = 466;
ti.contents = '夏日油养 清爽上市';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 192;
ti.color = c;
ti.leading = 204;
ti.tracking = 384;
ti.justification = Justification.LEFT;
ti.position = Array(176, 446);

// "一键轻盈入夏"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L7 = groupText.artLayers.add();
L7.name = "一键轻盈入夏";
L7.kind = LayerKind.TEXT;
var ti = L7.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1313;
ti.height = 466;
ti.contents = '一键轻盈入夏';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 192;
ti.color = c;
ti.leading = 204;
ti.tracking = 384;
ti.justification = Justification.LEFT;
ti.position = Array(176, 650);

// "打破精华油黏腻刻板印象"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=82; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L8 = groupText.artLayers.add();
L8.name = "打破精华油黏腻刻板印象";
L8.kind = LayerKind.TEXT;
var ti = L8.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 676;
ti.height = 136;
ti.contents = '打破精华油黏腻刻板印象';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 87;
ti.tracking = 0;
ti.justification = Justification.CENTER;
ti.position = Array(772, 2468);

// "轻薄感与滋润度的更佳平衡"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=82; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L9 = groupText.artLayers.add();
L9.name = "轻薄感与滋润度的更佳平衡";
L9.kind = LayerKind.TEXT;
var ti = L9.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 732;
ti.height = 136;
ti.contents = '轻薄感与滋润度的更佳平衡';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 87;
ti.tracking = 0;
ti.justification = Justification.CENTER;
ti.position = Array(744, 2556);

// "清爽版 · 哑光丝绒"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L10 = groupText.artLayers.add();
L10.name = "清爽版 · 哑光丝绒";
L10.kind = LayerKind.TEXT;
var ti = L10.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 396;
ti.height = 82;
ti.contents = '清爽版 · 哑光丝绒';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "✦"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L11 = groupText.artLayers.add();
L11.name = "✦";
L11.kind = LayerKind.TEXT;
var ti = L11.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 70;
ti.height = 82;
ti.contents = '✦';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1062, 2722);

// "唤醒肌肤轻润呼吸感"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L12 = groupText.artLayers.add();
L12.name = "唤醒肌肤轻润呼吸感";
L12.kind = LayerKind.TEXT;
var ti = L12.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 398;
ti.height = 82;
ti.contents = '唤醒肌肤轻润呼吸感';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1622, 2722);

var sf = new File(Folder.desktop + "/2026-07-02-小红书-岩玫瑰夏日油养_01.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

// ===== xhs-02 =====
var doc = app.documents.add(2160, 2880, 72, "2026-07-02-小红书-岩玫瑰夏日油养_02", NewDocumentMode.RGB);
app.preferences.rulerUnits = Units.PIXELS;

var groupBg = doc.layerSets.add();
groupBg.name = "背景与形状 (Backgrounds & Shapes)";
var groupText = doc.layerSets.add();
groupText.name = "排版文字 (Typography)";

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[0,0],[2160,0],[2160,2880],[0,2880]]);
createColorLayer("Rect Fill", 245, 241, 232, 100);
doc.selection.deselect();

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[176,1282],[1317,1282],[1317,1541],[176,1541]]);
createColorLayer("Rect Fill", 232, 223, 207, 100);
doc.selection.deselect();

// "配方升级"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L15 = groupText.artLayers.add();
L15.name = "配方升级";
L15.kind = LayerKind.TEXT;
var ti = L15.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 216;
ti.height = 94;
ti.contents = '配方升级';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "肤感特调"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L16 = groupText.artLayers.add();
L16.name = "肤感特调";
L16.kind = LayerKind.TEXT;
var ti = L16.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 216;
ti.height = 94;
ti.contents = '肤感特调';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(432, 192);

// "更适合夏日的"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L17 = groupText.artLayers.add();
L17.name = "更适合夏日的";
L17.kind = LayerKind.TEXT;
var ti = L17.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1194;
ti.height = 428;
ti.contents = '更适合夏日的';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 176;
ti.color = c;
ti.leading = 194;
ti.tracking = 264;
ti.justification = Justification.LEFT;
ti.position = Array(176, 264);

// "油养配方"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L18 = groupText.artLayers.add();
L18.name = "油养配方";
L18.kind = LayerKind.TEXT;
var ti = L18.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 832;
ti.height = 428;
ti.contents = '油养配方';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 176;
ti.color = c;
ti.leading = 194;
ti.tracking = 264;
ti.justification = Justification.LEFT;
ti.position = Array(176, 458);

// "唤醒肌肤轻润呼吸感"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=82; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L19 = groupText.artLayers.add();
L19.name = "唤醒肌肤轻润呼吸感";
L19.kind = LayerKind.TEXT;
var ti = L19.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 608;
ti.height = 136;
ti.contents = '唤醒肌肤"轻润"呼吸感';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 87;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 756);

// "经典配方延续，针对夏日肤感特调——打破精华油黏腻的刻板印"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L20 = groupText.artLayers.add();
L20.name = "经典配方延续，针对夏日肤感特调——打破精华油黏腻的刻板印";
L20.kind = LayerKind.TEXT;
var ti = L20.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1164;
ti.height = 276;
ti.contents = '经典配方延续，针对夏日肤感特调——打破精华油黏腻的刻板印象，在轻薄感与滋润度之间找到更佳平衡。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 940);

// "轻薄感与滋润度的更佳平衡"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L21 = groupText.artLayers.add();
L21.name = "轻薄感与滋润度的更佳平衡";
L21.kind = LayerKind.TEXT;
var ti = L21.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 924;
ti.height = 174;
ti.contents = '轻薄感与滋润度的更佳平衡';
ti.font = resolvePSFont("Noto Serif SC", "400", true);
ti.size = 72;
ti.color = c;
ti.leading = 97;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(238, 1314);

// "— 夏日油养配方"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L22 = groupText.artLayers.add();
L22.name = "— 夏日油养配方";
L22.kind = LayerKind.TEXT;
var ti = L22.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 362;
ti.height = 94;
ti.contents = '— 夏日油养配方';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 54;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(238, 1450);

// "轻盈入夏"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L23 = groupText.artLayers.add();
L23.name = "轻盈入夏";
L23.kind = LayerKind.TEXT;
var ti = L23.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 198;
ti.height = 82;
ti.contents = '轻盈入夏';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "—"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L24 = groupText.artLayers.add();
L24.name = "—";
L24.kind = LayerKind.TEXT;
var ti = L24.textItem;
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
ti.position = Array(948, 2722);

// "肤感特调 · 经典延续"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L25 = groupText.artLayers.add();
L25.name = "肤感特调 · 经典延续";
L25.kind = LayerKind.TEXT;
var ti = L25.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 436;
ti.height = 82;
ti.contents = '肤感特调 · 经典延续';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1584, 2722);

var sf = new File(Folder.desktop + "/2026-07-02-小红书-岩玫瑰夏日油养_02.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

// ===== xhs-03 =====
var doc = app.documents.add(2160, 2880, 72, "2026-07-02-小红书-岩玫瑰夏日油养_03", NewDocumentMode.RGB);
app.preferences.rulerUnits = Units.PIXELS;

var groupBg = doc.layerSets.add();
groupBg.name = "背景与形状 (Backgrounds & Shapes)";
var groupText = doc.layerSets.add();
groupText.name = "排版文字 (Typography)";

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[0,0],[2160,0],[2160,2880],[0,2880]]);
createColorLayer("Rect Fill", 245, 241, 232, 100);
doc.selection.deselect();

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[176,498],[1056,498],[1056,1378],[176,1378]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[1104,498],[1984,498],[1984,1378],[1104,1378]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// "选油指南"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L29 = groupText.artLayers.add();
L29.name = "选油指南";
L29.kind = LayerKind.TEXT;
var ti = L29.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 216;
ti.height = 94;
ti.contents = '选油指南';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "系列对比"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L30 = groupText.artLayers.add();
L30.name = "系列对比";
L30.kind = LayerKind.TEXT;
var ti = L30.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 216;
ti.height = 94;
ti.contents = '系列对比';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(432, 192);

// "岩玫瑰精华油系列选油指南"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L31 = groupText.artLayers.add();
L31.name = "岩玫瑰精华油系列选油指南";
L31.kind = LayerKind.TEXT;
var ti = L31.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1437;
ti.height = 272;
ti.contents = '岩玫瑰精华油系列选油指南';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 112;
ti.color = c;
ti.leading = 132;
ti.tracking = 112;
ti.justification = Justification.LEFT;
ti.position = Array(176, 280);

// "清爽版"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L32 = groupText.artLayers.add();
L32.name = "清爽版";
L32.kind = LayerKind.TEXT;
var ti = L32.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 228;
ti.height = 150;
ti.contents = '清爽版';
ti.font = resolvePSFont("Playfair Display", "400", true);
ti.size = 64;
ti.color = c;
ti.leading = 90;
ti.tracking = 0;
ti.justification = Justification.CENTER;
ti.position = Array(520, 1430);

// "滋润版（经典款）"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L33 = groupText.artLayers.add();
L33.name = "滋润版（经典款）";
L33.kind = LayerKind.TEXT;
var ti = L33.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 548;
ti.height = 150;
ti.contents = '滋润版（经典款）';
ti.font = resolvePSFont("Playfair Display", "400", true);
ti.size = 64;
ti.color = c;
ti.leading = 90;
ti.tracking = 0;
ti.justification = Justification.CENTER;
ti.position = Array(1288, 1430);

// "质地"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=55; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L34 = groupText.artLayers.add();
L34.name = "质地";
L34.kind = LayerKind.TEXT;
var ti = L34.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 122;
ti.height = 82;
ti.contents = '质地';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 360;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1594);

// "质地"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=55; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L35 = groupText.artLayers.add();
L35.name = "质地";
L35.kind = LayerKind.TEXT;
var ti = L35.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 122;
ti.height = 82;
ti.contents = '质地';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 360;
ti.justification = Justification.LEFT;
ti.position = Array(1104, 1594);

// "哑光丝绒质地"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L36 = groupText.artLayers.add();
L36.name = "哑光丝绒质地";
L36.kind = LayerKind.TEXT;
var ti = L36.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 348;
ti.height = 118;
ti.contents = '哑光丝绒质地';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1644);

// "水光滋润质地"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L37 = groupText.artLayers.add();
L37.name = "水光滋润质地";
L37.kind = LayerKind.TEXT;
var ti = L37.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 348;
ti.height = 118;
ti.contents = '水光滋润质地';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(1104, 1644);

// "肤感"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=55; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L38 = groupText.artLayers.add();
L38.name = "肤感";
L38.kind = LayerKind.TEXT;
var ti = L38.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 122;
ti.height = 82;
ti.contents = '肤感';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 360;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1746);

// "肤感"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=55; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L39 = groupText.artLayers.add();
L39.name = "肤感";
L39.kind = LayerKind.TEXT;
var ti = L39.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 122;
ti.height = 82;
ti.contents = '肤感';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 360;
ti.justification = Justification.LEFT;
ti.position = Array(1104, 1746);

// "好吸收清爽不粘腻"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L40 = groupText.artLayers.add();
L40.name = "好吸收清爽不粘腻";
L40.kind = LayerKind.TEXT;
var ti = L40.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 444;
ti.height = 118;
ti.contents = '好吸收清爽不粘腻';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1796);

// "滋养盈润 润而不油"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L41 = groupText.artLayers.add();
L41.name = "滋养盈润 润而不油";
L41.kind = LayerKind.TEXT;
var ti = L41.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 456;
ti.height = 118;
ti.contents = '滋养盈润 润而不油';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(1104, 1796);

// "人群"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=55; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L42 = groupText.artLayers.add();
L42.name = "人群";
L42.kind = LayerKind.TEXT;
var ti = L42.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 122;
ti.height = 82;
ti.contents = '人群';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 360;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1896);

// "人群"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=55; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L43 = groupText.artLayers.add();
L43.name = "人群";
L43.kind = LayerKind.TEXT;
var ti = L43.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 122;
ti.height = 82;
ti.contents = '人群';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 360;
ti.justification = Justification.LEFT;
ti.position = Array(1104, 1896);

// "偏油性肌肤 / 夏秋季"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L44 = groupText.artLayers.add();
L44.name = "偏油性肌肤 / 夏秋季";
L44.kind = LayerKind.TEXT;
var ti = L44.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 486;
ti.height = 118;
ti.contents = '偏油性肌肤 / 夏秋季';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1946);

// "偏干性肌肤 / 冬春季"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L45 = groupText.artLayers.add();
L45.name = "偏干性肌肤 / 冬春季";
L45.kind = LayerKind.TEXT;
var ti = L45.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 486;
ti.height = 118;
ti.contents = '偏干性肌肤 / 冬春季';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(1104, 1946);

// "选对版本"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L46 = groupText.artLayers.add();
L46.name = "选对版本";
L46.kind = LayerKind.TEXT;
var ti = L46.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 198;
ti.height = 82;
ti.contents = '选对版本';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "—"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L47 = groupText.artLayers.add();
L47.name = "—";
L47.kind = LayerKind.TEXT;
var ti = L47.textItem;
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
ti.position = Array(948, 2722);

// "四季皆宜 · 按需选择"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L48 = groupText.artLayers.add();
L48.name = "四季皆宜 · 按需选择";
L48.kind = LayerKind.TEXT;
var ti = L48.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 436;
ti.height = 82;
ti.contents = '四季皆宜 · 按需选择';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1584, 2722);

var sf = new File(Folder.desktop + "/2026-07-02-小红书-岩玫瑰夏日油养_03.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

// ===== xhs-04 =====
var doc = app.documents.add(2160, 2880, 72, "2026-07-02-小红书-岩玫瑰夏日油养_04", NewDocumentMode.RGB);
app.preferences.rulerUnits = Units.PIXELS;

var groupBg = doc.layerSets.add();
groupBg.name = "背景与形状 (Backgrounds & Shapes)";
var groupText = doc.layerSets.add();
groupText.name = "排版文字 (Typography)";

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[0,0],[2160,0],[2160,2880],[0,2880]]);
createColorLayer("Rect Fill", 245, 241, 232, 100);
doc.selection.deselect();

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[447,656],[1713,656],[1713,1368],[447,1368]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[984,1882],[1176,1882],[1176,1886],[984,1886]]);
createColorLayer("Rect Fill", 46, 107, 79, 100);
doc.selection.deselect();

// "技术背书"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L52 = groupText.artLayers.add();
L52.name = "技术背书";
L52.kind = LayerKind.TEXT;
var ti = L52.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 216;
ti.height = 94;
ti.contents = '技术背书';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "专利科技"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L53 = groupText.artLayers.add();
L53.name = "专利科技";
L53.kind = LayerKind.TEXT;
var ti = L53.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 216;
ti.height = 94;
ti.contents = '专利科技';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(432, 192);

// "油溶纳米包裹技术"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L54 = groupText.artLayers.add();
L54.name = "油溶纳米包裹技术";
L54.kind = LayerKind.TEXT;
var ti = L54.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1101;
ti.height = 312;
ti.contents = '油溶纳米包裹技术';
ti.font = resolvePSFont("Noto Serif SC", "500", true);
ti.size = 128;
ti.color = c;
ti.leading = 164;
ti.tracking = 0;
ti.justification = Justification.CENTER;
ti.position = Array(568, 1452);

// "打破油养厚重黏腻偏见"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=82; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L55 = groupText.artLayers.add();
L55.name = "打破油养厚重黏腻偏见";
L55.kind = LayerKind.TEXT;
var ti = L55.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 620;
ti.height = 136;
ti.contents = '打破油养厚重黏腻偏见';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 87;
ti.tracking = 0;
ti.justification = Justification.CENTER;
ti.position = Array(800, 1678);

// "吸收率 +32.24%"
var c = new SolidColor(); c.rgb.red=46; c.rgb.green=107; c.rgb.blue=79; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L56 = groupText.artLayers.add();
L56.name = "吸收率 +32.24%";
L56.kind = LayerKind.TEXT;
var ti = L56.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 696;
ti.height = 224;
ti.contents = '吸收率 +32.24%';
ti.font = resolvePSFont("Playfair Display", "400", true);
ti.size = 96;
ti.color = c;
ti.leading = 134;
ti.tracking = 0;
ti.justification = Justification.CENTER;
ti.position = Array(752, 1964);

// "专利绿色小分子油发酵技术"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L57 = groupText.artLayers.add();
L57.name = "专利绿色小分子油发酵技术";
L57.kind = LayerKind.TEXT;
var ti = L57.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 636;
ti.height = 118;
ti.contents = '专利绿色小分子油发酵技术';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.CENTER;
ti.position = Array(792, 2196);

// "肌肤渗透吸收率显著提升"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L58 = groupText.artLayers.add();
L58.name = "肌肤渗透吸收率显著提升";
L58.kind = LayerKind.TEXT;
var ti = L58.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 588;
ti.height = 118;
ti.contents = '肌肤渗透吸收率显著提升';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.CENTER;
ti.position = Array(816, 2276);

// "专利技术"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L59 = groupText.artLayers.add();
L59.name = "专利技术";
L59.kind = LayerKind.TEXT;
var ti = L59.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 198;
ti.height = 82;
ti.contents = '专利技术';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "✦"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L60 = groupText.artLayers.add();
L60.name = "✦";
L60.kind = LayerKind.TEXT;
var ti = L60.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 70;
ti.height = 82;
ti.contents = '✦';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(982, 2722);

// "小分子油发酵技术"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L61 = groupText.artLayers.add();
L61.name = "小分子油发酵技术";
L61.kind = LayerKind.TEXT;
var ti = L61.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 358;
ti.height = 82;
ti.contents = '小分子油发酵技术';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1662, 2722);

var sf = new File(Folder.desktop + "/2026-07-02-小红书-岩玫瑰夏日油养_04.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

// ===== xhs-05 =====
var doc = app.documents.add(2160, 2880, 72, "2026-07-02-小红书-岩玫瑰夏日油养_05", NewDocumentMode.RGB);
app.preferences.rulerUnits = Units.PIXELS;

var groupBg = doc.layerSets.add();
groupBg.name = "背景与形状 (Backgrounds & Shapes)";
var groupText = doc.layerSets.add();
groupText.name = "排版文字 (Typography)";

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[0,0],[2160,0],[2160,2880],[0,2880]]);
createColorLayer("Rect Fill", 245, 241, 232, 100);
doc.selection.deselect();

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[176,1000],[1048,1000],[1048,2163],[176,2163]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// Rect Fill
app.activeDocument.activeLayer = groupBg;
doc.selection.select([[1112,1000],[1984,1000],[1984,2163],[1112,2163]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// "效果对比"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L65 = groupText.artLayers.add();
L65.name = "效果对比";
L65.kind = LayerKind.TEXT;
var ti = L65.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 216;
ti.height = 94;
ti.contents = '效果对比';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "真实体验"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L66 = groupText.artLayers.add();
L66.name = "真实体验";
L66.kind = LayerKind.TEXT;
var ti = L66.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 216;
ti.height = 94;
ti.contents = '真实体验';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(432, 192);

// "只见水光"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L67 = groupText.artLayers.add();
L67.name = "只见水光";
L67.kind = LayerKind.TEXT;
var ti = L67.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 832;
ti.height = 428;
ti.contents = '只见水光';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 176;
ti.color = c;
ti.leading = 194;
ti.tracking = 264;
ti.justification = Justification.LEFT;
ti.position = Array(176, 288);

// "不见油光"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L68 = groupText.artLayers.add();
L68.name = "不见油光";
L68.kind = LayerKind.TEXT;
var ti = L68.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 832;
ti.height = 428;
ti.contents = '不见油光';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 176;
ti.color = c;
ti.leading = 194;
ti.tracking = 264;
ti.justification = Justification.LEFT;
ti.position = Array(176, 482);

// "告别浮油难吸收"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=82; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L69 = groupText.artLayers.add();
L69.name = "告别浮油难吸收";
L69.kind = LayerKind.TEXT;
var ti = L69.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 452;
ti.height = 136;
ti.contents = '告别浮油难吸收';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 87;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 796);

// "Before"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L70 = groupText.artLayers.add();
L70.name = "Before";
L70.kind = LayerKind.TEXT;
var ti = L70.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 200;
ti.height = 94;
ti.contents = 'Before';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 160;
ti.justification = Justification.CENTER;
ti.position = Array(530, 2214);

// "After"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L71 = groupText.artLayers.add();
L71.name = "After";
L71.kind = LayerKind.TEXT;
var ti = L71.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 172;
ti.height = 94;
ti.contents = 'After';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 160;
ti.justification = Justification.CENTER;
ti.position = Array(1480, 2214);

// "真实体验"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L72 = groupText.artLayers.add();
L72.name = "真实体验";
L72.kind = LayerKind.TEXT;
var ti = L72.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 198;
ti.height = 82;
ti.contents = '真实体验';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "—"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L73 = groupText.artLayers.add();
L73.name = "—";
L73.kind = LayerKind.TEXT;
var ti = L73.textItem;
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
ti.position = Array(948, 2722);

// "清爽不粘腻 · 好吸收"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L74 = groupText.artLayers.add();
L74.name = "清爽不粘腻 · 好吸收";
L74.kind = LayerKind.TEXT;
var ti = L74.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 436;
ti.height = 82;
ti.contents = '清爽不粘腻 · 好吸收';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1584, 2722);

var sf = new File(Folder.desktop + "/2026-07-02-小红书-岩玫瑰夏日油养_05.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

alert("✅ PSD 已存入桌面！共 5 个文件。");