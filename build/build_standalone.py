#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立可执行文件打包脚本
生成完全独立的exe文件，无需Python环境
"""

import os
import sys
import subprocess
import shutil
import platform

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    print("PyInstaller安装完成")

def create_standalone_spec():
    """创建独立打包spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../process', 'process'),
    ],
    hiddenimports=[
        'playwright',
        'playwright.async_api',
        'playwright._impl',
        'playwright._impl._api_structures',
        'playwright._impl._browser_type',
        'playwright._impl._cdp_session',
        'playwright._impl._connection',
        'playwright._impl._driver',
        'playwright._impl._element_handle',
        'playwright._impl._frame',
        'playwright._impl._js_handle',
        'playwright._impl._network',
        'playwright._impl._page',
        'playwright._impl._path_utils',
        'playwright._impl._selectors',
        'playwright._impl._transport',
        'playwright._impl._wait_helper',
        'playwright._impl._web_socket',
        'yt_dlp',
        'yt_dlp.extractor',
        'yt_dlp.downloader',
        'yt_dlp.postprocessor',
        'tqdm',
        'requests',
        'rich',
        'rich.console',
        'rich.progress',
        'rich.text',
        'rich.panel',
        'rich.table',
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
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'tkinter',
        'test',
        'tests',
        'pytest',
        'unittest',
    ],
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
)
'''
    
    with open('link2video_standalone.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("独立打包spec文件创建完成")

def install_playwright_browsers():
    """安装Playwright浏览器到打包目录"""
    print("正在安装Playwright浏览器...")
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    print("Playwright浏览器安装完成")

def build_standalone_exe():
    """构建独立exe文件"""
    print("开始构建独立exe文件...")
    
    # 清理
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    # 构建
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "link2video_standalone.spec",
        "--clean",
        "--noconfirm",
        "--onefile",
        "--console",
        "--add-data", "process;process",
        "--hidden-import", "playwright",
        "--hidden-import", "yt_dlp",
        "--hidden-import", "tqdm",
        "--hidden-import", "requests",
        "--hidden-import", "rich"
    ]
    
    subprocess.run(cmd, check=True)
    print("独立exe文件构建完成")

def create_installer_script():
    """创建Windows安装脚本"""
    installer_content = '''@echo off
title Link2Video 安装程序
echo ========================================
echo    Link2Video 安装程序
echo ========================================
echo.
echo 正在安装Link2Video到您的系统...
echo.

REM 创建程序目录
if not exist "D:\\Link2Video" (
    echo 创建程序目录: D:\\Link2Video
    mkdir "D:\\Link2Video"
)

REM 复制可执行文件
echo 复制程序文件...
copy "link2video.exe" "D:\\Link2Video\\" >nul
if errorlevel 1 (
    echo 错误: 无法复制程序文件
    pause
    exit /b 1
)

REM 创建桌面快捷方式
echo 创建桌面快捷方式...
echo [InternetShortcut] > "%USERPROFILE%\\Desktop\\Link2Video.url"
echo URL=file:///D:/Link2Video/link2video.exe >> "%USERPROFILE%\\Desktop\\Link2Video.url"
echo IconFile=D:\\Link2Video\\link2video.exe >> "%USERPROFILE%\\Desktop\\Link2Video.url"
echo IconIndex=0 >> "%USERPROFILE%\\Desktop\\Link2Video.url"

REM 添加到PATH环境变量
echo 添加到系统PATH...
setx PATH "%PATH%;D:\\Link2Video" /M >nul 2>&1

REM 创建开始菜单快捷方式
echo 创建开始菜单快捷方式...
if not exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Link2Video" (
    mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Link2Video"
)
echo [InternetShortcut] > "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Link2Video\\Link2Video.url"
echo URL=file:///D:/Link2Video/link2video.exe >> "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Link2Video\\Link2Video.url"
echo IconFile=D:\\Link2Video\\link2video.exe >> "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Link2Video\\Link2Video.url"
echo IconIndex=0 >> "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Link2Video\\Link2Video.url"

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 程序位置: D:\\Link2Video\\link2video.exe
echo 桌面快捷方式: 已创建
echo 开始菜单: 已创建
echo 系统PATH: 已添加
echo.
echo 现在您可以在任何地方使用 link2video 命令了
echo 或者双击桌面快捷方式运行
echo.
echo 按任意键退出...
pause >nul
'''
    
    with open('install.bat', 'w', encoding='utf-8') as f:
        f.write(installer_content)
    print("Windows安装脚本创建完成")

def create_usage_guide():
    """创建使用指南"""
    guide_content = '''# Link2Video 使用指南

## 🚀 快速开始

### 方法一：命令行使用
1. 打开命令提示符（Win+R，输入cmd）
2. 输入以下命令：
   ```
   link2video "视频链接" -v
   ```

### 方法二：图形界面使用
1. 双击桌面上的"Link2Video"快捷方式
2. 按提示输入视频链接和选项

## 📱 支持的平台
- 抖音 (Douyin)
- 小红书 (Xiaohongshu)
- 哔哩哔哩 (Bilibili)
- YouTube
- 其他1000+平台

## ⚙️ 下载选项
- `-a`: 只下载音频
- `-v`: 只下载视频
- `-av`: 下载音视频
- `-all`: 下载全部内容（视频+音频+封面+信息）

## 💡 使用示例

### 下载抖音视频
```
link2video "https://v.douyin.com/xxxxx/" -v
```

### 下载小红书视频
```
link2video "https://www.xiaohongshu.com/explore/xxxxx" -all
```

### 下载B站视频
```
link2video "https://www.bilibili.com/video/BV1xxx" -av
```

