#!/bin/sh
# Reproduces the full census reported in
# problems/woodalls-conjecture/attacks/zero-weight-frontier/README.md
# Deterministic: no seeds, no dependencies beyond the Python 3 stdlib.
# Recorded run: Python 3.11.15, ~4 min total on one core.
set -e
cd "$(dirname "$0")"
mkdir -p out
python3 test_census.py                                             # 13 known-answer tests
python3 census.py --nmin 2 --nmax 5 --ly-nmax 5           --out out   # {0,1},  n <= 5
python3 census.py --nmin 6 --nmax 6 --ly-nmax 5           --out out   # {0,1},  n = 6
python3 census.py --nmin 2 --nmax 5 --ly-nmax 0 --wmax 2  --out out   # {0,1,2}, n <= 5
