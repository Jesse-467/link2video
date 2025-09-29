import asyncio
import json
import os
import re
import time
import requests
from playwright.async_api import async_playwright
import traceback
from process.download import Download


async def get_xiaohongshu_video_with_playwright(share_url: str):
    """使用Playwright获取小红书视频信息"""
    video_info = None
    found_event = asyncio.Event()
    
    async def intercept_response(response):
        nonlocal video_info
        try:
            url = response.url
            headers = response.headers
            
            # 拦截API响应
            if 'application/json' in headers.get('content-type', '').lower():
                try:
                    json_body = await response.json()
                    if isinstance(json_body, dict):
                        print(f"拦截到JSON响应: {url}")
                        print(f"JSON内容预览: {str(json_body)[:200]}...")
                        
                        # 查找包含视频信息的响应
                        if 'data' in json_body and 'note' in json_body['data']:
                            video_info = json_body['data']['note']
                            print(f"从data.note获取到视频信息: {video_info}")
                            found_event.set()
                        elif 'note' in json_body:
                            video_info = json_body['note']
                            print(f"从note获取到视频信息: {video_info}")
                            found_event.set()
                        elif 'item' in json_body and 'note' in json_body['item']:
                            video_info = json_body['item']['note']
                            print(f"从item.note获取到视频信息: {video_info}")
                            found_event.set()
                        elif 'aweme' in json_body:
                            video_info = json_body['aweme']
                            print(f"从aweme获取到视频信息: {video_info}")
                            found_event.set()
                        elif 'video' in json_body:
                            video_info = json_body['video']
                            print(f"从video获取到视频信息: {video_info}")
                            found_event.set()
                except Exception as e:
                    print(f"解析JSON响应失败: {e}")
                    pass
            
            # 拦截视频URL
            if 'video' in url or 'mp4' in url:
                print(f"发现视频URL: {url}")
                if not video_info:
                    video_info = {'video_url': url}
                else:
                    video_info['video_url'] = url
                # 不要因为找到视频URL就标记为成功，需要等待完整的视频信息
                
        except Exception as e:
            pass

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            java_script_enabled=True,
            viewport={'width': 375, 'height': 667},  # 手机尺寸
            device_scale_factor=2
        )
        
        page = await context.new_page()
        page.on("response", intercept_response)
        
        try:
            print(f"正在访问小红书链接: {share_url}")
            await page.goto(share_url, wait_until="networkidle", timeout=30000)
            
            # 等待数据加载
            try:
                await asyncio.wait_for(found_event.wait(), timeout=15)
                print("成功获取到视频信息")
            except asyncio.TimeoutError:
                print("网络拦截未获取到数据，尝试从页面提取...")
                
                # 备用方案：从页面脚本中提取数据
                scripts = await page.query_selector_all('script')
                for script in scripts:
                    content = await script.inner_text()
                    if 'window.__INITIAL_STATE__' in content or 'note' in content:
                        try:
                            print("在脚本中找到相关数据，尝试解析...")
                            # 尝试提取初始状态
                            match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', content)
                            if match:
                                initial_state = json.loads(match.group(1))
                                if 'note' in initial_state:
                                    video_info = initial_state['note']
                                    print(f"从脚本中提取到note数据: {video_info}")
                                    break
                            
                            # 尝试提取note数据
                            match = re.search(r'"note":\s*({.*?})', content)
                            if match:
                                note_data = json.loads(match.group(1))
                                video_info = note_data
                                print(f"从脚本中提取到note数据: {video_info}")
                                break
                                
                        except Exception as e:
                            print(f"解析页面数据失败: {e}")
                            continue
                
                # 如果还是没有完整的视频信息，尝试从DOM获取基本信息
                if not video_info or not video_info.get('title') or video_info.get('title') == '小红书视频':
                    print("尝试从DOM获取基本信息...")
                    dom_info = await extract_basic_info_from_dom(page)
                    if dom_info:
                        # 合并DOM信息和已有的视频URL
                        if video_info:
                            video_info.update(dom_info)
                        else:
                            video_info = dom_info
                else:
                    print("已有完整视频信息，跳过DOM提取")
        
        except Exception as e:
            print(f"获取视频信息时出错: {e}")
            traceback.print_exc()
        finally:
            await browser.close()
    
    return video_info


