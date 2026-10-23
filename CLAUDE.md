# CLAUDE.md: fridgerepairblacktown.com.au (complete project brief)

Put this file in the root of the repo (`kamran7305-ctrl1/blacktownfridge`) and Claude Code will read it every session. It explains the business, the SEO plan, the code, the design system, the content rules and the exact steps to build a page and put it live. Follow it without asking the owner to repeat anything.

Owner quick note (Roman Urdu): Claude Code ko sirf page ka naam, URL, primary keyword aur secondary keywords do. Baqi sab (competitor research, content, meta, schema, internal links, design, sitemap, .htaccess, branch, pull request) is file ke mutabiq Claude Code khud karega. Merge aap karoge, phir Actions tab mein green tick dekho.

---

## 1. The business

- **Site:** https://fridgerepairblacktown.com.au
- **Business:** Fridge Repairs Blacktown. A local fridge, freezer and coolroom repair business in Blacktown NSW 2148, servicing Western Sydney. Mobile service: technicians come to the customer's home or business.
- **Goal of the site:** rank for fridge repair keywords in and around Blacktown and turn visitors into booking requests (form or email). The domain is exact-match for one suburb, so the site stays small, focused and locally deep.
- **Confirmed business facts (use these, nothing else):**
  - Call-out fee from $69 (covers the visit and diagnosis). Always write "from $69", never a flat "$69"
  - Warranty of up to 12 months on parts and labour. Always write "up to 12 months", never "1 year"
  - Around 30 years of experience
  - Fully trained and licensed technicians, with public liability insurance
  - Senior discounts available
  - Same-day service where available
  - Upfront quote before work starts; the customer approves the price first
  - Emergency service 24 hours, 7 days (nights, weekends, Sundays, public holidays)
  - Services: residential, commercial, emergency, freezer, coolroom, regas and compressor, fault diagnosis
  - Owner confirmed on 20 Oct 2026 (safe to use in copy): we are an independent repairer, not a Fisher & Paykel service centre, and repair all Fisher & Paykel ranges listed on the brand page; we repair camping and 12V fridges; we repair ice machines and ice makers, including servicing; the call-out fee stays the same at any hour; we repair walk-in coolrooms and freezer rooms including compressors and condensing units, and offer coolroom maintenance schedules; commercial brands Skope, Bromic, Williams, Husky, True, Electrolux Professional and Westinghouse.
- **Contact:** the booking form (`/#contact-form`, posts to `/send_mail.php`) and **info@fridgerepairblacktown.com.au**. There is no published phone number, street address, licence number, review count or rating. Do not invent any. Do not write `[PHONE]` or other placeholders on live pages.
- **Never mention ARC or ARCtick.** Say "licensed" or "fully trained and licensed" only.

## 2. Hosting, repo and deploy

- Repo: `kamran7305-ctrl1/blacktownfridge`. Live branch: **`Main`** (capital M, default).
- Merging to `Main` runs GitHub Actions "Deploy to Hostinger (FTP)" (`.github/workflows/deploy.yml`). Three jobs run in order: `checks` (`python3 tests/seo_check.py`: PHP syntax, unique titles and descriptions, canonicals, schema, FAQ match, links, sitemap), `deploy` (SamKirkland FTP-Deploy-Action uploads the repo to `public_html`, excluding `.github`, `tests`, `CLAUDE.md` and `README.md`) and `smoke-test` (`tests/smoke_live.py` fetches every sitemap URL on the live site). If `checks` fails, nothing is deployed. Run `python3 tests/seo_check.py` before every push.
- FTP credentials are GitHub Secrets (`FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`). Never write them in chat, files or commits.
- **Rules:**
  1. Never push to `Main` directly.
  2. For every task create a branch `claude/<task-name>` from an up-to-date `Main`, commit there.
  3. When the work is done, always open a Pull Request **against `Main`** (a PR against any other branch does not publish the site).
  4. End every task by giving the owner the PR link and telling them to merge it, then open the Actions tab and wait for the green tick on all three jobs (checks, deploy, smoke-test), then check the live URL and `/sitemap.xml`.
  5. Commit messages end with the attribution lines the session tells you to use.

## 3. Repo structure (static HTML and PHP at the root, no framework)

