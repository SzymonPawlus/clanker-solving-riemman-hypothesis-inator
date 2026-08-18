#!/usr/bin/env python3
"""Oler lower bound for s(n): circle packing in an equilateral triangle.

Status of the output: `numerical` (RULES.md section 3) -- it is arithmetic
evaluating the closed-form bound derived in README.md section 2.2 (that
derivation is `sketch` -- mine, from the `cited` Oler inequality, which would cap
it at `cited` if promoted; see README.md section 5 for the standing invitation to
Codex to grant `verified:review` themselves).

What the numbers do NOT show.  For n <= 15 the "known s(n)" column is the true
optimum, so "gap > 0" really does mean Oler is slack there.  For n = 16, 17, 18
the comparison column is the best known *construction*, i.e. an UPPER bound on an
unknown s(n).  s_Oler(n) < U(n) does not imply s_Oler(n) < s(n); s(n) could equal
s_Oler(n) with every published packing non-optimal.  Nothing printed below
discharges the issue-#17 kill-criterion -- see README.md section 5.1.

Derivation being evaluated (see README §2):

    Oler (1961): for a Jordan polygon pi whose vertices all belong to a finite
    point set E contained in the closed region bounded by pi, with all pairwise
    distances in E at least 1,

        N  <=  (2/sqrt 3) A(pi) + (1/2) M(pi) + 1.

    Applied to the convex hull of n points at mutual distance >= 2 inside an
    equilateral triangle of side d (so rescale by 1/2: side a = d/2, distance 1):

        n <= (2/sqrt 3)(sqrt 3 a^2 / 4) + (1/2)(3a) + 1 = (a^2 + 3a + 2)/2

    hence a >= (sqrt(8n+1) - 3)/2 (solving for a >= 0), d = 2a >= sqrt(8n+1) - 3,
    and since s = d + 2 sqrt 3,

        s(n) >= 2 sqrt 3 + sqrt(8n+1) - 3   =:  s_Oler(n).

    CAVEAT on the small cases, see README section 2.2.  That hull argument needs
    the hull to be a Jordan polygon, which fails when E lies on a line -- always
    for n = 1, 2, and for collinear configurations of any size.  Those cases are
    covered separately and elementarily (the extreme two points are >= n-1 apart
    and the triangle has diameter a, so a >= n-1, which implies the same bound and
    is strictly stronger for n >= 2).  The n = 1 and n = 2 rows printed below are
    therefore NOT instances of Oler's theorem.

Run:  python3 oler_bound.py       (stdlib only, no dependencies)
"""

from math import sqrt, isqrt

SQRT3 = sqrt(3.0)


def s_oler(n: int) -> float:
    """Oler lower bound on the triangle side s(n) holding n unit circles."""
    return 2.0 * SQRT3 + sqrt(8 * n + 1) - 3.0


def is_triangular(n: int) -> bool:
    r = isqrt(8 * n + 1)
    return r * r == 8 * n + 1


# Known values of s(n), n <= 15.  (n = 20 is also settled in the literature --
# `cited`, qualified by abstract-only provenance for Payan 1997; see the problem
# README's "The n = 20 attribution" section.  It is deliberately NOT added here:
# this table is the n <= 15 range whose values were checked against primary or
# open-access sources.)
#
# Sources, all `cited`:
#   - exact expressions: problems/circle-packing-equilateral-triangle/README.md
#     (which sources them from Friedman's Packing Center and Wikipedia);
#   - n = 13 exact value recomputed here from Joos's separation distance
#     d13 = 9 - 5 sqrt3 - (7/2) sqrt6 + 6 sqrt2 in a UNIT triangle
#     [Joos, Aequat. Math. 95 (2021) 35-65, as quoted by Tedeschi & Mackey,
#      AJUR 18(2) (2021) 3-12];
#   - "proven" column: Wikipedia states optimality is proven for all n <= 15 and
#     for every triangular number; attribution per Melissen & Schuur, Discrete
#     Math. 142(1-3) (1995) 333-342 [doi:10.1016/0012-365X(95)90139-C], plus Payan
#     (1997) for n = 14 and Joos (2021) for n = 13.  See README section 3.
d13_unit = 9 - 5 * sqrt(3) - 3.5 * sqrt(6) + 6 * sqrt(2)