async def extract_basic_info_from_dom(page):
    """从DOM提取基本信息"""
    try:
        print("开始从DOM提取视频信息...")
        
        # 调试：输出页面HTML内容
        try:
            page_content = await page.content()
            print(f"页面HTML长度: {len(page_content)}")
        except Exception as e:
            print(f"获取页面内容失败: {e}")
        
        # 获取标题 - 尝试多种选择器
        title = "小红书视频"
        title_selectors = [
            'meta[property="og:title"]',
            'title',
            '[data-testid="note-title"]',
            '.note-title',
            '.title',
            'h1',
            '[class*="title"]',
            '[class*="content"]',
            '[class*="desc"]',
            '[class*="text"]',
            'p',
            'div[class*="text"]',
            'span[class*="text"]'
        ]
        
        for selector in title_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    content = await element.get_attribute('content') or await element.inner_text()
                    if content and content.strip() and content != "小红书":
                        title = content.strip()
                        # 清理标题，去掉"- 小红书"等后缀
                        if title.endswith(" - 小红书"):
                            title = title[:-6].strip()
                        print(f"从 {selector} 获取到标题: {title}")
                        break
            except Exception as e:
                continue
        
        # 获取作者信息 - 尝试多种选择器
        author_name = "小红书用户"
        author_selectors = [
            '[data-testid="user-name"]',
            '.user-name',
            '.author-name',
            '[class*="user"]',
            '[class*="author"]',
            '.username',
            '.nickname'
        ]
        
        for selector in author_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    content = await element.inner_text()
                    if content and content.strip():
                        author_name = content.strip()
                        print(f"从 {selector} 获取到作者: {author_name}")
                        break
            except Exception as e:
                continue
        
        # 获取视频URL
        video_element = await page.query_selector('video')
        video_url = None
        if video_element:
            video_url = await video_element.get_attribute('src')
            if not video_url:
                # 尝试获取source标签
                source_element = await video_element.query_selector('source')
                if source_element:
                    video_url = await source_element.get_attribute('src')
        
        # 获取封面
        cover_element = await page.query_selector('meta[property="og:image"]')
        cover_url = None
        if cover_element:
            cover_url = await cover_element.get_attribute('content')
        
        # 获取描述
        desc_element = await page.query_selector('meta[property="og:description"]')
        desc = title
        if desc_element:
            desc = await desc_element.get_attribute('content') or title
        
        print(f"DOM提取结果 - 标题: {title}, 作者: {author_name}")
        
        return {
            'title': title,
            'video_url': video_url,
            'cover_url': cover_url,
            'desc': desc,
            'author': {'nickname': author_name}
        }
    except Exception as e:
        print(f"从DOM提取信息失败: {e}")
        traceback.print_exc()
        return None


def download_video_directly(video_url: str, file_path: str):
    """直接下载视频文件"""
    try:
        print(f"开始下载视频: {video_url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://www.xiaohongshu.com/',
            'Accept': 'video/mp4,video/*,*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(video_url, headers=headers, stream=True, timeout=30)
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code != 200:
            print(f"HTTP错误: {response.status_code}")
            return False, f"HTTP错误: {response.status_code}"
        
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'wb') as f:
            total_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    total_size += len(chunk)
        
        # 检查文件是否真的被创建
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"视频下载成功: {file_path} (大小: {os.path.getsize(file_path)} 字节)")
            return True, file_path
        else:
            print(f"文件创建失败或为空: {file_path}")
            return False, "文件创建失败或为空"
            
    except Exception as e:
        print(f"直接下载失败: {e}")
        traceback.print_exc()
        return False, str(e)


