# scrapers/scamadvisor.py

import requests
from bs4 import BeautifulSoup
from db import insert_scraped_report

# Add domains you want to evaluate from top reddit/trustpilot results
DOMAINS_TO_CHECK = ["scamstore123.com", "cheapguccishoes.ru"]

def scrape_domain(domain):
    url = f"https://www.scamadviser.com/check-website/{domain}"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        risk_section = soup.find("div", {"class": "trust-score-box"})
        if risk_section:
            score_text = risk_section.text.strip()
            score = int("".join(filter(str.isdigit, score_text)))
            return score
    except Exception as e:
        print(f"❌ Error fetching ScamAdviser for {domain}: {e}")
    return None

def main():
    print("🔍 Checking ScamAdviser scores...")
    for domain in DOMAINS_TO_CHECK:
        score = scrape_domain(domain)
        if score is not None:
            confidence = 100 - score  # inverse mapping: low score = high scam confidence
            insert_scraped_report(
                domain=domain,
                source="ScamAdviser",
                content=f"ScamAdviser score: {score}",
                confidence=confidence
            )
            print(f"✅ {domain} scored {score}/100")

if __name__ == "__main__":
    main()