```
index.html                          homepage (design system source of truth, about 120 KB)
about-us.html                       /about-us/
commercial-fridge-repair-blacktown.html   /commercial-fridge-repair-blacktown/
emergency-fridge-repair.html        /emergency-fridge-repair/
freezer-repair-blacktown.html       /freezer-repair-blacktown/   <- best template for new pages
blog.php                            /blog/  (blog list, reads blog-api.php)
single-post.php                     /blog/<slug>  (single post, adds BlogPosting + BreadcrumbList schema)
404.php                             404 page (full header and footer)
blog-api.php                        public JSON endpoint for published posts (MySQL)
send_mail.php                       contact form handler (POST: name, email, country_code, phone, message)
sitemap.php  sitemap-static.xml  robots.txt  .htaccess
tests/                              seo_check.py (runs before every deploy), smoke_live.py (runs after deploy)
images/                             logo.webp, heroimage1.png, blacktown.webp, blacktownImage.webp,
                                    bookyourblacktownfridge.webp, emergency.jpeg, emergencyimage.webp, show1-5.jpeg
admin/                              PHP + MySQL admin (gallery, blog posts, testimonials). See admin/README.md
.github/workflows/deploy.yml        FTP deploy on push to Main
```

- Pages are named `<slug>.html` at the root. Clean URLs are made with one `RewriteRule` per page in `.htaccess`:
  `RewriteRule ^fridge-regas/?$ fridge-regas.html [L]`
- `.htaccess` and `index.html` use **CRLF** line endings. Every other file uses LF. When scripting edits, open and write with `newline=''` (Python) so line endings are preserved, and check `git diff --stat` shows only a few changed lines per file, not a whole-file rewrite.
- The blog is database-driven: posts are written in `/admin/` and served through `blog-api.php`; clean URLs `/blog/<slug>` rewrite to `single-post.php?post=<slug>`. A blog post is therefore content entered in the admin, not a new file (see section 9).
- The old WordPress CMS at `/cms/` is no longer used.

## 4. Site map and status

Live on `Main` (in sitemap.xml):
`/`, `/about-us/`, `/blog/`, `/commercial-fridge-repair-blacktown/`, `/freezer-repair-blacktown/`, `/emergency-fridge-repair/`.

Built and waiting to be pushed (the owner has the files; check whether they exist on `Main` before linking to them):
- `/residential-fridge-repair/` (`residential-fridge-repair.html`)
- `/fridge-not-cooling-repair/` (`fridge-not-cooling-repair.html`)
- `/fridge-regas/` (`fridge-regas.html`)

Still to build (the full 58 new page plan and publish order is in section 13, which overrides this short list):
- Contact page (separate page; the homepage has a contact form section)
- Coolroom repair
- Fridge leaking water (fault page)
- Freezer not freezing (fault page)
- Brands hub `/brands-we-repair/` (one H2 per brand)
- Blog: update the 2 existing posts, then 4 new posts (weeks 3, 5, 6, 8) and a backlog of 8 more.
- Suburb pages ARE planned (40, see section 13). Build them only from the suburb plan and only with unique local content.

Internal link targets (use these exact paths): `/`, `/#contact-form`, `/#services`, `/#brands`, `/about-us/`, `/blog/`, `/residential-fridge-repair/`, `/fridge-not-cooling-repair/`, `/fridge-regas/`, `/freezer-repair-blacktown/`, `/commercial-fridge-repair-blacktown/`, `/emergency-fridge-repair/`.

## 5. Design system (match it exactly)

Every page carries the same inline `<style>` block from `index.html` (global `frb-` classes) plus Google Fonts Montserrat and Font Awesome 6.4. Do not invent new styles; reuse the classes.

