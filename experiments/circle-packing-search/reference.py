"""Reference values to validate the search against. Nothing here is computed by us.

Two conventions are in play and conflating them is the easiest way to fool yourself:

* This repo (``problems/circle-packing-equilateral-triangle/README.md``) uses ``s(n)``, the side
  of the smallest equilateral triangle holding ``n`` **unit** circles, and the equivalent point
  formulation: ``n`` points at pairwise distance >= 2 in a triangle of side ``D = s - 2*sqrt(3)``.

* Graham & Lubachevsky (EJC 2 (1995) #A1) tabulate ``d(n)``, the disk *diameter* measured in
  units equal to the side of the smallest equilateral triangle containing all disk **centres**
  (their Section 2, the 15-significant-digit number printed under each packing diagram).

The search in ``search.py`` maximises ``m``, the minimum pairwise distance of ``n`` points in a
**unit** equilateral triangle. That is exactly Graham-Lubachevsky's ``d(n)`` when the optimal
configuration spans the triangle, so::

    m  =  d(n)          D = 2 / m          s(n) = 2 / m + 2 * sqrt(3)

The n <= 15 entries below are the exact closed forms from Erich Friedman's Packing Center
(https://erich-friedman.github.io/packing/cirintri/), cross-checked against the decimals printed
in Graham-Lubachevsky Figures 5.1-5.3 where those overlap (n = 4, 8, 11, 12, 13, 16, 17, 18, 19).
"""

from __future__ import annotations

import math

SQRT3 = math.sqrt(3.0)

# n -> exact s(n) as a closed form, for n <= 15. Source: Friedman, Packing Center.
# "proved" / "found" is Friedman's own marking; see issue #1 -- the repo README flags a
# proven-vs-best-known discrepancy with Wikipedia that is NOT resolved here and is not
# this experiment's business. We only use these as *numerical* targets.
EXACT_S: dict[int, tuple[float, str, str]] = {
    2: (2 + 2 * SQRT3, "2 + 2*sqrt(3)", "trivial"),
    3: (2 + 2 * SQRT3, "2 + 2*sqrt(3)", "trivial"),
    4: (4 * SQRT3, "4*sqrt(3)", "proved"),
    5: (4 + 2 * SQRT3, "4 + 2*sqrt(3)", "proved"),
    6: (4 + 2 * SQRT3, "4 + 2*sqrt(3)", "proved"),
    7: (2 + 4 * SQRT3, "2 + 4*sqrt(3)", "proved"),
    8: (2 + 2 * SQRT3 + 2 * math.sqrt(33) / 3, "2 + 2*sqrt(3) + 2*sqrt(33)/3", "proved"),
    9: (6 + 2 * SQRT3, "6 + 2*sqrt(3)", "proved"),
    10: (6 + 2 * SQRT3, "6 + 2*sqrt(3)", "proved"),
    11: (4 + 2 * SQRT3 + 4 * math.sqrt(6) / 3, "4 + 2*sqrt(3) + 4*sqrt(6)/3", "proved"),
    12: (4 + 4 * SQRT3, "4 + 4*sqrt(3)", "proved"),
    13: (
        4 + 2 * math.sqrt(6) / 3 + 10 * SQRT3 / 3,
        "4 + 2*sqrt(6)/3 + 10*sqrt(3)/3",
        "best known",
    ),
    14: (8 + 2 * SQRT3, "8 + 2*sqrt(3)", "best known"),
    15: (8 + 2 * SQRT3, "8 + 2*sqrt(3)", "proved"),
}

# n -> d(n) exactly as printed in Graham-Lubachevsky (15 significant digits), for the best
# packing they report ("a" suffix).  Entries for n in {20, 21, 27, 28, 35, 36} are not printed
# as diagrams in the paper: those are the triangular numbers T(k) = k(k+1)/2 and T(k) - 1, where
# the packing is the k-row triangular lattice and d = 1/(k-1) exactly (paper, Section 2:
# "We performed a small number of runs with n = 21, 27, 28, 35 and 36 disks. In every case, the
# resulting packings were consistent with the existing results").
GL_D: dict[int, str] = {
    4: "0.577350269189626",
    7: "0.366025403784439",
    8: "0.343070330817254",
    11: "0.275255128608411",
    12: "0.267949192431123",
    13: "0.251813236653061",
    16: "0.216227269309782",
    17: "0.211324865405187",
    18: "0.203465240539124",
    19: "0.200321458983439",
    20: "0.2",
    21: "0.2",
    22: "0.179396908611866",
    23: "0.175153309170525",
    24: "0.174457630187010",
    25: "0.169065874417891",
    26: "0.166738399395271",
    27: "0.166666666666667",
    28: "0.166666666666667",
    29: "0.152189614060732",
    30: "0.150761500215428",
    31: "0.148543145110506",
    32: "0.145102169183849",
    33: "0.143447408371201",
    34: "0.142869646754496",
    35: "0.142857142857143",
    36: "0.142857142857143",
}


def s_from_m(m: float) -> float:
    """Side of the smallest equilateral triangle holding n unit circles, from the max-min
    distance ``m`` of n points in a unit equilateral triangle."""
    return 2.0 / m + 2.0 * SQRT3


def m_from_s(s: float) -> float:
    """Inverse of :func:`s_from_m`."""
    return 2.0 / (s - 2.0 * SQRT3)


def reference_m(n: int) -> tuple[float, str] | None:
    """Best published ``m = d(n)`` for this ``n``, with a source tag, or None if unknown.

    Exact closed forms win over Graham-Lubachevsky's decimals where both exist, since the closed
    form is infinitely precise and the decimal is truncated at 15 digits.
    """
    if n in EXACT_S:
        return m_from_s(EXACT_S[n][0]), "Friedman (exact closed form)"
    if n in GL_D:
        return float(GL_D[n]), "Graham-Lubachevsky 1995 (15 s.f.)"
    return None


def agreement_digits(got: float, ref: float) -> float:
    """Significant decimal digits of agreement between ``got`` and ``ref``.

    Returns ``inf`` on an exact bit-for-bit match. Negative-ish values mean disagreement in the
    first significant digit. This is a *relative* measure, so it is unaffected by which of the
    m / D / s conventions you feed it as long as both arguments use the same one.
    """
    if got == ref:
        return float("inf")
    rel = abs(got - ref) / abs(ref)
    return -math.log10(rel)
