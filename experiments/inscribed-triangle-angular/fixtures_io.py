"""Read the sibling experiment's committed fixtures as DATA.

`experiments/inscribed-triangle-polygons/out/fixtures/*.json` is a committed artifact of
another lane.  This module reads those files and nothing else: it imports no code from that
directory, so the two deciders share only the polygon coordinates and the recorded answers
that are being compared.  The files are never written.
"""

from __future__ import annotations

import json
import os
from fractions import Fraction

from q3 import Q3

SIBLING = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "inscribed-triangle-polygons", "out", "fixtures"))


def _q(p):
    """["a","b"] -> a + b*sqrt3."""
    return Q3(Fraction(p[0]), Fraction(p[1]))


def load_all(path=None):
    path = path or SIBLING
    names = sorted(f for f in os.listdir(path) if f.endswith(".json"))
    out = []
    for f in names:
        with open(os.path.join(path, f)) as fh:
            d = json.load(fh)
        d["_poly"] = [(_q(v[0]), _q(v[1])) for v in d["vertices_exact"]]
        out.append(d)
    return out
