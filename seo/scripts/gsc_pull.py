#!/usr/bin/env python3
"""Pull Search Console data one day at a time into seo/data/gsc/.

Pulls two reports per day:
  <day>.pages.json    dimension=page         (accurate page totals)
  <day>.queries.json  dimensions=page,query  (Google drops some rows here, so never sum it for totals)

Skips days already on disk, so reruns are cheap and stay under quota.
Search Console data lands 2-3 days late, so the newest day pulled is today - 3.

Auth: set GSC_ACCESS_TOKEN, or have gcloud Application Default Credentials with the
webmasters.readonly scope (see seo/README.md). Site: set GSC_SITE_URL or "site_url" in state.json.
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import subprocess
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "gsc"
API = "https://searchconsole.googleapis.com/webmasters/v3/sites/{}/searchAnalytics/query"


def access_token():
    token = os.environ.get("GSC_ACCESS_TOKEN")
    if token:
        return token
    try:
        return subprocess.check_output(
            ["gcloud", "auth", "application-default", "print-access-token"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        sys.exit("No token. Set GSC_ACCESS_TOKEN or run the gcloud login step in seo/README.md.")


def site_url():
    site = os.environ.get("GSC_SITE_URL")
    if not site:
        site = json.loads((ROOT / "state.json").read_text()).get("site_url", "")
    if not site or site.startswith("TODO"):
        sys.exit("Set GSC_SITE_URL or site_url in seo/state.json.")
    return site


def query(site, token, day, dimensions):
    body = {
        "startDate": day,
        "endDate": day,
        "dimensions": dimensions,
        "rowLimit": 25000,
        "dataState": "final",
    }
    req = urllib.request.Request(
        API.format(urllib.parse.quote(site, safe="")),
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp).get("rows", [])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=28, help="how many days back to cover (default 28)")
    args = ap.parse_args()

    site, token = site_url(), access_token()
    OUT.mkdir(parents=True, exist_ok=True)
    newest = dt.date.today() - dt.timedelta(days=3)
    pulled = 0
    for i in range(args.days):
        day = (newest - dt.timedelta(days=i)).isoformat()
        for name, dims in (("pages", ["page"]), ("queries", ["page", "query"])):
            path = OUT / f"{day}.{name}.json"
            if path.exists():
                continue
            path.write_text(json.dumps(query(site, token, day, dims), indent=1, ensure_ascii=False))
            pulled += 1
    print(f"{pulled} new files in {OUT.relative_to(ROOT.parent)} (newest day {newest})")


if __name__ == "__main__":
    main()
