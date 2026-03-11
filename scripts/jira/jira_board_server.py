#!/usr/bin/env python3
"""
jira_board_server.py — Local Jira board server plus direct Jira automation commands.

Usage:
    python3 scripts/jira/jira_board_server.py
    python3 scripts/jira/jira_board_server.py serve --port 8765
    python3 scripts/jira/jira_board_server.py assign --assignee adrian.vremere GMS-16 GMS-17
    python3 scripts/jira/jira_board_server.py move --column proposed GMS-35
    python3 scripts/jira/jira_board_server.py bulk-move --column proposed GMS-35 GMS-36
    python3 scripts/jira/jira_board_server.py update --key GMS-35 --summary "New summary"
    python3 scripts/jira/jira_board_server.py comment --key GMS-35 --text "Reviewed"
    python3 scripts/jira/jira_board_server.py bulk-update --summary "New summary" GMS-35 GMS-36
    python3 scripts/jira/jira_board_server.py bulk-comment --text "Reviewed" GMS-35 GMS-36
    python3 scripts/jira/jira_board_server.py create --issue-type Task --summary "New task"
    python3 scripts/jira/jira_board_server.py users --query "Adrian Vremere"

Open documentation/jira/board.html in VS Code Live Preview while the server runs.
"""

import argparse
import json
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed. Run: pip3 install requests")
    sys.exit(1)

ROOT = Path(__file__).parent.parent.parent

PRIORITY_COLOR = {
    "Highest": "#c9372c",
    "High": "#e56910",
    "Medium": "#f5cd47",
    "Low": "#4c9aff",
    "Lowest": "#8590a2",
}

TYPE_ICON = {
    "Story": "S",
    "User Story": "S",
    "Task": "T",
    "Sub-task": "ST",
    "Bug": "B",
    "Epic": "E",
    "Improvement": "I",
    "Job Story": "J",
}


def load_env():
    env_path = ROOT / ".env"
    if not env_path.exists():
        print(f"ERROR: .env not found at {env_path}")
        sys.exit(1)
    env = {}
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip()
    return env


def load_config():
    config_path = ROOT / "documentation" / "confluence" / "confluence_pages.json"
    if not config_path.exists():
        print(f"ERROR: Config not found at {config_path}")
        sys.exit(1)
    return json.loads(config_path.read_text())


def slugify(text):
    return "-".join("".join(ch.lower() if ch.isalnum() else " " for ch in text).split()) or "column"


def normalize_description(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=True, indent=2)


def split_csv(value):
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


