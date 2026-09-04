"""Independent exact verification of eo-covering-construct's power-diagram certificates.

Reconstructed from the DEFINITION printed in the certificate, not from the lane's code:
  cell_i = { x : |x-p_i|^2 - w_i  <=  |x-p_j|^2 - w_j  for all j },  clipped to T_a.
Expanding, that is the half-plane   2<x, p_j - p_i>  <=  Q(p_j) - w_j - Q(p_i) + w_i,
linear in x.  Work in the lattice basis (u,v) where
  Q(u,v) = u^2 + u v + v^2      and      <x,y> = ux*uy + (ux*vy + vx*uy)/2 + vx*vy,
both rational, so no square root ever appears and every test is exact over Q.

T_a = {u >= 0, v >= 0, u + v <= a}.
"""
import json, sys
from fractions import Fraction as F
from itertools import combinations

def Q(u, v):            return u*u + u*v + v*v
def ip(x, y):           return x[0]*y[0] + (x[0]*y[1] + x[1]*y[0])/2 + x[1]*y[1]

def clip_halfplane(poly, al, be, ga):
    """keep {(u,v) : al*u + be*v <= ga}"""
    out = []
    m = len(poly)
    for i in range(m):
        cur, nxt = poly[i], poly[(i+1) % m]
        sc = ga - al*cur[0] - be*cur[1]
        sn = ga - al*nxt[0] - be*nxt[1]
        if sc >= 0: out.append(cur)
        if (sc > 0 and sn < 0) or (sc < 0 and sn > 0):
            t = sc / (sc - sn)
            out.append((cur[0] + t*(nxt[0]-cur[0]), cur[1] + t*(nxt[1]-cur[1])))
    return out

def shoelace2(poly):
    s = F(0); m = len(poly)
    for i in range(m):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % m]
        s += x1*y2 - x2*y1
    return abs(s)

def dedupe(poly):
    out = []
    for p in poly:
        if not out or p != out[-1]:
            out.append(p)
    if len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return out

def verify(path):
    d = json.load(open(path))
    a = F(int(d['a'][0]), int(d['a'][1])) if isinstance(d['a'], list) else F(d['a'])
    sites = [(F(u), F(v)) for u, v in d['sites']]
    ws = [F(w) for w in d['weights']]
    n = d['n']
    assert len(sites) == n == len(ws), (len(sites), n, len(ws))
    T = [(F(0), F(0)), (a, F(0)), (F(0), a)]
    cells = []
    for i in range(n):
        poly = T
        for j in range(n):
            if i == j: continue
            dp = (sites[j][0]-sites[i][0], sites[j][1]-sites[i][1])
            # 2<x,dp> <= Q(pj) - wj - Q(pi) + wi
            al = 2*(dp[0] + dp[1]/2)
            be = 2*(dp[1] + dp[0]/2)
            ga = Q(*sites[j]) - ws[j] - Q(*sites[i]) + ws[i]
            poly = clip_halfplane(poly, al, be, ga)
            if len(poly) < 3: break
        cells.append(dedupe(poly) if len(poly) >= 3 else [])
    nonempty = [c for c in cells if len(c) >= 3]
    # diameters
    worst = F(0); worst_i = None
    for i, c in enumerate(nonempty):
        for p, q in combinations(c, 2):
            v = Q(p[0]-q[0], p[1]-q[1])
            if v > worst: worst, worst_i = v, i
    # areas
    tot = sum(shoelace2(c) for c in nonempty)
    Tarea = shoelace2(T)
    # containment (clipping guarantees it, but check)
    inside = all(p[0] >= 0 and p[1] >= 0 and p[0]+p[1] <= a for c in nonempty for p in c)
    print(f"  {path}")
    print(f"    a = {a} = {float(a):.6f}   sites = {n}   non-empty cells = {len(nonempty)}")
    print(f"    max squared diameter (exact) = {worst}  = {float(worst):.12f}")
    print(f"    diameter <= 1 ?  {'YES' if worst <= 1 else 'NO'}"
          f"   (strictly < 1 ? {'yes' if worst < 1 else 'no'})")
    print(f"    sum of cell areas == area(T_a) ?  {tot == Tarea}   ({tot} vs {Tarea})")
    print(f"    all cell vertices inside T_a ?  {inside}")
    ok = (worst <= 1) and (tot == Tarea) and inside and len(nonempty) <= n
    print(f"    ==> certificate {'VERIFIES' if ok else 'FAILS'}: T_{float(a):.4f} is covered by "
          f"{len(nonempty)} convex sets of diameter <= 1")
    if ok:
        print(f"    ==> implies a_{{{len(nonempty)}+1}} = a_{{{len(nonempty)+1}}} >= {float(a):.6f}")
    return ok, a, len(nonempty), worst

