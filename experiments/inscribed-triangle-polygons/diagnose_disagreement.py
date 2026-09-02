"""Adjudicate the disagreements between geom.py and sympy's geometry (issue #132).

`crosscheck_sympy.py` found three vertices where the two implementations disagree. A
disagreement means at least one is wrong, so it has to be settled, not averaged. This script
settles it three ways, the first of which does not trust either implementation:

  1. A PROOF, in exact rational arithmetic, that each disputed vertex is NOT good. The disputed
     fixtures are convex, so the whole polygon lies in the closed cone of the interior angle at
     the vertex; if that angle is < 60 degrees the rotated cone meets the original only at the
     vertex, so rho(J) & J = {O} and O cannot be good. The angle test reduces to a single
     comparison of integers.
  2. A demonstration that sympy's own witness fails sympy's own containment test at high
     precision -- i.e. sympy contradicts itself, rather than my code being the odd one out.
  3. The same witness re-tested in exact Q(sqrt 3) arithmetic.

    python3 diagnose_disagreement.py
"""

from __future__ import annotations

import json
import os
from fractions import Fraction as F

import sympy as sp
from sympy.geometry import Point2D, Segment2D

from k3 import K
from geom import (point_on_polygon, vertex_angle_class, decide_good, psub, cross, dot,
                  rot60)
from fixtures import battery
from crosscheck_sympy import to_sp, rot

HERE = os.path.dirname(os.path.abspath(__file__))
S3 = sp.sqrt(3)

DISPUTED = [("cvx-iso-t5773502691896257_10000000000000000", 0),
            ("cvx-iso-t5773502691896258_10000000000000000", 1),
            ("cvx-iso-t5773502691896258_10000000000000000", 2)]


def cone_proof(poly, i):
    """Exact proof that vertex i of a CONVEX polygon with interior angle < 60 is not good.

    With u, w the two edge vectors at the vertex, c = u.w and s = u x w, the interior angle
    theta of a convex vertex satisfies tan theta = |s|/c when c > 0, so
        theta < 60  <=>  c > 0 and s^2 < 3c^2.
    Both sides are exact numbers in Q(sqrt 3); for a rational polygon they are rational, and
    the comparison is a comparison of integers after clearing denominators.

    Given theta < 60: the polygon is convex, so it lies in the closed cone of angle theta at the
    vertex. Rotating that cone by +-60 degrees produces a cone spanning angles [60, 60+theta] or
    [-60, theta-60], and [0, theta] meets either of those only at the apex when theta < 60.
    Hence rho(J) & J = {O} and the vertex is not good -- no computation over segment pairs
    required.
    """
    n = len(poly)
    V, U, W = poly[i], poly[(i - 1) % n], poly[(i + 1) % n]
    u, w = psub(U, V), psub(W, V)
    c, s = dot(u, w), cross(u, w)
    lhs = s * s
    rhs = K(3) * c * c
    return {
        "c_positive": c.sign() > 0,
        "s_squared": lhs.as_pair(),
        "three_c_squared": rhs.as_pair(),
        "s_squared_lt_3c_squared": (lhs - rhs).sign() < 0,
        "therefore_interior_angle_lt_60": c.sign() > 0 and (lhs - rhs).sign() < 0,
        "therefore_not_good": c.sign() > 0 and (lhs - rhs).sign() < 0,
    }


def sympy_witness(spoly, O):
    n = len(spoly)
    segs = [Segment2D(spoly[k], spoly[(k + 1) % n]) for k in range(n)]
    for sigma in (1, -1):
        rsegs = [Segment2D(rot(spoly[k], O, sigma), rot(spoly[(k + 1) % n], O, sigma))
                 for k in range(n)]
        for ri, rs in enumerate(rsegs):
            for si, s in enumerate(segs):
                for obj in rs.intersection(s):
                    pts = [obj] if isinstance(obj, Point2D) else [obj.p1, obj.p2]
                    for X in pts:
                        if X != O:
                            return {"sigma": sigma, "rot_edge": ri, "edge": si, "X": X,
                                    "claimed_on_orig": segs[si], "claimed_on_rot": rs}
    return None


