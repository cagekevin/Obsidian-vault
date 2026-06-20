# PSD 输出模块 · 使用说明

## 用法

```bash
cd 详情页/xxx产品-详情页
node ../psd/html-to-psd.cjs .          # 合并长图（默认）
node ../psd/html-to-psd.cjs . --split  # 分屏模块
```

## 输出

| 模式 | 截图 | PSD |
|------|------|-----|
| 默认 | `产品名.png` 1 张 | 跑 JSX 得 1 个完整 PSD |
| `--split` | `产品名-M01.png` ~ `M09.png` 18 张 | 跑 JSX 得 9 个独立 PSD 到桌面 |

## 首次使用

```bash
npm install --no-save playwright && npx playwright install chromium
```

## 注意事项

- 容器用 `class="page"`（合并模式）或 `class="mod"` / `class="mod-auto"`（分屏模式）
- PSD 文字图层双击可编辑，形状图层双击可改色
- 分屏模式跑完自动关闭文件防 PS 卡死，合并模式保留打开状态
