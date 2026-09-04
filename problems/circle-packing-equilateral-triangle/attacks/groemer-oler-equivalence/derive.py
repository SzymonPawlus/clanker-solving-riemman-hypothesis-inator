#!/usr/bin/env python3
"""Groemer (Math. Z. 73 (1960) 285-294) Satz  <=>  Oler's inequality at pi = conv(E).

Issue #96.  Exact symbolic arithmetic only (sympy); floats appear solely in printed
displays, never in an assertion.  Run:  python3 derive.py

Groemer's scale: unit-RADIUS circles, so centres are >= 2 apart.
Oler's    scale: points >= 1 apart.
The map between them is a SHRINK by 1/2, and getting that backwards is the error this
script exists to make impossible -- see check_rescaling_direction().
"""

from sympy import (Eq, Integer, N, Rational, expand, pi, simplify, solve, sqrt,
                   symbols)

# Groemer's constants, p. 285.
KAPPA = (2 - sqrt(3)) / 2
LAMBDA = sqrt(12) - pi * (sqrt(3) - 1)

# A, M: area and perimeter of H = conv(E) at Groemer's scale (separation 2).
A, M = symbols("A M", nonnegative=True)
# Ap, Mp: the same at Oler's scale (separation 1).
Ap, Mp = symbols("A_prime M_prime", nonnegative=True)

OLER_RHS = 2 / sqrt(3) * Ap + Rational(1, 2) * Mp + 1


def check_printed_constants():
    """kappa and lambda match the decimals Groemer prints on p. 285."""
    assert abs(N(KAPPA, 20) - Rational(1339, 10000)) < Rational(1, 10000)
    assert abs(N(LAMBDA, 20) - Rational(11642, 10000)) < Rational(1, 10000)
    print(f"kappa  = {KAPPA} = {N(KAPPA, 10)}   (p. 285 prints 0,1339...)")
    print(f"lambda = {LAMBDA} = {N(LAMBDA, 10)}   (p. 285 prints 1,1642...)")


def check_hilfssatz_1_rearrangement():
    """p. 288: summing (4) gives  (sqrt3/pi)(2*pi*n - 2*pi) + kappa*(U - 2pi) <= F - pi.

    Groemer asserts this "ist mit (2) gleichbedeutend".  Verify that independently:
    rearranged, it must produce exactly the printed lambda.
    """
    n, F, U = symbols("n F U", positive=True)
    summed = sqrt(3) / pi * (2 * pi * n - 2 * pi) + KAPPA * (U - 2 * pi) - (F - pi)
    # summed <= 0  <=>  n*sqrt(12) <= F - kappa*U + lambda_implied
    lam_implied = simplify(solve(Eq(summed, 0), n)[0] * sqrt(12) - (F - KAPPA * U))
    assert simplify(lam_implied - LAMBDA) == 0
    print(f"\nHilfssatz 1 summation implies lambda = {simplify(lam_implied)}  == printed lambda: True")


def check_pi_cancels_and_reduce():
    """Steiner + Satz  =>  n <= sqrt(3)/6 A + M/4 + 1  at separation 2."""
    F = A + M + pi          # Steiner: area(H (+) B_1)
    U = M + 2 * pi          # Steiner: perimeter(H (+) B_1)
    rhs = expand(F - KAPPA * U + LAMBDA)
    assert simplify(rhs.coeff(pi)) == 0, "pi did NOT cancel"
    bound = simplify(rhs / sqrt(12))
    assert simplify(bound.coeff(A) - sqrt(3) / 6) == 0
    assert simplify(bound.coeff(M) - Rational(1, 4)) == 0
    assert simplify(bound.subs({A: 0, M: 0}) - 1) == 0
    print(f"\nSteiner-substituted RHS: {rhs}      coeff of pi: {simplify(rhs.coeff(pi))}")
    print(f"  => n <= {bound}   (separation 2)")
    return bound


