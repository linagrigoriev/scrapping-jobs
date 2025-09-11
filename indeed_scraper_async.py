import asyncio
from playwright_html_downloader_async import playwright_downloader
from bs4_html_parser import bs4_parser_csv

if __name__ == "__main__": 
    asyncio.run(playwright_downloader())
    bs4_parser_csv()