import json
import mimetypes
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests

@dataclass
class RouteResult:
    status: int
    content_type: str
    body: bytes


class StaticAssetServer:
    def __init__(self, board_dir):
        self.routes = {
            "/": board_dir / "board.html",
            "/index.html": board_dir / "board.html",
            "/board.html": board_dir / "board.html",
            "/board.css": board_dir / "board.css",
            "/board.js": board_dir / "board.js",
        }

    def resolve(self, path):
        return self.routes.get(path)

    def serve(self, path):
        file_path = self.resolve(path)
        if not file_path:
            return None
        if not file_path.exists() or not file_path.is_file():
            return RouteResult(404, "application/json; charset=utf-8", json.dumps({"error": "Static asset not found"}).encode("utf-8"))
        content_type, _ = mimetypes.guess_type(str(file_path))
        if not content_type:
            content_type = "application/octet-stream"
        return RouteResult(200, f"{content_type}; charset=utf-8" if content_type.startswith("text/") or content_type in {"application/javascript", "application/json"} else content_type, file_path.read_bytes())


class JiraApiRouter:
    def __init__(self, client, build_board_payload, build_issue_payload, resolve_column):
        self.client = client
        self.build_board_payload = build_board_payload
        self.build_issue_payload = build_issue_payload
        self.resolve_column = resolve_column

    def handle_get(self, path, query):
        if path == "/api/board":
            return 200, self.build_board_payload(self.client)
        if path.startswith("/api/issues/"):
            key = path.split("/")[3]
            board_payload = self.build_board_payload(self.client)
            column_id = ""
            for column in board_payload["columns"]:
                if any(issue["key"] == key for issue in column["issues"]):
                    column_id = column["id"]
                    break
            return 200, self.build_issue_payload(self.client, key, column_id)
        if path == "/api/users":
            term = (query.get("query") or [""])[0]
            return 200, self.client.search_users(term)
        return None

    def handle_post(self, path, payload):
        if path == "/api/issues/create":
            return 200, self.client.create_issue(payload)

        if path == "/api/issues/bulk-assign":
            self.client.bulk_assign(payload.get("keys", []), payload.get("assigneeName", ""))
            return 200, {"ok": True}

        if path == "/api/issues/bulk-move":
            column = self.resolve_column(self.client, payload.get("columnId", ""))
            for key in payload.get("keys", []):
                self.client.move_issue_to_column(key, column)
            return 200, {"ok": True}

        if path == "/api/issues/bulk-update":
            self.client.bulk_update(payload.get("keys", []), payload.get("fields", {}))
            return 200, {"ok": True}

        if path == "/api/issues/bulk-comment":
            self.client.bulk_comment(payload.get("keys", []), payload.get("text", ""))
            return 200, {"ok": True}

        if path.startswith("/api/issues/") and path.endswith("/move"):
            key = path.split("/")[3]
            column = self.resolve_column(self.client, payload.get("columnId", ""))
            self.client.move_issue_to_column(key, column)
            return 200, {"ok": True}

        if path.startswith("/api/issues/") and path.endswith("/comment"):
            key = path.split("/")[3]
            self.client.add_comment(key, payload.get("text", ""))
            return 200, {"ok": True}

        if path.startswith("/api/issues/"):
            key = path.split("/")[3]
            self.client.update_issue(key, payload)
            return 200, {"ok": True}

        return None


class JiraBoardApp:
    def __init__(self, board_dir, client, build_board_payload, build_issue_payload, resolve_column):
        self.api = JiraApiRouter(client, build_board_payload, build_issue_payload, resolve_column)
        self.static_assets = StaticAssetServer(board_dir)

    def route_get(self, raw_path):
        parsed = urlparse(raw_path)
        path = parsed.path or "/"
        query = parse_qs(parsed.query)

        if path.startswith("/api/"):
            return self.api.handle_get(path, query)

        return self.static_assets.serve(path)

    def route_post(self, raw_path, payload):
        parsed = urlparse(raw_path)
        path = parsed.path
        if not path.startswith("/api/"):
            return None
        return self.api.handle_post(path, payload)


def json_error_from_exception(exc):
    if isinstance(exc, requests.HTTPError):
        response_text = exc.response.text if exc.response is not None else str(exc)
        return 502, {"error": response_text}
    return 500, {"error": str(exc)}