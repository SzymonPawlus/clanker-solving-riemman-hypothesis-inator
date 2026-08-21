#!/bin/sh
# All checks for problems/circle-packing-equilateral-triangle/attacks/eo-verification/.
# Python standard library only; exact arithmetic throughout; no floats decide anything.
set -e
cd "$(dirname "$0")"
for f in check_partition.py check_corner_deficit.py check_barrier.py check_cio_and_small.py; do
  echo "=== $f ==="
  python3 "$f"
  echo
done
