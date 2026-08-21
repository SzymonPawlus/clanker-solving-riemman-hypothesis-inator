"""Freeze a float convex subdivision of T_a into an EXACT rational certificate.

Everything below is exact rational arithmetic in the triangular basis
e1=(1,0), e2=(1/2,sqrt3/2), where |u e1 + v e2|^2 = u^2+uv+v^2 is RATIONAL.
T_a = {u>=0, v>=0, u+v<=a}.  With a rational, every coordinate, every squared
diameter and every area below is an exact rational; no float decides anything.

Why the covering is proved and not sampled:
  * each face is a simple (indeed strictly convex) polygon whose vertices all
    satisfy u>=0, v>=0, u+v<=a, hence face  subset of  T_a (T_a is convex);
  * the faces come from a fixed planar subdivision, and their shoelace areas are
    checked to sum EXACTLY to the shoelace area of T_a;
  * so  sum |F_i| = |T_a|  with  F_i subset T_a, forcing |union F_i| = |T_a|;
    the union is closed, so T_a \ union is relatively open and null, hence empty.
  * finally every face has squared diameter STRICTLY below 1, so it holds at
    most one point of a set with pairwise distances >= 1.
"""
import json, math, sys
from fractions import Fraction as F
from exact import q3, Q3, diam2, shoelace2, triangle, cross, dist2

SQ3 = math.sqrt(3.0)

def to_uv(x, y):
    return x - y/SQ3, 2.0*y/SQ3

def snap(V, a_f, a_q, den, tol=1e-7):
    """round each unique vertex once, forcing boundary vertices EXACTLY onto the
    corresponding side of T_a so that the area identity is exact by construction."""
    out = []
    for (x, y) in V:
        u, v = to_uv(x, y)
        U = F(round(u*den), den); Vv = F(round(v*den), den)
        onu = abs(u) < tol*a_f          # side CA : u = 0
        onv = abs(v) < tol*a_f          # side AB : v = 0
        onw = abs(u+v-a_f) < tol*a_f    # side BC : u+v = a
        if onu: U = F(0)
        if onv: Vv = F(0)
        if onw:
            if onu:   U, Vv = F(0), a_q
            elif onv: U, Vv = a_q, F(0)
            else:     Vv = a_q - U
        if U < 0: U = F(0)
        if Vv < 0: Vv = F(0)
        out.append((U, Vv))
    return out

def check(P, a_q, verbose=True, strict=True):
    """P: list of faces, each a list of (u,v) exact Fractions, ccw."""
    a = q3(a_q)
    ok = True
    msgs = []
    # 1. containment
    for k, f in enumerate(P):
        for (u, v) in f:
            if u < 0 or v < 0 or u+v > a_q:
                msgs.append("FAIL face %d vertex outside T_a" % k); ok = False
    # 2. strict convexity + ccw  (=> simple polygon, shoelace = area)
    for k, f in enumerate(P):
        m = len(f)
        if m < 3:
            msgs.append("FAIL face %d degenerate" % k); ok = False; continue
        for i in range(m):
            o, p, q = f[i], f[(i+1) % m], f[(i+2) % m]
            cr = (p[0]-o[0])*(q[1]-o[1]) - (p[1]-o[1])*(q[0]-o[0])
            if cr <= 0:
                msgs.append("FAIL face %d not strictly convex/ccw at vertex %d" % (k, i))
                ok = False
    # 3. squared diameters, STRICTLY < 1
    worst = F(0); wk = -1
    for k, f in enumerate(P):
        d = F(0)
        for i in range(len(f)):
            for j in range(i+1, len(f)):
                du = f[i][0]-f[j][0]; dv = f[i][1]-f[j][1]
                q = du*du + du*dv + dv*dv
                if q > d: d = q
        if d > worst: worst, wk = d, k
        if (d >= 1) if strict else (d > 1):
            msgs.append("FAIL face %d squared diameter %s (>= 1)" % (k, d)); ok = False
    # 4. exact area identity
    tot = F(0)
    for f in P:
        s = F(0)
        for i in range(len(f)):
            x1, y1 = f[i]; x2, y2 = f[(i+1) % len(f)]
            s += x1*y2 - x2*y1
        if s <= 0:
            msgs.append("FAIL face has non-positive shoelace"); ok = False
        tot += s
    target = a_q*a_q          # shoelace2 of {(0,0),(a,0),(0,a)} = a^2
    if tot != target:
        msgs.append("FAIL area sum %s != %s" % (tot, target)); ok = False
    if verbose:
        for m in msgs: print("  " + m)
        print("  faces %d   max squared diameter %s  (~%.15f)  face %d"
              % (len(P), "" if len(str(worst)) > 60 else worst, float(worst), wk))
        print("  max diameter ~ %.15f     strictly < 1 : %s" % (math.sqrt(float(worst)), worst < 1))
        print("  exact area identity  sum = a^2 : %s" % (tot == target))
        print("  VERDICT : %s" % ("PASS" if ok else "FAIL"))
    return ok, worst

def certify(src, den=10**5, verbose=True):
    d = json.load(open(src))
    a_f = d["a"]
    Vf = d["V"]; faces = d["faces"]
    # largest a this configuration supports, from the float max diameter
    best = None
    lo, hi = F(0), F(int(a_f*10**6), 10**6)
    # binary search on a rational a: rescale the (u,v) config to side a, snap, check
    Vuv = [to_uv(x, y) for (x, y) in Vf]
    def attempt(a_q):
        r = float(a_q)/a_f
        Vs = [(x*r, y*r) for (x, y) in Vf]
        S = snap(Vs, float(a_q), a_q, den)
        P = [[S[k] for k in f] for f in faces]
        return check(P, a_q, verbose=False), P
    # scan downward from the float estimate
    return attempt, faces

if __name__ == "__main__":
    src = sys.argv[1]
    den = int(sys.argv[2]) if len(sys.argv) > 2 else 10**5
    d = json.load(open(src))
    a_f = d["a"]; Vf = d["V"]; faces = d["faces"]
    amax = d["a_max"]
    print("%s : float a_max = %.9f" % (src, amax))
    # try successively smaller rational a until the exact strict check passes
    best = None
    for k in range(200):
        a_q = F(int((amax*10**6) - k*100), 10**6)   # step 1e-4 downward
        r = float(a_q)/a_f
        Vs = [(x*r, y*r) for (x, y) in Vf]
        S = snap(Vs, float(a_q), a_q, den)
        P = [[S[j] for j in f] for f in faces]
        ok, worst = check(P, a_q, verbose=False)
        if ok:
            best = (a_q, P, worst); break
    if best is None:
        print("  no rational a certified"); sys.exit(1)
    a_q, P, worst = best
    print("EXACT CERTIFICATE at a = %s = %.9f" % (a_q, float(a_q)))
    check(P, a_q, verbose=True)
    json.dump({"a": [str(a_q.numerator), str(a_q.denominator)],
               "faces_uv": [[[str(u.numerator)+"/"+str(u.denominator),
                              str(v.numerator)+"/"+str(v.denominator)] for (u, v) in f] for f in P],
               "max_sq_diam": str(worst)},
              open(src.replace(".json", "_cert.json"), "w"), indent=1)
    print("written", src.replace(".json", "_cert.json"))
