"""Convex m-piece subdivisions of T_a with max diameter < 1  ->  a_{m+1} >= a.

Written from the problem statement (problems/circle-packing-equilateral-triangle/
{README,RULES}.md) for worker C3; it does NOT read or import the certifier or the
search of attacks/n16-covering.

Two stages, kept strictly apart:
  * SEARCH  (floats)  -- decides nothing.  Multi-start descent on vertex positions
    of a fixed planar subdivision, minimising the largest face diameter.
  * CERTIFY (exact)   -- Fraction arithmetic only, in the triangular basis
    e1=(1,0), e2=(1/2,sqrt3/2) where |u e1 + v e2|^2 = u^2+uv+v^2 is rational.
    T_a = {u>=0, v>=0, u+v<=a}.  No square root anywhere.

The covering is *proved*, not sampled, by four independent exact facts:
  (C1) every face vertex satisfies u>=0, v>=0, u+v<=a; faces are convex, so each
       face is a subset of the convex set T_a;
  (C2) every directed face edge (i,j) is matched by exactly one (j,i) in another
       face, or else lies wholly inside one side of T_a -- so the faces form a
       closed 2-complex whose boundary is exactly partial T_a;
  (C3) all C(m,2) face pairs have zero-area intersection (exact convex clipping);
  (C4) the face areas sum EXACTLY to area(T_a).
  (C1)+(C3)+(C4) already force the union to be T_a (the union is closed and its
  complement in T_a is relatively open with measure 0, hence empty); (C2) is an
  independent combinatorial witness of the same thing.
Finally (C5) max over faces of max over vertex pairs of (u^2+uv+v^2) < 1 STRICTLY.
For a polygon (convex or not) the diameter is attained at two vertices, so (C5) is
the exact diameter test.
"""
import math, json, os, random, itertools, sys
from fractions import Fraction as F

SQ3 = math.sqrt(3.0)
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- basis asserts
def d2(p, q):
    du = p[0] - q[0]; dv = p[1] - q[1]
    return du * du + du * dv + dv * dv

def to_xy(u, v): return (u + 0.5 * v, v * SQ3 / 2.0)
def to_uv(x, y): return (x - y / SQ3, 2.0 * y / SQ3)

def _assert_basis():
    for (u, v) in [(1, 0), (0, 1), (1, 1), (2, -1), (0.3, 1.7), (-0.9, 2.2)]:
        x, y = to_xy(u, v)
        assert abs(d2((u, v), (0, 0)) - (x * x + y * y)) < 1e-12
    assert abs(to_uv(*to_xy(0.3, 1.7))[0] - 0.3) < 1e-12
    # shoelace orientation in uv agrees with xy (change of basis has det>0)
    tri = [(0, 0), (1, 0), (0, 1)]
    s_uv = sum(tri[i][0] * tri[(i+1) % 3][1] - tri[(i+1) % 3][0] * tri[i][1] for i in range(3))
    txy = [to_xy(*p) for p in tri]
    s_xy = sum(txy[i][0] * txy[(i+1) % 3][1] - txy[(i+1) % 3][0] * txy[i][1] for i in range(3))
    assert s_uv > 0 and s_xy > 0
_assert_basis()

def cross(o, p, q):
    return (p[0]-o[0]) * (q[1]-o[1]) - (p[1]-o[1]) * (q[0]-o[0])

def shoelace2(poly):          # 2 * signed uv-area
    s = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % len(poly)]
        s += x1*y2 - x2*y1
    return s

# ------------------------------------------------------- power diagram -> faces
def clip_half(poly, A, B, C):
    """keep {(u,v) : A*u + B*v <= C}."""
    out = []
    n = len(poly)
    for i in range(n):
        p = poly[i]; q = poly[(i+1) % n]
        fp = A*p[0] + B*p[1] - C
        fq = A*q[0] + B*q[1] - C
        if fp <= 0: out.append(p)
        if (fp > 0) != (fq > 0):
            t = fp / (fp - fq)
            out.append((p[0] + t*(q[0]-p[0]), p[1] + t*(q[1]-p[1])))
    return out

