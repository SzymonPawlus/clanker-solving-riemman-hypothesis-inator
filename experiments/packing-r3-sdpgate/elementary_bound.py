#!/usr/bin/env python3
"""The elementary 'mean pairwise squared distance' bound, for comparison against
what the level-2 moment relaxation actually returns.

STATUS: the arithmetic here is exact; the *argument* it encodes is `sketch`
(an informal argument by an agent, RULES.md §3).  It is recorded because the
level-2 SDP values coincide with it to solver precision, which is the diagnosis
of why the relaxation is slack.

Argument (sketch).  For points p_1..p_n with centroid c,
    sum_{i<j} ||p_i - p_j||^2  =  n * sum_i ||p_i - c||^2 ,
and the left side is a convex function of each p_i separately, so over the
closed unit triangle T_1 it is maximised with every p_i at a vertex.  If a, b, c
points sit at the three vertices (a+b+c = n, side 1) the sum is ab+bc+ca, which
over the *real* simplex a+b+c=n is at most n^2/3.  Hence

    min_{i<j} ||p_i-p_j||^2  <=  mean_{i<j} ||p_i-p_j||^2
                             <=  (n^2/3) / C(n,2)  =  2n / (3(n-1)) ,

i.e.  d(n) >= 2 / sqrt(2n/(3(n-1))) = sqrt(6(n-1)/n).

This is a true but worthless lower bound: it increases to sqrt(6) = 2.449... and
stops, while d(n) grows like sqrt(8n).

Run:  python3 elementary_bound.py
"""
from fractions import Fraction
from math import sqrt

SQRT3 = sqrt(3.0)
KNOWN_D = {2: 2.0, 3: 2.0, 4: 2 * SQRT3, 5: 4.0, 6: 4.0, 7: 2 + 2 * SQRT3,
           8: 2 + 2 * sqrt(33) / 3, 9: 6.0, 10: 6.0, 11: 4 + 4 * sqrt(6) / 3,
           12: 4 + 2 * SQRT3, 13: 4 + 2 * sqrt(6) / 3 + 4 * SQRT3 / 3,
           14: 8.0, 15: 8.0}


def mean_bound_f(n):
    """Upper bound on f(n) = max min squared distance in the unit triangle."""
    return min(Fraction(1), Fraction(2 * n, 3 * (n - 1)))


def main():
    print(f"{'n':>3} {'f_mean-bound':>14} {'d from it':>11} {'known d(n)':>11} "
          f"{'rel gap':>9}")
    for n in range(2, 21):
        f = mean_bound_f(n)
        d = 2 / sqrt(float(f))
        if n in KNOWN_D:
            dt = KNOWN_D[n]
            print(f"{n:>3} {str(f):>14} {d:>11.6f} {dt:>11.6f} "
                  f"{100*(dt-d)/dt:>8.2f}%")
        else:
            print(f"{n:>3} {str(f):>14} {d:>11.6f} {'(open)':>11} {'':>9}")
    print("\nlimit as n -> infinity:  d >= sqrt(6) = 2.449489...,  "
          "while d(n) ~ sqrt(8n).")


if __name__ == "__main__":
    main()
