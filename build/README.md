# Build 目录说明

本目录包含所有与项目打包相关的文件和文档。

## 📁 目录结构

```
build/
├── README.md                    # 本说明文件
├── build.py                     # 通用打包脚本
├── build_simple.py             # 简化版打包脚本（推荐）
├── build_standalone.py         # 完整版打包脚本
├── build_windows.py            # Windows专用打包脚本
├── build_macos.py              # macOS专用打包脚本
├── test_build.py               # 打包环境测试脚本
├── BUILD_GUIDE.md              # 完整打包指南（开发者用）
├── PACKAGE_README.md           # 打包说明文档
└── 用户使用说明.md              # 最终用户使用说明
```

## 🚀 快速开始

### 开发者（打包）
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

# 5. 运行简化打包（推荐）
python build_simple.py
```

### 最终用户（使用exe）
- 查看 `用户使用说明.md` 了解如何使用打包好的exe文件
- 无需安装Python或任何依赖

## 📋 文件说明

### 打包脚本
- **build.py**: 通用打包脚本，支持多平台
- **build_simple.py**: 简化版打包，生成单个exe文件（推荐）
- **build_standalone.py**: 完整版打包，包含安装脚本和说明
- **build_windows.py**: Windows专用打包脚本
- **build_macos.py**: macOS专用打包脚本

### 测试和文档
- **test_build.py**: 测试打包环境是否正常
- **BUILD_GUIDE.md**: 详细的打包指南（开发者用）
- **PACKAGE_README.md**: 打包说明文档
- **用户使用说明.md**: 最终用户使用说明

## 🎯 使用流程

1. **开发阶段**: 使用 `test_build.py` 测试环境
2. **打包阶段**: 使用 `build_simple.py` 或 `build_standalone.py` 打包
3. **分发阶段**: 将生成的exe文件分发给用户
4. **用户使用**: 用户查看 `用户使用说明.md` 了解使用方法

## 📦 输出位置

打包完成后，生成的文件将位于：
- **Windows**: `../dist/link2video.exe`
- **macOS**: `../dist/link2video` 或 `../dist/Link2Video.app/`

## 🔧 注意事项

1. 打包前请确保在项目根目录的虚拟环境中
2. 首次打包可能需要较长时间下载依赖
3. 生成的exe文件约50-100MB
4. 普通用户无需任何环境即可运行exe文件
