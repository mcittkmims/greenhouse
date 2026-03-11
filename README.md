# Greenhouse Management System (GMS)

PBL IoT course project — Technical University of Moldova (UTM)

**Team:** Alexei Maxim, Vremere Adrian, Cojocaru Daniel, Rațeeva Daria, Mutruc Victoria

---

## Repository Structure

```
documentation/
  confluence/
    confluence_pages.json   ← page ID map + config
    cloud/                  ← auto-synced copies fetched from Confluence (do not manually edit)
    wip/                    ← files currently being actively worked on
    resources/              ← local reference/learning materials (not synced to Confluence)
  jira/
    board.html              ← local interactive Jira board shell
scripts/
  confluence/
    confluence_sync.py      ← fetch pages from Confluence
    confluence_push.py      ← push local edits back to Confluence
  jira/
    jira_board_server.py    ← local interactive Jira board API/server + Jira automation commands
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
python3 scripts/jira/jira_board_server.py bulk-move --column proposed GMS-35 GMS-36
python3 scripts/jira/jira_board_server.py update --key GMS-35 --summary "New summary"
python3 scripts/jira/jira_board_server.py bulk-update --assignee adrian.vremere GMS-35 GMS-36
python3 scripts/jira/jira_board_server.py comment --key GMS-35 --text "Reviewed"
python3 scripts/jira/jira_board_server.py bulk-comment --text "Reviewed" GMS-35 GMS-36
python3 scripts/jira/jira_board_server.py create --issue-type Task --summary "New task"
```

---

## Confluence Workflow

Confluence-specific files live only in `documentation/confluence/` and `scripts/confluence/`.

Fetch pages from Confluence up to a given work package:

```sh
python3 scripts/confluence/confluence_sync.py --up-to 5.4
```

Pages are fetched in ascending WP order: 1.1 → 2.1 → 3.1 → 3.2 → 3.3 → 3.4 → 4.1 → 4.2 → 4.3 → 5.1 → 5.2 → 5.3 → 5.4 → ...

---

## Pushing Changes to Confluence

```sh
python3 scripts/confluence/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.md
```

- Shows a diff against the cached cloud copy before pushing
- Use `--dry-run` to preview without pushing
- Use `--no-confirm` to skip the confirmation prompt

---

## Editing Workflow

1. Move the target file from `documentation/confluence/cloud/` to `documentation/confluence/wip/`
2. Edit the file
3. Push back to Confluence using `scripts/confluence/confluence_push.py`
4. Move the file back to `documentation/confluence/cloud/`
