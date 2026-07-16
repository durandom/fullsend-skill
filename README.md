# fullsend-skill

The `/fullsend` skill for Claude Code — validate and debug Fullsend configuration,
trigger and inspect agent runs, and manage upgrades.

## Install

```bash
npx skills add fullsend-ai/skill
```

Then invoke the skill from any repository:

```text
/fullsend
/fullsend inspect 123456789
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
| `upgrade` | Upgrade CLI, scaffold files, and dispatch workflows |
| `help` | Onboarding companion — agent pipeline, local deployment overview |
| `custom-agents` | Guide for building custom standalone agents |

## Usage

```
/fullsend <command> [args]
```

Run `/fullsend` with no arguments for the command menu.

## Fullsend session history

Importing Fullsend sessions and visualizing them in AgentsView is available through
the separate [`fs-sessions` and `agentsview` skills](https://github.com/durandom/fullsend-sessions).
That repository contains the transcript import and viewer integration formerly bundled
here.

```bash
npx skills add -g git@github.com:durandom/fullsend-sessions.git \
  --skill fs-sessions agentsview \
  --agent claude-code codex \
  --copy -y
```
