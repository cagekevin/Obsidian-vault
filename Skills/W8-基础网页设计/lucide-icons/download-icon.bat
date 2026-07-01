@echo off
REM Lucide 图标下载脚本 — 自动将 stroke-width 设为 1
REM 用法: download-icon <图标名> [输出目录]
REM 示例: download-icon heart
REM        download-icon heart C:\Users\xinye\Downloads

setlocal enabledelayedexpansion

set ICON_NAME=%1
set OUT_DIR=%2
if "%OUT_DIR%"=="" set OUT_DIR=%USERPROFILE%\Downloads

set SRC_DIR=g:\Obsidian-vault\node_modules\lucide-static\icons

if "%ICON_NAME%"=="" (
    echo 用法: download-icon ^<图标名^> [输出目录]
    echo 示例: download-icon heart
    exit /b 1
)

if not exist "%SRC_DIR%\%ICON_NAME%.svg" (
    echo 未找到图标: %ICON_NAME%
    echo 可用图标列表: dir "%SRC_DIR%"
    exit /b 1
)

REM 复制并修改 stroke-width
powershell -Command "(Get-Content '%SRC_DIR%\%ICON_NAME%.svg') -replace 'stroke-width=\"2\"', 'stroke-width=\"1\"' | Set-Content '%OUT_DIR%\%ICON_NAME%.svg'"

echo ✓ 已下载: %OUT_DIR%\%ICON_NAME%.svg ^(stroke-width: 1^)
