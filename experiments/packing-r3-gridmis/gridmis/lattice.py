"""Exact construction of the grid-rounding conflict graph G(n, d, g).

All soundness-critical arithmetic is exact: integers and ``fractions.Fraction``.
No floating point is used anywhere in this module except in ``__repr__``-style
reporting helpers, which are clearly marked.

Geometry conventions (problems/circle-packing-equilateral-triangle/RULES.md §2):

    A = (0, 0),  B = (d, 0),  C = (d/2, d*sqrt(3)/2)

    T_d = { (x,y) :  y >= 0,
                     sqrt(3)*x - y >= 0,
                     sqrt(3)*(d-x) - y >= 0 }

Lattice.  The triangular lattice of spacing ``g`` anchored at the origin,

    L = { i*(g, 0) + j*(g/2, g*sqrt(3)/2) : i, j in Z }.

We index a lattice point by the integer pair ``(a, j)`` with ``a = 2i + j``
(so ``a = j (mod 2)``), giving

    x = g*a/2,      y = g*j*sqrt(3)/2.

Then x is rational and y is (rational)*sqrt(3), so every squared distance
between lattice points is rational:

    |v - v'|^2 = (g^2/4) * ( da^2 + 3*dj^2 ).

That is what makes every comparison below exact.
"""

from fractions import Fraction
from math import isqrt

__all__ = [
    "covering_radius_bound",
    "LatticeGraph",
    "build_graph",
]


