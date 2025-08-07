import asyncio
from playwright.async_api import Page
import random
from time_text_parser import parse_relative_time
import time
import colorama
async def scroll_comments_section(page):
    comment_section = await page.query_selector("div[data-e2e='comment-list']")
    
    last_height = await comment_section.evaluate("this.scrollHeight")
    
    while True:
        # 滚动评论区到底部
        await comment_section.evaluate('this.scrollTop = this.scrollHeight')
        
        # 等待页面加载
        await page.wait_for_timeout(1000)
        
        # 获取新的滚动高度
        new_height = await comment_section.evaluate("this.scrollHeight")
        
        # 如果滚动到底部没有变化，说明已经到底
        if new_height == last_height:
            break
        
        last_height = new_height

async def scrape_comments(page: Page):
    # 滚动评论区到底部并加载所有评论
    await scroll_comments_section(page)

    # 查找所有“展开回复”按钮并点击、
    while True:
        reply_buttons = await page.query_selector_all("button.comment-reply-expand-btn")
        if len(reply_buttons) == 0:
            break

        try:
            await reply_buttons[0].click()
            await page.wait_for_timeout(1000)  # 等待展开后的内容加载
        except Exception as e:
            print(f"点击展开按钮时出错: {e}")
    
    # 提取评论内容
    comments = await page.query_selector_all("div[data-e2e='comment-item']")
    
    for comment in comments:
        try:
            user_link = await comment.query_selector("a.uz1VJwFY")  # 使用正确的类名
            user_href = await user_link.get_attribute("href") if user_link else "未知链接"

            # 提取评论内容
            content_elem = await comment.query_selector("div.C7LroK_h span")
            content = await content_elem.inner_text() if content_elem else "没有评论内容"
            
            print(colorama.Fore.GREEN + f"用户链接: https:{user_href}\t评论: {content}" + colorama.Fore.RESET)
        except Exception as e:
            print(e)
            print("可能div class更新请及时更新")
    # 打印条数
    print(f"已获取 {len(comments)} 条评论")
    
async def fetch_video_info(page: Page):
    try:
        print("=== 当前视频信息 ===")
        
        # 使用 data-e2e="feed-active-video" 精确定位当前视频
        active_videos = page.locator('[data-e2e="feed-active-video"]')
        await active_videos.wait_for(state="attached", timeout=300)  # 超过3秒没有找到元素则报错
        count = await active_videos.count() # 直播找不到活动视频 需要跳过
        
        video_info = {}

        if count > 0:
            print(f"检测到 {count} 个活动视频")
            # 通常只有一个活动视频，但为了保险起见，我们使用第一个
            active_video = active_videos.first
            
            # 定义要提取的信息和对应的选择器
            info_extractors = [
                ("用户名", '[data-e2e="feed-video-nickname"]', 'div.account span'),
                ("视频描述", '[data-e2e="video-desc"]', 'div.title'),
                ("发布时间", 'div.video-create-time span', 'span.time')
            ]
            
            for info_name, primary_selector, fallback_selector in info_extractors:
                try:
                    # 优先使用主要选择器
                    locator = active_video.locator(primary_selector)
                    if await locator.count() == 0:
                        # 如果主要选择器找不到，使用备用选择器
                        locator = active_video.locator(fallback_selector)
                    
                    if await locator.count() > 0:
                        text = await locator.first.inner_text()
                        video_info[info_name] = text
                    else:
                        print(f"未找到{info_name}元素")
                except Exception as e:
                    print(f"获取{info_name}失败: {e}")

            print(colorama.Fore.GREEN + f"视频信息: {video_info}" + colorama.Fore.RESET)
            
            delat_time_second = time.time() - parse_relative_time(video_info["发布时间"]).timestamp() 
            print(f"delta time: {delat_time_second}")
            if delat_time_second < 24 * 60 * 60: # 24小时内的才抓评论
                await scrape_comments(page)
            else:
                print(colorama.Fore.RED + "当前视频已超过24小时，跳过抓取评论" + colorama.Fore.RESET)
        else:
            print(colorama.Fore.RED + "未找到当前活动视频，可能是直播" + colorama.Fore.RESET)
            
    except Exception as e:
        print(f"获取视频信息时出错: {e}")
async def task_1(page: Page):
    """
    定义的任务1
    任务描述：不停刷抖音，随机停留5-10秒，抓取视频信息，避开直播。
    """

    print("将展开评论区")
    await page.wait_for_timeout(5000) # 等评论区展开
    await page.keyboard.press("x")
    await page.wait_for_timeout(1000) # 等评论区展开
    print("已展开评论区")


    while True:
        # div video 
        await fetch_video_info(page)

        await asyncio.sleep(random.randint(3, 6))
        print("正在滚动到下一个视频")
        await page.keyboard.press('ArrowDown')
