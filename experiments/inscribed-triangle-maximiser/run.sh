#!/bin/sh
# Everything this lane claims, from one command.  ~4 minutes total on one core.
# CPython 3.11.15, standard library + numpy 2.4.6 (floats only ever PROPOSE; every
# reported number is re-derived exactly in Q(sqrt3)).
set -e
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1

echo "== tests (19) ==============================================="
python3 -m unittest discover -s tests -q

echo "== validate: the three hand-known answers ===================="
python3 run.py validate

echo "== fixtures: 190 committed fixtures, 2270 boundary points ===="
python3 run.py fixtures

echo "== global: vertices vs 8613 sampled edge points =============="
python3 run.py global

echo "== cw: exact upper bound for h = 1 + cos(5t)/24 =============="
python3 run.py cw 192 3600
