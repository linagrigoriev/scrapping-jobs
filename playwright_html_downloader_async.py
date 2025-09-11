from playwright.async_api import async_playwright
import asyncio
import os

url = "https://www.indeed.com/jobs?q=dentist&l=Chicago%2C+IL"

async def get_page_content(url, page_num, max_retries=3):
    async with async_playwright() as p:
        for attempt in range(1, max_retries + 1):
            print(f"Attempt {attempt} to load: {url}")
            
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/129.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            await page.goto(url)

            # Scroll down to load jobs
            last_height = await page.evaluate("document.body.scrollHeight")
            while True:
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
                new_height = await page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # get HTML
            content = await page.content()

            # detect login wall
            if "resultContent" not in content:
                print("Login page detected, retrying...")
                await browser.close()
                await asyncio.sleep(5)  # wait before retry
                continue  # try again
            else:
                print("Successfully loaded jobs page")
                number_page_container = page.locator('[data-testid="pagination-page-current"]')
                current_page_text = await number_page_container.inner_text()
                await browser.close()
                print(current_page_text)
                
                if current_page_text == str(page_num):
                    return content, False 
                else:
                    return content, True # reached last page already

        print(f"Failed to bypass login after retries for {url}")
        return None
    
async def scrape_multiple_pages(base_url, max_pages=10):
    os.makedirs("content", exist_ok=True)
    page_num = 0
    
    for page_num in range(max_pages):
        # update URL for each page
        url = f"{base_url}&start={page_num * 10}"
        print(f"Scraping page: {url}")
        
        content, last_page = await get_page_content(url, page_num+1)

        
        if not last_page:
            # save each page separately
            if content:
                filename = f"content\content_page{page_num+1}.html"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
      
                print(f"Saved {filename}")
        else:
            print("Last page reached, stopping.")
            break

        page_num += 1

# scraping data
async def playwright_downloader():
    await scrape_multiple_pages(url)

if __name__ == "__main__":
    asyncio.run(playwright_downloader()) 