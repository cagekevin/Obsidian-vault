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
var doc = app.documents.add(2160, 2880, 72, "2026-07-13-胶囊精华种草_01", NewDocumentMode.RGB);
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
doc.selection.select([[176,1350],[1984,1350],[1984,2457],[176,2457]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// "Vol.01"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L3 = groupText.artLayers.add();
L3.name = "Vol.01";
L3.kind = LayerKind.TEXT;
var ti = L3.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 208;
ti.height = 94;
ti.contents = 'Vol.01';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "胶囊精华 · CAPSULE"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L4 = groupText.artLayers.add();
L4.name = "胶囊精华 · CAPSULE";
L4.kind = LayerKind.TEXT;
var ti = L4.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 504;
ti.height = 94;
ti.contents = '胶囊精华 · CAPSULE';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(424, 192);

// "封面 · 功效美学"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=55; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L5 = groupText.artLayers.add();
L5.name = "封面 · 功效美学";
L5.kind = LayerKind.TEXT;
var ti = L5.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 446;
ti.height = 98;
ti.contents = '封面 · 功效美学';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 42;
ti.color = c;
ti.leading = 59;
ti.tracking = 462;
ti.justification = Justification.LEFT;
ti.position = Array(176, 342);

// "一颗胶囊的"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L6 = groupText.artLayers.add();
L6.name = "一颗胶囊的";
L6.kind = LayerKind.TEXT;
var ti = L6.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1439;
ti.height = 604;
ti.contents = '一颗胶囊的';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 248;
ti.color = c;
ti.leading = 263;
ti.tracking = 496;
ti.justification = Justification.LEFT;
ti.position = Array(176, 434);

// "功效美学"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L7 = groupText.artLayers.add();
L7.name = "功效美学";
L7.kind = LayerKind.TEXT;
var ti = L7.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1181;
ti.height = 604;
ti.contents = '功效美学';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 248;
ti.color = c;
ti.leading = 263;
ti.tracking = 496;
ti.justification = Justification.LEFT;
ti.position = Array(176, 696);

// "是美学，也是功效"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L8 = groupText.artLayers.add();
L8.name = "是美学，也是功效";
L8.kind = LayerKind.TEXT;
var ti = L8.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 612;
ti.height = 168;
ti.contents = '是美学，也是功效';
ti.font = resolvePSFont("Playfair Display", "400", true);
ti.size = 72;
ti.color = c;
ti.leading = 101;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1108);

// "[产品图占位] 替换为胶囊精华主图"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L9 = groupText.artLayers.add();
L9.name = "[产品图占位] 替换为胶囊精华主图";
L9.kind = LayerKind.TEXT;
var ti = L9.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 722;
ti.height = 94;
ti.contents = '[产品图占位] 替换为胶囊精华主图';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 160;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2486);

// "把功效装进一颗胶囊，把美学写进每一次护肤的仪式感。"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=82; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L10 = groupText.artLayers.add();
L10.name = "把功效装进一颗胶囊，把美学写进每一次护肤的仪式感。";
L10.kind = LayerKind.TEXT;
var ti = L10.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1460;
ti.height = 136;
ti.contents = '把功效装进一颗胶囊，把美学写进每一次护肤的仪式感。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 87;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2556);

// "美学 AESTHETIC"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L11 = groupText.artLayers.add();
L11.name = "美学 AESTHETIC";
L11.kind = LayerKind.TEXT;
var ti = L11.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 376;
ti.height = 82;
ti.contents = '美学 AESTHETIC';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "—"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L12 = groupText.artLayers.add();
L12.name = "—";
L12.kind = LayerKind.TEXT;
var ti = L12.textItem;
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
ti.position = Array(1094, 2722);

// "Vol.01 / 05"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L13 = groupText.artLayers.add();
L13.name = "Vol.01 / 05";
L13.kind = LayerKind.TEXT;
var ti = L13.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 322;
ti.height = 82;
ti.contents = 'Vol.01 / 05';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1698, 2722);

