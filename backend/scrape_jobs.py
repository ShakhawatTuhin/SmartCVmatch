import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_remoteok():
    url = "https://remoteok.com/remote-python-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    job_rows = soup.find_all("tr", class_="job")
    print("Found jobs:", len(job_rows))
    for row in job_rows:
        title = row.find("h2", itemprop="title")
        company = row.find("h3", itemprop="name")
        tags = row.find_all("div", class_="tag")
        skills = [tag.text.strip().lower() for tag in tags]
        link = row.find("a", class_="preventLink")
        description = ""
        if link and link.get("href"):
            job_url = "https://remoteok.com" + link.get("href")
            job_resp = requests.get(job_url, headers=headers)
            job_soup = BeautifulSoup(job_resp.text, "html.parser")
            desc_div = job_soup.find("div", class_="description")
            if desc_div:
                description = desc_div.get_text(separator=" ", strip=True)
            time.sleep(1)  # Be polite and avoid hammering the server
        if title and company:
            jobs.append({
                "title": title.text.strip(),
                "company": company.text.strip(),
                "description": description,
                "skills": skills
            })
    return jobs

if __name__ == "__main__":
    jobs = scrape_remoteok()
    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    print(f"Scraped {len(jobs)} jobs and saved to jobs.json")