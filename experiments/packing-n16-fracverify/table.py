#!/usr/bin/env python3
"""K2 deliverable: the LP-value-vs-N table for the fractional lane, plus the
exact statement of what bound each row would have given had it verified.

A row verifies iff lp_value < budget.  The bound from a verified row is
N/sqrt(Qmax) with Qmax the exact maximal squared diameter in grid units^2,
NOT N/(UNIT-1) -- that is only the worst case Qmax = (UNIT-1)^2.
"""
import json, os, sys
from fractions import Fraction as F

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "packing-n16-fractional", "certs", "results.jsonl")
rows = []
with open(SRC) as f:
    for line in f:
        line = line.strip()
        if line:
            rows.append(json.loads(line))

REC_SQ = None  # 1+2*sqrt3, compared numerically only for the "beats?" column
rec = 1 + 2 * 3 ** 0.5
print(f"{'label':>6} {'N':>5} {'budget':>7} {'lp_value':>12} {'status':>10} "
      f"{'a=N/64':>9} {'bound if verified':>18} {'beats 1+2sqrt3?':>16}")
for r in sorted(rows, key=lambda r: (r.get("label", ""), r.get("N", 0))):
    N, b = r.get("N"), r.get("budget")
    lp = r.get("lp_value")
    st = r.get("status")
    qmax = r.get("qmax")
    if qmax:
        q = F(qmax) if isinstance(qmax, str) else F(qmax)
        bound = N / (float(q) ** 0.5)
    else:
        bound = N / 63.0        # worst case, only indicative
    lp_s = f"{lp:.6f}" if isinstance(lp, (int, float)) else str(lp)
    print(f"{r.get('label',''):>6} {N:>5} {b:>7} {lp_s:>12} {st:>10} "
          f"{N/64:>9.5f} {bound:>18.7f} {str(bound > rec):>16}")
print()
print(f"record 1+2sqrt3 = {rec:.7f};  a row is a repo record only if it is "
      f"BOTH verified AND its bound exceeds that.")
