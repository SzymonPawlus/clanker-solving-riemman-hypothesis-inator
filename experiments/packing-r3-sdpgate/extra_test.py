#!/usr/bin/env python3
"""Does the level-2 relaxation improve if we add redundant VALID inequalities?

The obvious objection to the negative result in
problems/circle-packing-equilateral-triangle/attacks/r3-sdpgate/README.md is
"you under-built the relaxation".  This script tests it: it re-solves level 2 at
small n after adding, as explicit constraints, the pairwise products of the three
half-plane containments at each point (valid, degree 2, localised at order 1) and
the products of containments with the separation constraints for one point pair.

STATUS: `numerical`.  Float SDP output.

Run:  python3 extra_test.py
"""
import itertools
import json

from moment_gate import (build_problem, build_sdp, poly_mul, KNOWN_D)
import math


def augment(n, tcap=1.0, mode="corner"):
    nv, obj, cons, labels = build_problem(n, tcap)
    extra = []
    if mode in ("corner", "both"):
        # h_{i,k} * h_{i,l} >= 0 for the three containment half-planes of point i
        for i in range(n):
            hs = [c for c, lab in zip(cons, labels) if lab.endswith(f"({i})")
                  and lab.startswith("edge")]
            for a, b in itertools.combinations(hs, 2):
                extra.append(poly_mul(a, b))
    if mode in ("cross", "both"):
        # h_{i,k} * h_{j,l} >= 0 across distinct points (couples the points)
        for i, j in itertools.combinations(range(n), 2):
            hi = [c for c, lab in zip(cons, labels)
                  if lab.startswith("edge") and lab.endswith(f"({i})")]
            hj = [c for c, lab in zip(cons, labels)
                  if lab.startswith("edge") and lab.endswith(f"({j})")]
            for a in hi:
                for b in hj:
                    extra.append(poly_mul(a, b))
    return nv, obj, cons + extra, len(extra)


def run(n, mode, level=2):
    nv, obj, cons, nextra = augment(n, 1.0, mode)
    prob, M, sizes = build_sdp(nv, obj, cons, level)
    prob.solve(solver="SCS", eps=1e-6, max_iters=200000, time_limit_secs=400)
    f = prob.value
    d = 2 / math.sqrt(f)
    return dict(n=n, mode=mode, extra=nextra, f=f, d=d,
                d_true=KNOWN_D[n], rel_gap=(KNOWN_D[n] - d) / KNOWN_D[n],
                status=prob.status)


if __name__ == "__main__":
    out = []
    for n in (4, 5):
        for mode in ("none", "corner", "both"):
            r = run(n, mode) if mode != "none" else None
            if r is None:
                nv, obj, cons, _ = build_problem(n, 1.0)
                prob, M, sizes = build_sdp(nv, obj, cons, 2)
                prob.solve(solver="SCS", eps=1e-6, max_iters=200000)
                r = dict(n=n, mode="none", extra=0, f=prob.value,
                         d=2 / math.sqrt(prob.value), d_true=KNOWN_D[n],
                         rel_gap=(KNOWN_D[n] - 2 / math.sqrt(prob.value)) / KNOWN_D[n],
                         status=prob.status)
            print(json.dumps({k: (round(v, 8) if isinstance(v, float) else v)
                              for k, v in r.items()}), flush=True)
            out.append(r)
    json.dump(out, open("results_extra.json", "w"), indent=2)
