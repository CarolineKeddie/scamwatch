import os
import psycopg2
import uuid
from datetime import datetime
import streamlit as st # <-- Import streamlit

# We are removing the top-level os.getenv call here
# DATABASE_URL = os.getenv("DATABASE_URL") # <-- REMOVE OR COMMENT THIS LINE

def get_conn():
    """Gets the database connection string from Streamlit secrets or env var."""
    DATABASE_URL = None

    # --- START: Modified section to look for "DATABASE_URL" key ---
    # Try to get the connection string from Streamlit secrets first (for Streamlit Cloud)
    # We are looking for the key "DATABASE_URL" inside the [connections.supabase] section
    if "connections" in st.secrets and "supabase" in st.secrets["connections"] and "DATABASE_URL" in st.secrets["connections"]["supabase"]:
        DATABASE_URL = st.secrets["connections"]["supabase"]["DATABASE_URL"] # <-- Now correctly looking for 'DATABASE_URL' key
    else:
        # Fallback to environment variable (e.g., for local development or GitHub Actions)
        DATABASE_URL = os.getenv("DATABASE_URL")
    # --- END: Modified section ---


    # Check if we successfully got the URL
    if not DATABASE_URL:
         # Raise an error if no URL was found in either place
         raise ValueError("Database connection URL not found. Please set it in Streamlit secrets (under [connections.supabase] with key DATABASE_URL) or as an environment variable.")

    # Optional: Add some logging for debugging (masking password)
    print(f"Attempting to connect to database...")
    # print(f"Connecting using URL (sensitive parts masked): {DATABASE_URL.split('@')[-1]}") # Use with caution

    return psycopg2.connect(DATABASE_URL)

# --- Your existing database functions remain the same ---

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
