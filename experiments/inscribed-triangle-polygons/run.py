"""Driver for the exact inscribed-equilateral-triangle enumerator (issue #132).

    python3 run.py validate      # hand-checked unit tests + the three control shapes
    python3 run.py battery       # the whole fixture battery, writing out/

Every fixture's result is written to out/fixtures/<name>.json as soon as it is computed, so a
killed run still leaves everything it finished. out/summary.json holds the aggregate and the
four conjecture verdicts.

Status of everything produced here: `numerical` (RULES.md 3). The arithmetic is exact, so each
fixture's answer is certain; the CONJECTURES are statements about infinite families and are
only ever tested on finitely many fixtures here.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from fractions import Fraction as F

from geom import (decide_good, edges, is_convex, is_simple, orientation,
                  point_on_polygon, sample_edge_point, vertex_angle_class, pt_pair, pt_float)
from fixtures import battery

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FXOUT = os.path.join(OUT, "fixtures")

# Rational parameters at which non-vertex points of each edge are sampled.
SAMPLE_TS_FULL = [F(1, 5), F(1, 3), F(1, 2), F(2, 3), F(4, 5)]
SAMPLE_TS_LIGHT = [F(1, 2)]


def analyse(fx, sample_ts):
    poly = fx["poly"]
    simple, why = is_simple(poly)
    convex = is_convex(poly)
    rec = {
        "name": fx["name"],
        "group": fx["group"],
        "note": fx.get("note", ""),
        "n_vertices": len(poly),
        "simple": simple,
        "simple_reason": why,
        "convex": convex,
        "orientation": orientation(poly),
        "vertices_exact": [pt_pair(v) for v in poly],
        "vertices_display": [pt_float(v) for v in poly],
        "vertices": [],
        "edge_samples": [],
    }
    if not simple:
        return rec

    for i, V in enumerate(poly):
        cls = vertex_angle_class(poly, i)
        res = decide_good(poly, V)
        rec["vertices"].append({
            "index": i,
            "point_display": pt_float(V),
            "interior_angle_display_deg": round(cls["degrees_display"], 9),
            "reflex": cls["reflex"],
            "cmp60": cls["cmp60"],          # -1 / 0 / +1  vs an interior angle of 60 degrees
            "good": res["good"],
            "witness": res["witness"],
            "witness_verified": res["verified_ok"],
            "witness_detail": res["verified"],
            "pairs_tested": res["pairs_tested"],
            "nonempty_pairs": res["nonempty_pairs"],
            "trivial_only_pairs": res["trivial_only_pairs"],
        })

    for ei, (A, B) in enumerate(edges(poly)):
        for t in sample_ts:
            X = sample_edge_point(A, B, t)
            assert point_on_polygon(X, poly)
            res = decide_good(poly, X)
            rec["edge_samples"].append({
                "edge": ei, "t": str(t),
                "point_display": pt_float(X),
                "good": res["good"],
                "witness_verified": res["verified_ok"],
            })
    return rec


def verdicts(records):
    """The four questions the brief asks, evaluated over everything computed."""
    v = {
        "C1_convex_vertex_good_iff_angle_ge_60": {"tested": 0, "violations": []},
        "C2_convex_nonvertex_points_all_good": {"tested": 0, "violations": []},
        "C3_max_nongood_vertices_in_a_convex_polygon": {"max": 0, "argmax": None,
                                                        "three_or_more": []},
        "C4_nonconvex_sub60_vertex_that_is_good": {"examples": []},
        "C5_nonconvex_nonvertex_points_all_good": {"tested": 0, "violations": []},
        "C6_nonconvex_vertex_angle_ge_60_but_not_good": {"tested": 0, "examples": []},
        "C7_rational_polygon_never_has_an_exactly_60_vertex": {"tested": 0, "violations": []},
        "witness_verification_failures": [],
    }
    for r in records:
        if not r["simple"]:
            continue
        rational = all(c[1] == "0" for xy in r["vertices_exact"] for c in xy)
        if rational:
            for w in r["vertices"]:
                v["C7_rational_polygon_never_has_an_exactly_60_vertex"]["tested"] += 1
                if w["cmp60"] == 0:
                    v["C7_rational_polygon_never_has_an_exactly_60_vertex"]["violations"].append(
                        [r["name"], w["index"]])
        for w in r["vertices"]:
            if w["good"] and not w["witness_verified"]:
                v["witness_verification_failures"].append([r["name"], w["index"]])
        if r["convex"]:
            nongood = 0
            for w in r["vertices"]:
                v["C1_convex_vertex_good_iff_angle_ge_60"]["tested"] += 1
                predicted = (w["cmp60"] >= 0)
                if predicted != w["good"]:
                    v["C1_convex_vertex_good_iff_angle_ge_60"]["violations"].append({
                        "fixture": r["name"], "vertex": w["index"],
                        "angle_deg_display": w["interior_angle_display_deg"],
                        "cmp60": w["cmp60"], "good": w["good"]})
                if not w["good"]:
                    nongood += 1
            for s in r["edge_samples"]:
                v["C2_convex_nonvertex_points_all_good"]["tested"] += 1
                if not s["good"]:
                    v["C2_convex_nonvertex_points_all_good"]["violations"].append(
                        {"fixture": r["name"], "edge": s["edge"], "t": s["t"]})
            if nongood > v["C3_max_nongood_vertices_in_a_convex_polygon"]["max"]:
                v["C3_max_nongood_vertices_in_a_convex_polygon"]["max"] = nongood
                v["C3_max_nongood_vertices_in_a_convex_polygon"]["argmax"] = r["name"]
            if nongood >= 3:
                v["C3_max_nongood_vertices_in_a_convex_polygon"]["three_or_more"].append(r["name"])
        else:
            for s_ in r["edge_samples"]:
                v["C5_nonconvex_nonvertex_points_all_good"]["tested"] += 1
                if not s_["good"]:
                    v["C5_nonconvex_nonvertex_points_all_good"]["violations"].append(
                        {"fixture": r["name"], "edge": s_["edge"], "t": s_["t"]})
            for w in r["vertices"]:
                if w["cmp60"] >= 0:
                    v["C6_nonconvex_vertex_angle_ge_60_but_not_good"]["tested"] += 1
                    if not w["good"]:
                        v["C6_nonconvex_vertex_angle_ge_60_but_not_good"]["examples"].append({
                            "fixture": r["name"], "vertex": w["index"],
                            "angle_deg_display": w["interior_angle_display_deg"],
                            "reflex": w["reflex"]})
                if w["cmp60"] == -1 and w["good"]:
                    v["C4_nonconvex_sub60_vertex_that_is_good"]["examples"].append({
                        "fixture": r["name"], "vertex": w["index"],
                        "angle_deg_display": w["interior_angle_display_deg"],
                        "witness": w["witness"]})
    return v


def env_block():
    try:
        import sympy
        sv = sympy.__version__
    except Exception:
        sv = "not installed (not used by the decision procedure)"
    return {
        "python": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "sympy_present": sv,
        "dependencies_of_the_decider": "standard library only (fractions)",
    }


def cmd_validate(args):
    print("== hand-checked unit tests ==")
    rc = subprocess.call([sys.executable, os.path.join(HERE, "test_iet.py")])
    if rc != 0:
        print("UNIT TESTS FAILED -- stopping before the battery")
        return rc
    print()
    print("== the three controls, in detail ==")
    names = ["ctl-equilateral", "ctl-tri-30-30-120", "ctl-unit-square"]
    fxs = {f["name"]: f for f in battery()}
    os.makedirs(FXOUT, exist_ok=True)
    recs = []
    for n in names:
        rec = analyse(fxs[n], SAMPLE_TS_FULL)
        recs.append(rec)
        with open(os.path.join(FXOUT, f"{n}.json"), "w") as fh:
            json.dump(rec, fh, indent=1)
        print(f"\n{n}  ({'convex' if rec['convex'] else 'non-convex'}, "
              f"{rec['n_vertices']} vertices, simple={rec['simple']})")
        print(f"  {rec['note']}")
        for w in rec["vertices"]:
            print(f"    vertex {w['index']} at {['%.6g' % c for c in w['point_display']]}"
                  f"  interior angle {w['interior_angle_display_deg']:.6f} deg"
                  f"  ({'<' if w['cmp60'] < 0 else ('=' if w['cmp60'] == 0 else '>')}60)"
                  f"  -> good={w['good']}"
                  + (f"  [witness verified={w['witness_verified']}]" if w["good"] else
                     f"  [{w['nonempty_pairs']} intersecting pairs, all {w['trivial_only_pairs']} "
                     f"of them meeting only at O]"))
        ng = sum(1 for s in rec["edge_samples"] if not s["good"])
        print(f"    non-vertex samples: {len(rec['edge_samples'])} tested, {ng} not good")
    print("\ncontrols written to out/fixtures/")
    return 0


def cmd_battery(args):
    os.makedirs(FXOUT, exist_ok=True)
    fxs = battery()
    if args.only:
        fxs = [f for f in fxs if args.only in f["name"]]
    records = []
    t0 = time.time()
    for i, f in enumerate(fxs):
        light = f["group"] == "random"
        rec = analyse(f, SAMPLE_TS_LIGHT if light else SAMPLE_TS_FULL)
        records.append(rec)
        with open(os.path.join(FXOUT, f"{f['name']}.json"), "w") as fh:
            json.dump(rec, fh, indent=1)
        if (i + 1) % 10 == 0 or i + 1 == len(fxs):
            ng = sum(1 for r in records for w in r["vertices"] if not w["good"])
            print(f"  [{i+1}/{len(fxs)}] {time.time()-t0:6.1f}s  {f['name']}"
                  f"  (non-good vertices so far: {ng})", flush=True)
            with open(os.path.join(OUT, "summary.json"), "w") as fh:
                json.dump({"partial": True, "n_done": i + 1, "n_total": len(fxs),
                           "environment": env_block(), "verdicts": verdicts(records)},
                          fh, indent=1)

    summary = {
        "partial": False,
        "issue": 132,
        "status": "numerical (RULES.md 3): exact arithmetic on finitely many fixtures; "
                  "certain about each fixture, evidence only about the general conjectures",
        "environment": env_block(),
        "seconds": round(time.time() - t0, 2),
        "n_fixtures": len(records),
        "n_vertices_decided": sum(len(r["vertices"]) for r in records),
        "n_nonvertex_points_decided": sum(len(r["edge_samples"]) for r in records),
        "all_simple": all(r["simple"] for r in records),
        "verdicts": verdicts(records),
        "per_fixture": [
            {"name": r["name"], "group": r["group"], "convex": r["convex"],
             "n_vertices": r["n_vertices"],
             "good": [w["good"] for w in r["vertices"]],
             "cmp60": [w["cmp60"] for w in r["vertices"]],
             "angles_deg_display": [w["interior_angle_display_deg"] for w in r["vertices"]],
             "nonvertex_samples": len(r["edge_samples"]),
             "nonvertex_nongood": sum(1 for s in r["edge_samples"] if not s["good"])}
            for r in records],
    }
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1)

    v = summary["verdicts"]
    print("\n== verdicts ==")
    print(f"fixtures {summary['n_fixtures']}, vertices decided {summary['n_vertices_decided']}, "
          f"non-vertex points decided {summary['n_nonvertex_points_decided']}, "
          f"{summary['seconds']}s")
    c1 = v["C1_convex_vertex_good_iff_angle_ge_60"]
    print(f"C1 convex: good <=> interior angle >= 60   : {c1['tested']} vertices, "
          f"{len(c1['violations'])} violations")
    for x in c1["violations"][:20]:
        print("    VIOLATION", x)
    c2 = v["C2_convex_nonvertex_points_all_good"]
    print(f"C2 convex: every non-vertex point is good  : {c2['tested']} points, "
          f"{len(c2['violations'])} violations")
    for x in c2["violations"][:20]:
        print("    VIOLATION", x)
    c3 = v["C3_max_nongood_vertices_in_a_convex_polygon"]
    print(f"C3 max non-good vertices on a convex polygon: {c3['max']} "
          f"(at {c3['argmax']}); with >=3: {c3['three_or_more']}")
    c4 = v["C4_nonconvex_sub60_vertex_that_is_good"]
    print(f"C4 non-convex sub-60 vertices that ARE good : {len(c4['examples'])}")
    for x in c4["examples"][:10]:
        print(f"    {x['fixture']} vertex {x['vertex']} angle "
              f"{x['angle_deg_display']:.6f} deg is GOOD")
    c5 = v["C5_nonconvex_nonvertex_points_all_good"]
    print(f"C5 non-convex: every non-vertex point good  : {c5['tested']} points, "
          f"{len(c5['violations'])} violations")
    for x in c5["violations"][:20]:
        print("    VIOLATION", x)
    c6 = v["C6_nonconvex_vertex_angle_ge_60_but_not_good"]
    print(f"C6 non-convex vertices with angle >= 60     : {c6['tested']} tested, "
          f"{len(c6['examples'])} of them NOT good")
    for x in c6["examples"][:20]:
        print("    ", x)
    c7 = v["C7_rational_polygon_never_has_an_exactly_60_vertex"]
    print(f"C7 rational-coordinate vertices             : {c7['tested']} tested, "
          f"{len(c7['violations'])} at exactly 60 deg (must be 0: tan 60 = sqrt 3 is irrational)")
    print(f"witness verification failures: {v['witness_verification_failures']}")
    return 0


def cmd_hunt(args):
    """A large seeded search for a counterexample to C1 (hence to C3).

    C3 -- 'no convex polygon has three non-good vertices' -- follows from C1 plus the
    exterior-angle count, so the only way to break C3 is to break the forward half of C1:
    a convex vertex whose interior angle is >= 60 but which is NOT good. This hunts for one
    over pseudorandom convex polygons, including heavily squashed ones (a rational affine
    squash preserves convexity and manufactures near-degenerate angles)."""
    from fixtures import random_convex
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    n_poly = n_vert = 0
    c1_viol = []
    ge3 = []
    hist = {}
    batch = 250
    done = 0
    while done < args.count:
        take = min(batch, args.count - done)
        for f in random_convex(seed=args.seed + done, count=take, max_pts=args.max_pts):
            poly = f["poly"]
            ok, _ = is_simple(poly)
            if not ok or not is_convex(poly):
                continue
            n_poly += 1
            nongood = 0
            for i, V in enumerate(poly):
                n_vert += 1
                cls = vertex_angle_class(poly, i)
                res = decide_good(poly, V)
                key = ("lt60" if cls["cmp60"] < 0 else ("eq60" if cls["cmp60"] == 0 else "ge60"),
                       res["good"])
                hist[str(key)] = hist.get(str(key), 0) + 1
                if (cls["cmp60"] >= 0) != res["good"]:
                    c1_viol.append({"fixture": f["name"], "seed_block": args.seed + done,
                                    "vertex": i, "cmp60": cls["cmp60"], "good": res["good"],
                                    "angle_deg_display": cls["degrees_display"],
                                    "vertices_exact": [pt_pair(p) for p in poly]})
                if not res["good"]:
                    nongood += 1
            if nongood >= 3:
                ge3.append({"fixture": f["name"], "seed_block": args.seed + done,
                            "vertices_exact": [pt_pair(p) for p in poly]})
        done += take
        rec = {"seed": args.seed, "requested": args.count, "generated_so_far": done,
               "polygons_tested": n_poly, "vertices_decided": n_vert,
               "seconds": round(time.time() - t0, 2), "histogram": hist,
               "C1_violations": c1_viol, "C3_three_or_more_nongood": ge3,
               "environment": env_block()}
        with open(os.path.join(OUT, "hunt.json"), "w") as fh:
            json.dump(rec, fh, indent=1)
        print(f"  {done}/{args.count} requested; {n_poly} convex polygons, {n_vert} vertices, "
              f"{len(c1_viol)} C1 violations, {len(ge3)} with >=3 non-good "
              f"({time.time()-t0:.1f}s)", flush=True)
    print("\nhistogram (angle class, good):", hist)
    print("C1 violations:", c1_viol if c1_viol else "none")
    print("convex polygons with >= 3 non-good vertices:", ge3 if ge3 else "none")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    b = sub.add_parser("battery")
    b.add_argument("--only", default=None, help="substring filter on fixture names")
    h = sub.add_parser("hunt")
    h.add_argument("--count", type=int, default=4000)
    h.add_argument("--seed", type=int, default=20260829)
    h.add_argument("--max-pts", dest="max_pts", type=int, default=12)
    args = ap.parse_args()
    return {"validate": cmd_validate, "battery": cmd_battery, "hunt": cmd_hunt}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
