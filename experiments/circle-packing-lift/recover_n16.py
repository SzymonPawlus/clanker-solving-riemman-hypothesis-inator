#!/usr/bin/env python3
"""Reproduce the numerical integer-relation candidate for the n=16 separation.

Run through ``recover_n16.sh`` so mpmath is the version pinned by the neighbouring
search experiment.  PSLQ is evidence only: the emitted polynomial is not known to
vanish exactly until an algebraic elimination/certification step proves it.
"""

from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp

from lift import extract_contacts, load_candidate, obvious_rattlers
from solve import solve_candidate

EXPECTED = (9, -246, 3112, -23836, 121624, -429448, 1055998, -1772356, 1925755, -1211242, 331654)


def recover() -> dict:
    root = Path(__file__).resolve().parent
    candidate = load_candidate(root.parent / "circle-packing-search" / "out" / "n16.json")
    graph = extract_contacts(candidate, 1e-10)
    point_ids = tuple(i for i in range(candidate.n) if i not in obvious_rattlers(candidate, graph))
    solved = solve_candidate(candidate, graph, point_ids, digits=260)

    mp.mp.dps = 250
    value = mp.mpf(str(solved.m))
    relation = None
    degree = None
    for candidate_degree in range(1, 11):
        relation = mp.pslq(
            mp.matrix([value**power for power in range(candidate_degree + 1)]),
            tol=mp.mpf("1e-220"),
            maxcoeff=10**8,
            maxsteps=10_000,
        )
        if relation:
            degree = candidate_degree
            break
    coefficients = tuple(map(int, relation)) if relation else ()
    if degree != 10 or coefficients != EXPECTED:
        raise AssertionError(f"unexpected first relation: degree={degree}, coefficients={coefficients}")
    residual = sum(mp.mpf(coefficient) * value**power for power, coefficient in enumerate(coefficients))
    return {
        "status": "numerical",
        "n": 16,
        "m_250_digits": mp.nstr(value, 250),
        "coefficient_order": "constant term first",
        "polynomial_coefficients": list(coefficients),
        "first_relation_degree_searched_through": degree,
        "pslq_tolerance": "1e-220",
        "pslq_max_coefficient": 10**8,
        "absolute_residual": mp.nstr(abs(residual), 20),
        "warning": "PSLQ relation only; exact vanishing and minimality are not proved",
    }


if __name__ == "__main__":
    print(json.dumps(recover(), indent=2))