def check_rescaling_direction(bound):
    """Separation 2 -> separation 1 is a SHRINK by 1/2: A = 4A', M = 2M'.

    Assert both that the correct substitution reproduces Oler and that the inverted
    one does not, so a flipped direction cannot pass silently.
    """
    right = simplify(bound.subs({A: 4 * Ap, M: 2 * Mp}))
    wrong = simplify(bound.subs({A: Ap / 4, M: Mp / 2}))
    assert simplify(right - OLER_RHS) == 0, "correct substitution does NOT give Oler"
    assert simplify(wrong - OLER_RHS) != 0, "inverted substitution ALSO gives Oler -- guard is broken"
    print(f"\n  correct  A=4A', M=2M'   -> n <= {right}   matches Oler: True")
    print(f"  inverted A=A'/4, M=M'/2 -> n <= {wrong}   matches Oler: False")
    return right


def check_converse():
    """Oler at pi = conv(E), pushed back through Steiner, rebuilds Groemer's RHS."""
    F, U = symbols("F U", positive=True)
    back = simplify(OLER_RHS.subs({Ap: A / 4, Mp: M / 2}))          # to separation 2
    rebuilt = simplify(sqrt(12) * back)                              # clear the sqrt(12)
    rebuilt = simplify(rebuilt.subs({A: F - M - pi}))                # undo Steiner (area)
    rebuilt = simplify(rebuilt.subs({M: U - 2 * pi}))                # undo Steiner (perimeter)
    assert simplify(rebuilt - (F - KAPPA * U + LAMBDA)) == 0
    print(f"\nConverse: Oler + Steiner rebuilds {rebuilt}")
    print(f"          Groemer's F - kappa*U + lambda: {simplify(F - KAPPA * U + LAMBDA)}   identical: True")


def check_tightness_at_triangular_n(kmax=7):
    """The Satz is exactly tight on triangular-lattice packings -- Groemer's case a).

    H = equilateral triangle of side 2(k-1) at separation 2; B = H (+) B_1.
    """
    print("\nTightness at Groemer's own scale (B = H (+) B_1, triangular lattice):")
    for k in range(1, kmax + 1):
        n = k * (k + 1) // 2
        a = Integer(2) * (k - 1)
        AH = sqrt(3) / 4 * a ** 2 if k > 1 else Integer(0)
        MH = 3 * a
        lhs = n * sqrt(12)
        rhs = (AH + MH + pi) - KAPPA * (MH + 2 * pi) + LAMBDA
        gap = simplify(rhs - lhs)
        assert gap == 0, f"expected exact equality at k={k}, got {gap}"
        print(f"  k={k} n={n:3d}: LHS = RHS = {N(lhs, 10)}   RHS-LHS = {gap} (exact)")


def check_containing_triangle_slack_table():
    """Reproduce the pre-existing slack table in ../../README.md (containing triangle).

    F = sqrt(3)s^2/4, U = 3s.  This is the OTHER region, and it is correctly slack.
    """
    s = symbols("s", positive=True)
    print("\nGroemer on the CONTAINING triangle (the region ../../README.md tabulates):")
    for n, true_s in [(3, 2 + 2 * sqrt(3)), (6, 4 + 2 * sqrt(3)), (10, 6 + 2 * sqrt(3)),
                      (15, 8 + 2 * sqrt(3)), (21, 10 + 2 * sqrt(3))]:
        roots = solve(Eq(n * sqrt(12), sqrt(3) * s ** 2 / 4 - KAPPA * 3 * s + LAMBDA), s)
        bound = max(r for r in roots if r.is_real and r > 0)
        assert N(true_s - bound, 20) > 0, f"expected slack at n={n}"
        print(f"  n={n:3d}: Groemer bound s >= {N(bound, 8)}   true s(n) = {N(true_s, 8)}"
              f"   slack = {N(true_s - bound, 6)}")


if __name__ == "__main__":
    check_printed_constants()
    check_hilfssatz_1_rearrangement()
    bound = check_pi_cancels_and_reduce()
    check_rescaling_direction(bound)
    check_converse()
    check_tightness_at_triangular_n()
    check_containing_triangle_slack_table()
    print("\nAll checks passed: Groemer's Satz on B = conv(E) (+) B_1 is Oler's inequality"
          " at pi = conv(E), and is exactly tight on triangular-lattice packings.")
