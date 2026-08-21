"""CLAIM 1 -- the partition lemma of attacks/eo-exhaustion/ Sec. 3.

    Lemma. P convex, partitioned into convex pieces P_1..P_m, I the total length
    of the internal cuts.  Then  sum_i B(P_i) = B(P) + I + (m-1),
    where B(R) = (2/sqrt3)A(R) + M(R)/2 + 1 is Oler's bound applied to a region.

Everything is exact (Surd).  Each test computes I *independently* from the
construction, never by inverting the identity being tested.
"""

from fractions import Fraction as F
from surd import Surd, oler_bound, perimeter, shoelace, tri, edge_len
from shapes import cells

REPORT = []


def record(name, ok, detail=""):
    REPORT.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (("   " + detail) if detail else ""))
    return ok


def check_identity(name, P, pieces, I, expect_holds=True):
    """P: outer polygon.  pieces: list of polygons.  I: Surd, independent cut length."""
    m = len(pieces)
    lhs = Surd(0)
    for p in pieces:
        lhs = lhs + oler_bound(p)
    rhs = oler_bound(P) + I + Surd(m - 1)
    # area additivity and the perimeter identity, separately
    area_ok = sum((shoelace(p) for p in pieces), F(0)) == shoelace(P)
    per_lhs = Surd(0)
    for p in pieces:
        per_lhs = per_lhs + perimeter(p)
    per_ok = per_lhs == perimeter(P) + I * 2
    ok = (lhs == rhs)
    detail = f"m={m}  sum(B)-B(P) = {lhs - oler_bound(P)}   predicted {I + Surd(m-1)}"
    if not area_ok:
        detail += "  [AREA ADDITIVITY FAILS]"
    if not per_ok:
        detail += "  [PERIMETER IDENTITY FAILS]"
    return record(name, ok == expect_holds, detail)


# ---------------------------------------------------------------------------
# 1. m = 1  (trivial edge case)
# ---------------------------------------------------------------------------
a = F(6)
check_identity("m=1, no cut", tri(a), [tri(a)], Surd(0))

# ---------------------------------------------------------------------------
# 2. horizontal strips (the case eo-exhaustion Sec.3 quotes: k=7 strips, a=6,
#    loss 24)
# ---------------------------------------------------------------------------
def strips(a, k):
    """T_a cut by k-1 lines parallel to the base (v = j*a/k)."""
    a = F(a)
    pieces = []
    for j in range(k):
        lo, hi = F(j) * a / k, F(j + 1) * a / k
        if j == k - 1:
            pieces.append([(F(0), lo), (a - lo, lo), (F(0), a)])
        else:
            pieces.append([(F(0), lo), (a - lo, lo), (a - hi, hi), (F(0), hi)])
    I = Surd(sum((a - F(j) * a / k for j in range(1, k)), F(0)))
    return pieces, I


for k in (2, 3, 7):
    pieces, I = strips(6, k)
    check_identity(f"T_6 into {k} horizontal strips", tri(6), pieces, I)

pieces, I = strips(6, 7)
loss = sum((oler_bound(p) for p in pieces), Surd(0)) - oler_bound(tri(6))
record("eo-exhaustion Sec.3 arithmetic: 7 strips at a=6 lose exactly 24",
       loss == Surd(24), f"loss = {loss}")

# ---------------------------------------------------------------------------
# 3. the uniform m^2-cell subdivision
# ---------------------------------------------------------------------------


for m in (2, 3, 4, 5):
    pcs, I = cells(6, m)
    check_identity(f"T_6 into {m}^2 = {m*m} cells", tri(6), pcs, I)
    record(f"cell count is exactly {m}^2", len(pcs) == m * m, f"got {len(pcs)}")

# ---------------------------------------------------------------------------
# 4. pieces meeting at a single point (three pieces around the centroid)
# ---------------------------------------------------------------------------
a = F(6)
g = (a / 3, a / 3)
Tv = tri(a)
pieces = [[Tv[0], Tv[1], g], [Tv[1], Tv[2], g], [Tv[2], Tv[0], g]]
I = edge_len(Tv[0], g) + edge_len(Tv[1], g) + edge_len(Tv[2], g)
check_identity("three pieces meeting at the centroid", Tv, pieces, I)

