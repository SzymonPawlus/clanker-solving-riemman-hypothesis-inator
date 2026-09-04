#!/bin/sh
# Reproduces every check cited by problems/woodalls-conjecture/attacks/tau2-complete/README.md.
# Deterministic; pure Python 3 stdlib (recorded: Python 3.11.15).  Tests take ~1 minute.
# The optional counterexample hunts (numerical, all empty in the recorded runs) are behind --hunt.
set -e
cd "$(dirname "$0")"
python3 test_tau2.py
if [ "$1" = "--hunt" ]; then
  python3 hunt_counterexample.py --n 7 8 --seconds 45 --seed 152 --out hits_probe.json
  python3 hunt_counterexample.py --n 9 10 11 --seconds 300 --seed 153 --weightings 200 --out hits_n9-11.json
  python3 ring_family.py
  python3 ring_family2.py 270
  python3 build_counterexample.py || true
fi
