# Tools/instructions.md

## 这是我的工具箱

这里是我常用的实用脚本。不绑定到某个具体技能，独立存在。

## 文件结构

根目录放独立脚本（.py / .jsx），子文件夹放工具包：

```
Tools/
├── *.py              ← 独立脚本（压缩、OCR、下载等）
├── ps_*.jsx          ← Photoshop 脚本
├── MarkItDown文档转换/  ← Word/Excel/PDF 转 Markdown
├── tts/              ← 文字转语音
├── 网盘下载/           ← 网盘文件下载
├── aliyun/           ← 阿里云相关
└── instructions.md
```

## 触发方式

通过"兔子"、"tools"、"用 xxx 脚本"等关键词触发。

## AI 的角色

- Kevin 说"兔子"、"用 xx 工具"时，AI 来这里找对应的脚本
- 使用任何脚本前，先读该脚本头部注释获取用法
- Python 脚本执行：`python 脚本名.py`
- 依赖已在根目录 `requirements.txt` 中
