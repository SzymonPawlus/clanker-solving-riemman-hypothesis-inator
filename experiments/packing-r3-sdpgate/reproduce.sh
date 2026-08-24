#!/usr/bin/env bash
# Single reproduce command for experiments/packing-r3-sdpgate.
# Deterministic: no random seeds are used anywhere in this experiment.
set -euo pipefail
cd "$(dirname "$0")"

python3 -c "import cvxpy" 2>/dev/null || pip install 'cvxpy==1.9.2'

echo "=== 1. S_n-isotypic block structure (exact integer arithmetic) ==="
python3 symmetry_sizes.py

echo
echo "=== 2. moment-relaxation machinery self-tests ==="
python3 moment_gate.py --selftest

echo
echo "=== 3. elementary mean-distance bound ==="
python3 elementary_bound.py

echo
echo "=== 4. dense level-2 strength gate (slow: 20-40 min) ==="
python3 -u moment_gate.py --sweep --level 2 --ns 4,5,6,7,8,10,12 --tcap 1.0 \
        --solver SCS --out results_reproduce.json
