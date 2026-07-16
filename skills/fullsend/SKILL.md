---
name: fullsend
description: |
  Operates Fullsend from a repository where it is already installed. Discovers
  the repository's actual Fullsend installation, available agents, harnesses,
  skills, workflows, and configuration sources before helping users trigger,
  watch, or inspect agent runs. Use when asked what Fullsend can do in the
  current repo, which agents or skills are available, how an agent is configured,
  to run an `/fs-*` agent, monitor a run, investigate a failed run, or find the
  relevant upstream Fullsend user guide. This is not an installation,
  administration, upgrade, or agent-authoring skill.
---

# Fullsend

Use the Fullsend installation present in the current repository. Treat local
configuration and pinned workflow references as evidence; do not assume that a
stock agent set or a particular deployment layout is installed.

<essential_principles>

## Essential principles

1. **Orient before acting.** Load the repository's Fullsend context before every
   task unless it is already current in this conversation. Agent names, skills,
   workflow paths, and configuration sources vary by installation.
2. **The checkout is the starting point.** Resolve the git root from the current
   directory, then inspect its `.fullsend/` content and Fullsend workflow files.
   Follow pinned reusable-workflow or agent sources only when local files do not
   answer the user's question.
3. **Report observed facts separately from inference.** Label an agent or skill
   as available only when the installation exposes it. If a remote source cannot
   be read, report the source and the resulting uncertainty.
4. **Stay user-facing.** Help developers understand and operate an existing
   installation. Do not install or uninstall Fullsend, edit infrastructure,
   upgrade the CLI or scaffold, manage org enrollment, or build/customize agents.
   Point those requests to the canonical upstream guides.
5. **Confirm shared-state writes.** Show the exact repository, issue or PR, and
   comment body before posting a slash command. Read-only inspection needs no
   confirmation.
6. **Prefer canonical documentation.** Link to Fullsend's upstream guides rather
   than reproducing setup, configuration, or workflow documentation here.

</essential_principles>

<orientation>

## Mandatory orientation

Run:

```bash
python3 scripts/orient.py --repo <checkout-path>
```

Consume the complete JSON output. Do not filter it through `head`, `tail`,
`grep`, or `jq`. If the script cannot find Fullsend markers, state that this
checkout does not appear to use Fullsend and ask for the correct repository.

Read `references/orient.md` when the user asks about available agents, skills,
configuration, or when the local report contains unresolved remote sources.

</orientation>

<intake>

## Commands

| Command | Purpose |
|---|---|
| `orient [repo-path]` | Explain the installation, agents, skills, and configuration sources |
| `trigger <agent> <issue-or-PR>` | Post a verified `/fs-*` command |
| `watch <issue-or-PR-or-run-id>` | Monitor a run until it finishes |
| `inspect [issue-or-PR-or-run-id]` | Summarize run status, output, and failure evidence |
| `help [topic]` | Link to the relevant canonical user documentation |

If the user already expressed an intent, route directly. If invoked without an
intent, show this table and ask what they want to do.

</intake>

<routing>

## Routing

| Intent | Reference |
|---|---|
| `orient`, `agents`, `skills`, `config`, `how is this installed` | `references/orient.md` |
| `trigger`, `run`, `/fs-*` | `references/trigger.md` |
| `watch`, `wait`, `monitor` | `references/watch.md` |
| `inspect`, `status`, `logs`, `failed run`, `what happened` | `references/inspect.md` |
| `help`, `docs`, `guide`, `run locally` | `references/help.md` |

Load only the routed reference. Orientation is shared context, not a separate
user-visible prerequisite command.

</routing>

<repo_resolution>

## Repository resolution

Use this order:

1. An explicit path or `--repo owner/name` supplied by the user.
2. The git root containing the current working directory.
3. A parent directory containing `.fullsend/` or a Fullsend workflow.

For GitHub operations, derive `owner/name` from `git remote get-url origin` or
`gh repo view --json nameWithOwner`. Never use organization-specific fallback
paths or repositories.

</repo_resolution>

<boundaries>

## Out-of-scope requests

For installation, administration, configuration changes, agent authoring, or
upgrades, do not improvise a procedure. Explain that this skill is scoped to
users of an existing installation and link the matching page from the
[upstream guide index](https://github.com/fullsend-ai/fullsend/tree/main/docs/guides).

Session artifact importing and transcript visualization remain separate from
this skill.

</boundaries>
