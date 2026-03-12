#!/usr/bin/env python3
"""
Push-diff test: compare what Confluence has now vs what push script would send.
i.e. fetch live HTML, convert local GCM → HTML (same as push), diff the two.
"""
import json
import sys
from pathlib import Path
from difflib import unified_diff

sys.path.insert(0, str(Path(__file__).parent))
from gcm_to_html import gcm_to_html

ROOT = Path(__file__).resolve().parent.parent.parent
CLOUD_DIR = ROOT / "documentation" / "confluence" / "cloud"
SAVE_DIR = ROOT / "scripts" / "confluence" / "_rt_tmp"
SAVE_DIR.mkdir(exist_ok=True)

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

config = json.loads((ROOT / "documentation" / "confluence" / "confluence_pages.json").read_text())
jira_cfg = config.get("jira", {})

FILENAME = "WP5.1_Analyze_Stakeholder_Requirements.gcm"
page_entry = next(p for p in config["pages"] if p["local_file"] == FILENAME)
page_id = page_entry["id"]

# 1. Fetch live HTML from Confluence (what's currently there)
print(f"Fetching WP5.1 (id={page_id}) from Confluence...")
resp = requests.get(
    f"{base}/rest/api/content/{page_id}?expand=body.storage,version,title",
    auth=auth, timeout=30
)
resp.raise_for_status()
data = resp.json()
live_html = data["body"]["storage"]["value"]
title = data["title"]
version = data["version"]["number"]
print(f"  Title: {title!r}  version={version}  len={len(live_html)}")

# 2. Read local GCM (the file push would use)
local_gcm_path = CLOUD_DIR / FILENAME
local_gcm = local_gcm_path.read_text(encoding="utf-8")
print(f"  Local GCM: {local_gcm_path.relative_to(ROOT)}  len={len(local_gcm)}")

# 3. Convert local GCM → HTML exactly as push script does
push_html, _meta = gcm_to_html(
    local_gcm,
    jira_server=jira_cfg.get("server", ""),
    jira_server_id=jira_cfg.get("server_id", ""),
)
print(f"  Push HTML length: {len(push_html)} chars")

# 4. Save files
(SAVE_DIR / "live_confluence.html").write_text(live_html)
(SAVE_DIR / "push_converted.html").write_text(push_html)
print(f"  Saved to _rt_tmp/live_confluence.html and _rt_tmp/push_converted.html")

# 5. Diff
live_lines = live_html.splitlines(keepends=True)
push_lines = push_html.splitlines(keepends=True)
diff = list(unified_diff(live_lines, push_lines,
                         fromfile=f"confluence (v{version})",
                         tofile="push (local GCM converted)", n=3))

diff_path = SAVE_DIR / "push_diff.txt"
diff_path.write_text("".join(diff))

if not diff:
    print("\nRESULT: NO DIFF — what push would send is identical to what Confluence has.")
else:
    added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
    print(f"\nRESULT: DIFF found — {len(diff)} diff lines (+{added} added / -{removed} removed)")
    print(f"  Full diff saved to _rt_tmp/push_diff.txt")
    # Print first 60 lines so we can see what's different
    print("\n--- First 60 diff lines ---")
    for line in diff[:60]:
        print(line, end="")
