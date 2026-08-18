#!/usr/bin/env bash
# One command that reproduces this experiment, given `uv`.
#
#   ./run.sh
#
# PREREQUISITE: `uv` on PATH. Everything else -- the Python interpreter, sympy,
# pytest, all at the versions locked in uv.lock -- is installed by step 1. This
# script deliberately does not install `uv` itself: that would mean piping a remote
# installer into a shell, which is not something a verification tool should do
# behind your back. See https://docs.astral.sh/uv/getting-started/installation/.
#
# Creates the pinned environment, regenerates the reference certificates, runs the
# exact checker over them, and runs the full validation suite (accepts + rejects).
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v uv > /dev/null 2>&1; then
  echo "run.sh needs 'uv' on PATH; it is the only thing you have to install yourself." >&2
  echo "Install it from https://docs.astral.sh/uv/getting-started/installation/ and rerun." >&2
  exit 127
fi

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
