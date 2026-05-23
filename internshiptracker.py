import json
import os
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
APPLIED_FILE=os.path.join(BASE_DIR,'applied_jobs.json')
def get_jobs():
    import requests
    from bs4 import BeautifulSoup
    url = "https://www.linkedin.com/jobs/search/?currentJobId=4403867709&f_I=96%2C4%2C6&geoId=106155005&keywords=internship&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R"
    headers = {
    "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup=BeautifulSoup(response.text, "html.parser")
    jobs=[]
    keywords=["software","developer","engineer","backend","back end","front end","full stack","fullstack","web","ai","ml","machine learning","data","python","java","c++","node","cloud","cyber","devops"]
    job_cards=soup.find_all("div",class_="base-search-card")
    for card in job_cards:
        title=card.find("h3")
        company=card.find("h4")
        location=card.find("span",class_="job-search-card__location")
        date_posted=card.find("time")
        link=card.find("a")
        if title and link:
            title_text=title.text.strip()
            if not any(keywords.lower() in title_text.lower() for keywords in keywords):
                continue
            jobs.append({"title":title.text.strip(),
                         "company": company.text.strip() if company else "Unknown Company",
                         "location":location.text.strip() if location else "Unknown Location",
                         "date posted":date_posted.text.strip() if date_posted else "Unknown Date",
                         "link":link["href"]})
    return jobs
def save_applied(job):
    import json
    applied_jobs=get_applied_jobs()
    if any(
        j["link"]==job["link"]
        for j in applied_jobs
    ):
        return
    applied_jobs.append(job)
    with open(APPLIED_FILE,"w") as f:
        json.dump(applied_jobs,f,indent=4)
def get_applied_jobs():
    import json
    try:
        with open(APPLIED_FILE,"r") as f:
            applied_jobs=json.load(f)
    except:
        applied_jobs=[]
    return applied_jobs
def is_applied(job):
    applied_jobs=get_applied_jobs()
    return any(
        j["link"]==job["link"]
        for j in applied_jobs
    )
def remove_applied(job):
    import json
    applied_jobs=get_applied_jobs()
    applied_jobs=[
        j for j in applied_jobs
        if j["link"]!=job["link"]
    ]
    with open(
        APPLIED_FILE,
        "w"
    ) as f:
        json.dump(applied_jobs,f,indent=4)

def export_applied_jobs():
    import csv
    import os
    jobs=get_applied_jobs()
    filepath=os.path.abspath("applied_jobs.csv")
    print("saving to",filepath)
    print("Exporting: ",len(jobs),"jobs")
    with open(
        "applied_jobs.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:
        writer=csv.writer(f)
        writer.writerow([
            "Title",
            "Company",
            "Location",
            "Date Posted",
            "Link",
        ])
        for job in jobs:
            writer.writerow([
                job["title"],
                job["company"],
                job["location"],
                job["date posted"],
                job["link"],
            ])
    print("Exported: ",len(jobs),"jobs")
if __name__ == "__main__":
    jobs=get_jobs()
    for job in jobs:
            print(job["title"])
            print(job["company"])
            print(job["location"])
            print(job["date posted"])
            print(job["link"])
            print()
