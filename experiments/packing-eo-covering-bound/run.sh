#!/bin/sh
# One command reproduces every DECISION in attacks/eo-covering-bound/.
# (The float search that *proposed* the configurations is optimize.py / shrink.py / hop.py; its
#  output is already checked in under out/, and nothing it says decides anything.)
set -e
cd "$(dirname "$0")"
echo "== Theorem 1: corner-refined isodiametric floor (exact rational enclosures) =="
python3 bound_area.py
echo
echo "== Separated-point certificates: exact rational verification =="
python3 verify.py 22 23 24 25 26 27
echo
echo "== Independent re-check of the same certificates by the cartesian route =="
python3 recheck.py
echo
echo "== chi-vs-alpha gap search on the n=25 certificate (grid 1/16) =="
python3 gap.py 16 25
