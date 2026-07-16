# orient

Build an evidence-based map of the Fullsend installation used by the checkout.

## Usage

```text
/fullsend orient [repo-path]
```

## Prerequisites

Run `python3 scripts/orient.py --repo <repo-path>` and consume its complete JSON
output before continuing.

## Procedure

1. Confirm the resolved git root and installation markers.
2. Classify the installation only when the files establish the mode. Otherwise
   report `unknown`; do not infer a mode from the repository name.
3. Inventory local harnesses and agent definitions. For each harness, report its
   name, `role`, `slug`, agent definition, declared skills, model, runtime,
   image, policy, providers, plugins, timeout, base, and source when present.
   List mounted file sources only by path; never read credential contents.
4. Inventory repository skills from `.agents/skills/` and `.claude/skills/`.
   Record the skill name and description from `SKILL.md`; indicate symlinked or
   duplicate paths without counting the same resolved directory twice.
5. Report Fullsend workflow files and their pinned `uses:` references.
6. If agent or skill availability remains unresolved and a workflow points to a
   remote repository, use read-only `gh api` calls to inspect the referenced path
   at its pinned ref. Do this only when `gh` is authenticated. If it is not, show
   the unresolved source and continue; do not ask the user to install tooling.
7. Treat deprecated `customized/` content as an observed legacy layer, not as a
   recommended configuration mechanism.

Do not expose secret values. List environment file names and variable names only
when they materially explain an agent's runtime configuration.

## Report

```markdown
## Fullsend orientation: <repo>

- Installation: <per-repo | per-org | local definitions | unknown>
- Evidence: <marker files>
- Configuration sources: <local paths and pinned remote sources>

### Available agents
| Agent | Role | Definition | Skills | Runtime/config | Evidence |
|---|---|---|---|---|---|

### Repository skills
| Skill | Description | Path |
|---|---|---|

### Workflows
| Workflow | Remote sources | Slash commands observed |
|---|---|---|

### Unknowns
- <anything hidden behind an unreadable source>
```

Omit empty sections. Keep paths relative to the repository root.

## Success criteria

- Every reported agent and skill has a local or pinned-remote evidence source.
- The report identifies where configuration comes from.
- Unknowns are explicit rather than filled with Fullsend defaults.
