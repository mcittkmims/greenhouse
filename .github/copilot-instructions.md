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

## Confluence Source of Truth

- **Base URL:** `http://confluence.microlab.club`
- **GMS project page:** `http://confluence.microlab.club/display/PBL26/04+-+GMS+-Greenhouse+Management+System`
- **Only fetch from this GMS project** — do not read pages from other projects (AFB, AGC, CDR, PDD, SPM)
- **Credentials:** `CONFLUENCE_USER`, `CONFLUENCE_PASS`, `CONFLUENCE_URL` in `.env`

---

## Sync Rules

When asked to **update**, **fetch**, or **sync** documentation:

1. Read `documentation/confluence_pages.json` for the page list and IDs
2. Only fetch pages with WP number **≤ the requested limit** (e.g. "update up to 4.2" → fetch WP1.1, 2.1, 3.1, 3.2, 3.3, 3.4, 4.1 — stop before 4.3 or higher)
3. Pages in ascending WP order: 1.1 → 2.1 → 3.1 → 3.2 → 3.3 → 3.4 → 4.1 → 4.2 → ...
4. Pages marked `"skip_fetch": true` in the config are **maintained locally only** — never overwrite from Confluence
5. Use the sync script: `python3 scripts/confluence_sync.py --up-to X.Y`

---

## WIP Folder

`documentation/wip/` contains files currently being actively edited.
When the user says they are "working on" a document, move or copy it to `wip/`.
When a document is released/finalised, it moves back to `documentation/`.

---

## Fetching a Page Manually

```sh
source .env
# Get content by page ID
curl -s -u "$CONFLUENCE_USER:$CONFLUENCE_PASS" \
  "$CONFLUENCE_URL/rest/api/content/<PAGE_ID>?expand=body.storage" | python3 -c "
import sys, json, re
data = json.load(sys.stdin)
html = data['body']['storage']['value']
text = re.sub(r'<[^>]+>', ' ', html)
for e,r in [('&nbsp;',' '),('&lt;','<'),('&gt;','>'),('&amp;','&')]:
    text = text.replace(e, r)
text = re.sub(r'\s{3,}', '\n', text)
print(text[:12000])
"
```

All page IDs are in `documentation/confluence_pages.json`.
