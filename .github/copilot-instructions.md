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
    board.html              ← local GMS board shell (open while server runs)
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
  jira/                     ← GMS board (issue management: assignments, moves, comments)
    jira_board_server.py    ← local board server + GMS issue automation
  logging/                  ← PBL26 course board (work logging & time tracking per WP)
    log_work.py             ← log tasks locally + post worklogs to PBL26 tickets
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

There are **two separate Jira boards** — use the correct script for each. Never mix them up.

- **URL:** `http://jira.microlab.club`
- **Auth:** `JIRA_USER`, `JIRA_PASS`, `JIRA_URL` in `.env` (falls back to `CONFLUENCE_USER`/`CONFLUENCE_PASS` when needed)

### GMS Board — `scripts/jira/jira_board_server.py`

The **GMS board** contains the actual project issues (user stories, tasks, job stories). Use this for issue management: creating issues, changing assignees, moving to columns, adding comments, updating fields.

- **Board shell:** `documentation/jira/board.html` (open in browser while server runs)
- **Script:** `scripts/jira/jira_board_server.py`

Key flags available on `create`, `update`, and `bulk-update`:
- `--epic GMS-X` — link issue to an epic (sets Epic Link field)
- `--labels "Functional,EARS-Event"` — comma-separated labels
- `--priority Highest` — priority name (Highest/High/Medium/Low/Lowest)

Key flags available on `move` and `bulk-move`:
- `--force` — walk through intermediate transitions when no direct path exists (e.g. Backlog → In Work → Proposed)

Only GMS board content and automation live under `documentation/jira/` and `scripts/jira/`.

### PBL26 Course Board — `scripts/logging/log_work.py`

The **PBL26 course board** tracks work packages (WP1.1, WP2.1 … WP10.x) for `adrian.vremere` as part of the university course. Use this for work logging, posting time entries (worklogs), and transitioning WP tickets. **Never use `jira_board_server.py` for PBL26 operations.**

- **Script:** `scripts/logging/log_work.py`
- **Ticket format:** `PBL26-XXX` (e.g. `PBL26-548` for WP5.1)

**Agent rule:** Always prefer the built-in CLI commands (`jira_board_server.py`, `confluence_sync.py`, `confluence_push.py`, `log_work.py`) over writing inline Python. Only write custom Python when the built-in scripts provably do not support the required operation. Check available subcommands with `--help` before resorting to custom code.

---

## Work Logging

**When to log:** After completing any task that is **GMS project development work** — writing or editing GMS documentation (Confluence pages, WP files), or writing code that belongs to the Greenhouse Management System itself (sensors, firmware, backend, cloud logic, etc.).

**When NOT to log:** Tooling/codespace work — changes to sync scripts (`confluence_sync.py`, `confluence_push.py`, `gcm_*.py`), Jira board scripts, the logging system itself, or any infrastructure/automation that supports the workspace but is not part of the GMS product.

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

- `--score` — effort weight 1–10 (default 5). Higher score = more time allocated when posting worklogs.
- `--ticket` — auto-detected from the WP number in `--task` or `--files`. Prints candidates and exits code 2 if it can't match.
- Writes a timestamped JSON to `logging/YYYY-MM-DDTHHMMSS.json`.

### Posting worklogs to Jira

```sh
python3 scripts/logging/log_work.py worklog \
  --from 2026-03-10 [--to 2026-03-12] [--hours 6]
```

Reads log entries in the date range, divides `--hours` (default 6) proportionally by `score`, and POSTs a worklog to each entry's `pbl26_ticket`. Time is rounded to the nearest 5 minutes. **Duplicate-safe:** skips any entry whose task description exactly matches an already-posted worklog comment on that ticket.

### Logging work done outside Claude (direct Jira worklog)

```sh
python3 scripts/logging/log_work.py log-direct \
  --ticket 5.4 \
  --task "Filled in WP5.4 risk table" \
  --hours 1.5 \
  [--date 2026-03-11]
```

Posts a worklog directly to Jira without creating a local log file. Use for work done manually or outside of Claude sessions. `--ticket` accepts WP number or full key; `--date` defaults to today.

### Workshop day logging (report-log)

```sh
python3 scripts/logging/log_work.py report-log --date 2026-03-12
python3 scripts/logging/log_work.py report-log --date 2026-03-12 --task "Custom desc 1" "Custom desc 2"
```

Posts two fixed worklogs to `PBL26-1362` (the tracking/attendance ticket) for a class workshop day. Fixed slots: `15:15` and `19:00`, each 1h 30m. Descriptions default to generic workshop text; `--task` overrides them (up to 2 strings). `--date` defaults to today.

### Weekly standup report

```sh
python3 scripts/logging/log_work.py report --from 2026-03-10 [--to 2026-03-16]
```

Fetches all worklogs from every PBL26 ticket in the date range, prints a standup-style summary (what was done, what's next, total hours), and **posts it as a comment on `PBL26-1362`**. `--to` defaults to now. Use `--no-post` to print only without posting.

### PBL26 ticket management

```sh
python3 scripts/logging/log_work.py list-tickets
python3 scripts/logging/log_work.py list-transitions PBL26-563
python3 scripts/logging/log_work.py move --to "Resolve Issue" PBL26-563 PBL26-558
```

These target the **PBL26 course board** for `adrian.vremere`, not the GMS board. Do not use `jira_board_server.py` for PBL26 operations. Available transitions: **Start Progress**, **Resolve Issue**, **Close Issue**, **Rejected**.

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
