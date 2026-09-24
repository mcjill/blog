#!/usr/bin/env python3
"""PreToolUse hook: force a human yes before anything that publishes, spends money, or submits URLs.

On GitHub Pages a push to the default branch IS publishing, so every push asks.
"""
import json
import re
import sys

BASH_RULES = [
    (r"\bgit\s+push\b", "git push publishes the site on GitHub Pages"),
    (r"\bserp\.py\b.*--live\b", "--live spends DataForSEO credits"),
    (r"indexing\.googleapis\.com|urlNotifications|/sitemaps/", "submits URLs to Google"),
    (r"\bcurl\b.*(-X\s*(POST|PUT|PATCH|DELETE)|--data|-d\s)", "writes to an external service"),
]
MCP_WRITE = re.compile(r"^mcp__.*(push|create|update|merge|delete|publish|submit|write)", re.I)

event = json.load(sys.stdin)
tool, args = event.get("tool_name", ""), event.get("tool_input", {})
reason = None
if tool == "Bash":
    cmd = args.get("command", "")
    reason = next((why for pat, why in BASH_RULES if re.search(pat, cmd)), None)
elif MCP_WRITE.search(tool):
    reason = f"{tool} changes something outside this folder"

if reason:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": f"SEO guard: {reason}. Approve only if you meant to ship this.",
    }}))
sys.exit(0)
