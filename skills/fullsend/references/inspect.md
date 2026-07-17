# inspect

Investigate a Fullsend run using GitHub Actions metadata, status comments, job
logs, and artifacts available to the user.

## Usage

```text
/fullsend inspect [run-id | issue-or-PR]
```

## Prerequisites

- Load the current orientation report.
- Verify `gh auth status`.
- Resolve the GitHub repository.

## Procedure

1. Resolve a specific run. For an issue or PR, use Fullsend status-comment run
   links or IDs and corroborate them with Actions metadata. With no argument,
   inspect the most recent run from a workflow identified during orientation.
2. Gather `gh run view <id> --json` metadata, including jobs, timestamps,
   conclusion, event, URL, branch, and commit.
3. Fetch failed job logs with `gh run view <id> --log-failed`. Quote only the
   minimal lines needed to establish the failure.
4. List run artifacts. Download relevant, unexpired artifacts to a temporary
   directory when logs do not explain the result or the user asks about agent
   behavior. Do not assume a fixed artifact name or directory layout.
5. Correlate the run with Fullsend status comments, resulting commits, branches,
   or pull requests when those identifiers are present.
6. Separate infrastructure/workflow failures, sandbox/runtime failures, agent
   task failures, and successful runs with unexpected output. Base diagnoses on
   observed evidence and label inference explicitly.
7. **Review agent sandbox context.** When inspecting a review run, remember that
   the sandbox contains default branch HEAD (main), not the PR branch. The agent
   reads the PR diff via API. If the user reports the agent ignored `AGENTS.md`
   or project instructions added in the PR, check whether those changes have
   merged to main — unmerged changes are invisible to the review agent's sandbox.
7. Remove temporary downloads after analysis unless the user asked to keep them.

Do not import sessions or start a transcript viewer; those capabilities are
maintained separately.

## Report

```markdown
## Fullsend run <id>

- Status: <status / conclusion>
- Workflow and agent: <observed values>
- Trigger: <event and issue/PR when known>
- Duration: <elapsed>
- Result: <commit/PR/status comment when known>

### Findings
- <evidence-backed finding>

### Likely cause
<cause, explicitly marked as inference when necessary>

### Next action
<smallest useful user action>
```

If evidence is incomplete, say which logs or artifacts were unavailable.
