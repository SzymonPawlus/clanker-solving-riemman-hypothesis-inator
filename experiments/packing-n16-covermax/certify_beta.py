#!/usr/bin/env python3
"""Exact certification that A_15 <= 4.801, worker C5, 2026-08-22.

A_15 := sup{ a : T_a is covered by 15 sets of diameter < 1 }.

Claim certified here (the arithmetic half; the geometry is in the attack README):

  THEOREM U.  No 15 sets of diameter < 1 cover T_{a*} for a* = 4801/1000.
  Hence A_15 <= 4801/1000 = 4.801  (T_a contains T_{a*} for every a >= a*).

Structure of the proof (README, Theorem F + Theorem U):
  For a* >= 1+2sqrt3 every 15-piece covering has EXACTLY
     3 corner pieces   (area <= pi/6 each),
     9 one-side pieces (3 per side, per-side trace lengths sum >= a*-2,
                        area <= g(l) = pi/2 - asin(l/2) - (l/2)sqrt(1-l^2/4)),
     3 interior pieces (area <= pi/4 each, isodiametric).
  With h = min(pi/4, g) concave nonincreasing, Jensen gives the budget
     area(T_a*) = sqrt3/4 a*^2  <=  3*(pi/6) + 9*h((a*-2)/3) + 3*(pi/4).
  This script certifies that the inequality FAILS at a* by exact rational
  arithmetic: every transcendental enters only as a certified rational bound,
  rounded AGAINST the conclusion (area from below, budget from above).

Decisions: Fraction only.  No floats anywhere in a decided quantity.
"""

from fractions import Fraction as F
from math import isqrt

# ---------------------------------------------------------------- guards ----
# Circularity guard (KILL-CRITERION K7): the best-known 16-point packing value
# is a COMPARISON TARGET ONLY.  It is not an input to any quantity below.
COMPARISON_ONLY_packing_target = F(46247636, 10**7)   # 4.6247636 -- never used in a bound

# Tripwire (K2): the repo's exactly certified covering value.  Any bound at or
# below this is a bug in THIS argument and must abort the run.
CERTIFIED_COVERING_LB = F(4463841021, 10**9)          # n16-shapes exact certificate


# ------------------------------------------------- certified enclosures -----
def sqrt_lo(q: F, digits: int = 30) -> F:
    """Rational r with r*r <= q (lower bound on sqrt(q)), q >= 0."""
    scale = 10 ** digits
    n = (q.numerator * scale * scale) // q.denominator   # floor(q * scale^2)
    r = F(isqrt(n), scale)
    assert r * r <= q
    return r


def sqrt_hi(q: F, digits: int = 30) -> F:
    """Rational r with r*r >= q (upper bound on sqrt(q))."""
    scale = 10 ** digits
    n = (q.numerator * scale * scale) // q.denominator
    r = F(isqrt(n) + 1, scale)
    assert r * r >= q
    return r


def atan_bounds(inv_x: int, terms: int) -> tuple[F, F]:
    """(lo, hi) rational bounds on arctan(1/inv_x) via the alternating series.

    arctan(y) = y - y^3/3 + y^5/5 - ...  For 0 < y < 1 the partial sums
    alternate around the limit: ending on a subtracted term gives a lower
    bound, ending on an added term an upper bound.
    """
    y = F(1, inv_x)
    s = F(0)
    lo = hi = None
    for k in range(terms):
        t = y ** (2 * k + 1) / (2 * k + 1)
        if k % 2 == 0:
            s += t
            hi = s
        else:
            s -= t
            lo = s
    assert lo is not None and hi is not None and lo < hi
    return lo, hi


def pi_bounds() -> tuple[F, F]:
    """Machin: pi = 16 arctan(1/5) - 4 arctan(1/239)."""
    a5_lo, a5_hi = atan_bounds(5, 24)
    a239_lo, a239_hi = atan_bounds(239, 8)
    lo = 16 * a5_lo - 4 * a239_hi
    hi = 16 * a5_hi - 4 * a239_lo
    return lo, hi


def asin_lo(x: F, terms: int = 40) -> F:
    """Lower bound on arcsin(x), 0 <= x < 1, by the Maclaurin partial sum.

    arcsin(x) = sum_{n>=0} C(2n,n) / (4^n (2n+1)) x^(2n+1).
    Every term is positive, so any partial sum is a rigorous lower bound.
    """
    assert 0 <= x < 1
    s = F(0)
    c = 1  # C(2n, n)
    for n in range(terms):
        s += F(c, (4 ** n) * (2 * n + 1)) * x ** (2 * n + 1)
        c = c * (2 * n + 1) * (2 * n + 2) // ((n + 1) * (n + 1))
    return s