def from_sp(e):
    """sympy expression in Q(sqrt3) -> K. Raises if it is not of that form."""
    e = sp.expand(sp.nsimplify(e))
    b = sp.expand(e.coeff(S3))
    a = sp.expand(e - b * S3)
    assert a.is_rational and b.is_rational, (a, b)
    return K(F(sp.Rational(a)), F(sp.Rational(b)))


def main():
    fx = {f["name"]: f for f in battery()}
    out = []
    for name, vi in DISPUTED:
        poly = fx[name]["poly"]
        rec = {"fixture": name, "vertex": vi,
               "interior_angle_display_deg": vertex_angle_class(poly, vi)["degrees_display"],
               "my_verdict_good": decide_good(poly, poly[vi])["good"]}
        rec["proof_1_cone"] = cone_proof(poly, vi)

        spoly = [to_sp(p) for p in poly]
        O = spoly[vi]
        w = sympy_witness(spoly, O)
        rec["sympy_claims_good"] = w is not None
        if w is not None:
            X = w["X"]

            def colin(seg):
                A, B = seg.p1, seg.p2
                return sp.N((B.x - A.x) * (X.y - A.y) - (B.y - A.y) * (X.x - A.x), 60)

            c_orig = colin(w["claimed_on_orig"])
            c_rot = colin(w["claimed_on_rot"])
            tol = sp.Float("1e-50")
            rec["proof_2_sympy_self_contradiction"] = {
                "witness_display": [float(X.x), float(X.y)],
                "claimed_on_edge": w["edge"], "from_rotated_edge": w["rot_edge"],
                "sigma": w["sigma"],
                "cross_vs_original_edge_at_60_digits": str(c_orig),
                "cross_vs_rotated_edge_at_60_digits": str(c_rot),
                "on_original_edge_at_60_digits": bool(abs(c_orig) < tol),
                "on_rotated_edge_at_60_digits": bool(abs(c_rot) < tol),
                # a genuine intersection point must lie on BOTH
                "sympy_self_consistent": bool(abs(c_orig) < tol and abs(c_rot) < tol),
            }
            # exact re-test in K: X must be on J AND rho^-1(X) must be on J
            try:
                XK = (from_sp(X.x), from_sp(X.y))
                QK = rot60(XK, poly[vi], -w["sigma"])
                rec["proof_3_exact_recheck"] = {
                    "witness_exact": [XK[0].as_pair(), XK[1].as_pair()],
                    "X_on_polygon_exactly": point_on_polygon(XK, poly),
                    "Q_exact": [QK[0].as_pair(), QK[1].as_pair()],
                    "Q_on_polygon_exactly": point_on_polygon(QK, poly),
                    "witness_is_genuine": point_on_polygon(XK, poly) and point_on_polygon(QK, poly),
                }
            except Exception as exc:  # pragma: no cover
                rec["proof_3_exact_recheck"] = {"error": repr(exc)}
        out.append(rec)
        print(json.dumps(rec, indent=1))
        print()

    verdict = {
        "disagreements": len(out),
        "all_resolved_in_favour_of_geom_py": all(
            (not r["my_verdict_good"]) and r["proof_1_cone"]["therefore_not_good"]
            and r["sympy_claims_good"]
            and not r["proof_2_sympy_self_contradiction"]["sympy_self_consistent"]
            and not r["proof_3_exact_recheck"]["witness_is_genuine"]
            for r in out),
        "records": out,
    }
    with open(os.path.join(HERE, "out", "disagreement_diagnosis.json"), "w") as fh:
        json.dump(verdict, fh, indent=1, default=str)
    print("all three resolved in favour of geom.py:",
          verdict["all_resolved_in_favour_of_geom_py"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
