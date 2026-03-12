---
description: Manage PBL26 Jira ticket transitions (course board, NOT GMS board)
---
# PBL26 Ticket Management

> **Board:** PBL26 course board (`scripts/logging/log_work.py`)
> **NOT the GMS board** — never use `jira_board_server.py` here.

Tickets are WP work packages (e.g. `PBL26-548` = WP5.1). Available transitions: **Start Progress**, **Resolve Issue**, **Close Issue**, **Rejected**.

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
