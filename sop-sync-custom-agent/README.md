# Jira-Confluence Sync Agent

A custom Claude Code agent that bridges Jira ticket requirements to Confluence documentation automatically.

## What It Does

Given a Jira Ticket ID, this agent:

1. Fetches the ticket's full data (summary, description, priority, comments)
2. Synthesizes a documentation search intent via a sub-agent
3. Finds the 3 closest matching Confluence pages
4. Prompts you to select a page to update — or create a new one
5. Appends a structured requirements section (with your confirmation)
6. Reports the final page URL

All steps are tracked as todo items in the VS Code UI.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Jira account with API token
- Confluence account with API token
- Node.js (for `npx` MCP server bootstrap)

## Quick Start

**1. Clone / open this workspace in VS Code.**

**2. Copy the environment template and fill in your credentials:**

```bash
cp .env.example .env
```

Edit `.env` with your actual values (see [docs/setup.md](docs/setup.md) for field-by-field guidance).

**3. Start Claude Code in this workspace:**

```bash
claude
```

The MCP servers for Jira and Confluence will start automatically via `.vscode/mcp.json`.

**4. Invoke the agent with a Jira ticket:**

```
@jira-confluence-sync PROJ-123
```

Or use any supported input format:
- `PROJ-123`
- `https://yourorg.atlassian.net/browse/PROJ-123`
- `sync ticket PROJ-123`

## Project Structure

```
sop-sync-custom-agent/
├── README.md                    # This file
├── .env.example                 # Environment variables template
├── .github/
│   └── agents/
│       └── jira-confluence-sync.agent.md   # Agent definition
├── .vscode/
│   └── mcp.json                 # MCP server configuration
├── docs/
│   ├── workflow.md              # Step-by-step workflow reference
│   └── setup.md                 # MCP & credentials setup guide
└── skills/
    └── README.md                # Skills extension guide
```

## Key Constraints

- **Read-only on Jira** — the agent never modifies tickets
- **Append-only on Confluence** — never overwrites existing content
- **Confirmation required** — every write operation requires explicit approval

## Documentation

| Doc | Purpose |
|-----|---------|
| [docs/setup.md](docs/setup.md) | Configure MCP servers and API credentials |
| [docs/workflow.md](docs/workflow.md) | Understand the 6-step sync workflow |
| [skills/README.md](skills/README.md) | Extend the agent with custom skills |
| [.github/agents/jira-confluence-sync.agent.md](.github/agents/jira-confluence-sync.agent.md) | Full agent definition |
