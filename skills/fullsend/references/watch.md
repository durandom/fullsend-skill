# watch

Monitor a Fullsend GitHub Actions run through completion.

## Usage

```text
/fullsend watch <run-id | issue-or-PR>
```

## Prerequisites

- Load the current orientation report.
- Verify `gh auth status`.
- Resolve the GitHub repository.

## Procedure

1. If given a run ID, verify it with `gh run view`.
2. If given an issue or PR, inspect its Fullsend status comments and recent
   workflow runs. Match explicit run IDs or URLs; do not select an unrelated
   recent run merely because its event type looks plausible.
3. Report the run URL, workflow, status, conclusion, and elapsed time.
4. Poll with the environment's non-blocking wait mechanism. Recheck at a
   reasonable interval and keep the user informed during long runs.
5. When the run completes, report the final conclusion, failed-job names, and
   links. If the user requested diagnosis as well as monitoring, route the
   resolved run ID through the parent skill's `inspect` command.

If no associated run is visible yet, report that GitHub Actions may not have
created it and retry briefly. Do not fabricate an association.

## Report

Return the final conclusion, failed-job summary, and relevant links. If
monitoring stops, include the run URL and the last observed status.
