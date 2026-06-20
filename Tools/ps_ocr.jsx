#target photoshop

function main() {
    if (app.documents.length === 0) return;
    
    var doc = app.activeDocument;
    var isWin = $.os.indexOf("Windows") !== -1;
    var pythonCmd = isWin ? "python" : "python3";
    
    var pyScriptPath = isWin
        ? "C:/Users/xinye/Nutstore/1/我的坚果云/skills-main/tools/ocr-image-to-text.py"
        : "/Users/kevin/Nutstore Files/我的坚果云/skills-main/tools/ocr-image-to-text.py";

    var tempDir = Folder(Folder.temp.fsName + "/ps_ocr_engine");
    if (!tempDir.exists) tempDir.create();

    var imagePath = tempDir.fsName + "/temp_poster.jpg";
    var jsonPath = tempDir.fsName + "/layout_data.json";

    if (File(imagePath).exists) File(imagePath).remove();
    if (File(jsonPath).exists) File(jsonPath).remove();

    var dupDoc = doc.duplicate("temp_export", true); 
    app.activeDocument = dupDoc;

    var jpgSaveOptions = new JPEGSaveOptions();
    jpgSaveOptions.quality = 8; 
    dupDoc.saveAs(new File(imagePath), jpgSaveOptions, true, Extension.LOWERCASE);
    dupDoc.close(SaveOptions.DONOTSAVECHANGES);
    app.activeDocument = doc;

    var logPath = tempDir.fsName + (isWin ? "\\ocr_log.txt" : "/ocr_log.txt");
    if (File(logPath).exists) File(logPath).remove();

    if (isWin) {
        // 💡 建立一个“任务完成”信号文件
        var flagPath = tempDir.fsName + "\\done.flag";
        var flagFile = new File(flagPath);
        if (flagFile.exists) flagFile.remove();

        var batFile = new File(tempDir.fsName + "\\run_ocr.bat");
        batFile.encoding = "UTF-8";
        batFile.open("w");
        batFile.writeln("@echo off");
        batFile.writeln("chcp 65001 >nul"); 
        
        var scriptFolder = pyScriptPath.substring(0, pyScriptPath.lastIndexOf("/")).replace(/\//g, "\\");
        batFile.writeln('cd /d "' + scriptFolder + '"');
        
        var wScript = pyScriptPath.replace(/\//g, "\\");
        var wImg = File(imagePath).fsName;
        var wJson = File(jsonPath).fsName;
        
        var cmdLine = pythonCmd + ' "' + wScript + '" "' + wImg + '" "' + wJson + '" > "' + logPath + '" 2>&1';
        batFile.writeln(cmdLine);
        // Python 跑完后，自动生成这个信号文件
        batFile.writeln('echo done > "' + flagPath + '"');
        batFile.close();
        
        var vbsFile = new File(tempDir.fsName + "\\run_ocr_silent.vbs");
        vbsFile.encoding = "UTF-8";
        vbsFile.open("w");
        vbsFile.writeln('Set WshShell = CreateObject("WScript.Shell")');
        vbsFile.writeln('WshShell.Run "cmd.exe /c ""' + batFile.fsName + '""", 0, True'); 
        vbsFile.close();
        
        // 🚀 终极杀招：不用 app.system，而是直接让系统静默“双击”运行这个 vbs
        vbsFile.execute();
        
        // ⏳ 让 PS 每隔 0.5 秒检查一次信号文件，最多等 30 秒
        var maxWait = 60; // 60 * 500ms = 30s
        var waitCount = 0;
        while (!flagFile.exists && waitCount < maxWait) {
            $.sleep(500);
            waitCount++;
        }
        
    } else {
        var shellCmd = pythonCmd + " \"" + pyScriptPath + "\" \"" + imagePath + "\" \"" + jsonPath + "\" > \"" + logPath + "\" 2>&1";
        app.system("osascript -e 'do shell script \"" + shellCmd + "\"'");
    }

    var jsonFile = File(jsonPath);
    if (!jsonFile.exists) {
        alert("❌ 解析失败，可能 Python 执行超时或崩溃。\n请检查:\n" + logPath);
        return;
    }

    jsonFile.encoding = "UTF8";
    jsonFile.open("r");
    var jsonStr = jsonFile.read();
    jsonFile.close();

    var originalRuler = app.preferences.rulerUnits;
    var originalType = app.preferences.typeUnits;
    app.preferences.rulerUnits = Units.PIXELS;
    app.preferences.typeUnits = TypeUnits.PIXELS;

    try {
        var data = eval("(" + jsonStr + ")");
        var blocks = [];
        if (data instanceof Array) blocks = data;
        else if (data && data.blocks instanceof Array) blocks = data.blocks;

        if (blocks.length === 0) {
            alert("⚠ JSON 生成成功但没抓到数据，请确认图层。");
            return;
        }

        var masterGroup = doc.layerSets.add();
        masterGroup.name = "✨ 智能重构布局";

        var screenHeight = 1500; 
        var screenGroups = {};
        var successCount = 0;
        
        var solidBlack = new SolidColor();
        solidBlack.rgb.red = 0;
        solidBlack.rgb.green = 0;
        solidBlack.rgb.blue = 0;

        var sizeMultiplier = 1.3; 
        var targetFont = "NotoSansSC-Regular"; 

        for (var i = 0; i < blocks.length; i++) {
            var b = blocks[i];
            
            try {
                var safeContent = String(b.content || "");
                if (safeContent.replace(/\s/g, "") === "") continue;

                var rawFontSize = parseFloat(b.inferred_font_size);
                if (isNaN(rawFontSize) || rawFontSize <= 0) rawFontSize = 14; 
                
                var finalFontSize = rawFontSize * sizeMultiplier;
                
                var leftPos = 0;
                var topPos = 0;
                if (b.rect) {
                    leftPos = parseFloat(b.rect.left) || 0;
                    topPos = parseFloat(b.rect.top) || 0;
                }

                var screenIndex = Math.floor(topPos / screenHeight) + 1;
                var sIdx = screenIndex.toString(); 
                
                if (!screenGroups[sIdx]) {
                    var sGroup = masterGroup.layerSets.add();
                    sGroup.name = "模块 " + screenIndex;
                    screenGroups[sIdx] = sGroup;
                }

                var textLayer = screenGroups[sIdx].artLayers.add();
                textLayer.kind = LayerKind.TEXT;
                
                var cleanName = safeContent.replace(/[\r\n]/g, " ").substring(0, 15);
                textLayer.name = cleanName; 

                var textItem = textLayer.textItem;
                textItem.contents = safeContent;
                textItem.color = solidBlack;

                try {
                    textItem.font = targetFont;
                } catch(fontErr) {}
                
                textItem.size = new UnitValue(finalFontSize, "px");
                textItem.position = [leftPos, topPos + rawFontSize];
                
                successCount++;
                
            } catch (innerErr) {
                // 如果单行报错不再弹窗干扰，静默跳过即可
            }
        }

        if (successCount > 0) {
            alert("🎉 全画幅解析完成！\n成功生成 " + successCount + " 个文本图层。");
        }

    } catch(e) {
        alert("❌ 整体结构出错：\n" + e.toString() + "\n行号：" + e.line);
    } finally {
        app.preferences.rulerUnits = originalRuler;
        app.preferences.typeUnits = originalType;
    }
}

app.activeDocument.suspendHistory("一键解析重构", "main()");