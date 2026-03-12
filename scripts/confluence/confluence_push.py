#!/usr/bin/env python3
"""
confluence_push.py — Push a local GCM file back to Confluence.

Compares the local file against the last-synced cloud/ copy to show what
changed, then converts GCM → Confluence storage XHTML and updates the page.

Usage:
    python3 scripts/confluence/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.gcm
    python3 scripts/confluence/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.gcm --dry-run
    python3 scripts/confluence/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.gcm --no-confirm

Options:
    --file FILE     Filename to push (in documentation/confluence/cloud/)
    --dry-run       Show diff and converted XHTML without pushing
    --no-confirm    Skip confirmation prompt
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime
from difflib import unified_diff
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed.  Run: pip3 install requests")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from gcm_to_html import gcm_to_html  # noqa: E402
from gcm_spec import parse_frontmatter  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = ROOT / "documentation" / "confluence" / "confluence_pages.json"
CLOUD_DIR = ROOT / "documentation" / "confluence" / "cloud"
CACHE_DIR = CLOUD_DIR / ".cache"
LOG_DIR = CACHE_DIR / "push_logs"


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    env = {}
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    for key in ("CONFLUENCE_USER", "CONFLUENCE_PASS"):
        if key not in env:
            print(f"ERROR: {key} not set in .env")
            sys.exit(1)
    return env


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def find_page_entry(config, filename):
    """Find a page config entry matching the given filename."""
    basename = Path(filename).name
    for p in config["pages"]:
        if p["local_file"] == basename:
            return p
    return None


def fetch_page(page_id, base_url, auth):
    url = f"{base_url}/rest/api/content/{page_id}"
    params = {"expand": "body.storage,version,title"}
    resp = requests.get(url, params=params, auth=auth, timeout=30)
    resp.raise_for_status()
    return resp.json()


def push_page(page_id, title, version_number, storage_xhtml, base_url, auth):
    url = f"{base_url}/rest/api/content/{page_id}"
    payload = {
        "id": page_id,
        "type": "page",
        "title": title,
        "version": {"number": version_number, "minorEdit": True},
        "body": {
            "storage": {
                "value": storage_xhtml,
                "representation": "storage",
            }
        },
    }
    resp = requests.put(url, json=payload, auth=auth, timeout=30)
    resp.raise_for_status()
    return resp.json()


def compute_diff(old_text, new_text, from_label, to_label):
    """Return (diff_lines, added_count, removed_count)."""
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)
    diff = list(unified_diff(old_lines, new_lines,
                             fromfile=from_label, tofile=to_label))
    added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
    return diff, added, removed


def show_diff(old_text, new_text, from_label, to_label):
    """Print a unified diff. Returns the diff lines (empty if identical)."""
    diff, added, removed = compute_diff(old_text, new_text, from_label, to_label)
    if not diff:
        return diff
    print(f"\n--- Diff: {added} added, {removed} removed ---\n")
    for line in diff:
        print(line, end="")
    print()
    return diff


def write_push_log(basename, page_entry, diff_lines, result_status, details=""):
    """Write a push log entry to .cache/push_logs/."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now()
    ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
    ts_file = ts.strftime("%Y%m%d_%H%M%S")
    wp = page_entry["wp"]
    log_name = f"{ts_file}_WP{wp}_{result_status}.log"
    log_path = LOG_DIR / log_name

    lines = [
        f"Push Log — {ts_str}",
        f"File:    {basename}",
        f"Page:    WP{wp} (ID {page_entry['id']})",
        f"Result:  {result_status}",
    ]
    if details:
        lines.append(f"Details: {details}")
    lines.append("")
    if diff_lines:
        lines.append("=== Diff ===")
        lines.extend(l.rstrip("\n") for l in diff_lines)
        lines.append("=== End Diff ===")
    else:
        lines.append("(no diff — identical to last sync)")
    lines.append("")
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Log written: {log_path.relative_to(ROOT)}")
    return log_path


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Push a local GCM file to Confluence."
    )
    parser.add_argument(
        "--file", required=True, metavar="FILE",
        help="GCM filename to push (e.g. WP4.2_Analyze_Stakeholder_Requirements.gcm)"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Show diff and converted XHTML without pushing")
    parser.add_argument("--no-confirm", action="store_true",
                        help="Skip confirmation prompt")
    args = parser.parse_args()

    env = load_env()
    config = load_config()
    auth = (env["CONFLUENCE_USER"], env["CONFLUENCE_PASS"])
    base_url = env.get("CONFLUENCE_URL", config["base_url"])
    jira_cfg = config.get("jira", {})

    # Locate local file
    basename = Path(args.file).name
    local_path = CLOUD_DIR / basename
    if not local_path.exists():
        print(f"ERROR: File not found: {local_path}")
        sys.exit(1)
    print(f"Local file:  {local_path}")

    # Find config entry
    page_entry = find_page_entry(config, basename)
    if not page_entry:
        print(f"ERROR: No page entry for '{basename}' in confluence_pages.json")
        sys.exit(1)

    page_id = page_entry["id"]
    print(f"Page ID:     {page_id}  (WP{page_entry['wp']})")

    # Fetch live page for version and conflict check
    print("Fetching current Confluence content...")
    try:
        data = fetch_page(page_id, base_url, auth)
    except Exception as e:
        print(f"ERROR: Failed to fetch page: {e}")
        sys.exit(1)

    current_version = data["version"]["number"]
    title = data["title"]
    print(f"Confluence version: {current_version}  |  Title: {title}")

    # Conflict detection: ensure we're editing the same version we last synced
    ver_cache = CACHE_DIR / f"{basename}.version"
    if ver_cache.exists():
        cached_version = ver_cache.read_text().strip()
        if str(current_version) != cached_version:
            print(f"\nCONFLICT: Confluence was modified since your last sync.")
            print(f"  Cached version : {cached_version}")
            print(f"  Live version   : {current_version}")
            print(f"\nSync first:  python3 scripts/confluence/confluence_sync.py --up-to {page_entry['wp']} --force")
            sys.exit(1)
    else:
        print("Warning: No version cache — skipping conflict check.")

    # Diff local file vs cached cloud copy
    local_text = local_path.read_text(encoding="utf-8")
    hash_cache = CACHE_DIR / f"{basename}.hash"
    if hash_cache.exists():
        stored_hash = hash_cache.read_text().strip()
        local_hash = hashlib.md5(local_text.encode()).hexdigest()
        if local_hash == stored_hash:
            print("\nNo changes detected vs last synced version. Nothing to push.")
            sys.exit(0)

    print(f"\nLocal file has been modified since last sync.")

    # Show XHTML-level diff: current Confluence content vs. what we'd push
    cloud_xhtml = data["body"]["storage"]["value"]

    # Convert GCM → Confluence storage XHTML
    storage_xhtml, meta = gcm_to_html(
        local_text,
        jira_server=jira_cfg.get("server", ""),
        jira_server_id=jira_cfg.get("server_id", ""),
    )

    # Show diff between cloud XHTML and what we'd push
    diff_lines = show_diff(cloud_xhtml, storage_xhtml,
                           f"confluence (v{current_version})", "local (converted)")
    if not diff_lines:
        print("\nNo XHTML differences detected. Nothing to push.")
        write_push_log(basename, page_entry, [], "SKIPPED", "No XHTML diff")
        return

    if args.dry_run:
        print("\n[dry-run] Nothing pushed.")
        write_push_log(basename, page_entry, diff_lines, "DRY_RUN")
        return

    new_version = current_version + 1
    print(f"New version: {new_version}")
    print(f"XHTML size:  {len(storage_xhtml)} chars")

    if not args.no_confirm:
        answer = input(f"\nPush WP{page_entry['wp']} to Confluence? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            sys.exit(0)

    print("Pushing...")
    try:
        result = push_page(page_id, title, new_version, storage_xhtml, base_url, auth)
    except requests.HTTPError as e:
        print(f"ERROR: Push failed: {e}")
        if e.response is not None:
            print(e.response.text[:1000])
        write_push_log(basename, page_entry, diff_lines, "FAILED", str(e))
        sys.exit(1)

    pushed_version = result.get("version", {}).get("number", new_version)
    print(f"\nSUCCESS: WP{page_entry['wp']} pushed (version {pushed_version})")
    write_push_log(basename, page_entry, diff_lines, "SUCCESS",
                   f"v{current_version} → v{pushed_version}")

    # Update caches
    CACHE_DIR.mkdir(exist_ok=True)
    ver_cache.write_text(str(pushed_version), encoding="utf-8")
    hash_cache.write_text(
        hashlib.md5(local_text.encode()).hexdigest(), encoding="utf-8"
    )
    print(f"Updated version cache: v{pushed_version}")


if __name__ == "__main__":
    main()