class JiraClient:
    def __init__(self):
        self.env = load_env()
        self.config = load_config()
        self.base_url = self.env.get("JIRA_URL", "http://jira.microlab.club")
        self.auth = (
            self.env.get("JIRA_USER") or self.env.get("CONFLUENCE_USER"),
            self.env.get("JIRA_PASS") or self.env.get("CONFLUENCE_PASS"),
        )
        if not self.auth[0] or not self.auth[1]:
            raise SystemExit("ERROR: Missing Jira credentials in .env")
        self.board_id = self.config.get("jira_board_id")
        if not self.board_id:
            raise SystemExit("ERROR: Missing jira_board_id in documentation/confluence/confluence_pages.json")

    def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        response = requests.request(method, url, auth=self.auth, timeout=30, **kwargs)
        response.raise_for_status()
        if response.content:
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()
        return None

    def fetch_board(self):
        return self.request("GET", f"/rest/agile/1.0/board/{self.board_id}")

    def fetch_board_configuration(self):
        try:
            return self.request("GET", f"/rest/agile/1.0/board/{self.board_id}/configuration")
        except requests.HTTPError:
            return None

    def fetch_all_issues(self):
        issues = []
        start_at = 0
        max_results = 100
        while True:
            data = self.request(
                "GET",
                f"/rest/agile/1.0/board/{self.board_id}/issue"
                f"?maxResults={max_results}&startAt={start_at}"
                "&fields=summary,status,assignee,priority,issuetype,duedate,parent,description,labels",
            )
            batch = data.get("issues", [])
            issues.extend(batch)
            start_at += len(batch)
            if start_at >= data.get("total", 0) or not batch:
                break
        return issues

    def fetch_issue(self, key):
        return self.request(
            "GET",
            f"/rest/api/2/issue/{key}?fields=summary,description,status,assignee,priority,issuetype,duedate,parent,labels",
        )

    def fetch_transitions(self, key):
        data = self.request("GET", f"/rest/api/2/issue/{key}/transitions")
        return data.get("transitions", [])

    def search_users(self, query):
        return self.request("GET", f"/rest/api/2/user/search?username={quote(query)}")

    def project_key(self):
        configured = self.config.get("jira_project_key")
        if configured:
            return configured
        issues = self.fetch_all_issues()
        if not issues:
            raise ValueError("Unable to infer Jira project key from board issues")
        return issues[0]["key"].split("-", 1)[0]

    def update_issue(self, key, payload):
        fields = {}
        if "summary" in payload:
            fields["summary"] = payload["summary"]
        if "description" in payload:
            fields["description"] = payload["description"]
        if "dueDate" in payload:
            fields["duedate"] = payload["dueDate"] or None
        if "assigneeName" in payload:
            assignee_name = (payload["assigneeName"] or "").strip()
            fields["assignee"] = None if not assignee_name else {"name": assignee_name}
        if "priority" in payload:
            priority_name = (payload["priority"] or "").strip()
            if priority_name:
                fields["priority"] = {"name": priority_name}
        if "labels" in payload:
            fields["labels"] = payload["labels"]
        if not fields:
            return
        self.request("PUT", f"/rest/api/2/issue/{key}", json={"fields": fields})

    def bulk_assign(self, keys, assignee_name):
        for key in keys:
            self.update_issue(key, {"assigneeName": assignee_name})

    def bulk_update(self, keys, payload):
        for key in keys:
            self.update_issue(key, payload)

    def move_issue_to_column(self, key, column):
        transitions = self.fetch_transitions(key)
        target_status_names = {status["name"] for status in column["statuses"]}
        chosen = None
        for transition in transitions:
            to_status = (transition.get("to") or {}).get("name")
            if to_status in target_status_names or transition.get("name") in target_status_names:
                chosen = transition
                break
        if not chosen:
            raise ValueError(f"No valid transition from {key} to column '{column['name']}'")
        self.request(
            "POST",
            f"/rest/api/2/issue/{key}/transitions",
            json={"transition": {"id": chosen["id"]}},
        )

    def add_comment(self, key, text):
        self.request("POST", f"/rest/api/2/issue/{key}/comment", json={"body": text})

    def bulk_comment(self, keys, text):
        for key in keys:
            self.add_comment(key, text)

    def create_issue(self, payload):
        fields = {
            "project": {"key": payload.get("projectKey") or self.project_key()},
            "summary": payload["summary"],
            "issuetype": {"name": payload.get("issueType") or "Task"},
        }
        if payload.get("description"):
            fields["description"] = payload["description"]
        if payload.get("assigneeName"):
            fields["assignee"] = {"name": payload["assigneeName"]}
        if payload.get("priority"):
            fields["priority"] = {"name": payload["priority"]}
        if payload.get("labels"):
            fields["labels"] = payload["labels"]
        if payload.get("dueDate"):
            fields["duedate"] = payload["dueDate"]
        if payload.get("parentKey"):
            fields["parent"] = {"key": payload["parentKey"]}
        return self.request("POST", "/rest/api/2/issue", json={"fields": fields})


def normalize_issue(raw, base_url, column_id):
    fields = raw.get("fields", {})
    assignee = fields.get("assignee") or {}
    issue_type = (fields.get("issuetype") or {}).get("name", "Issue")
    priority = (fields.get("priority") or {}).get("name", "")
    parent = fields.get("parent") or {}
    return {
        "key": raw["key"],
        "summary": fields.get("summary") or "",
        "description": normalize_description(fields.get("description")),
        "status": (fields.get("status") or {}).get("name", "Unknown"),
        "assigneeDisplay": assignee.get("displayName") or "",
        "assigneeName": assignee.get("name") or assignee.get("accountId") or "",
        "priority": priority,
        "priorityColor": PRIORITY_COLOR.get(priority, "#c1c7d0"),
        "issueType": issue_type,
        "issueTypeIcon": TYPE_ICON.get(issue_type, issue_type[:2].upper()),
        "dueDate": fields.get("duedate") or "",
        "parentKey": parent.get("key") or "",
        "labels": fields.get("labels") or [],
        "onlineUrl": f"{base_url}/browse/{raw['key']}",
        "columnId": column_id,
    }


