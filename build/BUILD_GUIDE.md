# Link2Video 打包指南

本指南将帮助你将Link2Video项目打包成**完全独立**的可执行程序，普通用户无需安装Python或任何依赖即可运行。

## 🎯 打包目标

- ✅ **完全独立**: 单个exe文件，无需Python环境
- ✅ **跨平台**: 支持Windows和macOS
- ✅ **用户友好**: 普通用户可直接运行
- ✅ **功能完整**: 包含所有依赖和浏览器

## 📋 前置要求

### 开发者环境（仅打包时需要）
- Python 3.7+ 
- 稳定的网络连接
- 足够的磁盘空间（至少2GB）

### 最终用户环境（运行exe时）
- **Windows**: 无需任何环境，直接运行exe
- **macOS**: 无需任何环境，直接运行可执行文件
- **无需Python**: 普通用户无需安装Python或任何依赖
- **无需虚拟环境**: 普通用户无需了解虚拟环境概念

## 🚀 快速开始

> **重要**: 以下步骤仅适用于**开发者**（有Python环境的人）
> **最终用户**无需任何环境，直接使用打包好的exe文件即可

### 方法一：一键打包（推荐）

#### 完全独立版本
```bash
# 1. 创建虚拟环境（如果还没有）
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 进入build目录
cd build

# 5. 运行独立打包脚本
python build_standalone.py
```

#### 简化版本
```bash
# 1. 创建虚拟环境（如果还没有）
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 进入build目录
cd build

# 5. 运行简化打包脚本
python build_simple.py
```

### 方法二：平台专用脚本

#### Windows
```bash
# 1. 激活虚拟环境
source venv/bin/activate  # 在Git Bash中
# 或
venv\Scripts\activate     # 在CMD中

# 2. 运行Windows打包脚本
python build_windows.py
```

#### macOS
```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 运行macOS打包脚本
python build_macos.py
```

### 方法二：手动打包

#### 1. 安装PyInstaller
```bash
pip install pyinstaller
pip install pyinstaller[encryption]  # 可选，用于加密
```

#### 2. 安装Playwright浏览器
```bash
playwright install chromium
```

#### 3. 创建spec文件
```bash
pyi-makespec main.py --name link2video --onefile --console
```

#### 4. 修改spec文件
在生成的`link2video.spec`文件中添加以下内容：

```python
# 在datas部分添加
datas=[
    ('process', 'process'),
],

# 在hiddenimports部分添加
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
```

#### 5. 构建可执行文件
```bash
pyinstaller link2video.spec --clean --noconfirm
```

## 📁 输出文件

### Windows
```
dist/
├── link2video.exe          # 主程序
├── run_link2video.bat      # 运行脚本
└── install.bat             # 安装脚本
```

### 安装位置
- **程序目录**: `D:\Link2Video\`
- **下载目录**: `D:\Link2Video\downloads\`

### macOS
```
dist/
├── link2video              # 命令行工具
├── Link2Video.app/         # 应用程序包
├── run_link2video.sh       # 运行脚本
└── install.sh              # 安装脚本
```

## 🔧 高级配置

### 减小文件大小

1. **排除不需要的模块**
```python
excludes=[
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'tkinter',
]
```

2. **使用UPX压缩**
```bash
pip install upx-ucl
# 在spec文件中设置 upx=True
```

3. **排除测试文件**
```python
excludes=[
    'test*',
    '*test*',
    'pytest',
    'unittest',
]
```

### 添加图标

1. **Windows (.ico文件)**
```python
exe = EXE(
    # ... 其他参数 ...
    icon='icon.ico',
)
```

2. **macOS (.icns文件)**
```python
exe = EXE(
    # ... 其他参数 ...
    icon='icon.icns',
)
```

### 创建安装程序

#### Windows (使用NSIS)
```bash
pip install pyinstaller[nsis]
pyinstaller --onefile --windowed --add-data "icon.ico;." main.py
```

#### macOS (使用DMG)
```bash
# 创建DMG文件
hdiutil create -volname "Link2Video" -srcfolder dist/ -ov -format UDZO Link2Video.dmg
```

## 🐛 常见问题

### 1. 文件过大
**问题**: 生成的exe文件过大（>100MB）
**解决**: 
- 使用`--exclude-module`排除不需要的模块
- 启用UPX压缩
- 使用`--onedir`而不是`--onefile`

### 2. 缺少依赖
**问题**: 运行时提示缺少模块
**解决**: 
- 在spec文件的`hiddenimports`中添加缺失的模块
- 使用`--collect-all`收集所有依赖

### 3. Playwright浏览器问题
**问题**: Playwright浏览器无法启动
**解决**: 
- 确保安装了Chromium: `playwright install chromium`
- 在打包时包含浏览器文件

### 4. 路径问题
**问题**: 资源文件找不到
**解决**: 
- 使用`os.path.dirname(sys.executable)`获取可执行文件目录
- 在spec文件中正确配置`datas`

## 📦 分发建议

### 1. 文件压缩
- 使用7-Zip或WinRAR压缩
- 添加密码保护（可选）

### 2. 数字签名
- Windows: 使用代码签名证书
- macOS: 使用Apple Developer证书

### 3. 病毒扫描
- 上传到VirusTotal检查
- 确保没有误报

### 4. 测试
- 在干净的虚拟机中测试
- 测试不同操作系统版本
- 测试不同权限级别

## 🔄 持续集成

### GitHub Actions示例
```yaml
name: Build Executables

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python build_windows.py
      - uses: actions/upload-artifact@v2
        with:
          name: windows-exe
          path: dist/

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python build_macos.py
      - uses: actions/upload-artifact@v2
        with:
          name: macos-app
          path: dist/
```

## 📝 许可证

请确保在分发时包含适当的许可证文件和免责声明。

## 🆘 获取帮助

如果遇到问题，请：
1. 查看本文档的常见问题部分
2. 检查PyInstaller官方文档
3. 在项目Issues中提问
4. 提供详细的错误信息和系统环境

## 👥 最终用户使用说明

### 对于普通用户（无需任何环境）

1. **获得程序**: 从开发者处获得 `link2video.exe` 文件
2. **直接运行**: 双击 `link2video.exe` 即可使用
3. **无需安装**: 程序可以直接运行，无需任何环境配置
4. **详细说明**: 请查看 `用户使用说明.md` 文件

### 关键特点
- ✅ **完全独立**: 单个exe文件，无需Python环境
- ✅ **无需安装**: 直接运行，无需配置
- ✅ **用户友好**: 提供图形界面和命令行两种使用方式
- ✅ **功能完整**: 支持抖音、小红书、B站、YouTube等平台

---

**注意**: 打包后的可执行文件可能被杀毒软件误报，这是正常现象。建议在分发前进行充分测试。
