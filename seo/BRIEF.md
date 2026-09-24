# SEO brief

The agent reads this file first on every run. It judges pages only as well as this file explains what they sell.
Fill every `TODO` before the first real run. A run with `TODO` left in "Conversion" must stop and say so.

## Business

- Who runs this site: TODO (your name, not the original author's)
- What it sells or promotes: TODO (a service, a product, a job search, consulting calls, a newsletter)
- Who buys: TODO (one kind of reader, e.g. "data engineers in Brazil setting up WSL for the first time")
- Language and market: pt-BR, Brazil (all current posts are Portuguese)

## Conversion

- The one action that counts: TODO (e.g. newsletter signup, booked call, contact form sent)
- Named tracking event: TODO (e.g. `newsletter_signup` in PostHog or GA4). If this is blank, no page can be judged. Say so and stop.
- Where the call to action lives on each page: TODO (today: nowhere, the posts have no next step)

## Pages in scope

| URL path | Main topic | Has a next step? |
|---|---|---|
| /blog/tutorial/2022/como-configurar-wsl | WSL 2 setup (old) | no |
| /blog/tutorial/2023/configuração-do-windows-para-desenvolvimento | Windows dev setup with WSL 2 | no |
| /blog/serie/2023/tudo-que-voce-precisa-para-usar-linux | Linux basics | no |
| /blog/serie/2023/tudo-que-voce-precisa-para-usar-docker | Docker basics | no |
| /blog/serie/2023/tudo-que-voce-precisa-para-usar-terraform | Terraform basics | no |

Known overlap: the two WSL posts target the same query. Decide which one survives before measuring either.

## Rules for the agent

1. Every claim cites the URL or file it came from. Missing data is reported as missing, never guessed.
2. Recommend ONE change per week. Never bundle a title, intro and link change into one week.
3. Ignore ranking moves that last less than two weeks.
4. Never touch a page that already performs well without a strong, cited reason.
5. Judge every change on search AND conversions. Traffic without conversions is logged as a miss.
6. Never publish, push, or submit anything. Draft only. A human ships.
7. Do not edit this brief or `WEEKLY.md` during a running test.