var sf = new File(Folder.desktop + "/2026-07-13-胶囊精华种草_01.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

// ===== xhs-02 =====
var doc = app.documents.add(2160, 2880, 72, "2026-07-13-胶囊精华种草_02", NewDocumentMode.RGB);
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
doc.selection.select([[176,1313],[1984,1313],[1984,1579],[176,1579]]);
createColorLayer("Rect Fill", 232, 223, 207, 100);
doc.selection.deselect();

// "Vol.01"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L16 = groupText.artLayers.add();
L16.name = "Vol.01";
L16.kind = LayerKind.TEXT;
var ti = L16.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 208;
ti.height = 94;
ti.contents = 'Vol.01';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.CENTER;
ti.position = Array(176, 192);

// "幸运 BUFF"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L17 = groupText.artLayers.add();
L17.name = "幸运 BUFF";
L17.kind = LayerKind.TEXT;
var ti = L17.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 270;
ti.height = 94;
ti.contents = '幸运 BUFF';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.CENTER;
ti.position = Array(424, 192);

// "独家专利 · 四叶草设计"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=55; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L18 = groupText.artLayers.add();
L18.name = "独家专利 · 四叶草设计";
L18.kind = LayerKind.TEXT;
var ti = L18.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 600;
ti.height = 98;
ti.contents = '独家专利 · 四叶草设计';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 42;
ti.color = c;
ti.leading = 59;
ti.tracking = 462;
ti.justification = Justification.CENTER;
ti.position = Array(798, 342);

// "幸运buff"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L19 = groupText.artLayers.add();
L19.name = "幸运buff";
L19.kind = LayerKind.TEXT;
var ti = L19.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1223;
ti.height = 604;
ti.contents = '幸运buff';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 248;
ti.color = c;
ti.leading = 263;
ti.tracking = 496;
ti.justification = Justification.CENTER;
ti.position = Array(544, 458);

// "每一颗胶囊的剪开，"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L20 = groupText.artLayers.add();
L20.name = "每一颗胶囊的剪开，";
L20.kind = LayerKind.TEXT;
var ti = L20.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1229;
ti.height = 312;
ti.contents = '每一颗胶囊的剪开，';
ti.font = resolvePSFont("Noto Serif SC", "500", true);
ti.size = 128;
ti.color = c;
ti.leading = 164;
ti.tracking = 0;
ti.justification = Justification.CENTER;
ti.position = Array(504, 876);

// "都是幸运的开启。"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L21 = groupText.artLayers.add();
L21.name = "都是幸运的开启。";
L21.kind = LayerKind.TEXT;
var ti = L21.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1101;
ti.height = 312;
ti.contents = '都是幸运的开启。';
ti.font = resolvePSFont("Noto Serif SC", "500", true);
ti.size = 128;
ti.color = c;
ti.leading = 164;
ti.tracking = 0;
ti.justification = Justification.CENTER;
ti.position = Array(568, 1040);

// "独家专利四叶草设计，自带幸运 buff；每一次坚持护肤，"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L22 = groupText.artLayers.add();
L22.name = "独家专利四叶草设计，自带幸运 buff；每一次坚持护肤，";
L22.kind = LayerKind.TEXT;
var ti = L22.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1736;
ti.height = 272;
ti.contents = '独家专利四叶草设计，自带幸运 buff；每一次坚持护肤，都有美好收获。';
ti.font = resolvePSFont("Noto Serif SC", "400", true);
ti.size = 72;
ti.color = c;
ti.leading = 97;
ti.tracking = 0;
ti.justification = Justification.CENTER;
ti.position = Array(246, 1344);

// "幸运 LUCK"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L23 = groupText.artLayers.add();
L23.name = "幸运 LUCK";
L23.kind = LayerKind.TEXT;
var ti = L23.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 246;
ti.height = 82;
ti.contents = '幸运 LUCK';
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
ti.position = Array(1030, 2722);

// "Vol.02 / 05"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L25 = groupText.artLayers.add();
L25.name = "Vol.02 / 05";
L25.kind = LayerKind.TEXT;
var ti = L25.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 322;
ti.height = 82;
ti.contents = 'Vol.02 / 05';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1698, 2722);

