from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
url = "https://www.indeed.com/jobs?q=dentist&l=Chicago%2C+IL"
driver.get(url)

time.sleep(5) # waiting for jobs to load

jobs = driver.find_elements(By.CSS_SELECTOR, "a[data-jk]")
companies = driver.find_elements(By.CSS_SELECTOR, "span[data-testid='company-name']")

for j, c in zip(jobs, companies):
    print("Job: ", j)
    print("Company: ", c)

driver.quit()