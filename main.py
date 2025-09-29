import sys
import os
import argparse
import yt_dlp
from process.douyin import handle_aweme_download


def get_site(url: str):
    """根据链接判断所属平台"""
    if "douyin.com" in url:
        return "douyin"
    if "bilibili.com" in url:
        return "bilibili"
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    return "generic"


def handle_platform_download(url: str, site: str, download_mode: str = "all"):
    """下载分发逻辑"""
    if site == "douyin":
        print(">>> 检测到抖音链接，使用专用解析器下载")
        handle_aweme_download(url, download_mode)
        return

    # 其余平台用 yt-dlp 处理
    # 先获取视频标题，然后创建对应的文件夹
    print(f">>> 正在获取 [{site}] 视频信息...")
    
    # 临时获取视频信息以提取标题
    temp_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(temp_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', '未知标题')
            # 清理标题中的非法字符
            import re
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            safe_title = safe_title[:50]  # 限制长度
            
            base_dir = os.path.join("downloads", site, safe_title)
            os.makedirs(base_dir, exist_ok=True)
            
            common_opts = {
                'quiet': False,
                'outtmpl': os.path.join(base_dir, '%(title)s.%(ext)s'),
            }
        except Exception as e:
            print(f">>> 无法获取视频标题，使用默认文件夹: {e}")
            base_dir = os.path.join("downloads", site, "未知标题")
            os.makedirs(base_dir, exist_ok=True)
            
            common_opts = {
                'quiet': False,
                'outtmpl': os.path.join(base_dir, '%(title)s.%(ext)s'),
            }

    # 根据下载模式决定下载内容
    if download_mode in ["v", "av"]:
        print(f">>> 从 [{site}] 下载视频…")
        with yt_dlp.YoutubeDL({**common_opts, 'format': 'bv*'}) as ydl:
            ydl.download([url])

    if download_mode in ["a", "av"]:
        print(f">>> 从 [{site}] 下载音频…")
        with yt_dlp.YoutubeDL({**common_opts, 'format': 'ba'}) as ydl:
            ydl.download([url])


def main():
    parser = argparse.ArgumentParser(
        description="视频链接智能下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
下载模式说明:
  -a     只下载音频文件(.mp3)
  -v     只下载视频文件(.mp4)
  -av    只下载音频和视频文件(.mp3和.mp4)
  -all   下载所有文件(默认模式，包括封面、头像、JSON等)

示例:
  python main.py "https://v.douyin.com/xxxxx/" -a
  python main.py "https://v.douyin.com/xxxxx/" -v
  python main.py "https://v.douyin.com/xxxxx/" -av
  python main.py "https://v.douyin.com/xxxxx/" -all
        """
    )
    
    parser.add_argument("url", help="视频分享链接")
    parser.add_argument("-a", action="store_true", help="只下载音频文件(.mp3)")
    parser.add_argument("-v", action="store_true", help="只下载视频文件(.mp4)")
    parser.add_argument("-av", action="store_true", help="只下载音频和视频文件(.mp3和.mp4)")
    parser.add_argument("-all", action="store_true", help="下载所有文件(默认模式)")
    
    args = parser.parse_args()
    
    # 确定下载模式
    download_mode = "all"  # 默认模式
    if args.a and not args.v and not args.av:
        download_mode = "a"
    elif args.v and not args.a and not args.av:
        download_mode = "v"
    elif args.av and not args.a and not args.v:
        download_mode = "av"
    elif args.all:
        download_mode = "all"
    elif args.a or args.v or args.av:
        print("错误: 不能同时指定多个下载模式")
        sys.exit(1)
    
    site = get_site(args.url)
    print(f">>> 识别平台: {site}")
    print(f">>> 下载模式: {download_mode}")
    handle_platform_download(args.url, site, download_mode)


if __name__ == "__main__":
    main()