var sf = new File(Folder.desktop + "/2026-07-13-胶囊精华种草_02.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

// ===== xhs-03 =====
var doc = app.documents.add(2160, 2880, 72, "2026-07-13-胶囊精华种草_03", NewDocumentMode.RGB);
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
doc.selection.select([[1271,318],[1984,318],[1984,1269],[1271,1269]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// "Vol.01"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L28 = groupText.artLayers.add();
L28.name = "Vol.01";
L28.kind = LayerKind.TEXT;
var ti = L28.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 208;
ti.height = 94;
ti.contents = 'Vol.01';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "绿色便携 · GREEN"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L29 = groupText.artLayers.add();
L29.name = "绿色便携 · GREEN";
L29.kind = LayerKind.TEXT;
var ti = L29.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 446;
ti.height = 94;
ti.contents = '绿色便携 · GREEN';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(424, 192);

// "植物胶囊 · 可持续"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=55; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L30 = groupText.artLayers.add();
L30.name = "植物胶囊 · 可持续";
L30.kind = LayerKind.TEXT;
var ti = L30.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 498;
ti.height = 98;
ti.contents = '植物胶囊 · 可持续';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 42;
ti.color = c;
ti.leading = 59;
ti.tracking = 462;
ti.justification = Justification.LEFT;
ti.position = Array(176, 318);

// "绿色"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L31 = groupText.artLayers.add();
L31.name = "绿色";
L31.kind = LayerKind.TEXT;
var ti = L31.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 468;
ti.height = 428;
ti.contents = '绿色';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 176;
ti.color = c;
ti.leading = 194;
ti.tracking = 264;
ti.justification = Justification.LEFT;
ti.position = Array(176, 452);

// "便携"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L32 = groupText.artLayers.add();
L32.name = "便携";
L32.kind = LayerKind.TEXT;
var ti = L32.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 468;
ti.height = 428;
ti.contents = '便携';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 176;
ti.color = c;
ti.leading = 194;
ti.tracking = 264;
ti.justification = Justification.LEFT;
ti.position = Array(176, 646);

// "便携安心，出差旅行随心携带。"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L33 = groupText.artLayers.add();
L33.name = "便携安心，出差旅行随心携带。";
L33.kind = LayerKind.TEXT;
var ti = L33.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 732;
ti.height = 118;
ti.contents = '便携安心，出差旅行随心携带。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 994);

// "植物胶囊 100% 可降解，"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L34 = groupText.artLayers.add();
L34.name = "植物胶囊 100% 可降解，";
L34.kind = LayerKind.TEXT;
var ti = L34.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 588;
ti.height = 118;
ti.contents = '植物胶囊 100% 可降解，';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1072);

// "为地球减负。"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L35 = groupText.artLayers.add();
L35.name = "为地球减负。";
L35.kind = LayerKind.TEXT;
var ti = L35.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 348;
ti.height = 118;
ti.contents = '为地球减负。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1152);

// "[占位] 便携场景"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L36 = groupText.artLayers.add();
L36.name = "[占位] 便携场景";
L36.kind = LayerKind.TEXT;
var ti = L36.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 376;
ti.height = 94;
ti.contents = '[占位] 便携场景';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 160;
ti.justification = Justification.LEFT;
ti.position = Array(1270, 1298);

// "绿色 GREEN"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L37 = groupText.artLayers.add();
L37.name = "绿色 GREEN";
L37.kind = LayerKind.TEXT;
var ti = L37.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 272;
ti.height = 82;
ti.contents = '绿色 GREEN';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "—"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L38 = groupText.artLayers.add();
L38.name = "—";
L38.kind = LayerKind.TEXT;
var ti = L38.textItem;
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
ti.position = Array(1042, 2722);

// "Vol.03 / 05"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L39 = groupText.artLayers.add();
L39.name = "Vol.03 / 05";
L39.kind = LayerKind.TEXT;
var ti = L39.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 322;
ti.height = 82;
ti.contents = 'Vol.03 / 05';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1698, 2722);

var sf = new File(Folder.desktop + "/2026-07-13-胶囊精华种草_03.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

// ===== xhs-04 =====
var doc = app.documents.add(2160, 2880, 72, "2026-07-13-胶囊精华种草_04", NewDocumentMode.RGB);
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
doc.selection.select([[176,772],[1984,772],[1984,2501],[176,2501]]);
createColorLayer("Rect Fill", 226, 232, 240, 100);
doc.selection.deselect();

// "Vol.01"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L42 = groupText.artLayers.add();
L42.name = "Vol.01";
L42.kind = LayerKind.TEXT;
var ti = L42.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 208;
ti.height = 94;
ti.contents = 'Vol.01';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "锁住鲜活 · FRESH"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L43 = groupText.artLayers.add();
L43.name = "锁住鲜活 · FRESH";
L43.kind = LayerKind.TEXT;
var ti = L43.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 446;
ti.height = 94;
ti.contents = '锁住鲜活 · FRESH';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(424, 192);

// "密封次抛 · 隔氧避光"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=55; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L44 = groupText.artLayers.add();
L44.name = "密封次抛 · 隔氧避光";
L44.kind = LayerKind.TEXT;
var ti = L44.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 550;
ti.height = 98;
ti.contents = '密封次抛 · 隔氧避光';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 42;
ti.color = c;
ti.leading = 59;
ti.tracking = 462;
ti.justification = Justification.LEFT;
ti.position = Array(176, 318);

// "锁住鲜活"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L45 = groupText.artLayers.add();
L45.name = "锁住鲜活";
L45.kind = LayerKind.TEXT;
var ti = L45.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 832;
ti.height = 428;
ti.contents = '锁住鲜活';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 176;
ti.color = c;
ti.leading = 194;
ti.tracking = 264;
ti.justification = Justification.LEFT;
ti.position = Array(176, 428);

// "[产品图占位] 密封次抛设计"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L46 = groupText.artLayers.add();
L46.name = "[产品图占位] 密封次抛设计";
L46.kind = LayerKind.TEXT;
var ti = L46.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 592;
ti.height = 94;
ti.contents = '[产品图占位] 密封次抛设计';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 160;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2528);

// "密封次抛设计，隔氧避光，将新鲜与功效焊死在每一滴精华里。"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=80; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L47 = groupText.artLayers.add();
L47.name = "密封次抛设计，隔氧避光，将新鲜与功效焊死在每一滴精华里。";
L47.kind = LayerKind.TEXT;
var ti = L47.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1404;
ti.height = 118;
ti.contents = '密封次抛设计，隔氧避光，将新鲜与功效焊死在每一滴精华里。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 48;
ti.color = c;
ti.leading = 79;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2576);

