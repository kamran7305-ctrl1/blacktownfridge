---
name: seo-check
description: Run the repo's SEO, schema, routing and PHP syntax checks (tests/seo_check.py) and explain any failure with the exact file and fix. Use before every push or when asked to check the site.
---

Run `python3 -I tests/seo_check.py` from the repo root.

- If it passes, report the numbers it prints (pages, sitemap URLs, PHP files) in one line.
- If it fails, group the failures by file, explain the cause in plain words, fix the problem (title over 60 characters, duplicate title or description, wrong canonical, FAQ schema not matching visible text, missing sitemap entry or rewrite rule, broken link, orphan page, placeholder), then run it again.
- Do not weaken or skip a check to make it pass. If a check itself is wrong, say so and ask the owner.
- After a deploy, `python3 tests/smoke_live.py https://fridgerepairblacktown.com.au` tests the live site, but only works where the host is reachable.
