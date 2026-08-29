#!/bin/sh
# One command reproduces everything in this experiment (issue #132):
#
#     sh run.sh
#
# Pinned versions actually used:
#   CPython 3.11.15  -- the decision procedure imports only `fractions` from the standard
#                       library, so it has no external dependency at all.
#   sympy   1.14.0   -- used ONLY by crosscheck_sympy.py, an independent re-decision through
#                       sympy's own exact geometry. Nothing in the decider imports it.
# There is no random seed in the decider; the pseudorandom fixture generators are seeded
# explicitly (20260829) and the run is fully deterministic.
#
# Wall clock on the machine of record: validate ~1s, battery ~6s, hunt (20000 polygons)
# ~4.5 min, sympy cross-check ~10 min. Nothing here is compute-bound; every stage
# checkpoints to out/ as it goes.
set -e
cd "$(dirname "$0")"

echo "== 1. hand-checked unit tests, then the three controls in detail =="
python3 run.py validate

echo
echo "== 2. the full fixture battery -> out/fixtures/, out/summary.json =="
python3 run.py battery

echo
echo "== 3. seeded hunt for a counterexample to C1/C3 -> out/hunt.json =="
python3 run.py hunt --count 20000

echo
echo "== 4. independent re-decision of every named fixture with sympy -> out/crosscheck_sympy.json =="
python3 crosscheck_sympy.py
