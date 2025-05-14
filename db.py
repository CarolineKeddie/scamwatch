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
def insert_scraped_report(domain, source, content, confidence):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO scam_reports (id, merchant_domain, source, content, confidence, report_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (str(uuid.uuid4()), domain, source, content, confidence, datetime.utcnow())
    )
    conn.commit()
    conn.close()

def get_all_domains():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT merchant_domain FROM scam_reports")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]

def get_flagged_domains(threshold=60):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT domain, risk_score, label FROM merchants WHERE risk_score >= %s ORDER BY risk_score DESC", (threshold,))
    rows = cur.fetchall()
    conn.close()
    return [{"domain": r[0], "risk_score": r[1], "label": r[2]} for r in rows]

def get_reports_over_time():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT DATE(report_date) as report_day, COUNT(*) 
        FROM scam_reports 
        GROUP BY report_day 
        ORDER BY report_day
    """)
    rows = cur.fetchall()
    conn.close()
    return [{"report_date": r[0], "count": r[1]} for r in rows]

