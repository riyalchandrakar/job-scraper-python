import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://internshala.com/internships/python-internship/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("❌ Failed to fetch page:", e)
        return None

def parse_internships(html):
    soup = BeautifulSoup(html, "html.parser")
    internships = soup.find_all("div", class_="individual_internship")

    records = []

    for internship in internships:
        title = internship.find("h3", class_="job-internship-name")
        company = internship.find("h4", class_="company-name")
        location = internship.find("a", class_="location_link")
        stipend = internship.find("span", class_="stipend")
        duration = internship.find("div", class_="item_body")

        records.append({
            "Title": title.text.strip() if title else "N/A",
            "Company": company.text.strip() if company else "N/A",
            "Location": location.text.strip() if location else "Remote",
            "Stipend": stipend.text.strip() if stipend else "Not disclosed",
            "Duration": duration.text.strip() if duration else "N/A"
        })

    return records

def analyze_data(df):
    print("\n📊 Basic Analysis")
    print("-----------------")
    print("Total internships scraped:", len(df))
    print("\nTop Locations:")
    print(df["Location"].value_counts().head())

def main():
    print("🔍 Starting internship scraping...")

    html = fetch_page(URL)
    if not html:
        return

    data = parse_internships(html)
    if not data:
        print("⚠️ No data found.")
        return

    df = pd.DataFrame(data)
    df.to_csv("jobs.csv", index=False)

    print("✅ Scraping completed. jobs.csv file created.")
    analyze_data(df)

if __name__ == "__main__":
    main()
