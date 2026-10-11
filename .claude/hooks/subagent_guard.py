#!/usr/bin/env python3
"""Read-only guard for Claude Code subagents.

Wired to three hook events in .claude/settings.json:
  SubagentStart -> tells the subagent it is read-only before it plans anything
  PreToolUse    -> allowlist: subagents may only read/search; everything else is denied
  SubagentStop  -> logs tool-call and denial counts to .claude/logs/subagents.jsonl

The main session is never restricted: hook input only carries `agent_id`
when the call comes from inside a subagent.
Standard library only. No outside packages.
"""
import fnmatch
import json
import os
import re
import shlex
import sys
from datetime import datetime, timezone

PROJECT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
LOG_DIR = os.path.join(PROJECT, ".claude", "logs")

# Subagent types allowed to write. Built-in statusline-setup must edit settings to work.
WRITE_EXEMPT_AGENTS = {"statusline-setup"}

# Tools a subagent may call. Anything not listed (Write, Edit, NotebookEdit,
# every mcp__* tool, Artifact, etc.) is denied. SubagentHandback is how a
# subagent returns its report; the Task*/TodoWrite tools only track progress.
ALLOWED_TOOLS = {
    "Read", "Grep", "Glob", "Bash", "WebSearch", "WebFetch", "ToolSearch", "Agent",
    "SubagentHandback", "TodoWrite", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet",
}

READ_ONLY_COMMANDS = {
    "ls", "cat", "head", "tail", "wc", "grep", "rg", "find", "sort", "uniq", "cut",
    "tr", "stat", "file", "du", "pwd", "echo", "tree", "jq", "diff", "basename",
    "dirname", "realpath", "which", "date", "sed", "git",
}
READ_ONLY_GIT = {"log", "diff", "show", "status", "blame", "grep", "ls-files", "rev-parse", "shortlog"}

# test-runner may run checks and the repo's own test/backtest scripts.
# Known limit: any Python script can write files (backtests save results).
TEST_SCRIPT_PATTERNS = ["src/agents/test_execution/*.py", "src/data/rbi/*/test_*.py", "src/scripts/stress_test.py"]

CONTRACT = (
    "READ-ONLY MODE: you are a subagent. You may read, search, and run read-only commands. "
    "You may NOT create, edit, move, or delete files, install anything, commit, push, or call "
    "tools that change external systems. If the task needs a change, do not attempt it: put the "
    "exact file path and the change you recommend in your final report. The main agent makes all edits."
)

DENY_REASON = (
    "HARD BLOCK by subagent read-only guard (not a permission prompt): {why}. "
    "Do not retry with another command or tool. Stop trying to make this change, include the "
    "exact file and the edit you wanted in your final report, and finish."
)


