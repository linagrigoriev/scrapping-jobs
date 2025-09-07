import requests
from bs4 import BeautifulSoup

def getdata(url):
    r = requests.get(url)
    return r.text

def html_code(url):
    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser')
    return soup

def job_data(soup):
    jobs = []
    for item in soup.find_all("a", attrs={"data-jk": True}):
        title = item.get_text(strip=True)
        if title:
            jobs.append(title)
    return jobs

def company_data(soup):
    companies = []
    for item in soup.find_all("span", attrs={"data-testid": "company-name"}):
        name = item.get_text(strip=True)
        if name:
            companies.append(name)
    return companies

if __name__ == "__main__":
    job = "dentist"
    location = "Chicago%2C+IL"
    url = f"https://www.indeed.com/jobs?q={job}&l={location}"

    soup = html_code(url)

    job_res = job_data(soup)
    com_res = company_data(soup)

    print("Found", len(job_res), "jobs and", len(com_res), "companies")

    # Print jobs + companies
    for i in range(len(job_res)):
        job_title = job_res[i] if i < len(job_res) else "N/A"
        company = com_res[i] if i < len(com_res) else "N/A"
        print(f"Job: {job_title}")
        print(f"Company: {company}")
        print("-------------------------")
