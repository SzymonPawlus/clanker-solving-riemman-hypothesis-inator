#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v uv >/dev/null 2>&1; then
  echo "recover_n16.sh needs uv to use the neighbouring pinned mpmath environment" >&2
  exit 127
fi

uv run --project ../circle-packing-search --frozen python recover_n16.py
