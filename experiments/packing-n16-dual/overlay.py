"""Overlay the enemy on the covering: which packing points share a piece?

At the certified side a* the near-optimal 16-point configuration, rescaled to
T_{a*}, has minimum pairwise distance a*/a_16 < 1, so it is NOT a legal packing
there -- some pieces must swallow two of its points.  WHICH pairs they are is
exactly "where the covering wins", i.e. the binding obstruction.

FLOATS ONLY -- diagnostic, decides nothing.
"""
import sys, os, json, math, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dual import SQ3, d2, cross, max_diam2, shoelace2

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

def enemy_uv():
    d = json.load(open(os.path.join(ROOT, "experiments", "circle-packing-search",
                                    "out", "n16.json")))
    m = d["m_min_pairwise_distance_unit_triangle"]
    P = [((x - y/SQ3)/1.0, (2.0*y/SQ3)/1.0) for (x, y) in d["unit_triangle_points"]]
    return [(max(u, 0.0), max(v, 0.0)) for (u, v) in P], 1.0/m

def inside(poly, p, eps=1e-9):
    n = len(poly)
    return all(cross(poly[i], poly[(i+1) % n], p) >= -eps for i in range(n))

def main(m=15):
    B = json.load(open(os.path.join(HERE, "best_m%d.json" % m)))
    V = B["V"]; faces = B["faces"]
    delta = math.sqrt(B["delta2"]); astar = 1.0/delta
    P1, a16 = enemy_uv()                    # unit triangle, side 1
    P = [(u*astar, v*astar) for (u, v) in P1]   # rescale into T_{a*}
    Vs = [(u*astar, v*astar) for (u, v) in V]
    polys = [[Vs[i] for i in f] for f in faces]
    print("m = %d   a* = %.7f   piece max diameter = %.9f (=1 after scaling)"
          % (m, astar, math.sqrt(max_diam2(Vs, faces))))
    print("enemy rescaled into T_{a*}: min pairwise distance = %.7f  (a*/a16 = %.7f)"
          % (astar/a16, astar/a16))
    owner = []
    for k, p in enumerate(P):
        hit = [i for i, poly in enumerate(polys) if inside(poly, p)]
        owner.append(hit)
    cnt = {}
    for k, h in enumerate(owner):
        for i in h: cnt.setdefault(i, []).append(k)
    print("\npieces holding two or more of the 16 rescaled packing points:")
    nshare = 0
    for i in sorted(cnt):
        if len(cnt[i]) >= 2:
            nshare += 1
            pts = cnt[i]
            ds = ["P%d-P%d %.5f" % (x, y, math.sqrt(d2(P[x], P[y])))
                  for x, y in itertools.combinations(pts, 2)]
            print("   piece %2d (%d-gon, diam %.6f) holds %s   [%s]"
                  % (i, len(polys[i]),
                     math.sqrt(max(d2(a, b) for a, b in itertools.combinations(polys[i], 2))),
                     ["P%d" % x for x in pts], "; ".join(ds)))
    unowned = [k for k, h in enumerate(owner) if not h]
    print("\npoints on a piece boundary / unassigned: %s" % unowned)
    print("pieces holding >=2 points: %d ; pieces holding exactly 1: %d ; empty: %d"
          % (nshare, sum(1 for i in cnt if len(cnt[i]) == 1),
             m - len(cnt)))
    # which piece is the binding one (largest diameter)?
    dm = [(max(d2(a, b) for a, b in itertools.combinations(pl, 2)), i)
          for i, pl in enumerate(polys)]
    dm.sort(reverse=True)
    print("\npiece diameters, largest first:")
    for v, i in dm:
        cen = (sum(p[0] for p in polys[i])/len(polys[i]),
               sum(p[1] for p in polys[i])/len(polys[i]))
        onb = []
        if any(abs(p[1]) < 1e-9 for p in polys[i]): onb.append("AB")
        if any(abs(p[0]) < 1e-9 for p in polys[i]): onb.append("CA")
        if any(abs(p[0]+p[1]-astar) < 1e-7 for p in polys[i]): onb.append("BC")
        print("   piece %2d  %d-gon  diam=%.9f  area=%.6f  centroid=(%.3f,%.3f)  touches %s"
              % (i, len(polys[i]), math.sqrt(v), shoelace2(polys[i])/2*SQ3/2,
                 cen[0], cen[1], ",".join(onb) if onb else "-- INTERIOR"))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 15)
