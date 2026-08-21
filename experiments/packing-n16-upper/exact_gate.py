"""Checker A — the exact rational gate, in triangular (oblique) coordinates.

Built BEFORE any optimiser was run.  Problem ``RULES.md`` SS0: every optimiser returns a slightly
infeasible configuration and reports a record, and that result is always wrong.  So the decision
procedure is exact rational arithmetic with **no tolerance anywhere**, and a float configuration
is only ever a hypothesis handed to it.

Coordinates
-----------
Write a point as ``P = u*e1 + v*e2`` with ``e1 = (1,0)``, ``e2 = (1/2, sqrt(3)/2)``.  Then

    T_L = { (u, v) : u >= 0, v >= 0, u + v <= L }

is the equilateral triangle ``conv{(0,0), (L,0), (L/2, L*sqrt(3)/2)}`` -- the placement fixed by
problem ``RULES.md`` SS2 -- and for two points

    |PQ|^2 = (du + dv/2)^2 + 3*dv^2/4 = du^2 + du*dv + dv^2.

Both the containment test and the squared distance are therefore **rational**; no sqrt(3) enters
anywhere, so there is nothing to round.

What the gate decides
---------------------
Given exact rational points with ``u_i, v_i >= 0``:

    L_min  = max_i (u_i + v_i)                 the exact minimal enclosing side for this placement
    q_min  = min_{i<j} (du^2 + du*dv + dv^2)   the exact minimal squared separation

Scaling by ``1/sqrt(q_min)`` makes the minimum separation exactly 1 in a triangle of side
``a = L_min / sqrt(q_min)``, and the unit-triangle figure of merit is ``m = sqrt(q_min)/L_min``.
Comparing ``a`` against a record ``a_rec = 1/m_rec`` with ``m_rec`` rational is then the single
exact rational comparison

    a < a_rec   <==>   q_min > L_min^2 * m_rec^2.

No square root is ever taken to make a decision; the float values printed are for reading only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence

from normalisation import M16_HI, M16_LO, SQRT3

Rat = Fraction
Pt = tuple[Rat, Rat]


# --------------------------------------------------------------------------------------------
# rationalisation:  float (x, y) in the unit triangle  ->  exact (u, v) with u, v >= 0
# --------------------------------------------------------------------------------------------


def to_uv_float(x: float, y: float) -> tuple[float, float]:
    """Cartesian -> triangular.  Inverse of (u, v) -> (u + v/2, v*sqrt(3)/2)."""
    v = 2.0 * y / SQRT3
    u = x - y / SQRT3
    return u, v


def rationalise(points_xy: Sequence[Sequence[float]], max_den: int = 10**7) -> list[Pt]:
    """Round a float configuration to nearby rationals in triangular coordinates.

    Negative coordinates are clamped to exactly zero.  Clamping is a *modification* of the
    configuration, not a repair of a rounding error: the gate then measures the clamped
    configuration and reports facts about it.  That is the honest reading -- the object being
    certified is the rational one, never the float one it came from.
    """
    out: list[Pt] = []
    for x, y in points_xy:
        uf, vf = to_uv_float(float(x), float(y))
        u = Fraction(uf).limit_denominator(max_den)
        v = Fraction(vf).limit_denominator(max_den)
        if u < 0:
            u = Fraction(0)
        if v < 0:
            v = Fraction(0)
        out.append((u, v))
    return out


# --------------------------------------------------------------------------------------------
# the exact measurements
# --------------------------------------------------------------------------------------------


def sq_dist(p: Pt, q: Pt) -> Rat:
    du = p[0] - q[0]
    dv = p[1] - q[1]
    return du * du + du * dv + dv * dv


def min_sq_dist(pts: Sequence[Pt]) -> tuple[Rat, tuple[int, int]]:
    best: Rat | None = None
    pair = (-1, -1)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            q = sq_dist(pts[i], pts[j])
            if best is None or q < best:
                best, pair = q, (i, j)
    assert best is not None
    return best, pair


def minimal_side(pts: Sequence[Pt]) -> Rat:
    """Exact minimal L with every point in T_L.  Requires u, v >= 0 (checked by ``contained``)."""
    return max(u + v for u, v in pts)


def contained(pts: Sequence[Pt], L: Rat) -> tuple[bool, list[int]]:
    """Exact containment in T_L.  Non-strict, per problem ``RULES.md`` SS2."""
    bad = [i for i, (u, v) in enumerate(pts) if u < 0 or v < 0 or u + v > L]
    return (not bad), bad


@dataclass
class GateResult:
    n: int
    q_min: Rat
    closest_pair: tuple[int, int]
    L_min: Rat
    contained_ok: bool
    bad_points: list[int]
    m_exact_sq: Rat  # = q_min / L_min^2 ; the square of the unit-triangle figure of merit

    @property
    def m(self) -> float:
        return math.sqrt(float(self.m_exact_sq))

    @property
    def a(self) -> float:
        """separation-1 side length."""
        return 1.0 / self.m

    def beats(self, m_rec: Rat) -> bool:
        """Exact: is this configuration's side strictly below the side implied by ``m_rec``?"""
        return self.m_exact_sq > m_rec * m_rec

    def matches(self, lo: Rat, hi: Rat) -> bool:
        return lo * lo <= self.m_exact_sq <= hi * hi


def gate(pts: Sequence[Pt]) -> GateResult:
    q, pair = min_sq_dist(pts)
    L = minimal_side(pts)
    ok, bad = contained(pts, L)
    return GateResult(
        n=len(pts),
        q_min=q,
        closest_pair=pair,
        L_min=L,
        contained_ok=ok,
        bad_points=bad,
        m_exact_sq=q / (L * L),
    )


def verdict_n16(pts: Sequence[Pt]) -> str:
    g = gate(pts)
    if not g.contained_ok:
        return "INFEASIBLE (containment)"
    if g.beats(M16_HI):
        return "BEATS the Melissen-Schuur record  -- STOP, run the RULES.md SS7 procedure"
    if g.matches(M16_LO, M16_HI):
        return "matches the record inside its printed 15-s.f. window"
    return "does not beat the record"


# --------------------------------------------------------------------------------------------
# certificate emission at separation 2 (the repo's convention)
# --------------------------------------------------------------------------------------------


def rational_certificate_scale(q_min: Rat, extra_den: int = 10**9) -> Rat:
    """Smallest convenient rational ``c`` with ``c^2 * q_min >= 4``, i.e. separations >= 2.

    ``2/sqrt(q_min)`` is irrational in general, so an exactly-tight rational certificate does not
    exist; we round the scale *up*, which keeps every separation >= 2 and the side an honest
    upper bound.  ``RULES.md`` SS2 calls that untight, and it must be reported as such.
    """
    target = 2.0 / math.sqrt(float(q_min))
    c = Fraction(target).limit_denominator(extra_den)
    while c * c * q_min < 4:
        c += Fraction(1, extra_den)
    return c
