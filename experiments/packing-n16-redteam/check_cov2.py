"""
Red-team independent check of the n16-covering-2 headline certificate.

Polygons transcribed BY HAND from attacks/n16-covering-2/README.md's table
(not from the author's exact_1p2r3.py).  Triangular basis e1=(1,0),
e2=(1/2,sqrt3/2);  |u e1 + v e2|^2 = u^2+uv+v^2  (rational-in-Q(sqrt3)).
T_a = {u>=0, v>=0, u+v<=a},  a = 1+2 sqrt3.
"""
import sys, itertools
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/',1)[0])
from q3 import Q3, q3, R

r = R
a = q3(1) + 2*r
third = F(1,3)

def V(*pairs): return [(q3(u) if not isinstance(u,Q3) else u, q3(v) if not isinstance(v,Q3) else v) for u,v in pairs]

r3 = r*third          # r/3
r43 = 4*r*third       # 4r/3
FACES = [
 V((0,0),(1,0),(r3,r3),(0,1)),
 V((r3, q3(1)+r3),(0,r),(0,1),(r3,r3),(1,1)),
 V((r3, r43),(0,q3(1)+r),(0,r),(r3,q3(1)+r3),(1,r)),
 V((r3, q3(1)+r43),(0,2*r),(0,q3(1)+r),(r3,r43),(1,F(5,2))),
 V((1,2*r),(0,q3(1)+2*r),(0,2*r),(r3,q3(1)+r43)),
 V((1,0),(r,0),(q3(1)+r3,r3),(1,1),(r3,r3)),
 V((F(3,2),F(3,2)),(1,r),(r3,q3(1)+r3),(1,1),(q3(1)+r3,r3),(r,1)),
 V((q3(1)+r3,r43),(1,F(5,2)),(r3,r43),(1,r),(F(3,2),F(3,2)),(r,r)),
 V((r,q3(1)+r),(1,2*r),(r3,q3(1)+r43),(1,F(5,2)),(q3(1)+r3,r43)),
 V((r,0),(q3(1)+r,0),(r43,r3),(r,1),(q3(1)+r3,r3)),
 V((r43,q3(1)+r3),(r,r),(F(3,2),F(3,2)),(r,1),(r43,r3),(F(5,2),1)),
 V((q3(1)+r,r),(r,q3(1)+r),(q3(1)+r3,r43),(r,r),(r43,q3(1)+r3)),
 V((q3(1)+r,0),(2*r,0),(q3(1)+r43,r3),(F(5,2),1),(r43,r3)),
 V((2*r,1),(q3(1)+r,r),(r43,q3(1)+r3),(F(5,2),1),(q3(1)+r43,r3)),
 V((2*r,0),(q3(1)+2*r,0),(2*r,1),(q3(1)+r43,r3)),
]

def sq(du,dv): return du*du + du*dv + dv*dv     # squared euclidean length

def cross(o,p,qq):
    return (p[0]-o[0])*(qq[1]-o[1]) - (p[1]-o[1])*(qq[0]-o[0])

def shoelace2(poly):   # 2*signed area in uv coords
    s = q3(0)
    n = len(poly)
    for i in range(n):
        x1,y1 = poly[i]; x2,y2 = poly[(i+1)%n]
        s = s + (x1*y2 - x2*y1)
    return s

fails = []
def chk(cond, msg):
    if not cond: fails.append(msg)

chk(len(FACES)==15, "piece count != 15")

# 1. containment
for i,P in enumerate(FACES):
    for (u,v) in P:
        chk(u>=q3(0) and v>=q3(0) and (u+v)<=a, f"face {i}: vertex outside T_a")

# 2. strict convexity + ccw orientation
for i,P in enumerate(FACES):
    n=len(P); signs=set()
    for k in range(n):
        c = cross(P[k],P[(k+1)%n],P[(k+2)%n]).sign()
        signs.add(c)
    chk(signs=={1}, f"face {i}: not strictly convex ccw, signs={signs}")

# 3. squared diameters
maxsq = q3(0); argmax=None
persq = []
for i,P in enumerate(FACES):
    m = q3(0)
    for A,B in itertools.combinations(P,2):
        d = sq(A[0]-B[0], A[1]-B[1])
        if d > m: m = d
    persq.append(m)
    if m > maxsq: maxsq, argmax = m, i
print("per-face max squared diameters:", [str(x) for x in persq])
print("max squared diameter =", maxsq, "=", float(maxsq), " (face", argmax, ")")
chk(maxsq == q3(1), "max squared diameter is not exactly 1")
chk(all(x<=q3(1) for x in persq), "some face exceeds squared diameter 1")

# 4. area identity
tot = q3(0)
for P in FACES: tot = tot + shoelace2(P)
tri2 = a*a          # 2*area of T_a in uv-shoelace units
print("sum 2*shoelace areas =", tot, " a^2 =", tri2)
chk(tot == tri2, "areas do not sum to area(T_a)")

# 5. pairwise interior disjointness by exact convex clipping
def clip(subject, cl_a, cl_b):
    """Sutherland-Hodgman: keep the part of `subject` left of directed edge cl_a->cl_b."""
    out=[]; n=len(subject)
    for i in range(n):
        cur=subject[i]; nxt=subject[(i+1)%n]
        s_cur = cross(cl_a, cl_b, cur).sign()
        s_nxt = cross(cl_a, cl_b, nxt).sign()
        if s_cur >= 0: out.append(cur)
        if (s_cur>0 and s_nxt<0) or (s_cur<0 and s_nxt>0):
            # intersection point
            d1 = cross(cl_a, cl_b, cur); d2 = cross(cl_a, cl_b, nxt)
            t = d1/(d1-d2)
            out.append((cur[0] + t*(nxt[0]-cur[0]), cur[1] + t*(nxt[1]-cur[1])))
    return out

def inter_area2(P,Q):
    s = P[:]
    n=len(Q)
    for i in range(n):
        if not s: return q3(0)
        s = clip(s, Q[i], Q[(i+1)%n])
    if len(s)<3: return q3(0)
    return shoelace2(s)

bad=0
for i,j in itertools.combinations(range(15),2):
    A = inter_area2(FACES[i],FACES[j])
    if not (A == q3(0)):
        bad+=1; fails.append(f"faces {i},{j} overlap, 2*area={A}")
print("overlapping pairs:", bad, "of 105")

# 6. grid probe of coverage (rational offsets, independent of area identity)
def inside(P, pt):
    n=len(P)
    for k in range(n):
        if cross(P[k],P[(k+1)%n],pt).sign() < 0: return False
    return True
N=60
miss=0; tested=0
for i in range(N+1):
    for j in range(N+1-i):
        u = a*F(3*i+1, 3*N+2); v = a*F(3*j+1, 3*N+2)
        if (u+v) > a: continue
        tested+=1
        if not any(inside(P,(u,v)) for P in FACES):
            miss+=1
            if miss<4: fails.append(f"uncovered probe point {float(u)},{float(v)}")
print(f"grid probe: {tested} points, {miss} uncovered")

print()
if fails:
    print("FAILURES:")
    for f in fails[:20]: print("  -", f)
    sys.exit(1)
print("ALL CHECKS PASS: 15 strictly convex pieces, in T_a, pairwise interior-disjoint,")
print("areas sum exactly to area(T_a), max squared diameter EXACTLY 1, no probe hole.")