- **Colours:** `--primary #0F3D81`, `--primary-dark #0A2959`, `--primary-light #EBF1F8`, `--secondary #E63946` (red, buttons and accents), `--secondary-dark #C1121F`, `--text-dark #1E293B`, `--text-light #64748B`, `--bg-light #F8FAFC`, `--white`. Radius 16px (`--radius`) and 8px (`--radius-sm`). Font: Montserrat.
- **Page structure of a service or fault page:**
  1. `frb-global-styles` wrapper, `frb-site-header` (logo, nav with a Services dropdown, "Book Now" button, mobile toggle)
  2. `frb-page-banner` with the H1 and a short intro paragraph (blue gradient over `/images/blacktown.webp`)
  3. Intro block (`frb-intro-block`) with Email Us and Book buttons and a `frb-check-list`
  4. Alternating sections: `frb-container frb-reveal` (white) and `frb-bg-light` (grey), each starting with `<h2 class="frb-section-title center frb-text-center">`
  5. `frb-cta-section` closing call to action
  6. `frb-footer` (4 columns) and the sticky mobile book button, success modal and the page script
- **Reusable components:** `frb-faults-grid` + `frb-fault-card` (icon, title, one line), `frb-article-block` (long text with h3s), `frb-check-list` (ticks; add `left` to left-align), `frb-numbered-list` (ol), `frb-table-wrapper` + `frb-compare-table`, `frb-process-grid` + `frb-process-step` + `frb-step-num` (steps), `frb-tag-grid` + `frb-tag-item` (suburb and brand chips), `frb-faq-item` + `frb-faq-question` (h3) + `frb-faq-answer`, `frb-btn` and `frb-btn-outline`, `frb-reveal` (scroll fade-in).
- **Responsive:** the CSS is already mobile first with breakpoints. Pages must work on mobile, tablet and desktop. Test at 1366 px and 390 px wide with Playwright and confirm no horizontal scroll and no console errors. In a sandbox the Google Fonts and Font Awesome CDNs may be blocked, which makes icons vanish in screenshots only. That is not a page bug.
- **Fastest correct way to build a page:** copy `freezer-repair-blacktown.html` (from `Main`), keep everything from `<!DOCTYPE html>` down to and including `</header>` and everything from `<!-- FOOTER -->` to the end, and replace only (a) the `<title>`, meta description, canonical and JSON-LD block and (b) the body between `<!-- PAGE BANNER / H1 -->` and `<!-- FOOTER -->`. A small Python generator that does this is the least error-prone method. Beware Python f-strings: expressions cannot contain backslashes.

## 6. Content standard (apply to every page and blog, without being asked)

1. **Research first.** Analyse the top 10 competitors for the primary keyword across Australia, Sydney and Blacktown. Fetch the real pages and note word count, headings, fridge types, causes, prices, warranty, FAQs, schema and weaknesses. WebSearch skews to US results, so say ranking positions are unverified and tell the owner to check Semrush (AU). Never invent rankings.
   - Known top competitors (Sept 2026): Master Fridge Repairs, Fridge Experts, Fast Fridge Repairs, Commercial Fridge Repairs, Fridge Repair Experts, Ace Fridge Repairs (acefridgerepairs.sydney), AJ & T Appliances (Prospect), Hanna Refrigeration Services (Blacktown), Fridges R Us Blacktown, Parrahills Appliance Repairs. Aggregators on page 1: Airtasker, Oneflare, Yelp, TrueLocal, Whereis.
   - Recurring competitor weaknesses to beat: no prices or call-out fee, inconsistent warranty wording, contradictory hours (24/7 beside 7am to 7pm), vague "same-day" claims, thin or keyword-stuffed copy, no FAQs, missing fault explanations (beeping, light on but not cooling, warm fridge with cold freezer), integrated, built-in, double door and camping fridges ignored, templated suburb pages, copy and template errors.