def power_cells(a, sites, weights=None):
    """Bisector of sites P,Q with weights w: |X-P|^2 - wP <= |X-Q|^2 - wQ.
    In uv, |X-P|^2 = (X-P).M.(X-P) with M = [[1,.5],[.5,1]] (times 2)."""
    if weights is None: weights = [0.0]*len(sites)
    T = [(0.0, 0.0), (a, 0.0), (0.0, a)]
    cells = []
    for i, P in enumerate(sites):
        poly = list(T)
        for j, Q in enumerate(sites):
            if i == j: continue
            # |X-P|^2 - |X-Q|^2 = -2 X.M.(P-Q) + P.M.P - Q.M.Q   (M as above)
            dpu, dpv = P[0]-Q[0], P[1]-Q[1]
            # cell_i = { X : |X-P|^2 - w_i <= |X-Q|^2 - w_j }
            #        = { X : A*u + B*v >= C }  with
            A = 2*dpu + dpv
            B = dpu + 2*dpv
            C = d2(P, (0,0)) - d2(Q, (0,0)) - weights[i] + weights[j]
            poly = clip_half(poly, -A, -B, -C)
            if len(poly) < 3: poly = []; break
        cells.append(poly)
    return cells

def assemble(cells, a, tol=1e-9):
    """merge near-identical vertices, drop degenerate ones, return (V, faces)."""
    V = []
    def vid(p):
        for k, q in enumerate(V):
            if abs(q[0]-p[0]) < tol and abs(q[1]-p[1]) < tol: return k
        V.append([p[0], p[1]]); return len(V)-1
    faces = []
    for c in cells:
        if len(c) < 3: return None
        f = []
        for p in c:
            k = vid(p)
            if not f or f[-1] != k: f.append(k)
        if len(f) > 1 and f[0] == f[-1]: f.pop()
        if len(f) < 3: return None
        faces.append(f)
    return V, faces

# ---------------------------------------------------------------- vertex class
# 0 free, 1 on v=0, 2 on u=0, 3 on u+v=a, 4 pinned corner
def classify(V, a, tol=1e-7):
    cls = []
    for u, v in V:
        on = []
        if abs(v) < tol*a: on.append(1)
        if abs(u) < tol*a: on.append(2)
        if abs(u+v-a) < tol*a: on.append(3)
        cls.append(4 if len(on) >= 2 else (on[0] if on else 0))
    return cls

def project(V, cls, a):
    for k, c in enumerate(V):
        u, v = c
        if cls[k] == 1:
            v = 0.0; u = min(max(u, 0.0), a)
        elif cls[k] == 2:
            u = 0.0; v = min(max(v, 0.0), a)
        elif cls[k] == 3:
            u = min(max(u, 0.0), a); v = a - u
        elif cls[k] == 4:
            pass
        else:
            u = max(u, 0.0); v = max(v, 0.0)
            if u + v > a:
                s = a/(u+v); u *= s; v *= s
        V[k][0] = u; V[k][1] = v

# ---------------------------------------------------------------- validity (float)
def face_pairs(faces):
    return [(fi, p, q) for fi, f in enumerate(faces)
            for p, q in itertools.combinations(f, 2)]

def max_diam2(V, faces):
    return max(d2(V[p], V[q]) for _, p, q in face_pairs(faces))

def validate(V, faces, a, tol=1e-7):
    """edge pairing + convexity + containment + area, in floats."""
    msgs = []
    for k, f in enumerate(faces):
        m = len(f)
        for i in range(m):
            if cross(V[f[i]], V[f[(i+1) % m]], V[f[(i+2) % m]]) < -tol:
                msgs.append("face %d not convex/ccw" % k)
                break
        if shoelace2([V[i] for i in f]) <= 0:
            msgs.append("face %d non-positive area" % k)
    for u, v in V:
        if u < -tol or v < -tol or u+v > a+tol: msgs.append("vertex outside T_a")
    de = {}
    for k, f in enumerate(faces):
        m = len(f)
        for i in range(m):
            e = (f[i], f[(i+1) % m])
            de[e] = de.get(e, 0) + 1
    for (i, j), c in de.items():
        if c != 1: msgs.append("directed edge repeated")
        if de.get((j, i), 0) == 0:
            pu, pv = V[i]; qu, qv = V[j]
            onb = ((abs(pv) < tol*a and abs(qv) < tol*a) or
                   (abs(pu) < tol*a and abs(qu) < tol*a) or
                   (abs(pu+pv-a) < tol*a and abs(qu+qv-a) < tol*a))
            if not onb: msgs.append("unmatched interior edge %d->%d" % (i, j))
    tot = sum(shoelace2([V[i] for i in f]) for f in faces)
    if abs(tot - a*a) > tol*a*a: msgs.append("area mismatch %.3e" % (tot - a*a))
    return msgs

