#!/usr/bin/env python3
"""Pre-deploy SEO and routing checks for the static pages (stdlib only).

Run from the repo root:  python3 tests/seo_check.py
Exits non-zero if any check fails, so GitHub Actions blocks the deploy.
"""
import glob
import html
import json
import os
import re
import subprocess
import sys
import xml.dom.minidom

BASE = "https://fridgerepairblacktown.com.au"
errors = []


def fail(msg):
    errors.append(msg)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def url_for(page):
    return BASE + "/" if page == "index.html" else f"{BASE}/{page[:-5]}/"


# --- PHP syntax -----------------------------------------------------------
php = subprocess.run(["which", "php"], capture_output=True, text=True).stdout.strip()
php_files = [p for p in glob.glob("**/*.php", recursive=True)]
if php:
    for p in php_files:
        r = subprocess.run([php, "-l", p], capture_output=True, text=True)
        if r.returncode != 0:
            fail(f"PHP syntax error in {p}: {r.stdout.strip() or r.stderr.strip()}")
else:
    print("note: php not found, skipping PHP lint")

# --- sitemap --------------------------------------------------------------
pages = sorted(glob.glob("*.html"))
try:
    xml.dom.minidom.parse("sitemap-static.xml")
except Exception as exc:  # noqa: BLE001
    fail(f"sitemap-static.xml is not valid XML: {exc}")
sitemap = read("sitemap-static.xml")
locs = re.findall(r"<loc>(.*?)</loc>", sitemap)
if len(locs) != len(set(locs)):
    fail("sitemap-static.xml has duplicate URLs")
for loc in locs:
    if not loc.startswith(BASE + "/"):
        fail(f"sitemap URL is not on the preferred https host: {loc}")
    path = loc[len(BASE):].strip("/")
    if path in ("", "blog"):
        continue
    if not os.path.exists(path + ".html"):
        fail(f"sitemap URL has no page file: {loc}")
for page in pages:
    if url_for(page) not in locs:
        fail(f"page missing from sitemap-static.xml: {page}")

# --- .htaccess routes -----------------------------------------------------
htaccess = read(".htaccess")
for page in pages:
    if page == "index.html":
        continue
    slug = page[:-5]
    if f"^{slug}/?$ {page}" not in htaccess.replace("\r", ""):
        fail(f".htaccess has no rewrite rule for /{slug}/")
for required in ("ErrorDocument 404 /404.php", "sitemap.php"):
    if required not in htaccess:
        fail(f".htaccess is missing: {required}")

# --- per-page checks ------------------------------------------------------
titles, descs = {}, {}
for page in pages:
    s = read(page)
    t = re.findall(r"<title>(.*?)</title>", s, re.S)
    d = re.findall(r'<meta name="description" content="(.*?)"', s)
    c = re.findall(r'<link rel="canonical" href="(.*?)"', s)
    if len(t) != 1:
        fail(f"{page}: expected one <title>, found {len(t)}")
        continue
    title = html.unescape(t[0].strip())
    if len(title) > 60:
        fail(f"{page}: title is {len(title)} characters (max 60)")
    if title in titles:
        fail(f"{page}: duplicate title with {titles[title]}")
    titles[title] = page
    if len(d) != 1:
        fail(f"{page}: expected one meta description, found {len(d)}")
    else:
        desc = html.unescape(d[0])
        if desc in descs:
            fail(f"{page}: duplicate meta description with {descs[desc]}")
        descs[desc] = page
    if c != [url_for(page)]:
        fail(f"{page}: canonical {c} should be [{url_for(page)}]")
    if re.search(r'<meta[^>]+name="robots"[^>]+noindex', s, re.I):
        fail(f"{page}: has noindex")
    if len(re.findall(r"<h1[ >]", s)) != 1:
        fail(f"{page}: expected exactly one <h1>")
    if re.search(r"\[(CONFIRM|PHONE|ARC)[^\]]*\]", s):
        fail(f"{page}: has an unfilled placeholder")

    m = re.search(r'ld\+json">\s*(.*?)</script>', s, re.S)
    if not m:
        fail(f"{page}: no JSON-LD schema")
        continue
    try:
        data = json.loads(m.group(1))
    except ValueError as exc:
        fail(f"{page}: JSON-LD does not parse: {exc}")
        continue
    types = [n.get("@type") for n in data.get("@graph", [])]
    if not {"WebPage", "AboutPage", "ContactPage"} & set(types):
        fail(f"{page}: schema is missing WebPage")
    if "BreadcrumbList" not in types:
        fail(f"{page}: schema is missing BreadcrumbList")
    if "Product" in types or "ItemPage" in types:
        fail(f"{page}: schema must not use Product or ItemPage")
    faq = [n for n in data["@graph"] if n.get("@type") == "FAQPage"]
    if faq:
        visible = re.findall(
            r'frb-faq-question">(.*?)</h3><div class="frb-faq-answer"><p>(.*?)</p>', s)
        entities = faq[0]["mainEntity"]
        if len(visible) != len(entities):
            fail(f"{page}: {len(entities)} FAQ in schema but {len(visible)} visible")
        for ent, (q, a) in zip(entities, visible):
            vq = html.unescape(q)
            va = html.unescape(re.sub(r"<[^>]+>", "", a)).strip()
            if ent["name"] != vq or ent["acceptedAnswer"]["text"].strip() != va:
                fail(f"{page}: FAQ schema does not match visible text: {vq[:50]}")

# --- internal links -------------------------------------------------------
inbound = {url_for(p): 0 for p in pages}
inbound[BASE + "/blog/"] = 0
for src in pages + ["blog.php", "single-post.php", "404.php"]:
    s = read(src)
    for href in re.findall(r'href="(/[^"#?]*)"', s):
        full = BASE + href
        if full in inbound and src != "404.php":
            inbound[full] += 1
        path = href.strip("/")
        known = (
            href == "/" or path.startswith(("images", "admin", "blog"))
            or os.path.exists(path + ".html") or os.path.exists(path + ".php")
            or os.path.exists(path)
        )
        if not known:
            fail(f"{src}: broken internal link {href}")
for loc, n in inbound.items():
    if n == 0:
        fail(f"orphan page, no internal links point to {loc}")

# --- deployment safety ----------------------------------------------------
wf = read(".github/workflows/deploy.yml")
for need in ("CLAUDE.md", "tests/", "sitemap-static.xml"):
    if need == "sitemap-static.xml":
        continue
    if need not in wf:
        fail(f"deploy.yml should exclude {need} from the FTP upload")

if errors:
    print(f"SEO check failed: {len(errors)} problem(s)")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"SEO check passed: {len(pages)} pages, {len(locs)} sitemap URLs, {len(php_files)} PHP files")