2. **Better content.** Complete, unique, semantically optimised copy that answers the searcher quickly. Use the primary and every secondary keyword naturally (H1, intro, H2/H3, table, FAQs, areas) with related terms and entities. No keyword stuffing.
3. **Human voice.** Plain, specific and direct. No AI markers or filler phrases, no em dashes, no hype words, no generic reassurance. Short paragraphs, scannable headings.
4. **Standard sections** for a service or fault page: warning signs grid, what we fix or what causes it, symptom to cause to repair table, quick checks before you call, food safety, repair or replace and cost guidance (state the $69 call-out and what affects price; do not invent price ranges), how it works (6 steps), areas, brands, why choose us, 10 to 12 FAQs, strong CTA.
5. **Food safety wording:** fridge 3 to 5 degrees C, freezer -18 degrees C. Cold food above 5 degrees C for under 2 hours can go back in or be used; 2 to 4 hours use straight away; over 4 hours throw out. When in doubt, throw it out. Refer to the NSW Food Authority.
6. **Honesty:** flag any claim that is an assumption (for example brands serviced, fridge types, refrigerant types) for the owner to confirm. Never promise what the business has not confirmed.
7. **Areas list (use consistently):** Blacktown, Seven Hills, Prospect, Doonside, Rooty Hill, Mount Druitt, Marayong, Quakers Hill, Kings Park, Lalor Park, Kings Langley, Toongabbie, Riverstone, Schofields, Rouse Hill, The Ponds, Glenwood, Woodcroft, Glendenning, Plumpton, St Marys, Penrith, Parramatta, Westmead, Wetherill Park, Castle Hill, Baulkham Hills, Liverpool. The strategy also cares about Arndell Park, Huntingwood and Eastern Creek (industrial zones, good for commercial and coolroom pages) and Marsden Park, Box Hill, Tallawong (growth suburbs).
8. **Brands list:** Westinghouse, Electrolux, Fisher & Paykel, LG, Samsung, Bosch, Haier, Hisense, Beko, Kelvinator, Mitsubishi, Panasonic, Whirlpool, Miele, Liebherr, Smeg; add Skope, Bromic, True, Williams and Husky on commercial pages.

## 7. Meta and schema

- **Meta title:** 60 characters or fewer. Click-worthy: primary keyword, a benefit or differentiator, the $69 call-out. Example: `Fridge Regas Blacktown | Leak Found & Fixed | From $69`. Count characters in code.
- **Meta description:** about 150 to 160 characters. Primary keyword, benefit, from $69 call-out or up to 12 months warranty, and a CTA ("Book now"). Count characters.
- Also: `<link rel="canonical">` (absolute, trailing slash), `robots index, follow, max-image-preview:large`, favicon `/images/logo.webp`.
- **JSON-LD** (one block in the head): `@graph` with `WebPage`, the site-wide `HVACBusiness` node (`@id` `https://fridgerepairblacktown.com.au/#organization`: name, url, logo, email, priceRange `$$`, areaServed, 24/7 openingHoursSpecification; **no telephone, no address, no geo, no rating**), `Service` (name, serviceType, provider by @id, areaServed, description, url, `Offer` with a $69 AUD `PriceSpecification` (describe it as "from $69")), `BreadcrumbList`, `FAQPage`. FAQ text in the schema must match the visible FAQs word for word. Easiest: copy the node and shapes from `freezer-repair-blacktown.html` and edit. Validate that the JSON parses. Blog posts get `BlogPosting` and `BreadcrumbList` automatically from `single-post.php`.
- Do not add reviews or aggregate ratings until real reviews are shown on the page.

## 8. Internal linking and navigation

- Every new page links contextually to the 3 to 6 most related pages (inline links in the body plus the "Related" line in the final CTA) and to `/#contact-form`.
- Add the new page to the **Services dropdown** (`frb-dropdown-menu`) and the **footer "Our Services" list** on every page: `index.html`, `about-us.html`, `commercial-fridge-repair-blacktown.html`, `emergency-fridge-repair.html`, `freezer-repair-blacktown.html`, `404.php`, `blog.php`, `single-post.php` and every other page already in the repo. The dropdown item looks like `<li><a href="/slug/">Label</a></li>`. Footer items that point to `/#services` (for example "Fridge Regassing", "Home Fridge Repairs") should be repointed to the real page once it exists.
- Link back from related existing pages to the new page where it makes sense.
- Only link to pages that exist. Check before you link; remove links to pages that are not on the branch yet.

## 9. Step by step: add a new page and make it live

