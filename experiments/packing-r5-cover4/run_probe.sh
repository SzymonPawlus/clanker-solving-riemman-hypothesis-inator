#!/bin/sh
cd "$(dirname "$0")"
for spec in "2 4 25 1" "2 3 25 1" "3 9 25 1" "3 8 25 1" "3 8 25 2" "3 8 25 3"; do
  echo "### $spec"
  timeout 400 python3 minmaxdiam.py $spec 2>&1 | head -4
done
