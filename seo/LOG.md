# SEO log

Append only. Newest entry at the bottom. Never edit or delete an old entry.
Each entry: date, what the data said (with sources), the decision, what changed and when it went live.

## 2026-09-24: setup and first audit (manual, no live data)

Data available: none. No Search Console, analytics, or conversion access yet.

Findings from the repo itself:

- The site is a fork of another author's blog. Theme, nav links, `url`, author, Twitter handle, and
  all five posts belong to 1cadumagalhaes. Source: `git log`, `_config.yml`, theme `_includes/header.html`.
- `url` in `_config.yml` is `https://blog.cadumagalhaes.dev`. Canonical tags and the sitemap point there,
  which tells Google that domain owns the content. Not changed: the real domain is the owner's decision.
- The theme head gave every page the same meta description and loaded the original author's
  Google Tag Manager container (GTM-K7NN6RX). Source: theme `_includes/head.html`, `_layouts/*.html`.
- No page has a call to action or a tracked conversion. Nothing can be judged yet.

Changes made in this commit (not yet live):

- Local `_includes/head.html` override: per-page description, canonical, Open Graph tags, `lang`.
- GTM is now opt-in via `gtm_id` in `_config.yml`. The foreign container no longer loads.
- Theme asset paths now respect `baseurl`.
- Added `jekyll-sitemap`. Added a `description` to all five posts.

Decision: no page gets picked until the brief's Conversion section is filled and the event fires.