def bash_problem(cmd, agent_type):
    """Return why a Bash command is not read-only, or None if it is allowed."""
    if re.search(r"`|\$\(|<\(|>\(|\n", cmd):
        return "command substitution or multi-line commands are not allowed"
    stripped = cmd.replace("2>&1", "").replace("2>/dev/null", "").replace(">/dev/null", "").replace("> /dev/null", "")
    if re.search(r"(?<![&|])&(?![&>])", stripped):
        return "background '&' is not allowed"
    if ">" in stripped:
        return "output redirection writes files"

    for seg in re.split(r"&&|\|\||;|\|", cmd):
        seg = seg.strip()
        if not seg:
            continue
        try:
            words = shlex.split(seg)
        except ValueError:
            return "could not parse command"
        name = os.path.basename(words[0])

        if agent_type == "test-runner" and name in ("python", "python3"):
            if words[1:3] == ["-m", "py_compile"]:
                continue
            if len(words) >= 2 and all(not w.startswith(("-c", "-m")) for w in words[1:2]) and any(fnmatch.fnmatch(words[1].lstrip("./"), p) for p in TEST_SCRIPT_PATTERNS):
                continue
            return f"test-runner may only run py_compile or scripts matching {TEST_SCRIPT_PATTERNS}"

        if name not in READ_ONLY_COMMANDS:
            return f"'{name}' is not on the read-only command list"
        args = words[1:]
        if name == "find" and any(a in ("-exec", "-execdir", "-delete", "-ok", "-okdir") or a.startswith("-fprint") for a in args):
            return "find with -exec/-delete/-fprint can change files"
        if name == "sort" and any(a == "-o" or a.startswith("--output") for a in args):
            return "sort -o writes files"
        if name == "rg" and any(a.startswith("--pre") for a in args):
            return "rg --pre runs programs"
        if name == "sed":
            if "-n" not in args or any(a.startswith("-i") or a.startswith("--in-place") for a in args):
                return "only 'sed -n' (print) is allowed"
            script = " ".join(a for a in args if not a.startswith("-"))
            if re.search(r"(^|[;}\s/0-9$])[weWE]\b", script):
                return "sed w/e commands can write files or run programs"
        if name == "git":
            if any(a == "-c" or a.startswith("--output") or a.startswith("--exec") for a in args):
                return "git -c/--output is not allowed"
            rest = list(args)
            while rest and rest[0] in ("-C", "--no-pager", "--git-dir", "--work-tree") or (rest and rest[0].startswith(("--git-dir=", "--work-tree="))):
                rest = rest[2:] if rest[0] in ("-C", "--git-dir", "--work-tree") else rest[1:]
            sub = rest[0] if rest else None
            if sub not in READ_ONLY_GIT:
                return f"git {sub} is not read-only"
    return None


def deny(why):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": DENY_REASON.format(why=why),
    }}))


def log(entry):
    os.makedirs(LOG_DIR, exist_ok=True)
    entry["ts"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with open(os.path.join(LOG_DIR, "subagents.jsonl"), "a") as f:
        f.write(json.dumps(entry) + "\n")


def pre_tool_use(data):
    agent_type = data.get("agent_type", "")
    if agent_type in WRITE_EXEMPT_AGENTS:
        return
    tool = data.get("tool_name", "")
    if tool not in ALLOWED_TOOLS:
        why = f"subagents cannot use {tool}"
    elif tool == "Bash":
        why = bash_problem(data.get("tool_input", {}).get("command", ""), agent_type)
    else:
        why = None
    if why:
        # Log the tool and reason only, never the raw command (it could contain secrets).
        log({"event": "denied", "agent_type": agent_type, "agent_id": data.get("agent_id"), "tool": tool, "reason": why})
        deny(why)


def subagent_stop(data):
    tool_calls = 0
    path = data.get("agent_transcript_path")
    if path and os.path.exists(path):
        with open(path) as f:
            for line in f:
                tool_calls += line.count('"type":"tool_use"') + line.count('"type": "tool_use"')
    denials = 0
    log_path = os.path.join(LOG_DIR, "subagents.jsonl")
    if os.path.exists(log_path):
        with open(log_path) as f:
            denials = sum(1 for l in f if f'"agent_id": "{data.get("agent_id")}"' in l and '"denied"' in l)
    log({"event": "stop", "agent_type": data.get("agent_type"), "agent_id": data.get("agent_id"),
         "tool_calls": tool_calls, "denials": denials})


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("subagent_guard: invalid hook input", file=sys.stderr)
        sys.exit(2)

    event = data.get("hook_event_name")
    if event == "PreToolUse" and not data.get("agent_id"):
        return  # main session: never restricted, exit fast

    # This is a security check, so it fails closed: if the guard itself breaks
    # while checking a subagent, the tool call is denied instead of allowed.
    try:
        if event == "SubagentStart":
            if data.get("agent_type") not in WRITE_EXEMPT_AGENTS:
                print(json.dumps({"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": CONTRACT}}))
        elif event == "PreToolUse":
            pre_tool_use(data)
        elif event == "SubagentStop":
            subagent_stop(data)  # never blocks: a block would keep the subagent running
    except Exception as e:
        if event == "PreToolUse":
            deny(f"guard error ({type(e).__name__}); failing closed")


if __name__ == "__main__":
    main()
