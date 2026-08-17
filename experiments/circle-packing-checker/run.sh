#!/usr/bin/env bash
# One command that reproduces this experiment from scratch.
#
#   ./run.sh
#
# Creates the pinned environment, regenerates the reference certificates, runs the
# exact checker over them, and runs the full validation suite (accepts + rejects).
set -euo pipefail

cd "$(dirname "$0")"

echo "== 1/4  pinned environment (uv, versions in pyproject.toml)"
uv sync --extra dev --frozen

echo
echo "== 2/4  regenerate reference certificates for n = 3, 6, 10"
uv run python make_certificates.py

echo
echo "== 3/4  exact check of the reference certificates (must all ACCEPT)"
uv run python -m packcheck --require-tight certificates/*.json

echo
echo "== 4/4  validation suite (accepts, rejects down to 1e-60, no-float audit)"
uv run pytest

echo
echo "OK"
