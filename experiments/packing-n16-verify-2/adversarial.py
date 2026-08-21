#!/usr/bin/env python3
"""
Attempts to BREAK the n=16 covering certificate, before accepting its argument.

Everything here is exact rational arithmetic.  Attacks tried:

  A. The three corners of T_a, and the exact midpoints/quarter-points of its three
     edges -- a sliver hides on the boundary, where a chart-area argument is least
     intuitive and where the grid probe (offset off the boundary) never looks.
  B. A dense 1-D probe along each of the three edges of T_a.
  C. A dense probe in a small neighbourhood of every piece VERTEX -- if two pieces
     meet at a point with a wedge missing, that hole is anchored at a vertex.
  D. The realised diameter: for the piece attaining the maximum, exhibit the two
     points and confirm they are at distance < 1, and confirm that the SECOND
     largest squared diameter is also < 1 (guards against a single lucky pair).
  E. The converse sanity check: does T_a at the CEILING a = 4.6247636 admit a
     15-piece covering by these pieces scaled up?  (It must NOT, since a 16-point
     packing exists there.)  Scaling the certificate by mu = ceiling/a multiplies
     every squared diameter by mu^2; report that value.
  F. Pigeonhole arithmetic: confirm 15 < 16 and that the certificate does not
     secretly contain 16 pieces after merging duplicates.
"""

import json
import itertools
from fractions import Fraction as F

from covercheck import (qform, orient_ccw, point_in_convex, shoelace2,
                        convex_intersection_area2, rat, CEILING)

CERT = "../packing-n16-covering/sub_s2_cert.json"

raw = json.load(open(CERT))
a = rat(raw["a"])
faces = [[(rat(c[0]), rat(c[1])) for c in f] for f in raw["faces_uv"]]
ccw = [orient_ccw(list(f)) for f in faces]

fails = 0


def covered(p):
    return [i for i, f in enumerate(ccw) if point_in_convex(f, p)[0]]


def report(name, ok, detail=""):
    global fails
    print("  [%s] %s%s" % ("ok  " if ok else "FAIL", name,
                           ("  -- " + detail) if detail else ""))
    if not ok:
        fails += 1


print("=" * 78)
print("ADVERSARIAL PASS -- trying to break %s" % CERT)
print("a = %s = %.10f,  %d pieces" % (a, float(a), len(faces)))
print("=" * 78)

# ---------------------------------------------------------------- A. corners
print("\nA. corners and distinguished boundary points")
special = {
    "corner (0,0)": (F(0), F(0)),
    "corner (a,0)": (a, F(0)),
    "corner (0,a)": (F(0), a),
    "mid of edge v=0": (a / 2, F(0)),
    "mid of edge u=0": (F(0), a / 2),
    "mid of hypotenuse": (a / 2, a / 2),
    "quarter u-edge": (a / 4, F(0)),
    "3/4 u-edge": (3 * a / 4, F(0)),
    "quarter v-edge": (F(0), a / 4),
    "3/4 v-edge": (F(0), 3 * a / 4),
    "quarter hyp": (a / 4, 3 * a / 4),
    "3/4 hyp": (3 * a / 4, a / 4),
    "centroid": (a / 3, a / 3),
}
for name, p in special.items():
    c = covered(p)
    report("%-20s covered by pieces %r" % (name, c), len(c) >= 1)

# ---------------------------------------------------------------- B. edges
print("\nB. dense exact probe along each edge of T_a (2001 points per edge)")
N = 2000
for label, param in (("v = 0   ", lambda t: (a * t, F(0))),
                     ("u = 0   ", lambda t: (F(0), a * t)),
                     ("u+v = a ", lambda t: (a * t, a * (1 - t)))):
    holes = []
    for k in range(N + 1):
        t = F(k, N)
        p = param(t)
        if not covered(p):
            holes.append((str(p[0]), str(p[1])))
    report("edge %s fully covered" % label, not holes,
           "holes at %r" % holes[:4] if holes else "")

