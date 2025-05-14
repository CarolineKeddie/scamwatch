# scrapers/trustpilot.py

import requests
from bs4 import BeautifulSoup
from db import insert_scraped_report
from datetime import datetime
import time

SEARCH_TERMS = ["scam site", "didn’t deliver", "fraud", "never arrived", "ripoff"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_trustpilot(term):
    query = term.replace(" ", "+")
    url = f"https://www.trustpilot.com/search?query={query}"
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        domains = []
        for link in links:
            href = link["href"]
            if "/review/" in href:
                domain = href.split("/review/")[-1].split("?")[0]
                if "." in domain:
                    domains.append(domain.lower())

        return set(domains)

    except Exception as e:
        print(f"❌ Error scraping Trustpilot: {e}")
        return []

def main():
    print("🔍 Scraping Trustpilot...")
    for term in SEARCH_TERMS:
        domains = scrape_trustpilot(term)
        for domain in domains:
            insert_scraped_report(
                domain=domain,
                source="Trustpilot",
                content=f"Trustpilot search match for term: '{term}'",
                confidence=75
            )
            print(f"✅ Inserted: {domain} from '{term}'")

if __name__ == "__main__":
    main()