### 下载YouTube视频
```
link2video "https://www.youtube.com/watch?v=xxxxx" -v
```

## 📁 下载位置
视频将下载到以下位置：
- Windows: `D:\\Link2Video\\downloads\\`
- 或当前目录的 `downloads` 文件夹

## ❓ 常见问题

### Q: 提示"不是内部或外部命令"
A: 请重新运行安装程序，或手动添加D:\\Link2Video到系统PATH

### Q: 下载失败
A: 请检查网络连接和视频链接是否正确

### Q: 某些视频无法下载
A: 部分平台需要登录或VIP权限才能下载高质量视频

### Q: 程序运行缓慢
A: 首次运行需要初始化，后续会更快

## 🔧 卸载程序
1. 删除文件夹：D:\\Link2Video
2. 删除桌面快捷方式
3. 从开始菜单删除快捷方式
4. 从系统PATH中移除D:\\Link2Video

## 📞 技术支持
如遇问题，请提供：
1. 错误信息截图
2. 视频链接
3. 操作系统版本
4. 使用的下载选项

---
Link2Video v1.0.0 - 让视频下载更简单
'''
    
    with open('使用指南.txt', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    print("使用指南创建完成")

def create_batch_launcher():
    """创建批处理启动器"""
    launcher_content = '''@echo off
title Link2Video - 视频下载工具
color 0A
echo.
echo  ██╗     ██╗███╗   ██╗██╗  ██╗    ██╗   ██╗██╗██████╗ ███████╗ ██████╗ 
echo  ██║     ██║████╗  ██║██║ ██╔╝    ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗
echo  ██║     ██║██╔██╗ ██║█████╔╝     ██║   ██║██║██║  ██║█████╗  ██║   ██║
echo  ██║     ██║██║╚██╗██║██╔═██╗     ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║
echo  ███████╗██║██║ ╚████║██║  ██║     ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝
echo  ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝      ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝ 
echo.
echo  ========================================
echo    支持平台: 抖音、小红书、B站、YouTube等
echo  ========================================
echo.

:menu
echo 请选择操作:
echo [1] 下载视频
echo [2] 下载音频
echo [3] 下载音视频
echo [4] 下载全部内容
echo [5] 查看帮助
echo [0] 退出
echo.
set /p choice=请输入选项 (0-5): 

if "%choice%"=="1" goto download_video
if "%choice%"=="2" goto download_audio
if "%choice%"=="3" goto download_av
if "%choice%"=="4" goto download_all
if "%choice%"=="5" goto help
if "%choice%"=="0" goto exit
goto menu

:download_video
echo.
set /p url=请输入视频链接: 
if "%url%"=="" (
    echo 错误: 请输入有效的视频链接
    pause
    goto menu
)
link2video.exe "%url%" -v
pause
goto menu

:download_audio
echo.
set /p url=请输入视频链接: 
if "%url%"=="" (
    echo 错误: 请输入有效的视频链接
    pause
    goto menu
)
link2video.exe "%url%" -a
pause
goto menu

:download_av
echo.
set /p url=请输入视频链接: 
if "%url%"=="" (
    echo 错误: 请输入有效的视频链接
    pause
    goto menu
)
link2video.exe "%url%" -av
pause
goto menu

:download_all
echo.
set /p url=请输入视频链接: 
if "%url%"=="" (
    echo 错误: 请输入有效的视频链接
    pause
    goto menu
)
link2video.exe "%url%" -all
pause
goto menu

:help
echo.
echo ========================================
echo 使用说明:
echo ========================================
echo.
echo 支持的平台:
echo - 抖音 (douyin.com)
echo - 小红书 (xiaohongshu.com)
echo - 哔哩哔哩 (bilibili.com)
echo - YouTube (youtube.com)
echo - 其他1000+平台
echo.
echo 下载选项:
echo -v    只下载视频
echo -a    只下载音频
echo -av   下载音视频
echo -all  下载全部内容
echo.
echo 示例:
echo link2video.exe "https://v.douyin.com/xxxxx/" -v
echo link2video.exe "https://www.bilibili.com/video/BV1xxx" -av
echo.
pause
goto menu

:exit
echo.
echo 感谢使用Link2Video！
echo.
pause
exit
'''
    
    with open('Link2Video.bat', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    print("批处理启动器创建完成")

def main():
    """主函数"""
    print("=" * 60)
    print("Link2Video 独立可执行文件打包工具")
    print("=" * 60)
    print("此工具将生成完全独立的exe文件")
    print("普通用户无需安装Python即可运行")
    print("=" * 60)
    
    try:
        # 1. 安装PyInstaller
        install_pyinstaller()
        
        # 2. 安装Playwright浏览器
        install_playwright_browsers()
        
        # 3. 创建spec文件
        create_standalone_spec()
        
        # 4. 构建exe
        build_standalone_exe()
        
        # 5. 创建安装脚本
        create_installer_script()
        
        # 6. 创建使用指南
        create_usage_guide()
        
        # 7. 创建批处理启动器
        create_batch_launcher()
        
        print("\n" + "=" * 60)
        print("打包完成！")
        print("=" * 60)
        print("生成的文件:")
        print("  - dist/link2video.exe (主程序，约50-100MB)")
        print("  - install.bat (安装脚本)")
        print("  - Link2Video.bat (图形界面启动器)")
        print("  - 使用指南.txt (使用说明)")
        print("\n分发说明:")
        print("  1. 将dist/link2video.exe复制到目标机器")
        print("  2. 运行install.bat进行安装")
        print("  3. 或直接运行Link2Video.bat使用图形界面")
        print("  4. 普通用户无需安装Python或任何依赖")
        
    except Exception as e:
        print(f"打包失败: {e}")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
