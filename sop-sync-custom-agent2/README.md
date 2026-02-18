# Dev Workflow Automation Hub

An educational project demonstrating all key GitHub Copilot custom agent tools through three practical developer workflow automations.

---

## What This Project Teaches

GitHub Copilot's agent mode offers a suite of built-in tools — from file I/O and terminal execution to sub-agent delegation and MCP server integration. This project contains **3 custom agents** and a **Python sample app** designed to showcase every tool in a realistic context.

### Tool Coverage Matrix

| Tool | Code Review | Scaffolder | Release Notes |
|------|:-----------:|:----------:|:-------------:|
| `todo` | X | X | X |
| `read` | X | | X |
| `search` | X | | X |
| `edit` | X | X | X |
| `execute` (runTests) | X | | |
| `execute` (runInTerminal) | | X | X |
| `execute` (testFailure) | X | | |
| `runSubagent` | X | | |
| `agent` (delegation) | | X | |
| `web` (fetch) | | X | |
| MCP (`github`) | | | X |

---

## Prerequisites

- **VS Code** with GitHub Copilot (agent mode enabled)
- **Node.js 18+** (for `npx` to run the MCP server)
- **Python 3.8+** (for the sample app)
- **GitHub Personal Access Token** ([create one here](https://github.com/settings/tokens?type=beta)) with `repo`, `issues`, and `pull_requests` read scopes

---

## Quick Start

### 1. Clone and open in VS Code

```bash
git clone <this-repo-url>
cd dev-workflow-hub
code .
```

### 2. Set up the sample app

```bash
cd sample-app
pip install -r requirements.txt
pytest  # Expect 2 intentional failures
```

### 3. Configure GitHub MCP (optional — needed for Release Notes agent)

Copy the environment template:

```bash
cp .env.example .env
```

Edit `.env` and paste your GitHub PAT. Alternatively, the MCP server will prompt you for the token when it starts (configured via `${input:github_token}` in `.vscode/mcp.json`).

### 4. Invoke the agents

Open GitHub Copilot Chat in agent mode and try:

```
@code-review-assistant review sample-app/
@project-scaffolder add a logging utility with tests
@release-notes-generator generate notes since last tag
```

---

## Project Structure

```
.
├── README.md                          # This file
├── .env.example                       # GitHub token template
├── .github/
│   └── agents/
│       ├── code-review-assistant.agent.md   # Agent 1: Reviews code
│       ├── project-scaffolder.agent.md      # Agent 2: Generates components
│       └── release-notes-generator.agent.md # Agent 3: Builds changelogs
├── .vscode/
│   └── mcp.json                       # GitHub MCP server config
├── sample-app/
│   ├── main.py                        # Task tracker CLI (has bug)
│   ├── utils.py                       # Utilities (has 4 bugs)
│   ├── config.py                      # Config loader (clean)
│   ├── requirements.txt               # pytest dependency
│   └── tests/
│       ├── test_main.py               # Passing tests
│       └── test_utils.py              # 2 intentionally failing tests
└── docs/
    └── tool-reference.md              # Quick-ref for all Copilot tools
```

---

## The Agents

### 1. Code Review Assistant

**Purpose:** Reviews Python code for bugs, style issues, and test failures.

**Invoke:** `@code-review-assistant review sample-app/`

**Tools demonstrated:**
- `search` (fileSearch) — discovers Python files
- `read` (readFile) — loads source code
- `runSubagent` — delegates static analysis to an isolated sub-agent
- `execute` (runTests) — runs pytest
- `execute` (testFailure) — gets detailed failure diagnostics
- `edit` (editFiles) — applies fixes with user approval
- `todo` — tracks all 6 steps in VS Code UI

**Workflow:**
1. Discover files to review
2. Analyze code via sub-agent (bugs, style, security, performance)
3. Run tests and capture failures
4. Present structured review report
5. Apply user-approved fixes
6. Re-run tests to verify

---

### 2. Project Scaffolder

**Purpose:** Generates new modules and test files from plain-English descriptions.

**Invoke:** `@project-scaffolder add a caching module with tests`

**Tools demonstrated:**
- `web` (fetch) — researches best practices from the internet
- `edit` (createFile) — creates source and test files
- `execute` (runInTerminal) — installs dependencies, runs pytest
- `agent` — delegates to Code Review Assistant for validation
- `todo` — tracks all 5 steps

**Workflow:**
1. Research best practices via web fetch
2. Present scaffold plan for approval
3. Generate source + test files
4. Delegate validation to Code Review Assistant
5. Run tests and report results

---

### 3. Release Notes Generator

**Purpose:** Generates categorized release notes from git history and GitHub data.

**Invoke:** `@release-notes-generator generate notes since last tag`

**Tools demonstrated:**
- `execute` (runInTerminal) — runs git log, git tag, git diff
- MCP `github` tools — fetches issue/PR metadata from GitHub
- `search` (textSearch) — finds BREAKING CHANGE annotations
- `read` (readFile) — reads existing CHANGELOG.md
- `edit` (editFiles) — writes release notes to CHANGELOG.md
- `todo` — tracks all 6 steps

**Workflow:**
1. Determine version range from git tags
2. Extract and categorize commit history
3. Enrich with GitHub issue/PR data via MCP
4. Scan for breaking changes
5. Present draft release notes
6. Write to CHANGELOG.md (with approval)

---

## Tool-by-Tool Explainer

### `todo` — Visual Progress Tracking

Every agent creates todo items before starting each step and marks them complete after. This provides real-time feedback in the VS Code Copilot panel, so users always know what the agent is doing.

### `read` / `search` / `edit` — File Operations

The foundation of workspace interaction. `search` discovers files by pattern, `read` loads their contents, and `edit` modifies them. The Code Review Agent uses all three: search to find `.py` files, read to load code, edit to apply fixes.

### `execute` — Terminal & Test Execution

A family of tools for running commands. `runInTerminal` handles shell commands (git, pip, pytest). `runTests` is specialized for test execution. `testFailure` retrieves stack traces from failed tests. The Release Notes agent is terminal-heavy (git commands), while the Code Review agent focuses on test execution.

### `runSubagent` — Isolated Context Execution

Spawns a temporary sub-agent with its own context window. The Code Review Agent uses this to delegate static analysis — the sub-agent receives all file contents and analysis rules without polluting the main agent's context. This is the right pattern when you need a large, focused analysis.

### `agent` — Cross-Agent Delegation

Invokes a named agent defined in `.github/agents/`. The Project Scaffolder delegates to the Code Review Assistant after generating files — demonstrating how agents compose into larger workflows. The delegated agent runs its full workflow independently.

### `web` — Internet Access

Fetches content from URLs. The Project Scaffolder uses this to research best practices before generating code — ensuring the output follows current conventions rather than stale patterns.

### MCP Servers — External API Integration

Model Context Protocol servers extend agents with external tools. The GitHub MCP server gives the Release Notes agent access to issue titles, PR metadata, and contributor data — information that can't be derived from git history alone.

**Configuration:** `.vscode/mcp.json` defines servers with commands, args, and environment variables. The `${input:id}` pattern securely prompts for credentials at runtime.

---

## MCP Configuration

The `.vscode/mcp.json` file configures external MCP servers:

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "github_token",
      "description": "GitHub Personal Access Token",
      "password": true
    }
  ],
  "servers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_token}"
      }
    }
  }
}
```

**Key concepts:**
- `inputs` — Defines secrets that VS Code will prompt for at runtime (never stored in config)
- `servers` — Each server runs as a stdio process; VS Code manages the lifecycle
- `${input:github_token}` — References the input defined above; the value is injected securely

---

## Customization

### Adding a new agent

1. Create `.github/agents/my-agent.agent.md`
2. Define the YAML frontmatter with `name`, `description`, and `tools`
3. Write the role, input contract, workflow steps, and constraints
4. Invoke with `@my-agent <prompt>`

### Adding a new MCP server

1. Add the server config to `.vscode/mcp.json` under `servers`
2. Add any required secrets to `inputs`
3. Reference the tools in your agent's `tools` list

### Modifying the sample app

The `sample-app/` is designed to be extended. Add new modules and their tests — the Code Review Agent will automatically discover them.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not showing in Copilot | Ensure the `.agent.md` file is in `.github/agents/` and has valid YAML frontmatter |
| MCP server not connecting | Check that `npx` is available (`node -v`). Verify your GitHub PAT has the correct scopes |
| Tests not running | Run `pip install -r sample-app/requirements.txt` to install pytest |
| Token prompt not appearing | Restart VS Code to reload `.vscode/mcp.json` |
| Agent says "tool not available" | Verify the tool name in the agent's `tools:` list matches a built-in tool |

---

## Further Reading

- [GitHub Copilot Custom Agents Docs](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-extensibility/using-copilot-agents)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [docs/tool-reference.md](docs/tool-reference.md) — Quick-reference for all built-in tools
