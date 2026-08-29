"""Driver for the angular lane.  One command reproduces everything: see run.sh.

    python3 run.py validate     hand-checked controls + the collinear-ray cases
    python3 run.py fixtures     re-decide all 190 sibling fixtures, per-fixture agreement
    python3 run.py explore      structure of G(O) on the non-convex shapes; critical points
    python3 run.py hunt N       seeded hunt for a polygon with a large exceptional set

Every stage checkpoints to out/ as it goes.  Nothing here is a proof; status is `numerical`.
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
import time
from fractions import Fraction as F

from q3 import Q3
import angular as A
import shapes
import fixtures_io

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

SEED = 20260829


def deg(v):
    return math.degrees(math.atan2(float(v[1]), float(v[0]))) % 360.0


def save(name, obj):
    with open(os.path.join(OUT, name), "w") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)


# --------------------------------------------------------------------- validate
def _check(cond, msg, fails):
    if not cond:
        fails.append(msg)
    return cond


def validate():
    fails = []
    rec = {}

    # -- 1. the equilateral triangle inscribed in itself -----------------------
    P = shapes.equilateral()
    for i, O in enumerate(P):
        g = A.good_directions(O, P)
        _check(g["good"], "equilateral vertex %d not good" % i, fails)
        _check(g["n_components"] == 1 and g["n_point_components"] == 1,
               "equilateral vertex %d: G(O) is not a single direction" % i, fails)
        w = g["witness"]
        ok, d = A.recheck_witness(P, O, w[0], w[1])
        _check(ok, "equilateral vertex %d witness rejected" % i, fails)
        _check(d["side2"] == ["1", "0"], "equilateral side^2 != 1", fails)
    rec["equilateral"] = "3 vertices good, each with exactly one good direction, side^2 = 1"

    # -- 2. the 30-30-120 wedge witness (RULES 3.1) ---------------------------
    P = shapes.t30_30_120()
    g0 = A.good_directions(P[0], P)
    g1 = A.good_directions(P[1], P)
    g2 = A.good_directions(P[2], P)
    _check(not g0["good"] and not g1["good"], "a 30-degree apex is good", fails)
    _check(g2["good"], "the 120-degree apex is not good", fails)
    _check(g2["n_components"] == 3 and g2["n_point_components"] == 3,
           "120-degree apex: expected exactly 3 isolated good directions", fails)
    dg = sorted(round(deg(c["start"]), 6) for c in g2["components"])
    _check(dg == [210.0, 240.0, 270.0],
           "120-degree apex directions %s != [210,240,270]" % dg, fails)
    # the two collinear ones, by hand: 210 and 270 run along / onto an edge through O.
    # At 210 the ray runs ALONG the edge to (-1,0); its rotate by +60 is 270, straight down
    # onto the base.  The witness is the hand-checked triangle (0,r3/3),(-1/2,r3/6),(0,0).
    ok, d = A.recheck_witness(P, P[2], *A.good_directions(P[2], P)["witness"][:2])
    _check(ok and d["side2"] == ["1/3", "0"],
           "120-apex witness side^2 %s != 1/3" % d["side2"], fails)
    # every one of the three is independently re-decided
    for c in g2["components"]:
        okd, s = A.good_at_direction(P[2], P, c["start"])
        _check(okd, "component direction rejected by the checker", fails)
    rec["30-30-120"] = ("both 30-degree apexes not good (wedge test); the 120-degree apex "
                        "good in exactly 3 directions 210/240/270, two of them collinear "
                        "with an edge; witness side^2 = 1/3")

    # -- 3. the unit square ---------------------------------------------------
    P = shapes.unit_square()
    for i, O in enumerate(P):
        g = A.good_directions(O, P)
        _check(g["good"] and g["n_components"] == 1, "square corner %d" % i, fails)
        ok, d = A.recheck_witness(P, O, g["witness"][0], g["witness"][1])
        _check(ok and d["side2"] == ["8", "-4"],
               "square side^2 %s != 8-4sqrt3" % d["side2"], fails)
    rec["square"] = "4 corners good, one good direction each, side^2 = 8 - 4*sqrt3"

    # -- 4. COLLINEAR RAYS, the case a sampling check steps over ---------------
    # (a) O in the interior of an edge: both along-edge directions see a whole INTERVAL of
    #     scales, not a point.  Take the midpoint of the bottom edge of the unit square.
    P = shapes.unit_square()
    O = (Q3(F(1, 2)), Q3(0))
    S = A.ray_scales(O, P, A.V(1, 0))
    _check(len(S) == 1 and S[0][0].is_zero() and S[0][2] is True and S[0][1] == Q3(F(1, 2)),
           "along-edge ray from an edge-interior point: scales %s" % (S,), fails)
    S = A.ray_scales(O, P, A.V(-1, 0))
    _check(len(S) == 1 and S[0][0].is_zero() and S[0][2] is True and S[0][1] == Q3(F(1, 2)),
           "opposite along-edge ray: scales %s" % (S,), fails)
    _check(A.decide(O, P)[0], "edge midpoint of the unit square is not good", fails)
    # s = 0 must be excluded: the degenerate triangle O,O,O
    _check(all(not (iv[0].is_zero() and iv[2] is False) for iv in S),
           "a radial interval is closed at s = 0", fails)

    # (b) O a vertex: BOTH incident edges are collinear rays.
    P = shapes.equilateral()
    O = P[0]
    S = A.ray_scales(O, P, A.V(1, 0))
    _check(len(S) == 1 and S[0][0].is_zero() and S[0][2] is True and S[0][1] == Q3(1),
           "along-edge ray from a vertex: %s" % (S,), fails)

    # (c) the degenerate-solution trap: at EVERY boundary point the direction sets are
    #     nonempty, but s = 0 is never in them, so a point is never good for free.
    P = shapes.t30_30_120()
    O = P[0]
    for v in (A.V(1, 0), A.V(0, 1), A.V(-1, 0), A.V(0, -1), A.V(1, 1)):
        for iv in A.ray_scales(O, P, v):
            _check(iv[0].sgn() > 0 or iv[2] is True, "scale interval contains 0", fails)
    _check(not A.decide(O, P)[0], "wedge-test point reported good", fails)

    # (d) a polygon whose 60-degree rotate about O SHARES a line with an edge: the M = 0
    #     case, where a whole arc of directions is good.  Kite with a 60-degree angle is
    #     impossible over Q; build it in K.  Take the equilateral triangle's own vertex,
    #     already covered, and a rhombus of two equilateral triangles.
    r3 = Q3(0, 1)
    P = [A.V(0, 0), A.V(1, 0), (Q3(F(3, 2)), r3 * Q3(F(1, 2))),
         (Q3(F(1, 2)), r3 * Q3(F(1, 2)))]
    ok, why = A.is_simple(P)
    _check(ok, "rhombus not simple: %s" % why, fails)
    g = A.good_directions(P[0], P)
    _check(g["good"], "rhombus 60-degree vertex not good", fails)
    rec["rhombus60"] = {"n_components": g["n_components"],
                        "n_arc_components": g["n_arc_components"],
                        "arcs_deg": [[round(deg(c["start"]), 6), round(deg(c["end"]), 6)]
                                     for c in g["components"] if c["type"] == "arc"]}

    # -- 5. float pre-screen must not see a good direction we missed ----------
    import brute
    prescreen = []
    for name, f in shapes.NAMED.items():
        P = f()
        Pf = brute.to_float_poly(P)
        for i, O in enumerate(P):
            exact = A.decide(O, P)[0]
            flt = brute.is_good_float((float(O[0]), float(O[1])), Pf, steps=4000)
            if flt and not exact:
                prescreen.append([name, i, "float says good, exact says not"])
    _check(not prescreen, "float pre-screen found directions the exact decider missed: %s"
           % prescreen, fails)
    rec["float_prescreen"] = "no float-good / exact-not-good vertex over the named shapes"

    rec["failures"] = fails
    rec["ok"] = not fails
    save("validate.json", rec)
    print(json.dumps(rec, indent=1))
    if fails:
        print("VALIDATION FAILED: %d" % len(fails))
        return 1
    print("validate: all checks passed")
    return 0


# --------------------------------------------------------------------- fixtures
def fixtures():
    fx = fixtures_io.load_all()
    t0 = time.time()
    per = []
    disagreements = []
    tot_v = tot_e = 0
    bad_wit = []
    meta_mismatch = []
    for fi, d in enumerate(fx):
        P = d["_poly"]
        n = len(P)
        rec = {"name": d["name"], "group": d["group"], "n": n,
               "vertices": 0, "vertex_disagree": 0,
               "samples": 0, "sample_disagree": 0}
        ok, why = A.is_simple(P)
        if ok != d["simple"]:
            meta_mismatch.append([d["name"], "simple", ok, d["simple"]])
        if A.is_convex(P) != d["convex"]:
            meta_mismatch.append([d["name"], "convex", A.is_convex(P), d["convex"]])
        if A.signed_area2(P).sgn() != d["orientation"]:
            meta_mismatch.append([d["name"], "orientation"])
        for vi, vrec in enumerate(d["vertices"]):
            O = P[vi]
            mine, wit = A.decide(O, P)
            rec["vertices"] += 1
            tot_v += 1
            if mine != vrec["good"]:
                rec["vertex_disagree"] += 1
                disagreements.append({"fixture": d["name"], "kind": "vertex", "index": vi,
                                      "point_display": A.vfloat(O),
                                      "point_exact": A.vpair(O),
                                      "angular": mine, "sibling": vrec["good"]})
            if mine:
                wok, wd = A.recheck_witness(P, O, wit[0], wit[1])
                if not wok:
                    bad_wit.append([d["name"], "vertex", vi, wd])
        for si, srec in enumerate(d["edge_samples"]):
            ei = srec["edge"]
            t = Q3(F(srec["t"]))
            Aa, Bb = P[ei], P[(ei + 1) % n]
            O = A.vadd(Aa, A.vscale(t, A.vsub(Bb, Aa)))
            mine, wit = A.decide(O, P)
            rec["samples"] += 1
            tot_e += 1
            if mine != srec["good"]:
                rec["sample_disagree"] += 1
                disagreements.append({"fixture": d["name"], "kind": "edge_sample",
                                      "edge": ei, "t": srec["t"],
                                      "point_display": A.vfloat(O),
                                      "point_exact": A.vpair(O),
                                      "angular": mine, "sibling": srec["good"]})
            if mine:
                wok, wd = A.recheck_witness(P, O, wit[0], wit[1])
                if not wok:
                    bad_wit.append([d["name"], "sample", si, wd])
        rec["agree"] = (rec["vertex_disagree"] == 0 and rec["sample_disagree"] == 0)
        per.append(rec)
        if (fi + 1) % 20 == 0 or fi + 1 == len(fx):
            save("fixtures.json", {"per_fixture": per, "disagreements": disagreements,
                                   "bad_witnesses": bad_wit,
                                   "meta_mismatch": meta_mismatch,
                                   "done": fi + 1, "of": len(fx),
                                   "points_compared": tot_v + tot_e,
                                   "seconds": round(time.time() - t0, 2)})
            print("  %3d/%d  %s" % (fi + 1, len(fx), d["name"]), flush=True)
    summary = {"fixtures": len(fx), "fixtures_agreeing": sum(1 for r in per if r["agree"]),
               "vertices_compared": tot_v, "edge_samples_compared": tot_e,
               "points_compared": tot_v + tot_e,
               "disagreements": len(disagreements),
               "bad_witnesses": len(bad_wit), "meta_mismatch": meta_mismatch,
               "seconds": round(time.time() - t0, 2)}
    save("fixtures.json", {"summary": summary, "per_fixture": per,
                           "disagreements": disagreements, "bad_witnesses": bad_wit,
                           "meta_mismatch": meta_mismatch})
    print(json.dumps(summary, indent=1))
    return 0 if not disagreements and not bad_wit and not meta_mismatch else 2


# ---------------------------------------------------------------------- explore
def _describe(O, P):
    g = A.good_directions(O, P)
    return {
        "good": g["good"],
        "n_components": g["n_components"],
        "n_arc_components": g["n_arc_components"],
        "n_point_components": g["n_point_components"],
        "components_deg": [{"type": c["type"], "start": round(deg(c["start"]), 9),
                            "end": round(deg(c["end"]), 9)} for c in g["components"]],
        "critical": g["n_components"] == 1 and g["n_arc_components"] == 0,
    }


def explore():
    rng = random.Random(SEED)
    out = {"named": {}, "random": [], "critical_examples": [],
           "max_components": 0, "max_components_where": None}
    for name, f in shapes.NAMED.items():
        P = f()
        recs = []
        for i, O in enumerate(P):
            r = _describe(O, P)
            r["vertex"] = i
            r["angle_display"] = round(A.interior_angle_info(P, i)["degrees_display"], 6)
            recs.append(r)
        # a couple of edge-interior points per edge
        srecs = []
        n = len(P)
        for ei in range(n):
            for t in (F(1, 3), F(1, 2)):
                O = A.vadd(P[ei], A.vscale(Q3(t), A.vsub(P[(ei + 1) % n], P[ei])))
                r = _describe(O, P)
                r["edge"], r["t"] = ei, str(t)
                srecs.append(r)
        out["named"][name] = {"vertices": recs, "edge_points": srecs,
                              "convex": A.is_convex(P),
                              "n_exceptional_vertices": sum(1 for r in recs if not r["good"]),
                              "n_exceptional_edge_points": sum(1 for r in srecs
                                                               if not r["good"])}
        for r in recs + srecs:
            if r["n_components"] > out["max_components"]:
                out["max_components"] = r["n_components"]
                out["max_components_where"] = [name, r]
        save("explore.json", out)

    # random non-convex polygons: component census + critical points
    hist = {}
    for k in range(300):
        P = shapes.random_star(rng, rng.randint(5, 9)) if k % 2 else \
            shapes.random_spiky(rng, rng.randint(2, 4))
        ok, _ = A.is_simple(P)
        if not ok or A.is_convex(P):
            continue
        n = len(P)
        for i, O in enumerate(P):
            r = _describe(O, P)
            hist[r["n_components"]] = hist.get(r["n_components"], 0) + 1
            if r["n_components"] > out["max_components"]:
                out["max_components"] = r["n_components"]
                out["max_components_where"] = ["random#%d vertex %d" % (k, i), r]
            if r["critical"] and len(out["critical_examples"]) < 6:
                out["critical_examples"].append(
                    {"poly_exact": [A.vpair(p) for p in P],
                     "poly_display": [A.vfloat(p) for p in P],
                     "O_index": i, "O_display": A.vfloat(O),
                     "direction_deg": r["components_deg"][0]["start"],
                     "convex": A.is_convex(P)})
        if k % 50 == 0:
            out["component_histogram"] = {str(a): b for a, b in sorted(hist.items())}
            save("explore.json", out)
    out["component_histogram"] = {str(a): b for a, b in sorted(hist.items())}
    save("explore.json", out)
    print(json.dumps({"max_components": out["max_components"],
                      "component_histogram": out["component_histogram"],
                      "critical_examples": len(out["critical_examples"])}, indent=1))
    return 0


# ------------------------------------------------------------------------- hunt
def hunt(count):
    """Exceptional-set census.  For each polygon, count the boundary points found NOT good:
    every vertex, plus 3 interior points per edge.  Meyerson caps the exceptional set of a
    Jordan curve at 2; three would contradict the literature (RULES.md 7)."""
    rng = random.Random(SEED + 1)
    t0 = time.time()
    best = {"max_exceptional": 0, "examples": [], "polygons": 0, "nonconvex": 0,
            "boundary_points": 0, "histogram": {}}
    hist = {}
    for k in range(count):
        mode = k % 3
        if mode == 0:
            P = shapes.random_star(rng, rng.randint(4, 9))
        elif mode == 1:
            P = shapes.random_spiky(rng, rng.randint(2, 5))
        else:
            P = shapes.spikes(rng.randint(3, 6), rng.randint(10, 300),
                              F(1, rng.randint(50, 400)), rng.randint(1, 5))
        ok, _ = A.is_simple(P)
        if not ok:
            continue
        best["polygons"] += 1
        cvx = A.is_convex(P)
        if not cvx:
            best["nonconvex"] += 1
        n = len(P)
        exc = []
        for i, O in enumerate(P):
            if not A.decide(O, P)[0]:
                exc.append(["vertex", i, A.vfloat(O)])
            best["boundary_points"] += 1
        for ei in range(n):
            for t in (F(1, 4), F(1, 2), F(3, 4)):
                O = A.vadd(P[ei], A.vscale(Q3(t), A.vsub(P[(ei + 1) % n], P[ei])))
                if not A.decide(O, P)[0]:
                    exc.append(["edge", ei, str(t), A.vfloat(O)])
                best["boundary_points"] += 1
        hist[len(exc)] = hist.get(len(exc), 0) + 1
        if len(exc) > best["max_exceptional"]:
            best["max_exceptional"] = len(exc)
            best["examples"] = [{"poly_exact": [A.vpair(p) for p in P],
                                 "poly_display": [A.vfloat(p) for p in P],
                                 "convex": cvx, "exceptional": exc}]
        elif len(exc) == best["max_exceptional"] and len(best["examples"]) < 3:
            best["examples"].append({"poly_exact": [A.vpair(p) for p in P],
                                     "poly_display": [A.vfloat(p) for p in P],
                                     "convex": cvx, "exceptional": exc})
        if (k + 1) % 100 == 0:
            best["histogram"] = {str(a): b for a, b in sorted(hist.items())}
            best["seconds"] = round(time.time() - t0, 2)
            save("hunt.json", best)
            print("  %d/%d  max exceptional so far %d  (%.1fs)"
                  % (k + 1, count, best["max_exceptional"], time.time() - t0), flush=True)
    best["histogram"] = {str(a): b for a, b in sorted(hist.items())}
    best["seconds"] = round(time.time() - t0, 2)
    save("hunt.json", best)
    print(json.dumps({kk: best[kk] for kk in ("polygons", "nonconvex", "boundary_points",
                                              "max_exceptional", "histogram", "seconds")},
                     indent=1))
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if mode == "validate":
        sys.exit(validate())
    elif mode == "fixtures":
        sys.exit(fixtures())
    elif mode == "explore":
        sys.exit(explore())
    elif mode == "hunt":
        sys.exit(hunt(int(sys.argv[2]) if len(sys.argv) > 2 else 500))
    else:
        print(__doc__)
        sys.exit(64)
