#!/bin/sh
# Reproduces every number in
#   problems/circle-packing-equilateral-triangle/attacks/n16-budget/README.md
# Standard library + numpy/scipy.  scipy proposes LP duals; every reported LP
# value is re-derived from an exactly verified rational dual certificate, so no
# float takes part in any decision.  No network, no seeds, ~1 core, ~5 min cold
# (~10 s once out/fgrid.json is cached).
set -e
cd "$(dirname "$0")"
echo "== certified constants (pi by Machin vs Euler, sqrt, arcsin) =="
python3 exact.py
echo
echo "== certified LOWER bounds on f (explicit admissible sets) =="
python3 flower.py
echo
echo "== certified UPPER bounds on f (slab LP + exact dual certificates) =="
python3 fupper.py 128
echo
echo "== the pinned (3,3,3) area budget and its ceiling =="
python3 budget.py 128 48 192
