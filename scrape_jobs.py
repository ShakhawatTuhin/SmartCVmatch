import requests
from bs4 import BeautifulSoup
import json

def scrape_remoteok():
    url = "https://remoteok.com/remote-python-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    print(response.text[:1000])  # Print the first 1000 characters
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    job_rows = soup.find_all("tr", class_="job")
    print("Found jobs:", len(job_rows))  # Debug: print number of jobs found
    for row in job_rows:
        title = row.find("h2", itemprop="title")
        company = row.find("h3", itemprop="name")
        tags = row.find_all("div", class_="tag")
        skills = [tag.text.strip().lower() for tag in tags]
        if title and company:
            jobs.append({
                "title": title.text.strip(),
                "company": company.text.strip(),
                "description": "",  # You can try to extract more details if needed
                "skills": skills
            })
    return jobs

if __name__ == "__main__":
    jobs = scrape_remoteok()
    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    print(f"Scraped {len(jobs)} jobs and saved to jobs.json")