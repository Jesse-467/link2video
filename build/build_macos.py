#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS专用打包脚本
"""

import os
import sys
import subprocess
import shutil
import platform

def install_dependencies():
    """安装打包依赖"""
    print("正在安装打包依赖...")
    dependencies = [
        "pyinstaller",
        "pyinstaller[encryption]"
    ]
    
    for dep in dependencies:
        print(f"安装 {dep}...")
        subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
    
    print("依赖安装完成")

def create_macos_spec():
    """创建macOS专用spec文件"""
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
    
    with open('link2video_macos.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("macOS spec文件创建完成")

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    # 清理
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    # 构建
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "link2video_macos.spec",
        "--clean",
        "--noconfirm",
        "--onefile",
        "--console"
    ]
    
    subprocess.run(cmd, check=True)
    print("可执行文件构建完成")

def create_app_bundle():
    """创建macOS应用程序包"""
    print("创建macOS应用程序包...")
    
    app_name = "Link2Video.app"
    app_path = f"dist/{app_name}"
    
    # 创建应用程序包结构
    os.makedirs(f"{app_path}/Contents/MacOS", exist_ok=True)
    os.makedirs(f"{app_path}/Contents/Resources", exist_ok=True)
    
    # 复制可执行文件
    shutil.copy("dist/link2video", f"{app_path}/Contents/MacOS/")
    
    # 创建Info.plist
    info_plist = '''<?xml version="1.0" encoding="UTF-8"?>
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
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>'''
    
    with open(f"{app_path}/Contents/Info.plist", 'w') as f:
        f.write(info_plist)
    
    # 设置权限
    os.chmod(f"{app_path}/Contents/MacOS/link2video", 0o755)
    
    print(f"应用程序包创建完成: {app_path}")

def create_shell_scripts():
    """创建shell脚本"""
    
    # 运行脚本
    run_script = '''#!/bin/bash
# Link2Video 运行脚本

echo "========================================"
echo "    Link2Video - 视频下载工具"
echo "========================================"
echo ""
echo "支持的平台: 抖音、小红书、B站、YouTube等"
echo ""
echo "使用方法:"
echo "  ./link2video \"视频链接\" [选项]"
echo ""
echo "选项:"
echo "  -a    只下载音频"
echo "  -v    只下载视频"
echo "  -av   下载音视频"
echo "  -all  下载全部内容"
echo ""
echo "示例:"
echo "  ./link2video \"https://v.douyin.com/xxxxx/\" -v"
echo "  ./link2video \"https://www.bilibili.com/video/BV1xxx\" -av"
echo ""
echo "========================================"
echo ""

if [ $# -eq 0 ]; then
    echo "请输入视频链接作为参数"
    echo "例如: ./link2video \"https://v.douyin.com/xxxxx/\" -v"
    exit 1
fi

./link2video "$@"
'''
    
    with open('run_link2video.sh', 'w') as f:
        f.write(run_script)
    os.chmod('run_link2video.sh', 0o755)
    
    # 安装脚本
    install_script = '''#!/bin/bash
# Link2Video 安装脚本

echo "正在安装Link2Video..."

# 创建程序目录
sudo mkdir -p /usr/local/bin
sudo mkdir -p /Applications

# 复制可执行文件
sudo cp dist/link2video /usr/local/bin/
sudo chmod +x /usr/local/bin/link2video

# 复制应用程序包
sudo cp -r dist/Link2Video.app /Applications/

echo "安装完成！"
echo "命令行工具: /usr/local/bin/link2video"
echo "应用程序: /Applications/Link2Video.app"
echo ""
echo "现在可以在任何地方使用 link2video 命令了"
'''
    
    with open('install.sh', 'w') as f:
        f.write(install_script)
    os.chmod('install.sh', 0o755)
    
    print("Shell脚本创建完成")

def main():
    """主函数"""
    print("=" * 60)
    print("Link2Video macOS 打包工具")
    print("=" * 60)
    
    # 检查系统
    if platform.system() != "Darwin":
        print("错误: 此脚本只能在macOS上运行")
        sys.exit(1)
    
    try:
        # 1. 安装依赖
        install_dependencies()
        
        # 2. 创建spec文件
        create_macos_spec()
        
        # 3. 构建可执行文件
        build_executable()
        
        # 4. 创建应用程序包
        create_app_bundle()
        
        # 5. 创建shell脚本
        create_shell_scripts()
        
        print("\n" + "=" * 60)
        print("打包完成！")
        print("=" * 60)
        print("生成的文件:")
        print("  - dist/link2video (命令行工具)")
        print("  - dist/Link2Video.app (应用程序包)")
        print("  - run_link2video.sh (运行脚本)")
        print("  - install.sh (安装脚本)")
        print("\n使用方法:")
        print("  1. 运行 ./install.sh 安装到系统")
        print("  2. 或直接运行 ./run_link2video.sh")
        print("  3. 或直接运行 ./dist/link2video")
        print("  4. 或从Applications文件夹启动Link2Video.app")
        
    except Exception as e:
        print(f"打包失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
