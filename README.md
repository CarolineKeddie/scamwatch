# 🛡️ ScamWatch

A real-time scam intelligence platform powered by web scraping, user reports, and a risk scoring engine. Built with [Streamlit](https://streamlit.io) and [Supabase](https://supabase.com).

---

## 🌐 Live Demo

> _Coming soon on Streamlit Cloud_

---

## 🚀 Features

- ✅ Check domain risk score (0–100)
- 🧠 Aggregated reports from Reddit, Trustpilot, ScamAdvisor, ActionFraud, and users
- 📊 Confidence-weighted risk scoring system
- ✍️ Crowdsource scam reports via the frontend
- 🗃️ Supabase as scalable Postgres DB
- 🔁 GitHub Actions for daily scraping + updates

---

## 🧱 Tech Stack

- `Streamlit` – interactive front-end
- `Supabase` – PostgreSQL backend
- `psycopg2` – DB connection
- `GitHub Actions` – scheduled scraping automation
- `BeautifulSoup`, `requests` – data extraction
- `Reddit API`, `Trustpilot`, `ScamAdvisor` – sources

---

## 📁 Folder Structure


scamwatch/
│
├── app.py # Main Streamlit app
├── db.py # Supabase integration
├── risk_engine.py # Confidence scoring logic
├── scrapers/ # Scraper modules
│ ├── reddit.py
│ ├── trustpilot.py
│ ├── scamadvisor.py
│ └── actionfraud.py
├── populate_supabase.py # Initial seed script
├── requirements.txt
└── .github/workflows/ # GitHub Actions

## 🔧 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/scamwatch.git
cd scamwatch
