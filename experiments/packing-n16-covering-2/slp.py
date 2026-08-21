"""Sequential-LP minimax optimiser for convex subdivisions of the UNIT triangle T_1.

FLOATS ONLY -- this is the search stage and decides nothing; every output is re-frozen
as an exact rational certificate and re-checked by verify_c1.py.

Why this and not coordinate descent (what attacks/n16-covering used):
  fix the combinatorial structure of the subdivision.  For a face f and two of its
  vertices i,j the constraint  Q(v_i - v_j) <= D2  is CONVEX in the vertex coordinates,
  and the objective min D2 is linear.  The boundary conditions are linear.  The ONLY
  non-convex constraints are the orientation/strict-convexity conditions
  cross(v_i,v_{i+1},v_{i+2}) >= delta, and those are inactive at any non-degenerate
  optimum.  So for a fixed structure the problem is essentially a convex program, and a
  trust-region SLP with an exact line search converges to ITS optimum -- unlike a
  coordinate sweep, which stalls on the non-smooth max.

Coordinates: triangular basis, T_1 = {u>=0, v>=0, u+v<=1}; Q(du,dv) = du^2+du*dv+dv^2.
A subdivision of T_1 with max piece diameter D certifies  a_16 >= 1/D.
"""
import json, math, sys
import numpy as np
from scipy.optimize import linprog

SQ3 = math.sqrt(3.0)
TOLB = 1e-7


def plane_to_uv(x, y):
    return x - y / SQ3, 2.0 * y / SQ3


def classify(uv, tol=TOLB):
    """'C'=corner (pinned), 'AB' v=0, 'CA' u=0, 'BC' u+v=1, 'F' free."""
    out = []
    for (u, v) in uv:
        on = (abs(v) < tol, abs(u) < tol, abs(u + v - 1.0) < tol)
        if sum(on) >= 2:
            out.append('C')
        elif on[0]:
            out.append('AB')
        elif on[1]:
            out.append('CA')
        elif on[2]:
            out.append('BC')
        else:
            out.append('F')
    return out


