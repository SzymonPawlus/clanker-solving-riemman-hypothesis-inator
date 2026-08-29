"""Promote one CRITICALLY GOOD point -- good for exactly one direction -- to a committed
fixture, with every claim about it re-derived here rather than copied from explore.json.

A critically good point is the non-convex analogue of the convex lane's exactly-60-degree
boundary case: goodness holds, but only just, on a single direction, so any perturbation
that kills that one direction makes the point exceptional.

    python3 critical.py            -> out/critical_fixture.json
"""

from __future__ import annotations

import json
import math
import os
from fractions import Fraction as F

from q3 import Q3
import angular as A
import rotcheck

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def _load_candidates():
    with open(os.path.join(OUT, "explore.json")) as fh:
        return json.load(fh)["critical_examples"]


def _poly(pairs):
    return [(Q3(F(p[0][0]), F(p[0][1])), Q3(F(p[1][0]), F(p[1][1]))) for p in pairs]


def main():
    recs = []
    for cand in _load_candidates():
        P = _poly(cand["poly_exact"])
        ok, why = A.is_simple(P)
        assert ok, why
        O = P[cand["O_index"]]
        g = A.good_directions(P and O, P, verify=True)
        assert g["n_components"] == 1 and g["n_point_components"] == 1, g["n_components"]
        v = g["components"][0]["start"]
        gd, s = A.good_at_direction(O, P, v)
        assert gd
        Pw = A.vadd(O, A.vscale(s, v))
        Qw = A.vadd(O, A.vscale(s, A.rot(v, 1)))
        wok, wd = A.recheck_witness(P, O, Pw, Qw)
        assert wok, wd
        # the independent rotation decider must agree that O is good ...
        r_ok, X = rotcheck.decide_rot(O, P)
        assert r_ok
        r_q, r_x = rotcheck.triangle_from(O, X)
        rwok, _ = A.recheck_witness(P, O, r_q, r_x)
        assert rwok
        # ... and its witness must be the SAME triangle, since there is only one direction
        same = (A.veq(r_x, Pw) and A.veq(r_q, Qw)) or (A.veq(r_x, Qw) and A.veq(r_q, Pw))
        recs.append({
            "polygon_exact": [A.vpair(p) for p in P],
            "polygon_display": [A.vfloat(p) for p in P],
            "n_vertices": len(P),
            "simple": ok, "convex": A.is_convex(P),
            "O_index": cand["O_index"],
            "O_exact": A.vpair(O), "O_display": A.vfloat(O),
            "interior_angle_display_deg": A.interior_angle_info(P, cand["O_index"])
                                           ["degrees_display"],
            "n_good_directions": 1,
            "good_direction_exact": A.vpair(v),
            "good_direction_deg_display": math.degrees(
                math.atan2(float(v[1]), float(v[0]))) % 360.0,
            "scale_exact": s.pair(),
            "triangle_exact": [A.vpair(O), A.vpair(Pw), A.vpair(Qw)],
            "triangle_display": [A.vfloat(O), A.vfloat(Pw), A.vfloat(Qw)],
            "side_squared_exact": wd["side2"],
            "side_display": wd["side_display"],
            "witness_verified": wok,
            "rotation_decider_agrees": r_ok,
            "rotation_decider_same_triangle": same,
        })
    out = {
        "what": "boundary points that are good for EXACTLY ONE direction",
        "how": ("found by the angular sweep, re-decided direction by direction by "
                "good_at_direction, witness re-checked by recheck_witness, and confirmed "
                "good by the independent rotation decider rotcheck.decide_rot"),
        "status": "numerical",
        "count": len(recs),
        "examples": recs,
    }
    with open(os.path.join(OUT, "critical_fixture.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({"count": len(recs),
                      "all_witnesses_verified": all(r["witness_verified"] for r in recs),
                      "rotation_agrees": all(r["rotation_decider_agrees"] for r in recs),
                      "same_triangle": all(r["rotation_decider_same_triangle"]
                                           for r in recs),
                      "angles_deg": [round(r["interior_angle_display_deg"], 4)
                                     for r in recs],
                      "directions_deg": [round(r["good_direction_deg_display"], 6)
                                         for r in recs]}, indent=1))


if __name__ == "__main__":
    main()
