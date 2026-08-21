#!/bin/sh
# One command reproduces everything in this experiment (issue #74).
#   sh run.sh
# Pinned: python3 >= 3.10; numpy 2.4.6, scipy 1.17.1 (SEARCH ONLY), sympy 1.14.0 (DERIVATION ONLY).
# The checker and the exact arithmetic depend on NOTHING outside the standard library.
set -e
cd "$(dirname "$0")"
CERTS=../../problems/circle-packing-equilateral-triangle/attacks/exact-algebraic-constructions/certificates

echo "== 1. regenerate the exact certificates =="
python3 construct.py --out "$CERTS"

echo
echo "== 2. verify them in exact arithmetic (independent checker) =="
python3 exact_check.py --dir "$CERTS" --quiet

echo
echo "== 3. tests: arithmetic, parser, negative controls, published-value agreement =="
python3 test_exact.py | tail -5

echo
echo "== 4. cross-check the two certificates already on main =="
python3 exact_check.py \
  ../../problems/circle-packing-equilateral-triangle/results/n003-lean-corners.json \
  ../../problems/circle-packing-equilateral-triangle/results/n006-lean-t3-lattice.json --quiet

echo
echo "== 5. (optional, ~2 min, needs numpy+scipy) regenerate the candidate search =="
echo "   python3 search.py --nmax 8 --starts 80 --seed 20260819 --out search_results.json"
