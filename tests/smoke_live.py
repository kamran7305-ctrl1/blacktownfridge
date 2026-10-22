#!/usr/bin/env python3
"""Post-deploy smoke test against the live site (stdlib only).

Usage: python3 tests/smoke_live.py [base_url]
Checks the sitemap and every URL in it return 200, robots.txt is reachable,
and an unknown URL returns a real 404. Exits non-zero on any failure.
"""
import re
import sys
import urllib.error
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://fridgerepairblacktown.com.au").rstrip("/")
failures = []


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


opener = urllib.request.build_opener(NoRedirect)


def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "frb-smoke-test"})
    try:
        with opener.open(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), dict(e.headers)


status, body, hdr = get("/sitemap.xml")
if status != 200 or "<urlset" not in body:
    failures.append(f"/sitemap.xml returned {status}")
    urls = []
else:
    urls = re.findall(r"<loc>(.*?)</loc>", body)
    print(f"sitemap has {len(urls)} URLs")
for u in urls:
    path = u[len("https://fridgerepairblacktown.com.au"):] or "/"
    code, _, _ = get(path)
    print(code, path)
    if code != 200:
        failures.append(f"{path} returned {code}")
code, _, _ = get("/robots.txt")
if code != 200:
    failures.append(f"/robots.txt returned {code}")
code, _, _ = get("/this-page-should-not-exist-smoke/")
if code != 404:
    failures.append(f"unknown URL returned {code}, expected 404")
code, _, h = get("/fridge-regas")
if code != 301:
    failures.append(f"/fridge-regas should 301 to the slash URL, got {code}")

if failures:
    print("SMOKE TEST FAILED")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("smoke test passed")
