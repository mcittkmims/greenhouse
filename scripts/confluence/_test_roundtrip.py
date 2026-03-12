#!/usr/bin/env python3
"""Round-trip test: fetch WP5.1 HTML → GCM → HTML, diff against original."""
import sys
from pathlib import Path
from difflib import unified_diff

sys.path.insert(0, str(Path(__file__).parent))
from gcm_from_html import html_to_gcm
from gcm_to_html import gcm_to_html

ROOT = Path(__file__).resolve().parent.parent.parent

# Load credentials
env = {}
for line in (ROOT / ".env").read_text().splitlines():
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip()

import requests

base = env.get("CONFLUENCE_URL", "http://confluence.microlab.club")
auth = (env["CONFLUENCE_USER"], env["CONFLUENCE_PASS"])

# 1. Fetch original HTML from Confluence
print("Fetching WP5.1 from Confluence...")
resp = requests.get(
    f"{base}/rest/api/content/42634147?expand=body.storage,version",
    auth=auth, timeout=30
)
resp.raise_for_status()
data = resp.json()
original_html = data["body"]["storage"]["value"]
title = data["title"]
version = str(data["version"]["number"])
print(f"  Title: {title!r}  version={version}  len={len(original_html)}")

# 2. HTML → GCM (full text with frontmatter)
gcm_text = html_to_gcm(original_html, title=title, page_id="42634147",
                        version=version, source_url="test")
print(f"  GCM length: {len(gcm_text)} chars")

# 3. GCM → HTML  (pass full GCM text incl. frontmatter; returns (html, meta))
round_tripped_html, _meta = gcm_to_html(gcm_text)
print(f"  Round-tripped HTML length: {len(round_tripped_html)} chars")

# 4. Diff
orig_lines = original_html.splitlines(keepends=True)
rt_lines   = round_tripped_html.splitlines(keepends=True)
diff = list(unified_diff(orig_lines, rt_lines, fromfile="original", tofile="round-tripped", n=2))

SAVE_DIR = ROOT / "scripts" / "confluence" / "_rt_tmp"
SAVE_DIR.mkdir(exist_ok=True)
(SAVE_DIR / "original.html").write_text(original_html)
(SAVE_DIR / "roundtrip.html").write_text(round_tripped_html)
(SAVE_DIR / "page.gcm").write_text(gcm_text)
print(f"  Files saved to scripts/confluence/_rt_tmp/")

if diff:
    added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
    (SAVE_DIR / "diff.txt").write_text("".join(diff))
    print(f"\nDIFF found — {len(diff)} diff lines (+{added} added / -{removed} removed)")
    print("Diff written to scripts/confluence/_rt_tmp/diff.txt")
else:
    print("\nPERFECT ROUND-TRIP: no diff!")
