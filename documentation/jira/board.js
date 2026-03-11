const API_BASE = "http://127.0.0.1:8765";

const state = {
  board: null,
  columns: [],
  issueMap: new Map(),
  detailMap: new Map(),
  selectedKey: null,
  loadingKey: null,
  filter: "",
  sortables: [],
};

const boardEl = document.getElementById("board");
const issueDetailPanelEl = document.getElementById("issue-detail-panel");
const detailEmptyEl = document.getElementById("detail-empty");
const issueViewEl = document.getElementById("issue-view");
const boardTitleEl = document.getElementById("board-title");
const boardNameButtonEl = document.getElementById("board-name-button");
const metaTextEl = document.getElementById("meta-text");
const statusBannerEl = document.getElementById("status-banner");
const errorOverlayEl = document.getElementById("error-overlay");
const searchInputEl = document.getElementById("search-input");
const refreshBtnEl = document.getElementById("refresh-btn");
const openOnlineLinkEl = document.getElementById("open-online-link");
const createIssueTriggerEl = document.getElementById("create-issue-trigger");
const createDialogEl = document.getElementById("create-dialog");
const closeCreateDialogEl = document.getElementById("close-create-dialog");
const cancelCreateDialogEl = document.getElementById("cancel-create-dialog");
const createIssueFormEl = document.getElementById("create-issue-form");
const closeIssuePanelEl = document.getElementById("close-issue-panel");

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[char]);
}

function avatarText(name) {
  const clean = String(name || "").trim();
  if (!clean) return "?";
  const parts = clean.split(/\s+/).slice(0, 2);
  const initials = parts.map((part) => part[0]?.toUpperCase() || "").join("");
  return initials || clean.slice(0, 2).toUpperCase();
}

function formatDate(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}

