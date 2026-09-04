"""Drivers for the exact inscribed-triangle MAXIMISER lane.

    python3 run.py validate          # hand-known answers (equilateral, square, 30-30-120)
    python3 run.py fixtures          # all 190 committed fixtures, both maximisers,
                                     # both committed deciders, both their verifiers
    python3 run.py global [ntest]    # global max over O: vertices vs sampled edge points
    python3 run.py cw [J D]          # the constant-width body: exact upper bound on m

Every stage checkpoints into out/ after each fixture, so a killed run still produced
something (`../../RULES.md` §6).
"""
from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction as F

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

from iet.qs3 import Q3                                            # noqa: E402
from iet import maximiser as M                                    # noqa: E402
from iet.maximiser import V, vfloat, vpair, max_at_point, global_max, edges  # noqa: E402
from iet.pairmax import max_at_point_pairs                        # noqa: E402

SEED = 20260830           # every generator in this lane; nothing here is random today


def controls():
    """The three hand-known answers, plus two structural ones."""
    return {
        "equilateral-side-1": ([V(0, 0), V(1, 0), (Q3(1, 0, 2), Q3(0, 1, 2))],
                               {"expect_all_vertices": Q3(1, 0, 1)}),
        "unit-square": ([V(0, 0), V(1, 0), V(1, 1), V(0, 1)],
                        {"expect_all_vertices": Q3(8, -4, 1)}),
        "tri-30-30-120": ([V(-1, 0), V(1, 0), (Q3(0), Q3(0, 1, 3))],
                          {"expect_per_vertex": [None, None, Q3(4, 0, 9)]}),
        "rect-2x1": ([V(0, 0), V(2, 0), V(2, 1), V(0, 1)], {}),
        "equilateral-side-2": ([V(0, 0), V(2, 0), (Q3(1, 0, 1), Q3(0, 1, 1))],
                               {"expect_all_vertices": Q3(4, 0, 1)}),
    }


def _cmp_point(poly, O, sib=None):
    """Run both maximisers at O and, when `sib` is given, both committed deciders."""
    a = max_at_point(O, poly)
    b = max_at_point_pairs(O, poly)
    rec = {"O": vpair(O), "O_display": vfloat(O),
           "good": a["good"], "side2": a["side2"].pair() if a["good"] else None,
           "side_display": float(a["side2"]) ** 0.5 if a["good"] else None,
           "agree_pairmax": (a["good"] == b["good"]
                             and (not a["good"] or a["side2"] == b["side2"])),
           "pair_side2": b["side2"].pair() if b["good"] else None}
    if sib is not None:
        pd = sib.poly_decide(poly, O)
        ad, _ = sib.ang_decide(poly, O)
        rec["poly_good"] = bool(pd["good"])
        rec["ang_good"] = bool(ad)
        rec["agree_deciders"] = (rec["poly_good"] == a["good"] == rec["ang_good"])
        if a["good"]:
            okp, _ = sib.poly_verify(poly, O, a["P"], a["Q"])
            oka, _ = sib.ang_verify(poly, O, a["P"], a["Q"])
            rec["poly_verify"] = bool(okp)
            rec["ang_verify"] = bool(oka)
        else:
            rec["poly_verify"] = rec["ang_verify"] = None
    return rec, a, b


def stage_validate():
    import iet.siblings as sib
    res = {}
    bad = []
    for name, (poly, exp) in controls().items():
        ok_simple, why = M.is_simple(poly)
        assert ok_simple, (name, why)
        pts = []
        for i, O in enumerate(poly):
            rec, a, b = _cmp_point(poly, O, sib)
            rec["vertex"] = i
            pts.append(rec)
            if not rec["agree_pairmax"]:
                bad.append(("pairmax", name, i))
            if not rec["agree_deciders"]:
                bad.append(("deciders", name, i))
            if a["good"] and not (rec["poly_verify"] and rec["ang_verify"]):
                bad.append(("verify", name, i))
        checks = {}
        if "expect_all_vertices" in exp:
            e = exp["expect_all_vertices"]
            checks["all_vertices_side2"] = all(
                p["good"] and Q3.from_pair(p["side2"]) == e for p in pts)
            checks["expected"] = e.pair()
        if "expect_per_vertex" in exp:
            e = exp["expect_per_vertex"]
            checks["per_vertex_side2"] = all(
                (p["good"] is (ei is not None))
                and (ei is None or Q3.from_pair(p["side2"]) == ei)
                for p, ei in zip(pts, e))
            checks["expected"] = [None if x is None else x.pair() for x in e]
        for k, v in checks.items():
            if v is False:
                bad.append(("control", name, k))
        res[name] = {"vertices": pts, "checks": checks,
                     "convex": M.is_convex(poly), "n": len(poly)}
        print("  %-22s %s" % (name, checks or "(no hand value)"), flush=True)
    res["_failures"] = bad
    _write("validate.json", res)
    print("failures:", bad)
    return not bad


def _write(fn, obj):
    with open(os.path.join(OUT, fn), "w") as fh:
        json.dump(obj, fh, indent=1, default=str)


