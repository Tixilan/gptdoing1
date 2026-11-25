# Desktop Clock / 桌面时钟

一个轻量、离线、可自定义的 Windows 桌面悬浮时钟。A lightweight, offline, customizable floating clock for Windows.

![Desktop Clock preview](docs/preview.svg)

## 下载与使用 / Download

1. 从 [最新版本页面](https://github.com/Tixilan/gptdoing1/releases/latest) 下载 `DesktopClock-v1.0.0-windows-x64.exe`。
2. 双击运行，无需安装 Python。拖动窗口可以改变位置，右键窗口打开设置菜单。
3. 如需验证文件完整性，可同时下载 `.sha256` 文件并在 PowerShell 中运行：

   ```powershell
   Get-FileHash .\DesktopClock-v1.0.0-windows-x64.exe -Algorithm SHA256
   ```

Download the executable from the [latest release](https://github.com/Tixilan/gptdoing1/releases/latest), run it directly, drag to reposition, and right-click for settings. Python is not required.

> 首版 EXE 未进行商业代码签名，Windows SmartScreen 可能显示“Windows 已保护你的电脑”。请只从本仓库 Release 下载，并使用 SHA-256 文件核对完整性。The first release is unsigned, so Windows SmartScreen may show a warning. Only download it from this repository and verify its SHA-256 checksum.

## 功能 / Features

- 秒级数字时钟与完整日期 / Digital clock with seconds and full date
- 12/24 小时制 / 12/24-hour format
- 深色与浅色主题 / Dark and light themes
- 中文与 English 界面 / Chinese and English UI
- 可拖动、可置顶、自动记忆位置 / Draggable, always-on-top, persistent position
- 无网络请求、无遥测 / No network access or telemetry

设置保存在 `%APPDATA%\DesktopClock\settings.json`。删除该文件即可恢复默认设置；卸载只需退出程序、删除 EXE，并按需删除该设置目录。

Settings are stored in `%APPDATA%\DesktopClock\settings.json`. Delete the file to reset defaults. To uninstall, exit the clock, delete the executable, and optionally remove that settings directory.

## 从源码运行 / Run from source

需要 Python 3.12 或更高版本。Requires Python 3.12 or later.

```powershell
git clone https://github.com/Tixilan/gptdoing1.git
cd gptdoing1
python -m desktop_clock
```

运行测试 / Run tests:

```powershell
python -m unittest discover -s tests -v
```

构建 Windows EXE / Build the Windows executable:

```powershell
python -m pip install -r requirements-build.txt
python tools/generate_icon.py
pyinstaller --clean --noconfirm DesktopClock.spec
```

输出文件位于 `dist\DesktopClock.exe`。GitHub Actions 会在 `main` 分支更新时自动测试、打包并更新 v1.0.0 Release。

## 快捷操作 / Controls

- 左键拖动：移动窗口 / Left-drag: move the clock
- 右键：打开设置 / Right-click: open settings
- `Ctrl+Q`：退出 / Exit

## 系统要求 / Requirements

- Windows 10 或 Windows 11，x64
- 不需要管理员权限 / No administrator privileges required
- 不需要联网 / No internet connection required

## 许可 / License

本项目目前未附加开源许可证，默认保留全部权利。No open-source license is currently granted; all rights are reserved.

