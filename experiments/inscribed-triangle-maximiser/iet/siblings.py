"""Read-only adapters onto the two committed deciders.

`experiments/inscribed-triangle-polygons/` and `experiments/inscribed-triangle-angular/`
belong to other lanes.  This module IMPORTS them and never writes to them (bytecode caching
is switched off before the import so that not even a `__pycache__` entry appears).  It exists
so that every triangle this lane reports can be re-checked by two verifiers written by other
authors, and so that this lane's `side2 > 0` can be compared against their booleans.
"""

from __future__ import annotations

import os
import sys

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

_HERE = os.path.dirname(os.path.abspath(__file__))
_EXP = os.path.dirname(os.path.dirname(_HERE))
POLY_DIR = os.path.join(_EXP, "inscribed-triangle-polygons")
ANG_DIR = os.path.join(_EXP, "inscribed-triangle-angular")
FIXTURE_DIR = os.path.join(POLY_DIR, "out", "fixtures")

for _d in (POLY_DIR, ANG_DIR):
    if _d not in sys.path:
        sys.path.append(_d)

import geom as _geom        # noqa: E402  (the polygons lane)
import k3 as _k3            # noqa: E402
import angular as _ang      # noqa: E402  (the angular lane)
import q3 as _q3            # noqa: E402

__all__ = ["to_poly_pt", "to_ang_pt", "poly_decide", "poly_verify",
           "ang_decide", "ang_verify", "load_fixture", "fixture_names"]


def to_poly_pt(p):
    """A point of this lane -> a point of the polygons lane (its own K)."""
    return (_k3.K(_frac(p[0])[0], _frac(p[0])[1]), _k3.K(_frac(p[1])[0], _frac(p[1])[1]))


def to_ang_pt(p):
    """A point of this lane -> a point of the angular lane (its own Q3)."""
    return (_q3.Q3(*_frac(p[0])), _q3.Q3(*_frac(p[1])))


def _frac(x):
    from fractions import Fraction
    return (Fraction(x.a, x.c), Fraction(x.b, x.c))


def poly_decide(poly, O):
    return _geom.decide_good([to_poly_pt(p) for p in poly], to_poly_pt(O))


def poly_verify(poly, O, P, Q):
    return _geom.verify_triangle([to_poly_pt(p) for p in poly],
                                 to_poly_pt(O), to_poly_pt(P), to_poly_pt(Q))


def ang_decide(poly, O):
    ok, wit = _ang.decide(to_ang_pt(O), [to_ang_pt(p) for p in poly])
    return ok, wit


def ang_verify(poly, O, P, Q):
    return _ang.recheck_witness([to_ang_pt(p) for p in poly],
                                to_ang_pt(O), to_ang_pt(P), to_ang_pt(Q))


def fixture_names():
    return sorted(f[:-5] for f in os.listdir(FIXTURE_DIR) if f.endswith(".json"))


def load_fixture(name):
    """The committed fixture's vertex list, as points of THIS lane."""
    import json
    from .qs3 import Q3
    with open(os.path.join(FIXTURE_DIR, name + ".json")) as fh:
        d = json.load(fh)
    poly = [(Q3.from_pair(p[0]), Q3.from_pair(p[1])) for p in d["vertices_exact"]]
    return poly, d