def stage_fixtures(limit=None):
    import iet.siblings as sib
    names = sib.fixture_names()
    if limit:
        names = names[:int(limit)]
    summary = {"n_fixtures": 0, "n_points": 0, "n_vertices": 0, "n_edge_samples": 0,
               "disagree_pairmax": [], "disagree_deciders": [], "verify_rejects": [],
               "disagree_recorded_good": [], "seed": SEED, "per_fixture": {}}
    t0 = time.time()
    for idx, name in enumerate(names):
        poly, d = sib.load_fixture(name)
        pts = []
        for i, O in enumerate(poly):
            rec, a, b = _cmp_point(poly, O, sib)
            rec["kind"] = "vertex"
            rec["index"] = i
            pts.append(rec)
            summary["n_vertices"] += 1
        for s in d.get("edge_samples", []):
            e = int(s["edge"])
            t = Q3.of(F(s["t"]))
            A, B = edges(poly)[e]
            O = M.vadd(A, M.vscale(t, M.vsub(B, A)))
            rec, a, b = _cmp_point(poly, O, sib)
            rec["kind"] = "edge"
            rec["index"] = e
            rec["t"] = s["t"]
            rec["recorded_good"] = bool(s["good"])
            if rec["good"] != rec["recorded_good"]:
                summary["disagree_recorded_good"].append([name, e, s["t"]])
            pts.append(rec)
            summary["n_edge_samples"] += 1
        for p in pts:
            if not p["agree_pairmax"]:
                summary["disagree_pairmax"].append([name, p["kind"], p["index"]])
            if not p["agree_deciders"]:
                summary["disagree_deciders"].append([name, p["kind"], p["index"]])
            if p["good"] and not (p["poly_verify"] and p["ang_verify"]):
                summary["verify_rejects"].append([name, p["kind"], p["index"]])
        summary["per_fixture"][name] = {
            "n": len(poly), "convex": d.get("convex"),
            "max_side2_over_vertices": max(
                (p["side2"] for p in pts if p["kind"] == "vertex" and p["good"]),
                key=lambda s: float(Q3.from_pair(s)), default=None),
            "points": pts}
        summary["n_fixtures"] += 1
        summary["n_points"] += len(pts)
        if idx % 10 == 0 or idx == len(names) - 1:
            _write("fixtures.json", summary)
            print("  [%3d/%3d] %-40s pts=%d  %.0fs" %
                  (idx + 1, len(names), name, summary["n_points"], time.time() - t0),
                  flush=True)
    _write("fixtures.json", summary)
    print(json.dumps({k: (len(v) if isinstance(v, list) else v)
                      for k, v in summary.items() if k != "per_fixture"}, indent=1))
    return not (summary["disagree_pairmax"] or summary["disagree_deciders"]
                or summary["verify_rejects"] or summary["disagree_recorded_good"])


TS = tuple(F(a, b) for a, b in
           ((1, 7), (1, 5), (1, 4), (1, 3), (2, 5), (1, 2), (3, 5), (2, 3), (3, 4), (4, 5), (6, 7)))


def stage_global(limit=None):
    """Global max over O.  Exact over the vertices; the edge sweep is a SAMPLE and is
    labelled as one -- it can only refute Lemma V, never confirm it."""
    import iet.siblings as sib
    names = sib.fixture_names()
    if limit:
        names = names[:int(limit)]
    out = {"seed": SEED, "sample_ts": [str(t) for t in TS], "violations": [],
           "per_fixture": {}, "n_sampled_points": 0}
    t0 = time.time()
    for idx, name in enumerate(names):
        poly, d = sib.load_fixture(name)
        g = global_max(poly, sample_ts=TS)
        best = g["best"]
        rec = {"n": len(poly), "convex": d.get("convex"),
               "best_side2": best[1]["side2"].pair() if best else None,
               "best_side_display": float(best[1]["side2"]) ** 0.5 if best else None,
               "best_where": list(best[0]) if best else None,
               "n_good_vertices": sum(1 for _, r in g["per_vertex"] if r["good"]),
               "n_exceptional_vertices": sum(1 for _, r in g["per_vertex"] if not r["good"])}
        mx = None
        for (i, t, r) in g["sampled"]:
            if r["good"] and (mx is None or (r["side2"] - mx[0]).sgn() > 0):
                mx = (r["side2"], i, str(t))
        rec["best_sampled_side2"] = mx[0].pair() if mx else None
        rec["best_sampled_display"] = float(mx[0]) ** 0.5 if mx else None
        rec["sampled_beats_vertices"] = bool(g["lemma_v_violation"])
        if g["lemma_v_violation"]:
            out["violations"].append([name, str(g["lemma_v_violation"][1])])
        out["n_sampled_points"] += len(g["sampled"])
        out["per_fixture"][name] = rec
        if idx % 10 == 0 or idx == len(names) - 1:
            _write("global.json", out)
            print("  [%3d/%3d] %-40s %.0fs" % (idx + 1, len(names), name, time.time() - t0),
                  flush=True)
    _write("global.json", out)
    print("Lemma V violations:", out["violations"], " sampled points:", out["n_sampled_points"])
    return not out["violations"]


def stage_cw(J=192, D=1200, eps=F(1, 24)):
    from iet import cw
    res = cw.run(J=int(J), D=int(D), eps=eps, progress=100)
    _write("cw.json", res)
    print(json.dumps({k: v for k, v in res.items() if k != "per_direction"}, indent=1))
    return res["proves_disk_not_extremal"]


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "validate"
    args = sys.argv[2:]
    ok = {"validate": stage_validate, "fixtures": stage_fixtures,
          "global": stage_global, "cw": stage_cw}[cmd](*args)
    print("STAGE", cmd, "OK" if ok else "FAILED")
    sys.exit(0 if ok else 1)
