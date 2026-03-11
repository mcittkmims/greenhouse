from collections import OrderedDict
from datetime import datetime, timezone


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


def slugify(text):
    return "-".join("".join(ch.lower() if ch.isalnum() else " " for ch in text).split()) or "column"


def make_unique_slug(base, seen):
    count = seen.get(base, 0) + 1
    seen[base] = count
    return base if count == 1 else f"{base}-{count}"


def normalize_description(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    import json
    return json.dumps(value, ensure_ascii=True, indent=2)


def normalize_comment(raw):
    author = raw.get("author") or {}
    update_author = raw.get("updateAuthor") or {}
    return {
        "id": raw.get("id") or "",
        "body": normalize_description(raw.get("body")),
        "created": raw.get("created") or "",
        "updated": raw.get("updated") or "",
        "author": {
            "displayName": author.get("displayName") or "Unknown user",
            "name": author.get("name") or author.get("accountId") or "",
        },
        "updateAuthor": {
            "displayName": update_author.get("displayName") or "",
            "name": update_author.get("name") or update_author.get("accountId") or "",
        },
    }


def normalize_issue(raw, base_url, column_id, epic_field_id="", epic_name_by_key=None):
    fields = raw.get("fields", {})
    assignee = fields.get("assignee") or {}
    reporter = fields.get("reporter") or {}
    issue_type_data = fields.get("issuetype") or {}
    priority_data = fields.get("priority") or {}
    issue_type = issue_type_data.get("name", "Issue")
    priority = priority_data.get("name", "")
    parent = fields.get("parent") or {}
    avatar_urls = assignee.get("avatarUrls") or {}
    epic_key = fields.get(epic_field_id, "") if epic_field_id else ""
    return {
        "key": raw["key"],
        "summary": fields.get("summary") or "",
        "description": normalize_description(fields.get("description")),
        "status": (fields.get("status") or {}).get("name", "Unknown"),
        "assigneeDisplay": assignee.get("displayName") or "",
        "assigneeName": assignee.get("name") or assignee.get("accountId") or "",
        "assigneeAvatarUrl": avatar_urls.get("24x24") or avatar_urls.get("32x32") or "",
        "reporterDisplay": reporter.get("displayName") or "",
        "reporterName": reporter.get("name") or reporter.get("accountId") or "",
        "priority": priority,
        "priorityColor": PRIORITY_COLOR.get(priority, "#c1c7d0"),
        "priorityIconUrl": priority_data.get("iconUrl") or "",
        "issueType": issue_type,
        "issueTypeIcon": TYPE_ICON.get(issue_type, issue_type[:2].upper()),
        "issueTypeIconUrl": issue_type_data.get("iconUrl") or "",
        "dueDate": fields.get("duedate") or "",
        "parentKey": parent.get("key") or "",
        "labels": fields.get("labels") or [],
        "epicKey": epic_key or "",
        "epicName": (epic_name_by_key or {}).get(epic_key, "") if epic_key else "",
        "created": fields.get("created") or "",
        "updated": fields.get("updated") or "",
        "onlineUrl": f"{base_url}/browse/{raw['key']}",
        "columnId": column_id,
    }


def build_issue_payload(client, key, column_id=""):
    issue = client.fetch_issue(key)
    normalized = normalize_issue(issue, client.base_url, column_id)
    comments = (issue.get("fields", {}).get("comment") or {}).get("comments", [])
    normalized["comments"] = [normalize_comment(comment) for comment in comments]

    # Resolve which columns are reachable via available Jira transitions
    transitions = client.fetch_transitions(key)
    reachable_status_ids = set()
    for t in transitions:
        to_id = str((t.get("to") or {}).get("id", ""))
        if to_id:
            reachable_status_ids.add(to_id)

    board_payload = build_board_payload(client)
    reachable_column_ids = []
    for col in board_payload["columns"]:
        if col["id"] == column_id:
            reachable_column_ids.append(col["id"])  # current column always selectable
            continue
        for status in col["statuses"]:
            if str(status.get("id", "")) in reachable_status_ids:
                reachable_column_ids.append(col["id"])
                break
    normalized["reachableColumnIds"] = reachable_column_ids

    return normalized


def build_board_payload(client):
    board = client.fetch_board()
    config = client.fetch_board_configuration()
    epic_field_id = ""
    if config:
        epic_field_id = ((config.get("estimation") or {}).get("globalConfig") or {}).get("epicConfig", {}).get("epicLinkFieldId", "")
        if not epic_field_id:
            epic_field_id = (config.get("columnConfig") or {}).get("epicConfig", {}).get("epicLinkFieldId", "")
        if not epic_field_id:
            epic_field_id = (config.get("epicConfig") or {}).get("epicLinkFieldId", "")
        if not epic_field_id:
            epic_field_id = ((config.get("globalConfig") or {}).get("epicConfig") or {}).get("epicLinkFieldId", "")

    extra_fields = [epic_field_id] if epic_field_id else []
    issues = client.fetch_all_issues(extra_fields=extra_fields)
    epic_name_by_key = {
        issue["key"]: (issue.get("fields") or {}).get("summary") or issue["key"]
        for issue in issues
    }

    if config and config.get("columnConfig", {}).get("columns"):
        columns = []
        seen_column_ids = {}
        for column in config["columnConfig"]["columns"]:
            statuses = column.get("statuses", [])
            if not statuses:
                continue
            column_id = make_unique_slug(slugify(column["name"]), seen_column_ids)
            columns.append({
                "id": column_id,
                "name": column["name"],
                "statuses": statuses,
                "issues": [],
            })
    else:
        grouped = OrderedDict()
        for issue in issues:
            name = (issue.get("fields", {}).get("status") or {}).get("name", "Unknown")
            grouped.setdefault(name, []).append(issue)
        seen_column_ids = {}
        columns = [
            {
                "id": make_unique_slug(slugify(name), seen_column_ids),
                "name": name,
                "statuses": [{"name": name}],
                "issues": [],
            }
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
        column["issues"].append(normalize_issue(issue, client.base_url, column["id"], epic_field_id, epic_name_by_key))

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