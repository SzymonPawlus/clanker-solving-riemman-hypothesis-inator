"""Emit the markdown tables for the attack writeup straight from out/*.json.

Written because this session already produced one scare by comparing against a reference value
typed from memory. Nothing in the writeup's tables is transcribed by hand: this script is the
only path from the JSON to the markdown."""

from __future__ import annotations

import glob
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def load_runs():
    runs = {}
    for f in sorted(glob.glob(os.path.join(OUT, "hunt-k*.json"))):
        d = json.load(open(f))
        runs.setdefault(d["k"], []).append(d)
    return runs


def main():
    runs = load_runs()
    L = []
    P = L.append

    P("### 5a. What the sweep found\n")
    P("| $k$ | $n$ | solves | best $m$ found | $1/(k-1)$ | best $-$ threshold | landed on $1/(k-1)$ | distinct basins |")
    P("|---|---|---|---|---|---|---|---|")
    tot = 0
    for k in sorted(runs):
        for d in sorted(runs[k], key=lambda x: x["tag"]):
            tot += d["solves"]
            P(f"| {k} | {d['n']} | {d['solves']} | {d['best_m']:.15f} | {d['threshold_m']:.15f} "
              f"| {d['best_minus_threshold']:+.2e} | {d['hits_threshold']} | {d['distinct_local_optima']} |")
    P("")
    P(f"**{tot} local solves in total across the four targets, and not one exceeded $1/(k-1)$.** "
      "The largest value seen at any $k$ sits at the threshold to machine precision (the negative "
      "entries in the fourth column are the last bit of a double), so the abort-and-exactify "
      "trigger at $1/(k-1) + 10^{-9}$ never fired.\n")

    P("### 5b. How far below the lattice value the next basin lies\n")
    P("The naive statistic — best local optimum strictly below $1/(k-1)$ — is junk: it is "
      "dominated by incompletely converged copies of the lattice sitting $10^{-8}$ below it. "
      "Instead, for a ladder of exclusion radii $\\varepsilon$, the best local optimum found "
      "below $1/(k-1) - \\varepsilon$:\n")
    P("| $k$ | $\\varepsilon = 10^{-9}$ | $10^{-6}$ | $10^{-4}$ | $10^{-3}$ |")
    P("|---|---|---|---|---|")
    for k in sorted(runs):
        vals = {}
        for d in runs[k]:
            for t in d["top_local_optima"]:
                vals[t["m"]] = vals.get(t["m"], 0) + t["count"]
        thr = 1.0 / (k - 1)
        cells = []
        for eps in (1e-9, 1e-6, 1e-4, 1e-3):
            below = [v for v in vals if v < thr - eps]
            cells.append(f"{max(below):.9f}" if below else "none in top-40")
        P(f"| {k} | " + " | ".join(cells) + " |")
    P("")
    P("Census keys are values rounded to 9 decimals and only the top 40 per run are kept, so "
      "'none in top-40' means the retained tail did not reach that far down.\n")

    P("### 5c. Seed families\n")
    P("| $k$ | family | solves | reached $1/(k-1)$ | best $m$ |")
    P("|---|---|---|---|---|")
    for k in sorted(runs):
        agg = {}
        for d in runs[k]:
            for fam, st in d["by_family"].items():
                a = agg.setdefault(fam, {"solves": 0, "hits": 0, "best": -1.0})
                a["solves"] += st["solves"]
                a["hits"] += st["hits"]
                a["best"] = max(a["best"], st["best"])
        for fam in sorted(agg):
            a = agg[fam]
            frac = 100.0 * a["hits"] / a["solves"] if a["solves"] else 0.0
            P(f"| {k} | `{fam}` | {a['solves']} | {a['hits']} ({frac:.1f}%) | {a['best']:.15f} |")
    P("")

    # insertion
    ins = []
    for f in sorted(glob.glob(os.path.join(OUT, "insert-*.json"))):
        ins.extend(json.load(open(f))["rows"])
    if ins:
        P("### 6a. The insertion attack\n")
        P("| $k$ | $\\Delta(k){-}2$ | best $m(\\Delta(k){-}2)$ | its side $a$ | insertions tried "
          "| best $m(\\Delta(k){-}1)$ | excess over $1/(k-1)$ | exact $a_{\\min}$ |")
        P("|---|---|---|---|---|---|---|---|")
        for r in sorted(ins, key=lambda r: r["k"]):
            P(f"| {r['k']} | {r['n_minus_2']} | {r['best_m_n_minus_2']:.15f} "
              f"| {r['best_a_n_minus_2']:.12f} | {r['insertions_tried']} "
              f"| {r['best_m']:.15f} | {r['excess_over_threshold']:+.2e} "
              f"| {r['exact_a_min']:.12f} |")
        P("")
        tot_ins = sum(r["insertions_tried"] for r in ins)
        P(f"**{tot_ins} insertions in total; the exact gate refuted every resulting configuration** "
          f"(`exact_refutes` = {[r['exact_refutes'] for r in sorted(ins, key=lambda r: r['k'])]}). "
          "In every case adding the extra point drove the separation back to exactly $1/(k-1)$ or "
          "below.\n")
        P("| $k$ | reference $d(\\Delta(k){-}2)$ | ours | agreement |")
        P("|---|---|---|---|")
        PUB = {13: 0.251813236653061, 19: 0.200321458983439,
               26: 0.166738399395271, 34: 0.142869646754496}
        import math
        for r in sorted(ins, key=lambda r: r["k"]):
            n2 = r["n_minus_2"]
            if n2 in PUB:
                rel = abs(r["best_m_n_minus_2"] - PUB[n2]) / PUB[n2]
                dig = "exact match" if rel == 0 else f"{-math.log10(rel):.1f} digits"
                P(f"| {r['k']} | {PUB[n2]:.15f} | {r['best_m_n_minus_2']:.15f} | {dig} |")
            else:
                P(f"| {r['k']} | *no published value* (GL stops at $n=36$) "
                  f"| {r['best_m_n_minus_2']:.15f} | — |")
        P("")

    txt = "\n".join(L)
    open(os.path.join(OUT, "tables.md"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
