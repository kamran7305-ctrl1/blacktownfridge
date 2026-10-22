# Technical SEO audit: fridgerepairblacktown.com.au (22 Oct 2026)

Scope: static HTML pages plus PHP blog, GitHub Actions FTP deploy to Hostinger. Branch `claude/modest-euler-mp89t1` (nothing deployed to production by this work; deploy happens only when the PR is merged).

## A. Executive diagnosis

**Confirmed code issues (fixed in this branch)**
1. Every public blog page started a PHP session, so it sent `Set-Cookie: PHPSESSID` and `Cache-Control: no-store, no-cache` plus `Expires: 1981`. Googlebot got a cookie and a non-cacheable response on every blog URL.
2. The sitemap had no `lastmod` and no blog posts. New posts were discoverable only through `/blog/`.
3. Duplicate URLs: `/about-us`, `/about-us/` and `/about-us.html` all returned 200 (same for every landing page, and `/blog/slug/` vs `/blog/slug`). Canonical tags covered it, but redirects are stronger.
4. No `ErrorDocument`, so unknown URLs relied on the host's default 404 page.
5. `CLAUDE.md` (internal notes) was public at `/CLAUDE.md` after each deploy.
6. No pre-deploy checks, no post-deploy test, no concurrency guard in the deploy workflow.

**Plausible causes of low crawl count (not code defects)**: the site is about a month old, has Authority Score 0 and about 1 backlink, no Google Business Profile, and the sitemap was probably only just submitted. 54 crawl requests on its own is normal for a new small site and is not proof of a technical fault. Not guaranteed to change with these fixes.

**Not verified (no access)**: live HTTP responses (the sandbox proxy returns 403 for the production host), server logs, Search Console data, Googlebot verification, Cloudflare/WAF settings, whether Hostinger already forces HTTPS and www redirects.

## B. Audit table

| Issue | Severity | Evidence | Root cause | File | Fix | Test | Status |
|---|---|---|---|---|---|---|---|
| Session cookie and no-store on public blog pages | P1 | Local Apache run of the original code: `Set-Cookie: PHPSESSID`, `Cache-Control: no-store`, `Expires: 1981` on `/blog/<slug>` | `admin/config.php` always called `session_start()` | `admin/config.php`, `blog.php`, `single-post.php`, `blog-api.php`, `sitemap.php` | `SKIP_SESSION` constant, `Cache-Control: public, max-age=300` | Apache run: no Set-Cookie, cache header present | Fixed, not deployed |
| Sitemap missing lastmod and blog posts | P1 | Original `sitemap.xml`: 0 `lastmod`, 1 blog URL | Hand-edited static file | `sitemap.php` (new), `sitemap-static.xml` (renamed), `.htaccess` | Dynamic sitemap, lastmod from file time or post `updated_at`, static fallback if DB is down | DB-up run: post with lastmod 2026-10-10, draft excluded, valid XML; DB-down run: 200 with 17 static URLs | Fixed, not deployed |
| Duplicate URLs (no slash, .html, blog trailing slash) | P1 | Original: `/about-us`, `/about-us.html`, `/fridge-regas.html`, `/blog/x/` all 200 | Rewrite rules accepted every variant | `.htaccess` | 301 to the canonical form | Apache run: all variants return 301 to the canonical URL | Fixed, not deployed |
| No custom 404 handler | P2 | Unknown URL used host default | Missing `ErrorDocument` | `.htaccess` | `ErrorDocument 404 /404.php` | Apache run: `/nope/` returns 404 with branded page, `/blog/nope` 404, draft post 404 | Fixed, not deployed |
| Internal notes public | P2 | Original: `/CLAUDE.md` returned 200 | Whole repo uploaded | `deploy.yml`, `.htaccess` | Exclude from upload, deny `.md` and `.sql` | Apache run: `/CLAUDE.md` 403 | Fixed, not deployed. Delete the file already on the server (see E) |
| No pre or post deploy checks | P1 | Workflow only ran the upload | Missing jobs | `.github/workflows/deploy.yml`, `tests/` | `checks` then `deploy` then `smoke-test`, concurrency lock | `tests/seo_check.py` passes; deliberately broken page makes it fail | Fixed, runs on first merge |
| FTP is unencrypted | P2 | `protocol: ftp` | Host setting | `deploy.yml` | Not changed (might break the deploy) | n/a | Open, see E |

Checked and found fine: robots.txt (blocks only `/admin/`, `/blog-api.php`, `/send_mail.php`, has sitemap line), no accidental `noindex` (only on 404), every page has one H1, a unique title and description, correct canonical, schema parses, FAQ schema matches visible text, no orphan pages, no broken internal links (16 pages, 17 sitemap URLs), `admin/database/` already denied by its own `.htaccess`, blog pages and posts are server-rendered with real `<a href>` links.

