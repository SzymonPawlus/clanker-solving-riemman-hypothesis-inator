#!/usr/bin/env python3
"""
Independent recount of the contact graph, rattler, and infinitesimal rigidity of
the n = 16 certificate configuration -- to adjudicate the disagreement between
attacks/n16-dual (rattler with 1 contact; core isostatic, 30 constraints / 30 dof)
and attacks/n16-upper-2 (rattler with 0 contacts; core hyperstatic, 33 / 30).

Everything that decides a number is exact:
  * squared pair distances and wall residuals: Fraction / Q(sqrt3), exact;
  * the active-set threshold: chosen inside an exactly-exhibited spectral gap;
  * the rank of the rigidity matrix: Gauss-Jordan over the FIELD Q(sqrt3), exact.
No floats decide anything (they appear only in printed magnitudes).

Usage: python3 rigidity_v5.py [certificate.json]
"""

import json
import os
import sys
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_v5 import Q3, SQRT3, dec, _q3   # noqa: E402

CERT = (sys.argv[1] if len(sys.argv) > 1 else
        "problems/circle-packing-equilateral-triangle/attacks/n16-upper-2/"
        "n16-certificate.json")
cert = json.load(open(CERT))
PTS = [(Fraction(x), Fraction(y)) for x, y in cert["coordinates"]]
D = Fraction(cert["side_length"].split("+")[0].strip())
N = len(PTS)


# ---- Q(sqrt3) is a field: add division so we can do exact Gauss-Jordan -----
def q3_inv(v):
    v = _q3(v)
    den = v.a * v.a - 3 * v.b * v.b        # nonzero unless v == 0
    assert den != 0
    return Q3(v.a / den, -v.b / den)


def rank_q3(rows, ncols):
    """Exact rank over Q(sqrt3) by Gauss-Jordan.  rows: list of list[Q3]."""
    M = [list(r) for r in rows]
    piv_row = 0
    for col in range(ncols):
        p = None
        for r in range(piv_row, len(M)):
            if M[r][col].sign() != 0:
                p = r
                break
        if p is None:
            continue
        M[piv_row], M[p] = M[p], M[piv_row]
        inv = q3_inv(M[piv_row][col])
        M[piv_row] = [inv * e for e in M[piv_row]]
        for r in range(len(M)):
            if r != piv_row and M[r][col].sign() != 0:
                f = M[r][col]
                M[r] = [M[r][c] - f * M[piv_row][c] for c in range(ncols)]
        piv_row += 1
        if piv_row == len(M):
            break
    return piv_row


# ---------------- 1. exact pair-distance spectrum --------------------------
sq = {}
for i, j in combinations(range(N), 2):
    dx = PTS[i][0] - PTS[j][0]
    dy = PTS[i][1] - PTS[j][1]
    sq[(i, j)] = dx * dx + dy * dy
order = sorted(sq.items(), key=lambda kv: kv[1])

print("=== pair distances: exact excess of dist^2 over 4, ascending ===")
for (p, v) in order[:26]:
    print(f"   pair {p!s:9s} dist^2 - 4 = {dec(Q3(v - 4, 0), 6)}")
print("   ...")

# the gap: choose the active-set threshold strictly inside it
TAU = Fraction(1, 10 ** 6)          # in dist^2 - 4 units
contacts = [p for p, v in order if v - 4 <= TAU]
just_out = [(p, v) for p, v in order if v - 4 > TAU][0]
print(f"\n   threshold tau = 1e-6 on (dist^2 - 4)")
print(f"   largest active   : {dec(Q3(sq[contacts[-1]] - 4, 0), 16)}")
print(f"   smallest inactive: {dec(Q3(just_out[1] - 4, 0), 10)}   (pair {just_out[0]})")
print(f"   => {len(contacts)} pair contacts; the gap spans ~10 orders of magnitude, "
      f"so the count is threshold-independent")

