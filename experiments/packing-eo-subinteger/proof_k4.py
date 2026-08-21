"""Independent re-check of the k=4 certificate, separate from the LP pipeline.

Claim: 9 points at mutual distance >= 1 do not fit in a closed equilateral
triangle of side a < 3   (Erdos-Oler at k=4; equivalently d(9)=6, s(9)=6+2sqrt3;
`cited` in ../../README.md as Melissen 1993 -- this is a re-proof, status `sketch`).

Cover:  T_a  =  Delta_A(t) u Delta_B(t) u Delta_C(t) u H,   t = a/3,
        H = {u_A,u_B,u_C >= t}.
  * a point outside all three corner triangles has u_V > t for every V, so it is in H;
  * each Delta_V(t) is an equilateral triangle of side t = a/3 < 1: diameter < 1, so
    it holds at most 1 point of a separated set;
  * H is a regular hexagon of side t, circumradius t < 1, so by Lemma D it holds at
    most 5.
  Total <= 3*1 + 5 = 8 < 9.

Everything below is exact rational arithmetic; nothing here uses any d(n) value.
"""
from fractions import Fraction as F
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom

print("a          t=a/3   diam^2(corner)  hex sides           circumradius^2(H)   verdict")
ok = True
for num in list(range(1, 30)) + [299, 2999, 299999]:
    a = F(num, 10) if num < 30 else F(num, 10 ** len(str(num)) // 10 * 10 // 10)
    a = F(num, 10) if num < 30 else (F(299, 100) if num == 299 else F(2999, 1000) if num == 2999 else F(299999, 100000))
    if a >= 3:
        continue
    t = a / 3
    tot = 2 * a
    corner = geom.polygon(tot, [F(0), F(0), F(0)], [t, a, a])   # Delta_A(t)
    H = geom.polygon(tot, [t, t, t], [a, a, a])
    dc = geom.diam2(corner)
    sides = set()
    for i in range(len(H)):
        sides.add(geom.d2(H[i], H[(i + 1) % len(H)]))
    _, rho2 = geom._mec(H)
    good = (dc < 1) and (len(H) == 6) and (sides == {t * t}) and (rho2 == t * t) and (rho2 < 1)
    ok &= good
    print(f"{str(a):<10} {str(t):<7} {str(dc):<15} {'regular, side^2='+str(sides.pop()):<19} {str(rho2):<19} {'OK' if good else 'FAIL'}")
print()
print("all a tested: corner diameter < 1, H is a REGULAR hexagon of side a/3 with")
print("circumradius exactly a/3 < 1  ->  cap <= 3*1 + 5 = 8 < 9   [", "PASS" if ok else "FAIL", "]")
print()
print("Lemma D at m=6, restated and machine-checked on the tight case:")
print("  6 points pairwise >= 1 in a disk of radius rho: some angular gap <= 60 deg,")
print("  and for that pair |PQ|^2 = r_i^2 - r_i r_j + r_j^2 <= max(r_i,r_j)^2 <= rho^2.")
print("  So rho >= 1.  Tight: the regular hexagon inscribed in the unit circle.")
h = [(F(0), F(0))]
# regular hexagon of side 1 in the (v_A,v_C) chart: vertices of {v>=0,sum=3, v_V<=2}
hex1 = geom.polygon(F(3), [F(0)] * 3, [F(2)] * 3)
d = sorted(set(geom.d2(hex1[i], hex1[j]) for i in range(6) for j in range(i + 1, 6)))
print("  regular hexagon of side 1: pairwise squared distances =", [str(x) for x in d],
      "-> min distance 1, so 6 points DO fit at rho = 1 exactly")
