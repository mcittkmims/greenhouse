#!/usr/bin/env python3
"""
confluence_sync.py — Fetch GMS Confluence pages and convert to local GCM files.

Usage:
    python3 scripts/confluence/confluence_sync.py --up-to 4.2
    python3 scripts/confluence/confluence_sync.py --up-to 5.4 --dry-run
    python3 scripts/confluence/confluence_sync.py --up-to 3.3 --force

Options:
    --up-to X.Y     Fetch all pages with WP number <= X.Y (ascending order)
    --dry-run       Print what would be fetched without writing files
    --force         Re-fetch even if the page version hasn't changed

Credentials are read from .env in the workspace root:
    CONFLUENCE_USER=...
    CONFLUENCE_PASS=...
    CONFLUENCE_URL=http://confluence.microlab.club   (optional override)

Pages config: documentation/confluence/confluence_pages.json
Output dir:   documentation/confluence/cloud/
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed.  Run: pip3 install requests")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from gcm_from_html import html_to_gcm  # noqa: E402
from confluence_attachments import download_attachments  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = ROOT / "documentation" / "confluence" / "confluence_pages.json"
CLOUD_DIR = ROOT / "documentation" / "confluence" / "cloud"
CACHE_DIR = CLOUD_DIR / ".cache"
ATTACHMENTS_DIR = CLOUD_DIR / "attachments"


# ── Config / auth helpers ────────────────────────────────────────────────────

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


def wp_key(wp_str):
    """Parse 'X.Y' into (X, Y) for comparison."""
    parts = wp_str.split(".")
    return tuple(int(x) for x in parts)


def pages_up_to(config, limit_str):
    """Return pages list where WP <= limit, sorted ascending."""
    limit = wp_key(limit_str)
    selected = [p for p in config["pages"] if wp_key(p["wp"]) <= limit]
    selected.sort(key=lambda p: wp_key(p["wp"]))
    return selected


def fetch_page(page_id, base_url, auth):
    """Fetch a Confluence page via REST API. Returns JSON response."""
    url = f"{base_url}/rest/api/content/{page_id}"
    params = {"expand": "body.storage,version,title"}
    resp = requests.get(url, params=params, auth=auth, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Sync GMS Confluence pages to local GCM files."
    )
    parser.add_argument(
        "--up-to", required=True, metavar="X.Y",
        help="Fetch pages with WP number up to X.Y"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be done without writing"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Re-fetch even if version hasn't changed"
    )
    args = parser.parse_args()

    env = load_env()
    config = load_config()
    auth = (env["CONFLUENCE_USER"], env["CONFLUENCE_PASS"])
    base_url = env.get("CONFLUENCE_URL", config["base_url"])

    CLOUD_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)

    pages = pages_up_to(config, args.up_to)
    if not pages:
        print(f"No pages found with WP <= {args.up_to}")
        sys.exit(0)

    print(f"Pages to sync (up to WP {args.up_to}):")
    for p in pages:
        skip = p.get("skip_fetch", False)
        note = f"  [SKIP — {p.get('note', 'local-only')}]" if skip else ""
        print(f"  WP{p['wp']} — {p['local_file']}{note}")

    if args.dry_run:
        print("\n[dry-run] No files written.")
        return

    print()
    updated = 0
    skipped = 0
    errors = 0

    for page in pages:
        wp = page["wp"]
        local_file = page["local_file"]

        if page.get("skip_fetch"):
            print(f"  SKIP      WP{wp} ({page.get('note', 'local-only')})")
            skipped += 1
            continue

        local_path = CLOUD_DIR / local_file

        # Check cached version to avoid unnecessary fetches
        ver_cache = CACHE_DIR / f"{local_file}.version"
        cached_version = ver_cache.read_text().strip() if ver_cache.exists() else None

        try:
            data = fetch_page(page["id"], base_url, auth)
        except Exception as e:
            print(f"  ERROR     WP{wp} — {e}")
            errors += 1
            continue

        current_version = str(data.get("version", {}).get("number", ""))
        title = data.get("title", f"WP{wp}")
        html = data["body"]["storage"]["value"]
        source_url = f"{base_url}/rest/api/content/{page['id']}"

        if not args.force and cached_version == current_version and local_path.exists():
            print(f"  UP-TO-DATE  WP{wp} (v{current_version})")
            continue

        # Conflict check: warn if local file was edited since last sync
        hash_cache = CACHE_DIR / f"{local_file}.hash"
        if not args.force and local_path.exists() and hash_cache.exists():
            stored_hash = hash_cache.read_text().strip()
            local_hash = hashlib.md5(local_path.read_bytes()).hexdigest()
            if local_hash != stored_hash:
                print(f"  CONFLICT  WP{wp} — local file has uncommitted edits")
                print(f"            Push your changes first, or use --force to overwrite.")
                continue

        # Convert HTML → GCM
        gcm_text = html_to_gcm(
            html, title=title, page_id=page["id"],
            version=current_version, source_url=source_url,
        )

        local_path.write_text(gcm_text, encoding="utf-8")
        ver_cache.write_text(current_version, encoding="utf-8")
        hash_cache.write_text(
            hashlib.md5(gcm_text.encode()).hexdigest(), encoding="utf-8"
        )
        updated += 1
        ver_note = f"v{cached_version} → v{current_version}" if cached_version else f"v{current_version}"
        print(f"  UPDATED   WP{wp} — {local_file} ({ver_note})")

        # Download attachments (images, diagrams, etc.)
        att_dir = ATTACHMENTS_DIR / Path(local_file).stem
        try:
            n = download_attachments(page["id"], base_url, auth, att_dir, dry_run=args.dry_run)
            if n:
                print(f"            {n} attachment(s) → attachments/{Path(local_file).stem}/")
        except Exception as e:
            print(f"            WARNING: could not download attachments — {e}")

    print(f"\nSync complete: {updated} updated, {skipped} skipped, {errors} errors.")


if __name__ == "__main__":
    main()
