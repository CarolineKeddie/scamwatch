import os
import psycopg2
import uuid
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def get_reports_by_domain(domain):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT source, content, confidence FROM scam_reports WHERE merchant_domain = %s", (domain,))
    rows = cur.fetchall()
    conn.close()
    return [{"source": r[0], "content": r[1], "confidence": r[2]} for r in rows]

def submit_user_report(domain, content):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scam_reports (id, merchant_domain, source, content, confidence, report_date) VALUES (%s, %s, %s, %s, %s, %s)",
        (str(uuid.uuid4()), domain, "User", content, 60, datetime.utcnow())
    )
    conn.commit()
    conn.close()
