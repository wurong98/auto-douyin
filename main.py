import asyncio
from playwright.async_api import async_playwright
import os
import pickle
from task_1 import task_1

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
        context = await p.chromium.launch_persistent_context(
            executable_path=executable_path,
            headless=False,  # 如果你希望看到浏览器界面，设置为 False
            # 保存用户数据
            user_data_dir="./.cache/user_data"
        )

        # 创建一个新的页面
        page = await context.new_page()


        await page.goto("https://www.douyin.com/?recommend=1")

        await task_1(page)

        # 关闭浏览器
        await page.close()

# 运行异步主函数
if __name__ == "__main__":
    asyncio.run(main())
