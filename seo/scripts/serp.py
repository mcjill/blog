#!/usr/bin/env python3
"""DataForSEO helper: top 10 results, AI Mode answer, and search volume for a query.

Defaults to the sandbox (fake data, same shape, no charge). Pass --live to spend real credits;
the Claude Code hook asks before any --live call runs.

Auth: DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD.
Defaults target Brazil in Portuguese (location 2076, language pt).
"""
import argparse
import base64
import json
import os
import sys
import urllib.request

ENDPOINTS = {
    "serp": "/v3/serp/google/organic/live/advanced",
    "ai-mode": "/v3/serp/google/ai_mode/live/advanced",
    "volume": "/v3/keywords_data/google_ads/search_volume/live",
}


def call(host, path, task):
    login, password = os.environ.get("DATAFORSEO_LOGIN"), os.environ.get("DATAFORSEO_PASSWORD")
    if not (login and password):
        sys.exit("Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD.")
    auth = base64.b64encode(f"{login}:{password}".encode()).decode()
    req = urllib.request.Request(
        f"https://{host}{path}",
        data=json.dumps([task]).encode(),
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=ENDPOINTS)
    ap.add_argument("keywords", nargs="+", help="one query for serp/ai-mode, one or more for volume")
    ap.add_argument("--location", type=int, default=2076)
    ap.add_argument("--language", default="pt")
    ap.add_argument("--live", action="store_true", help="use the paid API instead of the sandbox")
    args = ap.parse_args()

    task = {"location_code": args.location, "language_code": args.language}
    if args.kind == "volume":
        task["keywords"] = args.keywords
    else:
        task["keyword"] = " ".join(args.keywords)
        if args.kind == "serp":
            task["depth"] = 10
    host = "api.dataforseo.com" if args.live else "sandbox.dataforseo.com"
    print(json.dumps(call(host, ENDPOINTS[args.kind], task), indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
