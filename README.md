# Greenhouse Management System (GMS)

PBL IoT course project — Technical University of Moldova (UTM)

**Team:** Alexei Maxim, Vremere Adrian, Cojocaru Daniel, Rațeeva Daria, Mutruc Victoria

---

## Repository Structure

```
documentation/
  confluence/
    confluence_pages.json   ← page ID map + config
    cloud/                  ← auto-synced .gcm files fetched from Confluence
    wip/                    ← files currently being actively worked on
    resources/              ← local reference/learning materials (not synced)
  jira/
    board.html              ← local interactive Jira board shell
logging/
  schema.json               ← log entry format reference
  YYYY-MM-DDTHHMMSS.json    ← one file per logged GMS task
scripts/
  confluence/
    confluence_sync.py      ← fetch Confluence → local .gcm files
    confluence_push.py      ← push local .gcm edits back to Confluence
    gcm_from_html.py        ← converter: Confluence storage HTML → GCM
    gcm_to_html.py          ← converter: GCM → Confluence storage HTML
    gcm_spec.py             ← shared GCM constants and utilities
    GCM_SPEC.md             ← GCM format specification
  jira/
    jira_board_server.py    ← local interactive Jira board API/server + GMS automation commands
  logging/
    log_work.py             ← work logging + PBL26 ticket management
.env                        ← credentials (never commit)
```

---

## Setup

Copy `.env.example` to `.env` and fill in your credentials:

```
CONFLUENCE_URL=http://confluence.microlab.club
CONFLUENCE_USER=your_username
CONFLUENCE_PASS=your_password

# Optional — defaults to jira.microlab.club and falls back to CONFLUENCE_USER/PASS
JIRA_URL=http://jira.microlab.club
JIRA_USER=your_username
JIRA_PASS=your_password
```

---

## Jira Workflow

Start the live local board server:

```sh
python3 scripts/jira/jira_board_server.py
```

Then open `documentation/jira/board.html` in VS Code Live Preview.

Jira-specific files live only in `documentation/jira/` and `scripts/jira/`.

The board pulls live data from Jira and supports local edits for summary, description, due date, assignee, and status transitions. Jira ticket references in Confluence pages (for example `[CDR-53](../../jira/board.html#cdr-53)`) resolve to the local board, while push back to Confluence still restores proper Jira macros linked to the online Jira instance.

The same script also exposes direct CLI commands for faster agentic operations:

```sh
python3 scripts/jira/jira_board_server.py users --query "Adrian Vremere"
python3 scripts/jira/jira_board_server.py assign --assignee adrian.vremere GMS-16 GMS-17
python3 scripts/jira/jira_board_server.py move --column proposed GMS-35
python3 scripts/jira/jira_board_server.py move --column proposed --force GMS-35        # multi-hop (e.g. Backlog → Proposed)
python3 scripts/jira/jira_board_server.py bulk-move --column proposed --force GMS-35 GMS-36
python3 scripts/jira/jira_board_server.py update --key GMS-35 --summary "New summary" --epic GMS-2 --labels "Functional,EARS-Event" --priority Highest
python3 scripts/jira/jira_board_server.py bulk-update --epic GMS-9 --labels "Functional,EARS-Event" --priority High GMS-35 GMS-36
python3 scripts/jira/jira_board_server.py comment --key GMS-35 --text "Reviewed"
python3 scripts/jira/jira_board_server.py bulk-comment --text "Reviewed" GMS-35 GMS-36
python3 scripts/jira/jira_board_server.py create --issue-type Story --summary "New SR" --epic GMS-2 --labels "Functional,EARS-Event" --priority Highest --assignee adrian.vremere
```

---

## Confluence Workflow

Confluence-specific files live only in `documentation/confluence/` and `scripts/confluence/`.

### GCM — GMS Confluence Markup

Local copies of Confluence pages are stored in **GCM format** (`.gcm` files), a custom
line-oriented markup designed for lossless round-tripping of Confluence storage HTML.
See `scripts/confluence/GCM_SPEC.md` for the full format specification.

Key syntax:
- Headings: `= H1`, `== H2`, `=== H3`
- Bold/italic: `**bold**`, `*italic*`
- Links: `[text](url)`, `{link page="Page Title"}text{/link}`
- Jira issues: `{jira:GMS-10}`
- Tables: `{table}…{/table}` with full `rowspan`/`colspan` support
- Images: `{image file="diagram.png" height=400}`
- Raw passthrough: `{raw}…{/raw}` for any unrecognized Confluence XML

