# 🎬 视频链接智能下载工具

这是一个基于 `yt-dlp` 和 `Playwright` 的命令行工具，可自动识别并下载来自多个短视频平台（如 **抖音**、**小红书**、**哔哩哔哩**、**YouTube** 等）的原始无水印视频。

对于 **抖音** 和 **小红书**，采用专用解析逻辑，获取真实视频地址；其他平台统一使用 `yt-dlp` 实现高清音视频下载。

---

## ✨ 功能特点

- ✅ **自动识别平台类型**：输入分享链接即可判断平台类型（抖音、小红书、B站、YouTube 等）
- 📥 **灵活下载模式**：支持只下载音频、视频、音视频组合或全部文件
- 🧼 **抖音无水印解析**：专为抖音设计，获取真实地址，绕过水印限制
- 📱 **小红书视频下载**：专为小红书设计，绕过反爬机制，获取高清视频
- 🖥️ **命令行操作简洁直观**：支持多种参数，适合批处理和自动化脚本集成
- 🌐 **多平台支持扩展性强**：基于 yt-dlp，支持1000+平台
- 📁 **智能文件夹管理**：每个视频自动创建独立文件夹，结构清晰

---

## 🧰 使用方法

### 1️⃣ 安装依赖

确保 Python 3.7 及以上版本已安装。

安装依赖：

```bash
pip install -r requirements.txt
```

安装 Playwright 浏览器驱动（仅首次）：

```bash
playwright install
```

---

### 2️⃣ 命令行使用

#### **基本语法**
```bash
python main.py <视频分享链接> [下载模式]
```

#### **下载模式参数**
| 参数 | 功能 | 下载内容 |
|------|------|----------|
| `-a` | 只下载音频 | `.mp3` 文件 |
| `-v` | 只下载视频 | `.mp4` 文件 |
| `-av` | 下载音视频 | `.mp3` + `.mp4` 文件 |
| `-all` | 下载全部 | 音频 + 视频 + 封面 + 头像 + JSON |
| 无参数 | 默认模式 | 等同于 `-all` |

#### **使用示例**

**抖音视频：**
```bash
# 下载所有文件（默认）
python main.py "https://v.douyin.com/xxxxx/"

# 只下载音频
python main.py "https://v.douyin.com/xxxxx/" -a

# 只下载视频
python main.py "https://v.douyin.com/xxxxx/" -v

# 下载音视频
python main.py "https://v.douyin.com/xxxxx/" -av
```

**小红书视频：**
```bash
# 下载所有文件（默认）
python main.py "https://www.xiaohongshu.com/explore/xxxxx"

# 只下载视频
python main.py "https://www.xiaohongshu.com/explore/xxxxx" -v

# 下载音视频
python main.py "https://www.xiaohongshu.com/explore/xxxxx" -av
```

**其他平台：**
```bash
# B站视频
python main.py "https://www.bilibili.com/video/BV1xxx" -av

# YouTube视频
python main.py "https://youtube.com/watch?v=xxx" -v

# Twitter视频
python main.py "https://twitter.com/xxx/status/xxx" -a
```

---

## 📂 下载路径说明

所有下载内容将保存在：

```
./downloads/{平台名}/{视频标题}/
```

**文件夹结构示例：**
```
downloads/
├── douyin/
│   ├── 视频标题1/
│   │   ├── 时间戳_标题_video.mp4
│   │   ├── 时间戳_标题_music_音乐名.mp3
│   │   ├── 时间戳_标题_cover.jpeg
│   │   ├── 时间戳_标题_avatar.jpeg
│   │   └── 时间戳_标题_result.json
│   └── 视频标题2/
│       └── [文件...]
├── xiaohongshu/
│   ├── 视频标题-作者名/
│   │   ├── 视频标题.mp4
│   │   └── 视频标题_cover.jpg
│   └── 另一个视频-另一个作者/
│       └── [文件...]
├── bilibili/
│   └── 视频标题/
│       ├── 视频标题.mp4
│       └── 视频标题.m4a
└── youtube/
    └── 视频标题/
        ├── 视频标题.mp4
        └── 视频标题.webm
```

---

## 📌 当前支持平台

| 平台名称 | 处理方式 | 支持下载 | 特殊功能 |
|----------|----------|----------|----------|
| 抖音 | Playwright | ✅ 无水印 | 专用解析器，支持封面、头像、JSON |
| 小红书 | Playwright | ✅ 高清 | 专用解析器，绕过反爬机制 |
| 哔哩哔哩 | yt-dlp | ✅ | 高清音视频 |
| YouTube | yt-dlp | ✅ | 多格式支持 |
| Twitter/X | yt-dlp | ✅ | 短视频下载 |
| Instagram | yt-dlp | ✅ | 图片/视频 |
| TikTok | yt-dlp | ✅ | 短视频 |
| 其他平台 | yt-dlp | ✅ | 支持yt-dlp的所有平台 |

> 🔗 可参考 [yt-dlp 支持平台列表](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

---

## 🛠️ 技术栈

- **Python 3.7+**
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - 多平台视频下载
- **Playwright** - 抖音页面模拟解析
- **requests** - HTTP请求处理
- **rich** - 终端美化显示
- **tqdm** - 进度条显示

---

## 📁 项目结构

```
.
├── main.py                              # 主程序入口
├── process/
│   ├── __init__.py
│   ├── douyin.py                        # 抖音处理器
│   ├── douyin_downloader_playwright_v6.py  # 抖音专用解析器
│   ├── download.py                      # 通用下载器
│   ├── result.py                        # 数据转换器
│   └── utils.py                         # 工具函数
├── downloads/                           # 视频保存路径
├── requirements.txt                     # 依赖文件
├── run.sh                              # 启动脚本
├── .vscode/settings.json               # IDE配置
├── .python-version                     # Python版本
└── README.md                           # 项目说明文档
```

---

## 🚀 快速开始

1. **克隆项目**
```bash
git clone <repository-url>
cd link2video
```

2. **创建虚拟环境**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
playwright install
```

4. **开始使用**
```bash
python main.py "https://v.douyin.com/xxxxx/" -av
```

---

## 🔧 高级配置

### **IDE配置**
项目已包含VS Code/Cursor配置文件，自动使用虚拟环境：
- `.vscode/settings.json` - Python解释器配置
- `.python-version` - Python版本指定

### **Cookie支持**
抖音下载支持cookies.txt文件：
1. 将cookies.txt放在项目根目录
2. 程序会自动加载并使用cookies

### **代理设置**
yt-dlp支持代理设置，可在代码中添加：
```python
'proxy': 'http://proxy-server:port'
```

---

## 🤝 贡献

欢迎提交 PR 或 Issue：

- 添加新平台支持（如快手、小红书）
- 优化解析流程与错误处理
- 改进用户体验与交互提示
- 增加新的下载模式

---

## 📄 License

本项目采用 [MIT License](./LICENSE) 开源协议。

---

## ⚠️ 免责声明

本工具仅供学习与技术研究使用，请勿用于任何违反平台服务协议或侵犯他人权益的行为。

使用者需对自己的使用行为负责，因使用本工具下载、传播、修改他人内容所引发的一切法律纠纷及后果，均与作者无关。

如涉及版权问题，请联系原视频平台或相关内容创作者处理。

---

## 📞 支持

如果遇到问题或有建议，请：

1. 查看 [Issues](../../issues) 是否有类似问题
2. 创建新的 Issue 描述问题
3. 提供详细的错误信息和复现步骤

**享受下载的乐趣！** 🎉