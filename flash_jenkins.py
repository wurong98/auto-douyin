import asyncio
from playwright.async_api import async_playwright
import os
import pickle

async def load_session(page):
    # 加载 session cookies
    if os.path.exists('cookies.pkl'):
        with open('cookies.pkl', 'rb') as f:
            cookies = pickle.load(f)
        await page.context.add_cookies(cookies)

async def main():
    async with async_playwright() as p:
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


        ##########################################
#         L352507606062zM
# L352507606056zG
# L352507606055zF
# L352507606051zB
# L352507606049zz
# L352507606048zy

# L352507606047zx

# L352507606046zw
        sn = [
            "L352507606062zM",
            "L352507606056zG",
            "L352507606055zF",
            "L352507606051zB",
            "L352507606049zz",
            "L352507606048zy",
            "L352507606047zx",
            "L352507606046zw"
        ]

        for i in sn:
            print(i)

            await page.goto("https://jenkins.autoxing.com/job/chassis-deploy-firmware/build?delay=0sec")

            # 选择 firmware
            await page.select_option('select[name="value"]', value="baseboard_canbus_stm32")

            # # 填写 SN
            await page.locator('div[name="parameter"]:has(input[name="name"][value="SN"]) input[name="value"]').fill(i)


            # # 勾选 dry
            # await page.check('input[type="checkbox"][name="value"]')

            # # 选择 TARGET_HOST
            # await page.select_option('select[name="value"] >> nth=1', value="tunnelglobal.autoxing.com")

            # # 点击 Build 按钮
            await page.click('button:has-text("Build")')

            # 等待跳转或确认
            await page.wait_for_timeout(2000)  # 可改为 wait_for_url / wait_for_response 更智能



        # 关闭浏览器
        await page.wait_for_event("close")

# 运行异步主函数
if __name__ == "__main__":
    asyncio.run(main())
