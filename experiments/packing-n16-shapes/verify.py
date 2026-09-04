"""Independent re-verification of a certificate file, from the problem statement.

Reads only the certificate JSON (15 polygons, exact rationals, triangular basis) and
checks, in exact rational arithmetic:
  1. exactly 15 pieces, each a simple strictly-convex ccw polygon;
  2. every vertex satisfies u >= 0, v >= 0, u + v <= a, so every piece lies in T_a;
  3. max squared diameter over vertex pairs is < 1 STRICTLY;
  4. T_a minus the union of the pieces is empty (exact polygon difference) -- this is
     the covering proof, and it does not use areas or disjointness at all;
  5. reports the total overlap, i.e. whether this is a partition or a real covering.
Then a_16 >= a / sqrt(max_sq_diam) and s(16) >= 2*a_16 + 2*sqrt3.
"""
import sys, os, json, math
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom

c = json.load(open(sys.argv[1]))
a = F(int(c["a"][0]), int(c["a"][1]))
P = [[(F(p[0]), F(p[1])) for p in poly] for poly in c["pieces_uv"]]
print("certificate: %s" % sys.argv[1])
print("a = %s = %.9f     pieces = %d" % (a, float(a), len(P)))
ok = True
def chk(name, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("  %-56s %s %s" % (name, "ok" if cond else "*** FAIL ***", extra))

chk("exactly 15 pieces", len(P) == 15)
chk("every piece is a simple strictly convex ccw polygon",
    all(geom.is_convex_ccw(geom.ccw(q)) for q in P))
chk("every vertex lies in T_a  (u,v >= 0, u+v <= a)",
    all(p[0] >= 0 and p[1] >= 0 and p[0] + p[1] <= a for q in P for p in q))
S = max(geom.diam2(q) for q in P)
chk("max squared diameter < 1 STRICTLY", S < 1, "S = %s = %.12f" % (S, float(S)))
rem = geom.cover_remainder(geom.tri(a), [geom.ccw(q) for q in P])
chk("T_a \\ union(pieces) is empty (exact difference)", len(rem) == 0,
    "leftover uv-area %s" % sum(geom.area_uv(r) for r in rem))

tot = sum(geom.area_uv(q) for q in P)
TA = geom.area_uv(geom.tri(a))
print("  sum of piece uv-areas %s  vs  uv-area(T_a) %s" % (tot, TA))
print("  overlap (sum - T_a) = %s = %.9f  ->  %s"
      % (tot - TA, float(tot - TA) * math.sqrt(3) / 2,
         "PARTITION (no overlap)" if tot == TA else "GENUINE OVERLAPPING COVERING"))
npair = 0
ov = F(0)
for i in range(len(P)):
    for j in range(i + 1, len(P)):
        Q = geom.ccw(P[i])
        for (aa, bb, cc) in geom.edges_halfplanes(geom.ccw(P[j])):
            Q = geom.clip_halfplane(Q, aa, bb, cc)
            if not Q:
                break
        if Q and geom.area_uv(Q) > 0:
            npair += 1
            ov += geom.area_uv(Q)
print("  %d of %d piece pairs overlap in positive area, total uv-area %s (%.9f Euclidean)"
      % (npair, len(P) * (len(P) - 1) // 2, ov, float(ov) * math.sqrt(3) / 2))

astar = float(a) / math.sqrt(float(S))
lo = F(c["a_star_rational_lower_bound"])
chk("quoted rational bound r satisfies r^2 * S <= a^2 (exact)", lo * lo * S <= a * a,
    "r = %s = %.12f" % (lo, float(lo)))
print()
print("  a_16 >= a/sqrt(S) = %.12f" % astar)
print("  s(16) = 2*a_16 + 2*sqrt3 >= %.9f" % (2 * astar + 2 * math.sqrt(3)))
print("  standing record  a_16 >= 446335/99998 = %.12f" % (446335 / 99998))
print("  improvement %.9f" % (astar - 446335 / 99998))
print()
print("VERIFIED" if ok else "VERIFICATION FAILED")
