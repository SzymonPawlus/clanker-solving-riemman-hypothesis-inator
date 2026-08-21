"""Two exact checks that do not depend on any `sketch`.

LEMMA P (projection bound), proved here and checked exactly.
  Let E be unit-separated in the closed equilateral triangle T of side a, and let
  k >= 3 with k-2 <= a < k-1.  Then for every corner V,
        #{ p in E : u_V(p) >= k-2 }  <=  2k-2.
  Proof.  The region {u_V >= k-2} is the trapezoid between the line u_V = k-2 and
  the side opposite V.  Its two parallel sides are parallel to that opposite side;
  write h for the perpendicular coordinate across the strip and x for the
  coordinate along it.  The strip's perpendicular width is w = (a-(k-2))*sqrt3/2,
  and w < sqrt3/2 because a < k-1.  Two points of E in the strip differ by v <= w
  perpendicular and by some x-distance g, and g^2 = d^2 - v^2 >= 1 - w^2 > 1/4.
  Their projections onto the x-axis therefore lie at mutual distance >= sqrt(1-w^2)
  in an interval of length at most a (the opposite side is the longest chord of the
  trapezoid in that direction), so
        m <= 1 + a / sqrt(1 - w^2).
  And a/sqrt(1-w^2) < 2k-2 for a < k-1, since that is equivalent to
        a^2 + 3(k-1)^2 (a-k+2)^2 < 4(k-1)^2,
  whose left side is increasing on [k-2, k-1] and equals the right side at a = k-1.
  Hence m <= 2k-2.                                                              []

  With n = T(k)-1 this is exactly S_{k-2}^{(V)} >= T(k-2): the top-scale instance of
  Prover A's (CIO-j), reproved with no appeal to Oler's inequality and no appeal to
  any `sketch`.  It also shows why that instance is break-even: the lattice at
  a = k-1 has 2k-1 points with u_V >= k-2, exactly one more.

AGGREGATE ACCOUNTING.  Viviani (sum u_V = 2a) forces, for a in [a0(k), k-1),
        sum_V sum_{j=1}^{k-2} S_j^{(V)}  >=  n*(k-3)      [call this V(k)]
  while (CIO-j) alone gives  >= 3*sum_j T(j)              [call this C(k)]
  and the open-corner-triangle capacities give  <= 3*sum_j N(j^-)   [U(k)].
"""

from fractions import Fraction as F
from exactiv import Ival
import geom as G


def tri(m):
    return m * (m + 1) // 2


def lemma_p_margin(k, a):
    """Exact sign check of a^2 + 3(k-1)^2 (a-k+2)^2 - 4(k-1)^2 (must be < 0)."""
    a = F(a)
    return a * a + 3 * (k - 1) ** 2 * (a - k + 2) ** 2 - 4 * (k - 1) ** 2


def lemma_p_bound(k, a, prec=40):
    """The explicit bound 1 + a/sqrt(1-w^2) as a rational interval."""
    a = F(a)
    w2 = F(3, 4) * (a - (k - 2)) ** 2
    g = Ival.sqrt_of(1 - w2, prec)
    return Ival(a) / g + 1


def aggregate(k, use_cited_N=True):
    n = tri(k) - 1
    J = k - 2
    Vb = n * (k - 3)
    Cb = 3 * sum(tri(j) for j in range(1, J + 1))
    caps = [G.N_upper_open(j) for j in range(1, J + 1)]
    Ub = 3 * sum(caps)
    return dict(n=n, J=J, V=Vb, C=Cb, U=Ub, caps=caps)


def check_all(kmax=12, out=print):
    out("LEMMA P -- exact sign of a^2 + 3(k-1)^2 (a-k+2)^2 - 4(k-1)^2 on [k-2, k-1]")
    out("   (must be < 0 strictly inside, = 0 at a = k-1)")
    bad = 0
    for k in range(3, kmax + 1):
        for num in (0, 1, 25, 50, 90, 99, 999, 1000):
            a = F(k - 2) + F(num, 1000)
            s = lemma_p_margin(k, a)
            want = 0 if num == 1000 else -1
            got = 0 if s == 0 else (1 if s > 0 else -1)
            if got != want:
                bad += 1
                out("   FAIL k=%d a=%s margin=%s" % (k, a, s))
    out("   checked %d (k, a) pairs, failures: %d" % ((kmax - 2) * 8, bad))
    out("")
    out("   the bound m <= 1 + a/sqrt(1-w^2), and the CIO cap n - T(k-2) = 2k-2:")
    out("   %3s %14s %22s %10s %10s" % ("k", "a", "1 + a/sqrt(1-w^2)", "floor", "2k-2"))
    for k in range(3, min(kmax, 9) + 1):
        for eps in (F(1, 10), F(1, 100), F(1, 10000)):
            a = F(k - 1) - eps
            b = lemma_p_bound(k, a)
            out("   %3d %14s %22s %10d %10d"
                % (k, str(a), repr(b), b.floor_upper(), 2 * k - 2))
    out("")
    out("AGGREGATE ACCOUNTING  (S = sum_V sum_j S_j^(V))")
    out("   %3s %5s %8s %8s %8s %10s %10s"
        % ("k", "n", "V(k)", "C(k)", "U(k)", "U-V", "k^2-4k+6"))
    for k in range(4, kmax + 1):
        d = aggregate(k)
        out("   %3d %5d %8d %8d %8d %10d %10d"
            % (k, d["n"], d["V"], d["C"], d["U"], d["U"] - d["V"], k * k - 4 * k + 6))
    out("")
    out("   V(k) - C(k) = (k-1)(k-6)/2, so Viviani only starts adding to CIO at k >= 7:")
    for k in range(4, kmax + 1):
        d = aggregate(k)
        assert d["V"] - d["C"] == (k - 1) * (k - 6) // 2, k
        out("      k=%2d  V-C = %4d   (formula %4d)" % (k, d["V"] - d["C"], (k - 1) * (k - 6) // 2))


if __name__ == "__main__":
    check_all()
