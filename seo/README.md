# SEO agent workspace

A Claude Code setup that finds the one page worth improving each week, checks it, and recommends one change. It never publishes. You do.

## What is here

| File | Purpose |
|---|---|
| `BRIEF.md` | What the site sells and what counts as a conversion. Fill this first. |
| `state.json` | Search Console property, conversion event, active test, per-page baselines. |
| `LOG.md` | Append-only record of every run and change. |
| `WEEKLY.md` | The prompt for the weekly scheduled run. |
| `scripts/gsc_pull.py` | Pulls Search Console data one day at a time into `data/gsc/`. |
| `scripts/serp.py` | DataForSEO: top 10, AI Mode answer, search volume. Sandbox by default. |
| `scripts/pagespeed.py` | PageSpeed Insights, mobile first, only failures over 300 ms. |
| `../.claude/hooks/require-approval.py` | Asks before any push, paid call, URL submission, or external write. |

`data/` is git-ignored. Search Console numbers stay on your machine.

## Setup, in order

Do not skip step 1. Every step after it is wasted without it.

1. **Make pages convert.** Pick one action (newsletter, contact, booked call). Add it to the post layout. Track it as a named event. Write both into `BRIEF.md`.
2. **Own the site.** Set `url`, `title`, `author` and social handles in `_config.yml` to yours. Set `gtm_id` to your own container if you use GTM. Canonical tags and the sitemap use `url`.
3. **Search Console.** Verify your property. Submit `<your url>/blog/sitemap.xml`. Put the property in `state.json` as `site_url`. Then authenticate once:
   ```sh
   gcloud auth application-default login \
     --scopes=https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform
   python3 seo/scripts/gsc_pull.py --days 90
   ```
4. **DataForSEO.** Export `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`. Test against the sandbox first: `python3 seo/scripts/serp.py serp "como usar docker"`. Add `--live` only once the output looks right. Set a spend limit in their dashboard.
5. **Page reading and web search (optional).** Add Firecrawl and Parallel as MCP servers with their own API keys:
   ```sh
   claude mcp add firecrawl -e FIRECRAWL_API_KEY=... -- npx -y firecrawl-mcp
   ```
   Keep keys out of the repo. Without these, the agent uses its built-in web fetch.
6. **Schedule.** Create a weekly scheduled task in Claude Code with `WEEKLY.md` as the prompt and this repo as the folder. Keep it in a permission mode that stops for approval. Cloud routines do not stop for approval: give those read-only access only.

## Rules that make this work

- One change at a time. Otherwise you cannot tell what worked.
- Wait at least two weeks before judging a change.
- Judge on conversions, not rankings.
- Every finding needs a source. No source, no action.
