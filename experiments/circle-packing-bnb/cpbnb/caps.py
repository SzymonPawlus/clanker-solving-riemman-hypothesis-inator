"""Capacity bounds for a sub-triangle, from the *cited* optimal side lengths.

Point formulation (``problems/circle-packing-equilateral-triangle/README.md``):
``d(k)`` is the smallest side of an equilateral triangle admitting ``k`` points at mutual
distance ``>= 2``, and ``s(k) = 2*sqrt(3) + d(k)``.

Every entry below is `cited` -- it is the ``s(k)`` column of the problem README's
"Proven optimal, n <= 15" table, minus ``2*sqrt(3)``.  Nothing here is derived by this
experiment, and this module is the *only* place where the search consumes an external
mathematical claim.  ``--max-cited`` in the CLI caps which entries may be used, so a run
can be made to depend on nothing beyond ``d(2) = 2`` (the triangle inequality's worth of
input: two points at distance >= 2 need side >= 2).

Rigour.  ``d(k)`` is algebraic, the cell side is an exact rational, so the comparison is
done by enclosing ``d(k)`` in an outward-rounded interval (``cpbnb/interval.py``) and
testing ``lo(d(k)) > side`` exactly in :class:`fractions.Fraction`.  The test therefore
fires only when ``d(k) > side`` really holds; when the enclosure is too wide to decide,
the answer is "no bound", which loses pruning but never soundness.
"""

from __future__ import annotations

from fractions import Fraction

from .interval import Interval, isqrt_interval

_ONE = Interval.exact(1.0)


def _i(k: int) -> Interval:
    return Interval.from_int(k)


def _d_table() -> dict[int, Interval]:
    """Enclosures of d(k) for k = 2..15.  Source: problem README, ``s(k) - 2*sqrt(3)``."""
    sqrt3 = isqrt_interval(3)
    sqrt6 = isqrt_interval(6)
    sqrt33 = isqrt_interval(33)
    three = _i(3)
    return {
        # d(2) = d(3) = 2 -- two points at distance 2 need side 2 (trivial / Oler n=3).
        2: _i(2),
        3: _i(2),
        # s(4) = 4*sqrt(3)                      -> d(4) = 2*sqrt(3)
        4: _i(2) * sqrt3,
        # s(5) = s(6) = 4 + 2*sqrt(3)           -> d = 4
        5: _i(4),
        6: _i(4),
        # s(7) = 2 + 4*sqrt(3)                  -> d = 2 + 2*sqrt(3)
        7: _i(2) + _i(2) * sqrt3,
        # s(8) = 2 + 2*sqrt(3) + 2*sqrt(33)/3   -> d = 2 + 2*sqrt(33)/3
        8: _i(2) + (_i(2) * sqrt33) / three,
        # s(9) = s(10) = 6 + 2*sqrt(3)          -> d = 6
        9: _i(6),
        10: _i(6),
        # s(11) = 4 + 2*sqrt(3) + 4*sqrt(6)/3   -> d = 4 + 4*sqrt(6)/3
        11: _i(4) + (_i(4) * sqrt6) / three,
        # s(12) = 4 + 4*sqrt(3)                 -> d = 4 + 2*sqrt(3)
        12: _i(4) + _i(2) * sqrt3,
        # s(13) = 4 + 2*sqrt(6)/3 + 10*sqrt(3)/3 -> d = 4 + 2*sqrt(6)/3 + 4*sqrt(3)/3
        13: _i(4) + (_i(2) * sqrt6) / three + (_i(4) * sqrt3) / three,
        # s(14) = s(15) = 8 + 2*sqrt(3)         -> d = 8
        14: _i(8),
        15: _i(8),
    }


D_ENCLOSURE = _d_table()

#: Largest ``k`` for which an optimal ``d(k)`` is cited in the problem README.
MAX_CITED = max(D_ENCLOSURE)


def capacity(side: Fraction, max_cited: int) -> int | None:
    """Upper bound on the number of points at mutual distance ``>= 2`` in ``T(side)``.

    ``side`` is the exact side length of the (equilateral) cell.  Returns ``None`` when no
    entry ``k <= max_cited`` proves a bound, i.e. when the cell is at least as large as
    every cited ``d(k)`` available.
    """
    if side < 0:
        raise ValueError("negative side")
    for k in range(2, min(max_cited, MAX_CITED) + 1):
        if D_ENCLOSURE[k].gt_fraction(side):
            # side < d(k)  =>  at most k-1 points fit.
            return k - 1
    return None


def capacity_by_level(d: Fraction, levels: int, max_cited: int) -> list[int | None]:
    """``capacity`` for each subdivision level ``0..levels`` (cell side ``d / 2**L``)."""
    return [capacity(d / (1 << level), max_cited) for level in range(levels + 1)]