1. Get the page name, URL, primary keyword and secondary keywords from the owner.
2. Do the competitor research (section 6) and write the content (human, unique, semantic).
3. `git checkout Main && git pull && git checkout -b claude/<task-name>`.
4. Build `<slug>.html` from the template method in section 5, with meta and JSON-LD from section 7.
5. Add the `.htaccess` RewriteRule (keep CRLF). Add the URL to `sitemap-static.xml` (same format as the others: `<changefreq>monthly</changefreq>`, `<priority>0.8</priority>`). `/sitemap.xml` is generated from that file by `sitemap.php`, which adds `lastmod` and the published blog posts. Never edit or recreate a static `sitemap.xml`.
6. Add the menu and footer links on every page (section 8), preserving line endings.
7. Verify: page renders at 1366 px and 390 px with no console errors and no horizontal scroll; JSON-LD parses and FAQ schema matches visible FAQs; no em dashes, no "ARC", no `[PLACEHOLDER]`; sitemap parses as XML; all internal hrefs resolve to existing files or routes.
8. Commit, push the branch, open a PR **against `Main`**, give the owner the PR link, and remind them to merge and check the Actions tab green tick and the live URL.
9. Also deliver (when the owner asks for documents): a Word file with competitor analysis, SEO setup (meta, keyword map), the page content and the schema.

**Blog posts:** these are created in `/admin/blog_form.php` (title, slug, excerpt, HTML content, featured image, meta description, draft or published). Write the post as clean HTML (h2/h3, lists, tables, internal links) following the same content standard, and give the owner the title, slug, meta description, excerpt and the HTML body to paste. Published posts appear at `/blog/<slug>` automatically.

## 10. Known issues to confirm with the owner (do not fix silently)

- `send_mail.php` sends quote requests to **info@fastfridgerepairs.com.au**, which looks like another business's domain. The site's own address is info@fridgerepairblacktown.com.au. Ask the owner which is correct before changing it.
- (Resolved 19 Oct 2026) ARC placeholders and wording were removed from the commercial and freezer pages. `tests/seo_check.py` now fails on unfilled `[CONFIRM]`, `[PHONE]` and `[ARC]` placeholders.
- `heroimageMob.webp` and `heroimageTab.webp` are referenced by `index.html` but are not in `images/`.
- `admin/config.php` has placeholder database credentials and the seeded admin login must be changed on the live server. Never commit real credentials.
- Phone number, street address, ARC or licence number, reviews and Google Business Profile details are not yet published. Ask the owner before adding any of them to the site or the schema.

## 11. Project documents (in the Claude project "fridgerepairblacktown.com.au")

- `claude/seo-strategy-2-months-summary.md`: the older lean 2 month plan. SUPERSEDED by section 13 (it said no suburb pages).
- `claude/keyword-list-v1.csv`: 558 keywords in 11 clusters (the owner is running them through Semrush AU).
- `claude/competitor-analysis-summary.md`: top 10 competitors and the gaps listed above.
- Page briefs already written as Word files for the owner: commercial, emergency, freezer, residential, fridge not cooling, fridge regas, homepage, about, contact and blog posts.

## 12. Working style with the owner

- The owner writes short Roman Urdu or English requests such as "page name, page type, url, primary keyword, secondary keyword, from competitor". That is the whole brief. Do the research and build the page; do not ask them to repeat the standard rules.
- Replies: short, plain English, results first. "Today's task" summaries are 2 to 3 short bullets, one point per task or page.
- If a push fails with a 403 from the git proxy, do not look for a workaround. Give the owner a zip of the changed files and ask them to authorise the repo.
- Never use `pkill -f` with a pattern that matches your own shell.

## 13. Semrush keyword strategy v2 (16 Oct 2026): follow this for all page work

Source files are in the repo at `.github/seo/` (not deployed to the website): `SEO_Keyword_Strategy_Semrush_v2.xlsx` plus CSV exports `page-map.csv`, `suburb-pages.csv`, `keywords.csv`, `action-plan.csv`. Read the matching row before working on any page. This section overrides the older "no suburb pages" plan.

**How to work, one page at a time, in the order of the Page Map and the 8-Week Action Plan (starts Mon 19 Oct 2026):**
1. Find the page's row in `page-map.csv`: status (EXISTING - optimise, or NEW), URL, primary keyword, secondary keywords, title tag, H1, word count.
2. EXISTING page: update it in place (title, meta description, H1, copy, FAQ, internal links, schema). NEW page: build it from the template method in section 5.
3. **Every page gets its own unique content, unique meta title and unique meta description.** Never reuse or lightly reword another page's copy or meta. Use the sheet's title and H1 as the starting point, check the length (title 60 characters or fewer, description about 150 to 160) and make sure no two pages share a title or description.
4. **Schema on every page, always** (WebPage, HVACBusiness, Service with the $69 AUD Offer, BreadcrumbList, FAQPage; BlogPosting for blog posts). FAQ schema must match the visible FAQs word for word. Validate the JSON before pushing.
5. Add the page to `.htaccess`, `sitemap.xml`, the Services dropdown and footer on every page, as in sections 8 and 9. Branch and PR rules in section 2 apply.