class Struct:
    """A combinatorial subdivision of T_1 plus a current float embedding."""

    def __init__(self, uv, faces, cls=None):
        self.uv = [list(p) for p in uv]
        self.faces = [list(f) for f in faces]
        self.cls = cls if cls is not None else classify(self.uv)
        self.orient()
        self.build_dofs()
        self.build_cons()

    # ---------------- setup ----------------
    def orient(self):
        for f in self.faces:
            s = 0.0
            for i in range(len(f)):
                p = self.uv[f[i]]; q = self.uv[f[(i + 1) % len(f)]]
                s += p[0] * q[1] - q[0] * p[1]
            if s < 0:
                f.reverse()

    def build_dofs(self):
        nv = len(self.uv)
        rows_u, rows_v, bu, bv, x0 = [], [], [], [], []
        nd = 0
        for k in range(nv):
            u, v = self.uv[k]
            cu = {}; cv = {}
            if self.cls[k] == 'C':
                pass
            elif self.cls[k] == 'AB':
                cu[nd] = 1.0; x0.append(u); nd += 1
            elif self.cls[k] == 'CA':
                cv[nd] = 1.0; x0.append(v); nd += 1
            elif self.cls[k] == 'BC':
                cu[nd] = 1.0; cv[nd] = -1.0; x0.append(u); nd += 1
            else:
                cu[nd] = 1.0; x0.append(u); nd += 1
                cv[nd] = 1.0; x0.append(v); nd += 1
            rows_u.append(cu); rows_v.append(cv)
            bu.append(u - sum(c * x0[i] for i, c in cu.items()))
            bv.append(v - sum(c * x0[i] for i, c in cv.items()))
        self.nd = nd
        self.Au = np.zeros((nv, nd)); self.Av = np.zeros((nv, nd))
        for k in range(nv):
            for i, c in rows_u[k].items(): self.Au[k, i] = c
            for i, c in rows_v[k].items(): self.Av[k, i] = c
        self.bu = np.array(bu); self.bv = np.array(bv)
        self.x = np.array(x0)

    def build_cons(self):
        self.pairs = []       # (i,j) vertex index pairs, unique
        seen = set()
        for f in self.faces:
            for i in range(len(f)):
                for j in range(i + 1, len(f)):
                    a, b = f[i], f[j]
                    key = (min(a, b), max(a, b))
                    if key not in seen:
                        seen.add(key); self.pairs.append(key)
        self.tris = []        # (o,p,q) consecutive triples for strict convexity
        for f in self.faces:
            m = len(f)
            for i in range(m):
                self.tris.append((f[i], f[(i + 1) % m], f[(i + 2) % m]))
        # linear side/containment constraints as rows  L.x <= r  in dof space
        L, r = [], []
        nv = len(self.uv)
        for k in range(nv):
            if self.cls[k] == 'C':
                continue
            L.append(-self.Au[k]); r.append(self.bu[k])                  # u >= 0
            L.append(-self.Av[k]); r.append(self.bv[k])                  # v >= 0
            L.append(self.Au[k] + self.Av[k]); r.append(1.0 - self.bu[k] - self.bv[k])
        # keep boundary vertices ordered along each side
        for side, key in (('AB', 0), ('CA', 1), ('BC', 0)):
            idx = [k for k in range(nv) if self.cls[k] == side]
            if side == 'AB':
                idx.sort(key=lambda k: self.uv[k][0]); co = self.Au; bo = self.bu
            elif side == 'CA':
                idx.sort(key=lambda k: self.uv[k][1]); co = self.Av; bo = self.bv
            else:
                idx.sort(key=lambda k: self.uv[k][0]); co = self.Au; bo = self.bu
            for p, q in zip(idx, idx[1:]):
                L.append(co[p] - co[q]); r.append(bo[q] - bo[p] - 1e-4)
        self.L = np.array(L) if L else np.zeros((0, self.nd))
        self.r = np.array(r) if L else np.zeros(0)

    # ---------------- evaluation ----------------
    def coords(self, x):
        return self.Au @ x + self.bu, self.Av @ x + self.bv

    def qvals(self, x):
        U, V = self.coords(x)
        i = np.array([p[0] for p in self.pairs]); j = np.array([p[1] for p in self.pairs])
        du = U[i] - U[j]; dv = V[i] - V[j]
        return du * du + du * dv + dv * dv, du, dv, i, j

    def cvals(self, x):
        U, V = self.coords(x)
        o = np.array([t[0] for t in self.tris]); p = np.array([t[1] for t in self.tris])
        q = np.array([t[2] for t in self.tris])
        return ((U[p] - U[o]) * (V[q] - V[o]) - (V[p] - V[o]) * (U[q] - U[o])), o, p, q

    def areas(self, x):
        U, V = self.coords(x)
        out = []
        for f in self.faces:
            s = 0.0
            for i in range(len(f)):
                a, b = f[i], f[(i + 1) % len(f)]
                s += U[a] * V[b] - U[b] * V[a]
            out.append(s / 2)
        return out

    def feasible(self, x, delta):
        c, _, _, _ = self.cvals(x)
        if c.min() < delta:
            return False
        if len(self.r) and (self.L @ x - self.r).max() > 1e-12:
            return False
        if min(self.areas(x)) < 1e-7:
            return False
        return True

    def maxq(self, x=None):
        if x is None: x = self.x
        return self.qvals(x)[0].max()

    # ---------------- the SLP ----------------
    def run(self, iters=400, rho0=0.02, delta=0.0, verbose=False,
            abort_below=None, abort_at=70, stall_max=30):
        nd = self.nd
        rho = rho0
        best = self.maxq(self.x)
        stall = 0
        for it in range(iters):
            if abort_below is not None and it == abort_at and best > abort_below:
                break
            x = self.x
            qv, du, dv, ii, jj = self.qvals(x)
            # gradient rows for the diameter constraints
            Pu = self.Au[ii] - self.Au[jj]           # (npair, nd)
            Pv = self.Av[ii] - self.Av[jj]
            G = (2 * du + dv)[:, None] * Pu + (du + 2 * dv)[:, None] * Pv
            cv, o, p, q = self.cvals(x)
            U, V = self.coords(x)
            H = ((V[q] - V[o])[:, None] * (self.Au[p] - self.Au[o])
                 + (U[p] - U[o])[:, None] * (self.Av[q] - self.Av[o])
                 - (U[q] - U[o])[:, None] * (self.Av[p] - self.Av[o])
                 - (V[p] - V[o])[:, None] * (self.Au[q] - self.Au[o]))
            nA = len(G) + len(H) + len(self.L)
            A = np.zeros((nA, nd + 1)); b = np.zeros(nA)
            A[:len(G), :nd] = G; A[:len(G), nd] = -1.0; b[:len(G)] = -qv
            k = len(G)
            A[k:k + len(H), :nd] = -H; b[k:k + len(H)] = cv - delta
            k += len(H)
            if len(self.L):
                A[k:, :nd] = self.L; b[k:] = self.r - self.L @ x
            c = np.zeros(nd + 1); c[nd] = 1.0
            bnds = [(-rho, rho)] * nd + [(0.0, None)]
            res = linprog(c, A_ub=A, b_ub=b, bounds=bnds, method="highs")
            if not res.success:
                rho *= 0.5
                if rho < 1e-13: break
                continue
            step = res.x[:nd]
            if np.abs(step).max() < 1e-15:
                rho *= 0.5
                if rho < 1e-13: break
                continue
            # exact line search on the true nonlinear constraints
            bt, bv_ = 0.0, best
            t = 1.0
            for _ in range(40):
                xt = x + t * step
                if self.feasible(xt, delta):
                    v = self.maxq(xt)
                    if v < bv_ - 1e-16:
                        bt, bv_ = t, v
                        break
                t *= 0.6
            if bt == 0.0:
                rho *= 0.5
                stall += 1
                if rho < 1e-13 or stall > stall_max: break
                continue
            self.x = x + bt * step
            stall = 0 if bv_ < best * (1 - 1e-11) else stall + 1
            best = bv_
            if stall > stall_max:
                break
            if bt > 0.5:
                rho = min(rho * 1.6, 0.05)
            else:
                rho *= 0.7
            if verbose and it % 25 == 0:
                print("   it %4d  rho %.2e  D %.9f  a_max %.7f"
                      % (it, rho, math.sqrt(best), 1.0 / math.sqrt(best)), flush=True)
        U, V = self.coords(self.x)
        self.uv = [[U[k], V[k]] for k in range(len(self.uv))]
        return best

    def dump(self, path, extra=None):
        U, V = self.coords(self.x)
        d = {"a": 1.0, "uv": [[U[k], V[k]] for k in range(len(self.uv))],
             "faces": self.faces, "cls": self.cls,
             "max_diam": math.sqrt(self.maxq()), "a_max": 1.0 / math.sqrt(self.maxq())}
        if extra: d.update(extra)
        json.dump(d, open(path, "w"))


def from_plane_json(path):
    """load a sub_*.json (plane coords V, faces, side a) and rescale to the unit triangle"""
    d = json.load(open(path))
    a = d["a"]
    uv = []
    for (x, y) in d["V"]:
        u, v = plane_to_uv(x, y)
        uv.append([u / a, v / a])
    return Struct(uv, d["faces"])


def from_struct_json(path):
    d = json.load(open(path))
    return Struct(d["uv"], d["faces"], d.get("cls"))


if __name__ == "__main__":
    src = sys.argv[1]
    S = from_plane_json(src) if "sub_" in src else from_struct_json(src)
    print("%s: %d faces, %d vertices, %d dofs" % (src, len(S.faces), len(S.uv), S.nd))
    print("start  a_max %.7f" % (1.0 / math.sqrt(S.maxq())))
    b = S.run(iters=int(sys.argv[3]) if len(sys.argv) > 3 else 500, verbose=True)
    print("FINAL  D = %.12f   a_max = %.9f" % (math.sqrt(b), 1.0 / math.sqrt(b)))
    if len(sys.argv) > 2:
        S.dump(sys.argv[2])
