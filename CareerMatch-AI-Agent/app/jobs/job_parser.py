from bs4 import BeautifulSoup


def parse_job_posting(html: str):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select_one("h1").get_text(strip=True)
    company = soup.select_one(".company").get_text(strip=True)
    description = soup.select_one(".description").get_text(strip=True)
    return {
        "title": title,
        "company": company,
        "description": description,
    }
