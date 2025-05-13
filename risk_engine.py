def score_domain(domain):
    from db import get_reports_by_domain
    reports = get_reports_by_domain(domain)
    if not reports:
        return 10, "Unknown"
    avg_conf = sum(r['confidence'] for r in reports) / len(reports)
    if avg_conf > 75:
        return int(avg_conf), "Likely Scam"
    elif avg_conf > 50:
        return int(avg_conf), "Suspicious"
    else:
        return int(avg_conf), "Low Risk"
