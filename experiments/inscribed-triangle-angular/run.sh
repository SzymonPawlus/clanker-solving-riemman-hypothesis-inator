#!/bin/sh
# One command reproduces this experiment (the angular lane):
#
#     sh run.sh
#
# Pinned versions actually used on the machine of record:
#   CPython 3.11.15 -- the decider imports only `fractions`, `math`, `json`, `random` and
#                      `unittest` from the standard library.  There is NO external
#                      dependency: no sympy, no numpy, no library geometry predicate.
# Seeds: every generator is seeded explicitly (SEED = 20260829 in run.py, and the literal
# seeds in test_angular.py); the run is deterministic.
#
# Wall clock on the machine of record: unit tests ~45 s, validate ~2 s, fixtures ~23 s,
# structure ~20 s, explore ~4 min, critical ~5 s, hunt 1500 ~23 min.  The hunt is the only
# long stage; it checkpoints every 100 polygons, so cutting it short still leaves a result
# in out/hunt.json (the committed run was cut off at 1450 of 1500 by its wall-clock budget).
# Lower the hunt count for a short run.  Every stage checkpoints into out/.
set -e
cd "$(dirname "$0")"

echo "== 0. unit tests: the field, the direction order, collinear rays, both deciders =="
python3 -m unittest -q test_angular

echo
echo "== 1. hand-checked controls and the collinear-ray cases -> out/validate.json =="
python3 run.py validate

echo
echo "== 2. re-decide the sibling's 190 committed fixtures -> out/fixtures.json =="
python3 run.py fixtures

echo
echo "== 3. component structure of G(O) over the battery -> out/structure.json =="
python3 run.py structure

echo
echo "== 4. structure of G(O) on seeded non-convex polygons -> out/explore.json =="
python3 run.py explore

echo
echo "== 5. the critically good points, re-derived -> out/critical_fixture.json =="
python3 critical.py

echo
echo "== 6. exceptional-set census, every decision taken twice -> out/hunt.json =="
python3 run.py hunt 1500
