# GitHub Copilot Built-in Tools — Quick Reference

A cheat sheet for all tools available to custom agents in GitHub Copilot's agent mode.

---

## Tool Categories

### 1. `agent` — Delegate Tasks to Other Agents

Invokes another agent defined in `.github/agents/`. Enables multi-agent workflows where one agent delegates a subtask to a specialized agent.

| Property | Detail |
|----------|--------|
| **What it does** | Passes a task to another agent and waits for its result |
| **Used by** | Project Scaffolder (delegates to Code Review Assistant) |
| **Example** | `@code-review-assistant Review sample-app/logger.py` |

---

### 2. `runSubagent` — Isolated Sub-Agent Execution

Spawns an inline sub-agent in an isolated context. Unlike `agent`, this doesn't invoke a named agent — it creates a temporary one with a custom prompt. Useful for tasks that need a clean context window.

| Property | Detail |
|----------|--------|
| **What it does** | Runs a prompt in isolation, returns the result |
| **Used by** | Code Review Assistant (static analysis sub-agent) |
| **When to use** | Large analysis tasks, JSON generation, context-sensitive parsing |

---

### 3. `todo` — Task Tracking in VS Code UI

Creates and manages todo items visible in the VS Code Copilot panel. Provides real-time progress feedback to the user.

| Property | Detail |
|----------|--------|
| **What it does** | Creates, updates, and completes todo items |
| **Used by** | All 3 agents |
| **Best practice** | Create todo BEFORE starting a step, complete it AFTER finishing |

---

### 4. `execute` — Run Code and Terminal Commands

A family of sub-tools for executing code and commands.

| Sub-tool | What it does | Used by |
|----------|-------------|---------|
| `runInTerminal` | Runs a shell command | Release Notes (git), Scaffolder (pip, pytest) |
| `runTests` | Runs the project's test suite | Code Review Assistant |
| `testFailure` | Gets detailed test failure info | Code Review Assistant |
| `createAndRunTask` | Creates a VS Code task and runs it | — |
| `getTerminalOutput` | Reads output from a running terminal | — |
| `killTerminal` | Stops a running terminal | — |
| `awaitTerminal` | Waits for a terminal command to finish | — |
| `runNotebookCell` | Executes a Jupyter notebook cell | — |

---

### 5. `read` — Read Files

Reads file contents from the workspace. Supports text files, notebooks, and structured data.

| Property | Detail |
|----------|--------|
| **What it does** | Returns the text content of a file |
| **Used by** | Code Review Assistant, Release Notes Generator |
| **Example** | `readFile("sample-app/utils.py")` |

---

### 6. `search` — Search Files in Workspace

Finds files and text content within the workspace.

| Sub-tool | What it does | Used by |
|----------|-------------|---------|
| `fileSearch` | Finds files by glob pattern | Code Review Assistant (`**/*.py`) |
| `textSearch` | Searches file contents by text/regex | Release Notes Generator (`BREAKING CHANGE`) |

---

### 7. `edit` — Edit Files in Workspace

Creates and modifies files within the workspace.

| Sub-tool | What it does | Used by |
|----------|-------------|---------|
| `editFiles` | Modifies existing file content | Code Review (fixes), Release Notes (CHANGELOG) |
| `createFile` | Creates a new file | Project Scaffolder |
| `createDirectory` | Creates a new directory | — |

---

### 8. `web` — Fetch Information from the Web

Retrieves content from URLs. Useful for fetching documentation, best practices, or API references.

| Property | Detail |
|----------|--------|
| **What it does** | Fetches a URL and returns its content |
| **Used by** | Project Scaffolder (best-practice research) |
| **Note** | Subject to rate limits; use for reference, not scraping |

---

### 9. `vscode` — VS Code Features

Interacts with VS Code itself — opening files, running commands, managing extensions.

| Sub-tool | What it does |
|----------|-------------|
| `runVscodeCommand` | Executes a VS Code command |
| `installExtension` | Installs a VS Code extension |
| `openSimpleBrowser` | Opens a URL in the VS Code simple browser |

---

### 10. MCP Servers — External Tool Integration

Model Context Protocol servers extend agent capabilities with external tools. Configured in `.vscode/mcp.json`.

| Property | Detail |
|----------|--------|
| **What it does** | Connects agents to external APIs (GitHub, Jira, etc.) |
| **Used by** | Release Notes Generator (`github` MCP server) |
| **Config file** | `.vscode/mcp.json` |
| **Auth pattern** | `${input:token_name}` for secure credential prompting |

---

## Tool Coverage by Agent

| Tool | Code Review | Scaffolder | Release Notes |
|------|:-----------:|:----------:|:-------------:|
| `todo` | Yes | Yes | Yes |
| `read` | Yes | | Yes |
| `search` | Yes | | Yes |
| `edit` | Yes | Yes | Yes |
| `execute` (runTests) | Yes | | |
| `execute` (runInTerminal) | | Yes | Yes |
| `execute` (testFailure) | Yes | | |
| `runSubagent` | Yes | | |
| `agent` (delegation) | | Yes | |
| `web` (fetch) | | Yes | |
| MCP (`github`) | | | Yes |
