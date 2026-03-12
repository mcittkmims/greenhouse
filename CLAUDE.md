# GMS Workspace Instructions

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
logging/
  schema.json               ← log entry format reference
  YYYY-MM-DDTHHMMSS.json    ← one file per logged task
scripts/
  confluence/
    confluence_sync.py      ← fetch Confluence → local .gcm files
    confluence_push.py      ← push local .gcm edits back to Confluence
    gcm_from_html.py        ← converter: Confluence storage HTML → GCM
    gcm_to_html.py          ← converter: GCM → Confluence storage HTML
    gcm_spec.py             ← shared GCM constants and utilities
    GCM_SPEC.md             ← GCM format specification
  jira/
    jira_board_server.py    ← local Jira board server + GMS board automation commands
  logging/
    log_work.py             ← work logging + PBL26 ticket management
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

**Agent rule:** Always prefer the built-in CLI commands (`jira_board_server.py`, `confluence_sync.py`, `confluence_push.py`) over writing inline Python. Only write custom Python when the built-in scripts provably do not support the required operation. Check available subcommands with `--help` before resorting to custom code.

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

## Work Logging

**When to log:** After completing any task that is **GMS project development work** — writing or editing GMS documentation (Confluence pages, WP files), or writing code that belongs to the Greenhouse Management System itself (sensors, firmware, backend, cloud logic, etc.).

**When NOT to log:** Tooling/codespace work — changes to sync scripts (`confluence_sync.py`, `confluence_push.py`, `gcm_*.py`), Jira board scripts, the logging system itself, CLAUDE.md updates, or any infrastructure/automation that supports the workspace but is not part of the GMS product.

**Script:** `scripts/logging/log_work.py`

### Logging a task

```sh
python3 scripts/logging/log_work.py log \
  --task "Short description of what was done" \
  --score 7 \
  --files "documentation/confluence/wip/WP5.4_foo.gcm" \
  [--details "Optional extra context"] \
  [--ticket PBL26-563]
```

- `--score` — effort weight 1–10 (default 5). Used to proportionally split hours when posting worklogs. Higher score = more time allocated.
- `--ticket` — auto-detected from the WP number in `--task` or `--files`. If it can't match, prints candidates and exits with code 2; re-run with `--ticket`.
- Writes a timestamped JSON to `logging/YYYY-MM-DDTHHMMSS.json`.

### Posting worklogs to Jira

```sh
python3 scripts/logging/log_work.py worklog \
  --from 2026-03-10 \
  [--to 2026-03-12] \
  [--hours 6]
```

- Reads all log entries in the date range, divides `--hours` (default 6) proportionally by `score`, and POSTs a worklog to each entry's `pbl26_ticket`.
- Time per task is rounded to the nearest 5 minutes (minimum 5m).
- `--to` defaults to now; a date-only value (e.g. `2026-03-12`) is treated as end of that day.
- **Duplicate-safe:** before posting, fetches existing worklogs for each ticket and skips any entry whose task description exactly matches an already-posted comment.

### Logging work done outside Claude (direct Jira worklog)

```sh
python3 scripts/logging/log_work.py log-direct \
  --ticket 5.4 \
  --task "Filled in WP5.4 risk table" \
  --hours 1.5 \
  [--date 2026-03-11]
```

- Posts a worklog directly to Jira without creating a local log file. Use this for work done manually, on another device, or in any session without Claude.
- `--ticket` accepts a WP number (e.g. `5.4`) or a full key (e.g. `PBL26-563`).
- `--hours` supports decimals (`1.5` = 1h 30m), rounded to nearest 5 minutes.
- `--date` defaults to today.

### Workshop day logging (report-log)

Posts two fixed worklogs to the PBL26 tracking ticket (`PBL26-1362`) for a class workshop day. Used to fill in the daily attendance/participation report without specifying times manually.

```sh
python3 scripts/logging/log_work.py report-log --date 2026-03-12
python3 scripts/logging/log_work.py report-log --date 2026-03-12 --task "Custom desc 1" "Custom desc 2"
```

Always posts exactly two entries:
- `15:15` — 1h 30m — default: `"Attended PBL26 workshop session"`
- `19:00` — 1h 30m — default: `"Continued GMS project work during lab"`

`--task` is optional; supply 1 or 2 strings to override the defaults. `--date` defaults to today.

### Weekly standup report

```sh
python3 scripts/logging/log_work.py report --from 2026-03-10 [--to 2026-03-16]
```

Fetches all worklogs from every PBL26 ticket in the date range and prints a standup-style summary: what was done, what's next (first WP with no worklogs), total hours logged. `--to` defaults to now.

### PBL26 ticket management

```sh
python3 scripts/logging/log_work.py list-tickets
python3 scripts/logging/log_work.py list-transitions PBL26-563
python3 scripts/logging/log_work.py move --to "Resolve Issue" PBL26-563 PBL26-558
```

- `list-tickets` — shows all PBL26 tickets for `adrian.vremere` (excluding PBL26-1362 tracking).
- `list-transitions KEY` — shows available status transitions for a ticket.
- `move --to NAME KEY...` — transitions one or more tickets; `--to` matches case-insensitively (e.g. `--to resolve`). Available transitions: **Start Progress**, **Resolve Issue**, **Close Issue**, **Rejected**.

> These commands target the **PBL26 course board**, not the GMS board. Do not use `jira_board_server.py` for PBL26 operations.

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
