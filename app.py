import streamlit as st
from risk_engine import score_domain
from db import get_reports_by_domain, submit_user_report

st.title("🛡️ ScamWatch: Real-Time Scam Detection")

domain = st.text_input("Enter a store domain (e.g., scamstore123.com)")

if st.button("Check Domain"):
    if domain:
        score, label = score_domain(domain)
        st.subheader(f"Risk Score: {score} / 100 ({label})")
        reports = get_reports_by_domain(domain)
        for report in reports:
            st.markdown(f"🗣️ **{report['source']}**: _{report['content']}_")

st.markdown("---")
st.subheader("Submit a Scam Report")
user_domain = st.text_input("Domain")
user_content = st.text_area("Describe the issue")
if st.button("Submit Report"):
    submit_user_report(user_domain, user_content)
    st.success("Thanks! Your report has been submitted.")
