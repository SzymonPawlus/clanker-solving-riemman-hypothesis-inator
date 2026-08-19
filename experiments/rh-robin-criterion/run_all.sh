#!/bin/sh
# Reproduce the whole experiment from one command. Takes ~4 minutes on one core.
# Tool versions pinned in VERSIONS.txt; no randomness anywhere (no seeds needed).
set -e
cd "$(dirname "$0")"
gcc -O2 -o sigma_sieve sigma_sieve.c -lm

# gate 1 (mandatory): reproduce the known Robin exception list below 5041
python3 validate_5040.py

# gate 2: cross-validate the C sieve against factorization-based sigma
python3 - <<'PY'
from robin_core import certified_threshold_double, sigma_exact
import subprocess, tempfile, os
with tempfile.TemporaryDirectory() as td:
    tab, dmp = os.path.join(td, "tab"), os.path.join(td, "dump")
    open(tab, "w").write(f"5041 105041 {certified_threshold_double(5041).hex()}\n")
    subprocess.run(["./sigma_sieve", tab, os.devnull, os.devnull, dmp], check=True)
    bad = 0
    for line in open(dmp):
        n, s = map(int, line.split())
        bad += (sigma_exact(n) != s)
    assert bad == 0, f"{bad} sigma mismatches"
    print("sieve cross-validation vs factorization sigma: 100000/100000 exact matches")
PY

# main run: certified thresholds, sieve to 1e9 (checkpointed), certify output
mkdir -p checkpoints
python3 - <<'PY'
from robin_core import certified_threshold_double
S, N, L = 1 << 20, 10**9, 5041
with open("checkpoints/thresholds.txt", "w") as f:
    while L < N:
        R = min(L + S, N)
        f.write(f"{L} {R} {certified_threshold_double(L).hex()}\n")
        L = R
PY
rm -f checkpoints/segments.csv checkpoints/candidates.txt
./sigma_sieve checkpoints/thresholds.txt checkpoints/segments.csv checkpoints/candidates.txt
python3 certify_results.py
