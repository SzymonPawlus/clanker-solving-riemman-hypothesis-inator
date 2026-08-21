"""EXACT certificate over Q(sqrt3) for the extremal configuration at a = 1 + 2*sqrt3.

The SLP optimiser (slp.py) converges, from six independently obtained starting
structures, to a subdivision of T_a into 15 convex pieces all of diameter exactly 1 at
    a = 1 + 2*sqrt(3) = 4.4641016151377...
Its boundary vertices divide every side of T_a as  1, sqrt3-1, 1, sqrt3-1, 1, and
27 of its 31 vertices sit at points of Q(sqrt3); the remaining 4 are RATTLERS (they move
freely without changing any diameter -- verified numerically, max-min slack 0.137), so
they are simply placed at convenient rational points here.

This file writes that configuration down exactly and verifies it in exact Q(sqrt3)
arithmetic.  Its max squared diameter is exactly 1, NOT less, so by itself it proves
nothing (see RULES.md section 2: separation is non-strict).  The bound comes from
dilating it:

    for every 0 < mu < 1 the dilation x -> mu*x maps this subdivision to a subdivision
    of T_{mu*(1+2 sqrt3)} into 15 convex pieces of diameter exactly mu < 1,

so no 16 points at pairwise distance >= 1 fit in T_a for ANY a < 1+2*sqrt3, and hence
    a_16 >= 1 + 2*sqrt(3),      s(16) >= 2*(1+2 sqrt3) + 2 sqrt3 = 2 + 6*sqrt(3).
"""
from fractions import Fraction as F
import math
from q3 import Q3
import verify_c1 as V

r3 = Q3(0, 1)
t = Q3(0, F(1, 3))                 # sqrt3/3
A = Q3(1, 2)                       # 1 + 2 sqrt3

P = {
    0:  (Q3(0), Q3(0)),                    30: (A, Q3(0)),        14: (Q3(0), A),
    1:  (Q3(1), Q3(0)),        15: (r3, Q3(0)),        22: (Q3(1, 1), Q3(0)),
    27: (Q3(0, 2), Q3(0)),
    3:  (Q3(0), Q3(1)),        5:  (Q3(0), r3),        8:  (Q3(0), Q3(1, 1)),
    11: (Q3(0), Q3(0, 2)),
    13: (Q3(1), Q3(0, 2)),     21: (r3, Q3(1, 1)),     26: (Q3(1, 1), r3),
    29: (Q3(0, 2), Q3(1)),
    2:  (t, t),                4:  (t, Q3(1, F(1, 3))),
    7:  (t, Q3(0, F(4, 3))),   10: (t, Q3(1, F(4, 3))),
    9:  (Q3(1), r3),           16: (Q3(1, F(1, 3)), t),
    18: (r3, Q3(1)),           19: (Q3(1, F(1, 3)), Q3(0, F(4, 3))),
    20: (r3, r3),              23: (Q3(0, F(4, 3)), t),
    24: (Q3(0, F(4, 3)), Q3(1, F(1, 3))),  28: (Q3(1, F(4, 3)), t),
    # the four rattlers, put at convenient rational points inside their free region
    6:  (Q3(1), Q3(1)),        12: (Q3(1), Q3(F(5, 2))),
    17: (Q3(F(3, 2)), Q3(F(3, 2))),        25: (Q3(F(5, 2)), Q3(1)),
}

FACES = [[0, 1, 2, 3], [4, 5, 3, 2, 6], [7, 8, 5, 4, 9], [10, 11, 8, 7, 12],
         [13, 14, 11, 10], [1, 15, 16, 6, 2], [17, 9, 4, 6, 16, 18],
         [19, 12, 7, 9, 17, 20], [21, 13, 10, 12, 19], [15, 22, 23, 18, 16],
         [24, 20, 17, 18, 23, 25], [26, 21, 19, 20, 24], [22, 27, 28, 25, 23],
         [29, 26, 24, 25, 28], [27, 30, 29, 28]]

if __name__ == "__main__":
    faces = [[P[k] for k in f] for f in FACES]
    print(__doc__.split("\n\n")[0])
    print()
    ok, worst = V.check(A, faces, do_cover=True, verbose=True, strict=False)
    print()
    print("  max squared diameter is EXACTLY 1 : %s" % (worst == 1))
    print("  (so this configuration alone certifies nothing; the bound is the dilation limit)")
    if ok and worst <= 1:
        print()
        print("  => for every a < 1 + 2*sqrt3, T_a is covered by 15 convex pieces of")
        print("     diameter < 1, hence holds no 16 points at pairwise distance >= 1.")
        print("  => a_16 >= 1 + 2*sqrt(3)  = %.15f" % (1 + 2 * math.sqrt(3)))
        print("  => s(16) >= 2 + 6*sqrt(3) = %.15f" % (2 + 6 * math.sqrt(3)))
