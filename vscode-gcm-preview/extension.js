const vscode = require('vscode');
const { execFile } = require('child_process');
const path = require('path');
const fs = require('fs');

// Map from file path → WebviewPanel
const panels = new Map();

function getScriptPath(workspaceRoot) {
    return path.join(workspaceRoot, 'scripts', 'confluence', 'gcm_preview.py');
}

function getWorkspaceRoot() {
    const folders = vscode.workspace.workspaceFolders;
    if (!folders || folders.length === 0) return null;
    return folders[0].uri.fsPath;
}

async function renderPreview(panel, filePath) {
    const workspaceRoot = getWorkspaceRoot();
    if (!workspaceRoot) {
        panel.webview.html = errorHtml('No workspace folder open.');
        return;
    }

    const scriptPath = getScriptPath(workspaceRoot);
    if (!fs.existsSync(scriptPath)) {
        panel.webview.html = errorHtml(
            `Preview script not found: ${scriptPath}`
        );
        return;
    }

    panel.webview.html = loadingHtml(path.basename(filePath));

    execFile('python3', [scriptPath, filePath], { maxBuffer: 10 * 1024 * 1024 }, (err, stdout, stderr) => {
        if (err) {
            panel.webview.html = errorHtml(stderr || err.message);
        } else {
            panel.webview.html = stdout;
        }
    });
}

function loadingHtml(name) {
    return `<!DOCTYPE html><html><body style="font-family:sans-serif;padding:24px;color:#6B778C">
    <p>Rendering <strong>${name}</strong>…</p>
    </body></html>`;
}

function errorHtml(msg) {
    const escaped = msg.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return `<!DOCTYPE html><html><body style="font-family:sans-serif;padding:24px">
    <h3 style="color:#BF2600">GCM Preview Error</h3>
    <pre style="background:#FFEBE6;padding:12px;border-radius:4px;color:#BF2600;font-size:12px">${escaped}</pre>
    </body></html>`;
}

function openPreview(filePath) {
    const name = path.basename(filePath);

    // Reuse existing panel if open
    let panel = panels.get(filePath);
    if (panel) {
        panel.reveal(vscode.ViewColumn.Beside);
        renderPreview(panel, filePath);
        return;
    }

    panel = vscode.window.createWebviewPanel(
        'gcmPreview',
        `Preview: ${name}`,
        vscode.ViewColumn.Beside,
        {
            enableScripts: false,
            retainContextWhenHidden: true,
        }
    );

    panels.set(filePath, panel);
    panel.onDidDispose(() => panels.delete(filePath));

    renderPreview(panel, filePath);
}

function activate(context) {
    // Command: GCM: Open Preview
    // uri is passed when invoked from the explorer context menu
    const cmdDisposable = vscode.commands.registerCommand('gcm.openPreview', (uri) => {
        let filePath;
        if (uri && uri.fsPath) {
            filePath = uri.fsPath;
        } else {
            const editor = vscode.window.activeTextEditor;
            if (!editor || !editor.document.fileName.endsWith('.gcm')) {
                vscode.window.showWarningMessage('This command only works on .gcm files.');
                return;
            }
            filePath = editor.document.fileName;
        }
        if (!filePath.endsWith('.gcm')) {
            vscode.window.showWarningMessage('This command only works on .gcm files.');
            return;
        }
        openPreview(filePath);
    });

    // Refresh on save
    const saveDisposable = vscode.workspace.onDidSaveTextDocument(doc => {
        if (!doc.fileName.endsWith('.gcm')) return;
        const panel = panels.get(doc.fileName);
        if (panel) renderPreview(panel, doc.fileName);
    });

    // Refresh on content change (debounced 600ms)
    let debounceTimer = null;
    const changeDisposable = vscode.workspace.onDidChangeTextDocument(event => {
        const doc = event.document;
        if (!doc.fileName.endsWith('.gcm')) return;
        const panel = panels.get(doc.fileName);
        if (!panel) return;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            // Write current content to a temp file and render that,
            // so the preview reflects unsaved edits too.
            const os = require('os');
            const tmp = path.join(os.tmpdir(), `gcm_preview_${Date.now()}.gcm`);
            fs.writeFile(tmp, doc.getText(), 'utf8', err => {
                if (err) return;
                const workspaceRoot = getWorkspaceRoot();
                if (!workspaceRoot) return;
                const scriptPath = getScriptPath(workspaceRoot);
                execFile('python3', [scriptPath, tmp], { maxBuffer: 10 * 1024 * 1024 }, (err2, stdout, stderr) => {
                    fs.unlink(tmp, () => {});
                    if (!panel || panel.webview === undefined) return;
                    panel.webview.html = err2 ? errorHtml(stderr || err2.message) : stdout;
                });
            });
        }, 600);
    });

    context.subscriptions.push(cmdDisposable, saveDisposable, changeDisposable);
}

function deactivate() {}

module.exports = { activate, deactivate };
