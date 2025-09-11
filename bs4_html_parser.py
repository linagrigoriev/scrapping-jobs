from bs4 import BeautifulSoup
import pandas as pd
import os

directory = 'content'

def extract_data(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, features="lxml")

    listings = soup.find_all('td', class_='resultContent')

    page_data = []
    for i, listing in enumerate(listings):

        title = listing.select('[title]')[0].get_text()

        company_name = listing.select('[data-testid="company-name"]')[0].get_text()

        company_location = listing.select('[data-testid="text-location"]')[0].get_text()

        page_data.append([title, company_name, company_location])
    
    return page_data

def save_to_sf():
    total_data = []

    for filename in os.scandir(directory):  
        page_data = extract_data(filename=filename.path)
        total_data.extend(page_data)

    df = pd.DataFrame(total_data, columns=["Title", "Company Name", "Company Location"])
    df.to_csv("d.csv", index="False")

def main():
    save_to_sf()

main()