// "鲜活 FRESH"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L48 = groupText.artLayers.add();
L48.name = "鲜活 FRESH";
L48.kind = LayerKind.TEXT;
var ti = L48.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 272;
ti.height = 82;
ti.contents = '鲜活 FRESH';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "—"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L49 = groupText.artLayers.add();
L49.name = "—";
L49.kind = LayerKind.TEXT;
var ti = L49.textItem;
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
ti.position = Array(1042, 2722);

// "Vol.04 / 05"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L50 = groupText.artLayers.add();
L50.name = "Vol.04 / 05";
L50.kind = LayerKind.TEXT;
var ti = L50.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 322;
ti.height = 82;
ti.contents = 'Vol.04 / 05';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1698, 2722);

var sf = new File(Folder.desktop + "/2026-07-13-胶囊精华种草_04.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

// ===== xhs-05 =====
var doc = app.documents.add(2160, 2880, 72, "2026-07-13-胶囊精华种草_05", NewDocumentMode.RGB);
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

// "Vol.01"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L52 = groupText.artLayers.add();
L52.name = "Vol.01";
L52.kind = LayerKind.TEXT;
var ti = L52.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 208;
ti.height = 94;
ti.contents = 'Vol.01';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(176, 192);

// "精准控量 · DOSE"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L53 = groupText.artLayers.add();
L53.name = "精准控量 · DOSE";
L53.kind = LayerKind.TEXT;
var ti = L53.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 416;
ti.height = 94;
ti.contents = '精准控量 · DOSE';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 40;
ti.color = c;
ti.leading = 56;
ti.tracking = 240;
ti.justification = Justification.LEFT;
ti.position = Array(424, 192);

// "升级 350mg · 大容量"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=55; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L54 = groupText.artLayers.add();
L54.name = "升级 350mg · 大容量";
L54.kind = LayerKind.TEXT;
var ti = L54.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 602;
ti.height = 98;
ti.contents = '升级 350mg · 大容量';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 42;
ti.color = c;
ti.leading = 59;
ti.tracking = 462;
ti.justification = Justification.LEFT;
ti.position = Array(176, 342);

// "精准控量"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L55 = groupText.artLayers.add();
L55.name = "精准控量";
L55.kind = LayerKind.TEXT;
var ti = L55.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 832;
ti.height = 428;
ti.contents = '精准控量';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 176;
ti.color = c;
ti.leading = 194;
ti.tracking = 264;
ti.justification = Justification.LEFT;
ti.position = Array(176, 452);

// "升级 350mg 大容量，精准补足脸部与颈部滋养所需，减"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=82; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L56 = groupText.artLayers.add();
L56.name = "升级 350mg 大容量，精准补足脸部与颈部滋养所需，减";
L56.kind = LayerKind.TEXT;
var ti = L56.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 1668;
ti.height = 136;
ti.contents = '升级 350mg 大容量，精准补足脸部与颈部滋养所需，减少浪费。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 87;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(176, 822);

// "升级大容量"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L57 = groupText.artLayers.add();
L57.name = "升级大容量";
L57.kind = LayerKind.TEXT;
var ti = L57.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 488;
ti.height = 204;
ti.contents = '升级大容量';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 84;
ti.color = c;
ti.leading = 118;
ti.tracking = 84;
ti.justification = Justification.LEFT;
ti.position = Array(416, 1106);

// "01"
var c = new SolidColor(); c.rgb.red=46; c.rgb.green=107; c.rgb.blue=79; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L58 = groupText.artLayers.add();
L58.name = "01";
L58.kind = LayerKind.TEXT;
var ti = L58.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 112;
ti.height = 130;
ti.contents = '01';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 78;
ti.tracking = 224;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1144);

