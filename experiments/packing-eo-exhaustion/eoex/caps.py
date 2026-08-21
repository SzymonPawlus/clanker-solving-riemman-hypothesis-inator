"""How many separation-2 points fit in a closed equilateral triangle of side ``side``.

Three independent sound caps, combined by ``min``:

* **diameter** — a triangle of side < 2 has diameter < 2, so it holds at most one point.
  Depends on nothing.
* **Oler** — ``floor(side^2/8 + 3*side/4 + 1)``.  Depends on Oler (1961), `cited`.
* **cited d(k)** — if ``side < d(k+1)`` then at most ``k`` points fit, using the cited
  optimal values for ``k+1 <= 15``.  Depends on the literature table in the problem
  README, `cited`.

``max_cited`` bounds which of the third family may be used; ``max_cited = 1`` switches it
off entirely and ``use_oler = False`` switches the second off, leaving a run that depends
on no external claim at all.
"""

from __future__ import annotations

from fractions import Fraction

from .algebraic import MAX_CITED, strictly_less_than_cited_d
from .oler import cell_capacity_oler


def capacity(side: Fraction, n: int, max_cited: int = MAX_CITED, use_oler: bool = True) -> int:
    """Upper bound on the number of separation-2 points in a closed triangle of side ``side``."""
    cap = n
    if side < 2:
        cap = 1
        return cap
    if use_oler:
        cap = min(cap, cell_capacity_oler(side))
    for k in range(2, min(max_cited, MAX_CITED) + 1):
        verdict = strictly_less_than_cited_d(side, k)
        if verdict:
            cap = min(cap, k - 1)
            break
    return max(cap, 1)
