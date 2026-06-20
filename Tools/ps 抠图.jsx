#target photoshop

function main() {
    if (app.documents.length === 0) {
        alert("请先打开一个文档！");
        return;
    }

    var doc = app.activeDocument;
    var layer = doc.activeLayer;

    if (layer.isBackgroundLayer) {
        alert("检测到锁定背景图层，请先双击解锁！");
        return;
    }

    var layerName = layer.name.toLowerCase();
    var extraArgs = "--model bria-rmbg"; 
    var modeTip = "🚀 BRIA 电商顶流模式";

    if (layerName.indexOf("人") !== -1 || layerName.indexOf("模特") !== -1) {
        extraArgs = "--model u2net_human_seg --matting";
        modeTip = "👤 人像发丝模式";
    } 

    var isWin = $.os.indexOf("Windows") !== -1;
    var pythonCmd = isWin ? "python" : "python3";
    var pyScriptPath = isWin
        ? "C:/Users/xinye/Nutstore/1/我的坚果云/skills-main/tools/remove-bg.py"
        : "/Users/kevin/Nutstore Files/我的坚果云/skills-main/tools/remove-bg.py";

    var tempDir = Folder(Folder.temp.fsName + "/ps_ai_matting");
    if (!tempDir.exists) tempDir.create();

    var inputPath = tempDir.fsName + "/input.png";
    var outputPath = tempDir.fsName + "/output.png";
    var logPath = tempDir.fsName + "/matting_log.txt";
    var flagPath = tempDir.fsName + "/done.flag";
    var flagFile = new File(flagPath);

    if (File(outputPath).exists) File(outputPath).remove();
    if (File(logPath).exists) File(logPath).remove();
    if (flagFile.exists) flagFile.remove();

    var dupDoc = app.documents.add(doc.width, doc.height, doc.resolution, "temp_export", NewDocumentMode.RGB, DocumentFill.TRANSPARENT);
    app.activeDocument = doc;
    layer.duplicate(dupDoc, ElementPlacement.PLACEATBEGINNING);
    app.activeDocument = dupDoc;
    dupDoc.layers[dupDoc.layers.length-1].remove();
    
    var file = new File(inputPath);
    var options = new PNGSaveOptions();
    dupDoc.saveAs(file, options, true, Extension.LOWERCASE);
    dupDoc.close(SaveOptions.DONOTSAVECHANGES);
    app.activeDocument = doc;

    if (isWin) {
        var batFile = new File(tempDir.fsName + "\\run_matting.bat");
        batFile.encoding = "UTF-8";
        batFile.open("w");
        batFile.writeln("@echo off");
        batFile.writeln("chcp 65001 >nul"); 
        
        var scriptFolder = pyScriptPath.substring(0, pyScriptPath.lastIndexOf("/")).replace(/\//g, "\\");
        batFile.writeln('cd /d "' + scriptFolder + '"');
        
        var wScript = pyScriptPath.replace(/\//g, "\\");
        var wImg = File(inputPath).fsName;
        var wOut = File(outputPath).fsName;
        var wLog = File(logPath).fsName;
        var wFlag = flagFile.fsName;
        
        var cmdLine = pythonCmd + ' "' + wScript + '" "' + wImg + '" -o "' + wOut + '" ' + extraArgs + ' --quiet > "' + wLog + '" 2>&1';
        batFile.writeln(cmdLine);
        batFile.writeln('echo done > "' + wFlag + '"');
        batFile.close();
        
        var vbsFile = new File(tempDir.fsName + "\\run_matting_silent.vbs");
        vbsFile.encoding = "UTF-8";
        vbsFile.open("w");
        vbsFile.writeln('Set WshShell = CreateObject("WScript.Shell")');
        vbsFile.writeln('WshShell.Run "cmd.exe /c ""' + batFile.fsName + '""", 0, True'); 
        vbsFile.close();
        
        vbsFile.execute();
        
        // 💡 修复：将超时时间从 60 秒延长到 300 秒（5分钟），给足下载大模型的时间！
        var maxWait = 600; 
        var waitCount = 0;
        while (!flagFile.exists && waitCount < maxWait) {
            $.sleep(500);
            waitCount++;
            var checkLog = File(logPath);
            if (checkLog.exists && checkLog.length > 0 && waitCount % 4 === 0) {
                checkLog.open("r");
                var logContent = checkLog.read().toLowerCase();
                checkLog.close();
                // 只有明确出现 error 或 exception 时才提前打断
                if (logContent.indexOf("error") !== -1 || logContent.indexOf("exception") !== -1) break; 
            }
        }
    } else {
        var shellCmd = pythonCmd + " \"" + pyScriptPath + "\" \"" + inputPath + "\" -o \"" + outputPath + "\" " + extraArgs + " --quiet > \"" + logPath + "\" 2>&1; touch \"" + flagPath + "\"";
        app.system("osascript -e 'do shell script \"" + shellCmd + "\"'");
        
        var maxWaitMac = 600;
        var waitCountMac = 0;
        while (!flagFile.exists && waitCountMac < maxWaitMac) {
            $.sleep(500);
            waitCountMac++;
        }
    }

    $.sleep(500);

    var outFile = File(outputPath);
    if (!outFile.exists) {
        // 💡 修复：恢复详细报错日志抓取
        var errorMsg = "❌ 抠图失败或等待超时！\n";
        var logFile = new File(logPath);
        if (logFile.exists && logFile.length > 0) {
            logFile.encoding = "UTF-8";
            logFile.open("r");
            errorMsg += "\n【后台日志与报错】:\n" + logFile.read().substring(0, 1000);
            logFile.close();
        } else {
            errorMsg += "\n没有找到报错日志。可能是大模型正在后台龟速下载中，PS 等了5分钟没等及。请不要关机，稍后重试！";
        }
        alert(errorMsg);
        return;
    }

    try {
        var maskDoc = app.open(outFile);
        maskDoc.selection.selectAll();
        maskDoc.selection.copy();
        maskDoc.close(SaveOptions.DONOTSAVECHANGES);
        
        app.activeDocument = doc;
        doc.activeLayer = layer;
        
        var idMk = charIDToTypeID( "Mk  " );
        var desc = new ActionDescriptor();
        var idNw = charIDToTypeID( "Nw  " );
        var idChnl = charIDToTypeID( "Chnl" );
        desc.putClass( idNw, idChnl );
        var idAt = charIDToTypeID( "At  " );
        var ref = new ActionReference();
        ref.putEnumerated( charIDToTypeID( "Chnl" ), charIDToTypeID( "Chnl" ), charIDToTypeID( "Msk " ) );
        desc.putReference( idAt, ref );
        var idUsng = charIDToTypeID( "Usng" );
        var idUsrM = charIDToTypeID( "UsrM" );
        var idRvlA = charIDToTypeID( "RvlA" );
        desc.putEnumerated( idUsng, idUsrM, idRvlA );
        executeAction( idMk, desc, DialogModes.NO );

        var descSel = new ActionDescriptor();
        var refSel = new ActionReference();
        refSel.putEnumerated( charIDToTypeID("Chnl"), charIDToTypeID("Chnl"), charIDToTypeID("Msk ") );
        descSel.putReference( charIDToTypeID("null"), refSel );
        descSel.putBoolean( charIDToTypeID("MkVs"), true );
        executeAction( charIDToTypeID("slct"), descSel, DialogModes.NO );

        doc.paste();

        var descRGB = new ActionDescriptor();
        var refRGB = new ActionReference();
        refRGB.putEnumerated( charIDToTypeID("Chnl"), charIDToTypeID("Chnl"), charIDToTypeID("RGB ") );
        descRGB.putReference( charIDToTypeID("null"), refRGB );
        executeAction( charIDToTypeID("slct"), descRGB, DialogModes.NO );
        
        layer.name = layer.name + " [" + modeTip + "]";
        doc.selection.deselect();
        
    } catch (e) {
        alert("导入蒙版时出错：\n" + e.toString());
    }
}

app.activeDocument.suspendHistory("一键神级 AI 抠图", "main()");