// "350mg 大容量，一瓶顶过往。"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=72; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L59 = groupText.artLayers.add();
L59.name = "350mg 大容量，一瓶顶过往。";
L59.kind = LayerKind.TEXT;
var ti = L59.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 652;
ti.height = 106;
ti.contents = '350mg 大容量，一瓶顶过往。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 44;
ti.color = c;
ti.leading = 68;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(1392, 1152);

// "脸颈同养"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L60 = groupText.artLayers.add();
L60.name = "脸颈同养";
L60.kind = LayerKind.TEXT;
var ti = L60.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 402;
ti.height = 204;
ti.contents = '脸颈同养';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 84;
ti.color = c;
ti.leading = 118;
ti.tracking = 84;
ti.justification = Justification.LEFT;
ti.position = Array(416, 1340);

// "02"
var c = new SolidColor(); c.rgb.red=46; c.rgb.green=107; c.rgb.blue=79; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L61 = groupText.artLayers.add();
L61.name = "02";
L61.kind = LayerKind.TEXT;
var ti = L61.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 112;
ti.height = 130;
ti.contents = '02';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 78;
ti.tracking = 224;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1378);

// "精准补足脸部与颈部滋养所需。"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=72; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L62 = groupText.artLayers.add();
L62.name = "精准补足脸部与颈部滋养所需。";
L62.kind = LayerKind.TEXT;
var ti = L62.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 676;
ti.height = 106;
ti.contents = '精准补足脸部与颈部滋养所需。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 44;
ti.color = c;
ti.leading = 68;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(1368, 1386);

