"""Lemma L, repaired: the STRICT-diameter version, verified exactly.

The bug (found by the manager, 2026-08-22): eo-covering-construct §2 states
Lemma L for  a <= p*sqrt3/2  with cells of diameter <= 1, and then pigeonholes
"at most one point per cell".  At a = p*sqrt3/2 EVERY cell has diameter exactly
1 (verified below), and this problem's RULES.md §2 fixes separation as
NON-strict, so a closed set of diameter exactly 1 can contain two points at
distance exactly 1.  The pigeonhole does not follow as stated.

The repair is a homothety, and it costs nothing: verify diam <= 1 at
a0 = p*sqrt3/2, then for any a < a0 the map x -> (a/a0) x carries the partition
of T_{a0} to a partition of T_a whose cells have diameter <= a/a0 < 1.
"""
from fractions import Fraction as F
from exact import q3, Q3, verify, diam2, shoelace2, triangle
from lattice import build, lattice_sites

def check_p(p, verbose=True):
    a0 = Q3(0, F(p, 2))                    # p*sqrt3/2
    cells = build(p, a0)
    assert len(cells) == p*(p+1)//2 and all(len(c) >= 3 for c in cells)
    ok, worst = verify(cells, a0, verbose=False, report=True)
    # ok is False only because of the STRICT test; check the non-strict one here
    nonstrict = all(diam2(c) <= q3(1) for c in cells)
    attained  = any(diam2(c) == q3(1) for c in cells)
    allone    = all(diam2(c) == q3(1) for c in cells)
    tot = q3(0)
    for c in cells:
        s = shoelace2(c)
        if s.sign() < 0: s = -s
        tot = tot + s
    areaok = (tot == shoelace2(triangle(a0)))
    if verbose:
        print("p=%2d  cells=%3d  a0=%.9f  max diam^2=%s  diam<=1:%s  =1 attained:%s  "
              "ALL cells diam=1:%s  area exact:%s"
              % (p, len(cells), a0.approx(), worst, nonstrict, attained, allone, areaok))
    return nonstrict and areaok, allone

def strict_at(p, a):
    """exact strict check of the scaled partition of T_a, a < p*sqrt3/2, a rational"""
    a = q3(a)
    a0 = Q3(0, F(p, 2))
    assert a < a0
    lam = a / a0
    sites = [(u*lam, v*lam) for (u, v) in lattice_sites(p, a0)]
    from exact import voronoi_cells
    cells = voronoi_cells(sites, a)
    ok, worst = verify(cells, a, verbose=False)
    return ok, worst

if __name__ == "__main__":
    print("== Lemma L at the threshold a0 = p*sqrt3/2 (non-strict), p = 2..8 ==")
    allone = {}
    for p in range(2, 9):
        good, one = check_p(p)
        assert good, "Lemma L failed at p=%d" % p
        allone[p] = one
    print()
    print("Every cell of every one of these partitions has diameter EXACTLY 1:",
          all(allone.values()))
    print("=> the non-strict statement cannot be pigeonholed directly.  Repair by homothety:")
    print()
    for p, a in ((5, F(433, 100)), (5, F(43301, 10000)), (7, F(606, 100))):
        ok, w = strict_at(p, a)
        print("p=%d  a=%s (%.6f < %.6f)  %d cells  max diam^2 = %.15f  STRICT PASS = %s"
              % (p, a, float(a), (Q3(0, F(p, 2))).approx(), p*(p+1)//2, w.approx(), ok))
        assert ok
    print()
    print("Conclusion: a_{Delta(p)+1} >= p*sqrt3/2.  For p=5: a_16 >= 5*sqrt3/2 = %.9f"
          % Q3(0, F(5, 2)).approx())