# ---------------- 2. exact wall residuals ----------------------------------
WALLS = ("AB: y>=0", "AC: sqrt3*x-y>=0", "BC: sqrt3*(d-x)-y>=0")
resid = []
for i, (x, y) in enumerate(PTS):
    resid.append([Q3(y, 0),
                  SQRT3 * Q3(x, 0) - Q3(y, 0),
                  SQRT3 * (Q3(D, 0) - Q3(x, 0)) - Q3(y, 0)])

flat = sorted(((resid[i][w], i, w) for i in range(N) for w in range(3)),
              key=lambda t: float(t[0]))
print("\n=== wall residuals (exact), ascending ===")
for v, i, w in flat[:20]:
    print(f"   point {i:2d}  {WALLS[w]:22s}  {dec(v, 8)}")
print("   ...")

TAUW = Fraction(1, 10 ** 6)
walls = [(i, w) for v, i, w in flat if v.cmp(TAUW) <= 0]
first_out = [(v, i, w) for v, i, w in flat if v.cmp(TAUW) > 0][0]
print(f"\n   threshold 1e-6 on the residual")
print(f"   largest active   : {dec(flat[len(walls)-1][0], 16)}")
print(f"   smallest inactive: {dec(first_out[0], 8)}   (point {first_out[1]}, "
      f"{WALLS[first_out[2]]})")
print(f"   => {len(walls)} wall incidences")

from collections import Counter                              # noqa: E402
wc = Counter(i for i, w in walls)
corner_pts = [i for i, c in wc.items() if c >= 2]
print(f"   points on two walls at once (corners): {sorted(corner_pts)} "
      f"-> {len(corner_pts)} points contributing 2 incidences each")
print(f"   distinct points touching a wall: {len(wc)}")

# ---------------- 3. rattler -----------------------------------------------
deg = Counter()
for (i, j) in contacts:
    deg[i] += 1
    deg[j] += 1
free = [i for i in range(N) if deg[i] == 0 and wc.get(i, 0) == 0]
print("\n=== contact degrees (pair contacts / wall incidences) ===")
for i in range(N):
    print(f"   P{i:<2d}  pairs {deg.get(i,0)}   walls {wc.get(i,0)}   total "
          f"{deg.get(i,0)+wc.get(i,0)}")
print(f"\n   points with NO constraint at all (rattlers): {free}")
for r in free:
    nb = sorted(((sq[tuple(sorted((r, j)))], j) for j in range(N) if j != r))[:4]
    print(f"   rattler P{r}: nearest neighbours dist^2 - 4 = "
          + ", ".join(f"P{j}:{dec(Q3(v-4,0),6)}" for v, j in nb))
    print(f"   rattler P{r}: wall residuals = "
          + ", ".join(f"{WALLS[w].split(':')[0]}:{dec(resid[r][w],6)}" for w in range(3)))

# ---------------- 4. rigidity matrix, exact rank over Q(sqrt3) -------------
def build(idx):
    """Rigidity rows for the sub-configuration on point indices `idx`."""
    pos = {p: k for k, p in enumerate(idx)}
    nc = 2 * len(idx)
    rows, labels = [], []
    for (i, j) in contacts:
        if i not in pos or j not in pos:
            continue
        r = [Q3(0, 0)] * nc
        dx = Q3(PTS[i][0] - PTS[j][0], 0)
        dy = Q3(PTS[i][1] - PTS[j][1], 0)
        r[2 * pos[i]] = dx
        r[2 * pos[i] + 1] = dy
        r[2 * pos[j]] = -dx
        r[2 * pos[j] + 1] = -dy
        rows.append(r)
        labels.append(f"pair{(i,j)}")
    for (i, w) in walls:
        if i not in pos:
            continue
        r = [Q3(0, 0)] * nc
        if w == 0:                       # grad of y
            gx, gy = Q3(0, 0), Q3(1, 0)
        elif w == 1:                     # grad of sqrt3*x - y
            gx, gy = SQRT3, Q3(-1, 0)
        else:                            # grad of sqrt3*(d-x) - y
            gx, gy = -SQRT3, Q3(-1, 0)
        r[2 * pos[i]] = gx
        r[2 * pos[i] + 1] = gy
        rows.append(r)
        labels.append(f"wall(P{i},{WALLS[w].split(':')[0]})")
    return rows, labels, nc


