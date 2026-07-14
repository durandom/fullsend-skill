# fullsend-skill

The `/fullsend` skill for Claude Code — validate and debug Fullsend configuration,
trigger and inspect agent runs, browse transcript history, and manage upgrades.

## Install

```bash
npx skills add fullsend-ai/skill
```

Then invoke the skill from any repository:

```text
/fullsend
/fullsend inspect 123456789
/fullsend runs setup
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
| `runs` | Install AgentsView integration and browse local or remote fullsend runs |
| `upgrade` | Upgrade CLI, scaffold files, and dispatch workflows |
| `help` | Onboarding companion — agent pipeline, local deployment overview |
| `custom-agents` | Guide for building custom standalone agents |

## Usage

```
/fullsend <command> [args]
```

Run `/fullsend` with no arguments for the command menu.

## AgentsView transcript history

`/fullsend runs setup` installs the bundled AgentsView integration into the current
repository. The integration can fetch GitHub Actions artifacts, reconstruct Fullsend
execution context, preserve nested subagent sessions, import local runs, and start a
containerized transcript viewer.

Run data is shared across repositories by default:

```text
${XDG_CACHE_HOME:-$HOME/.cache}/fullsend/agentsview/
├── artifacts/   # downloaded artifact ZIPs, workflow logs, revision context
├── runs/        # converted remote sessions
└── runs-local/  # imported local sessions
```

This keeps generated history out of whichever repository installed the skill. Override
the cache root when isolation is useful:

```bash
cd agentsview
FULLSEND_AGENTSVIEW_CACHE_DIR="$HOME/.cache/my-team/fullsend" make fetch
```

Advanced overrides are also available: `ARTIFACTS_DIR`, `RUNS_DIR`, and
`RUNS_LOCAL_DIR`. Run `make paths` inside `agentsview/` to see the resolved locations.

Repository-local caches created by older versions are not deleted. To continue using
one, set `FULLSEND_AGENTSVIEW_CACHE_DIR="$PWD"` while inside that repository's
`agentsview/` directory.
