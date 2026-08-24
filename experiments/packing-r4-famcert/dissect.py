"""Dissect the existing r3-qsqrt3 certificates into grain structure.

Read-only analysis of experiments/packing-r3-qsqrt3/certificates/*.json.
Hypothesis under test (the round-4 lens's claimed mechanism):

  every point is a point of the triangular lattice L = {(2i+r, r*sqrt3)} shifted
  by ONE OF FOUR FIXED offsets
      g_BL = (0,0)   g_BR = (2sqrt3, 0)   g_C = (sqrt3, 1)   g_T = (sqrt3, 3)
  i.e. four same-orientation grains separated by length-2 "stacking-fault" seams
  (|(sqrt3,1)| = |(0,2)| = 2; g_BR = (sqrt3,1)+(sqrt3,-1)).
"""
import os
from fractions import Fraction as F
from qsqrt3 import Q3, q3
from parse import load_certificate

R3DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "packing-r3-qsqrt3", "certificates")

OFFSETS = {
    "BL": (Q3(0, 0), Q3(0, 0)),
    "BR": (Q3(0, 2), Q3(0, 0)),
    "C":  (Q3(0, 1), Q3(1, 0)),
    "T":  (Q3(0, 1), Q3(3, 0)),
}


def lattice_coords(pt, off):
    """If pt - off is a point of L = {(2i+r, r sqrt3)}, return (i, r); else None."""
    x = pt[0] - off[0]
    y = pt[1] - off[1]
    # y must be r*sqrt3 with r a non-negative integer
    if y.a != 0:
        return None
    if y.b.denominator != 1:
        return None
    r = int(y.b)
    if x.b != 0 or x.a.denominator != 1:
        return None
    xi = int(x.a)
    if (xi - r) % 2 != 0:
        return None
    return ((xi - r) // 2, r)


def dissect(n, path):
    cert, pts, s, d = load_certificate(path)
    print("=" * 72)
    print("n = %d   s = %s   d = %s" % (n, s.sexpr(), d.sexpr()))
    grains = {k: [] for k in OFFSETS}
    unexplained = []
    for p in pts:
        hit = None
        for name, off in OFFSETS.items():
            lc = lattice_coords(p, off)
            if lc is not None:
                hit = (name, lc)
                break
        if hit is None:
            unexplained.append(p)
        else:
            grains[hit[0]].append(hit[1])
    for name in ("BL", "BR", "C", "T"):
        g = sorted(grains[name], key=lambda t: (t[1], t[0]))
        rows = {}
        for i, r in g:
            rows.setdefault(r, []).append(2 * i + r)
        print("  grain %-2s  (offset %s, %s)  %2d points" %
              (name, OFFSETS[name][0].sexpr(), OFFSETS[name][1].sexpr(), len(g)))
        for r in sorted(rows):
            print("      row r=%d  x = %s" % (r, sorted(rows[r])))
    print("  unexplained by the 4-offset hypothesis: %d  %s" %
          (len(unexplained), [(p[0].sexpr(), p[1].sexpr()) for p in unexplained]))
    tot = sum(len(v) for v in grains.values())
    print("  TOTAL explained %d / %d" % (tot, len(pts)))
    return grains, unexplained


if __name__ == "__main__":
    for n in (17, 24, 31):
        dissect(n, os.path.join(R3DIR, "n%03d-r3-qsqrt3.json" % n))
