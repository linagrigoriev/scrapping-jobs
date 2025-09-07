from playwright.sync_api import sync_playwright

url = "https://www.indeed.com/jobs?q=dentist&l=Chicago%2C+IL"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    )
    page = browser.new_page()
    page.goto(url)
    
    jobs = page.query_selector_all("a[data-jk]")
    companies = page.query_selector_all("span[data-testid='company-name']")

    for j, c in zip(jobs, companies):
        print("Job:", j.inner_text())
        print("Company:", c.inner_text())
        print("----------------")

    browser.close()