# ---------------------------------------------------------------- optimiser
def optimise(V, faces, cls, a, iters=4000, kappa0=40.0, kappa1=4000.0,
             step0=None, seed=0, cmin_rel=1e-5):
    rnd = random.Random(seed)
    pairs = face_pairs(faces)
    triples = []
    for f in faces:
        m = len(f)
        for i in range(m):
            triples.append((f[i], f[(i+1) % m], f[(i+2) % m]))
    n = len(V)
    if step0 is None: step0 = 0.02 * a
    cmin = cmin_rel * a * a
    best = [row[:] for row in V]; bestval = max_diam2(V, faces)
    step = step0
    for it in range(iters):
        t = it / max(1, iters-1)
        kappa = kappa0 * (kappa1/kappa0) ** t
        vals = [d2(V[p], V[q]) for _, p, q in pairs]
        M = max(vals)
        beta = kappa / M
        ws = [math.exp(beta*(v - M)) for v in vals]
        Z = sum(ws)
        g = [[0.0, 0.0] for _ in range(n)]
        for w, (_, p, q) in zip(ws, pairs):
            if w < 1e-12*Z: continue
            c = w / Z
            du = V[p][0]-V[q][0]; dv = V[p][1]-V[q][1]
            gu = c*(2*du+dv); gv = c*(du+2*dv)
            g[p][0] += gu; g[p][1] += gv
            g[q][0] -= gu; g[q][1] -= gv
        # convexity barrier
        lam = 50.0 * M
        minc = float("inf")
        for (i, j, k) in triples:
            cc = cross(V[i], V[j], V[k])
            if cc < minc: minc = cc
            if cc < cmin:
                r = 2.0*lam*(cc - cmin)
                # d cross / d each coordinate
                g[i][0] += r*(V[j][1]-V[k][1]); g[i][1] += r*(V[k][0]-V[j][0])
                g[j][0] += r*(V[k][1]-V[i][1]); g[j][1] += r*(V[i][0]-V[k][0])
                g[k][0] += r*(V[i][1]-V[j][1]); g[k][1] += r*(V[j][0]-V[i][0])
        if minc > 0.0 and M < bestval - 1e-15:
            bestval = M; best = [row[:] for row in V]
        gn = math.sqrt(sum(x*x+y*y for x, y in g)) or 1.0
        s = step / gn
        for k in range(n):
            if cls[k] == 4: continue
            V[k][0] -= s*g[k][0]; V[k][1] -= s*g[k][1]
        project(V, cls, a)
        step = step0 * (0.02 ** t) * (1.0 + 0.3*rnd.random())
    for k in range(n): V[k][0], V[k][1] = best[k][0], best[k][1]
    return bestval


# ============================== EXACT STAGE ==================================
# Everything below is Fraction-only.  No float may reach a conclusion.

def q_d2(p, q):
    du = p[0]-q[0]; dv = p[1]-q[1]
    return du*du + du*dv + dv*dv

def q_cross(o, p, q):
    return (p[0]-o[0])*(q[1]-o[1]) - (p[1]-o[1])*(q[0]-o[0])

def q_shoelace2(poly):
    s = F(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % len(poly)]
        s += x1*y2 - x2*y1
    return s

def q_clip_convex(poly, A, B):
    """clip convex poly to the half-plane left of directed line A->B (ccw inside)."""
    out = []
    n = len(poly)
    for i in range(n):
        p = poly[i]; q = poly[(i+1) % n]
        fp = q_cross(A, B, p); fq = q_cross(A, B, q)
        if fp >= 0: out.append(p)
        if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
            t = F(fp, fp-fq)
            out.append((p[0] + t*(q[0]-p[0]), p[1] + t*(q[1]-p[1])))
    return out

