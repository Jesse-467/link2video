#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows专用打包脚本
"""

import os
import sys
import subprocess
import shutil

def install_dependencies():
    """安装打包依赖"""
    print("正在安装打包依赖...")
    dependencies = [
        "pyinstaller",
        "pyinstaller[encryption]",
        "auto-py-to-exe"  # 图形化打包工具
    ]
    
    for dep in dependencies:
        print(f"安装 {dep}...")
        subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
    
    print("依赖安装完成")

def create_requirements_build():
    """创建打包专用requirements文件"""
    requirements = """# 打包专用依赖
pyinstaller>=5.0
playwright==1.52.0
yt_dlp==2025.5.22
tqdm==4.67.1
requests==2.32.3
rich==13.7.0
"""
    
    with open('requirements_build.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    print("打包依赖文件创建完成")

def create_simple_spec():
    """创建简化的spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('process', 'process'),
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
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

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
)
'''
    
    with open('link2video_simple.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("简化spec文件创建完成")

def build_exe():
    """构建exe文件"""
    print("开始构建exe文件...")
    
    # 清理
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    # 构建
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "link2video_simple.spec",
        "--clean",
        "--noconfirm",
        "--onefile",
        "--console"
    ]
    
    subprocess.run(cmd, check=True)
    print("exe文件构建完成")

def create_batch_files():
    """创建批处理文件"""
    
    # 运行脚本
    run_script = '''@echo off
title Link2Video - 视频下载工具
echo ========================================
echo    Link2Video - 视频下载工具
echo ========================================
echo.
echo 支持的平台: 抖音、小红书、B站、YouTube等
echo.
echo 使用方法:
echo   link2video.exe "视频链接" [选项]
echo.
echo 选项:
echo   -a    只下载音频
echo   -v    只下载视频  
echo   -av   下载音视频
echo   -all  下载全部内容
echo.
echo 示例:
echo   link2video.exe "https://v.douyin.com/xxxxx/" -v
echo   link2video.exe "https://www.bilibili.com/video/BV1xxx" -av
echo.
echo ========================================
echo.

if "%1"=="" (
    echo 请输入视频链接作为参数
    echo 例如: link2video.exe "https://v.douyin.com/xxxxx/" -v
    pause
    exit /b 1
)

link2video.exe %*
pause
'''
    
    with open('run_link2video.bat', 'w', encoding='utf-8') as f:
        f.write(run_script)
    
    # 安装脚本
    install_script = '''@echo off
echo 正在安装Link2Video...
echo.

REM 创建程序目录
if not exist "D:\\Link2Video" mkdir "D:\\Link2Video"

REM 复制文件
copy "dist\\link2video.exe" "D:\\Link2Video\\"
copy "run_link2video.bat" "D:\\Link2Video\\"

REM 添加到PATH
setx PATH "%PATH%;D:\\Link2Video" /M

echo 安装完成！
echo 程序位置: D:\\Link2Video\\link2video.exe
echo 桌面快捷方式: run_link2video.bat
echo.
echo 现在可以在任何地方使用 link2video 命令了
pause
'''
    
    with open('install.bat', 'w', encoding='utf-8') as f:
        f.write(install_script)
    
    print("批处理文件创建完成")

def main():
    """主函数"""
    print("=" * 60)
    print("Link2Video Windows 打包工具")
    print("=" * 60)
    
    try:
        # 1. 安装依赖
        install_dependencies()
        
        # 2. 创建requirements文件
        create_requirements_build()
        
        # 3. 创建spec文件
        create_simple_spec()
        
        # 4. 构建exe
        build_exe()
        
        # 5. 创建批处理文件
        create_batch_files()
        
        print("\n" + "=" * 60)
        print("打包完成！")
        print("=" * 60)
        print("生成的文件:")
        print("  - dist/link2video.exe (主程序)")
        print("  - run_link2video.bat (运行脚本)")
        print("  - install.bat (安装脚本)")
        print("\n使用方法:")
        print("  1. 运行 install.bat 安装到系统")
        print("  2. 或直接运行 run_link2video.bat")
        print("  3. 或直接运行 dist/link2video.exe")
        
    except Exception as e:
        print(f"打包失败: {e}")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
