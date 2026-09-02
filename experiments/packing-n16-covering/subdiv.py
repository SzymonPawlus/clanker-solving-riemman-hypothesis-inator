"""Free-vertex descent on a convex planar subdivision of T_a.

FLOATS ONLY -- search stage, decides nothing; every output is re-verified in
exact.py.  This family strictly contains the power diagrams used by
attacks/eo-covering-construct (every power diagram clipped to T_a *is* a convex
subdivision), so it can only do better, and it is the step that write-up's §7(i)
named as the next thing to try.

Representation: unique vertices V (floats, plane coords), faces = ccw index
cycles.  Interior vertices move freely (2 dof); vertices on a side of T_a slide
along that side (1 dof); the three corners of T_a are pinned.  Every face is
kept strictly convex, so the union is automatically a partition of T_a.
"""
import math, json, sys
from fsearch import triangle, power_cells

SQ3 = math.sqrt(3.0)

# ---------------- build the subdivision from a power diagram ----------------

def build(a, sites, weights, tol=1e-7):
    tri = triangle(a)
    cells = [c for c in power_cells(sites, weights, tri) if len(c) >= 3]
    V = []
    def vid(p):
        for k, q in enumerate(V):
            if abs(q[0]-p[0]) < tol and abs(q[1]-p[1]) < tol:
                return k
        V.append([p[0], p[1]])
        return len(V)-1
    faces = []
    for c in cells:
        f = []
        for p in c:
            k = vid(p)
            if not f or f[-1] != k:
                f.append(k)
        if len(f) > 2 and f[0] == f[-1]:
            f.pop()
        faces.append(f)
    # split T-junctions: a vertex lying in the interior of another face's edge
    changed = True
    while changed:
        changed = False
        for f in faces:
            m = len(f)
            for i in range(m):
                p, q = V[f[i]], V[f[(i+1) % m]]
                ex, ey = q[0]-p[0], q[1]-p[1]
                L2 = ex*ex+ey*ey
                if L2 < tol*tol: continue
                for k in range(len(V)):
                    if k in f: continue
                    r = V[k]
                    t = ((r[0]-p[0])*ex + (r[1]-p[1])*ey)/L2
                    if not (1e-9 < t < 1-1e-9): continue
                    d = abs((r[0]-p[0])*ey - (r[1]-p[1])*ex)/math.sqrt(L2)
                    if d < tol:
                        f.insert(i+1, k); changed = True; break
                if changed: break
            if changed: break
    return V, faces

# ---------------- vertex classes ----------------
# side 0: AB  y=0                     ; A=(0,0) B=(a,0) C=(a/2, a*sqrt3/2)
# side 1: BC  from B to C
# side 2: CA  from C to A

def classify(V, a, tol=1e-7):
    A = (0.0, 0.0); B = (a, 0.0); C = (a/2.0, a*SQ3/2.0)
    S = [(A, B), (B, C), (C, A)]
    cls = []
    for x, y in V:
        on = []
        for si, (P, Q) in enumerate(S):
            ex, ey = Q[0]-P[0], Q[1]-P[1]
            L = math.hypot(ex, ey)
            d = abs((x-P[0])*ey - (y-P[1])*ex)/L
            if d < tol*a:
                on.append(si)
        if len(on) >= 2:   cls.append(("pin", None))
        elif len(on) == 1: cls.append(("side", on[0]))
        else:              cls.append(("free", None))
    return cls, S

# ---------------- geometry ----------------

def face_diam2(V, f):
    d = 0.0
    for i in range(len(f)):
        xi, yi = V[f[i]]
        for j in range(i+1, len(f)):
            dx = xi - V[f[j]][0]; dy = yi - V[f[j]][1]
            v = dx*dx+dy*dy
            if v > d: d = v
    return d

