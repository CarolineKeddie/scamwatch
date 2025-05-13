# scrapers/reddit.py

import requests
import time
import re
from urllib.parse import urlparse
from db import insert_scraped_report

# Keywords that often appear in scam warnings
SCAM_KEYWORDS = ["scam", "fraud", "fake", "ripoff", "scammer", "avoid", "stole", "didn't arrive", "never arrived"]

# Subreddits that are scam-report-heavy
TARGET_SUBREDDITS = ["scams", "ScamReports", "ScamAlert", "UKPersonalFinance"]

# Time filter (last 24h)
def get_unix_day_range():
    now = int(time.time())
    one_day_ago = now - 86400
    return one_day_ago, now

# Extract domain from URL
def extract_domain(text):
    urls = re.findall(r'(https?://[^\s]+)', text)
    domains = []
    for url in urls:
        try:
            domain = urlparse(url).netloc
            if domain:
                domains.append(domain.lower())
        except Exception:
            continue
    return list(set(domains))

def fetch_posts(subreddit):
    after, before = get_unix_day_range()
    url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&after={after}&before={before}&size=100&sort=desc"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        print(f"❌ Error fetching posts from r/{subreddit}: {e}")
        return []

def is_scam_post(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in SCAM_KEYWORDS)

def main():
    print("🔍 Scraping Reddit for scam reports...")
    for subreddit in TARGET_SUBREDDITS:
        posts = fetch_posts(subreddit)
        for post in posts:
            content = f"{post.get('title', '')}\n{post.get('selftext', '')}"
            if is_scam_post(content):
                domains = extract_domain(content)
                for domain in domains:
                    try:
                        insert_scraped_report(
                            domain=domain,
                            source=f"Reddit:r/{subreddit}",
                            content=content[:500],  # Truncate to 500 chars
                            confidence=80  # Reddit reports are semi-reliable
                        )
                        print(f"✅ Inserted report for domain: {domain}")
                    except Exception as e:
                        print(f"⚠️ Failed to insert report: {e}")

if __name__ == "__main__":
    main()
