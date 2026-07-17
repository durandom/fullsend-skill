# fullsend-skill

The `/fullsend` skill for developers working in a repository where Fullsend is
already installed. It discovers that repository's actual agents, skills,
workflows, and configuration sources before helping users operate agent runs.

## Install

```bash
npx skills add fullsend-ai/skill
```

Then invoke the skill from a repository where Fullsend is installed:

```text
/fullsend
/fullsend inspect 123456789
```

## Commands

| Command | Description |
|---------|-------------|
| `orient` | Explain the installation, available agents, skills, and configuration sources |
| `inspect` | Investigate a fullsend agent run — status, timing, output, logs |
| `trigger` | Post a verified Fullsend slash command to start an available agent |
| `watch` | Monitor a Fullsend run until completion |
| `help` | Answer from local installation evidence and link canonical upstream docs |

## Usage

```
/fullsend <command> [args]
```

Run `/fullsend` with no arguments for the command menu.

Installation, administration, configuration changes, upgrades, and agent
authoring are intentionally out of scope. The skill links to the canonical
[Fullsend guides](https://github.com/fullsend-ai/fullsend/tree/main/docs/guides)
for those tasks instead of duplicating them.

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
