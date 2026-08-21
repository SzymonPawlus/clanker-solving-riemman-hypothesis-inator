"""K2/K3 controls: test the capacity machinery against REAL unit-separated packings.

Every certificate in the repo is an explicit configuration that provably exists.  If
any of them puts more points into a corner-coordinate box than `geom.capacity` allows,
the capacity code is wrong and every conclusion drawn from it is void.

The certificates use separation 2 and side 2a, so every coordinate is halved on load
(the same convention as ../packing-eo-hull-deficit and ../packing-oler-slack).
"""

import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "packing-oler-slack"))
import exact as EX                      # certificate parser + Q(sqrt3,sqrt11) arithmetic
import geom as G

CERT = os.path.join(os.path.dirname(__file__), "..", "..", "problems",
                    "circle-packing-equilateral-triangle", "attacks",
                    "exact-algebraic-constructions", "certificates")

SQ3_OVER_3 = EX.Alg.sqrt(3) / EX.Alg.rational(3)


def load(path):
    d = json.load(open(path))
    a = EX.parse_alg(d["point_triangle_side"]) / EX.Alg.rational(2)
    pts = [(EX.parse_alg(x) / EX.Alg.rational(2), EX.parse_alg(y) / EX.Alg.rational(2))
           for (x, y) in d["coordinates"]]
    return d["n"], a, pts


def corner_coords(a, p):
    x, y = p
    uA = x + y * SQ3_OVER_3
    uB = (a - x) + y * SQ3_OVER_3
    uC = a - y * SQ3_OVER_3 * EX.Alg.rational(2)
    return uA, uB, uC


def check_separation(pts):
    worst = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dx = pts[i][0] - pts[j][0]
            dy = pts[i][1] - pts[j][1]
            d2 = dx * dx + dy * dy
            if (d2 - EX.Alg.rational(1)).sign() < 0:
                return False, (i, j)
            if worst is None or (d2 - worst).sign() < 0:
                worst = d2
    return True, worst


def rational_above(alg, den=10 ** 6):
    """Smallest multiple of 1/den that is >= alg (exact decision)."""
    lo, hi = alg.interval(prec=40)
    import math
    q = F(math.ceil(hi * den), den)
    while (EX.Alg.rational(q) - alg).sign() < 0:
        q += F(1, den)
    return q


def run(verbose=True):
    files = sorted(f for f in os.listdir(CERT) if f.endswith(".json"))
    report = []
    for f in files:
        n, a, pts = load(os.path.join(CERT, f))
        if n < 3:
            continue
        ok, worst = check_separation(pts)
        assert ok, ("separation failure in " + f, worst)
        us = [corner_coords(a, p) for p in pts]
        # Viviani, exactly
        for (uA, uB, uC) in us:
            assert (uA + uB + uC - a * EX.Alg.rational(2)).is_zero(), ("Viviani", f)
            for u in (uA, uB, uC):
                assert u.sign() >= 0 and (a - u).sign() >= 0, ("containment", f)
        ap = rational_above(a)
        delta = EX.Alg.rational(ap) - a
        us2 = [(uA, uB + delta, uC + delta) for (uA, uB, uC) in us]
        J = int(ap)
        # S_j^{(V)} = #{u_V < j}, and the cited capacity of the open corner triangle
        srow = []
        for V in range(3):
            row = []
            for j in range(1, J + 2):
                s = sum(1 for u in us2 if (u[V] - EX.Alg.rational(j)).sign() < 0)
                cap = G.N_upper_open(j)
                assert s <= cap, ("open corner triangle capacity exceeded", f, V, j, s, cap)
                row.append(s)
            srow.append(row)
        # every integer box
        base = G.tri_constraints(ap)
        rng = [(l, h) for l in range(J + 2) for h in range(l + 1, J + 3)]
        worst_box = None
        nbox = 0
        for (lA, hA) in rng:
            for (lB, hB) in rng:
                for (lC, hC) in rng:
                    cnt = 0
                    for u in us2:
                        if (lA <= u[0] < hA and lB <= u[1] < hB and lC <= u[2] < hC):
                            cnt += 1
                    if cnt == 0:
                        continue
                    cons = list(base)
                    cons += G.bound_constraints(ap, 0, lA, hA)
                    cons += G.bound_constraints(ap, 1, lB, hB)
                    cons += G.bound_constraints(ap, 2, lC, hC)
                    cap = G.capacity(ap, cons)
                    nbox += 1
                    assert cnt <= cap, ("BOX CAPACITY EXCEEDED", f,
                                        (lA, hA, lB, hB, lC, hC), cnt, cap)
                    slack = cap - cnt
                    if worst_box is None or slack < worst_box[0]:
                        worst_box = (slack, (lA, hA, lB, hB, lC, hC), cnt, cap)
        report.append((f, n, ap, srow, nbox, worst_box))
        if verbose:
            print("  %-18s n=%2d  a<=%s  boxes tested %4d  tightest box %s"
                  % (f, n, ap, nbox, worst_box))
    return report


def cmp_int(u, j):
    return (u - EX.Alg.rational(j)).sign()


if __name__ == "__main__":
    run()
