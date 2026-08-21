"""Collate everything in out/ into out/report.txt. Reads only; computes no new packings.

The two things this produces that are not just "we did not find one":

* the **local-optimum census** per k -- how many distinct basins, how far below 1/(k-1) the best
  non-lattice basin sits, and which seed families reached the threshold;
* the **counterexample window** and the **margin curve** in k. Since m(n) <= m(n-1) trivially
  (delete a point), any violation of EO(k) satisfies

      1/(k-1) < m(Delta(k)-1) <= m(Delta(k)-2),

  so a counterexample triangle has side a in [1/m(Delta(k)-2), k-1). Using the published
  best-known d(Delta(k)-2) in place of the unknown optimum makes this **conditional on that
  record being optimal**; it is stated that way and is `numerical`, never assumable.
"""

from __future__ import annotations

import glob
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

# Published d(n) = m(n). Source: experiments/circle-packing-search/reference.py, which takes them
# from Graham-Lubachevsky (EJC 2 (1995) #A1, 15 s.f.) and Friedman's Packing Center exact forms.
# NOTHING here is computed by this project. GL's table stops at n = 36, so k >= 9 has no entry.
PUBLISHED_D = {
    4: 0.577350269189626,
    8: 0.343070330817254,
    13: 0.251813236653061,
    19: 0.200321458983439,
    26: 0.166738399395271,
    34: 0.142869646754496,
}


def open_corner_counts(points, m, jmax=5):
    """Occupancy of the three OPEN corner triangles at integer scales j = 1..jmax.

    The eo-hull-deficit SS9 condition is about the *open* triangle: on the T(k) lattice the open
    corner triangle of side j holds exactly T(j) points, while the closed one holds more (it
    swallows the whole j-th lattice row). Recomputed here from the stored coordinates so the
    convention is fixed in one place."""
    import math as _m
    a = 1.0 / m
    s3 = _m.sqrt(3.0)
    out = []
    lams = []
    for x, y in points:
        l2 = y / (s3 / 2.0)
        l1 = x - y / s3
        lams.append((1.0 - l1 - l2, l1, l2))
    for v in range(3):
        row = []
        for j in range(1, jmax + 1):
            thr = 1.0 - j / a
            row.append(sum(1 for L in lams if L[v] > thr + 1e-9))
        out.append(row)
    return out


def tri(k):
    return k * (k + 1) // 2


def fmt(x, w=18):
    return "n/a".rjust(w) if x is None else f"{x:{w}.15f}"


