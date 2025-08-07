import asyncio
from playwright.async_api import async_playwright
import os
import pickle
from task_1 import task_1

async def load_session(page):
    # 加载 session cookies
    if os.path.exists('cookies.pkl'):
        with open('cookies.pkl', 'rb') as f:
            cookies = pickle.load(f)
        await page.context.add_cookies(cookies)

async def main():
    async with async_playwright() as p:
        # 替换为你本地的 Chrome 浏览器路径
        # 如果是linux 系统
        print(os.name)
        if os.name == 'posix':
            executable_path = "/opt/google/chrome/google-chrome"
        elif os.name == 'nt':
            executable_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        
        # 启动浏览器并指定路径
        browser = await p.chromium.launch(
            executable_path=executable_path,
            headless=False  # 如果你希望看到浏览器界面，设置为 False
        )

        # 创建一个新的上下文（浏览器窗口）
        context = await browser.new_context()

        # 创建一个新的页面
        page = await context.new_page()

        # 尝试加载保存的 session
        await load_session(page)

        await page.goto("https://www.douyin.com/?recommend=1")

        await task_1(page)

        # 关闭浏览器
        await browser.close()

# 运行异步主函数
if __name__ == "__main__":
    asyncio.run(main())
