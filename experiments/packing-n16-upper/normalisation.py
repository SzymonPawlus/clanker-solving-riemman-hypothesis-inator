"""Normalisation, asserted in code before anything else runs.

Yesterday several workers shipped wrong headlines by mixing three conventions.  There are
exactly three, they are fixed here, and every other module in this directory imports from
this one rather than restating them.

    separation-1 form   n points, pairwise distance >= 1, in an equilateral triangle of side a
    unit-triangle form  n points in T = conv{(0,0),(1,0),(1/2,sqrt(3)/2)}, min pairwise dist m
    repo certificate    n points, pairwise distance >= 2, in a triangle of side d;  s = d + 2*sqrt(3)

Scaling the unit-triangle configuration by 1/m makes the minimum separation exactly 1 inside a
triangle of side 1/m, so

    a = 1 / m        d = 2 * a = 2 / m        s = d + 2*sqrt(3)

Graham & Lubachevsky (EJC 2 (1995) #A1) tabulate d(n) = the *disk diameter* in units of the side
of the smallest triangle containing all disk centres.  That is numerically identical to m(n).
The letter ``d`` therefore means two different things in the two sources; this module never uses
the bare name.  ``GL_D16`` is Graham-Lubachevsky's value; ``M16_*`` are bounds on m(16).

Nothing in this file is computed by us.  The reference decimal is transcribed from
``experiments/circle-packing-search/reference.py`` (read-only, by another worker), which in turn
transcribes Graham-Lubachevsky's printed 15 significant figures.  RULES.md of the problem
directory, SS4: never hand-type a reference value.  The transcription is checked below against
that file at import time.
"""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

SQRT3 = math.sqrt(3.0)

# --- the record, and honest error bars on it ------------------------------------------------
# Graham-Lubachevsky print 15 significant figures.  We do not know whether they truncated or
# rounded, so d(16) is bracketed by round-to-nearest at that precision *widened by one ulp of
# the decimal* on the low side to cover truncation.
GL_D16_STR = "0.216227269309782"
GL_D16 = float(GL_D16_STR)

_ULP = Fraction(1, 10**15)
M16_LO = Fraction(216227269309782, 10**15)              # truncation-safe lower bound on m(16)
M16_HI = Fraction(216227269309782, 10**15) + _ULP       # and upper bound
# Beating the record means m > M16_HI.  Any m in [M16_LO, M16_HI] is "matches the record".

A16_HI = 1.0 / float(M16_LO)   # largest side consistent with the record  (4.6247635795...)
A16_LO = 1.0 / float(M16_HI)

#: the abort-and-exactify trigger of KILL-CRITERION.md
TRIGGER_M = float(M16_HI) + 1e-9


def m_to_a(m: float) -> float:
    """separation-1 side length from unit-triangle min distance."""
    return 1.0 / m


def m_to_d(m: float) -> float:
    """repo certificate side (separation 2)."""
    return 2.0 / m


def m_to_s(m: float) -> float:
    """side of the equilateral triangle holding n *unit circles*."""
    return 2.0 / m + 2.0 * SQRT3


def _self_test() -> None:
    # round trip
    m = float(M16_LO)
    assert abs(m_to_a(m) * m - 1.0) < 1e-15
    assert abs(m_to_d(m) - 2 * m_to_a(m)) < 1e-15
    assert abs(m_to_s(m) - (m_to_d(m) + 2 * SQRT3)) < 1e-15
    # the three headline numbers of the task statement
    assert abs(m_to_a(m) - 4.6247636) < 1e-6, m_to_a(m)
    assert abs(m_to_s(m) - 12.713629) < 1e-5, m_to_s(m)
    # 16 = T(5) + 1, and T(6) - 5
    assert 5 * 6 // 2 == 15 and 6 * 7 // 2 == 21
    # the reference decimal really is what the read-only reference file says
    ref = Path(__file__).resolve().parents[1] / "circle-packing-search" / "reference.py"
    text = ref.read_text()
    assert f'16: "{GL_D16_STR}"' in text, "reference.py disagrees with GL_D16_STR"


_self_test()

if __name__ == "__main__":
    print(f"GL d(16)      = {GL_D16_STR}   (== m(16), unit-triangle min distance)")
    print(f"m(16) window  = [{float(M16_LO):.18f}, {float(M16_HI):.18f}]")
    print(f"a(16) <= {A16_HI:.15f}   (separation 1, side a = 1/m)")
    print(f"d(16) <= {2*A16_HI:.15f}   (repo certificate, separation 2)")
    print(f"s(16) <= {m_to_s(float(M16_LO)):.15f}   (unit circles)")
    print(f"abort-and-exactify trigger: m > {TRIGGER_M:.18f}")
