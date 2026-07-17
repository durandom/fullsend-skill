# fullsend-skill

A user-facing skill for operating Fullsend from a repository where it is
already installed. It first discovers that repository's actual agents, skills,
workflows, and configuration sources, then helps developers trigger, monitor,
and investigate agent runs.

## Install

Install the skill globally so it is available from every Fullsend-enabled
repository:

```bash
npx skills add -g durandom/fullsend-skill \
  --skill fullsend \
  --agent claude-code codex \
  -y
```

Omit `--agent claude-code codex` to let the installer select from detected
agents interactively. To install only in the current project, omit `-g`.

Update a global installation with:

```bash
npx skills update -g fullsend
```

Then open a repository where Fullsend is installed and ask the agent to use
Fullsend, for example:

```text
/fullsend
/fullsend orient
/fullsend inspect 123456789
```

In clients without slash-command syntax, use the same requests in plain
language, such as `Use fullsend to inspect run 123456789`.

## Commands

| Command | Description |
|---------|-------------|
| `orient` | Explain the installation, available agents, skills, and configuration sources |
| `inspect` | Investigate a fullsend agent run — status, timing, output, logs |
| `trigger` | Post a verified Fullsend slash command to start an available agent |
| `watch` | Monitor a Fullsend run until completion |
| `help` | Answer from local installation evidence and link canonical upstream docs |

## Usage

```text
/fullsend <command> [args]
```

Run `/fullsend` with no arguments for the command menu. The skill begins from
the current checkout and uses its local Fullsend configuration as the source of
truth.

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
