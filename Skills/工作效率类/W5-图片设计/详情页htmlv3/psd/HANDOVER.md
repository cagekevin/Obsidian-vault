# PSD 输出模块

## 用法

```bash
# 合并长图
node psd/html-to-psd.cjs <ProjectName> <ProjectRootDir>

# 全部分屏
node psd/html-to-psd.cjs <ProjectName> <ProjectRootDir> --split

# 指定第 N 屏
node psd/html-to-psd.cjs <ProjectName> <ProjectRootDir> --split --index=3
```

## 输出

| 模式 | 截图 | PSD |
|------|------|-----|
| 默认 | `项目名.png` 1 张 | 跑 JSX 得 1 个完整 PSD |
| `--split` | `项目名-screen_01.png` ~ 16 张 | 跑 JSX 得 8 个独立 PSD 到桌面 |

## 注意事项

- 依赖 `playwright`，统一装在 `skills-main/` 根目录
- 分屏模式：识别 `class="mod" id="screen-XX"`
- 合并模式：识别 `class="page-wrapper"`
- PSD 文字图层双击可编辑，形状图层双击可改色
