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
# explore ~4 min, critical ~5 s, hunt 1500 ~23 min.  Every stage checkpoints into out/.
# Drop the last line, or lower its count, for a short run.
set -e
cd "$(dirname "$0")"

echo "== 0. unit tests: the field, the direction order, collinear rays, the deciders =="
python3 -m unittest -q test_angular

echo
echo "== 1. hand-checked controls and the collinear-ray cases -> out/validate.json =="
python3 run.py validate

echo
echo "== 2. re-decide the sibling's 190 committed fixtures -> out/fixtures.json =="
python3 run.py fixtures

echo
echo "== 3. structure of the good-direction set G(O) -> out/explore.json =="
python3 run.py explore

echo
echo "== 4. the critically good points, re-derived -> out/critical_fixture.json =="
python3 critical.py

echo
echo "== 5. exceptional-set census -> out/hunt.json =="
python3 run.py hunt 1500
