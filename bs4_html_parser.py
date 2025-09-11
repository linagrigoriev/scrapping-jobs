from bs4 import BeautifulSoup
import pandas as pd

with open('content.html', 'r', encoding="utf-8") as f:
    content = f.read()

soup = BeautifulSoup(content, features="lxml")

listings = soup.find_all('td', class_='resultContent')

total_data = []
for i, listing in enumerate(listings):

    title = listing.select('[title]')[0].get_text()

    company_name = listing.select('[data-testid="company-name"]')[0].get_text()

    company_location = listing.select('[data-testid="text-location"]')[0].get_text()

    total_data.append([title, company_name, company_location])

# Dataframe

df = pd.DataFrame(total_data, columns=["Title", "Company Name", "Company Location"])
print(df)