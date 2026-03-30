---
description: Sync documentation from Confluence to local GCM format
---
# Syncing Documentation

Fetches Confluence pages via REST API, converts storage HTML → GCM, and writes `.gcm` files to `documentation/confluence/cloud/`.

**Options:**
- `--up-to X.Y` — fetch pages with WP ≤ limit (e.g., `--up-to 4.2` fetches WP1.1 → 4.2)
- `--all` — fetch all pages listed in `confluence_pages.json`
- `--page WP [WP ...]` — fetch one or more specific pages by WP number (e.g., `--page 6.1 6.2`)
- `--dry-run` — list pages without writing files
- `--force` — re-fetch even if the cached version matches

**Commands:**
```sh
python3 scripts/confluence/confluence_sync.py --up-to <WP_LIMIT>
python3 scripts/confluence/confluence_sync.py --all
python3 scripts/confluence/confluence_sync.py --page 6.1 6.2
```

**Adding New Pages:**
If a WP is requested but not in `documentation/confluence/confluence_pages.json`:
1. Try to discover the page ID by querying the parent page (use `gms_root_page_id`)
2. Once found, add the entry to `confluence_pages.json` with `wp`, `id`, and `local_file` (use `.gcm` extension)
3. Run the sync command
