# Link2Video 项目结构说明

## 📁 完整项目结构

```
link2video/
├── main.py                              # 主程序入口
├── requirements.txt                     # 依赖文件
├── run.sh                              # 启动脚本
├── README.md                           # 项目说明文档
├── README.en.md                        # 英文说明文档
├── XIAOHONGSHU_SUPPORT.md              # 小红书支持说明
├── PROJECT_STRUCTURE.md                # 项目结构说明（本文件）
├── .vscode/
│   └── settings.json                   # IDE配置
├── process/                            # 核心处理模块
│   ├── __init__.py
│   ├── douyin.py                       # 抖音处理器
│   ├── douyin_downloader_playwright_v6.py  # 抖音专用解析器
│   ├── download.py                     # 通用下载器
│   ├── result.py                       # 数据转换器
│   ├── utils.py                        # 工具函数
│   └── xiaohongshu_playwright.py       # 小红书专用解析器
├── build/                              # 打包相关文件
│   ├── README.md                       # 打包说明
│   ├── build.py                        # 通用打包脚本
│   ├── build_simple.py                 # 简化版打包脚本（推荐）
│   ├── build_standalone.py             # 完整版打包脚本
│   ├── build_windows.py                # Windows专用打包
│   ├── build_macos.py                  # macOS专用打包
│   ├── test_build.py                   # 打包环境测试
│   ├── BUILD_GUIDE.md                  # 打包指南（开发者用）
│   ├── PACKAGE_README.md               # 打包说明文档
│   └── 用户使用说明.md                  # 最终用户使用说明
└── downloads/                          # 视频保存路径
    ├── douyin/                         # 抖音视频
    ├── xiaohongshu/                    # 小红书视频
    ├── bilibili/                       # B站视频
    └── youtube/                        # YouTube视频
```

## 🎯 目录说明

### 核心文件
- **main.py**: 程序入口，处理命令行参数和平台识别
- **requirements.txt**: Python依赖包列表
- **run.sh**: 便捷启动脚本

### process/ 目录
包含所有核心处理逻辑：
- **douyin.py**: 抖音视频处理
- **xiaohongshu_playwright.py**: 小红书视频处理
- **download.py**: 通用下载器
- **result.py**: 数据结构定义
- **utils.py**: 工具函数

### build/ 目录
包含所有打包相关文件：
- **build_simple.py**: 简化版打包（推荐使用）
- **build_standalone.py**: 完整版打包
- **test_build.py**: 打包环境测试
- **用户使用说明.md**: 最终用户使用指南

### downloads/ 目录
自动创建的下载文件存储目录，按平台分类存储。

## 🚀 使用流程

### 开发者
1. **开发**: 修改 `process/` 目录中的代码
2. **测试**: 运行 `python main.py` 测试功能
3. **打包**: 进入 `build/` 目录运行打包脚本
4. **分发**: 将生成的exe文件分发给用户

### 最终用户
1. **获得**: 从开发者处获得 `link2video.exe` 文件
2. **运行**: 直接双击exe文件即可使用
3. **无需环境**: 不需要安装Python或任何依赖

## 📦 打包说明

### 推荐打包方式
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

### 打包结果
- **Windows**: `dist/link2video.exe` (约50-100MB)
- **macOS**: `dist/link2video` 或 `dist/Link2Video.app/`

## 🔧 技术特点

- ✅ **完全独立**: 打包后的exe文件无需任何环境
- ✅ **跨平台**: 支持Windows和macOS
- ✅ **用户友好**: 提供图形界面和命令行两种使用方式
- ✅ **功能完整**: 支持抖音、小红书、B站、YouTube等平台
- ✅ **结构清晰**: 代码和打包文件分离，便于维护

---

**总结**: 项目结构清晰，开发和使用分离，支持完全独立的可执行文件打包。