## C. Change log

- `admin/config.php`: session only starts when `SKIP_SESSION` is not defined.
- `blog.php`, `single-post.php`, `blog-api.php`: define `SKIP_SESSION`; blog pages send `Cache-Control: public, max-age=300`.
- `sitemap.php` (new): dynamic sitemap. `sitemap.xml` renamed to `sitemap-static.xml` (editable page list, not public).
- `.htaccess` (CRLF kept): ErrorDocument 404, deny `.sql` and `.md`, `/sitemap.xml` to `sitemap.php`, `/sitemap-static.xml` 404, trailing-slash and `.html` 301s, blog slash rules.
- `tests/seo_check.py`, `tests/smoke_live.py` (new). `.github/workflows/deploy.yml`: three jobs, concurrency lock, excludes `CLAUDE.md` and `tests/`.
- `CLAUDE.md`: new section 15 and updated sitemap and deploy steps.

## D. Baseline vs corrected (measured on a local Apache 2.4 + PHP 8.3 copy, not on production)

| Check | Baseline (original code) | After |
|---|---|---|
| `/about-us`, `/about-us.html`, `/fridge-regas.html` | 200 (duplicates) | 301 to `/slug/` |
| `/blog/<slug>/` | 200 (duplicate) | 301 to `/blog/<slug>` |
| Blog response headers | Set-Cookie, no-store | no cookie, public cache |
| Sitemap lastmod / blog URLs | 0 / 1 | every URL has lastmod / posts included |
| `/CLAUDE.md` | 200 | 403 |
| Unknown URL, draft post | 404 | 404 (branded) |
| Orphan pages, broken internal links | 0, 0 | 0, 0 |
| TTFB | 1 to 4 ms locally (not representative of the host) | same |

## E. Hosting tasks for the owner

1. Hostinger hPanel > Websites > Security (or SSL) > turn on **Force HTTPS**. Then check `http://` and `https://www.` both end on `https://fridgerepairblacktown.com.au/` in one redirect. (Not forced in `.htaccess`, because a wrong rule can loop and take the site down.)
2. After the first deploy, delete `CLAUDE.md` in `public_html` using File Manager (the deploy will not remove an old upload with certainty), and delete the old `sitemap.xml` file if it is still there (the new rule overrides it anyway).
3. Ask Hostinger whether FTPS or SFTP is available. If yes, change `protocol: ftp` to `ftps` in the workflow and test.
4. If Cloudflare or a security plugin is on, make sure it does not challenge Googlebot (do not allow-list by user agent; use Cloudflare's "verified bots").

## F. Search Console checklist

1. Sitemaps: submit `https://fridgerepairblacktown.com.au/sitemap.xml`. Check status "Success" and the discovered page count (expect 17 plus blog posts).
2. URL Inspection on `/`, `/coolroom-repair/`, `/fisher-paykel-fridge-repair/`, one blog post: confirm "URL is on Google" or request indexing; check "User-declared canonical" equals "Google-selected canonical".
3. Settings > Crawl stats: note total requests, response codes (expect 200 and 301), average response time.
4. Indexing > Pages: note counts for Indexed, "Discovered, currently not indexed" and "Crawled, currently not indexed". Send screenshots of these for the next review.

## G. Monitoring

- 24 hours after deploy: GitHub Actions three green ticks; `https://.../sitemap.xml` loads with lastmod; `/about-us` redirects once; Search Console shows the sitemap as processed.
- 7 days: crawl stats show 200 and 301 only, no 5xx; new pages appear under Indexing.
- 14 days: indexed page count rising; check Google-selected canonicals match.
- 30 days: compare crawl requests and indexed pages. Crawl rate and indexing are not guaranteed to increase.

## Rollback

Everything is in separate commits on the PR. To undo: revert the PR in GitHub (Revert button on the merged PR), which restores the previous files on the next deploy. The only manual cleanup is described in E.2.

## Remaining and unverified

- Live behaviour of the new `.htaccess` rules on Hostinger's server (tested on Apache 2.4 locally; Hostinger often runs LiteSpeed, which reads the same rules, but this is unverified). The smoke-test job checks the sitemap URLs, a 404 and the `/fridge-regas` 301 after deploy.
- Homepage blog preview and the blog sidebar load via JavaScript. Posts are still linked in plain HTML on `/blog/`, so crawling is unaffected; adding a server-rendered list to the homepage is a P2 option.
- `/blog/` shows the latest 50 posts only, with no pagination. Add pagination once there are more than 50 posts.
- `about-us.html` uses `AboutPage` and a plain `Organization` type for the shared business `@id`; other pages use `HVACBusiness`. Harmless, can be aligned later.