def q_intersect_area2(P, Q):
    """|2*area| of the intersection of two ccw convex polygons, exactly."""
    poly = list(P)
    n = len(Q)
    for i in range(n):
        poly = q_clip_convex(poly, Q[i], Q[(i+1) % n])
        if len(poly) < 3: return F(0)
    return abs(q_shoelace2(poly))

def snap(V, cls, den):
    """one rational per vertex; boundary vertices forced EXACTLY onto their side
    of T_1 (a = 1 here).  Shared vertices stay shared, so the topology is kept."""
    out = []
    for k, (u, v) in enumerate(V):
        U = F(round(u*den), den); Vv = F(round(v*den), den)
        c = cls[k]
        if c == 1: Vv = F(0)
        elif c == 2: U = F(0)
        elif c == 3: Vv = 1 - U
        elif c == 4:
            U = F(0) if u < 0.5 else F(1)
            Vv = F(1) if v > 0.5 else F(0)
            if U == 1: Vv = F(0)
        if U < 0: U = F(0)
        if Vv < 0: Vv = F(0)
        out.append((U, Vv))
    return out

def certify(faces_q, a_q, verbose=True):
    """faces_q: list of ccw polygons of exact (u,v) Fractions, in T_{a_q}.
    Returns (ok, max_d2, report)."""
    R = []; ok = True
    def say(good, txt):
        nonlocal ok
        if not good: ok = False
        R.append(("ok  " if good else "FAIL") + "  " + txt)

    # C1 containment
    bad = [(k, p) for k, f in enumerate(faces_q) for p in f
           if p[0] < 0 or p[1] < 0 or p[0]+p[1] > a_q]
    say(not bad, "C1 every vertex in T_a  (u>=0, v>=0, u+v<=a)")

    # convexity / simplicity / ccw
    nonconv = []
    for k, f in enumerate(faces_q):
        m = len(f)
        if m < 3: nonconv.append(k); continue
        if q_shoelace2(f) <= 0: nonconv.append(k); continue
        for i in range(m):
            if q_cross(f[i], f[(i+1) % m], f[(i+2) % m]) <= 0:
                nonconv.append(k); break
    say(not nonconv, "C1' every face strictly convex and ccw (so face subset T_a)")

    # C2 edge pairing: directed edges cancel except on the boundary
    de = {}
    for f in faces_q:
        m = len(f)
        for i in range(m):
            e = (f[i], f[(i+1) % m])
            de[e] = de.get(e, 0) + 1
    dup = [e for e, c in de.items() if c != 1]
    unmatched = []
    for (p, q) in de:
        if (q, p) not in de:
            onb = ((p[1] == 0 and q[1] == 0) or (p[0] == 0 and q[0] == 0) or
                   (p[0]+p[1] == a_q and q[0]+q[1] == a_q))
            if not onb: unmatched.append((p, q))
    say(not dup and not unmatched,
        "C2 directed edges pair up; unmatched ones lie inside a side of T_a")

    # C3 pairwise interior-disjoint
    over = []
    for i, j in itertools.combinations(range(len(faces_q)), 2):
        if q_intersect_area2(faces_q[i], faces_q[j]) != 0: over.append((i, j))
    say(not over, "C3 all %d face pairs meet in exactly zero area"
        % (len(faces_q)*(len(faces_q)-1)//2))

    # C4 areas sum exactly to area(T_a)
    tot = sum(q_shoelace2(f) for f in faces_q)
    say(tot == a_q*a_q, "C4 sum of face areas == area(T_a)  (2*uv-shoelace: %s vs %s)"
        % (tot, a_q*a_q))

    # C5 strict diameter
    md = F(0); arg = None
    for k, f in enumerate(faces_q):
        for p, q in itertools.combinations(f, 2):
            v = q_d2(p, q)
            if v > md: md = v; arg = (k, p, q)
    say(md < 1, "C5 max squared diameter = %s = %.12f  <  1  STRICTLY"
        % (md, float(md)))
    if verbose:
        for line in R: print("   " + line)
    return ok, md, R
