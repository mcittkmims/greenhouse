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

Open http://127.0.0.1:8765/ while the server runs.
"""

import argparse
import json
import socket
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from board_payloads import build_board_payload, build_issue_payload, resolve_column
from jira_client import ROOT, JiraClient, split_csv
from server_app import JiraBoardApp, RouteResult, json_error_from_exception

BOARD_DIR = ROOT / "documentation" / "jira"


class JiraBoardHandler(BaseHTTPRequestHandler):
    client = JiraClient()
    app = JiraBoardApp(BOARD_DIR, client, build_board_payload, build_issue_payload, resolve_column)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        super().end_headers()

    def log_message(self, fmt, *args):
        return

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        self.send_bytes(status, "application/json; charset=utf-8", body)

    def send_bytes(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_route_result(self, result):
        self.send_bytes(result.status, result.content_type, result.body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        try:
            result = self.app.route_get(self.path)
            if isinstance(result, RouteResult):
                self.send_route_result(result)
                return
            if result is not None:
                status, payload = result
                self.send_json(status, payload)
                return
            self.send_json(404, {"error": "Not found"})
        except Exception as exc:
            status, payload = json_error_from_exception(exc)
            self.send_json(status, payload)

    def do_POST(self):
        try:
            result = self.app.route_post(self.path, self.read_json())
            if result is not None:
                status, payload = result
                self.send_json(status, payload)
                return

            self.send_json(404, {"error": "Not found"})
        except Exception as exc:
            status, payload = json_error_from_exception(exc)
            self.send_json(status, payload)


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
        ThreadingHTTPServer.allow_reuse_address = True
        server = ThreadingHTTPServer((args.host, args.port), JiraBoardHandler)
    except OSError as exc:
        if exc.errno in (48, 98):  # 48=macOS, 98=Linux Address already in use
            print(f"ERROR: Port {args.port} is already in use. Another Jira board server is likely running.")
            sys.exit(1)
        raise
    url = f"http://{args.host}:{args.port}"
    print(f"Jira board server listening on {url}")
    print(f"Open {url}/ in your browser.")
    if not args.no_browser:
        webbrowser.open(url + "/")
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
    serve.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")

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
        args.no_browser = False

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