def face_ok(V, f, eps=1e-12):
    """strictly convex, ccw, non-degenerate"""
    m = len(f)
    for i in range(m):
        o = V[f[i]]; p = V[f[(i+1) % m]]; q = V[f[(i+2) % m]]
        cr = (p[0]-o[0])*(q[1]-o[1]) - (p[1]-o[1])*(q[0]-o[0])
        if cr < eps: return False
    return True

def orient(V, faces):
    for f in faces:
        s = 0.0
        for i in range(len(f)):
            x1, y1 = V[f[i]]; x2, y2 = V[f[(i+1) % len(f)]]
            s += x1*y2 - x2*y1
        if s < 0: f.reverse()

# ---------------- descent ----------------

class Sub:
    def __init__(self, a, V, faces):
        self.a = a; self.V = V; self.faces = faces
        orient(V, faces)
        self.cls, self.S = classify(V, a)
        self.inc = [[] for _ in V]
        for fi, f in enumerate(faces):
            for k in f: self.inc[k].append(fi)
        self.d = [face_diam2(V, f) for f in faces]

    def valid(self, fis):
        return all(face_ok(self.V, self.faces[fi]) for fi in fis)

    def obj(self, p):
        mx = max(self.d)
        return math.sqrt(mx) * sum((x/mx)**(p/2.0) for x in self.d)**(1.0/p)

    def truemax(self):
        return math.sqrt(max(face_diam2(self.V, f) for f in self.faces))

    def try_move(self, k, dx, dy, p, cur):
        old = list(self.V[k])
        self.V[k][0] += dx; self.V[k][1] += dy
        fis = self.inc[k]
        if not self.valid(fis):
            self.V[k] = old; return cur, False
        oldd = [self.d[fi] for fi in fis]
        for fi in fis: self.d[fi] = face_diam2(self.V, self.faces[fi])
        v = self.obj(p)
        if v < cur*(1-1e-15):
            return v, True
        self.V[k] = old
        for fi, dd in zip(fis, oldd): self.d[fi] = dd
        return cur, False

    def sweep(self, p, step):
        improved = False
        for k in range(len(self.V)):
            c, si = self.cls[k]
            if c == "pin": continue
            if c == "free":
                dirs = [(step,0.),(-step,0.),(0.,step),(0.,-step),
                        (step*.7,step*.7),(-step*.7,-step*.7),(step*.7,-step*.7),(-step*.7,step*.7)]
            else:
                P, Q = self.S[si]
                ex, ey = Q[0]-P[0], Q[1]-P[1]
                L = math.hypot(ex, ey); ex/=L; ey/=L
                dirs = [(step*ex, step*ey), (-step*ex, -step*ey)]
            cur = self.obj(p)
            for dx, dy in dirs:
                cur, ok = self.try_move(k, dx, dy, p, cur)
                if ok: improved = True
        return improved

    def run(self, ps=(8.,20.,60.,200.,800.), step0=None, tol=1e-9, verbose=False):
        if step0 is None: step0 = 0.05*self.a
        for p in ps:
            step = step0
            while step > tol*self.a:
                if not self.sweep(p, step): step *= 0.6
            if verbose: print("   p=%5.0f  max diam %.9f" % (p, self.truemax()), flush=True)
        return self.truemax()

def from_json(path):
    d = json.load(open(path))
    a = d["a"]; V, faces = build(a, [tuple(s) for s in d["sites"]], d["weights"])
    return a, V, faces

if __name__ == "__main__":
    a, V, faces = from_json(sys.argv[1])
    S = Sub(a, V, faces)
    print("faces %d, vertices %d, start max diam %.9f (a_max %.6f)"
          % (len(faces), len(V), S.truemax(), a/S.truemax()))
    b = S.run(verbose=True)
    print("AFTER free-vertex descent: max diam %.9f  -> a_max %.6f" % (b, a/b))
    json.dump({"a": a, "V": S.V, "faces": S.faces, "max_diam": b, "a_max": a/b},
              open(sys.argv[2], "w"))
