#!/usr/bin/env python3
"""
log_work.py — Log completed GMS project work and link to a PBL26 Jira ticket.

Commands
--------

log — Record a completed GMS task locally.
    Saves a timestamped JSON entry to logging/YYYY-MM-DDTHHMMSS.json.
    Auto-detects the matching PBL26 ticket from the WP number in --task or --files.
    If detection fails, prints candidates and exits so you can re-run with --ticket.

    python3 scripts/logging/log_work.py log \\
        --task "Updated WP5.4 review section" \\
        --score 7 \\
        --files "documentation/confluence/wip/WP5.4.gcm" \\
        [--details "Added traceability table and review sign-offs"] \\
        [--ticket PBL26-563]

    --score (1-10, default 5): effort weight used when splitting hours in worklog.
    Higher score = more time allocated relative to other tasks in the same period.

list-tickets — Show all PBL26 tickets assigned to adrian.vremere.
    Prints each ticket key, summary, and current status. Useful to find the right
    ticket before logging work or moving a ticket to a new status.

    python3 scripts/logging/log_work.py list-tickets

list-transitions PBL26-XXX — Show which status transitions are available for a ticket.
    Jira only allows specific transitions from each status (e.g. you cannot close a ticket
    that has not been started). Run this first if you are unsure what --to value to use.

    python3 scripts/logging/log_work.py list-transitions PBL26-563

move --to STATUS PBL26-XXX [...] — Move one or more tickets to a new status.
    Matches STATUS case-insensitively (partial match works, e.g. "resolve" -> "Resolve Issue").
    Available transitions: Start Progress, Resolve Issue, Close Issue, Rejected.

    python3 scripts/logging/log_work.py move --to "Start Progress" PBL26-563
    python3 scripts/logging/log_work.py move --to "Resolve Issue" PBL26-563 PBL26-558

worklog --from DATE [--to DATE] [--hours N] — Post time entries to Jira for a date range.
    Reads all local log entries between --from and --to (default: today), totals --hours
    (default 6), splits the hours proportionally by score across tasks, then POSTs a
    worklog entry to each task's PBL26 ticket. Time is rounded to the nearest 5 minutes.

    python3 scripts/logging/log_work.py worklog --from 2026-03-10 --to 2026-03-12 --hours 6

report --from DATE [--to DATE] — Generate a weekly standup-style summary.
    Pulls all worklogs from each PBL26 ticket within the date range and formats them
    as a readable report showing time logged per ticket, total hours, and which WP to
    work on next (first WP with no worklogs posted yet).

    python3 scripts/logging/log_work.py report --from 2026-03-10 --to 2026-03-16

log-direct --ticket WP_OR_KEY --task DESC --hours N [--date YYYY-MM-DD] — Post a worklog
    entry directly to Jira without creating a local log file. Use this for work done
    outside of Claude (manually, on another device, etc.).
    --ticket accepts either a WP number (e.g. 5.4) or a full ticket key (e.g. PBL26-563).
    --hours supports decimals (e.g. 1.5 = 1h 30m), rounded to nearest 5 minutes.
    --date defaults to today if omitted.

    python3 scripts/logging/log_work.py log-direct \\
        --ticket 5.4 \\
        --task "Filled in WP5.4 risk table" \\
        --hours 1.5 \\
        [--date 2026-03-11]

report-log [--date YYYY-MM-DD] [--task DESC1 DESC2] — Post two fixed worklogs to the PBL26
    tracking/report ticket (PBL26-1362) for a class workshop day. Always posts:
      • 15:15 — 1h 30m — first description (default: "Attended PBL26 workshop session")
      • 19:00 — 1h 30m — second description (default: "Continued GMS project work during lab")
    Descriptions are optional — omit --task to use the defaults, or supply 1-2 overrides.

    python3 scripts/logging/log_work.py report-log --date 2026-03-12
    python3 scripts/logging/log_work.py report-log --date 2026-03-12 --task "Custom desc 1" "Custom desc 2"
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError
from base64 import b64encode

ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "logging"
ENV_FILE = ROOT / ".env"

TRACKING_TICKET = "PBL26-1362"
ASSIGNEE = "adrian.vremere"

# WP number → PBL26 ticket key (known active mapping)
WP_TO_TICKET = {
    "1.1": "PBL26-29",
    "1.2": "PBL26-59",
    "2.1": "PBL26-95",
    "2.2": "PBL26-125",
    "2.3": "PBL26-155",
    "3.1": "PBL26-285",
    "3.2": "PBL26-290",
    "3.3": "PBL26-295",
    "3.4": "PBL26-300",
    "4.1": "PBL26-414",
    "4.2": "PBL26-419",
    "4.3": "PBL26-424",
    "5.1": "PBL26-548",
    "5.2": "PBL26-553",
    "5.3": "PBL26-558",
    "5.4": "PBL26-563",
    "6.1": "PBL26-700",
    "6.2": "PBL26-705",
    "6.3": "PBL26-710",
    "6.4": "PBL26-715",
    "6.5": "PBL26-720",
    "7.1": "PBL26-866",
    "7.2": "PBL26-871",
    "7.3": "PBL26-876",
    "7.4": "PBL26-881",
    "8.1": "PBL26-996",
    "8.2": "PBL26-1001",
    "8.3": "PBL26-1006",
    "9.1": "PBL26-1116",
    "9.2": "PBL26-1121",
    "9.3": "PBL26-1126",
    "9.4": "PBL26-1131",
    "10.1": "PBL26-1268",
    "10.2": "PBL26-1273",
    "10.3": "PBL26-1278",
    "10.4": "PBL26-1283",
    "10.5": "PBL26-1288",
}


def load_env():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    env.update(os.environ)
    return env


def _auth_headers(env):
    user = env.get("JIRA_USER") or env.get("CONFLUENCE_USER")
    password = env.get("JIRA_PASS") or env.get("CONFLUENCE_PASS")
    token = b64encode(f"{user}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}", "Accept": "application/json"}


def _base_url(env):
    return (env.get("JIRA_URL") or env.get("CONFLUENCE_URL", "").replace("confluence", "jira")).rstrip("/")


def jira_get(env, path):
    url = _base_url(env) + path
    req = Request(url, headers=_auth_headers(env))
    with urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def jira_post(env, path, payload):
    url = _base_url(env) + path
    body = json.dumps(payload).encode()
    headers = {**_auth_headers(env), "Content-Type": "application/json"}
    req = Request(url, data=body, headers=headers, method="POST")
    with urlopen(req, timeout=10) as resp:
        raw = resp.read()
        return json.loads(raw) if raw else {}


def fetch_tickets(env):
    jql = (
        f"project=PBL26 AND assignee={ASSIGNEE} AND key != {TRACKING_TICKET}"
        " ORDER BY status ASC, key ASC"
    )
    qs = urlencode({"jql": jql, "fields": "key,summary,status", "maxResults": "60"})
    data = jira_get(env, f"/rest/api/2/search?{qs}")
    return data.get("issues", [])


def extract_wp(text):
    """Return WP number string like '5.4' from text, or None."""
    m = re.search(r'\bWP\s*(\d+\.\d+)\b', text, re.IGNORECASE)
    return m.group(1) if m else None


def auto_match_ticket(task, files):
    """Try to find WP number in task or file paths and return a ticket key."""
    for source in ([task] + (files or [])):
        wp = extract_wp(source)
        if wp and wp in WP_TO_TICKET:
            return WP_TO_TICKET[wp]
    return None


def cmd_list_tickets(env):
    try:
        tickets = fetch_tickets(env)
    except URLError as e:
        print(f"ERROR: Could not reach Jira: {e}", file=sys.stderr)
        sys.exit(1)
    for t in tickets:
        status = t["fields"]["status"]["name"]
        print(f"{t['key']}\t{status}\t{t['fields']['summary']}")


def cmd_log(env, args):
    files = args.files or []
    ticket = args.ticket

    # Auto-match ticket if not provided
    if not ticket:
        ticket = auto_match_ticket(args.task, files)

    # If still no ticket, fetch live and try to match; otherwise print candidates
    if not ticket:
        try:
            live_tickets = fetch_tickets(env)
        except URLError as e:
            print(f"ERROR: Could not reach Jira: {e}", file=sys.stderr)
            sys.exit(1)

        # Try matching against summaries
        for t in live_tickets:
            wp = extract_wp(t["fields"]["summary"])
            if wp:
                match_source = args.task + " " + " ".join(files)
                if wp in match_source or f"WP{wp}" in match_source.replace(" ", ""):
                    ticket = t["key"]
                    break

        if not ticket:
            print("Could not auto-match a PBL26 ticket. Active tickets for adrian.vremere:\n")
            for t in live_tickets:
                status = t["fields"]["status"]["name"]
                print(f"  {t['key']}\t{status}\t{t['fields']['summary'][:70]}")
            print("\nRe-run with --ticket PBL26-XXX to specify manually.")
            sys.exit(2)

    # Build and write log entry
    ts = datetime.now().strftime("%Y-%m-%dT%H%M%S")
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "task": args.task,
        "pbl26_ticket": ticket,
    }
    if args.score is not None:
        entry["score"] = args.score
    if args.details:
        entry["details"] = args.details
    if files:
        entry["files_changed"] = files

    log_file = LOG_DIR / f"{ts}.json"
    log_file.write_text(json.dumps(entry, indent=2, ensure_ascii=True) + "\n")
    print(f"Logged → {log_file.relative_to(ROOT)}  (ticket: {ticket})")


def fetch_transitions(env, key):
    data = jira_get(env, f"/rest/api/2/issue/{key}/transitions")
    return data.get("transitions", [])


def resolve_transition(transitions, name):
    """Match a transition by exact name or case-insensitive substring."""
    name_lower = name.lower()
    exact = [t for t in transitions if t["name"].lower() == name_lower]
    if exact:
        return exact[0]
    partial = [t for t in transitions if name_lower in t["name"].lower()]
    if len(partial) == 1:
        return partial[0]
    if len(partial) > 1:
        names = ", ".join(f'"{t["name"]}"' for t in partial)
        print(f"ERROR: '{name}' is ambiguous — matches: {names}", file=sys.stderr)
        sys.exit(1)
    names = ", ".join(f'"{t["name"]}"' for t in transitions)
    print(f"ERROR: No transition matching '{name}'. Available: {names}", file=sys.stderr)
    sys.exit(1)


def cmd_list_transitions(env, args):
    try:
        transitions = fetch_transitions(env, args.key)
    except URLError as e:
        print(f"ERROR: Could not reach Jira: {e}", file=sys.stderr)
        sys.exit(1)
    for t in transitions:
        print(f"{t['id']}\t{t['name']}")


def parse_date(s):
    """Parse YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS into a naive datetime."""
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(f"Cannot parse date '{s}'. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS.")


def minutes_to_jira(total_minutes):
    """Convert total minutes to Jira timeSpent string like '2h 30m', rounded to nearest 5."""
    total_minutes = max(5, round(total_minutes / 5) * 5)
    h, m = divmod(total_minutes, 60)
    if h and m:
        return f"{h}h {m}m"
    if h:
        return f"{h}h"
    return f"{m}m"


def to_jira_started(dt):
    """Format a naive local datetime as Jira's started field (with local UTC offset)."""
    local_offset = datetime.now(timezone.utc).astimezone().utcoffset()
    total_seconds = int(local_offset.total_seconds())
    sign = "+" if total_seconds >= 0 else "-"
    abs_seconds = abs(total_seconds)
    hh, mm = divmod(abs_seconds // 60, 60)
    return dt.strftime(f"%Y-%m-%dT%H:%M:%S.000{sign}{hh:02d}{mm:02d}")


def load_log_entries(start_dt, end_dt):
    """Return log entries (dict + path) with timestamps in [start_dt, end_dt], sorted."""
    entries = []
    for f in sorted(LOG_DIR.glob("*.json")):
        if f.name == "schema.json":
            continue
        try:
            data = json.loads(f.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        ts_str = data.get("timestamp", "")
        try:
            ts = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
        if start_dt <= ts <= end_dt:
            entries.append((ts, data, f))
    return entries


def resolve_ticket_arg(ticket_arg):
    """Accept either 'PBL26-XXX' or 'X.Y' WP number and return the PBL26 key."""
    if re.match(r'^\d+\.\d+$', ticket_arg):
        wp = ticket_arg
        if wp in WP_TO_TICKET:
            return WP_TO_TICKET[wp]
        print(f"ERROR: WP {wp} not found in the WP_TO_TICKET map.", file=sys.stderr)
        sys.exit(1)
    return ticket_arg  # already a PBL26-XXX key


def fetch_worklog_comments(env, ticket):
    """Return a set of comment strings already posted to a ticket's worklog."""
    try:
        data = jira_get(env, f"/rest/api/2/issue/{ticket}/worklog")
        return {wl.get("comment", "").strip() for wl in data.get("worklogs", [])}
    except Exception:
        return set()


def cmd_log_direct(env, args):
    ticket = resolve_ticket_arg(args.ticket)
    task = args.task
    time_str = minutes_to_jira(args.hours * 60)

    dt = datetime.now()
    if args.date:
        try:
            dt = parse_date(args.date)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)

    started = to_jira_started(dt)
    payload = {"started": started, "timeSpent": time_str, "comment": task}
    try:
        result = jira_post(env, f"/rest/api/2/issue/{ticket}/worklog", payload)
        worklog_id = result.get("id", "?")
        print(f"OK  {ticket}  {time_str}  [{dt.strftime('%Y-%m-%d')}]  \"{task}\"  (worklog {worklog_id})")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_worklog(env, args):
    try:
        start_dt = parse_date(args.start)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    end_dt = datetime.now() if not args.end else None
    if args.end:
        try:
            end_dt = parse_date(args.end)
            # If only a date was given, treat it as end of that day
            if "T" not in args.end:
                end_dt = end_dt.replace(hour=23, minute=59, second=59)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)

    entries = load_log_entries(start_dt, end_dt)

    if not entries:
        print(f"No log entries found between {start_dt.date()} and {end_dt.date()}.")
        sys.exit(0)

    DEFAULT_SCORE = 5.0
    total_minutes = args.hours * 60
    scores = [data.get("score", DEFAULT_SCORE) for _, data, _ in entries]
    total_score = sum(scores)

    print(f"Found {len(entries)} entries — {args.hours}h total (weighted by score)\n")

    errors = []
    for (ts, data, f), score in zip(entries, scores):
        ticket = data.get("pbl26_ticket", "")
        task = data.get("task", "(no description)")
        if not ticket:
            print(f"  SKIP  {f.name}  (no pbl26_ticket field)")
            continue
        # Duplicate check: skip if this exact comment was already posted
        existing_comments = fetch_worklog_comments(env, ticket)
        if task in existing_comments:
            print(f"  SKIP  {ticket}  [{ts.strftime('%Y-%m-%d')}]  \"{task[:55]}\"  (already posted)")
            continue
        task_minutes = (score / total_score) * total_minutes
        time_str = minutes_to_jira(task_minutes)
        started = to_jira_started(ts)
        payload = {"started": started, "timeSpent": time_str, "comment": task}
        try:
            result = jira_post(env, f"/rest/api/2/issue/{ticket}/worklog", payload)
            worklog_id = result.get("id", "?")
            score_label = f"score={score}" if data.get("score") is not None else f"score={DEFAULT_SCORE}(default)"
            print(f"  OK    {ticket}  {time_str}  [{ts.strftime('%Y-%m-%d')}]  {score_label}  \"{task[:55]}\"  (worklog {worklog_id})")
        except Exception as e:
            msg = f"  FAIL  {ticket}  {f.name}: {e}"
            print(msg)
            errors.append(msg)

    if errors:
        print(f"\n{len(errors)} error(s) occurred.")
        sys.exit(1)


