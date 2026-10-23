#!/usr/bin/env python3
"""PostToolUse hook for Edit/Write: run tests/seo_check.py after a page edit.

Only runs when a root-level page, .htaccess or sitemap-static.xml changed. If
the check fails, the output is sent back to Claude (exit code 2) so it fixes
the problem before moving on. Note: during a multi-step build the check may
fail until all files are updated; that is expected and not a blocker.
"""
import json
import os
import subprocess
import sys

try:
    data = json.load(sys.stdin)
except ValueError:
    sys.exit(0)

path = (data.get("tool_input") or {}).get("file_path", "")
root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
rel = os.path.relpath(path, root).replace(os.sep, "/") if path else ""
watched = rel in (".htaccess", "sitemap-static.xml") or (rel.endswith(".html") and "/" not in rel)
if not watched or not os.path.exists(os.path.join(root, "tests", "seo_check.py")):
    sys.exit(0)

result = subprocess.run([sys.executable, "-I", "tests/seo_check.py"], cwd=root, capture_output=True, text=True, timeout=120)
if result.returncode != 0:
    sys.stderr.write(result.stdout + result.stderr)
    sys.exit(2)
sys.exit(0)