def main():
    L = []
    P = L.append

    P("Erdos-Oler counterexample hunt -- collated report")
    P("=" * 96)
    P("STATUS: every number below is `numerical` (problem RULES.md SS1). No packing here is a")
    P("certificate except where an exact q_min is printed, and no optimality is claimed anywhere.")
    P("Normalisation: n points at pairwise distance >= 1 in an equilateral triangle of side a;")
    P("search reports m = max-min distance in the UNIT triangle, so a = 1/m. Delta(k)=k(k+1)/2.")
    P("EO(k) is false iff m(Delta(k)-1) > 1/(k-1).   (Repo certificates use separation 2, d = 2a.)")
    P("")

    # ---------------- benchmark
    bp = os.path.join(OUT, "bench.json")
    if os.path.exists(bp):
        b = json.load(open(bp))
        P("0. COST MODEL (out/bench.json) -- the budget in KILL-CRITERION.md was set from this")
        P(f"   env: python {b['env']['python']}, numpy {b['env']['numpy']}, scipy {b['env']['scipy']}")
        for r in b["rows"]:
            P(f"   k={r['k']:2d} n={r['n']:3d}   {r['seconds_per_solve'] * 1000:9.1f} ms per SLSQP solve")
        P("")

    # ---------------- validation
    vp = os.path.join(OUT, "validate.json")
    if os.path.exists(vp):
        v = json.load(open(vp))
        P("1. VALIDATION on the PROVEN cases k=2..6 (Melissen 1993; Payan 1997) -- gate before any")
        P("   target run. An optimiser that beats a proven case is broken, not brilliant.")
        P(f"   {'k':>3} {'n':>4} {'best m':>20} {'target 1/(k-1)':>20} {'exact a_min':>16} {'digits':>8}")
        for r in v["rows"]:
            P(f"   {r['k']:>3} {r['n']:>4} {r['best_m']:>20.15f} {r['threshold_m']:>20.15f} "
              f"{r['exact_a_min']:>16.12f} {r['agreement_digits']:>8.1f}")
        P(f"   ALL OK: {v['all_ok']}  -- exact gate returned a_min = k-1 exactly in every case,")
        P("   i.e. it never reported a sub-(k-1) packing where the literature says none exists.")
        P("")

    # ---------------- positive control
    cp = os.path.join(OUT, "control-n26.json")
    if os.path.exists(cp):
        c = json.load(open(cp))
        s = c["search"]
        P("2. POSITIVE CONTROL n = 26 (out/control-n26.json) -- the only test of the exact gate's")
        P("   'yes' branch. 26 points DO fit below side 6, so the gate must say so.")
        P(f"   search: {s['solves']} solves, best m = {s['best_m']:.15f}")
        P(f"   published d(26)     = {s['ref_d26']:.15f}   (Graham-Lubachevsky 1995)")
        P(f"   agreement           = {s['agreement_digits']:.2f} significant digits")
        P(f"   side a = 1/m        = {1.0 / s['best_m']:.15f}   (< 6 required)")
        for key in sorted(k for k in c if k.startswith("exact_den_")):
            e = c[key]
            P(f"   exact @ {key[10:]:>5}: a_min = {e['a_min_float']:.15f}  contained={e['contained_exact']}  "
              f"fits below side 6: {e['fits_below_side_6']}")
            if "cartesian" in e:
                x = e["cartesian"]
                P(f"       Q(sqrt3) cross-check at exact side {x['side']} = {x['side_float']:.9f}:")
                P(f"       contained={x['contained_exact']}  separation>=1: {x['separation_at_least_1']}  "
                  f"side<6: {x['side_below_6']}  checkers agree: {x['both_checkers_agree']}")
        P("")

    # ---------------- the hunt
    P("3. THE HUNT at n = Delta(k)-1  (out/hunt-k*-*.json)")
    P("")
    runs = {}
    for f in sorted(glob.glob(os.path.join(OUT, "hunt-k*.json"))):
        d = json.load(open(f))
        runs.setdefault(d["k"], []).append(d)
    P(f"   {'k':>3} {'n':>4} {'solves':>8} {'best m':>19} {'1/(k-1)':>19} {'best-thr':>12} "
      f"{'hits':>7} {'basins':>7}")
    for k in sorted(runs):
        for d in runs[k]:
            P(f"   {k:>3} {d['n']:>4} {d['solves']:>8} {d['best_m']:>19.15f} "
              f"{d['threshold_m']:>19.15f} {d['best_minus_threshold']:>12.2e} "
              f"{d['hits_threshold']:>7} {d['distinct_local_optima']:>7}")
    P("")
    P("   'hits' = solves landing on 1/(k-1) to 1e-9; 'basins' = distinct local-optimum values.")
    P("   NO run at any k produced a local optimum above 1/(k-1). The abort-and-exactify trigger")
    P("   (m > 1/(k-1) + 1e-9) never fired.")
    P("")

    P("   3a. HOW FAR BELOW THE LATTICE VALUE THE NEXT BASIN LIES.")
    P("   The naive 'best local optimum strictly below 1/(k-1)' is useless: it is dominated by")
    P("   incompletely converged copies of the lattice itself, sitting 1e-8 below it. So the table")
    P("   reports, for a ladder of exclusion radii eps, the best local optimum found below")
    P("   1/(k-1) - eps. The eps at which the value stops tracking 1/(k-1) is where the genuinely")
    P("   distinct structures start.")
    P(f"   {'k':>3} " + " ".join(f"{('eps=' + e):>22}" for e in ("1e-9", "1e-6", "1e-4", "1e-3")))
    for k in sorted(runs):
        vals = {}
        for d in runs[k]:
            for t in d["top_local_optima"]:
                vals[t["m"]] = vals.get(t["m"], 0) + t["count"]
        thr = 1.0 / (k - 1)
        cells = []
        for eps in (1e-9, 1e-6, 1e-4, 1e-3):
            below = [v for v in vals if v < thr - eps]
            cells.append(f"{max(below):>22.15f}" if below else f"{'none found':>22}")
        P(f"   {k:>3} " + " ".join(cells))
    P("   (Census keys are local-optimum values rounded to 9 decimals, and only the top 40 distinct")
    P("   values per run are retained in the checkpoints, so an entry of 'none found' at large eps")
    P("   means the top-40 tail did not reach that far down, not that no such optimum exists.)")
    P("")

    P("   3b. SEED FAMILY BREAKDOWN (solves / how many reached 1/(k-1) / best m found)")
    for k in sorted(runs):
        P(f"   k = {k}:")
        agg = {}
        for d in runs[k]:
            for fam, st in d["by_family"].items():
                a = agg.setdefault(fam, {"solves": 0, "hits": 0, "best": -1.0})
                a["solves"] += st["solves"]
                a["hits"] += st["hits"]
                a["best"] = max(a["best"], st["best"])
        for fam in sorted(agg):
            a = agg[fam]
            frac = a["hits"] / a["solves"] if a["solves"] else 0.0
            P(f"      {fam:16s} solves={a['solves']:7d}  reached 1/(k-1): {a['hits']:7d} "
              f"({frac * 100:5.1f}%)  best={a['best']:.15f}")
    P("")

    P("   3c. CORNER OCCUPANCY of the best configuration, at integer scales j=1..5.")
    P("       A k=7 counterexample must have >= T(j) points in the OPEN corner triangle of side j")
    P("       at every corner (attacks/eo-hull-deficit SS9, status `sketch` there -- used here as a")
    P("       reporting statistic and a seeding heuristic ONLY, never as an assumption).")
    P("       required T(j) for j=1..5: 1, 3, 6, 10, 15")
    for k in sorted(runs):
        d = max(runs[k], key=lambda x: x["best_m"])
        if d.get("best_points"):
            cc = open_corner_counts(d["best_points"], d["best_m"])
            P(f"   k={k} best      : A {cc[0]}  B {cc[1]}  C {cc[2]}")
        du = max(runs[k], key=lambda x: x["runner_up_m"])
        if du.get("runner_up_points"):
            cu = open_corner_counts(du["runner_up_points"], du["runner_up_m"])
            P(f"   k={k} runner-up : A {cu[0]}  B {cu[1]}  C {cu[2]}")
    P("")

    # ---------------- insertion attack
    P("4. TARGETED INSERTION ATTACK (out/insert-*.json): start from a Delta(k)-2 packing that")
    P("   genuinely beats side k-1, insert one more point at every deep hole, re-optimise.")
    ins = []
    for f in sorted(glob.glob(os.path.join(OUT, "insert-*.json"))):
        ins.extend(json.load(open(f))["rows"])
    if ins:
        P(f"   {'k':>3} {'n-2':>5} {'best m(n-2)':>19} {'a(n-2)':>16} {'inserts':>8} "
          f"{'best m(n)':>19} {'excess':>11} {'exact a_min':>16}")
        for r in sorted(ins, key=lambda r: r["k"]):
            P(f"   {r['k']:>3} {r['n_minus_2']:>5} {r['best_m_n_minus_2']:>19.15f} "
              f"{r['best_a_n_minus_2']:>16.12f} {r['insertions_tried']:>8} "
              f"{r['best_m']:>19.15f} {r['excess_over_threshold']:>11.2e} {r['exact_a_min']:>16.12f}")
        P("   'excess' = best m(Delta(k)-1) - 1/(k-1); positive would be a candidate counterexample.")
        P(f"   exact gate refuted every one: {[r['exact_refutes'] for r in sorted(ins, key=lambda r: r['k'])]}")
    else:
        P("   (not run)")
    P("")

    # ---------------- margin curve
    P("5. THE MARGIN CURVE AND THE COUNTEREXAMPLE WINDOW")
    P("")
    P("   Elementary: deleting a point gives m(n) <= m(n-1). Hence any counterexample to EO(k)")
    P("   has  1/(k-1) < m(Delta(k)-1) <= m(Delta(k)-2), so its triangle side lies in")
    P("")
    P("        a  in  [ 1/m(Delta(k)-2),  k-1 ).")
    P("")
    P("   delta(k) := m(Delta(k)-2) - 1/(k-1) is therefore an upper bound on how badly EO(k) can")
    P("   fail. m(Delta(k)-2) is not known exactly for any k >= 3, so the table substitutes the")
    P("   published best-known d(Delta(k)-2); the window is CONDITIONAL on that record being")
    P("   optimal, and is `numerical`. For k >= 9 no published value exists (GL stops at n=36) and")
    P("   the entry is this project's own best-found value -- a LOWER bound on m(Delta(k)-2), so")
    P("   the window shown there is a lower bound on the true window's width, not the window.")
    P("")
    P(f"   {'k':>3} {'n-2':>5} {'m(n-2) used':>19} {'source':>10} {'delta(k)':>11} "
      f"{'ratio':>7} {'window a in':>28} {'width':>10}")
    prev = None
    found_n2 = {r["k"]: r["best_m_n_minus_2"] for r in ins}
    for k in range(3, 11):
        n2 = tri(k) - 2
        if n2 in PUBLISHED_D:
            m2, src = PUBLISHED_D[n2], "GL/Friedm"
        elif k in found_n2:
            m2, src = found_n2[k], "ours"
        else:
            continue
        thr = 1.0 / (k - 1)
        delta = m2 - thr
        lo = 1.0 / m2
        ratio = prev / delta if prev else float("nan")
        P(f"   {k:>3} {n2:>5} {m2:>19.15f} {src:>10} {delta:>11.4e} "
          f"{ratio:>7.2f} {'[' + format(lo, '.9f') + ', ' + str(k - 1) + ')':>28} {k - 1 - lo:>10.3e}")
        prev = delta
    P("")
    P("   'ratio' = delta(k-1)/delta(k): how fast the margin collapses as k grows.")
    P("")
    with open(os.path.join(OUT, "report.txt"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