def parse_jira_datetime(s):
    """Parse Jira's started field (e.g. '2026-03-12T11:00:00.000+0100') to a naive datetime."""
    m = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", s)
    return datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S") if m else None


def extract_action(summary):
    """Pull the core action out of a PBL26 ticket summary."""
    m = re.search(r"Contribute to:\s*(.+?)\s+for the team", summary, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Fallback: strip WPX.Y prefix and trailing team tag
    s = re.sub(r"^WP\d+\.\d+\s*:\s*", "", summary).strip()
    s = re.sub(r"\s+for the team.*$", "", s, flags=re.IGNORECASE).strip()
    return s


def seconds_to_display(total_seconds):
    """Convert seconds to a human-readable string rounded to nearest 5 minutes."""
    return minutes_to_jira(total_seconds / 60)


def cmd_report(env, args):
    try:
        start_dt = parse_date(args.start)
        if args.end:
            end_dt = parse_date(args.end)
            if "T" not in args.end:
                end_dt = end_dt.replace(hour=23, minute=59, second=59)
        else:
            end_dt = datetime.now()
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Sorted WP keys in ascending order
    sorted_wps = sorted(WP_TO_TICKET.keys(), key=lambda x: [int(n) for n in x.split(".")])

    # Fetch worklogs from Jira for each ticket
    in_range = []        # (wp, comment, seconds) — worklogs inside the date window
    has_any_worklog = set()  # WPs that have ANY worklog (ever)

    print(f"Fetching worklogs from {start_dt.date()} to {end_dt.date()}...", file=sys.stderr)
    for wp in sorted_wps:
        ticket = WP_TO_TICKET[wp]
        try:
            data = jira_get(env, f"/rest/api/2/issue/{ticket}/worklog")
        except Exception as e:
            print(f"  WARN: could not fetch {ticket}: {e}", file=sys.stderr)
            continue
        for wl in data.get("worklogs", []):
            has_any_worklog.add(wp)
            started = parse_jira_datetime(wl.get("started", ""))
            if started and start_dt <= started <= end_dt:
                comment = wl.get("comment", "").strip()
                seconds = wl.get("timeSpentSeconds", 0)
                in_range.append((wp, comment, seconds))

    if not in_range:
        print(f"No worklogs found between {start_dt.date()} and {end_dt.date()}.", file=sys.stderr)
        sys.exit(0)

    # Total time
    total_seconds = sum(s for _, _, s in in_range)
    total_time = seconds_to_display(total_seconds)

    # Next ticket: first WP in order with no worklogs at all
    next_action = None
    next_ticket_key = None
    for wp in sorted_wps:
        if wp not in has_any_worklog:
            next_ticket_key = WP_TO_TICKET[wp]
            try:
                issue = jira_get(env, f"/rest/api/2/issue/{next_ticket_key}?fields=summary")
                next_action = extract_action(issue["fields"]["summary"])
            except Exception:
                next_action = next_ticket_key
            break

    # Build report
    lines = []
    lines.append("What did you do last week to advance the project?\n")
    for _, comment, _ in in_range:
        if comment:
            lines.append(f"    {comment}\n")
    lines.append("")
    lines.append("What will you do this week to advance the project?\n")
    lines.append(f"    {next_action or '-'}\n")
    lines.append("")
    lines.append("What are the impediments in your way?\n")
    lines.append("    -\n")
    lines.append("")
    lines.append("How many hours did you invest and track in the project last week.\n")
    lines.append(f"    {total_time} - to advance the project\n")
    lines.append("")
    lines.append("How many hours do you plan to invest and track in the project next week.\n")
    lines.append("    6h")

    print("\n" + "\n".join(lines))


def cmd_move(env, args):
    try:
        for key in args.keys:
            transitions = fetch_transitions(env, key)
            transition = resolve_transition(transitions, args.to)
            jira_post(env, f"/rest/api/2/issue/{key}/transitions", {"transition": {"id": transition["id"]}})
            print(f"{key} → {transition['name']}")
    except URLError as e:
        print(f"ERROR: Could not reach Jira: {e}", file=sys.stderr)
        sys.exit(1)


REPORT_SLOTS = [
    (15, 15, "Attended PBL26 workshop session"),   # 3:15 PM
    (19,  0, "Continued GMS project work during lab"),  # 7:00 PM
]
REPORT_DURATION = "1h 30m"


def cmd_report_log(env, args):
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    try:
        base_dt = parse_date(date_str)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    user_tasks = args.task or []
    slots = [(h, m, user_tasks[i] if i < len(user_tasks) else default)
             for i, (h, m, default) in enumerate(REPORT_SLOTS)]

    errors = []
    for hour, minute, task in slots:
        dt = base_dt.replace(hour=hour, minute=minute, second=0)
        started = to_jira_started(dt)
        payload = {"started": started, "timeSpent": REPORT_DURATION, "comment": task}
        try:
            result = jira_post(env, f"/rest/api/2/issue/{TRACKING_TICKET}/worklog", payload)
            worklog_id = result.get("id", "?")
            print(f"  OK  {TRACKING_TICKET}  {REPORT_DURATION}  [{dt.strftime('%Y-%m-%d %H:%M')}]  \"{task}\"  (worklog {worklog_id})")
        except Exception as e:
            msg = f"  FAIL  {TRACKING_TICKET}  {dt.strftime('%H:%M')}: {e}"
            print(msg)
            errors.append(msg)

    if errors:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Log GMS work and link to a PBL26 ticket.")
    sub = parser.add_subparsers(dest="command")

    log_p = sub.add_parser("log", help="Write a work log entry (default command)")
    log_p.add_argument("--task", required=True, help="Short description of what was done")
    log_p.add_argument("--score", type=float, help="Effort score 1-10 (used to weight hours in worklog)")
    log_p.add_argument("--details", help="Optional extra context")
    log_p.add_argument("--files", nargs="*", help="Files created or modified (relative paths)")
    log_p.add_argument("--ticket", help="PBL26 ticket key (auto-detected if omitted)")

    sub.add_parser("list-tickets", help="List PBL26 tickets for adrian.vremere")

    lt = sub.add_parser("list-transitions", help="Show available transitions for a ticket")
    lt.add_argument("key", help="PBL26 ticket key (e.g. PBL26-563)")

    move_p = sub.add_parser("move", help="Transition one or more tickets to a new status")
    move_p.add_argument("--to", required=True, help='Transition name (e.g. "Start Progress", "Resolve Issue")')
    move_p.add_argument("keys", nargs="+", help="PBL26 ticket keys")

    rp = sub.add_parser("report", help="Generate weekly standup report from Jira worklogs")
    rp.add_argument("--from", dest="start", required=True, metavar="DATE",
                    help="Start of the reporting period (YYYY-MM-DD)")
    rp.add_argument("--to", dest="end", metavar="DATE",
                    help="End of the reporting period (default: now)")

    wl_p = sub.add_parser("worklog", help="Post Jira worklogs for log entries in a date range")
    wl_p.add_argument("--from", dest="start", required=True, metavar="DATE",
                      help="Start date (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
    wl_p.add_argument("--to", dest="end", metavar="DATE",
                      help="End date (default: now). YYYY-MM-DD treated as end of day.")
    wl_p.add_argument("--hours", type=float, default=6.0,
                      help="Total hours worked in this period (default: 6)")

    rl_p = sub.add_parser("report-log", help=f"Post two fixed worklogs to {TRACKING_TICKET} (15:15 and 19:00, 1h30m each)")
    rl_p.add_argument("--task", nargs="*", metavar="DESC",
                      help="Optional descriptions (up to 2). Omit to use defaults.")
    rl_p.add_argument("--date", metavar="YYYY-MM-DD",
                      help="Date to log work for (default: today)")

    ld_p = sub.add_parser("log-direct", help="Post a worklog directly to Jira (no local log file created)")
    ld_p.add_argument("--ticket", required=True,
                      help="WP number (e.g. 5.4) or full ticket key (e.g. PBL26-563)")
    ld_p.add_argument("--task", required=True, help="Description of what was done")
    ld_p.add_argument("--hours", type=float, required=True,
                      help="Time spent in hours (decimals ok, e.g. 1.5 = 1h 30m)")
    ld_p.add_argument("--date", metavar="YYYY-MM-DD",
                      help="Date the work was done (default: today)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    env = load_env()

    if args.command == "list-tickets":
        cmd_list_tickets(env)
    elif args.command == "list-transitions":
        cmd_list_transitions(env, args)
    elif args.command == "move":
        cmd_move(env, args)
    elif args.command == "report":
        cmd_report(env, args)
    elif args.command == "worklog":
        cmd_worklog(env, args)
    elif args.command == "log":
        cmd_log(env, args)
    elif args.command == "log-direct":
        cmd_log_direct(env, args)
    elif args.command == "report-log":
        cmd_report_log(env, args)


if __name__ == "__main__":
    main()
