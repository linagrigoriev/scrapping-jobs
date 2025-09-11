from playwright.sync_api import sync_playwright
import time


url = "https://www.indeed.com/jobs?q=dentist&l=Chicago%2C+IL"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False
        # executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    )
    context= browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    page.goto(url)
    time.sleep(3)

    last_height = page.evaluate("document.body.scrollHeight")   # need to handle infinite scrolling
    
    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)                             # wait for 2 seconds to load
        new_height = page.evaluate("document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    content = page.content()
    
    with open('content.html', 'w', encoding='utf-8') as f:
        f.write(content)

    browser.close()