// "次抛定量"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L63 = groupText.artLayers.add();
L63.name = "次抛定量";
L63.kind = LayerKind.TEXT;
var ti = L63.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 402;
ti.height = 204;
ti.contents = '次抛定量';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 84;
ti.color = c;
ti.leading = 118;
ti.tracking = 84;
ti.justification = Justification.LEFT;
ti.position = Array(416, 1574);

// "03"
var c = new SolidColor(); c.rgb.red=46; c.rgb.green=107; c.rgb.blue=79; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L64 = groupText.artLayers.add();
L64.name = "03";
L64.kind = LayerKind.TEXT;
var ti = L64.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 112;
ti.height = 130;
ti.contents = '03';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 78;
ti.tracking = 224;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1612);

// "每颗独立定量，一次一颗刚好。"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=72; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L65 = groupText.artLayers.add();
L65.name = "每颗独立定量，一次一颗刚好。";
L65.kind = LayerKind.TEXT;
var ti = L65.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 676;
ti.height = 106;
ti.contents = '每颗独立定量，一次一颗刚好。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 44;
ti.color = c;
ti.leading = 68;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(1368, 1620);

// "减少浪费"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L66 = groupText.artLayers.add();
L66.name = "减少浪费";
L66.kind = LayerKind.TEXT;
var ti = L66.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 402;
ti.height = 204;
ti.contents = '减少浪费';
ti.font = resolvePSFont("Noto Serif SC", "500", false);
ti.size = 84;
ti.color = c;
ti.leading = 118;
ti.tracking = 84;
ti.justification = Justification.LEFT;
ti.position = Array(416, 1808);

// "04"
var c = new SolidColor(); c.rgb.red=46; c.rgb.green=107; c.rgb.blue=79; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L67 = groupText.artLayers.add();
L67.name = "04";
L67.kind = LayerKind.TEXT;
var ti = L67.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 112;
ti.height = 130;
ti.contents = '04';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 56;
ti.color = c;
ti.leading = 78;
ti.tracking = 224;
ti.justification = Justification.LEFT;
ti.position = Array(176, 1846);

// "告别多余与浪费。"
var c = new SolidColor(); c.rgb.red=22; c.rgb.green=37; c.rgb.blue=27; c; var _oa=72; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L68 = groupText.artLayers.add();
L68.name = "告别多余与浪费。";
L68.kind = LayerKind.TEXT;
var ti = L68.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 412;
ti.height = 106;
ti.contents = '告别多余与浪费。';
ti.font = resolvePSFont("Noto Serif SC", "400", false);
ti.size = 44;
ti.color = c;
ti.leading = 68;
ti.tracking = 0;
ti.justification = Justification.LEFT;
ti.position = Array(1632, 1854);

// "精准 DOSE"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L69 = groupText.artLayers.add();
L69.name = "精准 DOSE";
L69.kind = LayerKind.TEXT;
var ti = L69.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 246;
ti.height = 82;
ti.contents = '精准 DOSE';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(176, 2722);

// "—"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L70 = groupText.artLayers.add();
L70.name = "—";
L70.kind = LayerKind.TEXT;
var ti = L70.textItem;
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
ti.position = Array(1030, 2722);

// "Vol.05 / 05"
var c = new SolidColor(); c.rgb.red=93; c.rgb.green=102; c.rgb.blue=93; c; var _oa=100; if(_oa<100) app.activeDocument.activeLayer.opacity=_oa;;
var L71 = groupText.artLayers.add();
L71.name = "Vol.05 / 05";
L71.kind = LayerKind.TEXT;
var ti = L71.textItem;
ti.kind = TextType.PARAGRAPHTEXT;
ti.width = 322;
ti.height = 82;
ti.contents = 'Vol.05 / 05';
ti.font = resolvePSFont("IBM Plex Mono", "400", false);
ti.size = 36;
ti.color = c;
ti.leading = 50;
ti.tracking = 216;
ti.justification = Justification.LEFT;
ti.position = Array(1698, 2722);

var sf = new File(Folder.desktop + "/2026-07-13-胶囊精华种草_05.psd");
doc.saveAs(sf);
doc.close(SaveOptions.DONOTSAVECHANGES);

alert("✅ PSD 已存入桌面！共 5 个文件。");