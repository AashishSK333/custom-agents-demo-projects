# Jira-Confluence Sync Agent

A GitHub Copilot custom agent that bridges Jira ticket requirements to Confluence documentation using the Jira and Confluence MCP servers.

## What It Does

Given a Jira Ticket ID, this agent:

1. Fetches the ticket's full data (summary, description, priority, comments) via the Jira MCP server
2. Synthesizes a documentation search intent via a sub-agent
3. Finds the 3 closest matching Confluence pages via the Confluence MCP server
4. Prompts you to select a page to update — or create a new one
5. Appends a structured requirements section (with your confirmation)
6. Reports the final page URL

All steps are tracked as todo items in the VS Code Copilot panel.

## Prerequisites

- VS Code with the [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) extension
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed — the MCP servers run via `uvx`
  ```bash
  # macOS / Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Windows
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- Atlassian account with an API token — generate one at https://id.atlassian.com/manage-profile/security/api-tokens

## Quick Start

**1. Clone or open this workspace in VS Code.**

**2. Open GitHub Copilot Chat** (`Ctrl+Alt+I` / `Cmd+Option+I`).

**3. Start the MCP servers** — VS Code will prompt for your credentials the first time:
   - Atlassian domain (e.g. `mycompany.atlassian.net`)
   - Atlassian account email
   - Atlassian API token _(entered as a password — not shown)_
   - Confluence space key for new pages (e.g. `ENG`, `DOCS`)

**4. Invoke the agent:**

```
@jira-confluence-sync PROJ-123
```

Or use any supported input format:
- `PROJ-123`
- `https://yourorg.atlassian.net/browse/PROJ-123`
- `sync ticket PROJ-123`

## How It Works

The agent uses confirmed GitHub Copilot built-in tools plus two MCP servers:

| Tool | Type | Purpose |
|------|------|---------|
| `todo` | Built-in | Progress tracking in the Copilot panel |
| `runSubagent` | Built-in | Spawns an isolated sub-agent to synthesize the Confluence search intent |
| `jira` | MCP server | Reads ticket data via `jira_get_issue` and `jira_get_issue_comments` |
| `confluence` | MCP server | Searches, reads, and writes pages via `confluence_search`, `confluence_get_page`, `confluence_update_page`, `confluence_create_page` |

## MCP Server Configuration

Both MCP servers are configured in `.vscode/mcp.json` using the [`mcp-atlassian`](https://github.com/sooperset/mcp-atlassian) community package. Two separate server entries (`jira` and `confluence`) run from the same package — each scoped to its own service:

```
jira      → JIRA_URL + JIRA_USERNAME + JIRA_API_TOKEN
confluence → CONFLUENCE_URL + CONFLUENCE_USERNAME + CONFLUENCE_API_TOKEN + CONFLUENCE_SPACE_KEY
```

Credentials are entered via VS Code's secure `promptString` inputs — they are never written to disk or committed to version control.

## Project Structure

```
sop-sync-custom-agent/
├── README.md                                      # This file
├── .env.example                                   # Credential reference (not loaded by the agent)
├── .github/
│   └── agents/
│       └── jira-confluence-sync.agent.md          # Agent definition
└── .vscode/
    └── mcp.json                                   # MCP server configuration
```

## Key Constraints

- **Read-only on Jira** — the agent never modifies tickets
- **Append-only on Confluence** — never overwrites existing content
- **Confirmation required** — every write operation requires you to type `confirm`

## Known Linter Warning

VS Code's Copilot agent linter flags `jira` and `confluence` as _"Unknown tool"_ in the agent frontmatter. This is a false positive — the linter only validates against the built-in tool list and does not inspect `mcp.json` at edit time. The tools resolve correctly at runtime once the MCP servers are running.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `uvx: command not found` | Install `uv` — see Prerequisites above |
| MCP server fails to start | Run `uvx mcp-atlassian --help` in terminal to verify the package installs correctly |
| 401 Unauthorized | Re-enter credentials: restart VS Code or reload the MCP servers |
| 403 Forbidden | Your API token lacks write permission on the target Confluence space |
| 404 on ticket | Verify the Ticket ID and your Atlassian domain |
| Space not found on page create | Confirm the space key exists in your Confluence instance |
