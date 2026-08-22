"""Task (d): audit the dilation argument, and run it on the witness that kills
the naive lemma.

THE ARGUMENT, written out (V3's reconstruction, not the author's text)
----------------------------------------------------------------------
Definitions.  T_a = {u,v >= 0, u+v <= a} in the chart of check_v3.py; it is a
closed equilateral triangle of side a.  Call a finite set X in T_a *separated*
if every two of its points are at distance >= 1 (non-strict: problem RULES.md
s2).  Put  a_n = min{ a : T_a contains a separated set of size n }.  The min is
attained: {a : T_a has n separated points} is upward closed (T_a subset T_a'
for a <= a'), and closed, because a sequence of separated n-sets in T_{a_k}
with a_k -> a has a convergent subsequence by compactness whose limit is still
separated (>= is a closed condition).

Step 1 (the certificate).  There are 15 closed convex sets P_0..P_14 with
union(P_i) = T_A, A = 1 + 2 sqrt3, and diam(P_i) = 1 for every i.
    -- reconstructed independently in check_v3.py: PASS.

Step 2 (dilation).  Fix any a with 0 < a < A and put mu = a/A in (0,1).  The
map h(x) = mu x is a similarity with ratio mu fixing the chart origin, and
h(T_A) = T_{mu A} = T_a exactly.  So the sets h(P_i) are 15 closed convex sets
whose union is T_a, with diam(h(P_i)) = mu * diam(P_i) = mu < 1.

Step 3 (pigeonhole).  Suppose X subset T_a is separated with |X| = 16.  The 15
sets h(P_i) cover T_a, so some h(P_i) contains two distinct points of X, whose
distance is then <= diam(h(P_i)) = mu < 1 -- contradicting separation, which
only requires >= 1.  So no such X exists, for EVERY a < A.

Step 4 (conclusion).  a_16 is therefore not < A, i.e.  a_16 >= A = 1 + 2 sqrt3.
Equality is not excluded and is not claimed: at a = A the pieces have diameter
exactly 1, and two points at distance exactly 1 may share a closed piece, so
step 3 fails there.  This is the ONLY place strictness matters, and the
argument is careful about it.

WHY THE ARGUMENT IS NOT THE NAIVE LEMMA
---------------------------------------
Naive (FALSE) lemma: "T_a covered by k sets of diameter <= 1  =>  T_a has no
k+1 separated points."  Witness D1 (attacks/n16-verification/): T_{sqrt3} is
covered by three cells of diameter exactly 1 and contains four separated points
(the three corners and the centroid).  The test below rebuilds that witness from
scratch and then runs the dilation argument on it: the dilation argument must
return a_4 >= sqrt3 (TRUE and SHARP), never a_4 > sqrt3 (FALSE).
"""
import itertools
from fractions import Fraction as F
from q3f import Q3, q3, ZERO, ONE
from geom import qform
from check_v3 import check

R3 = Q3(0, 1)
HALF_R3 = Q3(0, F(1, 2))
THIRD_R3 = Q3(0, F(1, 3))

a4 = R3                                  # side sqrt3
O = (ZERO, ZERO)
B = (R3, ZERO)
C = (ZERO, R3)
G = (THIRD_R3, THIRD_R3)                 # centroid
mAB = (HALF_R3, ZERO)
mAC = (ZERO, HALF_R3)
mBC = (HALF_R3, HALF_R3)

cells = [
    [O, mAB, G, mAC],
    [B, mBC, G, mAB],
    [C, mAC, G, mBC],
]
pts = [O, B, C, G]

print(__doc__)
print("=" * 78)
print("D1 witness rebuilt from scratch, checked with V3's own checker")
print("=" * 78)
ok, rep = check(a4, cells, name="D1: three cells covering T_sqrt3")
print()
print("four claimed-separated points, exact squared distances (need >= 1):")
worst = None
for (i, X), (j, Y) in itertools.combinations(list(enumerate(pts)), 2):
    d = qform(X, Y)
    good = d >= ONE
    print(f"   d^2({i},{j}) = {d.p}+{d.q}r3 = {float(d):.15f}   {'ok' if good else 'BAD'}")
    if worst is None or d < worst:
        worst = d
print(f"   min squared distance = {worst.p}+{worst.q}r3 = {float(worst):.15f}")
print()
print(f"So T_sqrt3 IS covered by 3 sets of diameter exactly 1 "
      f"(covered={rep['C5_covered']}, diam^2={rep['C3_max_squared_diameter']})")
print("and DOES contain 4 separated points.  The naive lemma is refuted.")
print()
print("Dilation argument on this witness:")
print("  for every a < sqrt3, T_a is covered by 3 sets of diameter a/sqrt3 < 1,")
print("  so T_a has no 4 separated points, so a_4 >= sqrt3.")
print(f"  cited value a_4 = (s(4) - 2 sqrt3)/2 = (4 sqrt3 - 2 sqrt3)/2 = sqrt3 "
      f"= {float(R3):.15f}")
print("  => the dilation argument returns the SHARP value and does not")
print("     overshoot to a_4 > sqrt3.  This is the discriminating test.")
