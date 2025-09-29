# 🎬 Smart Video Link Downloader

A command-line tool based on `yt-dlp` and `Playwright` that automatically identifies and downloads original watermark-free videos from multiple short video platforms (such as **Douyin**, **Xiaohongshu**, **Bilibili**, **YouTube**, etc.).

For **Douyin** and **Xiaohongshu**, it uses dedicated parsing logic to obtain real video addresses; other platforms use `yt-dlp` for high-quality audio and video downloads.

---

## ✨ Features

- ✅ **Automatic Platform Detection**: Input a share link to identify platform type (Douyin, Bilibili, YouTube, etc.)
- 📥 **Flexible Download Modes**: Support audio-only, video-only, audio+video, or all files
- 🧼 **Douyin Watermark-Free Parsing**: Specially designed for Douyin, gets real addresses, bypasses watermark restrictions
- 🖥️ **Simple Command-Line Interface**: Supports multiple parameters, suitable for batch processing and automation scripts
- 🌐 **Extensive Platform Support**: Based on yt-dlp, supports 1000+ platforms
- 📁 **Smart Folder Management**: Each video automatically creates an independent folder with clear structure

---

## 🧰 Usage

### 1️⃣ Install Dependencies

Ensure Python 3.7+ is installed.

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browser drivers (first time only):

```bash
playwright install
```

---

### 2️⃣ Command Line Usage

#### **Basic Syntax**
```bash
python main.py <video_share_link> [download_mode]
```

#### **Download Mode Parameters**
| Parameter | Function | Downloads |
|-----------|----------|-----------|
| `-a` | Audio only | `.mp3` files |
| `-v` | Video only | `.mp4` files |
| `-av` | Audio + Video | `.mp3` + `.mp4` files |
| `-all` | All files | Audio + Video + Cover + Avatar + JSON |
| No parameter | Default mode | Same as `-all` |

#### **Usage Examples**

**Douyin Videos:**
```bash
# Download all files (default)
python main.py "https://v.douyin.com/xxxxx/"

# Audio only
python main.py "https://v.douyin.com/xxxxx/" -a

# Video only
python main.py "https://v.douyin.com/xxxxx/" -v

# Audio + Video
python main.py "https://v.douyin.com/xxxxx/" -av
```

**Other Platforms:**
```bash
# Bilibili video
python main.py "https://www.bilibili.com/video/BV1xxx" -av

# YouTube video
python main.py "https://youtube.com/watch?v=xxx" -v

# Twitter video
python main.py "https://twitter.com/xxx/status/xxx" -a
```

---

## 📂 Download Path Structure

All downloaded content will be saved in:

```
./downloads/{platform_name}/{video_title}/
```

**Folder Structure Example:**
```
downloads/
├── douyin/
│   ├── video_title1/
│   │   ├── timestamp_title_video.mp4
│   │   ├── timestamp_title_music_songname.mp3
│   │   ├── timestamp_title_cover.jpeg
│   │   ├── timestamp_title_avatar.jpeg
│   │   └── timestamp_title_result.json
│   └── video_title2/
│       └── [files...]
├── xiaohongshu/
│   ├── video_title-author_name/
│   │   ├── video_title.mp4
│   │   └── video_title_cover.jpg
│   └── another_video-another_author/
│       └── [files...]
├── bilibili/
│   └── video_title/
│       ├── video_title.mp4
│       └── video_title.m4a
└── youtube/
    └── video_title/
        ├── video_title.mp4
        └── video_title.webm
```

---

## 📌 Supported Platforms

| Platform | Processing Method | Download Support | Special Features |
|----------|------------------|------------------|------------------|
| Douyin | Playwright | ✅ Watermark-free | Dedicated parser, supports cover, avatar, JSON |
| Xiaohongshu | Playwright | ✅ High-quality | Dedicated parser, bypasses anti-crawling |
| Bilibili | yt-dlp | ✅ | High-quality audio/video |
| YouTube | yt-dlp | ✅ | Multi-format support |
| Twitter/X | yt-dlp | ✅ | Short video download |
| Instagram | yt-dlp | ✅ | Image/video |
| TikTok | yt-dlp | ✅ | Short video |
| Other Platforms | yt-dlp | ✅ | All platforms supported by yt-dlp |

> 🔗 See [yt-dlp Supported Sites List](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

---

## 🛠️ Tech Stack

- **Python 3.7+**
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Multi-platform video download
- **Playwright** - Douyin page simulation parsing
- **requests** - HTTP request handling
- **rich** - Terminal beautification
- **tqdm** - Progress bar display

---

## 📁 Project Structure

```
.
├── main.py                              # Main program entry
├── process/
│   ├── __init__.py
│   ├── douyin.py                        # Douyin processor
│   ├── douyin_downloader_playwright_v6.py  # Douyin dedicated parser
│   ├── download.py                      # Universal downloader
│   ├── result.py                        # Data converter
│   └── utils.py                         # Utility functions
├── downloads/                           # Video save path
├── requirements.txt                     # Dependencies
├── run.sh                              # Launch script
├── .vscode/settings.json               # IDE configuration
├── .python-version                     # Python version
└── README.en.md                        # Project documentation
```

---

## 🚀 Quick Start

1. **Clone Project**
```bash
git clone <repository-url>
cd link2video
```

2. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
playwright install
```

4. **Start Using**
```bash
python main.py "https://v.douyin.com/xxxxx/" -av
```

---

## 🔧 Advanced Configuration

### **IDE Configuration**
Project includes VS Code/Cursor configuration files, automatically uses virtual environment:
- `.vscode/settings.json` - Python interpreter configuration
- `.python-version` - Python version specification

### **Cookie Support**
Douyin download supports cookies.txt file:
1. Place cookies.txt in project root directory
2. Program will automatically load and use cookies

### **Proxy Settings**
yt-dlp supports proxy settings, can be added in code:
```python
'proxy': 'http://proxy-server:port'
```

---

## 🤝 Contributing

Welcome to submit PRs or Issues:

- Add new platform support (like Kuaishou, Xiaohongshu)
- Optimize parsing process and error handling
- Improve user experience and interaction prompts
- Add new download modes

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

## ⚠️ Disclaimer

This tool is for learning and technical research purposes only. Do not use it for any behavior that violates platform service agreements or infringes on others' rights.

Users are responsible for their own usage behavior. Any legal disputes and consequences arising from using this tool to download, distribute, or modify others' content are not related to the author.

For copyright issues, please contact the original video platform or content creators.

---

## 📞 Support

If you encounter problems or have suggestions, please:

1. Check [Issues](../../issues) for similar problems
2. Create a new Issue describing the problem
3. Provide detailed error information and reproduction steps

**Enjoy downloading!** 🎉