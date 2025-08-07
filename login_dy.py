import asyncio
from playwright.async_api import async_playwright
import os
import pickle

async def save_session(page):
    # 保存 session cookies
    cookies = await page.context.cookies()
    with open('cookies.pkl', 'wb') as f:
        pickle.dump(cookies, f)

async def main():
    async with async_playwright() as p:
        # 替换为你本地的 Chrome 浏览器路径
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


        # 打开网页
        await page.goto("https://www.douyin.com/?recommend=1")

        # 登录成功 等到用户Q键则退出
        # page.on("keydown", lambda event: event.key == "q" and browser.close())

        # 等待浏览器关闭
        await page.wait_for_event("close")
        await save_session(page)

        print("session 文件已经保存")
     

# 运行异步主函数
if __name__ == "__main__":
    asyncio.run(main())
