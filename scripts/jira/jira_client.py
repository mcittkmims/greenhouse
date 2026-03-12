import json
import sys
from pathlib import Path
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed. Run: pip3 install requests")
    sys.exit(1)


ROOT = Path(__file__).parent.parent.parent


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

    def fetch_all_issues(self, extra_fields=None):
        issues = []
        start_at = 0
        max_results = 100
        fields = [
            "summary",
            "status",
            "assignee",
            "priority",
            "issuetype",
            "duedate",
            "parent",
            "description",
            "labels",
        ]
        if extra_fields:
            fields.extend(extra_fields)
        while True:
            data = self.request(
                "GET",
                f"/rest/agile/1.0/board/{self.board_id}/issue"
                f"?maxResults={max_results}&startAt={start_at}"
                f"&fields={','.join(fields)}",
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
            f"/rest/api/2/issue/{key}?fields=summary,description,status,assignee,priority,issuetype,duedate,parent,labels,reporter,comment,created,updated",
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
        if "epicKey" in payload:
            epic_key = (payload["epicKey"] or "").strip()
            fields["customfield_10100"] = epic_key if epic_key else None
        if not fields:
            return
        self.request("PUT", f"/rest/api/2/issue/{key}", json={"fields": fields})

    def bulk_assign(self, keys, assignee_name):
        for key in keys:
            self.update_issue(key, {"assigneeName": assignee_name})

    def bulk_update(self, keys, payload):
        for key in keys:
            self.update_issue(key, payload)

    def _apply_transition(self, key, transition):
        self.request(
            "POST",
            f"/rest/api/2/issue/{key}/transitions",
            json={"transition": {"id": transition["id"]}},
        )

    def move_issue_to_column(self, key, column, force=False):
        transitions = self.fetch_transitions(key)
        target_status_ids = {str(status["id"]) for status in column["statuses"] if status.get("id")}
        target_status_names = {status["name"] for status in column["statuses"] if status.get("name")}
        chosen = None
        for transition in transitions:
            to = transition.get("to") or {}
            to_id = str(to.get("id", ""))
            to_name = to.get("name", "")
            if to_id in target_status_ids or to_name in target_status_names or transition.get("name") in target_status_names:
                chosen = transition
                break
        if chosen:
            self._apply_transition(key, chosen)
            return
        if not force:
            raise ValueError(
                f"No direct transition from {key} to column '{column['name']}'. "
                f"Use --force to attempt a multi-hop transition."
            )
        # Multi-hop: try every available transition and recurse once
        for transition in transitions:
            self._apply_transition(key, transition)
            hop_transitions = self.fetch_transitions(key)
            for t in hop_transitions:
                to = t.get("to") or {}
                if str(to.get("id", "")) in target_status_ids or to.get("name", "") in target_status_names:
                    self._apply_transition(key, t)
                    return
            # Undo by moving back — not feasible; just try next hop
        raise ValueError(f"Could not reach column '{column['name']}' from {key} even with --force")

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
        if payload.get("epicKey"):
            fields["customfield_10100"] = payload["epicKey"]
        return self.request("POST", "/rest/api/2/issue", json={"fields": fields})