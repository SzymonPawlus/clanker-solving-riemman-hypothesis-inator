#!/usr/bin/env sh
# Reproduce everything in this directory.  Python 3.11+, standard library only.
#
#   ./run.sh            tests + the closed-form tables + the short searches (~3 min)
#   ./run.sh full       additionally the Erdos-Oler sweep (~15 min wall on 4 cores)
#
# Every search is wall-clock limited from inside the process, so no job outlives its
# budget.  Results are written to out/ as they are produced; a run that does not say
# "proved" proves nothing.
set -e
cd "$(dirname "$0")"
mkdir -p out out/final

echo "== tests =="
python3 tests/test_eoex.py

echo
echo "== the bar: residual gap Erdos-Oler leaves for Oler's inequality (README 4.0) =="
python3 -m eoex gap --kmax 12 --out out/gap.json

echo
echo "== resolution theorem: level a cell method needs to reach ratio rho (README 3) =="
python3 -m eoex levels --kmax 7 --ratios 0.9 0.95 0.99 0.999

echo
echo "== short searches (pipeline validation against known values) =="
# k = 3, Erdos-Oler case n = 5, target d = 4.  Closes in 1 node at every d < 4 (README 4.1).
python3 -m eoex prove --n 5 --d 399/100 --max-level 7 --out out/k3-n5-d3.99.json  | tail -1
# k = 4, Erdos-Oler case n = 9, target d = 6.
python3 -m eoex prove --n 9 --d 57/10   --max-level 8 --out out/k4-n9-d5.7.json   | tail -1

if [ "$1" != "full" ]; then exit 0; fi

echo
echo "== full sweep: four concurrent single-core searches, 400 s each =="
run() { # n d max_level seconds tag
  python3 -m eoex prove --n "$1" --d "$2" --max-level "$3" --time-limit "$4" \
      --out "out/final/$5.json" > "out/final/$5.log" 2>&1 &
}
run 9  59/10    9  400 f-n9-5.9        # k=4
run 14 799/100  11 400 f-n14-7.99      # k=5
run 20 97/10    10 400 f-n20-9.7       # k=6, just above Oler's 9.68858
run 27 587/50   10 400 f-n27-11.74     # k=7, just above Oler's 11.73092
wait

echo
echo "== ablation: the per-node Oler-hull rule, on and off (README 4.5) =="
mkdir -p out/ablation
python3 -m eoex prove --n 14 --d 39/5 --max-level 10 --time-limit 400 \
    --out out/ablation/n14-7.8-hull-all.json --oler-hull-max-level 99 | tail -1
python3 -m eoex prove --n 14 --d 39/5 --max-level 10 --time-limit 400 \
    --out out/ablation/n14-7.8-nohull.json --no-oler-hull | tail -1

echo
for f in out/final/*.json out/ablation/*.json; do
  python3 -c "import json,sys;d=json.load(open(sys.argv[1]));\
print('%-32s n=%-3s d=%-9s %-10s nodes=%-9s %ss'%(sys.argv[1],d['n'],d['d'],d['status'],d['nodes'],d['elapsed_s']))" "$f"
done
