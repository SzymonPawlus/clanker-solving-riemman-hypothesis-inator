"""Structure of the enemy: the near-optimal 16-point configuration for T_a.

FLOATS ONLY.  This file decides nothing; it is a design heuristic.  Its output may
seed a subdivision topology and may not appear in any certified bound (KILL-CRITERION K5).

Reads (read-only) experiments/circle-packing-search/out/n16.json, rescales so the
minimum pairwise distance is exactly 1, and reports:
  * the contact graph (pairs at distance 1 within tol) and its rigidity/rattlers,
  * the Delaunay triangulation and the Voronoi cells inside T_a,
  * each Voronoi cell's diameter -- the quantity a covering piece must beat,
  * which pair of points is the "weak pair" as a shrinks.
"""
import json, math, os, sys, itertools

SQ3 = math.sqrt(3.0)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(ROOT, "experiments", "circle-packing-search", "out", "n16.json")

# ---- normalisation asserted before anything else (KILL-CRITERION) ----
def to_uv(x, y):   return (x - y / SQ3, 2.0 * y / SQ3)
def to_xy(u, v):   return (u + 0.5 * v, v * SQ3 / 2.0)
def d2uv(p, q):
    du, dv = p[0] - q[0], p[1] - q[1]
    return du * du + du * dv + dv * dv
for (u, v) in [(1, 0), (0, 1), (1, 1), (2, -1), (0.3, 1.7)]:
    x, y = to_xy(u, v)
    assert abs(d2uv((u, v), (0, 0)) - (x * x + y * y)) < 1e-12, "basis identity"
assert abs(to_uv(*to_xy(0.3, 1.7))[0] - 0.3) < 1e-12


def load():
    d = json.load(open(SRC))
    m = d["m_min_pairwise_distance_unit_triangle"]
    pts = [to_uv(x, y) for (x, y) in d["unit_triangle_points"]]
    a = 1.0 / m
    pts = [(u / m, v / m) for (u, v) in pts]          # min distance -> 1, side -> a
    # clamp tiny negatives from the float optimiser
    pts = [(max(u, 0.0), max(v, 0.0)) for (u, v) in pts]
    return a, pts, d


def contacts(pts, tol=1e-7):
    out = []
    for i, j in itertools.combinations(range(len(pts)), 2):
        d = math.sqrt(d2uv(pts[i], pts[j]))
        if d < 1.0 + tol:
            out.append((i, j, d))
    return out


def wall_contacts(a, pts, tol=1e-7):
    """which points sit on a side of T_a (u=0, v=0, u+v=a)."""
    out = {}
    for i, (u, v) in enumerate(pts):
        w = []
        if abs(u) < tol: w.append("CA(u=0)")
        if abs(v) < tol: w.append("AB(v=0)")
        if abs(u + v - a) < tol: w.append("BC(u+v=a)")
        if w: out[i] = w
    return out


def degrees(n, cts, walls):
    deg = [0] * n
    for i, j, _ in cts:
        deg[i] += 1; deg[j] += 1
    for i, w in walls.items():
        deg[i] += len(w)
    return deg


# ------------------- Delaunay (small n: brute force circumcircles) -------------
def circumcenter(P, Q, R):
    ax, ay = to_xy(*P); bx, by = to_xy(*Q); cx, cy = to_xy(*R)
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-14: return None
    ux = ((ax*ax+ay*ay)*(by-cy) + (bx*bx+by*by)*(cy-ay) + (cx*cx+cy*cy)*(ay-by)) / d
    uy = ((ax*ax+ay*ay)*(cx-bx) + (bx*bx+by*by)*(ax-cx) + (cx*cx+cy*cy)*(bx-ax)) / d
    return (ux, uy)


def delaunay(pts):
    n = len(pts); xy = [to_xy(*p) for p in pts]; tris = []
    for i, j, k in itertools.combinations(range(n), 3):
        c = circumcenter(pts[i], pts[j], pts[k])
        if c is None: continue
        r2 = (xy[i][0]-c[0])**2 + (xy[i][1]-c[1])**2
        if all((xy[l][0]-c[0])**2 + (xy[l][1]-c[1])**2 > r2 - 1e-9
               for l in range(n) if l not in (i, j, k)):
            tris.append((i, j, k))
    return tris


