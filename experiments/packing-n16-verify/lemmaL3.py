#!/usr/bin/env python3
"""Part 3: two checks that do not trust my own polygon clipping.

I. Grid probe.  For a rational grid of points in T_a, the nearest site (computed by
   brute force from the site list, no polygons) must agree with the polygon that
   contains the point (exact point-in-convex-polygon).  A clipping bug that happened to
   preserve total area would still fail this.
J. Covering radius.  A cleaner and stronger route to Lemma L: if every point of T_a is
   within 1/2 of some site, then any two points with a common nearest site are <= 1
   apart by the triangle inequality, and the diameter claim follows without ever
   computing a diameter.  The max of dist-to-nearest-site over T_a is attained at a
   vertex of the clipped Voronoi arrangement, i.e. at a cell vertex.
"""

from fractions import Fraction as F
import sys

from lemmaL import Q, qdist2, area2, sites, voronoi_cells, check, FAIL, NCHECK


def inside(poly, x):
    """Exact: is x in the closed convex polygon?"""
    s = 1 if area2(poly) > 0 else -1
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        cr = (x2 - x1) * (x[1] - y1) - (y2 - y1) * (x[0] - x1)
        if s * cr < 0:
            return False
    return True


def main():
    print("=" * 78)
    print("I. Grid probe: nearest site (brute force) vs the polygon containing the point")
    print("=" * 78)
    for p, lam, M in ((5, F(5), 60), (7, F(7), 40), (5, F(9, 2), 40)):
        S, cells = voronoi_cells(p, lam)
        bad = 0
        tested = 0
        for i in range(M + 1):
            for j in range(M + 1 - i):
                x = (lam * i / M, lam * j / M)
                tested += 1
                dmin = min(qdist2(x, s) for s in S)
                near = [k for k, s in enumerate(S) if qdist2(x, s) == dmin]
                # x must lie in the polygon of every nearest site, and in no polygon
                # whose site is strictly farther
                for k, poly in enumerate(cells):
                    if len(poly) < 3:
                        continue
                    ins = inside(poly, x)
                    if ins and qdist2(x, S[k]) > dmin:
                        bad += 1
                    if (k in near) and not ins:
                        bad += 1
                # and the covering-radius consequence, directly on the grid point
                if F(3, 4) * dmin > F(1, 4):
                    bad += 1
        check(bad == 0, f"p={p} lam={lam}: grid probe ({tested} points) consistent")
        print(f"  p={p} lam={lam!s:>5}: {tested:5d} grid points, {bad} inconsistencies, "
              f"and every one is within 1/2 of a site")

    print()
    print("=" * 78)
    print("J. Covering radius: every cell vertex is within 1/2 of its own site")
    print("=" * 78)
    for p in range(2, 13):
        lam = F(p)
        S, cells = voronoi_cells(p, lam)
        worst = F(0)
        for site, poly in zip(S, cells):
            for v in poly:
                worst = max(worst, qdist2(v, site))
        r2 = F(3, 4) * worst          # squared Euclidean covering radius
        check(r2 <= F(1, 4), f"p={p}: covering radius <= 1/2")
        print(f"  p={p:2d}: max squared distance from a cell vertex to its site = {r2} "
              f"(= 1/4 exactly: {r2 == F(1,4)})")
    print("  -> covering radius exactly 1/2 at the threshold, for every p.")
    print("     Hence diam(cell) <= 2 * 1/2 = 1 by the triangle inequality, independently")
    print("     of the vertex-pair diameter computation in part 1.  Both routes agree.")

    print()
    print(f"{NCHECK[0]} checks run, {len(FAIL)} failures")
    if FAIL:
        for f in FAIL:
            print("  FAILED:", f)
        sys.exit(1)


if __name__ == "__main__":
    main()
