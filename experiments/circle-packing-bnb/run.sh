#!/usr/bin/env bash
# One command that reproduces this experiment, given `uv`.
#
#   ./run.sh            # tests + the short reproductions (a few minutes)
#   ./run.sh full       # additionally re-runs the long n = 12 and n = 16 searches
#
# PREREQUISITE: `uv` on PATH.  Everything else -- the interpreter and pytest, at the
# versions pinned in pyproject.toml -- is installed by step 1.  Deliberately does not
# install `uv` itself.  https://docs.astral.sh/uv/getting-started/installation/
#
# The search is exact integer arithmetic and has no randomness anywhere, so there is no
# seed to pin: every run below is bit-for-bit deterministic given (n, d, max_level,
# max_cited, symmetry).  Only the wall-clock numbers vary.
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v uv > /dev/null 2>&1; then
  echo "run.sh needs 'uv' on PATH; it is the only thing you have to install yourself." >&2
  exit 127
fi

MODE="${1:-short}"

echo "== 1/4  pinned environment"
uv sync --extra dev

echo
echo "== 2/4  cited constants d(k), as outward-rounded enclosures"
uv run python -m cpbnb constants

echo
echo "== 3/4  test suite (interval soundness, subdivision cover, prune-rule soundness)"
uv run pytest

echo
echo "== 4/4  reproductions"
mkdir -p out

echo "-- the known-answer gate: proved below every cited d(n), never proved at or above"
uv run python -m cpbnb validate

echo
echo "-- headline n = 12 bound, no literature input (--max-cited 2)"
uv run python -m cpbnb prove --n 12 --d 6.95 --max-level 6 --max-cited 2 \
    --out out/repro-n12-d6_95-L6.json | tail -4

echo
echo "-- headline n = 16 bound, no literature input"
uv run python -m cpbnb prove --n 16 --d 7.999 --max-level 6 --max-cited 2 \
    --out out/repro-n16-d7_999-L6.json | tail -4

if [ "$MODE" = "full" ]; then
  echo "-- n = 12, tighter (minutes to hours)"
  uv run python -m cpbnb prove --n 12 --d 6.8 --max-level 6 --max-cited 2 \
      --checkpoint out/repro-n12-d6_8-L6.ckpt.json \
      --out out/repro-n12-d6_8-L6.json --time-limit 3600 | tail -4
  echo "-- n = 16 (this is the one that may not close; it checkpoints)"
  uv run python -m cpbnb prove --n 16 --d 8.05 --max-level 5 --max-cited 15 \
      --checkpoint out/repro-n16-d8_05-L5.ckpt.json \
      --out out/repro-n16-d8_05-L5.json --time-limit 3600 | tail -4
fi

echo
echo "OK"
