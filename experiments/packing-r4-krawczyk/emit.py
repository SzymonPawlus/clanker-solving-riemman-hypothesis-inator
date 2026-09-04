"""Certificate emission in the schema of
problems/circle-packing-equilateral-triangle/RULES.md §2.

CONSTRUCTION (upper bound) ONLY.  Nothing emitted here is an optimality claim.
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import isqrt

S3_SCALE = 10 ** 50
_S3_LO = Fraction(isqrt(3 * S3_SCALE * S3_SCALE), S3_SCALE)
_S3_HI = _S3_LO + Fraction(1, S3_SCALE)


def fstr(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def ystr(u: Fraction) -> str:
    """y = u * sqrt(3), as an exact algebraic expression (never a decimal string)."""
    if u == 0:
        return "0"
    if u.denominator == 1:
        return f"{u.numerator}*sqrt(3)"
    return f"{u.numerator}/{u.denominator}*sqrt(3)"


def _floor_to(q: Fraction, den: int) -> Fraction:
    return Fraction((q.numerator * den) // q.denominator, den)


def _ceil_to(q: Fraction, den: int) -> Fraction:
    return Fraction(-((-q.numerator * den) // q.denominator), den)


def y_bounds(u: Fraction, den: int = S3_SCALE) -> tuple[Fraction, Fraction]:
    """Rational enclosure of u*sqrt(3) for u >= 0."""
    assert u >= 0
    return _floor_to(u * _S3_LO, den), _ceil_to(u * _S3_HI, den)


def algebraic_certificate(n, w, rep, meta) -> dict:
    coords = [[fstr(w["xs"][i]), ystr(w["us"][i])] for i in range(n)]
    return {
        "n": n,
        "claim": "construction",
        "side_length": f"2*sqrt(3) + {fstr(w['d'])}",
        "coordinates": coords,
        "coordinate_type": "algebraic",
        "verified_by": (
            "experiments/packing-r4-krawczyk/witness.py verify_exact() -- exact rational "
            "arithmetic in the sheared coordinates (x, u) with y = sqrt(3)*u, stdlib Fraction "
            "only, no float in any accept/reject decision. SELF-CHECKED ONLY: under "
            "problems/circle-packing-equilateral-triangle/RULES.md §3 this earns "
            "verified:review only from a checker written independently by an agent of a "
            "different model family. That has not happened."
        ),
        "status": "numerical",
        "beats_record": meta["beats_record"],
        "_claim_is_upper_bound_only": (
            "This certifies s(n) <= the stated side length. It says nothing about optimality."
        ),
        "_tight": rep["tight"],
        "_min_squared_distance": fstr(rep["min_squared_distance"]),
        "_contacts_at_distance_exactly_2": rep["contacts_exactly_2"],
        "_points_on_the_boundary": rep["boundary_points"],
        "_repair_factor_lambda_minus_1": fstr(w["lam"] - 1),
        "_provenance": meta["provenance"],
        "_krawczyk": meta["krawczyk"],
    }


def interval_certificate(n, w, meta, shift: Fraction, pad: Fraction) -> tuple[dict, dict]:
    """Interval-typed certificate: EVERY selection of one point per box is a valid packing.

    y = u*sqrt(3) is irrational, so a box around a wall-AC point would poke outside the
    triangle.  The whole configuration is therefore translated right by the rational
    ``shift`` first.  A translation in x changes no pairwise distance at all, keeps
    u >= 0, and only improves x - u >= 0; d grows by exactly ``shift``.  ``pad`` then buys
    room for the BC wall against the outward-rounded y endpoints.
    """
    xs = [v + shift for v in w["xs"]]
    us = w["us"]
    boxes = []
    for i in range(n):
        ylo, yhi = y_bounds(us[i])
        boxes.append((xs[i], xs[i], ylo, yhi))
    d = max(xs[i] + us[i] for i in range(n)) + pad
    ok_sep = True
    m2 = None
    for i in range(n):
        for j in range(i + 1, n):
            dx = boxes[i][0] - boxes[j][0]
            lo = boxes[i][2] - boxes[j][3]
            hi = boxes[i][3] - boxes[j][2]
            if lo <= 0 <= hi:
                dy2 = Fraction(0)
            else:
                mn = min(abs(lo), abs(hi))
                dy2 = mn * mn
            q = dx * dx + dy2
            m2 = q if m2 is None or q < m2 else m2
            if q < 4:
                ok_sep = False
    ok_con = True
    for xlo, xhi, ylo, yhi in boxes:
        if ylo < 0 or xlo < 0:
            ok_con = False
        if not (3 * xlo * xlo >= yhi * yhi):
            ok_con = False
        if d - xhi < 0 or not (3 * (d - xhi) ** 2 >= yhi * yhi):
            ok_con = False
    cert = {
        "n": n,
        "claim": "construction",
        "side_length": f"2*sqrt(3) + {fstr(d)}",
        "coordinates": [
            [[fstr(b[0]), fstr(b[1])], [fstr(b[2]), fstr(b[3])]] for b in boxes
        ],
        "coordinate_type": "interval",
        "verified_by": (
            "experiments/packing-r4-krawczyk/emit.py interval_certificate() -- exact rational "
            "endpoints, exact rational comparisons, no float in any decision. "
            "SELF-CHECKED ONLY."
        ),
        "status": "numerical",
        "beats_record": meta["beats_record"],
        "_semantics": (
            "UNIVERSALLY QUANTIFIED: for every choice of one point from each coordinate box, "
            "all C(n,2) pairwise distances are >= 2 and every chosen point lies in the closed "
            "triangle A=(0,0), B=(d,0), C=(d/2, d*sqrt(3)/2) with d = side_length - 2*sqrt(3). "
            "Hence s(n) <= side_length. This is an honest upper bound and is NOT tight: the "
            "declared d exceeds the box-minimal enclosing side by less than " + fstr(pad)
            + ", and the configuration was translated right by " + fstr(shift)
            + " (a translation changes no pairwise distance). The exactly-tight version of "
            "the same packing is the algebraic certificate n" + f"{n:03d}" + "-r4-krawczyk.json."
        ),
        "_claim_is_upper_bound_only": (
            "This certifies s(n) <= the stated side length. It says nothing about optimality."
        ),
        "_tight": False,
        "_min_squared_distance_lower_bound_over_boxes": fstr(m2),
        "_provenance": meta["provenance"],
        "_krawczyk": meta["krawczyk"],
    }
    return cert, {"separation_ok": ok_sep, "containment_ok": ok_con}


def write(path, obj):
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=2)
        fh.write("\n")