**Page types in the plan (58 new pages):** service pages (ice machine, coolroom, mobile fridge repair, fridge repair cost, compressor, door seal, display fridge, bar fridge, Sydney hub), brand pages (Fisher & Paykel is the biggest opportunity at about 3,600 searches a month, then Westinghouse, LG, Samsung, Electrolux, Miele, Smeg), a `/service-areas/` hub, a Contact page, and suburb pages.
Do not claim "authorised service agent" for any brand unless the owner confirms it. Do not invent prices; the `/fridge-repair-cost/` page waits for real prices from the owner.

**Suburb pages (40, tiers 1 to 3 plus Extended, URL `/fridge-repair-<suburb>/`):** use `suburb-pages.csv` for URL, postcode and publish week. Each page needs:
- real suburb details (postcode, 3 to 5 nearby streets, landmarks or shopping centre, typical local housing), from the owner's real jobs, not guesses; ask the owner for anything you cannot verify
- at least 2 real jobs done in that suburb (fault, brand, fix) and a local photo with the suburb in the alt text, plus a real review when available
- its own 3 to 5 FAQs that differ per suburb (travel time, same-day availability, call-out fee, common brands there), a map, and the booking form above the fold
- internal links to the 3 most relevant service pages, 2 brand pages, `/service-areas/` and 2 neighbouring suburb pages; link it from `/service-areas/` and the homepage areas section
- never copy a page and swap the suburb name; no thin or doorway pages. After 8 weeks, merge or noindex any suburb page with zero Search Console impressions.
- Extended suburbs (Penrith, Parramatta, Castle Hill, Richmond, Campbelltown, Bankstown, Bossley Park, St Marys, Smithfield) go live only after the owner confirms the business services them.
- Build the suburb template and one data sheet per suburb first (week 1 task), then publish by tier and week.

**Honesty and data limits:** volumes are Semrush AU estimates, desktop, directional only. Validate with Google Search Console after 4 to 6 weeks. Most Blacktown suburbs show under 10 searches a month; they are built for local relevance and Map Pack proximity.

**Homepage status:** page 1 (`/`) was optimised on 16 Oct 2026 (title, H1, WebPage and Service schema added, placeholders and unverified reviews removed). Next in line: `/commercial-fridge-repair-blacktown/`, `/residential-fridge-repair/`, `/fisher-paykel-fridge-repair/`, `/emergency-fridge-repair/`.

## 14. Competitor analysis and content playbook (20 Oct 2026): follow this together with section 13

Full file: `.github/seo/Competitor_Analysis_and_Content_Playbook.md` (Part A analysis of fastfridgerepairs.com.au, Part B writing, linking and schema rules). Read Part B before writing or editing any page. Key rules adopted:

- **Voice:** Australian English, answer first, short sentences, symptom to cause to what we check to fix to cost and time. Honest repair or replace advice. Avoid the words "genuinely", "honestly" and "straightforward", hedged filler, "100% guaranteed", "best price", exclamation marks and emoji.
- **Local proof:** every page needs at least one thing the competitor lacks (price or time indicator, decision aid, real photo with descriptive alt text, named technician, or a local fact). Suburb pages need 5 verified local facts and no more than 30 percent text shared with other suburb pages.
- **Meta:** title 60 characters or fewer (aim 52 to 58), primary keyword first, no emoji. Description 140 to 155 characters with a call to action.
- **Headings:** one H1 with keyword and location, no skipped levels, FAQ questions are H3 under an H2.
- **Links:** hub and spoke. Contextual links 5 to 10 per page with descriptive, varied anchors (no "click here"), no `#anchor` pseudo-links in menus or footers, no links to pages that do not exist, add each new page to the sitemap and navigation in one pass.
- **Schema:** never use `Product` or `ItemPage` for services. Add `telephone`, address and `geo` only after the owner confirms them. Add `aggregateRating` or `review` only when real reviews are visible on the same page.
- **Scope:** only fridges, freezers, coolrooms, display, prep and bar fridges, ice machines, regas, controllers and seals. No exhaust, air conditioning or washing machines.
- **Missing facts:** never invent. List `[CONFIRM: ...]` items for the owner at the end of the reply, never inside published copy.
- **Priority order for the next 30 days (playbook B11):** homepage basics, coolroom, commercial freezer and display fridge pages, regas rewrite with prices and freezer regas, suburb pages (Mount Druitt, Seven Hills, Quakers Hill, Rouse Hill, Rooty Hill, Doonside, Schofields, Parklea, Toongabbie, Glenwood) then the `/areas/` hub, brand pages (Samsung, LG, Westinghouse, upgrade Fisher & Paykel), then blog posts (leaking water, regas cost, upgrade the not-cooling post).

