# Jira-Confluence Sync Agent

A GitHub Copilot custom agent that bridges Jira ticket requirements to Confluence documentation — no plugins or MCP servers required.

## What It Does

Given a Jira Ticket ID, this agent:

1. Fetches the ticket's full data (summary, description, priority, comments) via the Jira REST API
2. Synthesizes a documentation search intent via a sub-agent
3. Finds the 3 closest matching Confluence pages via the Confluence REST API
4. Prompts you to select a page to update — or create a new one
5. Appends a structured requirements section (with your confirmation)
6. Reports the final page URL

All steps are tracked as todo items in the VS Code Copilot panel.

## Prerequisites

- VS Code with the [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) extension
- Atlassian account with an API token — generate one at https://id.atlassian.com/manage-profile/security/api-tokens
- `curl` available in your terminal (standard on macOS and most Linux distros; install via `winget install curl` on Windows)

No npm packages, no MCP servers, no environment setup required.

## Quick Start

**1. Clone or open this workspace in VS Code.**

**2. Open GitHub Copilot Chat** (`Ctrl+Alt+I` / `Cmd+Option+I`).

**3. Invoke the agent:**

```
@jira-confluence-sync PROJ-123
```

Or use any supported input format:
- `PROJ-123`
- `https://yourorg.atlassian.net/browse/PROJ-123`
- `sync ticket PROJ-123`

**4. Provide your Atlassian credentials when prompted.**

The agent will ask for your domain, email, API token, and Confluence space key at the start of each session. These are used only for `curl` commands during the conversation and are never written to disk.

## How It Works

The agent uses only confirmed GitHub Copilot built-in tools:

| Tool | Purpose |
|------|---------|
| `todo` | Progress tracking — creates and completes items in the Copilot panel |
| `runSubagent` | Spawns an isolated sub-agent to synthesize the Confluence search intent |
| `execute → runInTerminal` | Runs `curl` commands against the Jira and Confluence REST APIs |

All Jira and Confluence communication happens through `curl` commands run in your local terminal. This means:
- No MCP server packages to install
- No environment variables to configure
- Credentials stay in the chat session only

## Project Structure

```
sop-sync-custom-agent/
├── README.md                                       # This file
├── .env.example                                    # Credential reference (not loaded by the agent)
└── .github/
    └── agents/
        └── jira-confluence-sync.agent.md           # Agent definition
```

## Key Constraints

- **Read-only on Jira** — the agent never modifies tickets
- **Append-only on Confluence** — never overwrites existing content
- **Confirmation required** — every write operation requires you to type `confirm`
- **No credential storage** — API token exists only in the chat session

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `curl: command not found` | Install curl or ensure it's in your PATH |
| 401 Unauthorized | Double-check your email and API token |
| 403 Forbidden | Your token may lack write permission on the target Confluence space |
| 404 on ticket | Verify the Ticket ID and your Atlassian domain |
| Space not found | Confirm the space key exists in your Confluence instance |
