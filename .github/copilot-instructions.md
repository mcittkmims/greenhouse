# GitHub Copilot — GMS Workspace Instructions

## Project
**Greenhouse Management System (GMS)** — PBL IoT course, Technical University of Moldova (UTM)

**Team:** Alexei Maxim, Vremere Adrian, Cojocaru Daniel, Rațeeva Daria, Mutruc Victoria

---

## Documentation Structure

```
documentation/
  confluence_pages.json     ← page ID map + config (READ THIS FIRST)
  CONFLUENCE_INDEX.md       ← human-readable link table
  cloud/                    ← auto-synced copies fetched from Confluence (do not manually edit)
  wip/                      ← files currently being actively worked on
  WP*.md                    ← locally maintained documents
scripts/
  confluence_sync.py        ← sync tool (see below)
.env                        ← credentials (never commit)
```

---

## Confluence

- **URL:** `http://confluence.microlab.club`
- **Project:** GMS (Space PBL26, root page ID 42633959) — do not read other projects (AFB, AGC, CDR, PDD, SPM)
- **Auth:** `CONFLUENCE_USER`, `CONFLUENCE_PASS`, `CONFLUENCE_URL` in `.env`
- **All page IDs:** `documentation/confluence_pages.json`

---

## Syncing Documentation

**Command:** `python3 scripts/confluence_sync.py --up-to X.Y`

**Rules:**
- Only fetch pages with WP ≤ requested limit (e.g., `--up-to 4.2` fetches WP1.1 → 4.2, stops before 4.3)
- Pages in ascending WP order: 1.1 → 2.1 → 3.1 → 3.2 → 3.3 → 3.4 → 4.1 → 4.2 → ...
- Pages marked `"skip_fetch": true` are maintained locally; never overwrite from Confluence
- Script auto-detects version changes via cache in `documentation/cloud/.cache/`

**Adding New Pages:**
If a WP is requested but not in `documentation/confluence_pages.json`:
1. Try to discover the page ID by querying the parent page (use `gms_root_page_id`)
2. Once found, add the entry to `confluence_pages.json` with `wp`, `id`, and `local_file`
3. Run the sync command

---

## Workflow

- **Synced files** (Confluence → Markdown): `documentation/cloud/`
- **Active work:** Move to `documentation/wip/` while editing, then back when done
- **Local-only files:** Root `documentation/` (not auto-synced)

---

## Manual Fetch (Advanced)

Use the REST API with page IDs (no display URL needed):

```sh
source .env
curl -s -u "$CONFLUENCE_USER:$CONFLUENCE_PASS" \
  "$CONFLUENCE_URL/rest/api/content/<PAGE_ID>?expand=body.storage"
```

**Example:** `curl ... /rest/api/content/42634112?expand=body.storage` (WP4.3)

For automatic multi-page fetching with HTML→Markdown conversion, **use the sync script** (recommended).
