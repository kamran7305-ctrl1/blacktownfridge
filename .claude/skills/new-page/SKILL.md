---
name: new-page
description: Build or update the next page from the Semrush page map for fridgerepairblacktown.com.au, wire it into .htaccess, sitemap-static.xml, menus and footers, run the SEO checks and open the PR. Use when the owner says "next page" or names a page.
disable-model-invocation: true
argument-hint: "[page URL, for example /electrolux-fridge-repair/] (optional)"
---

# New page workflow

Follow `CLAUDE.md` sections 1, 6, 7, 8, 9, 13, 14 and 15. Do not ask the owner to repeat rules.

1. **Find the page.** Use the URL in `$ARGUMENTS`, or the next page in `.github/seo/page-map.csv` order (skip pages that already exist on `Main`). Read its row: status (EXISTING optimise or NEW), primary and secondary keywords, title, H1, word count. Read the matching rows in `.github/seo/keywords.csv`.
2. **Sync.** `git fetch origin`. If the designated branch's earlier PR is merged, reset the branch to `origin/Main`; if it is still open, stack on it. Never push to `Main`.
3. **Existing page:** update title, meta description, H1, copy, FAQs, links and schema in place. **New page:** build with `.claude/skills/new-page/build.py` (copy it next to the repo root or add it to `sys.path`; run from the repo root).
4. **Write unique content.** Unique title (60 characters or fewer), description (140 to 165), H1, 10 FAQs. Use only confirmed facts from `CLAUDE.md` section 1. Write "from $69" and "up to 12 months". No em dashes, no phone number, no ARC, no authorised-agent claims, no invented prices, error codes or reviews. List unconfirmed assumptions for the owner at the end of the reply.
5. **Wire it in** (new pages): `wire(slug, label, ...)` adds the `.htaccess` rule (CRLF kept) and the `sitemap-static.xml` entry, and the menu and footer links. Repoint matching `#brands` or `#services` footer links to the new page.
6. **Verify.** `python3 tests/seo_check.py` must pass. Check the page at 1366 px and 390 px (no console errors). Never edit a static `sitemap.xml`.
7. **Ship.** Commit with the attribution lines from the session, push, open (or update) the PR against `Main`, give the owner the link, and remind them to merge and check the three green ticks in Actions.
8. **Report** in short bullets: meta lengths, what was built, what needs confirming. Reply in short plain English or Roman Urdu as the owner writes.
