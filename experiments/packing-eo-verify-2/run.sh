#!/bin/sh
# Second verification pass -- all checks, exact arithmetic, Python standard library only.
# Exits non-zero if any check fails.
set -e
cd "$(dirname "$0")"
mkdir -p out
{
  python3 check_part1_arith.py
  python3 check_t1.py
  python3 check_t1_unbounded.py
  python3 check_lemma_t.py
  python3 check_resolution.py
  python3 break_p1.py
  python3 check_epsilon.py
  python3 covercheck.py
} 2>&1 | tee out/report.txt
