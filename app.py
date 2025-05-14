import streamlit as st
import altair as alt
from risk_engine import score_domain
from db import get_reports_by_domain, submit_user_report, get_all_domains, get_flagged_domains, get_reports_over_time
# TEMP DEBUG LINE – check what DB URL Streamlit is seeing
st.write("🔍 Current DB URL:", os.getenv("DATABASE_URL"))

from datetime import datetime

st.set_page_config(page_title="ScamWatch", page_icon="🛡️")
st.title("🛡️ ScamWatch: Real-Time Scam Detection")


def clean_domain(raw):
    return raw.strip().lower().replace("https://", "").replace("http://", "").split("/")[0]


# --- Recent Domain Dropdown ---
st.markdown("## 🔍 Check a Domain")
all_domains = get_all_domains()
selected = st.selectbox("Choose from known domains (or type your own below)", options=[""] + all_domains)
typed_domain = st.text_input("Or enter a domain")

final_domain = clean_domain(typed_domain or selected)

if st.button("Check Domain"):
    if final_domain:
        with st.spinner("Analyzing domain..."):
            score, label = score_domain(final_domain)
            st.subheader(f"Risk Score: {score} / 100 — **{label}**")

            reports = get_reports_by_domain(final_domain)
            if reports:
                st.markdown("### Recent Reports")
                for report in reports:
                    st.markdown(f"🗣️ **{report['source']}**: _{report['content']}_")
            else:
                st.info("No reports found for this domain yet.")
    else:
        st.warning("Please enter or select a domain.")

st.markdown("---")

# --- Submit Scam Report ---
st.subheader("📣 Submit a Scam Report")
user_domain = st.text_input("Report Domain")
user_content = st.text_area("Describe what happened")

if st.button("Submit Report"):
    if user_domain and user_content:
        clean = clean_domain(user_domain)
        submit_user_report(clean, user_content)
        st.success("✅ Thanks! Your report has been submitted.")
    else:
        st.error("Please fill in both fields.")

# --- Admin Section ---
if st.sidebar.checkbox("🛠️ Admin View"):
    st.markdown("## ⚠️ Flagged Domains")
    flagged = get_flagged_domains()
    if flagged:
        st.dataframe(flagged)
    else:
        st.info("No high-risk domains flagged yet.")

    st.markdown("## 📊 Scam Reports Over Time")
    chart_data = get_reports_over_time()
    if chart_data:
        chart = alt.Chart(chart_data).mark_line(point=True).encode(
            x='report_date:T',
            y='count:Q',
            tooltip=["report_date:T", "count:Q"]
        ).properties(width=700, height=400)
        st.altair_chart(chart)
    else:
        st.info("No data yet to chart.")
