"""Independent uniform-level cell exhaustion: at which level does it actually close?

Compared against the level §5 says is 'needed'.  Everything exact (rational).
"""
from fractions import Fraction as F
import math, sys
from check_resolution import cells, close_at_level, threshold_level

CASES = [
    # n, d (rational), d(n) cited, label
    (5,  F(3998, 1000),  4,  "k=3, d=3.998"),
    (9,  F(59, 10),      6,  "k=4, d=5.9   (§4 says PROVED)"),
    (9,  F(55, 10),      6,  "k=4, d=5.5"),
    (14, F(799, 100),    8,  "k=5, d=7.99  (§4 says PROVED)"),
    (14, F(795, 100),    8,  "k=5, d=7.95  (§4 says PROVED)"),
    (14, F(75, 10),      8,  "k=5, d=7.5"),
    (20, F(97, 10),     10,  "k=6, d=9.7   (§4 says TIMEOUT)"),
    (27, F(1174, 100),  12,  "k=7, d=11.74 (§4 says TIMEOUT)"),
]
print(f"{'case':<32} {'rho':>9} {'L per §5':>9} {'closes at L':>12} {'note'}")
for n, d, dn, label in CASES:
    L5, thr, rho = threshold_level(n, d, dn)
    got = None; note = ""
    for L in range(1, 6):
        h = F(d) / 2 ** L
        if h >= 2:
            continue
        try:
            res, why = close_at_level(n, d, L, node_budget=300000)
        except Exception as e:
            note = f"L={L}: {e}"; break
        if res is None:
            note = f"L={L}: {why}"; break
        if res:
            got = (L, why); break
    s = f"L={got[0]}" if got else "not <=5"
    print(f"{label:<32} {rho:>9.6f} {L5:>9} {s:>12} {got[1] if got else note}")