function splitCsv(value) {
  return String(value || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function showStatus(message, tone = "info") {
  statusBannerEl.textContent = message;
  statusBannerEl.style.background = tone === "error" ? "#c9372c" : tone === "success" ? "#1f845a" : "#172b4d";
  statusBannerEl.classList.add("show");
  window.clearTimeout(showStatus._timer);
  showStatus._timer = window.setTimeout(() => statusBannerEl.classList.remove("show"), 2200);
}

async function api(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  if (!response.ok) {
    let errorText = `${response.status} ${response.statusText}`;
    const contentType = response.headers.get("Content-Type") || "";
    if (contentType.includes("application/json")) {
      const payload = await response.json();
      errorText = payload.error || errorText;
    } else {
      errorText = await response.text() || errorText;
    }
    throw new Error(errorText);
  }

  const contentType = response.headers.get("Content-Type") || "";
  return contentType.includes("application/json") ? response.json() : response.text();
}

function iconMarkup(url, fallbackClass, fallbackContent, title, alt) {
  if (url) {
    return `<img src="${escapeHtml(url)}" alt="${escapeHtml(alt)}" title="${escapeHtml(title)}">`;
  }
  return `<span class="${fallbackClass}" title="${escapeHtml(title)}">${escapeHtml(fallbackContent)}</span>`;
}

function cardMatches(issue) {
  const query = state.filter.trim().toLowerCase();
  if (!query) return true;
  return [
    issue.key,
    issue.summary,
    issue.status,
    issue.assigneeDisplay,
    issue.priority,
    issue.issueType,
    issue.epicName,
    ...(issue.labels || []),
  ]
    .filter(Boolean)
    .some((value) => String(value).toLowerCase().includes(query));
}

function destroySortables() {
  state.sortables.forEach((sortable) => sortable.destroy());
  state.sortables = [];
}

function initSortables() {
  destroySortables();
  if (!window.Sortable) {
    showStatus("SortableJS failed to load; drag and drop is unavailable", "error");
    return;
  }

  document.querySelectorAll(".ghx-issues").forEach((listEl) => {
    const sortable = new window.Sortable(listEl, {
      group: "jira-board",
      animation: 140,
      draggable: ".ghx-issue",
      handle: ".js-draggable-trigger",
      ghostClass: "is-dragging",
      onMove(event) {
        if (event.from === event.to) {
          return false;
        }
        return true;
      },
      onStart(event) {
        event.item.querySelector(".ghx-issue-card")?.classList.add("is-dragging");
      },
      async onEnd(event) {
        event.item.querySelector(".ghx-issue-card")?.classList.remove("is-dragging");
        const issueKey = event.item.dataset.issueKey;
        const targetColumnId = event.to.closest(".ghx-column")?.dataset.columnId;
        const sourceColumnId = event.from.closest(".ghx-column")?.dataset.columnId;

        if (!issueKey || !targetColumnId || targetColumnId === sourceColumnId) {
          await loadBoard(true, state.selectedKey);
          return;
        }

        await moveIssueToColumn(issueKey, targetColumnId);
      },
    });
    state.sortables.push(sortable);
  });
}

function syncIssueColumnHeights() {
  const lists = [...document.querySelectorAll(".ghx-issues")];
  if (!lists.length) return;
  for (const listEl of lists) {
    listEl.style.minHeight = "40px";
  }
  const maxHeight = Math.max(...lists.map((listEl) => listEl.scrollHeight), 40);
  for (const listEl of lists) {
    listEl.style.minHeight = `${maxHeight}px`;
  }
}

function closeIssuePanel() {
  state.selectedKey = null;
  state.loadingKey = null;
  issueDetailPanelEl.hidden = true;
  issueDetailPanelEl.classList.remove("is-open");
  issueViewEl.hidden = true;
  detailEmptyEl.hidden = false;
  detailEmptyEl.textContent = "Loading issue...";
  renderBoard();
}

function renderBoard() {
  boardEl.innerHTML = "";
  state.issueMap.clear();

  for (const column of state.columns) {
    const visibleIssues = column.issues.filter(cardMatches);
    const columnEl = document.createElement("section");
    columnEl.className = "ghx-column";
    columnEl.dataset.columnId = column.id;
    columnEl.innerHTML = `
      <div class="ghx-column-header">
        <span class="ghx-column-title">${escapeHtml(column.name)}</span>
        <span class="ghx-column-count">${visibleIssues.length}</span>
      </div>
      <div class="ghx-column-wrap">
        <div class="ghx-issues"></div>
      </div>
    `;

    const issuesEl = columnEl.querySelector(".ghx-issues");
    for (const issue of visibleIssues) {
      state.issueMap.set(issue.key, issue);
      const issueEl = document.createElement("article");
      issueEl.className = "ghx-issue";
      issueEl.dataset.issueKey = issue.key;
      issueEl.innerHTML = `
        <div class="ghx-issue-card ${state.selectedKey === issue.key ? "is-selected" : ""}">
          <div class="js-draggable-trigger" aria-hidden="true"></div>
          <div class="ghx-issue-content">
            <div class="ghx-issue-fields">
              <div class="ghx-key">
                <a href="#${escapeHtml(issue.key.toLowerCase())}" class="js-key-link ghx-key-link">${escapeHtml(issue.key)}</a>
              </div>
              <div class="ghx-summary"><span class="ghx-inner">${escapeHtml(issue.summary)}</span></div>
            </div>
            <div class="ghx-highlighted-fields">
              ${issue.epicName ? `<div class="ghx-highlighted-field"><span class="aui-label ghx-label-epic" title="${escapeHtml(issue.epicName)}">${escapeHtml(issue.epicName)}</span></div>` : ""}
            </div>
          </div>
          <div class="ghx-card-footer">
            <div class="ghx-footer-left">
              <div class="ghx-avatar" title="${escapeHtml(issue.assigneeDisplay || "Unassigned")}">
                ${issue.assigneeAvatarUrl
                  ? iconMarkup(issue.assigneeAvatarUrl, "ghx-avatar-fallback", avatarText(issue.assigneeDisplay), issue.assigneeDisplay || "Unassigned", `Assignee: ${issue.assigneeDisplay || "Unassigned"}`)
                  : `<span class="ghx-avatar-fallback">${escapeHtml(avatarText(issue.assigneeDisplay))}</span>`}
              </div>
            </div>
            <div class="ghx-footer-right">
              <div class="ghx-type" title="${escapeHtml(issue.issueType)}">
                ${iconMarkup(issue.issueTypeIconUrl, "ghx-type-fallback", issue.issueTypeIcon || "?", issue.issueType, `Issue Type: ${issue.issueType}`)}
              </div>
              <div class="ghx-priority" title="${escapeHtml(issue.priority || "No priority")}">
                ${issue.priorityIconUrl
                  ? iconMarkup(issue.priorityIconUrl, "ghx-priority-fallback", "", issue.priority || "No priority", `Priority: ${issue.priority || "None"}`)
                  : `<span class="ghx-priority-fallback" style="background:${escapeHtml(issue.priorityColor || "#c1c7d0")}"></span>`}
              </div>
            </div>
          </div>
        </div>
      `;

      issueEl.addEventListener("click", (event) => {
        if (event.target.closest(".js-draggable-trigger")) {
          return;
        }
        event.preventDefault();
        openIssue(issue.key);
      });

      issuesEl.appendChild(issueEl);
    }

    boardEl.appendChild(columnEl);
  }

  renderIssueView();
  initSortables();
  syncIssueColumnHeights();
  focusHashIssue();
}

function renderIssueView() {
  const key = state.selectedKey;
  if (!key) {
    issueDetailPanelEl.hidden = true;
    issueDetailPanelEl.classList.remove("is-open");
    issueViewEl.hidden = true;
    detailEmptyEl.hidden = false;
    detailEmptyEl.textContent = "Loading issue...";
    return;
  }

  issueDetailPanelEl.hidden = false;
  issueDetailPanelEl.classList.add("is-open");

  const detail = state.detailMap.get(key) || state.issueMap.get(key);
  if (!detail) {
    issueViewEl.hidden = true;
    detailEmptyEl.hidden = false;
    detailEmptyEl.textContent = `Loading ${key}…`;
    return;
  }

  const isLoading = state.loadingKey === key || !state.detailMap.has(key);

  const reachable = new Set(detail.reachableColumnIds || []);
  const statusOptions = state.columns.map((column) => {
    const isCurrent = column.id === detail.columnId;
    const canMove = reachable.size === 0 || reachable.has(column.id);
    const disabled = !canMove && !isCurrent ? "disabled" : "";
    const label = canMove || isCurrent ? escapeHtml(column.name) : `${escapeHtml(column.name)} (no transition)`;
    return `<option value="${escapeHtml(column.id)}" ${isCurrent ? "selected" : ""} ${disabled}>${label}</option>`;
  }).join("");

  const comments = detail.comments || [];
  const commentMarkup = comments.length
    ? comments.map((comment) => `
      <div class="comment-item">
        <div class="comment-avatar">${escapeHtml(avatarText(comment.author.displayName))}</div>
        <div class="comment-body-wrap">
          <div class="comment-head">
            <span class="comment-author">${escapeHtml(comment.author.displayName)}</span>
            <span class="comment-time">${escapeHtml(formatDate(comment.updated || comment.created))}</span>
          </div>
          <pre class="comment-body">${escapeHtml(comment.body)}</pre>
        </div>
      </div>
    `).join("")
    : '<div class="detail-chip">No comments yet</div>';

  const labels = detail.labels?.length ? detail.labels : [];

  issueViewEl.hidden = false;
  detailEmptyEl.hidden = true;
  issueViewEl.innerHTML = `
    <div class="issue-view-header">
      <div class="issue-view-key-row">
        <span class="ghx-type" title="${escapeHtml(detail.issueType)}">${iconMarkup(detail.issueTypeIconUrl, "ghx-type-fallback", detail.issueTypeIcon || "?", detail.issueType, `Issue Type: ${detail.issueType}`)}</span>
        <a href="${escapeHtml(detail.onlineUrl)}" target="_blank" rel="noreferrer">${escapeHtml(detail.key)}</a>
        ${detail.priority ? `<span class="detail-chip">${escapeHtml(detail.priority)}</span>` : ""}
        ${isLoading ? '<span class="detail-chip">Loading details...</span>' : ""}
      </div>
      <div class="field-row">
        <input class="issue-view-title" id="issue-summary" value="${escapeHtml(detail.summary)}">
        <button class="field-save-btn" type="button" id="save-summary-btn">Save</button>
      </div>
      <div class="issue-view-actions">
        <a class="aui-button" href="${escapeHtml(detail.onlineUrl)}" target="_blank" rel="noreferrer">Open in Jira</a>
      </div>
    </div>

    <section class="detail-section">
      <h3>Details</h3>
      <div class="detail-grid">
        <div class="label">Status</div>
        <div class="field-row">
          <select class="field-select" id="issue-status">${statusOptions}</select>
          <button class="field-save-btn" type="button" id="save-status-btn">Move</button>
        </div>

        <div class="label">Assignee</div>
        <div class="field-row">
          <input class="field-input" id="issue-assignee" value="${escapeHtml(detail.assigneeName || "")}" placeholder="Jira username">
          <button class="field-save-btn" type="button" id="save-assignee-btn">Save</button>
        </div>

        <div class="label">Reporter</div>
        <div>${detail.reporterDisplay ? escapeHtml(detail.reporterDisplay) : "Unknown"}</div>

        <div class="label">Due Date</div>
        <div class="field-row">
          <input class="field-input" id="issue-due-date" type="date" value="${escapeHtml(detail.dueDate || "")}">
          <button class="field-save-btn" type="button" id="save-due-date-btn">Save</button>
        </div>

        <div class="label">Labels</div>
        <div class="field-row">
          <input class="field-input" id="issue-labels" value="${escapeHtml(labels.join(", "))}" placeholder="comma,separated,labels">
          <button class="field-save-btn" type="button" id="save-labels-btn">Save</button>
        </div>

        <div class="label">Epic</div>
        <div>${detail.epicName ? `<span class="detail-chip">${escapeHtml(detail.epicName)}</span>` : "None"}</div>

        <div class="label">Created</div>
        <div>${detail.created ? escapeHtml(formatDate(detail.created)) : "Unknown"}</div>

        <div class="label">Updated</div>
        <div>${detail.updated ? escapeHtml(formatDate(detail.updated)) : "Unknown"}</div>
      </div>
    </section>

    <section class="detail-section">
      <h3>Description</h3>
      <textarea class="field-textarea" id="issue-description">${escapeHtml(detail.description || "")}</textarea>
      <div class="issue-view-actions">
        <button class="field-save-btn" type="button" id="save-description-btn">Save description</button>
      </div>
    </section>

    <section class="detail-section">
      <h3>Labels</h3>
      <div class="detail-chip-list">
        ${labels.length ? labels.map((label) => `<span class="detail-chip">${escapeHtml(label)}</span>`).join("") : '<span class="detail-chip">No labels</span>'}
      </div>
    </section>

    <section class="detail-section">
      <h3>Comments</h3>
      <div class="comment-list">${commentMarkup}</div>
    </section>

    <section class="detail-section">
      <h3>Add Comment</h3>
      <textarea class="field-textarea" id="issue-comment" placeholder="Write a comment"></textarea>
      <div class="issue-view-actions">
        <button class="aui-button aui-button-primary" type="button" id="add-comment-btn">Add Comment</button>
        <button class="aui-button" type="button" id="reload-issue-btn">Reload Issue</button>
      </div>
    </section>
  `;

  document.getElementById("save-summary-btn").addEventListener("click", () =>
    saveField(key, { summary: document.getElementById("issue-summary").value.trim() }, "summary"));
  document.getElementById("save-status-btn").addEventListener("click", () =>
    moveStatus(key, document.getElementById("issue-status").value));
  document.getElementById("save-assignee-btn").addEventListener("click", () =>
    saveField(key, { assigneeName: document.getElementById("issue-assignee").value.trim() }, "assignee"));
  document.getElementById("save-due-date-btn").addEventListener("click", () =>
    saveField(key, { dueDate: document.getElementById("issue-due-date").value }, "due date"));
  document.getElementById("save-labels-btn").addEventListener("click", () =>
    saveField(key, { labels: splitCsv(document.getElementById("issue-labels").value) }, "labels"));
  document.getElementById("save-description-btn").addEventListener("click", () =>
    saveField(key, { description: document.getElementById("issue-description").value }, "description"));
  document.getElementById("add-comment-btn").addEventListener("click", () => addComment(key));
  document.getElementById("reload-issue-btn").addEventListener("click", () => loadIssueDetail(key, true));
}

function focusHashIssue() {
  const hash = window.location.hash.replace(/^#/, "").toUpperCase();
  if (!hash) return;
  const issueEl = document.querySelector(`.ghx-issue[data-issue-key="${hash}"]`);
  issueEl?.scrollIntoView({ block: "center", inline: "center" });
}

function openIssue(key) {
  state.selectedKey = key;
  state.loadingKey = key;
  history.replaceState(null, "", `#${key.toLowerCase()}`);
  renderBoard();
  loadIssueDetail(key, true);
}

async function loadIssueDetail(key, force = false) {
  if (!force && state.detailMap.has(key)) {
    state.loadingKey = null;
    renderIssueView();
    return;
  }

  try {
    const detail = await api(`/api/issues/${encodeURIComponent(key)}`);
    const summaryIssue = state.issueMap.get(key);
    if (summaryIssue && !detail.columnId) {
      detail.columnId = summaryIssue.columnId;
    }
    state.detailMap.set(key, detail);
    if (state.loadingKey === key) {
      state.loadingKey = null;
    }
    if (state.selectedKey === key) {
      renderIssueView();
    }
  } catch (error) {
    if (state.loadingKey === key) {
      state.loadingKey = null;
    }
    showStatus(error.message, "error");
    if (state.selectedKey === key) {
      detailEmptyEl.hidden = false;
      issueViewEl.hidden = true;
      detailEmptyEl.textContent = error.message;
    }
  }
}

async function moveIssueToColumn(key, columnId) {
  try {
    showStatus(`Moving ${key}…`);
    await api(`/api/issues/${encodeURIComponent(key)}/move`, {
      method: "POST",
      body: JSON.stringify({ columnId }),
    });
    state.detailMap.delete(key);
    await loadBoard(true, key);
    await loadIssueDetail(key, true);
    showStatus(`Moved ${key}`, "success");
  } catch (error) {
    showStatus(error.message, "error");
    await loadBoard(true, key);
  }
}

async function saveField(key, payload, label) {
  try {
    showStatus(`Saving ${label}…`);
    await api(`/api/issues/${encodeURIComponent(key)}`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    state.detailMap.delete(key);
    await loadBoard(true, key);
    await loadIssueDetail(key, true);
    showStatus(`Saved ${label}`, "success");
  } catch (error) {
    showStatus(error.message, "error");
  }
}

async function moveStatus(key, columnId) {
  const current = state.issueMap.get(key);
  if (current && current.columnId === columnId) {
    showStatus("Already in that column", "info");
    return;
  }
  try {
    showStatus(`Moving ${key}…`);
    await api(`/api/issues/${encodeURIComponent(key)}/move`, {
      method: "POST",
      body: JSON.stringify({ columnId }),
    });
    state.detailMap.delete(key);
    await loadBoard(true, key);
    await loadIssueDetail(key, true);
    showStatus(`Moved ${key}`, "success");
  } catch (error) {
    showStatus(error.message, "error");
  }
}

async function addComment(key) {
  const commentEl = document.getElementById("issue-comment");
  const text = commentEl.value.trim();
  if (!text) {
    showStatus("Comment is empty", "error");
    return;
  }

  try {
    showStatus(`Commenting on ${key}…`);
    await api(`/api/issues/${encodeURIComponent(key)}/comment`, {
      method: "POST",
      body: JSON.stringify({ text }),
    });
    commentEl.value = "";
    state.detailMap.delete(key);
    await loadIssueDetail(key, true);
    showStatus(`Comment added to ${key}`, "success");
  } catch (error) {
    showStatus(error.message, "error");
  }
}

async function createIssue(event) {
  event.preventDefault();
  const payload = {
    summary: document.getElementById("create-summary").value.trim(),
    issueType: document.getElementById("create-issue-type").value,
    assigneeName: document.getElementById("create-assignee").value.trim(),
    priority: document.getElementById("create-priority").value,
    labels: splitCsv(document.getElementById("create-labels").value),
    dueDate: document.getElementById("create-due-date").value,
    description: document.getElementById("create-description").value,
  };

  if (!payload.summary) {
    showStatus("Summary is required", "error");
    return;
  }

  try {
    showStatus("Creating issue…");
    const created = await api("/api/issues/create", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    createDialogEl.close();
    createIssueFormEl.reset();
    await loadBoard(true, created.key || state.selectedKey);
    if (created.key) {
      openIssue(created.key);
    }
    showStatus(`Created ${created.key || "issue"}`, "success");
  } catch (error) {
    showStatus(error.message, "error");
  }
}

let _retryTimer = null;

async function loadBoard(preserveSelection = false, selectedKey = null) {
  window.clearTimeout(_retryTimer);
  try {
    const data = await api("/api/board");
    errorOverlayEl.classList.remove("show");
    document.getElementById("retry-connect-btn").disabled = false;
    state.board = data.board;
    state.columns = data.columns;
    state.selectedKey = preserveSelection ? (selectedKey || state.selectedKey) : state.selectedKey;
    boardTitleEl.textContent = data.board.name;
    if (boardNameButtonEl) boardNameButtonEl.textContent = data.board.name;
    metaTextEl.textContent = `Updated ${data.updatedAt ?? "just now"} · Drag cards between columns, create issues, edit fields, and comment from the detail panel`;
    openOnlineLinkEl.href = data.board.onlineUrl;
    renderBoard();
    if (state.selectedKey) {
      await loadIssueDetail(state.selectedKey);
    }
  } catch (error) {
    errorOverlayEl.classList.add("show");
    metaTextEl.textContent = "Local Jira server unavailable";
    document.getElementById("retry-connect-btn").disabled = false;
    // auto-retry every 3 seconds while overlay is visible
    _retryTimer = window.setTimeout(() => loadBoard(preserveSelection, selectedKey), 3000);
  }
}

searchInputEl.addEventListener("input", () => {
  state.filter = searchInputEl.value;
  renderBoard();
});

window.addEventListener("resize", syncIssueColumnHeights);

refreshBtnEl.addEventListener("click", () => loadBoard(true, state.selectedKey));

window.addEventListener("hashchange", () => {
  const key = window.location.hash.replace(/^#/, "").toUpperCase();
  if (key) {
    openIssue(key);
  } else {
    closeIssuePanel();
  }
});

createIssueTriggerEl.addEventListener("click", () => createDialogEl.showModal());
closeCreateDialogEl.addEventListener("click", () => createDialogEl.close());
cancelCreateDialogEl.addEventListener("click", () => createDialogEl.close());
createIssueFormEl.addEventListener("submit", createIssue);
closeIssuePanelEl.addEventListener("click", closeIssuePanel);
document.getElementById("retry-connect-btn").addEventListener("click", () => {
  document.getElementById("retry-connect-btn").disabled = true;
  window.clearTimeout(_retryTimer);
  loadBoard();
});

loadBoard();