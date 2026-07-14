#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Install the Fullsend AgentsView integration into a repository.

Usage:
  setup-agentsview.sh [--force] [target-dir]

Arguments:
  target-dir  Destination directory (default: ./agentsview)

Options:
  --force     Replace managed files that differ; preserve artifacts and runs
  -h, --help  Show this help

The command is idempotent. Without --force, it refuses to overwrite modified
managed files. Generated artifacts/, runs/, runs-local/, and .env are never
copied or removed.
EOF
}

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="${SCRIPT_DIR}/../assets/agentsview"
TARGET_DIR="agentsview"
FORCE=false
TARGET_SET=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      FORCE=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [ "$TARGET_SET" = true ]; then
        echo "error: only one target directory may be provided" >&2
        usage >&2
        exit 2
      fi
      TARGET_DIR="$1"
      TARGET_SET=true
      shift
      ;;
  esac
done

if [ ! -d "$SOURCE_DIR" ]; then
  echo "error: bundled AgentsView assets not found at $SOURCE_DIR" >&2
  echo "Reinstall the fullsend skill and try again." >&2
  exit 1
fi

if [ -e "$TARGET_DIR" ] && [ ! -d "$TARGET_DIR" ]; then
  echo "error: target exists and is not a directory: $TARGET_DIR" >&2
  exit 1
fi

FILES=(
  ".gitignore"
  "Makefile"
  "docker-compose.fullsend.yaml"
  "scripts/fetch-artifacts.sh"
  "scripts/convert-artifacts.sh"
  "scripts/import-local-run.sh"
)

conflicts=()
for relative_path in "${FILES[@]}"; do
  destination="${TARGET_DIR}/${relative_path}"
  if [ -f "$destination" ] && ! cmp -s "${SOURCE_DIR}/${relative_path}" "$destination"; then
    conflicts+=("$relative_path")
  fi
done

if [ ${#conflicts[@]} -gt 0 ] && [ "$FORCE" = false ]; then
  echo "error: managed AgentsView files differ in $TARGET_DIR:" >&2
  printf '  %s\n' "${conflicts[@]}" >&2
  echo "Re-run with --force to update them; generated run data will be preserved." >&2
  exit 1
fi

installed=0
unchanged=0
for relative_path in "${FILES[@]}"; do
  source_file="${SOURCE_DIR}/${relative_path}"
  destination="${TARGET_DIR}/${relative_path}"
  mkdir -p "$(dirname "$destination")"
  if [ -f "$destination" ] && cmp -s "$source_file" "$destination"; then
    unchanged=$((unchanged + 1))
    continue
  fi
  cp "$source_file" "$destination"
  case "$relative_path" in
    scripts/*.sh) chmod +x "$destination" ;;
  esac
  installed=$((installed + 1))
done

echo "AgentsView integration ready in $TARGET_DIR ($installed installed, $unchanged unchanged)."
echo "Next: cd $TARGET_DIR && make fetch   # download and convert remote runs"
echo "      cd $TARGET_DIR && make local   # import local runs and start the viewer"