def build_board_payload(client):
    board = client.fetch_board()
    config = client.fetch_board_configuration()
    issues = client.fetch_all_issues()

    if config and config.get("columnConfig", {}).get("columns"):
        columns = []
        for column in config["columnConfig"]["columns"]:
            columns.append({
                "id": slugify(column["name"]),
                "name": column["name"],
                "statuses": column.get("statuses", []),
                "issues": [],
            })
    else:
        grouped = OrderedDict()
        for issue in issues:
            name = (issue.get("fields", {}).get("status") or {}).get("name", "Unknown")
            grouped.setdefault(name, []).append(issue)
        columns = [
            {"id": slugify(name), "name": name, "statuses": [{"name": name}], "issues": []}
            for name in grouped.keys()
        ]

    def find_column(issue):
        status = issue.get("fields", {}).get("status") or {}
        status_id = str(status.get("id", ""))
        status_name = status.get("name", "Unknown")
        for column in columns:
            for mapped in column["statuses"]:
                if str(mapped.get("id", "")) == status_id or mapped.get("name") == status_name:
                    return column
        return columns[0]

    for issue in issues:
        column = find_column(issue)
        column["issues"].append(normalize_issue(issue, client.base_url, column["id"]))

    for column in columns:
        column["issues"].sort(key=lambda item: item["key"])

    return {
        "board": {
            "id": board["id"],
            "name": board.get("name") or f"Board {client.board_id}",
            "onlineUrl": f"{client.base_url}/secure/RapidBoard.jspa?rapidView={client.board_id}",
        },
        "columns": columns,
        "updatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }


def resolve_column(client, value):
    board_payload = build_board_payload(client)
    columns = board_payload["columns"]
    wanted = value.strip().lower()
    for column in columns:
        if column["id"] == wanted or column["name"].strip().lower() == wanted:
            return column
    raise ValueError(f"Unknown column '{value}'")


class JiraBoardHandler(BaseHTTPRequestHandler):
    client = JiraClient()

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        super().end_headers()

    def log_message(self, fmt, *args):
        return

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        try:
            if path == "/api/board":
                self.send_json(200, build_board_payload(self.client))
                return
            if path == "/api/users":
                term = (query.get("query") or [""])[0]
                self.send_json(200, self.client.search_users(term))
                return
            self.send_json(404, {"error": "Not found"})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            if path == "/api/issues/create":
                payload = self.read_json()
                created = self.client.create_issue(payload)
                self.send_json(200, created)
                return

            if path == "/api/issues/bulk-assign":
                payload = self.read_json()
                self.client.bulk_assign(payload.get("keys", []), payload.get("assigneeName", ""))
                self.send_json(200, {"ok": True})
                return

            if path == "/api/issues/bulk-move":
                payload = self.read_json()
                column = resolve_column(self.client, payload.get("columnId", ""))
                for key in payload.get("keys", []):
                    self.client.move_issue_to_column(key, column)
                self.send_json(200, {"ok": True})
                return

            if path == "/api/issues/bulk-update":
                payload = self.read_json()
                self.client.bulk_update(payload.get("keys", []), payload.get("fields", {}))
                self.send_json(200, {"ok": True})
                return

            if path == "/api/issues/bulk-comment":
                payload = self.read_json()
                self.client.bulk_comment(payload.get("keys", []), payload.get("text", ""))
                self.send_json(200, {"ok": True})
                return

            if path.startswith("/api/issues/") and path.endswith("/move"):
                key = path.split("/")[3]
                payload = self.read_json()
                column = resolve_column(self.client, payload.get("columnId", ""))
                self.client.move_issue_to_column(key, column)
                self.send_json(200, {"ok": True})
                return

            if path.startswith("/api/issues/") and path.endswith("/comment"):
                key = path.split("/")[3]
                payload = self.read_json()
                self.client.add_comment(key, payload.get("text", ""))
                self.send_json(200, {"ok": True})
                return

            if path.startswith("/api/issues/"):
                key = path.split("/")[3]
                payload = self.read_json()
                self.client.update_issue(key, payload)
                self.send_json(200, {"ok": True})
                return

            self.send_json(404, {"error": "Not found"})
        except requests.HTTPError as exc:
            response_text = exc.response.text if exc.response is not None else str(exc)
            self.send_json(502, {"error": response_text})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})


