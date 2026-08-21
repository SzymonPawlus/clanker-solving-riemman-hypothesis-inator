#!/bin/sh
# Reproduces every number in
#   problems/circle-packing-equilateral-triangle/attacks/n16-covering-limit/README.md
# Standard library + numpy/scipy (LP solve only; the LP's VALUE is then re-derived
# from an exact rational dual certificate, so no float takes part in a decision).
# Runtime ~7 min cold, ~35 s once out/f_grid.json is cached; no network.
set -e
cd "$(dirname "$0")"
echo "== certified constants =="
python3 exactconst.py
echo
echo "== f(l): certified upper bounds and the resulting bound on A_15 =="
python3 outer.py 128 48
echo
echo "== the method's own ceiling =="
python3 ceiling.py
echo
echo "== numerical slack check (lower bounds on f, status: numerical) =="
python3 f_lower.py
