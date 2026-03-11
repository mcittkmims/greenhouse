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
    cloud/                  ← auto-synced copies fetched from Confluence (do not manually edit)
    wip/                    ← files currently being actively worked on
    resources/              ← large local reference/learning materials (Markdown, not synced to Confluence)
  jira/
    board.html              ← local Jira board shell
scripts/
  confluence/
    confluence_sync.py      ← sync tool (see below)
    confluence_push.py      ← push local edits back to Confluence
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

**Rules:**
- Only fetch pages with WP ≤ requested limit (e.g., `--up-to 4.2` fetches WP1.1 → 4.2, stops before 4.3)
- Pages in ascending WP order: 1.1 → 2.1 → 3.1 → 3.2 → 3.3 → 3.4 → 4.1 → 4.2 → 4.3 → 5.1 → 5.2 → 5.3 → 5.4 → ...
- Pages marked `"skip_fetch": true` are maintained locally; never overwrite from Confluence
- Script auto-detects version changes via cache in `documentation/confluence/cloud/.cache/`

**Adding New Pages:**
If a WP is requested but not in `documentation/confluence/confluence_pages.json`:
1. Try to discover the page ID by querying the parent page (use `gms_root_page_id`)
2. Once found, add the entry to `confluence_pages.json` with `wp`, `id`, and `local_file`
3. Run the sync command

---

## Workflow

- **Synced files** (Confluence → Markdown): `documentation/confluence/cloud/`
- **Active work:** Move to `documentation/confluence/wip/` while editing, then back when done
- **Local-only files:** Root `documentation/` (not auto-synced)
- **Jira board:** Keep `documentation/jira/board.html` as the local board entry point; use `scripts/jira/jira_board_server.py` for live data and agentic operations

**Pushing local changes back to Confluence:**
```sh
python3 scripts/confluence/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.md
```
- Compares local file against the `cloud/` cached copy and shows a diff
- Only pushes if changes are detected; prompts for confirmation before pushing
- Converts Markdown → Confluence storage format automatically
- Updates the local `cloud/` cache after a successful push
- Use `--dry-run` to preview the diff and converted XHTML without pushing
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

For automatic multi-page fetching with HTML→Markdown conversion, **use the sync script** (recommended).