# ------------------- Voronoi cells clipped to T_a (half-plane clipping) -------
def clip(poly, nx, ny, c):
    """keep {p : nx*px+ny*py <= c}; poly in PLANE coords."""
    out = []
    m = len(poly)
    for i in range(m):
        p = poly[i]; q = poly[(i+1) % m]
        fp = nx*p[0]+ny*p[1]-c; fq = nx*q[0]+ny*q[1]-c
        if fp <= 1e-12: out.append(p)
        if (fp > 1e-12) != (fq > 1e-12):
            t = fp/(fp-fq)
            out.append((p[0]+t*(q[0]-p[0]), p[1]+t*(q[1]-p[1])))
    return out


def voronoi(a, pts):
    A = to_xy(0.0, 0.0); B = to_xy(a, 0.0); C = to_xy(0.0, a)
    cells = []
    for i, P in enumerate(pts):
        poly = [A, B, C]
        px, py = to_xy(*P)
        for j, Q in enumerate(pts):
            if j == i: continue
            qx, qy = to_xy(*Q)
            nx, ny = qx-px, qy-py
            c = (qx*qx+qy*qy - px*px - py*py) / 2.0
            poly = clip(poly, nx, ny, c)
            if not poly: break
        cells.append(poly)
    return cells


def polydiam(poly):
    return max((math.dist(p, q) for p, q in itertools.combinations(poly, 2)), default=0.0)


def polyarea(poly):
    s = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % len(poly)]
        s += x1*y2 - x2*y1
    return abs(s)/2.0


def main():
    a, pts, raw = load()
    n = len(pts)
    print("source          :", os.path.relpath(SRC, ROOT))
    print("a (side, sep=1) : %.10f   [d(16)/2 ; ceiling for any 15-piece covering]" % a)
    print("triangle area   : %.6f    15 x hexagon(diam 1) = %.6f  -> %.3f pieces needed"
          % (SQ3/4*a*a, 15*3*SQ3/8, (SQ3/4*a*a)/(3*SQ3/8)))
    cts = contacts(pts)
    walls = wall_contacts(a, pts)
    deg = degrees(n, cts, walls)
    print("\n--- points (u,v in triangular basis, separation 1) ---")
    for i, (u, v) in enumerate(pts):
        print("  P%-2d  u=%9.6f v=%9.6f  deg=%d  %s"
              % (i, u, v, deg[i], ",".join(walls.get(i, []))))
    print("\n--- contact graph: %d pairs at distance 1 (tol 1e-7) ---" % len(cts))
    for i, j, d in cts:
        print("  P%-2d - P%-2d  %.12f" % (i, j, d))
    print("\n--- wall contacts ---")
    for i in sorted(walls): print("  P%-2d on %s" % (i, ", ".join(walls[i])))
    rat = [i for i in range(n) if deg[i] <= 2]
    print("\nrattler candidates (total degree <= 2, i.e. under-constrained): %s"
          % (rat if rat else "none"))
    print("degree histogram:", {k: deg.count(k) for k in sorted(set(deg))})

    print("\n--- Voronoi cells in T_a ---")
    cells = voronoi(a, pts)
    tot = 0.0
    rows = []
    for i, c in enumerate(cells):
        d = polydiam(c); ar = polyarea(c); tot += ar
        rows.append((d, i, ar, len(c)))
    for d, i, ar, k in sorted(rows, reverse=True):
        print("  P%-2d  %d-gon  diam=%.6f  area=%.6f" % (i, k, d, ar))
    print("  sum of cell areas = %.6f   (area T_a = %.6f)" % (tot, SQ3/4*a*a))
    print("  max Voronoi cell diameter = %.6f  (a 16-piece covering needs < 1)"
          % max(r[0] for r in rows))

    print("\n--- Delaunay triangulation ---")
    tris = delaunay(pts)
    print("  %d triangles" % len(tris))
    edges = set()
    for (i, j, k) in tris:
        for e in ((i, j), (j, k), (i, k)):
            edges.add(tuple(sorted(e)))
    print("  %d Delaunay edges; of these %d are contacts (length 1)"
          % (len(edges), sum(1 for e in edges if any((i, j) == e for i, j, _ in cts))))
    print("  Delaunay edge lengths (shortest 12):")
    el = sorted((math.sqrt(d2uv(pts[i], pts[j])), i, j) for (i, j) in edges)
    for L, i, j in el[:12]:
        print("     P%-2d-P%-2d  %.9f" % (i, j, L))

    json.dump({"a": a, "points_uv": pts, "contacts": cts, "walls": walls,
               "degrees": deg, "delaunay": tris},
              open(os.path.join(HERE, "enemy.json"), "w"), indent=1)
    print("\nwrote enemy.json")


if __name__ == "__main__":
    main()
