from playwright.async_api import async_playwright
import asyncio

url = "https://www.indeed.com/jobs?q=dentist&l=Chicago%2C+IL"

async def get_page_content(url, max_retries=3):
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
                await browser.close()
                return content

        print(f"Failed to bypass login after retries for {url}")
        return None
    
async def scrape_multiple_pages(base_url, pages=3):
    
    for page_num in range(pages):
        # update URL for each page
        url = f"{base_url}&start={page_num * 10}"
        print(f"Scraping page: {url}")
        
        content = await get_page_content(url)

        # save each page separately
        if content:
            filename = f"content\content_page{page_num+1}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"Saved {filename}")

# scraping data
async def main():
    # Scrape job data from the specified URL
    await scrape_multiple_pages(url)

# The main function
asyncio.run(main()) 
    
    
