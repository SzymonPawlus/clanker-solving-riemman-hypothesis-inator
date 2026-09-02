#!/bin/sh
# One command reproduces the whole V5 independent verification.
#   sh experiments/packing-n16-verify-5/verify.sh
# Pure CPython >= 3.8, standard library only for the exact gates
# (numpy/scipy are used ONLY by the optional configuration-comparison note and
#  decide nothing).  Runs in ~3 s on one core.
set -e
C=problems/circle-packing-equilateral-triangle/attacks/n16-upper-2/n16-certificate.json
echo "### 1. exact independent checker"
python3 experiments/packing-n16-verify-5/check_v5.py "$C"
echo
echo "### 2. corruption-rejection suite (the checker must reject each defect)"
python3 experiments/packing-n16-verify-5/attack_v5.py "$C"
echo
echo "### 3. contact graph / rattler / exact rigidity rank over Q(sqrt3)"
python3 experiments/packing-n16-verify-5/rigidity_v5.py "$C"
