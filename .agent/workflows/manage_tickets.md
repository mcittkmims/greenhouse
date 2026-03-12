---
description: Manage PBL26 Jira tickets transitions
---
# PBL26 Ticket Management

Target the **PBL26 course board** for `adrian.vremere`, not the GMS board. Do not use `jira_board_server.py` for PBL26 operations. Available transitions: **Start Progress**, **Resolve Issue**, **Close Issue**, **Rejected**.

## List tickets
```sh
python3 scripts/logging/log_work.py list-tickets
```

## List transitions for a ticket
```sh
python3 scripts/logging/log_work.py list-transitions <TICKET_KEY>
```

## Move/transition a ticket
```sh
python3 scripts/logging/log_work.py move --to "<TRANSITION_NAME>" <TICKET_KEY>
```
