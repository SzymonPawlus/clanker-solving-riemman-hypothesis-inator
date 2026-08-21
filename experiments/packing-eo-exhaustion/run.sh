#!/usr/bin/env sh
# Reproduce everything in this directory.  Python 3.11+, standard library only.
#
#   ./run.sh            tests + the closed-form tables + the short searches (~3 min)
#   ./run.sh full       additionally the Erdos-Oler sweep (~30 min wall on 4 cores)
#
# Every search is wall-clock limited from inside the process, so no job outlives its
# budget.  Partial results are written to out/ as they are produced.
set -e
cd "$(dirname "$0")"
mkdir -p out

echo "== tests =="
python3 tests/test_eoex.py

echo
echo "== Erdos-Oler residual gap left by Oler's inequality =="
python3 -m eoex gap --kmax 12 --out out/gap.json

echo
echo "== short searches (validation of the pipeline against known values) =="
# k = 3: Erdos-Oler case n = 5, target d = 4.  Settled outright, see README.
python3 -m eoex prove --n 5  --d 399/100  --max-level 7  --out out/k3-n5-d3.99.json  | tail -1
# k = 4: Erdos-Oler case n = 9, target d = 6.
python3 -m eoex prove --n 9  --d 57/10    --max-level 8  --out out/k4-n9-d5.7.json   | tail -1

if [ "$1" != "full" ]; then exit 0; fi

echo
echo "== full sweep =="
run() { # n d max_level seconds tag
  python3 -m eoex prove --n "$1" --d "$2" --max-level "$3" --time-limit "$4" \
      --out "out/$5.json" > "out/$5.log" 2>&1 &
}
run 9  119/20   8  420 k4-n9-d5.95
run 14 77/10    10 420 k5-n14-d7.7
run 20 39/4     10 420 k6-n20-d9.75
run 27 47/4     10 420 k7-n27-d11.75
wait
run 9  599/100  9  420 k4-n9-d5.99
run 14 63/8     10 420 k5-n14-d7.875
run 20 199/20   10 420 k6-n20-d9.95
run 27 143/12   10 420 k7-n27-d11.9167
wait
grep -h '"status"' out/k*-*.json | sort | uniq -c
