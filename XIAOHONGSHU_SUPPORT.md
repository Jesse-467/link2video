# 小红书视频下载支持说明

## 🎯 实现方案

小红书视频下载采用了与抖音类似的Playwright方案，通过模拟真实浏览器环境来绕过反爬机制。

## 🔧 技术实现

### 1. 平台识别
- 在 `main.py` 中添加了 `xiaohongshu.com` 域名识别
- 自动路由到专用的小红书下载器

### 2. 专用下载器
- **文件位置**: `process/xiaohongshu_playwright.py`
- **核心功能**: 
  - 使用Playwright模拟手机浏览器访问
  - 拦截网络响应获取视频信息
  - 从DOM提取备用信息
  - 直接下载视频文件

### 3. 反爬绕过策略

#### 浏览器模拟
```python
context = await browser.new_context(
    user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    java_script_enabled=True,
    viewport={'width': 375, 'height': 667},  # 手机尺寸
    device_scale_factor=2
)
```

#### 网络拦截
- 拦截所有JSON响应，查找包含视频信息的API
- 拦截视频URL，直接获取下载链接
- 支持多种数据格式的解析

#### 备用方案
- 从页面脚本中提取 `window.__INITIAL_STATE__` 数据
- 从DOM元素中提取基本信息
- 多重备用机制确保成功率

## 📁 文件结构

```
process/
├── xiaohongshu_playwright.py    # 小红书专用下载器
├── xiaohongshu_simple.py        # 简化版本（备用）
└── xiaohongshu_downloader.py    # 完整版本（备用）
```

## 🚀 使用方法

### 基本命令
```bash
# 下载所有文件（默认）
python main.py "https://www.xiaohongshu.com/explore/xxxxx"

# 只下载视频
python main.py "https://www.xiaohongshu.com/explore/xxxxx" -v

# 下载音视频
python main.py "https://www.xiaohongshu.com/explore/xxxxx" -av
```

### 下载模式支持
- `-a`: 只下载音频（小红书通常没有独立音频）
- `-v`: 只下载视频 ✅
- `-av`: 下载音视频 ✅
- `-all`: 下载全部内容 ✅

## 📂 输出结构

```
downloads/xiaohongshu/
└── 视频标题-作者名/
    ├── 视频标题.mp4          # 主视频文件
    └── 视频标题_cover.jpg    # 封面图片（如果可用）
```

## ⚠️ 注意事项

### 1. 反爬限制
- 小红书有严格的反爬机制
- 需要模拟真实用户行为
- 建议控制下载频率

### 2. 成功率
- 网络拦截方案：较高成功率
- DOM解析方案：中等成功率
- 直接下载方案：较低成功率

### 3. 视频质量
- 获取的是平台提供的最高质量视频
- 通常为MP4格式
- 分辨率取决于原视频质量

## 🔄 更新日志

### v1.0.0 (2024-09-29)
- ✅ 添加小红书平台识别
- ✅ 实现Playwright专用下载器
- ✅ 支持多种下载模式
- ✅ 添加网络拦截和DOM解析
- ✅ 集成到主程序

## 🛠️ 技术细节

### 网络拦截逻辑
```python
async def intercept_response(response):
    # 拦截JSON API响应
    if 'application/json' in headers.get('content-type', '').lower():
        json_body = await response.json()
        if 'data' in json_body and 'note' in json_body['data']:
            video_info = json_body['data']['note']
            found_event.set()
    
    # 拦截视频URL
    if 'video' in url or 'mp4' in url:
        video_info['video_url'] = url
        found_event.set()
```

### 直接下载逻辑
```python
def download_video_directly(video_url: str, file_path: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)...',
        'Referer': 'https://www.xiaohongshu.com/',
    }
    response = requests.get(video_url, headers=headers, stream=True)
    # 保存文件...
```

## 🎯 未来优化

1. **Cookie支持**: 添加登录状态支持
2. **批量下载**: 支持用户主页批量下载
3. **质量选择**: 支持不同分辨率选择
4. **错误重试**: 增强错误处理和重试机制
5. **进度显示**: 添加下载进度条

## 📞 问题反馈

如果遇到下载问题，请提供：
1. 具体的视频链接
2. 错误信息截图
3. 系统环境信息
4. 下载模式参数

---

**注意**: 请遵守相关法律法规，仅用于个人学习和研究目的。
