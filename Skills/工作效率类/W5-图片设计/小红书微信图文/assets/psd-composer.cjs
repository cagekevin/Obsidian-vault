#!/usr/bin/env node
/*
 * PSD Generator Pipeline (Smart Coordinates + Buffer Read)
 * Usage: node psd-composer.cjs <task-dir>
 */
const fs = require('fs');
const path = require('path');

const taskDir = path.resolve(process.argv[2] || '.');
(function findNM(dir) {
  var nm = path.join(dir, 'node_modules');
  if (fs.existsSync(nm)) module.paths.unshift(nm);
  var parent = path.dirname(dir);
  if (parent !== dir) findNM(parent);
})(taskDir);

const { writePsd } = require('ag-psd');
const { createCanvas, loadImage } = require('canvas');

require('ag-psd/initialize-canvas');

const outDir = path.join(taskDir, 'output');
const psdLayersDir = path.join(outDir, 'psd_layers');

if (!fs.existsSync(psdLayersDir)) {
  console.error(`❌ 未找到图层碎片目录: ${psdLayersDir}`);
  process.exit(1);
}

(async () => {
  const posterFolders = fs.readdirSync(psdLayersDir)
    .filter(f => fs.statSync(path.join(psdLayersDir, f)).isDirectory());

  if (posterFolders.length === 0) {
    console.log('⚠️ 没有发现需要打包的海报图层文件夹。');
    return;
  }

  for (const folder of posterFolders) {
    const folderPath = path.join(psdLayersDir, folder);
    const metaPath = path.join(folderPath, 'meta.json');
    
    if (!fs.existsSync(metaPath)) {
      console.log(`⚠️ 文件夹 ${folder} 缺少 meta.json，跳过。`);
      continue;
    }

    // 读取该海报的绝对尺寸和图层坐标配置
    const metaData = JSON.parse(fs.readFileSync(metaPath, 'utf8'));

    const psd = {
      width: metaData.width,
      height: metaData.height,
      children: []
    };

    console.log(`📦 正在打包精准 PSD: ${folder}.psd (共 ${metaData.layers.length} 个独立图层)...`);

    // 使用 Buffer 绕过 canvas 原生模块对中文路径的支持问题
    const loadBuf = (p) => loadImage(fs.readFileSync(p));

    // 按 JSON 中记录的顺序（包含 layer_00 基地层）依次合成
    for (const layerData of metaData.layers) {
      const imgPath = path.join(folderPath, layerData.file);
      
      if (!fs.existsSync(imgPath)) continue;

      const img = await loadBuf(imgPath);
      const canvas = createCanvas(img.width, img.height);
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);

      // 将精准裁切后的图层压入 PSD，依靠 left/top 完美对齐
      psd.children.push({
        name: layerData.file.replace('.png', ''),
        left: layerData.left || 0,
        top: layerData.top || 0,
        canvas: canvas,
      });
    }

    const buf = writePsd(psd);
    const outputPath = path.join(outDir, `${folder}.psd`);
    fs.writeFileSync(outputPath, Buffer.from(buf));
    console.log(`✅ 已生成: ${outputPath}`);
  }
  
  console.log('🎉 所有 PSD 打包完成！');
})();