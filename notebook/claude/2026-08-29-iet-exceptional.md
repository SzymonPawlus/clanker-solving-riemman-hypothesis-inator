# 2026-08-29 — exceptional set of a simple polygon (lane `exceptional-set-polygons`)

Working journal. Agent `claude` (Claude Opus 5), branch
`claude/inscribe-equilateral-triangle-oj15x1`. Lane files owned:
`problems/inscribed-equilateral-triangle/attacks/exceptional-set-polygons/{README.md,KILL-CRITERION.md}`
and this file. Nothing else was written; `experiments/inscribed-triangle-polygons/` was **read and
run only**, never modified, and all scratch code lived outside the repo.

Brief: prove `|E(P)| ≤ 2` for every simple polygon, or find what actually happens.
**Outcome: the reduction closes, "exceptional ⟹ wedge-type" is false, the count does not close.**

---

## Order of work

1. Read `RULES.md` §0/§3/§7, the problem `README.md` and `RULES.md`, then the five briefed attack
   READMEs in full. Time well spent: three of them contain the same lemma under three names, and
   knowing that was what let me decide, up front, that I would re-derive rather than cite.
2. Designed the candidate witness **on paper** (the polygonal spiral channel) — before writing the
   kill-criterion. Said so in `KILL-CRITERION.md`'s provenance paragraph rather than pretending the
   file predated the idea.
3. Wrote `KILL-CRITERION.md`. Only then ran anything.
4. Validation gate (K1): three controls through the committed decider.
5. Built and decided the witness; verified the hand proof's hypotheses in exact `Q`.
6. Wrote a second decider from scratch; re-decided controls, witness, fork.
7. Polygon control on Theorem 1 (angle ≥ 60 ⟹ good; non-vertex ⟹ good).
8. Two seeded hunts for three exceptional vertices.
9. Wrote up.

Wall clock on computation: roughly six minutes total across all runs; nothing near the budget.

---

## The one idea

Everything follows from taking the criterion literally:

> `O` is exceptional ⟺ for **every** `r > 0`, the set of directions in which `J` meets the circle
> of radius `r` about `O` contains no two elements exactly `60°` apart.

That is a condition on **each circle separately**. It never compares different radii. So a curve is
free to occupy a *different* narrow arc at each radius, and the union of those arcs can be almost
the whole circle. `spiral-tip-witness` found this and called it the rotating wedge; that lane then
argued — as motivation only, flagged `sketch` — that polygons cannot do it, because the arc would
have to rotate through unboundedly many turns as `r → 0`.

**That inference is wrong, and it is the crux of this lane.** The arc does not have to rotate at
all, let alone infinitely often; it only has to be narrower than `60°`. Finite rotation is enough to
break wedge-type, and a polygon delivers finite rotation happily: a channel of constant angular
width, wound through `221°` in fourteen straight edges, terminating at `O` in an ordinary wedge.

