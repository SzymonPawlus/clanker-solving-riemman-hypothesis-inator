"""Validate the checker on solved instances BEFORE using it on anything, plus
negative controls (a checker that accepts everything proves nothing)."""
from fractions import Fraction as F
from q3 import Q3
import checker as ck

R3 = Q3(0, 1)


def show(name, rep):
    print("%-28s ok=%-5s tight=%-5s minsq=%-10s contacts=%-3d bdry=%-3d d_min=%s"
          % (name, rep["ok"], rep["tight"], rep["min_sq_distance"],
             rep["n_contacts"], rep["n_boundary"], rep["d_min"]))
    for f in rep["failures"][:4]:
        print("      FAIL:", f)


# n = 3, d = 2, s = 2 + 2 sqrt3   (the three corners)  -- proven optimum
pts3 = [(Q3(0), Q3(0)), (Q3(2), Q3(0)), (Q3(1), Q3(0, 1))]
show("n=3 corners (proven)", ck.check(pts3, Q3(2, 2), 3))

# n = 4, d = 2 sqrt3, s = 4 sqrt3 -- proven optimum: 3 corners + centroid
d4 = Q3(0, 2)
pts4 = [(Q3(0), Q3(0)), (d4, Q3(0)), (d4 * Q3(F(1, 2)), d4 * Q3(0, F(1, 2))),
        (d4 * Q3(F(1, 2)), d4 * Q3(0, F(1, 6)))]
show("n=4 (proven)", ck.check(pts4, Q3(0, 4), 4))

# n = 6, d = 4, s = 4 + 2 sqrt3 -- proven optimum: triangular lattice Delta(3)
pts6 = []
for r in range(3):
    for i in range(3 - r):
        pts6.append((Q3(2 * i + r), Q3(0, r)))
show("n=6 lattice (proven)", ck.check(pts6, Q3(4, 2), 6))

# n = 10, d = 6, s = 6 + 2 sqrt3 -- proven optimum Delta(4)
pts10 = []
for r in range(4):
    for i in range(4 - r):
        pts10.append((Q3(2 * i + r), Q3(0, r)))
show("n=10 lattice (proven)", ck.check(pts10, Q3(6, 2), 10))

print("--- negative controls ---")
bad = list(pts6)
bad[0] = (Q3(F(1, 100)), Q3(0))     # nudge -> overlap
show("NC1 overlap (expect ok=False)", ck.check(bad, Q3(4, 2), 6))
show("NC2 s inflated by 1 (expect ok=True, tight=False)", ck.check(pts6, Q3(5, 2), 6))
show("NC3 s deflated by 1 (expect ok=False)", ck.check(pts6, Q3(3, 2), 6))
out = list(pts6)
out[-1] = (Q3(0), Q3(-1))            # below AB
show("NC4 point outside (expect ok=False)", ck.check(out, Q3(4, 2), 6))
dup = list(pts6); dup[1] = dup[0]
show("NC5 duplicate point (expect ok=False)", ck.check(dup, Q3(4, 2), 6))
