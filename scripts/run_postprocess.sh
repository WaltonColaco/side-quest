#!/usr/bin/env bash
set -euo pipefail

# Run steps 4-6: normalize -> merge -> render
# Env overrides:
#   BUILDING_TYPE   (default: commercial_interiors)
#   DOC_PRIORITY    (default: "leed,standard")
#   PER_CATEGORY    (default: 12)

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

BUILDING_TYPE="${BUILDING_TYPE:-commercial_interiors}"
DOC_PRIORITY="${DOC_PRIORITY:-leed,standard}"
PER_CATEGORY="${PER_CATEGORY:-12}"

if [[ -x "./.venv/Scripts/python.exe" ]]; then
  PYTHON="./.venv/Scripts/python.exe"
elif command -v python >/dev/null 2>&1; then
  PYTHON="python"
elif command -v py >/dev/null 2>&1; then
  PYTHON="py -3"
else
  echo "No python interpreter found. Activate your venv or install Python." >&2
  exit 1
fi

"$PYTHON" scripts/normalize_json.py \
  --input-dir extracted_information \
  --output-dir normalized_information \
  --building-type "$BUILDING_TYPE"

"$PYTHON" scripts/merge_json.py \
  --input-dir normalized_information \
  --output merged/merged.json \
  --conflicts merged/conflicts.json \
  --doc-priority "$DOC_PRIORITY"

"$PYTHON" scripts/render_doc.py \
  --input merged/merged.json \
  --output reports/compiled.md \
  --per-category "$PER_CATEGORY"
