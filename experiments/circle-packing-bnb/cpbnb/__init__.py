"""Interval / exact-integer branch-and-bound for lower bounds on d(n).

See ``README.md``.  Nothing in this package establishes an exact optimum; the strongest
thing it can produce is ``d(n) > d`` for one explicit rational ``d``.
"""

from .search import Prover  # noqa: F401

__all__ = ["Prover"]
