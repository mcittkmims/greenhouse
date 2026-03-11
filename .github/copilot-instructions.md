# GitHub Copilot — GMS Workspace Instructions

## Project
**Greenhouse Management System (GMS)** — PBL IoT course, Technical University of Moldova (UTM)

**Team:** Alexei Maxim, Vremere Adrian, Cojocaru Daniel, Rațeeva Daria, Mutruc Victoria

---

## Documentation Structure

```
documentation/
  confluence/
    confluence_pages.json   ← page ID map + config (READ THIS FIRST)
    cloud/                  ← auto-synced .gcm files fetched from Confluence
    wip/                    ← files currently being actively worked on
    resources/              ← large local reference/learning materials (Markdown, not synced)
  jira/
    board.html              ← local Jira board shell
  GCM_Documentation.md     ← comprehensive GCM format documentation
scripts/
  confluence/
    confluence_sync.py      ← fetch Confluence → local .gcm files
    confluence_push.py      ← push local .gcm edits back to Confluence
    gcm_from_html.py        ← converter: Confluence storage HTML → GCM
    gcm_to_html.py          ← converter: GCM → Confluence storage HTML
    gcm_spec.py             ← shared GCM constants and utilities
    GCM_SPEC.md             ← GCM format specification
  jira/
    jira_board_server.py    ← local Jira board server + automation commands
.env                        ← credentials (never commit)
```

---

## Confluence

- **URL:** `http://confluence.microlab.club`
- **Project:** GMS (Space PBL26, root page ID 42633959) — do not read other projects (AFB, AGC, CDR, PDD, SPM)
- **Auth:** `CONFLUENCE_USER`, `CONFLUENCE_PASS`, `CONFLUENCE_URL` in `.env`
- **All page IDs:** `documentation/confluence/confluence_pages.json`

Only Confluence content and metadata live under `documentation/confluence/` and `scripts/confluence/`.

### GCM — GMS Confluence Markup

Local copies of Confluence pages are stored in **GCM format** (`.gcm` files), a custom
line-oriented markup designed for lossless round-tripping of Confluence storage HTML.

Quick reference specification: `scripts/confluence/GCM_SPEC.md`
Comprehensive documentation: `documentation/GCM_Documentation.md`

Key syntax:
- Headings: `= H1`, `== H2`, `=== H3` …
- Bold/italic: `**bold**`, `*italic*`
- Links: `[text](url)`, `{link page="Page Title"}text{/link}`
- Jira issues: `{jira:GMS-10}` (most common inline element)
- Anchors: `{anchor:ref4}`
- Tables: `{table}…{/table}` with `{td}`, `{th}`, `rowspan`, `colspan`
- Images: `{image file="diagram.png" height=400}`
- Status badges: `{status:Draft|color=Yellow}`
- Raw passthrough: `{raw}…{/raw}` for any unrecognized Confluence XML

Converter modules:
- `gcm_from_html.py` — Confluence storage HTML → GCM
- `gcm_to_html.py` — GCM → Confluence storage HTML
- `gcm_spec.py` — shared utilities (frontmatter, attribute parsing, escaping)

---

## Jira

- **URL:** `http://jira.microlab.club`
- **Auth:** `JIRA_USER`, `JIRA_PASS`, `JIRA_URL` in `.env` (falls back to `CONFLUENCE_USER`/`CONFLUENCE_PASS` when needed)
- **Board shell:** `documentation/jira/board.html`
- **Automation and local board server:** `scripts/jira/jira_board_server.py`

Only Jira content and automation live under `documentation/jira/` and `scripts/jira/`.

**Command:** `python3 scripts/jira/jira_board_server.py`

Use that script both for the local interactive board server and direct Jira automation commands such as assignee changes, comments, issue updates, moves, and issue creation.

---

## Syncing Documentation

**Command:** `python3 scripts/confluence/confluence_sync.py --up-to X.Y`

Fetches Confluence pages via REST API, converts storage HTML → GCM, and writes `.gcm` files
to `documentation/confluence/cloud/`.

**Options:**
- `--up-to X.Y` — fetch pages with WP ≤ limit (e.g., `--up-to 4.2` fetches WP1.1 → 4.2)
- `--dry-run` — list pages without writing files
- `--force` — re-fetch even if the cached version matches

**Rules:**
- Pages in ascending WP order: 1.1 → 2.1 → 3.1 → … → 5.4 → …
- Pages marked `"skip_fetch": true` are maintained locally; never overwrite from Confluence
- Version + hash cache in `documentation/confluence/cloud/.cache/` enables incremental sync
  and conflict detection (warns if local file was edited since last sync)

**Adding New Pages:**
If a WP is requested but not in `documentation/confluence/confluence_pages.json`:
1. Try to discover the page ID by querying the parent page (use `gms_root_page_id`)
2. Once found, add the entry to `confluence_pages.json` with `wp`, `id`, and `local_file` (use `.gcm` extension)
3. Run the sync command

---

## Workflow

- **Synced files** (Confluence → GCM): `documentation/confluence/cloud/*.gcm`
- **Active work:** Move to `documentation/confluence/wip/` while editing, then back when done
- **Local-only files:** Root `documentation/` (not auto-synced)
- **Jira board:** Keep `documentation/jira/board.html` as the local board entry point; use `scripts/jira/jira_board_server.py` for live data and agentic operations

**Pushing local changes back to Confluence:**
```sh
python3 scripts/confluence/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.gcm
```
- Only pushes if local file hash differs from last sync
- Detects version conflicts (warns if Confluence was modified since last sync)
- Converts GCM → Confluence storage XHTML automatically
- Updates the local version + hash cache after a successful push
- Use `--dry-run` to preview the converted XHTML without pushing
- Use `--no-confirm` to skip the confirmation prompt

---

## Manual Fetch (Advanced)

Use the REST API with page IDs (no display URL needed):

```sh
source .env
curl -s -u "$CONFLUENCE_USER:$CONFLUENCE_PASS" \
  "$CONFLUENCE_URL/rest/api/content/<PAGE_ID>?expand=body.storage"
```

**Example:** `curl ... /rest/api/content/42634150?expand=body.storage` (WP5.4)

For automatic multi-page fetching with HTML→GCM conversion, **use the sync script** (recommended).