The reason the *log spiral* needs infinite winding is different and specific to it: its two arms
are curves of zero width, so the only way to close the region into a Jordan curve is to spiral (that
lane's §4.1 is right about that). Make the arms the two **walls of a channel** and nothing has to
accumulate.

Once seen, the construction is forced: take a radially monotone polygonal chain `A` from `O`, and
let the second wall be `ω(A)` for a rotation `ω` by `w < 60°` about `O`. Then the two walls sit at
angular separation exactly `w` on **every** circle, by construction, because `ω` fixes every circle
about `O`. Rational rotation `(cos, sin) = (4/5, 3/5)` keeps everything in `Q`.

---

## Things I got wrong or nearly got wrong

- **The brief's suggested shortcut for the reduction is a real gap.** "Every non-vertex point has a
  tangent line, so the local cone is `180°`, so there is a triangle" — no: a tangent line gives two
  directions `180°` apart, and the criterion wants `60°`. The local *segment* of `J` through `O` is
  useless. What closes it is that the *interior* fills a half-disc, and converting an interior
  overlap into a curve intersection is exactly the region lemma, which needs the Jordan curve
  theorem and a measure argument. I nearly wrote the shortcut down before noticing.
- **I initially reached for an intermediate-value argument on the first-exit ("visibility") function
  `ψ(φ)`** from `O` into the polygon, hoping for `ψ(φ) = ψ(φ − 60°)`. It does not work: `ψ` jumps at
  directions aiming at reflex vertices, it is only lower semicontinuous, and `F = ψ(φ) − ψ(φ−60°)`
  can change sign *by jumping over zero*. Recorded so nobody spends an afternoon on it. The region
  route (Lemma 3 + Lemma 4) has no such problem because it never needs a continuous scalar function.
- **I checked that the witness proof does not need the region lemma at all.** My first draft ran
  `Ω̄ ⊆ channel` via a shear homeomorphism and a connectedness argument (the same device as
  `spiral-tip-witness` §4.3). Then I noticed the criterion is a statement about `J` as a bare point
  set, so `J ⊆ channel` — which is elementary — suffices. Dropping the topology from Theorem 3 made
  it much stronger and much easier to check. That simplification is the single best thing I did.
- **"Exceptional ⟹ hull vertex"** felt obviously true for about a minute. The witness has `O` in the
  interior of the convex hull (its directions span `258° > 180°`, so no supporting line at `O`).
- **The tuning fork.** My first idea for three exceptional points was three thin parallel prongs
  with tips at one end. It cannot work, and the reason generalises into Proposition 5 (no sweep):
  the angular separation between the own prong's wall (constant, since it is radial from the tip)
  and the neighbouring prong's wall (sweeping continuously from `0°` to `−90°` as the radius grows)
  must pass through `60°`. Confirmed exactly: a fork with `0.2858°` tips has both tips **good**.

---

## What I could not do

`|E(P)| ≤ 2`. The count dies at one identifiable place: the convex angle-sum argument needs
`∠Oⱼ Oᵢ O_k < 60°` at each exceptional `Oᵢ`, which is free for a wedge-type point and false for a
non-wedge one; and the criterion at `Oᵢ` constrains each circle separately, while `Oⱼ` and `O_k`
generally sit on *different* circles about `Oᵢ`, so exceptionality says nothing at all about the
angle they subtend. The measure route caps at two sets structurally (maximum independent sets in
`C₆` have size 3, so the density constant is exactly `½` and the proof never sees the angle). Both
of these are written up in the lane README §8, along with the routes I rejected.

Also unresolved: whether two *non*-wedge exceptional points can coexist. I did not try to construct
a double-tipped channel; radial monotonicity about two different points at once is the obstruction
and it looks hard, which is a hunch and not a result.

---

## Appendix A — the second, independent decider (full source)

Own `Q(√3)` arithmetic; decision by Cramer's rule per ordered edge pair rather than by a
segment-intersection routine. Shares no code with `experiments/inscribed-triangle-polygons/geom.py`.

```python
"""Independent exact decider, written from scratch for this lane.

Arithmetic: own Q(sqrt3) as pairs of Fractions (a,b) meaning a + b*sqrt3.
Method: for every ordered pair of edges (e,f), solve the LINEAR SYSTEM
    rho(A + t(B-A)) = C + u(D-C),   t,u in [0,1]
by Cramer's rule, instead of running a segment-intersection routine.
Parallel/degenerate cases handled separately.  Shares no code with geom.py.
"""
from fractions import Fraction as F

class Q3(tuple):
    __slots__ = ()
    def __new__(cls, a=0, b=0): return tuple.__new__(cls, (F(a), F(b)))
    def __add__(s,o): o=q(o); return Q3(s[0]+o[0], s[1]+o[1])
    __radd__=__add__
    def __neg__(s): return Q3(-s[0], -s[1])
    def __sub__(s,o): o=q(o); return Q3(s[0]-o[0], s[1]-o[1])
    def __rsub__(s,o): return q(o).__sub__(s)
    def __mul__(s,o):
        o=q(o); return Q3(s[0]*o[0] + 3*s[1]*o[1], s[0]*o[1] + s[1]*o[0])
    __rmul__=__mul__
    def inv(s):
        d = s[0]*s[0] - 3*s[1]*s[1]
        assert d != 0
        return Q3(s[0]/d, -s[1]/d)
    def __truediv__(s,o): return s*q(o).inv()
    def iszero(s): return s[0]==0 and s[1]==0
    def sign(s):
        a,b = s
        if a==0 and b==0: return 0
        if a>=0 and b>=0: return 1
        if a<=0 and b<=0: return -1
        # opposite signs: compare a^2 vs 3b^2
        d = a*a - 3*b*b
        assert d != 0, "a^2 = 3b^2 impossible for a,b != 0"
        return (1 if a>0 else -1) if d>0 else (1 if b>0 else -1)
    def __lt__(s,o): return (s-q(o)).sign() < 0
    def __le__(s,o): return (s-q(o)).sign() <= 0
    def __gt__(s,o): return (s-q(o)).sign() > 0
    def __ge__(s,o): return (s-q(o)).sign() >= 0
    def __eq__(s,o): return (s-q(o)).iszero()
    def __hash__(s): return tuple.__hash__(s)

def q(x):
    return x if isinstance(x, Q3) else Q3(x, 0)

HALF = Q3(F(1,2), 0)
S3H  = Q3(0, F(1,2))        # sqrt3/2

def rot(p, O, sigma):
    """rotate p about O by sigma*60 degrees; sigma = +1/-1"""
    x = p[0]-O[0]; y = p[1]-O[1]
    c = HALF; s = S3H if sigma > 0 else -S3H
    return (O[0] + c*x - s*y, O[1] + s*x + c*y)

def sub(a,b): return (a[0]-b[0], a[1]-b[1])
def cross(u,v): return u[0]*v[1] - u[1]*v[0]
def dot(u,v): return u[0]*v[0] + u[1]*v[1]
def eqp(a,b): return a[0]==b[0] and a[1]==b[1]

def on_seg(X, A, B):
    if not cross(sub(B,A), sub(X,A)).iszero(): return False
    d = dot(sub(B,A), sub(B,A))
    t = dot(sub(X,A), sub(B,A))
    return t >= Q3(0) and t <= d

def pair_hits(A,B,C,D,O):
    """return a point in seg(A,B) cap seg(C,D) different from O, or None."""
    u = sub(B,A); v = sub(D,C); den = cross(u,v)
    if not den.iszero():
        w = sub(C,A)
        t = cross(w,v)/den
        s = cross(w,u)/den
        if t < Q3(0) or t > Q3(1) or s < Q3(0) or s > Q3(1): return None
        X = (A[0]+t*u[0], A[1]+t*u[1])
        return None if eqp(X,O) else X
    # parallel
    if not cross(u, sub(C,A)).iszero(): return None      # parallel, distinct lines
    # collinear: intersect parameter intervals along u (u != 0 for a real edge)
    if u[0].iszero() and u[1].iszero():
        return None if eqp(A,O) or not on_seg(A,C,D) else A
    d2 = dot(u,u)
    tc = dot(sub(C,A),u)/d2; td = dot(sub(D,A),u)/d2
    lo = tc if tc <= td else td
    hi = td if tc <= td else tc
    lo = lo if lo > Q3(0) else Q3(0)
    hi = hi if hi < Q3(1) else Q3(1)
    if lo > hi: return None
    for t in (lo, hi, (lo+hi)*HALF):
        X = (A[0]+t*u[0], A[1]+t*u[1])
        if not eqp(X,O): return X
    return None

def good(poly, O):
    n = len(poly); E = [(poly[i], poly[(i+1)%n]) for i in range(n)]
    for sigma in (1,-1):
        for (A,B) in E:
            RA, RB = rot(A,O,sigma), rot(B,O,sigma)
            for (C,D) in E:
                X = pair_hits(RA,RB,C,D,O)
                if X is not None:
                    Qp = rot(X,O,-sigma)
                    d1 = dot(sub(Qp,O),sub(Qp,O)); d2 = dot(sub(X,O),sub(X,O))
                    d3 = dot(sub(X,Qp),sub(X,Qp))
                    assert d1==d2==d3 and d1.sign()>0, "not equilateral!"
                    assert any(on_seg(P_,*e) for e in E for P_ in [Qp]) and \
                           any(on_seg(X,*e) for e in E), "witness off curve"
                    return True, (Qp, X, d1)
    return False, None
```

## Appendix B — the hunts (full source)

```python
"""Hunt for a simple polygon with >= 3 exceptional vertices.
Uses the committed exact decider (read/run only)."""
import sys, random, json, time
from fractions import Fraction as F
sys.path.insert(0,"/home/user/clanker-solving-riemman-hypothesis-inator/experiments/inscribed-triangle-polygons")
from k3 import K
from geom import P, decide_good, is_simple, vertex_angle_class

SEED = 20260829
random.seed(SEED)

def star_polygon(n, M=60, squash=None):
    pts = set()
    while len(pts) < n:
        x = F(random.randint(-M, M)); y = F(random.randint(-M, M))
        if (x, y) != (0, 0): pts.add((x, y))
    pts = list(pts)
    def ang_key(p):
        x,y = p
        half = 0 if (y > 0 or (y == 0 and x > 0)) else 1
        return (half, p)
    def cmp(a, b):
        ha, hb = ang_key(a)[0], ang_key(b)[0]
        if ha != hb: return -1 if ha < hb else 1
        cr = a[0]*b[1] - a[1]*b[0]
        if cr > 0: return -1
        if cr < 0: return 1
        return 0
    import functools
    pts.sort(key=functools.cmp_to_key(cmp))
    if squash is not None:
        pts = [(x, y/squash) for x, y in pts]
    return [P(x, y) for x, y in pts]

best = 0; found = []
t0 = time.time(); trials = 0; simple_cnt = 0
hist = {}
while time.time() - t0 < 100:
    trials += 1
    n = random.randint(5, 12)
    sq = random.choice([None, F(3), F(8), F(20), F(60)])
    poly = star_polygon(n, squash=sq)
    ok, why = is_simple(poly)
    if not ok: continue
    simple_cnt += 1
    exc = []
    for i, v in enumerate(poly):
        a = vertex_angle_class(poly, i)
        if a["cmp60"] >= 0:      # angle >= 60 -> good, by the reduction; verify cheaply sometimes
            continue
        r = decide_good(poly, v)
        if not r["good"]: exc.append(i)
    hist[len(exc)] = hist.get(len(exc), 0) + 1
    if len(exc) > best:
        best = len(exc)
        found = [(str(v[0]), str(v[1])) for v in poly]
        print("new best", best, "n=", n, "squash=", sq)
    if len(exc) >= 3:
        print("!!! THREE OR MORE:", [(str(v[0]),str(v[1])) for v in poly], exc)
        break
print("trials", trials, "simple", simple_cnt, "max exceptional", best)
print("histogram of #exceptional vertices:", hist)
json.dump({"seed":SEED,"trials":trials,"simple":simple_cnt,"best":best,"hist":{str(k):v for k,v in hist.items()},"best_poly":found}, open("hunt_star.json","w"), indent=1)
```

```python
"""Targeted hunt: thin multi-armed polygons ('stars' with deep notches), the natural
candidates for several simultaneous sharp tips.  Exact decider throughout."""
import sys, random, time, functools, json
from fractions import Fraction as F
sys.path.insert(0,"/home/user/clanker-solving-riemman-hypothesis-inator/experiments/inscribed-triangle-polygons")
from k3 import K
from geom import P, decide_good, is_simple, vertex_angle_class
random.seed(31415)

def thin_star(k, R=200, rho=6, squash=None):
    """k tips at large random integer points, k notches near the origin, interleaved by angle."""
    tips = [(F(random.randint(-R,R)), F(random.randint(-R,R))) for _ in range(k)]
    notch = [(F(random.randint(-rho,rho)), F(random.randint(-rho,rho))) for _ in range(k)]
    pts = tips + notch
    def half(p): return 0 if (p[1]>0 or (p[1]==0 and p[0]>0)) else 1
    def cmp(a,b):
        if half(a)!=half(b): return -1 if half(a)<half(b) else 1
        cr=a[0]*b[1]-a[1]*b[0]
        return -1 if cr>0 else (1 if cr<0 else 0)
    tips.sort(key=functools.cmp_to_key(cmp)); notch.sort(key=functools.cmp_to_key(cmp))
    out=[]
    for i in range(k):
        out.append(tips[i]); out.append(notch[i])
    if squash is not None: out=[(x,y/squash) for x,y in out]
    return [P(x,y) for x,y in out]

best=0; hist={}; simple=0; trials=0; t0=time.time(); bestpoly=None
while time.time()-t0 < 90:
    trials+=1
    k=random.choice([3,3,3,4,4,5])
    poly=thin_star(k, squash=random.choice([None,None,F(4),F(15),F(50)]))
    if not is_simple(poly)[0]: continue
    simple+=1
    exc=[]
    for i,v in enumerate(poly):
        if vertex_angle_class(poly,i)["cmp60"]>=0: continue
        if not decide_good(poly,v)["good"]: exc.append(i)
    hist[len(exc)]=hist.get(len(exc),0)+1
    if len(exc)>best:
        best=len(exc); bestpoly=[(str(v[0]),str(v[1])) for v in poly]
        print("new best",best,"k=",k)
    if len(exc)>=3:
        print("!!! >=3 EXCEPTIONAL:",[(str(v[0]),str(v[1])) for v in poly],exc); break
print("trials",trials,"simple",simple,"best",best,"hist",hist)
print("best polygon:",bestpoly)
```

## Appendix C — polygon control on the reduction (full source)

```python
"""Polygon control on this lane's Theorem 1 (the reduction):
   (a) every vertex with interior angle >= 60 is good;
   (b) every sampled non-vertex boundary point is good."""
import sys, random, time, json
from fractions import Fraction as F
sys.path.insert(0,"/home/user/clanker-solving-riemman-hypothesis-inator/experiments/inscribed-triangle-polygons")
from k3 import K
from geom import P, decide_good, is_simple, vertex_angle_class, sample_edge_point
import functools
def star_polygon(n, M=60, squash=None):
    pts=set()
    while len(pts)<n:
        x=F(random.randint(-M,M)); y=F(random.randint(-M,M))
        if (x,y)!=(0,0): pts.add((x,y))
    pts=list(pts)
    def half(p): return 0 if (p[1]>0 or (p[1]==0 and p[0]>0)) else 1
    def cmp(a,b):
        if half(a)!=half(b): return -1 if half(a)<half(b) else 1
        cr=a[0]*b[1]-a[1]*b[0]
        return -1 if cr>0 else (1 if cr<0 else 0)
    pts.sort(key=functools.cmp_to_key(cmp))
    if squash is not None: pts=[(x,y/squash) for x,y in pts]
    return [P(x,y) for x,y in pts]
random.seed(4242)

nv_tested = nv_bad = 0
ne_tested = ne_bad = 0
t0=time.time(); polys=0
while time.time()-t0 < 70:
    poly = star_polygon(random.randint(5,10), squash=random.choice([None,F(3),F(12),F(40)]))
    if not is_simple(poly)[0]: continue
    polys += 1
    n=len(poly)
    for i,v in enumerate(poly):
        a=vertex_angle_class(poly,i)
        if a["cmp60"]>=0:
            ne_tested+=1
            if not decide_good(poly,v)["good"]:
                ne_bad+=1; print("VIOLATION angle>=60 not good", [(str(p[0]),str(p[1])) for p in poly], i)
    for i in range(n):
        for t in (F(1,3), F(1,2), F(4,7)):
            X = sample_edge_point(poly[i], poly[(i+1)%n], t)
            nv_tested+=1
            if not decide_good(poly,X)["good"]:
                nv_bad+=1; print("VIOLATION non-vertex not good", [(str(p[0]),str(p[1])) for p in poly], i, t)
print("polygons", polys)
print("vertices with angle>=60 tested:", ne_tested, "violations:", ne_bad)
print("non-vertex points tested:", nv_tested, "violations:", nv_bad)
```

## Appendix D — the tuning fork

```python
import sys
from fractions import Fraction as F
sys.path.insert(0,"/home/user/clanker-solving-riemman-hypothesis-inator/experiments/inscribed-triangle-polygons")
from k3 import K
from geom import P, decide_good, is_simple, vertex_angle_class
sys.path.insert(0,"/tmp/claude-0/-home-user-clanker-solving-riemman-hypothesis-inator/45689bea-431f-53e5-968e-24806e56ff25/scratchpad")
from indep import Q3, good as igood

# two-pronged fork: thin parallel prongs of length L, width 1, gap g, tips at y = 0
L, g = 400, 1
verts = [(0,0),(1,-L),(1+g,-L),(2+g,0),(3+g,-L-2),(-1,-L-2)]
poly=[P(F(x),F(y)) for x,y in verts]
print("simple:",is_simple(poly)[0])
ip=[(Q3(F(x),0),Q3(F(y),0)) for x,y in verts]
for i,v in enumerate(poly):
    a=vertex_angle_class(poly,i); r=decide_good(poly,v); ig=igood(ip, ip[i])[0]
    print("v%d %-12s angle=%9.5f good=%s indep=%s" % (i,str(verts[i]),a["degrees_display"],r["good"],ig))
```

---

## Appendix E — raw results

```
K1 controls (committed decider)
  equilateral      : v0 60.000000 good  v1 60.000000 good  v2 60.000000 good
  30-30-120        : v0 30.000000 NOT   v1 30.000000 NOT   v2 120.000000 good
  unit square      : all four 90.000000 good

witness (17-gon), committed decider
  simple: True
  v0  36.869898 NOT good      v1 116.565051 good     v2..v6 143.130102 good
  v7 206.565051 good          v8,v9 71.565051 good   v10 153.434949 good
  v11..v15 216.869898 good    v16 243.434949 good
  exceptional vertices: [0]
  independent decider: identical (exceptional vertices: [0])

exact rational checks behind the hand proof
  seg a1->a2 .. a6->a7 : |a|^2 doubles-and-quadruples as expected, dot(a, b-a) = (3/5)|a|^2 > 0
  seg a7->a8           : 4096 -> 16384, dot = 4096 > 0
  a8 = 2 a7            : True
  (9/10)|a8|^2 = 73728/5 >= |a7|^2 = 4096 : True
  angle(a1,a3)         : c = 28/25, s = 96/25, s^2 - 3c^2 = 6864/625 > 0  => > 60 degrees

polygon control on Theorem 1 (seed 4242, 70 s)
  polygons 746
  vertices with interior angle >= 60 tested: 4043   violations: 0
  non-vertex boundary points tested:        16749   violations: 0

hunt 1 — star-shaped random polygons (seed 20260829, 100 s)
  trials 3311, simple 3218, max exceptional 2
  histogram: {0: 571, 1: 849, 2: 1798}

hunt 2 — thin multi-armed polygons (seed 31415, 90 s)
  trials 13692, simple 2808, max exceptional 2
  histogram: {0: 31, 1: 370, 2: 2407}

tuning fork (0,0),(1,-400),(2,-400),(3,0),(4,-402),(-1,-402)
  v0 0.28577  good (both deciders)     v3 0.28577  good (both deciders)
  v1,v2 269.85676 good                 v4,v5 89.85747 good
```