def verify_explicit_cells(path):
    """cert28.json: explicit cells, vertices in Q(sqrt3) in the (e1,e2) lattice basis."""
    from exactq3 import Q3, q3
    import json as _j
    try:
        d = _j.load(open(path))
    except FileNotFoundError:
        print(f"  {path}: not present"); return None
    a = q3(F(d['a'])) if not isinstance(d['a'], list) else q3(F(int(d['a'][0]), int(d['a'][1])))
    def pv(vv):
        return (Q3(F(vv[0][0]), F(vv[0][1])), Q3(F(vv[1][0]), F(vv[1][1])))
    cells = [[pv(v) for v in c] for c in d['cells']]
    def Q3form(u, v): return u*u + u*v + v*v
    worst = q3(0)
    for c in cells:
        for p1, p2 in combinations(c, 2):
            val = Q3form(p1[0]-p2[0], p1[1]-p2[1])
            if val > worst: worst = val
    def sl2(poly):
        s = q3(0); m = len(poly)
        for i in range(m):
            x1, y1 = poly[i]; x2, y2 = poly[(i+1) % m]
            s = s + (x1*y2 - x2*y1)
        return s if s.sign() >= 0 else q3(0)-s
    tot = q3(0)
    for c in cells: tot = tot + sl2(c)
    Tarea = a*a
    inside = all(p[0] >= q3(0) and p[1] >= q3(0) and (p[0]+p[1]) <= a for c in cells for p in c)
    print(f"  {path}   [explicit-cell format, Q(sqrt3)]")
    print(f"    a = {a.float():.6f}   cells = {len(cells)}")
    print(f"    max squared diameter (exact Q(sqrt3)) = {worst}")
    print(f"    diameter <= 1 ?  {'YES' if worst <= q3(1) else 'NO'}"
          f"   (strictly < 1 ? {'yes' if worst < q3(1) else 'no -- equals 1'})")
    print(f"    sum of cell areas == area(T_a) ?  {tot == Tarea}")
    print(f"    all cell vertices inside T_a ?  {inside}")
    ok = (worst <= q3(1)) and (tot == Tarea) and inside
    print(f"    ==> certificate {'VERIFIES' if ok else 'FAILS'}: T_{a.float():.4f} covered by "
          f"{len(cells)} convex sets of diameter <= 1")
    return (ok, F(a.a), len(cells), worst)


if __name__ == "__main__":
    import math
    print("=" * 78)
    print("eo-covering-construct certificates -- independent exact verification")
    print("=" * 78)
    res = []
    for f in ("cert26.json", "cert27.json", "cert28opt.json"):
        try:
            res.append((f,) + verify("../packing-eo-covering/" + f))
        except FileNotFoundError:
            print(f"  {f}: not present")
        print()
    r = verify_explicit_cells("../packing-eo-covering/cert28.json")
    if r: res.append(("cert28.json",) + r)
    print()
    print("=" * 78)
    print("What each certificate proves, against Oler (a_n >= (-3+sqrt(8n+1))/2)")
    print("=" * 78)
    print(f"  {'cert':>14} {'N':>4} {'a_0':>10} {'gives':>22} {'Oler gives':>12} {'beats Oler?':>12}")
    for f, ok, a, N, w in res:
        if not ok: continue
        nn = N + 1
        oler = (-3 + math.sqrt(8*nn + 1)) / 2
        print(f"  {f:>14} {N:>4} {float(a):>10.6f} {'a_%d >= %.6f' % (nn, float(a)):>22} "
              f"{oler:>12.6f} {'YES' if float(a) > oler else 'no':>12}")
    print()
    print("  EO(7) needs a_27 >= 6 exactly.  A 26-piece cover of T_6 would prove it.")