def covering_radius_bound(g: Fraction, prec: int = 10 ** 12) -> Fraction:
    """Smallest multiple of 1/prec that is >= g/sqrt(3).

    ``g/sqrt(3)`` is the covering radius of the triangular lattice of spacing
    ``g`` (the circumradius of a lattice cell, an equilateral triangle of side
    ``g``).  We need a *rational upper bound* r >= g/sqrt(3); using a larger r
    only weakens the conclusion, never breaks soundness, so rounding up is safe.

    m/prec >= g/sqrt(3) = g*sqrt(3)/3  <=>  3*m*q >= prec*p*sqrt(3)   (g = p/q)
                                       <=>  (3*m*q)^2 >= 3*prec^2*p^2
    """
    assert g > 0
    p, q = g.numerator, g.denominator
    target = 3 * prec * prec * p * p          # want (3*m*q)^2 >= target
    root = isqrt(target)
    if root * root < target:
        root += 1                              # ceil(sqrt(target))
    m = -((-root) // (3 * q))                  # ceil(root / (3q))
    r = Fraction(m, prec)
    assert 3 * r * r >= g * g, "rational covering-radius bound failed"
    return r


class LatticeGraph:
    """The finite graph G(d, g) of Lemma 1.

    Vertices: lattice points (a, j) lying in the r-relaxed triangle
              T_d^{(r)} = { y >= -r, sqrt(3)x - y >= -2r, sqrt(3)(d-x) - y >= -2r },
              which is exactly the concentric equilateral triangle of side
              d + 2*sqrt(3)*r.
    Edges:    pairs at Euclidean distance strictly less than rho = 2 - 2r.
    """

    def __init__(self, d: Fraction, g: Fraction, r: Fraction):
        assert d > 0 and g > 0 and r > 0
        assert 3 * r * r >= g * g, "r must be >= g/sqrt(3)"
        self.d, self.g, self.r = d, g, r
        self.rho = 2 - 2 * r
        assert self.rho > 0, "need g < sqrt(3) so that snapping stays injective"
        self.verts = []          # list of (a, j)
        self.index = {}          # (a, j) -> position
        self.adj = []            # list of int bitmasks
        self.offsets = []        # edge offsets (da, dj)
        self.K = Fraction(4) * self.rho * self.rho / (self.g * self.g)
        self.Qmax = None         # largest integer Q with Q < K   (effective cut)
        self._build_vertices()
        self._build_edges()

    # -- containment tests, all exact -----------------------------------
    def _in_relaxed(self, a: int, j: int) -> bool:
        g, r, d = self.g, self.r, self.d
        # (1)  y >= -r   with y = g*j*sqrt(3)/2
        if j < 0:
            if 3 * g * g * j * j > 4 * r * r:
                return False
        # (2)  sqrt(3)*g*(a - j) >= -4r
        if a < j:
            m = j - a
            if 3 * g * g * m * m > 16 * r * r:
                return False
        # (3)  sqrt(3)*t >= -2r  with t = d - g*(a+j)/2
        t = d - g * (a + j) / 2
        if t < 0:
            if 3 * t * t > 4 * r * r:
                return False
        return True

    def _build_vertices(self):
        d, g, r = self.d, self.g, self.r
        # generous integer ranges; the exact test above does the real filtering
        jmax = int(d / g) + int(4 * r / g) + 4
        jmin = -(int(2 * r / g) + 4)
        amin = -(int(2 * r / g) + 4)
        amax = 2 * int((d + 2 * r) / g) + 4
        for j in range(jmin, jmax + 1):
            for a in range(amin + ((amin ^ j) & 1), amax + 1, 2):
                if (a - j) % 2 != 0:
                    continue
                if self._in_relaxed(a, j):
                    self.index[(a, j)] = len(self.verts)
                    self.verts.append((a, j))

    def _build_edges(self):
        # da^2 + 3*dj^2 < K  with K = 4*rho^2/g^2 ; LHS is a non-negative integer
        K = self.K
        Qmax = K.numerator // K.denominator
        if Fraction(Qmax) >= K:
            Qmax -= 1
        self.Qmax = Qmax
        offs = []
        djlim = isqrt(max(Qmax, 0) // 3) + 1
        for dj in range(-djlim, djlim + 1):
            rem = Qmax - 3 * dj * dj
            if rem < 0:
                continue
            dalim = isqrt(rem)
            for da in range(-dalim, dalim + 1):
                if (da - dj) % 2 != 0:
                    continue
                if da == 0 and dj == 0:
                    continue
                if da * da + 3 * dj * dj <= Qmax:
                    offs.append((da, dj))
        self.offsets = offs
        n = len(self.verts)
        adj = [0] * n
        idx = self.index
        for p, (a, j) in enumerate(self.verts):
            m = 0
            for (da, dj) in offs:
                q = idx.get((a + da, j + dj))
                if q is not None:
                    m |= 1 << q
            adj[p] = m
        self.adj = adj
        # symmetry sanity check (cheap, catches indexing bugs)
        for p in range(n):
            mm = adj[p]
            while mm:
                b = mm & -mm
                qq = b.bit_length() - 1
                assert adj[qq] >> p & 1, "adjacency not symmetric"
                mm ^= b

    # -- reporting ------------------------------------------------------
    @property
    def n_vertices(self):
        return len(self.verts)

    @property
    def n_edges(self):
        return sum(bin(m).count("1") for m in self.adj) // 2

    def rho_eff_sq(self) -> Fraction:
        """Exact rho_eff^2, where rho_eff is the *effective* separation.

        Non-adjacency means da^2 + 3dj^2 > Qmax, i.e. >= Qnext, the smallest
        integer > Qmax representable as da^2+3dj^2 with da = dj (mod 2).
        So independent sets are lattice sets with pairwise distance >= rho_eff
        = (g/2)*sqrt(Qnext) >= rho.  This is a free tightening of the lemma.
        """
        Q = self.Qmax + 1
        while True:
            ok = False
            djlim = isqrt(Q // 3) + 1
            for dj in range(0, djlim + 1):
                rem = Q - 3 * dj * dj
                if rem < 0:
                    continue
                s = isqrt(rem)
                if s * s == rem and (s - dj) % 2 == 0 and (s or dj):
                    ok = True
                    break
            if ok:
                return self.g * self.g * Fraction(Q, 4)
            Q += 1


def build_graph(d: Fraction, g: Fraction, prec: int = 10 ** 12) -> LatticeGraph:
    return LatticeGraph(d, g, covering_radius_bound(g, prec))
