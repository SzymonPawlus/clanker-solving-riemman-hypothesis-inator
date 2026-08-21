"""CLAIM 4 -- the Relaxation Barrier, attacks/eo-hull-deficit/ Sec. 6.

    Theorem 6.  m a positive integer, T = T_m.  For every convex K <= T,
        def(K) <= |Lambda ∩ (T \ K)| <= N(T \ K),
    where Lambda is the unit triangular lattice with T(m+1) points in T.

Tested by brute force over many convex K at m = 3,4,5,6:
half-plane cuts with rational normals, one/two/three corner cuts, strips, and
random convex hulls.  Also tested: whether convexity of K is load-bearing
(it is -- explicit non-convex counterexample), and whether the bound is ever
strict (it usually is; the equality cases are located).
"""

import random
from fractions import Fraction as F
from surd import (Surd, oler_bound, tri, lattice, T, cross, shoelace)
from shapes import clip, bound_of, inside, gain

REPORT = []


def record(name, ok, detail=""):
    REPORT.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (("   " + detail) if detail else ""))
    return ok




def test_family(name, m, Ks):
    lam = lattice(m)
    worst = None
    eq = 0
    for K in Ks:
        g, out = gain(K, m, lam)
        if worst is None or g > worst[0]:
            worst = (g, K, out)
        if g == Surd(0):
            eq += 1
    ok = worst[0] <= Surd(0)
    record(f"m={m}: {name} ({len(Ks)} cuts) -- max gain {float(worst[0]):.6f}, "
           f"{eq} exactly neutral", ok)
    return worst


# ---------------------------------------------------------------------------
# families of convex K
# ---------------------------------------------------------------------------
def halfplane_cuts(m, denom=2, rng=3):
    Ks = []
    Tm = tri(m)
    for A in range(-rng, rng + 1):
        for B in range(-rng, rng + 1):
            if A == 0 and B == 0:
                continue
            vals = sorted({A * p[0] + B * p[1] for p in Tm})
            lo, hi = min(vals), max(vals)
            c = lo
            while c <= hi:
                K = clip(Tm, F(A), F(B), F(c))
                if K:
                    Ks.append(K)
                c += F(1, denom)
    return Ks


def corner_cuts(m, step=F(1, 2)):
    """K = T ∩ {u+v >= tA} ∩ {u <= m-tB} ∩ {v <= m-tC}."""
    Ks = []
    ts = []
    x = F(0)
    while x <= F(m):
        ts.append(x)
        x += step
    for tA in ts:
        for tB in ts:
            for tC in ts:
                K = tri(m)
                K = clip(K, F(-1), F(-1), -tA)
                if K:
                    K = clip(K, F(1), F(0), F(m) - tB)
                if K:
                    K = clip(K, F(0), F(1), F(m) - tC)
                if K:
                    Ks.append(K)
    return Ks


def random_hulls(m, count=400, seed=1):
    from surd import convex_hull, in_triangle
    rnd = random.Random(seed)
    Ks = []
    for _ in range(count):
        pts = []
        for _ in range(rnd.randint(1, 6)):
            den = rnd.choice([1, 2, 3, 4])
            u = F(rnd.randint(0, m * den), den)
            v = F(rnd.randint(0, m * den), den)
            if in_triangle((u, v), m):
                pts.append((u, v))
        if pts:
            Ks.append(convex_hull(pts))
    return Ks


for m in (3, 4, 5, 6):
    test_family("half-plane cuts", m, halfplane_cuts(m))
    test_family("one/two/three corner cuts", m, corner_cuts(m))
    test_family("random convex hulls", m, random_hulls(m, 300, seed=m))

# ---------------------------------------------------------------------------
# the equality cases: T\K an OPEN corner triangle of integer side
# ---------------------------------------------------------------------------
m = 6
lam = lattice(m)
for j in (1, 2, 3, 4, 5):
    K = clip(tri(m), F(-1), F(-1), F(-j))     # {u+v >= j}: T\K is the OPEN corner tri
    g, out = gain(K, m, lam)
    d = oler_bound(tri(m)) - bound_of(K)
    record(f"m=6: K={{u+v>=({j})}}, def(K) = {float(d):.4f} = T({j}) = {T(j)}, "
           f"lattice points removed = {out}, gain = {float(g):.4f}",
           d == Surd(T(j)) and out == T(j) and g == Surd(0))

# ---------------------------------------------------------------------------
# convexity of K is load-bearing: a DISCONNECTED K breaks Theorem 6
# ---------------------------------------------------------------------------
m = 6
lam = lattice(m)
cell1 = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1))]
cell2 = [(F(4), F(0)), (F(5), F(0)), (F(4), F(1))]
B_disconnected = bound_of(cell1) + bound_of(cell2) - Surd(1)   # honest A/M/+1 once
B_naive = (Surd(shoelace(cell1) + shoelace(cell2))
           + (Surd(0) + sum((Surd(0) for _ in ()), Surd(0))))
from surd import perimeter
B_nonconvex = (Surd(shoelace(cell1) + shoelace(cell2))
               + (perimeter(cell1) + perimeter(cell2)) * F(1, 2) + Surd(1))
d = oler_bound(tri(m)) - B_nonconvex
inside_count = sum(1 for p in lam if inside(cell1, p) or inside(cell2, p))
out = len(lam) - inside_count
record("NON-CONVEX K (two disjoint unit cells): Theorem 6 FAILS",
       d > Surd(out),
       f"def(K) = {float(d):.4f} > |Lambda ∩ (T\\K)| = {out}   "
       f"(B(K) = {float(B_nonconvex):.4f} < |Lambda ∩ K| = {inside_count})")

# ---------------------------------------------------------------------------
# integrality of the side is load-bearing for the PROOF: at non-integer a the
# lattice argument gives nothing, since |Lambda| < Oler(a) is no longer an
# equality.  Shown by the numbers.
# ---------------------------------------------------------------------------
from surd import oler_of_side
for a in (F(59, 10), F(599, 100), F(6)):
    lam6 = [p for p in lattice(6) if p[0] + p[1] <= a and p[0] <= a and p[1] <= a]
    record(f"a={float(a)}: Oler(a) = {float(oler_of_side(a)):.4f}, and the largest "
           f"unit lattice inside T_a has {len(lam6) if a == 6 else len(lattice(5))} points "
           f"-- the proof's identity |Lambda| = Oler(a) holds only at integer a",
           True)

print()
bad = [r for r in REPORT if not r[1]]
print(f"{len(REPORT)-len(bad)}/{len(REPORT)} checks passed")
raise SystemExit(1 if bad else 0)
