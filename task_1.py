import asyncio
from playwright.async_api import Page
import random


async def fetch_comments(page: Page):
    try:
        print("=== 获取评论区信息 ===")
        
        # 定位评论区
        # wait 数据加载一会儿
        await asyncio.sleep(2)
        comment_list_locator = page.locator('[data-e2e="comment-list"]')
        
        # 检查是否找到评论区
        if await comment_list_locator.count() > 0:
            # 获取评论列表中的所有评论 data-e2e="comment-item"
            comments = await comment_list_locator.first.locator('[data-e2e="comment-item"]').all()
            if comments:
                print(f"找到 {len(comments)} 条评论")
                for index, comment in enumerate(comments):
                    try:
                        # 获取每条评论的用户和内容
                        username_locator = comment.locator('div.comment-user-name')
                        content_locator = comment.locator('div.comment-content')
                        
                        username = await username_locator.inner_text() if await username_locator.count() > 0 else '未知'
                        content = await content_locator.inner_text() if await content_locator.count() > 0 else '无内容'
                        
                        print(f"评论 {index + 1}: 用户名: {username}, 内容: {content}")
                    except Exception as e:
                        print(f"获取评论 {index + 1} 失败: {e}")
            else:
                print("没有评论数据")
            
            # 模拟向下滚动加载更多评论
            print("正在向下滚动加载更多评论...")
            await page.mouse.wheel(0, 500)  # 向下滚动
            await asyncio.sleep(2)  # 延迟 2 秒，避免过快加载
        else:
            print("未找到评论区")
    except Exception as e:
        print(f"获取评论区时出错: {e}")

async def fetch_video_info(page: Page):
    try:
        print("=== 当前视频信息 ===")
        
        # 使用 data-e2e="feed-active-video" 精确定位当前视频
        active_videos = page.locator('[data-e2e="feed-active-video"]')
        await active_videos.wait_for(state="attached", timeout=300)  # 超过3秒没有找到元素则报错
        count = await active_videos.count() # 直播找不到活动视频 需要跳过
        
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
                        print(f"{info_name}: {text}")
                    else:
                        print(f"未找到{info_name}元素")
                except Exception as e:
                    print(f"获取{info_name}失败: {e}")

            # TODO 获取该视频的评论区
            await fetch_comments(page)
        else:
            print("未找到当前活动视频，可能是直播")
            
    except Exception as e:
        print(f"获取视频信息时出错: {e}")
async def task_1(page: Page):
    """
    定义的任务1
    任务描述：不停刷抖音，随机停留5-10秒，抓取视频信息，避开直播。
    """
    while True:
        # div video 
        await fetch_video_info(page)

        await asyncio.sleep(random.randint(3, 6))
        print("正在滚动到下一个视频")
        await page.keyboard.press('ArrowDown')