**Where the playbook and this file differ, this file wins until the owner says otherwise:** the playbook allows naming ARCtick and a licence number, but section 1 says never mention ARC. The playbook says to confirm "30 years", "licensed" and "OEM parts" first; section 1 already lists years and licensed technicians as confirmed, so use them, and avoid claiming OEM or genuine parts.

**Open owner items from the playbook:** phone number, ABN, licence number, street address or service-area setting, real reviews, named technicians, real job photos, and Google Business Profile details.

## 15. Technical SEO rules (22 Oct 2026 audit): do not undo

Full report: `.github/seo/Technical_SEO_Audit_2026-10-22.md`. Rules that came out of it:

- **One URL per page.** Landing pages live at `/slug/` with a trailing slash. `.htaccess` 301-redirects `/slug` and `/slug.html` to `/slug/`. Blog posts live at `/blog/slug` with no trailing slash (`/blog/slug/` redirects to it). Canonical tags, the sitemap and internal links must always use these forms.
- **Real 404s.** `ErrorDocument 404 /404.php` is set and `404.php` sends a 404 status. Never turn a missing page into a 200 or a redirect to the homepage.
- **Public PHP pages must not start a session.** `blog.php`, `single-post.php`, `blog-api.php` and `sitemap.php` define `SKIP_SESSION` before requiring `admin/config.php`. Without it, PHP sends a `PHPSESSID` cookie and `Cache-Control: no-store` on every public page. Do the same for any new public PHP page. Only admin pages should use sessions.
- **Sitemap.** `sitemap.php` serves `/sitemap.xml` and falls back to the static pages if the database is down. `sitemap-static.xml` is not public. Add new pages there.
- **Nothing private on the web root.** `.sql` and `.md` files are denied in `.htaccess`, and `CLAUDE.md`, `tests/` and `.github/` are not uploaded. Never commit credentials.
- **Hosting tasks only the owner can do** (Hostinger hPanel): turn on Force HTTPS, confirm `www` redirects to the non-www domain, and in Search Console submit `https://fridgerepairblacktown.com.au/sitemap.xml`.

## 16. Claude Code automations (22 Oct 2026)

Project setup lives in `.claude/` and `.mcp.json` (excluded from the website upload):

- **Skill `/new-page [url]`** (`.claude/skills/new-page/`): the full next-page workflow, with `build.py`, the page generator and the `.htaccess`, sitemap, menu and footer wiring. User-invoked only.
- **Skill `/seo-check`**: runs `tests/seo_check.py` and fixes failures.
- **Subagent `seo-reviewer`** (`.claude/agents/`): independent review of a page against sections 1, 6, 7, 14 and 15 before the PR. Use it after building a page.
- **Hooks** (`.claude/settings.json`): `protect_files.py` denies edits to `sitemap.xml` and asks before `admin/config.php` or `send_mail.php`; `run_seo_check.py` runs the SEO check after an edit to a root page, `.htaccess` or `sitemap-static.xml` and returns failures to Claude. Hooks fire on Edit and Write only, not on scripts run through Bash, so still run `python3 tests/seo_check.py` before every push. During a multi-file build the check can fail until every file is updated; finish the build, then fix anything left.
- **MCP `playwright`** (`.mcp.json`): browser checks at 1366 px and 390 px. Needs `npx` and a browser on the machine; not tested in this cloud session.
