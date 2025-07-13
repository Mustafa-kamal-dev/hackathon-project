# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
# from webdriver_manager.chrome import ChromeDriverManager

def scrape_linkedin_jobs(job_title, location="Pakistan"):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver_path = r"C:\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    jobs_list = []

    for page in range(3):  # Scrape 75 jobs
        start = page * 25
        url = f"https://www.linkedin.com/jobs/search?keywords={job_title}&location={location}&start={start}"
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_cards = soup.find_all('div', class_='job-search-card')

        for card in job_cards:
            job = {}
            title = card.find('h3')
            job['title'] = title.text.strip() if title else 'N/A'

            company = card.find('h4')
            job['company'] = company.text.strip() if company else 'N/A'

            location_span = card.find('span', class_='job-search-card__location')
            job['location'] = location_span.text.strip() if location_span else 'N/A'

            date = card.find('time')
            job['date'] = date.text.strip() if date else 'Recently'

            link = card.find('a')
            job['link'] = 'https://www.linkedin.com' + link['href'] if link and link.get('href') else 'N/A'

            jobs_list.append(job)

        time.sleep(1)

    driver.quit()
    df = pd.DataFrame(jobs_list)
    df.to_csv("jobs.csv", index=False)
    return df
