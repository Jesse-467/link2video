#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版独立打包脚本
生成单个exe文件，无需任何依赖
"""

import os
import sys
import subprocess
import shutil

def main():
    print("=" * 50)
    print("Link2Video 简化打包工具")
    print("=" * 50)
    print("正在生成完全独立的exe文件...")
    print("普通用户无需Python环境即可运行")
    print("=" * 50)
    
    try:
        # 1. 安装PyInstaller
        print("1/6 安装PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        
        # 2. 安装Playwright浏览器
        print("2/6 安装Playwright浏览器...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        
        # 3. 清理旧文件
        print("3/6 清理旧文件...")
        for folder in ['build', 'dist', '__pycache__']:
            if os.path.exists(folder):
                shutil.rmtree(folder)
        
        # 4. 构建exe文件
        print("4/6 构建exe文件...")
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--console",
            "--name", "link2video",
            "--add-data", "../process;process",
            "--hidden-import", "playwright",
            "--hidden-import", "playwright.async_api",
            "--hidden-import", "yt_dlp",
            "--hidden-import", "tqdm",
            "--hidden-import", "requests",
            "--hidden-import", "rich",
            "--hidden-import", "process.douyin",
            "--hidden-import", "process.download",
            "--hidden-import", "process.result",
            "--hidden-import", "process.utils",
            "--hidden-import", "process.xiaohongshu_playwright",
            "--hidden-import", "process.douyin_downloader_playwright_v6",
            "--exclude-module", "matplotlib",
            "--exclude-module", "numpy",
            "--exclude-module", "pandas",
            "--exclude-module", "scipy",
            "--exclude-module", "tkinter",
            "../main.py"
        ]
        
        subprocess.run(cmd, check=True)
        
        # 5. 创建使用说明
        print("5/6 创建使用说明...")
        readme_content = '''# Link2Video 使用说明

## 快速开始
1. 双击 link2video.exe 运行
2. 按提示输入视频链接

## 支持的平台
- 抖音 (douyin.com)
- 小红书 (xiaohongshu.com)  
- 哔哩哔哩 (bilibili.com)
- YouTube (youtube.com)
- 其他1000+平台

## 使用方法
```
link2video.exe "视频链接" [选项]
```

## 选项
- -a    只下载音频
- -v    只下载视频
- -av   下载音视频
- -all  下载全部内容

## 示例
```
link2video.exe "https://v.douyin.com/xxxxx/" -v
link2video.exe "https://www.bilibili.com/video/BV1xxx" -av
```

## 注意事项
1. 首次运行可能需要较长时间初始化
2. 确保网络连接正常
3. 某些平台需要登录才能下载高质量视频

---
Link2Video v1.0.0
'''
        
        with open('dist/使用说明.txt', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # 6. 创建批处理启动器
        print("6/6 创建启动器...")
        launcher_content = '''@echo off
title Link2Video
echo ========================================
echo    Link2Video - 视频下载工具
echo ========================================
echo.
set /p url=请输入视频链接: 
if "%url%"=="" (
    echo 错误: 请输入有效的视频链接
    pause
    exit
)
echo.
echo 请选择下载模式:
echo [1] 只下载视频 (-v)
echo [2] 只下载音频 (-a)
echo [3] 下载音视频 (-av)
echo [4] 下载全部 (-all)
echo.
set /p mode=请选择 (1-4): 

if "%mode%"=="1" link2video.exe "%url%" -v
if "%mode%"=="2" link2video.exe "%url%" -a
if "%mode%"=="3" link2video.exe "%url%" -av
if "%mode%"=="4" link2video.exe "%url%" -all

pause
'''
        
        with open('dist/启动器.bat', 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        print("\n" + "=" * 50)
        print("打包完成！")
        print("=" * 50)
        print("生成的文件:")
        print("  - dist/link2video.exe (主程序)")
        print("  - dist/启动器.bat (图形界面)")
        print("  - dist/使用说明.txt (使用说明)")
        print("\n使用方法:")
        print("  1. 将dist文件夹复制到目标机器")
        print("  2. 双击 启动器.bat 使用图形界面")
        print("  3. 或直接运行 link2video.exe")
        print("  4. 普通用户无需安装任何依赖")
        
    except Exception as e:
        print(f"打包失败: {e}")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
