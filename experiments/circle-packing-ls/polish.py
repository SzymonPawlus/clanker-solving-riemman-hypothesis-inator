"""Adapter onto the polisher that already exists in ``experiments/circle-packing-search``.

Issue #12 asks for LS to be a **front end**: it finds basins, the existing SLSQP solve
finds the last several digits inside one.  Reimplementing that solve here would be
duplicated code, and — more importantly — it would wreck the comparison the issue
actually asks for.  The kill-criterion is "does LS seeding beat random seeding at equal
compute", and that question only has an answer if *both* arms descend with the identical
polisher.  So this module imports ``search.py`` rather than copying it.

``experiments/circle-packing-search/**`` is read-only from here: we import it, we never
write to it.  Nothing else in this directory depends on that package, so if it moves,
only this file breaks.
"""

from __future__ import annotations

import pathlib
import sys

import numpy as np

_SEARCH = (pathlib.Path(__file__).resolve().parent.parent / "circle-packing-search").resolve()
if str(_SEARCH) not in sys.path:
    sys.path.insert(0, str(_SEARCH))

import search as _search  # noqa: E402  (path must be set first)

__all__ = ["polish", "local_solve", "min_pair_distance", "sample_uniform", "sample_lattice"]

local_solve = _search.local_solve
min_pair_distance = _search.min_pair_distance
sample_uniform = _search.sample_uniform
sample_lattice = _search.sample_lattice


def polish(p: np.ndarray, rounds: int = 4) -> tuple[np.ndarray, float]:
    """Warm-restart SLSQP from its own output until it stops improving.

    Identical in behaviour to ``experiments/circle-packing-search/run.py``'s ``polish``
    (same function, same defaults), reproduced here only because ``run.py`` is a CLI
    module and importing it would execute its argument parsing.
    """
    best_p, best_m = p, min_pair_distance(p)
    for _ in range(rounds):
        q, m = local_solve(best_p, maxiter=500, ftol=1e-16)
        if m > best_m:
            best_p, best_m = q, m
    return best_p, best_m
