"""Finding 1: the '3 corner + 9 edge + 3 interior' layout is not forced.

(A) EXACT WITNESS that a piece meeting two sides can also meet a side's MIDDLE,
    which is the step used to exclude n2 = 6 (and, in n16-verification-3 sec.7,
    certified as correct).
(B) The repair: n_int <= 3 unconditionally, by counting CORNER-CONTAINING pieces
    out of the middles rather than all two-side pieces.
(C) The admissible layouts that nothing in the campaign excludes.
"""
from fractions import Fraction as F

# ---------------------------------------------------------------- (A) witness
# Corner A at the origin, side AB along the x-axis, side AC at 60 degrees.
# Work with squared lengths, exactly.  A point at distance t from A along AC is
# (t/2, t*sqrt3/2); a point at distance s along AB is (s, 0).  Their squared
# distance is s^2 - s*t + t^2  (exact, rational for rational s, t).
def d2(s, t):
    return s * s - s * t + t * t

a = F(1) + 2 * F(17320508075688772935, 10 ** 19)   # a lower rational proxy for 1+2 sqrt3
alpha = F(21, 20)      # footpoint on AB, at distance 1.05 from A
beta = F(1, 2)         # footpoint on AC, at distance 0.5  from A
sq = d2(alpha, beta)
print("(A) witness: a two-side piece that reaches the middle of AB")
print(f"    footpoints: alpha = {alpha} on AB, beta = {beta} on AC")
print(f"    squared distance = {sq} = {float(sq):.10f}")
print(f"    distance         = {float(sq) ** 0.5:.10f}   < 1 : {sq < 1}")
print(f"    alpha > 1 (so the AB footpoint is in the middle m_AB) : {alpha > 1}")
print(f"    a - alpha > 1 (ditto, from the far end)               : {a - alpha > 1}")
assert sq < 1 and alpha > 1 and a - alpha > 1
print("    => M_AB contains a piece that meets BOTH sides.  The claim that the")
print("       >=3 pieces covering a middle are all ONE-side pieces is FALSE.")

# the whole admissible beta-interval at this alpha, exactly: beta^2 - alpha*beta + alpha^2 - 1 < 0
disc = 4 - 3 * alpha * alpha
lo = (alpha - F(str(float(disc) ** 0.5))[0:1] if False else None)
import math
b1 = (float(alpha) - math.sqrt(float(disc))) / 2
b2 = (float(alpha) + math.sqrt(float(disc))) / 2
print(f"    (admissible beta at alpha = {float(alpha)}: ({b1:.6f}, {b2:.6f}) -- nonempty)")

# ---------------------------------------------------------------- (B) repair
print()
print("(B) the repair.  For 4 < a < 5 and 15 pieces of diameter < 1 covering T_a:")
print("    |M_e| >= 3 for each side (a middle of length a-2 > 2, traces of length < 1)")
print("    M_e pairwise disjoint  (min of sqrt(s^2-st+t^2) on s,t >= 1 is 1, at (1,1))")
print("    a piece containing a corner V lies in B(V,1), hence in no M_e; there are >= 3")
print("    => 9 <= |union M_e| <= n1 + (n2 - 3)   =>   n1 + n2 >= 12   =>   n_int <= 3")
print("    and n_int >= 1 (the incentre is at a/(2 sqrt3) = %.4f > 1 from every side)"
      % (float(a) / (2 * math.sqrt(3))))

# ------------------------------------------------------- (C) admissible layouts
print()
print("(C) layouts consistent with EVERYTHING proved (n1+n2+nint=15, n1+2n2>=15,")
print("    n1+n2>=12, n2>=3, 1<=nint<=3, and n1 >= 12-n2 from the middles):")
ok = []
for n2 in range(3, 16):
    for nint in range(1, 4):
        n1 = 15 - n2 - nint
        if n1 < 0:
            continue
        if n1 + 2 * n2 >= 15 and n1 + n2 >= 12 and n1 >= 12 - n2:
            ok.append((n1, n2, nint))
for t in ok:
    mark = "   <-- the layout claimed 'forced'" if t == (9, 3, 3) else ""
    print("    (n1, n2, n_int) = %s%s" % (str(t), mark))
print("    %d layouts survive; exactly one of them is 3+9+3." % len(ok))
