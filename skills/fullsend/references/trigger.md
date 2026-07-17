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
4. **Pre-flight sanity checks.** Before posting, verify the command will actually
   be dispatched. The router silently skips commands in several scenarios — warn
   the user instead of posting a comment that will be ignored.

   a. **Issue vs PR mismatch.** `/fs-fix` and `/fs-review` only dispatch on pull
      requests. If the target is an issue, warn the user and suggest `/fs-code`
      instead (or ask them to open a PR first).

   b. **Existing PR for issue.** `/fs-code` on an issue is skipped when an open,
      non-bot-authored PR already mentions the issue number in its title or body.
      Check with:
      ```bash
      gh pr list --repo <owner/name> --state open \
        --search "<issue-number> in:title,body" --json number,title,author
      ```
      Filter out PRs authored by `fullsend-ai[bot]` or `fullsend-ai-coder[bot]`.
      If human-authored PRs remain, warn the user: the code agent will be skipped
      because PR #N already references this issue. Suggest closing/merging that PR
      first, or confirm they want to post anyway (the comment will be silently
      ignored by the router).

   c. **Closed or merged target.** If the issue or PR is closed/merged, warn that
      the command is unlikely to trigger any agent.

   d. **Review agent does not checkout PR code.** The review agent's sandbox
      contains the **default branch HEAD** (main), not the PR branch. The PR diff
      is fetched via `gh api` (REST diff endpoint). This has two consequences:

      - **`AGENTS.md` / project instructions come from main.** If the PR adds or
        modifies `AGENTS.md`, the review agent will not see those changes until the
        PR merges. If the user expects new instructions to take effect, warn them.
      - **Source files in the sandbox are main's version.** The agent reads
        surrounding context from main. New files added by the PR do not exist on
        disk in the sandbox — the agent can only see them in the API diff.

      This is by design (security: prevents PRs from injecting code into the
      agent workflow). No action needed unless the user is confused about why
      the review agent ignored instructions from their PR branch.

5. Preserve any user-provided instruction after the slash command. If the
   installation's agent definition or canonical agent documentation says an
   instruction is required, obtain it before continuing.
6. Preview the exact repository, target, and comment body. Obtain explicit user
   confirmation because the comment triggers shared automation.
7. Post with `gh issue comment <number> --repo <owner/name> --body <body>`.

If availability cannot be verified because a pinned remote source is
unreadable, stop before posting and explain what source could not be checked.

## Report

Return the comment URL, the verified agent/configuration evidence, and suggest
watching the resulting run.
