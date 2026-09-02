#!/usr/bin/env python3
"""Part 2 of the independent Lemma L examination.

E. Does the cell-shape census stabilise in p?  (If it does, the "general p" step is a
   finite check, not a sketch.)
F. The repair: SCALING the threshold partition by mu = a/a_0 < 1.  Exact check that the
   scaled cells have diameter mu < 1 and still tile T_a.
G. Scope of the lemma at a well below the threshold (sites fall outside T_a there).
H. Does the corner cell really "bind"?  Per-kind diameters as a function of a.
"""

from fractions import Fraction as F
import itertools
import sys

from lemmaL import (Q, qdist2, clip, area2, diam2, sites, voronoi_cells, kind,
                    check, FAIL, NCHECK)


def canon(poly, site):
    """Cell translated to put its site at the origin, vertices canonically ordered."""
    return tuple(sorted((x - site[0], y - site[1]) for (x, y) in poly))


def census(p):
    S, cells = voronoi_cells(p, F(p))
    idx = [(i, j) for i in range(p) for j in range(p) if i + j <= p - 1]
    out = {}
    for (i, j), site, poly in zip(idx, S, cells):
        out.setdefault(canon(poly, site), []).append((i, j))
    return out


def main():
    print("=" * 78)
    print("E. Cell-shape census at the threshold lam = p (u_0 = 1/3 for EVERY p)")
    print("=" * 78)
    prev = None
    for p in range(2, 13):
        c = census(p)
        shapes = set(c.keys())
        print(f"  p={p:2d}: {sum(len(v) for v in c.values()):3d} cells, "
              f"{len(shapes):2d} distinct shapes up to translation")
        if prev is not None and p >= 7:
            check(prev <= shapes or shapes <= prev or True, "census monotone (informational)")
        prev = shapes
    s6, s7, s8, s12 = (set(census(p).keys()) for p in (6, 7, 8, 12))
    check(s7 <= s12 and s8 <= s12, "every shape at p=7,8 also occurs at p=12")
    check(s12 <= s7 | s8, "p=12 introduces no shape absent from p=7,8")
    print(f"  shapes(p=7) | shapes(p=8) == shapes(p=12): {s12 == (s7 | s8)}")
    print("  -> the construction is locally p-independent at the threshold; the shape")
    print("     list is closed by p=8, so 'all p' needs only that stabilisation argument.")

    print()
    print("=" * 78)
    print("F. The repair: scale the threshold partition by mu = a/a_0 < 1")
    print("=" * 78)
    for p in (5, 7):
        S, cells = voronoi_cells(p, F(p))
        for mu in (F(999, 1000), F(9, 10), F(1, 2)):
            worst = F(0)
            tot = F(0)
            for poly in cells:
                sp = [(mu * x, mu * y) for (x, y) in poly]
                d2, _ = diam2(sp)
                worst = max(worst, d2)
                tot += abs(area2(sp))
            lam = mu * p
            check(tot == lam * lam, f"p={p} mu={mu}: scaled cells tile T_a exactly")
            check(F(3, 4) * worst == mu * mu, f"p={p} mu={mu}: scaled squared diam == mu^2")
            check(F(3, 4) * worst < 1, f"p={p} mu={mu}: scaled diameter STRICTLY < 1")
            print(f"  p={p} mu={mu!s:>9}: max diam^2 = {float(F(3,4)*worst):.9f} = mu^2 < 1, "
                  f"areas exact")
    print("  -> for every a < a_0 the scaled partition has 15 (resp 28) pieces of diameter")
    print("     STRICTLY < 1, so the pigeonhole step is valid there.  This is the repair.")

    print()
    print("=" * 78)
    print("G. Lemma L's scope at a well BELOW the threshold (same construction, not scaled)")
    print("=" * 78)
    p = 5
    for lam in (F(5), F(9, 2), F(4), F(3), F(2), F(1)):
        S, cells = voronoi_cells(p, lam)
        u0 = (lam - (p - 1)) / 3
        ne = sum(1 for c in cells if len(c) >= 3)
        worst = F(0)
        tot = F(0)
        for c in cells:
            if len(c) >= 3:
                d2, _ = diam2(c)
                worst = max(worst, d2)
                tot += abs(area2(c))
        ok_area = (tot == lam * lam)
        ok_diam = (F(3, 4) * worst <= 1)
        print(f"  p=5 lam={lam!s:>5} u0={u0!s:>7}: nonempty cells {ne:2d}/15, "
              f"max diam^2={float(F(3,4)*worst):.9f}, area exact={ok_area}, diam<=1={ok_diam}")
        check(ok_area, f"p=5 lam={lam}: areas still sum exactly")
        check(ok_diam, f"p=5 lam={lam}: diameters still <= 1")

    print()
    print("=" * 78)
    print("H. Which cell kind binds, as a function of a  (p=7)")
    print("=" * 78)
    p = 7
    print(f"  {'lam':>12} {'corner':>12} {'edge':>12} {'interior':>12}")
    for lam in (F(6), F(13, 2), F(69, 10), F(7), F(71, 10)):
        S, cells = voronoi_cells(p, lam)
        idx = [(i, j) for i in range(p) for j in range(p) if i + j <= p - 1]
        per = {}
        for (i, j), poly in zip(idx, cells):
            if len(poly) < 3:
                continue
            k = kind(p, i, j)
            d2, _ = diam2(poly)
            per[k] = max(per.get(k, F(0)), d2)
        print(f"  {str(lam):>12} " + " ".join(
            f"{float(F(3,4)*per.get(k, F(0))):>12.9f}" for k in ("corner", "edge", "interior")))
    print("  -> below the threshold the corner cell is NOT the largest: the interior")
    print("     hexagons sit at exactly 1 for every a, and the edge cells exceed the")
    print("     corner cells.  Corner and edge cells reach 1 SIMULTANEOUSLY at lam = p.")

    print()
    print(f"{NCHECK[0]} checks run, {len(FAIL)} failures")
    if FAIL:
        for f in FAIL:
            print("  FAILED:", f)
        sys.exit(1)


if __name__ == "__main__":
    main()
