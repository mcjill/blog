#!/usr/bin/env python3
"""PageSpeed Insights check for one URL. Prints the score, Core Web Vitals field data when
Google has it, and only the failing audits that cost real time.

Optional: PAGESPEED_API_KEY (without it Google rate-limits you quickly).
"""
import argparse
import json
import os
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--strategy", choices=["mobile", "desktop"], default="mobile")
    args = ap.parse_args()

    params = {"url": args.url, "strategy": args.strategy, "category": "performance"}
    if os.environ.get("PAGESPEED_API_KEY"):
        params["key"] = os.environ["PAGESPEED_API_KEY"]
    with urllib.request.urlopen(f"{API}?{urllib.parse.urlencode(params)}") as resp:
        data = json.load(resp)

    lh = data["lighthouseResult"]
    field = data.get("loadingExperience", {}).get("metrics", {})
    failing = [
        {"id": a["id"], "title": a["title"], "savings_ms": a["details"]["overallSavingsMs"]}
        for a in lh["audits"].values()
        if a.get("score") is not None and a["score"] < 0.9
        and a.get("details", {}).get("overallSavingsMs", 0) >= 300
    ]
    print(json.dumps({
        "url": args.url,
        "strategy": args.strategy,
        "score": round(lh["categories"]["performance"]["score"] * 100),
        "field_data": {k: v.get("category") for k, v in field.items()} or "missing: not enough real-user traffic",
        "failing_audits_over_300ms": sorted(failing, key=lambda a: -a["savings_ms"]),
    }, indent=1))


if __name__ == "__main__":
    main()