# ---------------------------------------------------------------- C. vertices
print("\nC. neighbourhood of every piece vertex (8 directions, eps = 1/10^7)")
eps = F(1, 10 ** 7)
dirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
allv = sorted({v for f in faces for v in f})
print("   distinct piece vertices: %d" % len(allv))
holes = []
for (u, v) in allv:
    for du, dv in dirs:
        p = (u + du * eps, v + dv * eps)
        if p[0] < 0 or p[1] < 0 or p[0] + p[1] > a:
            continue          # outside T_a, nothing to cover
        if not covered(p):
            holes.append((str(p[0]), str(p[1])))
report("no uncovered point near any piece vertex", not holes,
       "holes at %r" % holes[:4] if holes else "%d in-T_a samples clean"
       % (len(allv) * 8 - 0))

# ---------------------------------------------------------------- D. diameter
print("\nD. the diameter, and how much room it has")
pairs = []
for i, f in enumerate(faces):
    for p, q in itertools.combinations(f, 2):
        pairs.append((qform(p[0] - q[0], p[1] - q[1]), i, p, q))
pairs.sort(reverse=True)
for rank in range(3):
    d, i, p, q = pairs[rank]
    print("   #%d  piece %2d  sq.diam = %s = %.12f  %s"
          % (rank + 1, i, d, float(d), "< 1" if d < 1 else ">= 1  <-- FATAL"))
report("largest squared diameter strictly < 1", pairs[0][0] < 1)
report("second largest strictly < 1", pairs[1][0] < 1)
slack = 1 - pairs[0][0]
print("   slack 1 - maxdiam^2 = %s = %.3e" % (slack, float(slack)))

# per-piece maxima, so no piece is silently at 1
per = []
for i, f in enumerate(faces):
    per.append(max(qform(p[0] - q[0], p[1] - q[1])
                   for p, q in itertools.combinations(f, 2)))
report("every one of the %d pieces has sq.diam < 1" % len(faces),
       all(d < 1 for d in per))
print("   per-piece squared diameters (sorted): %s"
      % ", ".join("%.9f" % float(d) for d in sorted(per, reverse=True)))

# ---------------------------------------------------------------- E. ceiling
print("\nE. what the same pieces would give if scaled to the ceiling")
mu = CEILING / a
print("   mu = ceiling/a = %s = %.10f" % (mu, float(mu)))
scaled = pairs[0][0] * mu * mu
print("   scaled max squared diameter = %.10f  (%s 1)"
      % (float(scaled), "<" if scaled < 1 else ">="))
report("scaled-to-ceiling covering is INVALID, as it must be "
       "(a 16-point packing exists at the ceiling)", scaled >= 1)

# ---------------------------------------------------------------- F. counting
print("\nF. piece count, after de-duplication")
canon = set()
for f in faces:
    canon.add(tuple(sorted(f)))
report("15 pieces, all distinct as vertex sets", len(canon) == 15,
       "found %d distinct" % len(canon))
report("15 < 16 (pigeonhole has a pigeon to spare)", len(faces) < 16)

# ---------------------------------------------------------------- G. union area
print("\nG. union area computed a second way (inclusion of pairwise overlaps)")
tot2 = sum(abs(shoelace2(f)) for f in faces)
ov2 = sum(convex_intersection_area2(ccw[i], ccw[j])
          for i, j in itertools.combinations(range(len(ccw)), 2))
print("   2*sum(areas)      = %s" % tot2)
print("   2*sum(pair ovlps) = %s" % ov2)
print("   2*area(T_a)       = %s" % (a * a))
report("union area == area(T_a) with zero total overlap",
       ov2 == 0 and tot2 == a * a)

print("\n" + "=" * 78)
print("ADVERSARIAL PASS: %s" % ("NO BREAK FOUND" if fails == 0
                                else "%d ATTACK(S) SUCCEEDED" % fails))
print("=" * 78)
raise SystemExit(1 if fails else 0)
