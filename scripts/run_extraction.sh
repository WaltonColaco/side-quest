#!/usr/bin/env bash
set -euo pipefail

# Runs the Markdown -> structured JSON extraction with OpenAI
# Usage: ./scripts/run_extraction.sh

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Allow overriding model via env var (default gpt-4.1)
MODEL_NAME="${MODEL_NAME:-gpt-4.1}"

# Pick a Python interpreter (prefers repo venv if present)
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

"$PYTHON" scripts/extract_md_to_structured.py \
  --markdown-dir markdown \
  --output-dir extracted_information \
  --ground-truth ground_truth_accessibility.json \
  --model "$MODEL_NAME" \
  --env-file .env
