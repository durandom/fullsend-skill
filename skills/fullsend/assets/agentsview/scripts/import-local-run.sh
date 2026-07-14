#!/usr/bin/env bash
# Import local fullsend agent runs into AgentsView's runs/ folder.
#
# Usage:
#   ./import-local-run.sh                      # auto-discover from $TMPDIR/fullsend
#   ./import-local-run.sh <output-dir>         # all runs in a specific output dir
#   ./import-local-run.sh <agent-dir>          # single agent run directory
#
# Without arguments, searches $TMPDIR/fullsend then /tmp/fullsend for agent-* dirs.
# Accepts either fullsend's --output-dir (discovers all agent-* subdirs)
# or a single agent run directory.
#
# Prerequisites: jq
#
# Directory layout produced (matches AgentsView Claude discovery):
#   runs-local/local_<agent>/local_issue-<N>_<iteration>_<transcript>.jsonl

set -euo pipefail

CACHE_ROOT="${FULLSEND_AGENTSVIEW_CACHE_DIR:-${XDG_CACHE_HOME:-${HOME}/.cache}/fullsend/agentsview}"
RUNS_DIR="${RUNS_DIR:-${CACHE_ROOT}/runs-local}"

usage() {
  cat <<'EOF'
Import local Fullsend run transcripts into the AgentsView session layout.

Usage:
  import-local-run.sh [output-dir|agent-dir]

With no path, search $TMPDIR/fullsend and /tmp/fullsend. Pass either a Fullsend
output directory containing agent-* children or one agent-* run directory.

Environment:
  FULLSEND_AGENTSVIEW_CACHE_DIR  Cache root (default: $XDG_CACHE_HOME/fullsend/agentsview)
  RUNS_DIR                       Session output override
EOF
}

case "${1:-}" in
  -h|--help) usage; exit 0 ;;
esac
if [ $# -gt 1 ]; then
  echo "error: only one input directory may be provided" >&2
  usage >&2
  exit 2
fi

INPUT_DIR="${1:-}"
if [ -z "$INPUT_DIR" ]; then
  # Auto-discover: check $TMPDIR/fullsend first (macOS per-user temp), then /tmp/fullsend
  for candidate in "${TMPDIR:-/tmp}/fullsend" "/tmp/fullsend"; do
    if [ -d "$candidate" ] && compgen -G "${candidate}/agent-*" >/dev/null 2>&1; then
      INPUT_DIR="$candidate"
      break
    fi
  done
  if [ -z "$INPUT_DIR" ]; then
    echo "error: no fullsend output directory found" >&2
    echo "" >&2
    echo "Searched:" >&2
    echo "  ${TMPDIR:-/tmp}/fullsend" >&2
    echo "  /tmp/fullsend" >&2
    echo "" >&2
    echo "Run with an explicit path or set TMPDIR:" >&2
    echo "  $0 /path/to/fullsend-output-dir" >&2
    exit 1
  fi
  echo "Auto-discovered: $INPUT_DIR"
fi

command -v jq >/dev/null 2>&1 || { echo "error: jq is required" >&2; exit 1; }

INPUT_DIR="$(cd "$INPUT_DIR" && pwd)"

# Collect agent directories: either the input itself or agent-* children
AGENT_DIRS=()
if [[ "$(basename "$INPUT_DIR")" == agent-* ]]; then
  AGENT_DIRS+=("$INPUT_DIR")
else
  while IFS= read -r -d '' d; do
    AGENT_DIRS+=("$d")
  done < <(find "$INPUT_DIR" -maxdepth 1 -type d -name 'agent-*' -print0)
fi

if [ ${#AGENT_DIRS[@]} -eq 0 ]; then
  echo "error: no agent-* directories found in $INPUT_DIR" >&2
  exit 1
fi

echo "Found ${#AGENT_DIRS[@]} agent run(s) in $INPUT_DIR"
echo

total_found=0
total_skipped=0

for AGENT_DIR in "${AGENT_DIRS[@]}"; do
  DIRNAME="$(basename "$AGENT_DIR")"

  # Parse agent-<name>-<issue>-<timestamp>, with issue optional.
  DIRNAME_NO_PREFIX="${DIRNAME#agent-}"
  if [[ "$DIRNAME_NO_PREFIX" =~ ^(.+)-([0-9]+)-([0-9]+)$ ]]; then
    AGENT_NAME="${BASH_REMATCH[1]}"
    ISSUE_NUM="${BASH_REMATCH[2]}"
    TIMESTAMP="${BASH_REMATCH[3]}"
  elif [[ "$DIRNAME_NO_PREFIX" =~ ^(.+)-([0-9]+)$ ]]; then
    AGENT_NAME="${BASH_REMATCH[1]}"
    ISSUE_NUM="unknown"
    TIMESTAMP="${BASH_REMATCH[2]}"
  else
    echo "  [skip] unrecognized run directory name: $DIRNAME" >&2
    continue
  fi

  # Derive ISO timestamp from the unix epoch in the directory name
  created_at=$(date -u -r "$TIMESTAMP" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ")

  DEST_DIR="${RUNS_DIR}/local_${AGENT_NAME}"
  mkdir -p "$DEST_DIR"

  echo "--- $DIRNAME ---"
  echo "  Agent: $AGENT_NAME | Issue: $ISSUE_NUM"

  found=0
  skipped=0

  while IFS= read -r -d '' jsonl; do
    iter=$(echo "$jsonl" | grep -oE 'iteration-[0-9]+' | head -1 || echo "iteration-1")
    dest_file="${DEST_DIR}/local_issue-${ISSUE_NUM}_${iter}_$(basename "$jsonl")"

    if [ -f "$dest_file" ]; then
      skipped=$((skipped + 1))
      continue
    fi

    meta_line=$(jq -nc \
      --arg agent "$AGENT_NAME" \
      --arg issue "$ISSUE_NUM" \
      --arg src "$AGENT_DIR" \
      --arg ts "$created_at" \
      --arg cwd "/fullsend/local_${AGENT_NAME}" \
      '{
        type: "user",
        timestamp: $ts,
        message: {
          content: ("[Local fullsend: \($agent)] issue #\($issue)\nSource: \($src)")
        },
        cwd: $cwd
      }')

    { echo "$meta_line"; cat "$jsonl"; } > "$dest_file"
    echo "  -> local_${AGENT_NAME}/$(basename "$dest_file")"
    found=$((found + 1))
  done < <(find "$AGENT_DIR" -name '*.jsonl' -path '*/transcripts/*' -print0)

  if [ "$found" -eq 0 ] && [ "$skipped" -eq 0 ]; then
    echo "  (no transcripts)"
  fi

  total_found=$((total_found + found))
  total_skipped=$((total_skipped + skipped))
done

echo
echo "Done: ${total_found} imported, ${total_skipped} already existed"
