---
name: Git操作安全护栏
description: 设置 Claude Code 钩子以在危险 git 命令（push、reset --hard、clean、branch -D 等）执行前拦截它们。用户想防止破坏性 git 操作、添加 git 安全钩子、或在 Claude Code 中阻止 git push/reset 时使用。
---

# 设置 Git 安全护栏

设置一个 PreToolUse 钩子，在 Claude 执行危险 git 命令之前拦截并阻止它们。

## 被阻止的命令

- `git push`（所有变体包括 `--force`）
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

当被阻止时，Claude 会看到一条消息，告诉它没有权限访问这些命令。

## 步骤

### 1. 询问范围

询问用户：仅为**本项目**安装（`.claude/settings.json`）还是为**所有项目**安装（`~/.claude/settings.json`）？

### 2. 复制钩子脚本

捆绑脚本位于：[scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh)

根据范围将其复制到目标位置：

- **项目**：`.claude/hooks/block-dangerous-git.sh`
- **全局**：`~/.claude/hooks/block-dangerous-git.sh`

使用 `chmod +x` 使其可执行。

### 3. 将钩子添加到设置

添加到相应的设置文件：

**项目**（`.claude/settings.json`）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

**全局**（`~/.claude/settings.json`）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

如果设置文件已存在，将钩子合并到现有的 `hooks.PreToolUse` 数组中——不要覆盖其他设置。

### 4. 询问自定义

询问用户是否要从阻止列表中添加或删除任何模式。相应地编辑复制的脚本。

### 5. 验证

运行快速测试：

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
```

应退出码为 2 并向 stderr 打印 BLOCKED 消息。
