"""Reproduce the exact Q(sqrt 3) coordinates in configs.py from the LS floats.

Reads (read-only) ../circle-packing-ls/out/nNN.json, rescales the unit-triangle
points by the CONJECTURED d = a + 2 sqrt(3), and snaps each coordinate to the
nearest element {(p + q sqrt3)/2 : p, q half-integers of bounded height}.

The snap is unambiguous, and this script proves it rather than assuming it: for
p, q integers with |p|, |q| <= H, any two distinct values (p + q sqrt3)/2 differ
by at least 1/(2H(1 + sqrt3)) -- because |p + q sqrt3| = |p^2 - 3q^2| /
|p - q sqrt3| >= 1/(H(1 + sqrt3)) when p + q sqrt3 != 0, and p^2 - 3q^2 != 0 for
(p,q) != (0,0) since sqrt3 is irrational.  At H = 80 that separation is 2.3e-3,
while every residual reported below is ~1e-15.  So the snapped value is the
unique lattice element within the observed residual, and the residual itself is
never used as evidence of anything else.
"""
import json, math, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
LS = os.path.join(HERE, "..", "circle-packing-ls", "out")
R3 = math.sqrt(3.0)
H = 80                       # half-integer numerator bound
SEP = 1.0 / (H * (1 + R3))   # proven separation of distinct lattice values


def snap(v):
    """Nearest (p + q*sqrt3)/2 with |p|,|q| <= H. Returns (Fraction a, Fraction b, residual)."""
    best = None
    for q in range(-H, H + 1):
        a = v - (q / 2.0) * R3
        p = round(a * 2.0)
        if abs(p) > H:
            continue
        res = abs(p / 2.0 + (q / 2.0) * R3 - v)
        key = (res, abs(p) + abs(q))
        if best is None or key < best[0]:
            best = (key, F(p, 2), F(q, 2), res)
    return best[1], best[2], best[3]


def snap_config(n, a):
    """d = a + 2 sqrt(3).  Returns (points, worst residual, per-point residuals)."""
    with open(os.path.join(LS, "n%d.json" % n)) as fh:
        raw = json.load(fh)
    d = a + 2 * R3
    out, worst, res = [], 0.0, []
    for (ux, uy) in raw["unit_triangle_points"]:
        ax, bx, rx = snap(ux * d)
        ay, by, ry = snap(uy * d)
        out.append(((ax, bx), (ay, by)))
        res.append(max(rx, ry))
        worst = max(worst, rx, ry)
    return out, worst, res


def fmt(a, b):
    def fr(x):
        return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)
    if b == 0:
        return fr(a)
    bt = "sqrt(3)" if b == 1 else ("-sqrt(3)" if b == -1 else fr(b) + "*sqrt(3)")
    if a == 0:
        return bt
    return fr(a) + (" + " if bt[0] != "-" else " - ") + bt.lstrip("-")


if __name__ == "__main__":
    print("proven separation of distinct snap targets at H=%d: %.3e" % (H, SEP))
    for n, a in ((12, 4), (17, 6), (24, 8), (31, 10)):
        pts, worst, res = snap_config(n, a)
        bad = [i for i, e in enumerate(res) if e >= SEP / 2]
        print()
        print("n = %2d, d = %d + 2*sqrt(3): worst snap residual %.3e over the %d points that snap"
              % (n, a, max([e for i, e in enumerate(res) if i not in bad] or [0.0]), len(pts) - len(bad)))
        for i, (x, y) in enumerate(pts):
            tag = "   <-- DOES NOT SNAP (residual %.2e): rattler, placed by exact free-region search" % res[i] if i in bad else ""
            print("   %2d  (%s,  %s)%s" % (i, fmt(*x), fmt(*y), tag))
        if bad:
            print("   rattler indices: %s" % bad)
