#!/usr/bin/env python3
"""
confluence_attachments.py — Download attachments from Confluence pages.

Provides download_attachments() for use by confluence_sync.py and other scripts.
"""

from pathlib import Path

try:
    import requests
except ImportError:
    import sys
    print("ERROR: 'requests' not installed.  Run: pip3 install requests")
    sys.exit(1)


def download_attachments(page_id, base_url, auth, dest_dir, dry_run=False):
    """Download all attachments for a page into dest_dir. Returns count."""
    url = f"{base_url}/rest/api/content/{page_id}/child/attachment"
    params = {"limit": 100}
    resp = requests.get(url, params=params, auth=auth, timeout=30)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        return 0
    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for att in results:
        filename = att["title"]
        download_path = att.get("_links", {}).get("download", "")
        if not download_path:
            continue
        if dry_run:
            count += 1
            continue
        file_resp = requests.get(f"{base_url}{download_path}", auth=auth, timeout=60, stream=True)
        file_resp.raise_for_status()
        (dest_dir / filename).write_bytes(file_resp.content)
        count += 1
    return count