def handle_xiaohongshu_download(share_url: str, download_mode: str = "all"):
    """处理小红书视频下载 - Playwright版本"""
    print(f"开始处理小红书视频: {share_url}")
    
    try:
        # 获取视频信息
        video_info = asyncio.run(get_xiaohongshu_video_with_playwright(share_url))
        
        if not video_info:
            print("无法获取视频信息")
            return False, "无法获取视频信息"
        
        # 提取基本信息
        title = video_info.get('title', '小红书视频')
        video_url = video_info.get('video_url') or video_info.get('play_url')
        cover_url = video_info.get('cover_url') or video_info.get('cover')
        author_name = video_info.get('author', {}).get('nickname', '小红书用户')
        desc = video_info.get('desc', title)
        
        print(f"视频标题: {title}")
        print(f"作者: {author_name}")
        if video_url:
            print(f"视频URL: {video_url[:100]}...")
        
        # 创建安全的文件名 - 格式：视频标题-作者
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()[:30]  # 限制标题长度
        safe_author = re.sub(r'[^\w\s-]', '', author_name).strip()[:20]  # 限制作者长度
        
        if not safe_title:
            safe_title = f"xiaohongshu_video_{int(time.time())}"
        if not safe_author:
            safe_author = "未知作者"
        
        # 创建文件夹名称：视频标题-作者
        folder_name = f"{safe_title}-{safe_author}"
        
        # 创建下载目录
        base_dir = os.path.join("downloads", "xiaohongshu", folder_name)
        os.makedirs(base_dir, exist_ok=True)
        
        # 如果有视频URL，尝试直接下载
        if video_url and video_url.startswith('http'):
            print("尝试直接下载视频...")
            video_file = os.path.join(base_dir, f"{safe_title}.mp4")
            success, message = download_video_directly(video_url, video_file)
            
            if success:
                print(f"视频下载成功: {message}")
                
                # 下载封面
                if cover_url and download_mode in ["all", "v"]:
                    try:
                        cover_file = os.path.join(base_dir, f"{safe_title}_cover.jpg")
                        cover_success, _ = download_video_directly(cover_url, cover_file)
                        if cover_success:
                            print(f"封面下载成功: {cover_file}")
                    except Exception as e:
                        print(f"封面下载失败: {e}")
                
                return True, base_dir
            else:
                print(f"直接下载失败: {message}")
        
        # 如果直接下载失败，尝试使用Download类
        print("尝试使用Download类下载...")
        downloader = create_downloader(download_mode)
        
        success, message = downloader.awemeDownload(
            video_url=video_url or "",
            video_title=title,
            aweme_id=video_info.get('id', ''),
            aweme_desc=desc,
            aweme_author=author_name,
            aweme_music_title="",
            aweme_music_author="",
            aweme_cover=cover_url,
            aweme_avatar="",
            awemePath=base_dir
        )
        
        if success:
            print(f"小红书视频下载成功: {message}")
            return True, message
        else:
            print(f"小红书视频下载失败: {message}")
            return False, message
            
    except Exception as e:
        print(f"处理小红书视频时出错: {e}")
        traceback.print_exc()
        return False, f"处理出错: {str(e)}"


def create_downloader(download_mode: str):
    """根据下载模式创建下载器"""
    if download_mode == "a":
        return Download(music=True, cover=False, avatar=False, resjson=False)
    elif download_mode == "v":
        return Download(music=False, cover=False, avatar=False, resjson=False)
    elif download_mode == "av":
        return Download(music=True, cover=False, avatar=False, resjson=False)
    else:  # "all" or default
        return Download(music=True, cover=True, avatar=True, resjson=True)


if __name__ == "__main__":
    # 测试用例
    test_url = "https://www.xiaohongshu.com/explore/1234567890"
    success, message = handle_xiaohongshu_download(test_url, "all")
    print(f"测试结果: {success}, {message}")