def cmd_users(client, args):
    users = client.search_users(args.query)
    for user in users:
        print(json.dumps({
            "name": user.get("name"),
            "displayName": user.get("displayName"),
            "active": user.get("active"),
        }, ensure_ascii=True))


def cmd_assign(client, args):
    client.bulk_assign(args.keys, args.assignee)
    print(f"Assigned {len(args.keys)} issues to {args.assignee}")


def cmd_move(client, args):
    column = resolve_column(client, args.column)
    for key in args.keys:
        client.move_issue_to_column(key, column)
        print(f"Moved {key} -> {column['name']}")


def cmd_bulk_move(client, args):
    column = resolve_column(client, args.column)
    for key in args.keys:
        client.move_issue_to_column(key, column)
    print(f"Moved {len(args.keys)} issues -> {column['name']}")


def cmd_update(client, args):
    payload = {}
    if args.summary is not None:
        payload["summary"] = args.summary
    if args.description is not None:
        payload["description"] = args.description
    if args.due_date is not None:
        payload["dueDate"] = args.due_date
    if args.assignee is not None:
        payload["assigneeName"] = args.assignee
    if args.priority is not None:
        payload["priority"] = args.priority
    if args.labels is not None:
        payload["labels"] = split_csv(args.labels)
    client.update_issue(args.key, payload)
    if args.column is not None:
        column = resolve_column(client, args.column)
        client.move_issue_to_column(args.key, column)
    print(f"Updated {args.key}")


def cmd_bulk_update(client, args):
    payload = {}
    if args.summary is not None:
        payload["summary"] = args.summary
    if args.description is not None:
        payload["description"] = args.description
    if args.due_date is not None:
        payload["dueDate"] = args.due_date
    if args.assignee is not None:
        payload["assigneeName"] = args.assignee
    if args.priority is not None:
        payload["priority"] = args.priority
    if args.labels is not None:
        payload["labels"] = split_csv(args.labels)
    client.bulk_update(args.keys, payload)
    if args.column is not None:
        column = resolve_column(client, args.column)
        for key in args.keys:
            client.move_issue_to_column(key, column)
    print(f"Updated {len(args.keys)} issues")


def cmd_comment(client, args):
    client.add_comment(args.key, args.text)
    print(f"Added comment to {args.key}")


def cmd_bulk_comment(client, args):
    client.bulk_comment(args.keys, args.text)
    print(f"Added comment to {len(args.keys)} issues")


def cmd_create(client, args):
    created = client.create_issue({
        "projectKey": args.project,
        "summary": args.summary,
        "description": args.description,
        "issueType": args.issue_type,
        "assigneeName": args.assignee,
        "priority": args.priority,
        "labels": split_csv(args.labels),
        "dueDate": args.due_date,
        "parentKey": args.parent,
    })
    print(created.get("key", json.dumps(created, ensure_ascii=True)))


