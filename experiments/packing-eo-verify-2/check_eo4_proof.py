"""The eo-subinteger-relaxation §5 proof of Erdos-Oler at k=4, checked from the statement.

Proposition: 9 points at mutual distance >= 1 do not fit in a closed equilateral triangle of
side a < 3.   Cover T_a by three corner triangles of side t = a/3 and the central hexagon H.
"""
from fractions import Fraction as F
import math

FAIL = []
def ck(n, c, e=""):
    if not c: FAIL.append(n)
    print(f"  [{'PASS' if c else 'FAIL'}] {n}{(' :: '+e) if e else ''}")

print("=" * 78)
print("Lemma D, re-derived: 6 points at mutual distance >= 1 need circumradius >= 1")
print("=" * 78)
print("  Sort m points by polar angle about O; some gap Delta <= 2pi/m, so cos Delta >= c.")
print("  |PiPj|^2 = ri^2 + rj^2 - 2 ri rj cos Delta <= ri^2 + rj^2 - 2c ri rj.")
print("  max of x^2+y^2-2cxy over [0,rho]^2 is rho^2 * max(1, 2-2c)  (corner (rho,0) or (rho,rho)).")
print("  m=6: c = 1/2, 2-2c = 1, so |PiPj|^2 <= rho^2.  rho < 1 => some pair is < 1 apart.")
# check the max claim numerically-exactly on a grid, for each m
bad = []
for m in range(2, 7):
    c = math.cos(2*math.pi/m)
    claim = max(1.0, 2 - 2*c)
    best = 0.0
    N = 400
    for i in range(N+1):
        for j in range(N+1):
            x, y = i/N, j/N
            v = x*x + y*y - 2*c*x*y
            best = max(best, v)
    if best > claim + 1e-12: bad.append((m, best, claim))
ck("max_{[0,1]^2} (x^2+y^2-2cxy) = max(1, 2-2c) for m = 2..6", not bad, str(bad))
ck("m=6 gives c=1/2 and 2-2c=1, so the bound is rho^2 exactly",
   abs(math.cos(math.pi/3) - 0.5) < 1e-15)
ck("equivalent form 1 <= 2 rho sin(pi/m): at m=6, 2 sin(pi/6) = 1, so rho >= 1",
   abs(2*math.sin(math.pi/6) - 1) < 1e-15)
print("  A point AT O is covered too: then |PiPj|^2 = rj^2 <= rho^2 < 1 directly.")
print("  => cap(circumradius < 1) <= 5.  CONFIRMED, and it uses no d(n) from any table.")

print()
print("=" * 78)
print("The k=4 cover: T_a = three corner triangles of side t=a/3, plus a regular hexagon")
print("=" * 78)
print("  (i) the cover is complete: a point outside every Delta_V(t) has u_V > t for all V,")
print("      which is the definition of H.")
ck("(ii) corner cuts are disjoint: need t + t <= a, i.e. 2(a/3) <= a", True, "true for a > 0")
print("  (iii) H is a regular hexagon of side t:")
for a_s in ("2", "5/2", "29/10", "299/100", "2999/1000"):
    a = F(a_s); t = a/3
    cut_edge = t                       # each corner cut contributes an edge of length t
    remnant = a - 2*t                  # what is left of each original side
    ok = (cut_edge == remnant == t) and t < 1
    print(f"    a={str(a_s):>9}  t=a/3={float(t):.6f}  cut edge={float(cut_edge):.6f}  "
          f"remnant={float(remnant):.6f}  regular? {cut_edge==remnant}  t<1? {t<1}")
    if not ok: FAIL.append(f"hexagon at a={a_s}")
ck("H is a regular hexagon of side t = a/3 < 1 for every a < 3", not [f for f in FAIL if "hexagon" in f])
print("  (iv) circumradius of a regular hexagon of side t is exactly t  (six equilateral triangles)")
print("  (v) corner triangle has diameter t < 1, so holds <= 1 point")
print()
print("  TOTAL:  3 * 1  +  5  =  8  <  9.")
ck("3*1 + 5 = 8 < 9", 3*1 + 5 == 8 < 9)
print()
print("  Boundary behaviour at a = 3 (the proof must say nothing there, since 10 points DO fit):")
print("    t = 1: corner triangles have side 1 (cap 3 each), H has circumradius 1 (cap 6),")
print("    total 3*3 + 6 = 15 -- vacuous, as it must be.")
ck("at a=3 the same cover gives 15, i.e. says nothing", 3*3 + 6 == 15)
print()
print("  CIRCULARITY CHECK: the two capacities used are (diameter < 1 => 1) and")
print("  (circumradius < 1 => 5).  Both are geometric.  Neither reads d(n), s(n) or a_n.")
print("  The proof is therefore NOT circular with respect to Erdos-Oler at any k.")
print()
print("FAILURES:", FAIL if FAIL else "none")
raise SystemExit(1 if FAIL else 0)
