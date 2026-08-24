"""Step 0 -- re-derive the claimed two-family merge and its value law FROM SCRATCH.

CONSTRUCTION-SIDE BOOKKEEPING ONLY.  Nothing here is a packing claim; this file
only checks arithmetic identities about index sets and compares a closed form
against the published best-known table.  Exact integer / Q(sqrt 3) arithmetic
throughout; the only floats appear in the comparison against the published
DECIMAL table, and that comparison is evidence, never an accept/reject step for
any packing.
"""
from fractions import Fraction as F
from qsqrt3 import Q3, q3

KMAX = 12


def tri(k):
    return k * (k + 1) // 2


def A_family(kmax=KMAX):
    """4*Delta(k), k = 1, 2, ..."""
    return [4 * tri(k) for k in range(1, kmax + 1)]


def B_family(kmax=KMAX):
    """2*(k+1)^2 - 1, k = 1, 2, ..."""
    return [2 * (k + 1) ** 2 - 1 for k in range(1, kmax + 1)]


def merged(kmax=KMAX):
    return sorted(set(A_family(kmax)) | set(B_family(kmax)))


def law_n(j):
    """The merged staircase, as a single closed form in j (derived here, not assumed).

    Claim to be checked:  n(j) = Delta(j+2) + floor(j/2) + 1.
    """
    return tri(j + 2) + j // 2 + 1


def law_s(j):
    """s = 2j + 4*sqrt(3), exact."""
    return Q3(2 * j, 4)


def law_d(j):
    """d = s - 2*sqrt(3) = 2j + 2*sqrt(3), exact."""
    return Q3(2 * j, 2)


def main():
    print("=" * 72)
    print("0. The two stated families")
    A = A_family()
    B = B_family()
    print("  A: 4*Delta(k)      =", A[:8])
    print("  B: 2*(k+1)^2 - 1   =", B[:8])
    M = merged()
    print("  merged            =", M[:12])
    print("  gaps              =", [M[i + 1] - M[i] for i in range(11)])
    assert A[:5] == [4, 12, 24, 40, 60], A[:5]
    assert B[:4] == [7, 17, 31, 49], B[:4]
    assert M[:9] == [4, 7, 12, 17, 24, 31, 40, 49, 60], M[:9]
    assert [M[i + 1] - M[i] for i in range(8)] == [3, 5, 5, 7, 7, 9, 9, 11]
    print("  -> merge, order and gaps CONFIRMED (gaps are 3,5,5,7,7,9,9,11, NOT a constant 7)")

    print("=" * 72)
    print("1. Single closed form for the staircase:  n(j) = Delta(j+2) + floor(j/2) + 1")
    for j in range(0, 17):
        assert law_n(j) == M[j], (j, law_n(j), M[j])
    print("  n(j) agrees with the merged list for j = 0..16.")
    # and the two sub-families fall out of parity, algebraically
    for m in range(0, 9):
        assert law_n(2 * m) == 4 * tri(m + 1), m           # even j  -> A-family
        assert law_n(2 * m + 1) == 2 * (m + 2) ** 2 - 1, m  # odd  j  -> B-family
    print("  even j = 2m  ->  4*Delta(m+1)      (A-family), verified m = 0..8")
    print("  odd  j = 2m+1 -> 2*(m+2)^2 - 1     (B-family), verified m = 0..8")
    print("  So the 'two interleaved families' are ONE staircase indexed by j.")

    print("=" * 72)
    print("2. The value law at the three PROVEN anchors (status: cited)")
    # s(4) = 4 sqrt3, s(7) = 2 + 4 sqrt3, s(12) = 4 + 4 sqrt3
    proven = {4: Q3(0, 4), 7: Q3(2, 4), 12: Q3(4, 4)}
    for n, s in proven.items():
        j = M.index(n)
        assert law_n(j) == n
        assert law_s(j) == s, (n, law_s(j).sexpr(), s.sexpr())
        print("  n = %2d : j = %d, law gives s = %-18s  matches the proven optimum"
              % (n, j, law_s(j).sexpr()))
    print("  -> all three proven anchors sit on the law EXACTLY (not approximately).")

    print("=" * 72)
    print("3. The three open members inside the published window")
    for n in (17, 24, 31):
        j = M.index(n)
        print("  n = %2d : j = %d, law gives s = %-18s  d = %s"
              % (n, j, law_s(j).sexpr(), law_d(j).sexpr()))

    print("=" * 72)
    print("4. Predictions PAST the end of the published Graham-Lubachevsky table (n <= 34)")
    for n in (40, 49, 60):
        j = M.index(n)
        print("  n = %2d : j = %d, s = %-18s  d = %s"
              % (n, j, law_s(j).sexpr(), law_d(j).sexpr()))
    print("  These are PREDICTIONS OF A PATTERN, not bounds.  They become upper")
    print("  bounds only if an exact packing is exhibited -- which is what the rest")
    print("  of this directory does, per n, never by extrapolation.")

    print("=" * 72)
    print("5. Float cross-check against the published best-known table (EVIDENCE ONLY)")
    import math
    pub = {  # s(n), Graham-Lubachevsky as tabulated in experiments/circle-packing-search
        4: 6.928203230275509, 7: 8.928203230275509, 12: 10.928203230275509,
        17: 12.928203230276, 24: 14.928203230275, 31: 16.928203230275,
    }
    for n, sv in sorted(pub.items()):
        j = M.index(n)
        pred = 2 * j + 4 * math.sqrt(3.0)
        print("  n = %2d  published %.12f   law %.12f   |diff| = %.2e"
              % (n, sv, pred, abs(sv - pred)))
    print("  (floats, display only -- no packing decision anywhere in this repo")
    print("   directory is taken on a float)")
    print("=" * 72)
    print("ALL FAMILY-LAW ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
