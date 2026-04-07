#!/bin/bash
# Logs when the Planner agent hands off work to another agent via runSubagent
# Usage: Called automatically by PreToolUse hook on runSubagent tool

set -e

HOOK_LOG_DIR="./.github/hooks/logs"
LOG_FILE="$HOOK_LOG_DIR/planner-handoffs.log"

# Create log directory if it doesn't exist
mkdir -p "$HOOK_LOG_DIR"

# Read input from stdin
HOOK_INPUT=$(cat)

# Extract tool name and arguments from the hook input
TOOL_NAME=$(echo "$HOOK_INPUT" | jq -r '.tool.name // empty' 2>/dev/null || echo "")
AGENT_NAME=$(echo "$HOOK_INPUT" | jq -r '.tool.arguments.agentName // empty' 2>/dev/null || echo "")
DESCRIPTION=$(echo "$HOOK_INPUT" | jq -r '.tool.arguments.description // empty' 2>/dev/null || echo "")

# Only log if this is the runSubagent tool
if [ "$TOOL_NAME" = "runSubagent" ]; then
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
  
  # Log the handoff event
  {
    echo "[$TIMESTAMP] PLANNER HANDOFF"
    echo "  → Target Agent: $AGENT_NAME"
    echo "  → Task: $DESCRIPTION"
    echo ""
  } >> "$LOG_FILE"
  
  # Output success to hook engine
  echo "{\"continue\": true}"
else
  # Not a runSubagent call, pass through
  echo "{\"continue\": true}"
fi