# ------------------------------------------------------------- the bound ----
def certify(a_star: F) -> F:
    """Return the certified positive margin of the refutation at side a_star,
    raising AssertionError if any step fails."""

    # --- side conditions of the forced-structure theorem (Theorem F) ---
    # (F1) a* >= 1 + 2 sqrt3   <=>  (a*-1)^2 >= 12    [inner-triangle corners >= 1 apart]
    assert a_star > 1 and (a_star - 1) ** 2 >= 12
    # (F2) a* > 2 + 4/sqrt3    <=>  3 (a*-2)^2 > 16   [deep middle longer than 2]
    assert a_star > 2 and 3 * (a_star - 2) ** 2 > 16
    # (F3) a* < 5              [per-edge mean trace l = (a*-2)/3 < 1]
    assert a_star < 5
    # (F4) vertices pairwise > 1 apart, opposite-side distance sqrt3 a/2 > 2:
    #      3 a*^2 > 16  (weaker than F2's consequence; recorded for completeness)
    assert 3 * a_star ** 2 > 16

    ell = (a_star - 2) / 3
    x = ell / 2

    pi_lo, pi_hi = pi_bounds()
    assert pi_hi - pi_lo < F(1, 10 ** 20)

    # g(ell) upper bound: pi/2 (upper) - asin(x) (lower) - x*sqrt(1-x^2) (lower)
    root_lo = sqrt_lo(1 - x * x)
    g_hi = pi_hi / 2 - asin_lo(x) - x * root_lo

    # h = min(pi/4, g); use whichever cap is smaller (both are valid caps)
    h_hi = min(pi_hi / 4, g_hi)

    # coverer's total budget, upper bound
    budget_hi = 3 * (pi_hi / 6) + 9 * h_hi + 3 * (pi_hi / 4)

    # area(T_a*) lower bound
    s3_lo = sqrt_lo(F(3))
    area_lo = s3_lo * a_star ** 2 / 4

    margin = area_lo - budget_hi
    assert margin > 0, f"certification FAILED at a*={a_star}: margin={float(margin)}"
    return margin


def main() -> None:
    a_star = F(4801, 1000)  # smallest certified rational tried (K3); 4803/1000 also certifies with margin 0.0172

    # K2 tripwire: the bound must sit strictly above the certified covering.
    assert a_star > CERTIFIED_COVERING_LB, "bound below certified covering: bug"
    # and the comparison target must not have leaked into the bound:
    assert a_star != COMPARISON_ONLY_packing_target

    margin = certify(a_star)
    print("THEOREM U certified:  A_15 <= 4801/1000 = 4.801")
    print(f"  refutation margin at a* (exact rational, printed as float): {float(margin):.6f}")
    print(f"  ell = (a*-2)/3 = {(a_star-2)/3} = {float((a_star-2)/3):.6f}")

    # --- adjudication exhibits (exact) --------------------------------------
    # R1's witness: P = (21/20, 0) on AB, Q at distance 1/2 from A along AC.
    al, be = F(21, 20), F(1, 2)
    d2 = al * al - al * be + be * be           # squared distance, 60-degree form
    assert d2 == F(331, 400) and d2 < 1
    assert al > 1                              # P lies in the distance-1 "middle"
    assert 3 * al * al < 4                     # but 21/20 < 2/sqrt3: inside deep-middle cutoff
    print("R1 witness confirmed exactly: |PQ|^2 = 331/400 < 1, alpha = 21/20 in (1, 2/sqrt3)")

    # The repaired constant: sup of the two-side trace reach is 2/sqrt3,
    # attained at beta = 1/sqrt3:  phi(beta)=(beta+sqrt(4-3 beta^2))/2.
    # Exact check at the critical point in Q(sqrt3): with b=1/sqrt3,
    # sqrt(4-3 b^2)=sqrt3, phi = (1/sqrt3+sqrt3)/2 = 2/sqrt3.  Verified as
    # an identity over Q(sqrt3): (1 + 3)/(2 sqrt3) = 2/sqrt3.
    #   (algebraic identity; nothing to compute)
    # And phi(beta) <= 2/sqrt3 for all beta:  (beta + sqrt(4-3 beta^2))/2 <= 2/sqrt3
    #   <=>  sqrt(4-3 beta^2) <= 4/sqrt3 - beta   (RHS > 0 for beta <= 2/sqrt3)
    #   <=>  4 - 3 b^2 <= 16/3 - 8 b/sqrt3 + b^2  <=>  0 <= (2b - 2/sqrt3)^2. QED
    print("two-side reach lemma: sup = 2/sqrt3, verified algebraically (see comments)")

    # sanity echo of thresholds as exact comparisons
    #   1+2sqrt3 < a*  <=> (a*-1)^2 > 12
    assert (a_star - 1) ** 2 > 12
    print("side conditions F1-F4 all hold at a* (exact)")


if __name__ == "__main__":
    main()