KNOWN = {
    1: (2 * SQRT3, "2*sqrt3", True),
    2: (2 + 2 * SQRT3, "2 + 2*sqrt3", True),
    3: (2 + 2 * SQRT3, "2 + 2*sqrt3", True),
    4: (4 * SQRT3, "4*sqrt3", True),
    5: (4 + 2 * SQRT3, "4 + 2*sqrt3", True),
    6: (4 + 2 * SQRT3, "4 + 2*sqrt3", True),
    7: (2 + 4 * SQRT3, "2 + 4*sqrt3", True),
    8: (2 + 2 * SQRT3 + 2 * sqrt(33) / 3, "2 + 2*sqrt3 + 2*sqrt33/3", True),
    9: (6 + 2 * SQRT3, "6 + 2*sqrt3", True),
    10: (6 + 2 * SQRT3, "6 + 2*sqrt3", True),
    11: (4 + 2 * SQRT3 + 4 * sqrt(6) / 3, "4 + 2*sqrt3 + 4*sqrt6/3", True),
    12: (4 + 4 * SQRT3, "4 + 4*sqrt3", True),
    13: (2 * SQRT3 + 2 / d13_unit, "2*sqrt3 + 2/d13", True),
    14: (8 + 2 * SQRT3, "8 + 2*sqrt3", True),
    15: (8 + 2 * SQRT3, "8 + 2*sqrt3", True),
}


def main() -> None:
    print(" n  tri?  s_Oler(n)   known s(n)   gap        exact s(n)")
    print("-" * 72)
    for n in range(1, 22):
        lo = s_oler(n)
        tri = "  T " if is_triangular(n) else "    "
        if n in KNOWN:
            val, expr, _ = KNOWN[n]
            gap = val - lo
            flag = "  TIGHT" if abs(gap) < 1e-12 else ""
            print(f"{n:2d} {tri}  {lo:9.6f}   {val:9.6f}   {gap:8.6f}{flag}   {expr}")
        else:
            print(f"{n:2d} {tri}  {lo:9.6f}      --          --")

    print()
    print("Triangular n in range, and the exact identity s_Oler(T_k) = 2 sqrt3 + 2(k-1):")
    for k in range(1, 9):
        t = k * (k + 1) // 2
        print(
            f"  k={k:2d}  T_k={t:3d}  s_Oler={s_oler(t):9.6f}  "
            f"2*sqrt3+2(k-1)={2 * SQRT3 + 2 * (k - 1):9.6f}  "
            f"agree={abs(s_oler(t) - (2 * SQRT3 + 2 * (k - 1))) < 1e-12}"
        )

    print()
    print("Open cases: Oler lower bound vs BEST-KNOWN construction (an upper bound).")
    print("These rows bracket s(n); they do NOT show Oler is slack here (README 5.1).")
    print("Separation distances t_n in a UNIT triangle from Melissen & Schuur,")
    print("Discrete Math. 142(1-3) (1995) 333-342 (open access), doi 10.1016/")
    print("0012-365X(95)90139-C.  s = 2 sqrt3 + 2/t_n.")
    print("  n   s_Oler(n)   best known   width of the interval that is still open")
    for n, t in ((16, 0.216227269), (17, (3 - SQRT3) / 6), (18, 0.203465240)):
        best = 2 * SQRT3 + 2 / t
        print(f" {n:2d}   {s_oler(n):9.6f}   {best:9.6f}    {best - s_oler(n):8.6f}")

    print()
    print("Sanity check of the point-formulation rescaling for n = 13:")
    print(f"  d13 (unit triangle, Joos)      = {d13_unit:.9f}")
    print(f"  d(13) = 2/d13                  = {2 / d13_unit:.9f}")
    print(f"  s(13) = 2 sqrt3 + 2/d13        = {2 * SQRT3 + 2 / d13_unit:.9f}")
    print("  README.md quotes s(13) ~ 11.406 -- agrees.")


if __name__ == "__main__":
    main()
