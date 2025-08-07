from playwright.sync_api  import sync_playwright 

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)   # 无头模式
    page = browser.new_page() 
    page.goto('https://www.douyin.com/?recommend=1') 
    html_content = page.content()   # 获取完整HTML 
    
    with open('douyin.html',  'w', encoding='utf-8') as f:
        f.write(html_content) 
    browser.close() 