# scrapers/actionfraud.py

from db import insert_scraped_report
from datetime import datetime

# Simulated public domain alerts
ACTION_FRAUD_DOMAINS = [
    {"domain": "dodgycryptoexchange.uk", "reason": "Reported to Action Fraud: fake crypto platform"},
    {"domain": "spoof-banklogin.com", "reason": "Fake banking login portal stealing info"},
]

def main():
    print("📢 Simulating Action Fraud ingestion...")
    for item in ACTION_FRAUD_DOMAINS:
        insert_scraped_report(
            domain=item["domain"],
            source="ActionFraud",
            content=item["reason"],
            confidence=90
        )
        print(f"✅ Inserted Action Fraud alert: {item['domain']}")

if __name__ == "__main__":
    main()
