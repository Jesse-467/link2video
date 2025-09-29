#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目打包脚本
支持Windows和macOS平台
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    print("PyInstaller安装完成")

def create_spec_file():
    """创建PyInstaller配置文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('process', 'process'),
        ('README.md', '.'),
        ('README.en.md', '.'),
        ('requirements.txt', '.'),
        ('run.sh', '.'),
    ],
    hiddenimports=[
        'playwright',
        'playwright.async_api',
        'yt_dlp',
        'tqdm',
        'requests',
        'rich',
        'process.douyin',
        'process.download',
        'process.result',
        'process.utils',
        'process.xiaohongshu_playwright',
        'process.douyin_downloader_playwright_v6',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='link2video',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('link2video.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("PyInstaller配置文件创建完成")

def install_playwright_browsers():
    """安装Playwright浏览器"""
    print("正在安装Playwright浏览器...")
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    print("Playwright浏览器安装完成")

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    # 清理之前的构建
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # 运行PyInstaller
    cmd = [sys.executable, "-m", "PyInstaller", "link2video.spec", "--clean"]
    subprocess.run(cmd, check=True)
    print("可执行文件构建完成")

def create_installer_script():
    """创建安装脚本"""
    system = platform.system().lower()
    
    if system == "windows":
        installer_content = '''@echo off
echo 正在安装Link2Video...
echo.

REM 创建程序目录
if not exist "C:\\Program Files\\Link2Video" mkdir "C:\\Program Files\\Link2Video"

REM 复制可执行文件
copy "dist\\link2video.exe" "C:\\Program Files\\Link2Video\\"

REM 创建桌面快捷方式
echo [InternetShortcut] > "%USERPROFILE%\\Desktop\\Link2Video.url"
echo URL=file:///C:/Program Files/Link2Video/link2video.exe >> "%USERPROFILE%\\Desktop\\Link2Video.url"
echo IconFile=C:\\Program Files\\Link2Video\\link2video.exe >> "%USERPROFILE%\\Desktop\\Link2Video.url"
echo IconIndex=0 >> "%USERPROFILE%\\Desktop\\Link2Video.url"

echo 安装完成！
echo 桌面快捷方式已创建
echo 程序位置: C:\\Program Files\\Link2Video\\link2video.exe
pause
'''
        with open('install.bat', 'w', encoding='utf-8') as f:
            f.write(installer_content)
    
    elif system == "darwin":  # macOS
        installer_content = '''#!/bin/bash
echo "正在安装Link2Video..."
echo

# 创建应用程序目录
sudo mkdir -p "/Applications/Link2Video.app/Contents/MacOS"
sudo mkdir -p "/Applications/Link2Video.app/Contents/Resources"

# 复制可执行文件
sudo cp "dist/link2video" "/Applications/Link2Video.app/Contents/MacOS/"

# 创建Info.plist
sudo cat > "/Applications/Link2Video.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>link2video</string>
    <key>CFBundleIdentifier</key>
    <string>com.link2video.app</string>
    <key>CFBundleName</key>
    <string>Link2Video</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
</dict>
</plist>
EOF

# 设置权限
sudo chmod +x "/Applications/Link2Video.app/Contents/MacOS/link2video"

echo "安装完成！"
echo "应用程序位置: /Applications/Link2Video.app"
echo "可以通过Launchpad或Applications文件夹启动"
'''
        with open('install.sh', 'w', encoding='utf-8') as f:
            f.write(installer_content)
        os.chmod('install.sh', 0o755)
    
    print(f"{system}安装脚本创建完成")

def create_readme():
    """创建使用说明"""
    readme_content = '''# Link2Video 可执行版本

## 使用方法

### Windows
1. 双击 `link2video.exe` 运行
2. 或在命令行中运行：
   ```
   link2video.exe "视频链接" -v
   ```

### macOS
1. 在终端中运行：
   ```
   ./link2video "视频链接" -v
   ```

## 支持的平台
- 抖音 (Douyin)
- 小红书 (Xiaohongshu)  
- 哔哩哔哩 (Bilibili)
- YouTube
- 其他yt-dlp支持的平台

## 下载模式
- `-a`: 只下载音频
- `-v`: 只下载视频
- `-av`: 下载音视频
- `-all`: 下载全部内容

## 示例
```
# 下载抖音视频
link2video.exe "https://v.douyin.com/xxxxx/" -v

# 下载小红书视频
link2video.exe "https://www.xiaohongshu.com/explore/xxxxx" -all

# 下载B站视频
link2video.exe "https://www.bilibili.com/video/BV1xxx" -av
```

## 注意事项
1. 首次运行可能需要较长时间来初始化
2. 确保网络连接正常
3. 某些平台可能需要登录才能下载高质量视频
'''
    
    with open('EXECUTABLE_README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("可执行版本说明文档创建完成")

def main():
    """主函数"""
    print("=" * 50)
    print("Link2Video 项目打包工具")
    print("=" * 50)
    
    system = platform.system()
    print(f"当前系统: {system}")
    
    try:
        # 1. 安装PyInstaller
        install_pyinstaller()
        
        # 2. 安装Playwright浏览器
        install_playwright_browsers()
        
        # 3. 创建配置文件
        create_spec_file()
        
        # 4. 构建可执行文件
        build_executable()
        
        # 5. 创建安装脚本
        create_installer_script()
        
        # 6. 创建说明文档
        create_readme()
        
        print("\n" + "=" * 50)
        print("打包完成！")
        print("=" * 50)
        print(f"可执行文件位置: dist/link2video{'exe' if system == 'Windows' else ''}")
        print("请查看 EXECUTABLE_README.md 了解使用方法")
        
    except Exception as e:
        print(f"打包过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
