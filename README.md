# fullsend-skill

The `/fullsend` skill for Claude Code — harness validation, drift checking, sandbox debugging, agent triggering, run inspection, and upgrade management.

## Install

```bash
npx skills add fullsend-ai/skill
```

## Commands

| Command | Description |
|---------|-------------|
| `validate` | Diff customized harness/env files against upstream scaffold |
| `inspect` | Investigate a fullsend agent run — status, timing, output, logs |
| `trigger` | Post a fullsend slash command to start an agent |
| `watch` | Monitor a triggered run until completion, then auto-inspect |
| `debug` | Run sandbox diagnostics |
| `comment` | Post a comment on an issue or PR |
| `label` | Add or remove a label on an issue or PR |
| `runs` | Browse fullsend runs in AgentsView |
| `upgrade` | Upgrade CLI, scaffold files, and dispatch workflows |
| `help` | Onboarding companion — agent pipeline, local deployment overview |
| `custom-agents` | Guide for building custom standalone agents |

## Usage

```
/fullsend <command> [args]
```

Run `/fullsend` with no arguments for the command menu.
