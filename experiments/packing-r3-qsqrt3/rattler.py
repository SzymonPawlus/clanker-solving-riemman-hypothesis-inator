"""Exact placement of the one rattler at n = 17 and n = 31.

A rattler is a point with strict slack in every constraint; its free region is
open and of positive measure, so ANY exact point of that region gives an equally
valid packing.  The optimiser's float position for it is arbitrary and (as
snap.py reports) is not a low-height element of Q(sqrt 3).

Method: enumerate candidate points (p/2 + q/2*sqrt3, u/2 + v/2*sqrt3) over small
integers, keep those exactly feasible against the already-snapped points, and
report the simplest.  FLOATS ARE USED ONLY TO PRE-FILTER CANDIDATES; every
candidate reported is re-checked in exact Q(sqrt 3) arithmetic here, and the
chosen point is checked again as part of the full certificate by check.py.
"""
from fractions import Fraction as F
from qsqrt3 import Q3, q3
import configs


def feasible_exact(pt, d, others):
    x, y = pt
    r = Q3(0, 1)
    if y < q3(0) or (r * x - y) < q3(0) or (r * (d - x) - y) < q3(0):
        return False
    for o in others:
        dx, dy = x - o[0], y - o[1]
        if dx * dx + dy * dy < q3(4):
            return False
    return True


def search(d, others, span=24, half=True):
    dens = (1, 2) if half else (1,)
    out = []
    for pn in range(-2 * span, 2 * span + 1):
        for pd in dens:
            for qn in range(-span, span + 1):
                for qd in dens:
                    x = Q3(F(pn, pd), F(qn, qd))
                    if x < q3(0) or x > d:
                        continue
                    for un in range(0, 2 * span + 1):
                        for ud in dens:
                            for vn in range(-span, span + 1):
                                for vd in dens:
                                    y = Q3(F(un, ud), F(vn, vd))
                                    if y < q3(0):
                                        continue
                                    if feasible_exact((x, y), d, others):
                                        cost = (x.a.denominator * x.b.denominator
                                                * y.a.denominator * y.b.denominator,
                                                abs(x.a.numerator) + abs(x.b.numerator)
                                                + abs(y.a.numerator) + abs(y.b.numerator))
                                        out.append((cost, x.sexpr(), y.sexpr()))
    out.sort()
    return out


if __name__ == "__main__":
    # exact search is expensive; run it on a narrow window around the known answer
    for n, idx in ((17, 13), (31, 13)):
        d = getattr(configs, "D%d" % n)
        pts = getattr(configs, "P%d" % n)
        others = [p for i, p in enumerate(pts) if i != idx]
        chosen = pts[idx]
        print("n = %d, rattler index %d" % (n, idx))
        print("  chosen placement: (%s, %s)" % (chosen[0].sexpr(), chosen[1].sexpr()))
        print("  exactly feasible against the other %d points: %s"
              % (len(others), feasible_exact(chosen, d, others)))
        # exhaustive exact confirmation that simpler rational alternatives exist,
        # over integer/half-integer coordinates in [0, d] x [0, d*sqrt3/2]
        alts = search(d, others, span=8, half=False)
        print("  simplest exactly-feasible integer alternatives found: %s"
              % ([(a, b) for _, a, b in alts[:5]] or "none in the integer window"))
        print()
