# trigger

Post a Fullsend slash command to an issue or pull request after verifying that
the current installation exposes the requested agent or command.

## Usage

```text
/fullsend trigger <agent-or-/fs-command> <issue-or-PR> [instruction]
```

## Prerequisites

- Load the current orientation report.
- Verify `gh auth status` before GitHub reads or writes.
- Resolve the GitHub repository using the shared repository-resolution rules.

## Procedure

1. Normalize `agent`, `fs-agent`, or `/fs-agent` to `/fs-<agent>`.
2. Verify the command against the agents, harnesses, workflow conditions, or
   remote configuration found during orientation. Do not validate against a
   hardcoded stock-agent list.
3. Read the target with `gh issue view` or `gh pr view` and confirm its title,
   type, and state.
4. Preserve any user-provided instruction after the slash command. If the
   installation's agent definition or canonical agent documentation says an
   instruction is required, obtain it before continuing.
5. Preview the exact repository, target, and comment body. Obtain explicit user
   confirmation because the comment triggers shared automation.
6. Post with `gh issue comment <number> --repo <owner/name> --body <body>`.

If availability cannot be verified because a pinned remote source is
unreadable, stop before posting and explain what source could not be checked.

## Report

Return the comment URL, the verified agent/configuration evidence, and suggest
watching the resulting run.
