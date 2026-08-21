"""Emit exact algebraic certificates (constructions / UPPER bounds only) for issue #74.

Every configuration here is written as exact algebraic coordinates. Nothing in this file is an
optimality claim: a feasible packing witnesses s(n) <= c and says nothing whatever about whether
some other packing does better. The published values quoted in the `matches_published` field come
from the `cited` table in problems/circle-packing-equilateral-triangle/README.md and are used only
as a target to reproduce, never as evidence produced here.

Derivations are recorded in
problems/circle-packing-equilateral-triangle/attacks/exact-algebraic-constructions/README.md.

Run:  python3 construct.py --out <dir>   then   python3 exact_check.py --dir <dir>
"""
from __future__ import annotations

import argparse
import json
import pathlib


def sq3(k: int) -> str:
    """Exact string for k*sqrt(3)."""
    if k == 0:
        return "0"
    if k == 1:
        return "sqrt(3)"
    return f"{k}*sqrt(3)"


def lattice(k: int):
    """The triangular lattice T(k): k(k+1)/2 points at mutual distance >= 2, d = 2(k-1).

    Row r (r = 0 is the bottom) holds k - r points at (2j + r, r*sqrt(3)), j = 0..k-1-r.
    """
    pts = []
    for r in range(k):
        for j in range(k - r):
            pts.append((str(2 * j + r), sq3(r)))
    return pts


def side_from_d_int(d: int) -> str:
    return "2*sqrt(3)" if d == 0 else f"{d} + 2*sqrt(3)"


def build():
    """Return {n: certificate dict}."""
    certs = {}

    # ---- family 1: full triangular lattice, n = k(k+1)/2, d = 2(k-1) ----------
    for k in range(1, 7):
        n = k * (k + 1) // 2
        d = 2 * (k - 1)
        certs[n] = dict(
            coordinates=lattice(k),
            side_length=side_from_d_int(d),
            point_triangle_side=str(d) if d else "0",
            construction=f"full triangular lattice T({k}) of side {d}",
            matches_published=side_from_d_int(d),
        )

    # ---- family 2: lattice minus the apex, n = k(k+1)/2 - 1, same d ----------
    # (the Erdos-Oler configuration; we assert only that it is FEASIBLE at this d)
    for k in range(2, 7):
        n = k * (k + 1) // 2 - 1
        d = 2 * (k - 1)
        pts = lattice(k)
        apex = (str(k - 1), sq3(k - 1))
        pts = [p for p in pts if p != apex]
        assert len(pts) == n
        certs[n] = dict(
            coordinates=pts,
            side_length=side_from_d_int(d),
            point_triangle_side=str(d) if d else "0",
            construction=f"triangular lattice T({k}) of side {d} with the apex point removed",
            matches_published=side_from_d_int(d),
        )

    # ---- n = 4: three corners plus the centroid, d = 2*sqrt(3) ---------------
    # centroid is at distance d/sqrt(3) = 2 from each corner, so all four contacts are exact.
    certs[4] = dict(
        coordinates=[("0", "0"), ("2*sqrt(3)", "0"), ("sqrt(3)", "3"), ("sqrt(3)", "1")],
        side_length="4*sqrt(3)",
        point_triangle_side="2*sqrt(3)",
        construction="three corners of the point-triangle plus its centroid",
        matches_published="4*sqrt(3)",
    )

    # ---- n = 7: d = 2 + 2*sqrt(3) -------------------------------------------
    # three corners; one point at distance 2 from A along AC and its mirror on BC; the point
    # (d/2, d/2) contacting both of those and the apex; and one RATTLER, placed at (d/2, 0).
    certs[7] = dict(
        coordinates=[
            ("0", "0"),
            ("2 + 2*sqrt(3)", "0"),
            ("1 + sqrt(3)", "3 + sqrt(3)"),
            ("1", "sqrt(3)"),
            ("1 + 2*sqrt(3)", "sqrt(3)"),
            ("1 + sqrt(3)", "1 + sqrt(3)"),
            ("1 + sqrt(3)", "0"),
        ],
        side_length="2 + 4*sqrt(3)",
        point_triangle_side="2 + 2*sqrt(3)",
        construction="three corners + two edge points at distance 2 from A and B + the point "
                     "(d/2, d/2) + one rattler at (d/2, 0)",
        matches_published="2 + 4*sqrt(3)",
    )

    # ---- n = 8: d = 2 + 2*sqrt(33)/3 ----------------------------------------
    # bottom row of three, a symmetric pair at height sqrt(11)/2 - sqrt(3)/6, a symmetric pair on
    # the two slanted edges at height sqrt(11), and the apex. d solves the contact system; see the
    # attack README.
    certs[8] = dict(
        coordinates=[
            ("0", "0"),
            ("1 + sqrt(33)/3", "0"),
            ("2 + 2*sqrt(33)/3", "0"),
            ("1/2 + sqrt(33)/6", "sqrt(11)/2 - sqrt(3)/6"),
            ("3/2 + sqrt(33)/2", "sqrt(11)/2 - sqrt(3)/6"),
            ("sqrt(33)/3", "sqrt(11)"),
            ("2 + sqrt(33)/3", "sqrt(11)"),
            ("1 + sqrt(33)/3", "sqrt(3) + sqrt(11)"),
        ],
        side_length="2 + 2*sqrt(3) + 2*sqrt(33)/3",
        point_triangle_side="2 + 2*sqrt(33)/3",
        construction="bottom row of 3; symmetric pair at height sqrt(11)/2 - sqrt(3)/6; "
                     "symmetric pair on edges AC/BC at height sqrt(11); apex",
        matches_published="2 + 2*sqrt(3) + 2*sqrt(33)/3",
    )

    return certs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=pathlib.Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)

    certs = build()
    for n in sorted(certs):
        c = certs[n]
        doc = {
            "n": n,
            "claim": "construction",
            "_claim_note": "UPPER BOUND ONLY: this is an explicit feasible packing witnessing "
                           "s(n) <= side_length. It is NOT an optimality proof and carries no "
                           "lower-bound content whatsoever.",
            "side_length": c["side_length"],
            "point_triangle_side": c["point_triangle_side"],
            "coordinates": [list(p) for p in c["coordinates"]],
            "coordinate_type": "algebraic",
            "tight": True,
            "construction": c["construction"],
            "verified_by": "experiments/packing-exact-algebraic/exact_check.py "
                           "(independent exact-arithmetic checker, issue #74)",
            "status": "sketch",
            "matches_published_upper_bound": c["matches_published"],
            "beats_record": "no - reproduces the value already tabulated in this problem's "
                            "README; upper bound only, no optimality claim",
        }
        p = a.out / f"n{n:03d}-exact.json"
        p.write_text(json.dumps(doc, indent=1) + "\n")
        print(f"wrote {p}")


if __name__ == "__main__":
    main()
