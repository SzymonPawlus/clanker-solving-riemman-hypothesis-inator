"""The 6 symmetries of the fixed triangle A=(0,0), B=(d,0), C=(d/2, d*sqrt3/2),
built exactly in Q(sqrt 3) as the affine maps permuting {A,B,C}.
(Each such map is an isometry of the equilateral triangle, so it maps any valid
packing to a valid packing with the same s.  RULES.md forbids CHECKERS from
searching over rigid motions; that is a rule about certificate validity, not a
statement that two symmetry-related configurations are different packings.)
"""
from fractions import Fraction as F
from itertools import permutations
from q3 import Q3, mat_inv2, mat_vec


def verts(d):
    return [(Q3(0), Q3(0)), (d, Q3(0)), (d * Q3(F(1, 2)), d * Q3(0, F(1, 2)))]


def maps(d):
    """Yield (name, f) for the 6 vertex permutations."""
    V = verts(d)
    A, B, C = V
    base = ((B[0] - A[0], C[0] - A[0]), (B[1] - A[1], C[1] - A[1]))
    binv = mat_inv2(base)
    out = []
    for perm in permutations(range(3)):
        Ap, Bp, Cp = V[perm[0]], V[perm[1]], V[perm[2]]
        tgt = ((Bp[0] - Ap[0], Cp[0] - Ap[0]), (Bp[1] - Ap[1], Cp[1] - Ap[1]))
        M = ((tgt[0][0] * binv[0][0] + tgt[0][1] * binv[1][0],
              tgt[0][0] * binv[0][1] + tgt[0][1] * binv[1][1]),
             (tgt[1][0] * binv[0][0] + tgt[1][1] * binv[1][0],
              tgt[1][0] * binv[0][1] + tgt[1][1] * binv[1][1]))
        t = Ap

        def f(p, M=M, t=t):
            v = mat_vec(M, p)
            return (v[0] + t[0], v[1] + t[1])

        # determinant tells rotation (+1) from reflection (-1)
        det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
        kind = "rot" if det == Q3(1) else "refl"
        out.append(("%s A->%s B->%s C->%s" % (kind, "ABC"[perm[0]], "ABC"[perm[1]], "ABC"[perm[2]]), f))
    return out
