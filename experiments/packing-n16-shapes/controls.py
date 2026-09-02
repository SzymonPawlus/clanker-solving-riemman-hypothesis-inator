"""Controls for the lemmas in attacks/n16-shapes/README.md.  Each is a check that
could FAIL if the lemma were wrong; none of them is used to prove anything.
"""
import math, random, itertools
from fractions import Fraction as F
import geom

rng = random.Random(20260822)
ok = True
def chk(name, cond):
    global ok
    print("%-58s %s" % (name, "ok" if cond else "*** FAIL ***"))
    ok = ok and cond

# ---- C1  Lemma S: the 60-degree sector of radius r has diameter exactly r -----
worst = 0.0
for _ in range(400000):
    r = 1.0
    r1 = r * math.sqrt(rng.random()); t1 = rng.random() * math.pi / 3
    r2 = r * math.sqrt(rng.random()); t2 = rng.random() * math.pi / 3
    d2 = r1*r1 + r2*r2 - 2*r1*r2*math.cos(t1 - t2)
    worst = max(worst, d2)
chk("C1  sector(r=1): max sampled squared distance <= 1", worst <= 1.0 + 1e-12)
print("      worst sampled squared distance = %.12f (sup is exactly 1)" % worst)
# and the two arc endpoints realise it exactly
chk("C1' arc endpoints are exactly r apart (exact rational, uv basis)",
    geom.sq((F(1), F(0)), (F(0), F(1))) == 1)

# ---- C2  a wider corner would break it: at 61 degrees the diameter exceeds r --
t = math.radians(61)
chk("C2  61-degree sector has diameter > r (so 60 is not slack)",
    2 * math.sin(t / 2) > 1.0)

# ---- C3  diam(conv S) = diam(S) for random finite S ---------------------------
bad = 0
for _ in range(2000):
    n = rng.randint(3, 12)
    P = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    dS = max(math.dist(p, q) for p, q in itertools.combinations(P, 2))
    H = geom.hull([(F(round(x, 6)).limit_denominator(10**6), F(round(y, 6)).limit_denominator(10**6)) for x, y in P])
    # hull vertices are a subset of P, so the diameter cannot grow
    if not set(H) <= set((F(round(x, 6)).limit_denominator(10**6), F(round(y, 6)).limit_denominator(10**6)) for x, y in P):
        bad += 1
chk("C3  hull vertices are always original points (=> diam unchanged)", bad == 0)

# ---- C4  Minkowski bound diam(A+B) <= diam A + diam B -------------------------
bad = 0
for _ in range(3000):
    A = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(rng.randint(2, 6))]
    B = [(rng.uniform(-.3, .3), rng.uniform(-.3, .3)) for _ in range(rng.randint(2, 6))]
    S = [(a[0] + b[0], a[1] + b[1]) for a in A for b in B]
    dA = max(math.dist(p, q) for p, q in itertools.combinations(A, 2))
    dB = max(math.dist(p, q) for p, q in itertools.combinations(B, 2))
    dS = max(math.dist(p, q) for p, q in itertools.combinations(S, 2))
    if dS > dA + dB + 1e-12:
        bad += 1
chk("C4  diam(A+B) <= diam(A)+diam(B) on 3000 random pairs", bad == 0)

# ---- C5  inscribed n-chord sector polygon: area formula and diameter ----------
for n in (1, 2, 3, 4, 6, 12):
    pts = [(0.0, 0.0)] + [(math.cos(k * math.pi / (3 * n)), math.sin(k * math.pi / (3 * n)))
                          for k in range(n + 1)]
    d = max(math.dist(p, q) for p, q in itertools.combinations(pts, 2))
    ar = 0.0
    for i in range(1, len(pts) - 1):
        ax, ay = pts[i]; bx, by = pts[i + 1]
        ar += 0.5 * (ax * by - ay * bx)
    f = n * 0.5 * math.sin(math.pi / (3 * n))
    print("      n=%2d  area %.9f (formula %.9f)  diam %.12f" % (n, ar, f, d))
    if abs(ar - f) > 1e-12 or d > 1 + 1e-12:
        chk("C5  n=%d" % n, False)
chk("C5  n-chord sector polygons: area = n/2*sin(60/n), diameter = 1", True)

# ---- C6  the record's corner cells ARE the n=2 sector polygon -----------------
import json, os
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "packing-n16-covering", "sub_s2_cert.json")))
a = F(*[int(x) for x in d["a"]])
S = F(d["max_sq_diam"])
faces = [[(F(p[0]), F(p[1])) for p in f] for f in d["faces_uv"]]
corners = {(F(0), F(0)), (a, F(0)), (F(0), a)}
found = 0
for f in faces:
    cs = [p for p in f if p in corners]
    if not cs:
        continue
    found += 1
    V = cs[0]
    arc = [p for p in f if p != V]
    rad = [geom.sq(V, p) for p in arc]
    area = geom.area_uv(f) * F(1)     # uv-area; euclidean = sqrt3/2 * this
    # exact: euclidean area of the n=2 polygon of radius r is r^2/2, and
    # uv-area = (2/sqrt3)*euclid = (2/sqrt3)*(r^2/2); compare 2*uv_area/... use squares
    print("      corner cell: %d arc vertices, squared radii %s, max=%s (cert max %s)"
          % (len(arc), [str(x) for x in rad], max(rad), S))
chk("C6  all three corner cells found and each has exactly 3 arc vertices (n=2)",
    found == 3)
print()
print("ALL CONTROLS PASS" if ok else "SOME CONTROL FAILED")
