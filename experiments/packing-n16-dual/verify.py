"""Independent re-verification of cert_m<m>.json, written separately from
dual.certify: it re-parses the file, re-derives every quantity, and adds two
checks that certify() does not make --

  * a deterministic exact GRID smoke test: every point of a rational grid in
    T_a, plus every face vertex and every face edge midpoint, lies in at least
    one face.  This cannot prove a covering, but it would catch a hole that the
    area identity missed.
  * the boundary chain: the unmatched directed edges, walked in order, must
    traverse each side of T_a from corner to corner with no gap and no overlap.

Exact rational arithmetic only.  Run:  python3 verify.py [m]
"""
import sys, os, json, itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))

def cross(o, p, q):
    return (p[0]-o[0])*(q[1]-o[1]) - (p[1]-o[1])*(q[0]-o[0])

def sq(p, q):
    du = p[0]-q[0]; dv = p[1]-q[1]
    return du*du + du*dv + dv*dv

def sh2(P):
    s = F(0)
    for i in range(len(P)):
        x1, y1 = P[i]; x2, y2 = P[(i+1) % len(P)]
        s += x1*y2 - x2*y1
    return s

def inside(P, x):
    n = len(P)
    return all(cross(P[i], P[(i+1) % n], x) >= 0 for i in range(n))

def clip(P, A, B):
    out = []
    for i in range(len(P)):
        p = P[i]; q = P[(i+1) % len(P)]
        fp = cross(A, B, p); fq = cross(A, B, q)
        if fp >= 0: out.append(p)
        if (fp > 0) != (fq > 0) and fp != fq:
            t = F(fp, fp-fq)
            out.append((p[0]+t*(q[0]-p[0]), p[1]+t*(q[1]-p[1])))
    return out

def main(m=15):
    D = json.load(open(os.path.join(HERE, "cert_m%d.json" % m)))
    a = F(D["a_numer"], D["a_denom"])
    faces = [[(F(p[0]), F(p[1])) for p in f] for f in D["faces_uv"]]
    fails = []
    print("certificate cert_m%d.json:  m = %d faces,  a = %s = %.10f"
          % (m, len(faces), a, float(a)))
    if len(faces) != m: fails.append("face count")

    # 1. containment + convexity
    for k, f in enumerate(faces):
        if sh2(f) <= 0: fails.append("face %d orientation/area" % k)
        n = len(f)
        for i in range(n):
            u, v = f[i]
            if u < 0 or v < 0 or u+v > a: fails.append("face %d vertex outside" % k)
            if cross(f[i], f[(i+1) % n], f[(i+2) % n]) <= 0:
                fails.append("face %d not strictly convex" % k)
    print("  containment + strict convexity: %s" % ("FAIL" if fails else "ok"))

    # 2. exact diameter
    md = F(0); who = None
    for k, f in enumerate(faces):
        for p, q in itertools.combinations(f, 2):
            s = sq(p, q)
            if s > md: md = s; who = k
    print("  max squared diameter = %s" % md)
    print("     = %.15f   %s 1   (attained on face %d)"
          % (float(md), "<" if md < 1 else ">=", who))
    if md >= 1: fails.append("diameter not < 1")

    # 3. areas
    tot = sum(sh2(f) for f in faces)
    print("  sum of 2*uv-shoelace areas == a^2 : %s" % (tot == a*a))
    if tot != a*a: fails.append("area")

    # 4. pairwise disjoint
    bad = 0
    for i, j in itertools.combinations(range(len(faces)), 2):
        P = list(faces[i]); Q = faces[j]
        for k in range(len(Q)):
            P = clip(P, Q[k], Q[(k+1) % len(Q)])
            if len(P) < 3: break
        if len(P) >= 3 and sh2(P) != 0: bad += 1
    print("  pairwise interior-disjoint (%d pairs): %s"
          % (len(faces)*(len(faces)-1)//2, "ok" if bad == 0 else "FAIL %d" % bad))
    if bad: fails.append("overlap")

    # 5. boundary chain covers each side exactly
    de = set()
    for f in faces:
        n = len(f)
        for i in range(n): de.add((f[i], f[(i+1) % n]))
    unm = [(p, q) for (p, q) in de if (q, p) not in de]
    sides = {"AB (v=0)": lambda p: p[1] == 0,
             "CA (u=0)": lambda p: p[0] == 0,
             "BC (u+v=a)": lambda p: p[0]+p[1] == a}
    for name, test in sides.items():
        segs = sorted(((min(p[0]+p[1] if name.startswith("BC") else
                            (p[0] if name.startswith("AB") else p[1]),
                            q[0]+q[1] if name.startswith("BC") else
                            (q[0] if name.startswith("AB") else q[1])),
                        max(p[0]+p[1] if name.startswith("BC") else
                            (p[0] if name.startswith("AB") else p[1]),
                            q[0]+q[1] if name.startswith("BC") else
                            (q[0] if name.startswith("AB") else q[1])))
                       for (p, q) in unm if test(p) and test(q)))
        # for BC parameterise by u instead (u+v=a is constant); redo:
        if name.startswith("BC"):
            segs = sorted((min(p[0], q[0]), max(p[0], q[0]))
                          for (p, q) in unm if test(p) and test(q))
        cur = F(0); ok = True
        for lo, hi in segs:
            if lo != cur: ok = False; break
            cur = hi
        if cur != a: ok = False
        print("  boundary chain on %-12s: %s  (%d segments)"
              % (name, "ok, gapless corner to corner" if ok else "FAIL", len(segs)))
        if not ok: fails.append("boundary " + name)

    # 6. grid smoke test
    G = 40
    miss = 0; tested = 0
    pts = []
    for i in range(G+1):
        for j in range(G+1-i):
            pts.append((a*F(i, G), a*F(j, G)))
    for f in faces:
        n = len(f)
        pts.extend(f)
        pts.extend(((f[i][0]+f[(i+1) % n][0])/2, (f[i][1]+f[(i+1) % n][1])/2)
                   for i in range(n))
    for x in pts:
        tested += 1
        if not any(inside(f, x) for f in faces): miss += 1
    print("  grid/vertex/midpoint smoke test: %d points, %d uncovered" % (tested, miss))
    if miss: fails.append("uncovered sample")

    print("\n  RESULT: %s" % ("ALL CHECKS PASS -- a_%d >= %s = %.10f"
                              % (m+1, a, float(a)) if not fails
                              else "FAILED: " + ", ".join(fails)))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 15)