# a four-piece fan around an interior point of a quadrilateral
Q = [(F(0), F(0)), (F(4), F(0)), (F(4), F(4)), (F(0), F(4))]
c = (F(1), F(2))
pieces = [[Q[i], Q[(i + 1) % 4], c] for i in range(4)]
I = Surd(0)
for q in Q:
    I = I + edge_len(q, c)
check_identity("quadrilateral fanned from an interior point", Q, pieces, I)

# ---------------------------------------------------------------------------
# 5. a T-junction: a cut that is an edge of one piece and only part of an edge
#    of another (three pieces meeting along a segment)
# ---------------------------------------------------------------------------
Q = [(F(0), F(0)), (F(4), F(0)), (F(4), F(4)), (F(0), F(4))]
P1 = [(F(0), F(0)), (F(4), F(0)), (F(4), F(2)), (F(0), F(2))]
P2 = [(F(0), F(2)), (F(2), F(2)), (F(2), F(4)), (F(0), F(4))]
P3 = [(F(2), F(2)), (F(4), F(2)), (F(4), F(4)), (F(2), F(4))]
I = edge_len((F(0), F(2)), (F(4), F(2))) + edge_len((F(2), F(2)), (F(2), F(4)))
check_identity("T-junction (three pieces, one cut split between two)", Q, [P1, P2, P3], I)

# ---------------------------------------------------------------------------
# 6. EDGE CASE: a lower-dimensional piece.  Adding the cut segment itself as a
#    'piece' keeps the union and the interiors disjoint, but breaks the identity.
# ---------------------------------------------------------------------------
Q = [(F(0), F(0)), (F(4), F(0)), (F(4), F(4)), (F(0), F(4))]
A = [(F(0), F(0)), (F(4), F(0)), (F(4), F(2)), (F(0), F(2))]
B = [(F(0), F(2)), (F(4), F(2)), (F(4), F(4)), (F(0), F(4))]
seg = [(F(0), F(2)), (F(4), F(2))]     # degenerate convex 'piece'
I = edge_len((F(0), F(2)), (F(4), F(2)))
lhs = oler_bound(A) + oler_bound(B) + (edge_len(seg[0], seg[1]) + Surd(1))
rhs = oler_bound(Q) + I + Surd(3 - 1)
record("EDGE CASE: identity FAILS when a piece is a segment (as it must)",
       lhs != rhs, f"lhs-rhs = {lhs - rhs}  (excess {lhs - rhs})")

# ---------------------------------------------------------------------------
# 7. EDGE CASE: counting a boundary-coincident segment inside I breaks it
# ---------------------------------------------------------------------------
pieces, Igood = strips(6, 2)
Ibad = Igood + edge_len((F(0), F(0)), (F(6), F(0)))   # add a piece of dP to I
check_identity("EDGE CASE: identity FAILS if a boundary segment is counted in I",
               tri(6), pieces, Ibad, expect_holds=False)

# ---------------------------------------------------------------------------
# 8. The identity's *corollary* -- 'every partition-and-count refinement of Oler
#    is dead' -- tested against the repo's own k=3 argument.
#    The 4-cell subdivision of T_a, a<2, gives capacity 4 by diameter, while Oler
#    on the whole triangle gives up to 6.  Summing TRUE capacities beats Oler;
#    summing OLER BOUNDS does not.  Both computed here.
# ---------------------------------------------------------------------------
for a in (F(19, 10), F(199, 100), F(1999, 1000)):
    pcs, I = cells(a, 2)
    sum_oler_pieces = sum((oler_bound(p) for p in pcs), Surd(0))
    oler_whole = oler_bound(tri(a))
    true_capacity = 4          # each cell has diameter a/2 < 1
    ok = (sum_oler_pieces > oler_whole) and (true_capacity < float(oler_whole))
    record(f"a={float(a):.4f}: sum of Oler-per-cell = {float(sum_oler_pieces):.4f} > "
           f"Oler(T) = {float(oler_whole):.4f} > true 4-cell capacity 4", ok)

print()
bad = [r for r in REPORT if not r[1]]
print(f"{len(REPORT)-len(bad)}/{len(REPORT)} checks passed")
raise SystemExit(1 if bad else 0)
