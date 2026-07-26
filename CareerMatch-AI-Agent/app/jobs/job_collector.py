import requests
from bs4 import BeautifulSoup


def collect_jobs(url: str):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []
    for card in soup.select(".job-card"):
        title = card.select_one(".job-title").get_text(strip=True)
        company = card.select_one(".company-name").get_text(strip=True)
        description = card.select_one(".job-description").get_text(strip=True)
        jobs.append({
            "title": title,
            "company": company,
            "description": description,
        })
    return jobs
