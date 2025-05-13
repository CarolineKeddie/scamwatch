### populate_supabase.py
# This script inserts example scam data into Supabase (PostgreSQL)
# Run this once to seed your database

import os
import psycopg2
import json
from datetime import datetime

# Supabase connection URL from your environment variables or replace directly
SUPABASE_URL = os.getenv("DATABASE_URL", "postgresql://your_user:your_pass@your_host:5432/your_db")

conn = psycopg2.connect(SUPABASE_URL)
cursor = conn.cursor()

# Define example domains with reports
EXAMPLE_DATA = [
    {
        "domain": "scamstore123.com",
        "label": "Likely Scam",
        "risk_score": 87,
        "reports": [
            {
                "source": "Reddit",
                "content": "Avoid this site, they never shipped the product.",
                "confidence": 75,
                "report_date": datetime.utcnow().isoformat()
            },
            {
                "source": "Trustpilot",
                "content": "Lots of 1-star reviews, many saying scam.",
                "confidence": 80,
                "report_date": datetime.utcnow().isoformat()
            }
        ]
    },
    {
        "domain": "legitstore.co.uk",
        "label": "Safe",
        "risk_score": 15,
        "reports": [
            {
                "source": "Trustpilot",
                "content": "Good service and on-time delivery.",
                "confidence": 20,
                "report_date": datetime.utcnow().isoformat()
            }
        ]
    }
]

# Insert each domain and its reports
for item in EXAMPLE_DATA:
    cursor.execute(
        """
        INSERT INTO merchants (domain, risk_score, label, reports)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (domain) DO NOTHING
        """,
        (item["domain"], item["risk_score"], item["label"], json.dumps(item["reports"]))
    )

    for report in item["reports"]:
        cursor.execute(
            """
            INSERT INTO scam_reports (merchant_domain, source, content, confidence, report_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (item["domain"], report["source"], report["content"], report["confidence"], report["report_date"])
        )

conn.commit()
cursor.close()
conn.close()

print("✅ Supabase seeded with example scam data.")
