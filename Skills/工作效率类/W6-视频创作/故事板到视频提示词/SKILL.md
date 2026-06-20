# 故事板到视频提示词

用户需提供：图片目录路径、Lovart 项目名。缺信息就问用户，**只问一次**，不问第二遍。

## 步骤

**1. 检查项目**
```bash
cd skills/工作效率类/W7-API链接/lovart-skill && python lovart_project.py list
```
没有就创建：`python lovart_project.py init "项目名" --output /路径`

**2. 写管线 JSON**
读取图片目录下所有 `storyboard_*.png` → 按数字排序 → 每张图一个 step。

- `output_dir` = 图片目录路径
- `name` = 文件名不含后缀（如 `storyboard_1_v1`），有几个文件就写几个 step
- 同一编号有多个版本（v1/v2/v3）时，只取版本号最大的那个
- `thread` = `"new"`
- prompt 末尾固定加「只输出提示词正文，不要任何前缀说明、不要分析过程、不要多余文字。直接输出提示词。」

命名规则：管线 JSON 存为 `项目名_故事板到视频提示词.json`

模板：
```json
{
  "mode": "pipeline",
  "name": "项目名-故事板到视频提示词",
  "project_id": "项目UUID",
  "output_dir": "图片目录",
  "step_delay": 5,
  "steps": [
    {
      "name": "storyboard_1_v1",
      "type": "analyze",
      "image": "图片路径/storyboard_1_v1.png",
      "follow_ups": 0,
      "thread": "new",
      "prompt": "这是我的故事板分镜图，画面内容描述。根据这张图写视频提示词，包含场景氛围、角色状态、镜头运动、光影色调。只输出提示词正文，不要任何前缀说明、不要分析过程、不要多余文字。直接输出提示词。"
    }
  ]
}
```

**3. 运行**
```bash
cd skills/工作效率类/W7-API链接/lovart-skill && python lovart.py /绝对路径/管线.json --auto-sync
```

## 异常处理

| 问题 | 处理 |
|------|------|
| 项目不存在 | 先 init 创建项目获取 UUID |
| 图片路径不对 | 检查文件名和路径是否匹配 |
| 管线报错 | 把报错给用户看，等指示 |