### Syncing

Fetch pages from Confluence up to a given work package:

```sh
python3 scripts/confluence/confluence_sync.py --up-to 5.4
python3 scripts/confluence/confluence_sync.py --up-to 5.4 --dry-run
python3 scripts/confluence/confluence_sync.py --up-to 5.4 --force
```

Pages are fetched in ascending WP order, converted from Confluence storage HTML to GCM,
and written to `documentation/confluence/cloud/*.gcm`. Version caching enables incremental sync.

### Pushing Changes

```sh
python3 scripts/confluence/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.gcm
python3 scripts/confluence/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.gcm --dry-run
```

- Only pushes if local file differs from last sync (hash-based detection)
- Detects Confluence version conflicts
- Use `--dry-run` to preview the converted XHTML without pushing
- Use `--no-confirm` to skip the confirmation prompt

### Editing Workflow

1. Edit the `.gcm` file in `documentation/confluence/cloud/`
2. Push back to Confluence using `scripts/confluence/confluence_push.py`

---

## Work Logging

`scripts/logging/log_work.py` tracks completed GMS work and links it to PBL26 course board tickets for `adrian.vremere`.

### Log a completed task

```sh
python3 scripts/logging/log_work.py log \
  --task "Updated WP5.4 review sign-off section" \
  --score 7 \
  --files "documentation/confluence/wip/WP5.4_Review.gcm" \
  [--details "Added traceability table"] \
  [--ticket PBL26-563]
```

`--score` (1–10, default 5) weights how much of the total work time is attributed to this task relative to others in the same period. `--ticket` is auto-detected from the WP number; if detection fails, candidates are printed and you re-run with `--ticket`.

Each entry is saved as `logging/YYYY-MM-DDTHHMMSS.json`.

### Post worklogs to Jira

```sh
python3 scripts/logging/log_work.py worklog --from 2026-03-10 [--to 2026-03-12] [--hours 6]
```

Reads all log entries in the date range and POSTs a worklog to each entry's Jira ticket. Hours (default 6) are split proportionally by score and rounded to the nearest 5 minutes. Duplicate-safe: skips any entry whose task description already appears as a worklog comment on that ticket.

### Log work directly to Jira (no local file)

```sh
python3 scripts/logging/log_work.py log-direct \
  --ticket 5.4 \
  --task "Filled in WP5.4 risk table" \
  --hours 1.5 \
  [--date 2026-03-11]
```

Posts a worklog straight to Jira without creating a local log file. Use for work done outside of Claude. `--ticket` accepts a WP number (`5.4`) or full key (`PBL26-563`). `--hours` supports decimals; `--date` defaults to today.

### Workshop day logging

```sh
python3 scripts/logging/log_work.py report-log --date 2026-03-12
python3 scripts/logging/log_work.py report-log --date 2026-03-12 --task "Custom desc 1" "Custom desc 2"
```

Posts two fixed worklogs to `PBL26-1362` (the tracking/attendance ticket) for a class workshop day:
- `15:15` — 1h 30m — default: `"Attended PBL26 workshop session"`
- `19:00` — 1h 30m — default: `"Continued GMS project work during lab"`

`--task` is optional (up to 2 overrides). `--date` defaults to today.

### Weekly standup report

```sh
python3 scripts/logging/log_work.py report --from 2026-03-10 [--to 2026-03-16]
```

Fetches all worklogs from every PBL26 ticket in the date range and prints a standup-style summary: what was done, what's next (first WP with no worklogs), total hours logged.

### PBL26 ticket utilities

```sh
# List all PBL26 tickets for adrian.vremere
python3 scripts/logging/log_work.py list-tickets

# Show available status transitions for a ticket
python3 scripts/logging/log_work.py list-transitions PBL26-563

# Move one or more tickets to a new status
python3 scripts/logging/log_work.py move --to "Resolve Issue" PBL26-563
python3 scripts/logging/log_work.py move --to "Start Progress" PBL26-548 PBL26-553
```

`--to` matches case-insensitively (e.g. `--to resolve`). Available transitions: **Start Progress**, **Resolve Issue**, **Close Issue**, **Rejected**.
