"""Krawczyk-certified enclosures + exact witness packings for circle packing in an
equilateral triangle.

CONSTRUCTION (UPPER BOUND) ONLY.  Nothing in this run bears on optimality.

Reproduce:  python3 run_all.py        (~ a few minutes, deterministic, no randomness)

Per n it:
  1. reads the LS candidate from ../circle-packing-ls/candidates/,
  2. identifies the tight contact/wall structure,
  3. picks a maximal nonsingular square subsystem (rank-revealing full pivoting), freezing
     the variables the tight system does not determine (rattler / flat directions),
  4. refines with Newton at 80 digits,
  5. runs the exact-rational interval Krawczyk test to certify existence and uniqueness of a
     solution of that subsystem inside an explicit rational box,
  6. builds an EXACT rational witness packing and verifies it from scratch exactly,
  7. writes certificates and a per-n checkpoint.
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction

from mpmath import mp

import emit
import exactvals
import iv
import krawczyk
import model
import witness

mp.dps = 80

CAND = os.path.join(os.path.dirname(__file__), "..", "circle-packing-ls", "candidates")
OUT = os.path.join(os.path.dirname(__file__), "out")
CERT = os.path.join(os.path.dirname(__file__), "certificates")

N_CALIB = [3, 6, 10, 15, 21, 8, 12]
N_OPEN = [16, 18, 19, 22, 23, 25, 26, 27, 29, 30, 32, 33, 34]
TOLS = ["1e-7", "1e-6", "1e-8", "1e-9"]
RADII = [10 ** 20, 10 ** 18, 10 ** 22, 10 ** 15, 10 ** 25]


def box_feasible(n, eqs, Z):
    """Strict feasibility of every NON-tight constraint over the whole box."""
    tight_pairs = {(e[1], e[2]) for e in eqs if e[0] == "pair"}
    tight_walls = {(e[0], e[1]) for e in eqs if e[0] != "pair"}
    bad = []
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) in tight_pairs:
                continue
            lo = krawczyk.ires(("pair", i, j), Z)[0]
            if lo <= 0:
                bad.append(("pair", i, j))
    for i in range(n):
        for kind in ("wA", "wB", "wC"):
            if (kind, i) in tight_walls:
                continue
            lo = krawczyk.ires((kind, i), Z)[0]
            if lo <= 0:
                bad.append((kind, i))
    return (len(bad) == 0), bad


def compare(n, d_wit: Fraction, encl_lo: Fraction | None, encl_hi: Fraction | None):
    """Compare the certified bound against exact known values and the published record.

    The Graham-Lubachevsky table prints d(n) to 15 significant figures, so the implied
    D = 2/d(n) is only known to an interval.  RULES.md §4 requires an improvement to exceed
    the error bars; comparing against a single rounded float would manufacture spurious
    "records" at the 1e-14 level.  So the printed value is turned into an exact rational
    interval here and the verdict is one of below / within-table-rounding / above.
    """
    out = {}
    if n in exactvals.EXACT_D:
        a, b, c = exactvals.EXACT_D[n]
        out["exact_d"] = f"{a} + {b}*sqrt({c})"
        out["witness_ge_exact"] = exactvals.cmp_rat_alg(d_wit, a, b, c) >= 0
        if encl_lo is not None:
            out["enclosure_contains_exact"] = (
                exactvals.cmp_rat_alg(encl_lo, a, b, c) <= 0
                and exactvals.cmp_rat_alg(encl_hi, a, b, c) >= 0
            )
    band = exactvals.gl_D_band(n)
    if band is not None:
        lo, hi = band
        out["gl_D_band"] = [float(lo), float(hi)]
        out["gl_D_band_width"] = float(hi - lo)
        if d_wit < lo:
            out["vs_record"] = "BELOW_TABLE_BAND"
        elif d_wit <= hi:
            out["vs_record"] = "within_table_rounding"
        else:
            out["vs_record"] = "above"
        out["witness_minus_gl_midpoint"] = float(d_wit - (lo + hi) / 2)
    return out


SEARCH = os.path.join(os.path.dirname(__file__), "..", "circle-packing-search", "out")


def candidate_sources(n):
    """Every float candidate on disk for this n, best (smallest d) first.

    Neither directory is written to; both are read-only inputs to this experiment.
    """
    out = []
    p = os.path.join(CAND, f"n{n:03d}-ls.json")
    if os.path.exists(p):
        npts, xs, us = model.load_candidate(p)
        if npts == n:
            out.append((f"experiments/circle-packing-ls/candidates/n{n:03d}-ls.json", xs, us))
    p = os.path.join(SEARCH, f"n{n}.json")
    if os.path.exists(p):
        npts, xs, us = model.load_search_candidate(p)
        if npts == n:
            out.append((f"experiments/circle-packing-search/out/n{n}.json", xs, us))
    p = os.path.join(OUT, "extra", f"n{n}.json")
    if os.path.exists(p):
        npts, xs, us = model.load_search_candidate(p)
        if npts == n:
            out.append((f"experiments/packing-r4-krawczyk/out/extra/n{n}.json", xs, us))
    out.sort(key=lambda t: float(max(x + u for x, u in zip(t[1], t[2]))))
    return out


def solve_from(n, xs, us):
    d0 = max(x + u for x, u in zip(xs, us))
    nvar = 2 * n + 1
    best = None
    for tol in TOLS:
        eqs = model.tight_structure(n, d0, xs, us, mp.mpf(tol))
        if not eqs:
            continue
        z = model.pack(d0, xs, us)
        rows, cols = model.select_square(eqs, z, nvar)
        if not rows:
            continue
        z2, res = model.newton(eqs, rows, cols, z)
        if res is None:
            continue
        cand = (res, tol, eqs, rows, cols, z2)
        if best is None or res < best[0]:
            best = cand
        if res < mp.mpf("1e-50"):
            break
    return best


def run_one(n):
    t0 = time.time()
    sources = candidate_sources(n)
    if not sources:
        return {"n": n, "ok": False, "reason": "no candidate configuration on disk"}
    best = None
    src_used = None
    for src, xs, us in sources:
        got = solve_from(n, xs, us)
        if got is None:
            continue
        w0 = witness.build_witness(n, got[5], got[2])
        if best is None or w0["d"] < best[0]:
            best = (w0["d"], got, src)
    if best is None:
        return {"n": n, "ok": False, "reason": "no tight structure / Newton failed"}
    _, got, src_used = best
    res, tol, eqs, rows, cols, z2 = got
    nvar = 2 * n + 1

    kr = {"attempted": True, "newton_residual": mp.nstr(res, 6), "tolerance": tol}
    result = None
    for rad in RADII:
        r = krawczyk.krawczyk_test(eqs, rows, cols, z2, rad)
        if r.get("ok"):
            result = r
            break
    encl_lo = encl_hi = None
    box_ok = None
    bad = []
    if result is not None:
        Z = [iv.from_int_units(v) for v in result["yhat"]]
        for c in result["cols"]:
            Z[c] = (result["yhat"][c] - result["radius_units"], result["yhat"][c] + result["radius_units"])
        box_ok, bad = box_feasible(n, eqs, Z)
        if model.DVAR in result["cols"]:
            a = result["cols"].index(model.DVAR)
            encl_lo = iv.to_frac_lo(result["enclosure"][a])
            encl_hi = iv.to_frac_hi(result["enclosure"][a])
        kr.update(
            {
                "succeeded": True,
                "square_system_size": result["k"],
                "box_radius": f"1/{10 ** iv.SCALE // result['radius_units']}",
                "d_enclosure": [emit.fstr(encl_lo), emit.fstr(encl_hi)] if encl_lo is not None else None,
                "d_enclosure_width_float": float(encl_hi - encl_lo) if encl_lo is not None else None,
                "max_row_magnitude_I_minus_CJ": float(result["max_row_mag"]) / iv.DEN,
                "nontight_constraints_strict_over_box": box_ok,
                "nontight_violations": [list(map(str, b)) for b in bad[:10]],
            }
        )
    else:
        kr["succeeded"] = False

    kr.update(
        {
            "tight_constraints": len(eqs),
            "variables": nvar,
            "rank_of_tight_jacobian": len(rows),
            "frozen_variables": nvar - len(cols),
            "dropped_tight_equations": len(eqs) - len(rows),
            "d_is_determined": model.DVAR in cols,
            "isostatic": len(eqs) == len(rows) == nvar,
        }
    )

    w = witness.build_witness(n, z2, eqs)
    rep = witness.verify_exact(w)
    wiv = witness.build_witness(n, z2, eqs, extra_slack=Fraction(1, 10 ** 42))

    g = exactvals.gl_D(n)
    beats = "unknown"
    if g is not None:
        beats = (
            "no. This reproduces the published Graham-Lubachevsky value; it does not improve "
            "it. Published record: Graham & Lubachevsky, Electron. J. Combin. 2 (1995) #A1, "
            "as tabulated in experiments/circle-packing-search/reference.py."
            if w["d"] >= g
            else "APPARENTLY BELOW the printed Graham-Lubachevsky value -- see the attack "
            "README; treat as a bug/misread until independently checked (RULES.md §4, §7)."
        )
    meta = {
        "beats_record": beats,
        "provenance": {
            "candidate": src_used,
            "method": (
                "LS/SLSQP float candidate -> tight-structure identification -> Newton at 80 "
                "digits on a nonsingular square subsystem -> snap to denominator 10**40 -> "
                "exact rational homothety repair -> exact verification. See README.md."
            ),
        },
        "krawczyk": kr,
    }
    cert = emit.algebraic_certificate(n, w, rep, meta)
    icert, ichk = emit.interval_certificate(
        n, wiv, meta, Fraction(1, 10 ** 45), Fraction(1, 10 ** 40)
    )
    emit.write(os.path.join(CERT, f"n{n:03d}-r4-krawczyk.json"), cert)
    emit.write(os.path.join(CERT, f"n{n:03d}-r4-krawczyk-interval.json"), icert)

    out = {
        "n": n,
        "ok": True,
        "seconds": round(time.time() - t0, 2),
        "candidate_source": src_used,
        "krawczyk": kr,
        "witness": {
            "d": emit.fstr(w["d"]),
            "d_float": float(w["d"]),
            "feasible": rep["feasible"],
            "tight": rep["tight"],
            "contacts_exactly_2": rep["contacts_exactly_2"],
            "boundary_points": rep["boundary_points"],
            "lambda_minus_1": float(w["lam"] - 1),
        },
        "interval_certificate_checks": ichk,
        "comparison": compare(n, w["d"], encl_lo, encl_hi),
        "beats_record": beats,
    }
    return out


def main(argv):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(CERT, exist_ok=True)
    ns = [int(a) for a in argv[1:]] or (N_CALIB + N_OPEN)
    summary = []
    for n in ns:
        try:
            r = run_one(n)
        except Exception as exc:  # checkpoint even on failure
            r = {"n": n, "ok": False, "reason": f"{type(exc).__name__}: {exc}"}
        with open(os.path.join(OUT, f"n{n:03d}.json"), "w") as fh:
            json.dump(r, fh, indent=2)
        summary.append(r)
        k = r.get("krawczyk", {})
        print(
            f"n={n:3d} ok={r.get('ok')} krawczyk={k.get('succeeded')} "
            f"K={k.get('tight_constraints')} rank={k.get('rank_of_tight_jacobian')} "
            f"vars={k.get('variables')} frozen={k.get('frozen_variables')} "
            f"dropped={k.get('dropped_tight_equations')} "
            f"boxfeas={k.get('nontight_constraints_strict_over_box')} "
            f"width={k.get('d_enclosure_width_float')} "
            f"d={r.get('witness', {}).get('d_float')} "
            f"feas={r.get('witness', {}).get('feasible')} "
            f"tight={r.get('witness', {}).get('tight')} "
            f"[{r.get('seconds')}s] {r.get('reason', '')}",
            flush=True,
        )
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)


if __name__ == "__main__":
    main(sys.argv)
