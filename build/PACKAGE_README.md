# Link2Video 独立可执行文件打包说明

## 🎯 打包目标

将Link2Video项目打包成**完全独立**的可执行文件，让普通用户无需安装Python或任何依赖即可运行。

## ✅ 已完成的配置

### 1. 默认安装目录
- **Windows**: `D:\Link2Video\` (已从C盘改为D盘)
- **macOS**: `/Applications/Link2Video.app/`

### 2. 下载目录
- **Windows**: `D:\Link2Video\downloads\`
- **macOS**: `~/Downloads/link2video/`

### 3. 打包脚本
- `build_simple.py` - 简化版打包（推荐）
- `build_standalone.py` - 完整版打包
- `build_windows.py` - Windows专用
- `build_macos.py` - macOS专用

## 🚀 快速打包

> **注意**: 以下步骤仅适用于**开发者**（有Python环境的人）
> **最终用户**无需任何环境，直接使用打包好的exe文件即可

### 方法一：简化版打包（推荐）
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

# 5. 运行简化打包
python build_simple.py
```

### 方法二：完整版打包
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

# 5. 运行完整打包
python build_standalone.py
```

## 📦 打包结果

### Windows
```
dist/
├── link2video.exe          # 主程序 (约50-100MB)
├── 启动器.bat              # 图形界面启动器
└── 使用说明.txt            # 使用说明
```

### macOS
```
dist/
├── link2video              # 命令行工具
├── Link2Video.app/         # 应用程序包
├── run_link2video.sh       # 运行脚本
└── install.sh              # 安装脚本
```

## 🎯 最终用户使用（无需任何环境）

### Windows用户
1. **下载**: 获得 `link2video.exe` 文件
2. **运行**: 直接双击 `link2video.exe` 即可使用
3. **安装**: 运行 `install.bat` 安装到系统（可选）
4. **位置**: 程序安装在 `D:\Link2Video\`
5. **使用**: 双击桌面快捷方式或运行 `link2video.exe`

> **重要**: 普通用户无需安装Python、虚拟环境或任何依赖！

### macOS用户
1. **下载**: 获得 `link2video` 可执行文件或 `Link2Video.app`
2. **运行**: 直接运行可执行文件即可使用
3. **安装**: 运行 `./install.sh` 安装到系统（可选）
4. **位置**: 程序安装在 `/Applications/Link2Video.app/`
5. **使用**: 从Launchpad启动或运行命令行工具

> **重要**: 普通用户无需安装Python、虚拟环境或任何依赖！

## 🔧 技术特点

### 完全独立
- ✅ 单个exe文件，无需Python环境
- ✅ 包含所有依赖和浏览器
- ✅ 支持Windows和macOS
- ✅ 普通用户可直接运行

### 功能完整
- ✅ 支持抖音、小红书、B站、YouTube等平台
- ✅ 支持多种下载模式（-a, -v, -av, -all）
- ✅ 自动创建规范的文件夹结构
- ✅ 图形界面和命令行两种使用方式

### 用户友好
- ✅ 自动安装到系统
- ✅ 创建桌面和开始菜单快捷方式
- ✅ 添加到系统PATH
- ✅ 详细的使用说明和帮助

## 📋 打包前检查

运行测试脚本确保环境正常：
```bash
python test_build.py
```

## 🚨 注意事项

1. **文件大小**: exe文件约50-100MB（包含所有依赖）
2. **首次运行**: 可能需要较长时间初始化
3. **杀毒软件**: 可能被误报，这是正常现象
4. **网络要求**: 需要稳定的网络连接
5. **权限要求**: Windows可能需要管理员权限安装

## 🎉 分发建议

1. **压缩**: 使用7-Zip压缩减少传输大小
2. **测试**: 在干净的虚拟机中测试
3. **说明**: 提供详细的使用说明
4. **支持**: 准备常见问题解答

---

**总结**: 现在你可以将Link2Video打包成完全独立的可执行文件，普通用户无需任何环境即可使用！