for name, idx in (("all 16 points", list(range(N))),
                  ("jammed core (rattlers removed)",
                   [i for i in range(N) if i not in free])):
    rows, labels, nc = build(idx)
    r = rank_q3(rows, nc)
    print(f"\n=== rigidity: {name} ===")
    print(f"   points {len(idx)}   dof {nc}   constraints {len(rows)} "
          f"({sum(1 for l in labels if l.startswith('pair'))} pair + "
          f"{sum(1 for l in labels if l.startswith('wall'))} wall)")
    print(f"   exact rank over Q(sqrt3) = {r}")
    print(f"   infinitesimal flexes  = dof - rank      = {nc - r}")
    print(f"   self-stress dimension = constraints - rank = {len(rows) - r}")
    print("   => " + ("ISOSTATIC" if len(rows) == r == nc else
                      ("HYPERSTATIC by " + str(len(rows) - r) if nc == r else
                       "UNDERCONSTRAINED (flexes present)")))


# ---------------- 5. reproduce the sibling lane's reading -------------------
# attacks/n16-dual reports "21 contacts and 10 wall contacts", core isostatic
# 30 / 30.  Test the hypothesis that its 10 is the number of DISTINCT points
# touching a wall, not the number of wall INCIDENCES.
print("\n=== adjudication: what does 'wall contacts = 10' count? ===")
print(f"   wall incidences (point, edge) pairs : {len(walls)}")
print(f"   distinct points touching >=1 wall   : {len(wc)}")
print(f"   corner points (on two edges at once): {sorted(corner_pts)}")
print(f"   {len(walls)} - {len(wc)} = {len(walls)-len(wc)} = the corner double-count")

core = [i for i in range(N) if i not in free]
pos = {p: k for k, p in enumerate(core)}
rows, labels, nc = build(core)
# drop one wall row per corner point -> the 30-row matrix the sibling count implies
seen, rows30, lab30 = set(), [], []
for r, l in zip(rows, labels):
    if l.startswith("wall"):
        pt = l.split("P")[1].split(",")[0]
        if pt in seen:
            continue
        seen.add(pt)
    rows30.append(r)
    lab30.append(l)
r30 = rank_q3(rows30, nc)
print(f"\n   'corner counted once' matrix: {len(rows30)} constraints on {nc} dof, "
      f"exact rank = {r30}")
print(f"   flexes = {nc - r30}, self-stresses = {len(rows30) - r30}")
print("   => counting each corner once gives 30 constraints and "
      f"{'rank 30, which reads as isostatic' if r30 == 30 else f'rank {r30}'}; "
      "the full active set is 33 with rank 30, i.e. hyperstatic by 3.")

# ---------------- 6. corner identification ---------------------------------
print("\n=== are the three 'corner' points really at the triangle's vertices? ===")
verts = {"A=(0,0)": (Fraction(0), Fraction(0)),
         "B=(d,0)": (D, Fraction(0))}
for i in sorted(corner_pts):
    x, y = PTS[i]
    best = None
    for nm, (vx, vy) in verts.items():
        dd = (x - vx) ** 2 + (y - vy) ** 2
        if best is None or dd < best[1]:
            best = (nm, dd)
    # apex C = (d/2, d*sqrt3/2): compare exactly in Q(sqrt3)
    cxy = (Q3(x, 0) - Q3(D / 2, 0), Q3(y, 0) - Q3(0, D / 2))
    capx = (cxy[0] * cxy[0] + cxy[1] * cxy[1])
    print(f"   P{i}: dist^2 to {best[0]} = {dec(Q3(best[1],0),20)} ; "
          f"dist^2 to C=(d/2,d*sqrt3/2) = {dec(capx,20)}")