def run_server(args):
    try:
        server = ThreadingHTTPServer((args.host, args.port), JiraBoardHandler)
    except OSError as exc:
        if exc.errno == 48:
            print(f"ERROR: Port {args.port} is already in use. Another Jira board server is likely running.")
            sys.exit(1)
        raise
    print(f"Jira board server listening on http://{args.host}:{args.port}")
    print("Open documentation/jira/board.html in VS Code Live Preview.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def build_parser():
    parser = argparse.ArgumentParser(description="Serve the local Jira board API and run Jira automation commands.")
    subparsers = parser.add_subparsers(dest="command")

    serve = subparsers.add_parser("serve", help="Start the local Jira board server")
    serve.add_argument("--host", default="127.0.0.1", help="Host to bind")
    serve.add_argument("--port", type=int, default=8765, help="Port to bind")

    users = subparsers.add_parser("users", help="Search Jira users")
    users.add_argument("--query", required=True, help="Display name or username to search")

    assign = subparsers.add_parser("assign", help="Bulk-assign issues")
    assign.add_argument("--assignee", required=True, help="Jira username to assign")
    assign.add_argument("keys", nargs="+", help="Issue keys")

    move = subparsers.add_parser("move", help="Move issues to a column via Jira transitions")
    move.add_argument("--column", required=True, help="Column id or display name")
    move.add_argument("keys", nargs="+", help="Issue keys")

    bulk_move = subparsers.add_parser("bulk-move", help="Move multiple issues to a column via Jira transitions")
    bulk_move.add_argument("--column", required=True, help="Column id or display name")
    bulk_move.add_argument("keys", nargs="+", help="Issue keys")

    update = subparsers.add_parser("update", help="Update one issue")
    update.add_argument("--key", required=True, help="Issue key")
    update.add_argument("--summary", help="New summary")
    update.add_argument("--description", help="New description")
    update.add_argument("--due-date", help="Due date as YYYY-MM-DD, empty string clears it")
    update.add_argument("--assignee", help="Jira username, empty string clears it")
    update.add_argument("--priority", help="Priority name")
    update.add_argument("--labels", help="Comma-separated labels")
    update.add_argument("--column", help="Move to column after update")

    bulk_update = subparsers.add_parser("bulk-update", help="Update multiple issues with the same fields")
    bulk_update.add_argument("--summary", help="New summary")
    bulk_update.add_argument("--description", help="New description")
    bulk_update.add_argument("--due-date", help="Due date as YYYY-MM-DD, empty string clears it")
    bulk_update.add_argument("--assignee", help="Jira username, empty string clears it")
    bulk_update.add_argument("--priority", help="Priority name")
    bulk_update.add_argument("--labels", help="Comma-separated labels")
    bulk_update.add_argument("--column", help="Move all issues to column after update")
    bulk_update.add_argument("keys", nargs="+", help="Issue keys")

    comment = subparsers.add_parser("comment", help="Add a comment to an issue")
    comment.add_argument("--key", required=True, help="Issue key")
    comment.add_argument("--text", required=True, help="Comment body")

    bulk_comment = subparsers.add_parser("bulk-comment", help="Add the same comment to multiple issues")
    bulk_comment.add_argument("--text", required=True, help="Comment body")
    bulk_comment.add_argument("keys", nargs="+", help="Issue keys")

    create = subparsers.add_parser("create", help="Create a new issue")
    create.add_argument("--summary", required=True, help="Issue summary")
    create.add_argument("--issue-type", default="Task", help="Issue type name")
    create.add_argument("--description", help="Issue description")
    create.add_argument("--assignee", help="Jira username")
    create.add_argument("--priority", help="Priority name")
    create.add_argument("--labels", help="Comma-separated labels")
    create.add_argument("--due-date", help="Due date as YYYY-MM-DD")
    create.add_argument("--parent", help="Parent issue key")
    create.add_argument("--project", help="Project key, defaults to board project")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        args.command = "serve"
        args.host = "127.0.0.1"
        args.port = 8765

    if args.command == "serve":
        run_server(args)
        return

    client = JiraClient()

    if args.command == "users":
        cmd_users(client, args)
    elif args.command == "assign":
        cmd_assign(client, args)
    elif args.command == "move":
        cmd_move(client, args)
    elif args.command == "bulk-move":
        cmd_bulk_move(client, args)
    elif args.command == "update":
        cmd_update(client, args)
    elif args.command == "bulk-update":
        cmd_bulk_update(client, args)
    elif args.command == "comment":
        cmd_comment(client, args)
    elif args.command == "bulk-comment":
        cmd_bulk_comment(client, args)
    elif args.command == "create":
        cmd_create(client, args)
    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
