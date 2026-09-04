"""
The Jump Lemma, made quantitative from the `cited` table in the problem README.

a(n) = d(n)/2 = smallest side of an equilateral triangle (separation-1 scale) holding n points.
N(a) = max{n : a(n) <= a} is the true counting function.  A jump of N at a of size J means
J values of n share the same a(n).

Claim under test:  N jumps by 2 exactly at a = k-1 (the Delta(k)-1 family) and by 1 elsewhere,
in the proven range.  This is what makes continuous bounds provably unable to close Delta(k)-1
while leaving them viable everywhere else.
"""
import math
from collections import defaultdict

SQ3 = math.sqrt(3.0)
# s(n) from the problem README table, n <= 15 plus n=20,21 (all `cited`).  a(n) = (s(n)-2sqrt3)/2.
s = {
 1: 2*SQ3,
 2: 2 + 2*SQ3,
 3: 2 + 2*SQ3,
 4: 4*SQ3,
 5: 4 + 2*SQ3,
 6: 4 + 2*SQ3,
 7: 2 + 4*SQ3,
 8: 2 + 2*SQ3 + 2*math.sqrt(33)/3,
 9: 6 + 2*SQ3,
 10: 6 + 2*SQ3,
 11: 4 + 2*SQ3 + 4*math.sqrt(6)/3,
 12: 4 + 4*SQ3,
 13: 4 + 2*math.sqrt(6)/3 + 10*SQ3/3,
 14: 8 + 2*SQ3,
 15: 8 + 2*SQ3,
 20: 10 + 2*SQ3,
 21: 10 + 2*SQ3,
}
a = {n: (v - 2*SQ3)/2 for n, v in s.items()}

def tri(k): return k*(k+1)//2

print("n   s(n)        d(n)=2a      a(n)")
for n in sorted(a): print(f"{n:2d}  {s[n]:10.6f}  {2*a[n]:10.6f}  {a[n]:10.6f}")
print()

groups = defaultdict(list)
for n, v in a.items():
    groups[round(v, 9)].append(n)
print("jump structure of N (values of a where several n share the same a(n)):")
tri_set = {tri(k) for k in range(2, 9)}
for v in sorted(groups):
    ns = sorted(groups[v])
    tag = ""
    if len(ns) >= 2:
        top = max(ns)
        if top in tri_set:
            k = next(k for k in range(2, 9) if tri(k) == top)
            tag = f"   <-- Delta({k})={top}, a = k-1 = {k-1}"
    print(f"  a = {v:10.6f}   jump size {len(ns)}   n in {ns}{tag}")
print()
print("So: jump 2 exactly at the triangular a = k-1 (n = Delta(k)-1 and Delta(k)); jump 1 elsewhere.")
print()
print("JUMP LEMMA.  Any valid bound B(a) >= N(a) satisfies B(k-1) >= Delta(k) (lattice witness).")
print("A proof of EO(k) needs B(a) < Delta(k)-1 for a < k-1, i.e. a LEFT jump of size > 1 at k-1.")
print("If B is left-continuous at k-1 it cannot: liminf_{a->(k-1)-} B(a) = B(k-1) >= Delta(k).")
print("At an n with jump size 1 (all other n) a continuous B can be sharp -- no obstruction.")
