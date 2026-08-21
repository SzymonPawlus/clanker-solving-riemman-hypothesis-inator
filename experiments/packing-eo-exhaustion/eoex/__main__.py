"""CLI.  Every subcommand prints exactly what it proved, in the point formulation.

    python3 -m eoex prove   --n 14 --d 79/10 --max-level 6
    python3 -m eoex sweep   --k 5 --time-limit 60
    python3 -m eoex gap     --kmax 12
    python3 -m eoex feasible --n 14 --d 8            # capacity/Oler screen, no search
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import sys
import time
from fractions import Fraction

from .algebraic import sqrt_lo_hi
from .oler import oler_bound_count, oler_excludes
from .search import Prover, frontier_digest


def _frac(text: str) -> Fraction:
    """Parse an exact rational.  Decimal strings are exact rationals and are accepted
    here (unlike in a certificate) because the theorem produced is about the rational
    that was actually used, which is echoed back in the output."""
    return Fraction(text)


def _meta() -> dict:
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def _report(args, res, d: Fraction) -> dict:
    lo, hi = sqrt_lo_hi(3, 10**20)
    out = {
        "schema": "eoex/1",
        "n": args.n,
        "d": str(d),
        "d_float": float(d),
        "max_level": args.max_level,
        "max_cited": args.max_cited,
        "oler_caps": not args.no_oler_caps,
        "oler_hull": not args.no_oler_hull,
        "oler_hull_max_level": args.oler_hull_max_level,
        "symmetry": not args.no_symmetry,
        "status": res.status,
        "nodes": res.nodes,
        "elapsed_s": round(res.elapsed, 3),
        "frontier_count": len(res.frontier),
        "frontier_digest": frontier_digest(res.frontier),
        "meta": _meta(),
    }
    if res.status == "proved":
        out["proves"] = f"d({args.n}) > {d}"
        out["proves_s"] = f"s({args.n}) > {float(d) + 2 * math.sqrt(3)}"
        out["ratio_to_target"] = None
    if res.witness is not None:
        out["witness"] = res.witness
    return out


def cmd_prove(args) -> int:
    d = _frac(args.d)
    p = Prover(
        args.n,
        d,
        args.max_level,
        max_cited=args.max_cited,
        use_oler_caps=not args.no_oler_caps,
        use_oler_hull=not args.no_oler_hull,
        oler_hull_max_level=args.oler_hull_max_level,
        symmetry=not args.no_symmetry,
    )
    res = p.run(time_limit=args.time_limit, node_limit=args.node_limit)
    rep = _report(args, res, d)
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        tmp = args.out + ".tmp"
        with open(tmp, "w") as fh:
            json.dump({**rep, "frontier": res.frontier}, fh, indent=1)
        os.replace(tmp, args.out)
    print(json.dumps(rep, indent=1))
    if res.status == "proved":
        print(
            f"PROVED: no {args.n} points at separation >= 2 in the closed equilateral "
            f"triangle of side {d}; hence d({args.n}) > {d} and "
            f"s({args.n}) > {d} + 2*sqrt(3) = {float(d) + 2 * math.sqrt(3):.9f}"
        )
    else:
        print(f"NOT PROVED ({res.status}). Nothing follows from this run.")
    return 0


def cmd_feasible(args) -> int:
    """Zero-search screen: what do the closed-form rules alone say?"""
    d = _frac(args.d)
    print(f"n = {args.n}, d = {d} = {float(d)}")
    print(f"  Oler count bound for T(d): {float(oler_bound_count(d)):.6f}")
    print(f"  Oler alone excludes n points: {oler_excludes(args.n, d)}")
    m = 8 * args.n + 1
    lo, _ = sqrt_lo_hi(m, 10**20)
    print(f"  Oler closed form: d({args.n}) > sqrt({m}) - 3 = {float(lo) - 3:.9f}")
    return 0


def cmd_gap(args) -> int:
    """The exact residual gap Erdos-Oler leaves for Oler's inequality, per k."""
    print(f"{'k':>3} {'n=T(k)-1':>9} {'target d':>9} {'Oler d >':>12} {'gap in d':>10} "
          f"{'ratio':>8}")
    rows = []
    for k in range(2, args.kmax + 1):
        n = k * (k + 1) // 2 - 1
        target = 2 * (k - 1)
        m = 8 * n + 1  # = 4k^2+4k-7
        lo, hi = sqrt_lo_hi(m, 10**25)
        oler_lo = lo - 3
        oler_hi = hi - 3
        gap_lo = target - oler_hi
        gap_hi = target - oler_lo
        ratio = float(oler_lo) / target if target else float("nan")
        print(f"{k:>3} {n:>9} {target:>9} {float(oler_lo):>12.7f} "
              f"{float(gap_hi):>10.7f} {ratio:>8.5f}")
        rows.append({"k": k, "n": n, "target_d": target,
                     "oler_lower_d": [str(oler_lo), str(oler_hi)],
                     "gap_d": [str(gap_lo), str(gap_hi)],
                     "ratio": ratio})
    print()
    print("gap in d = 2(k-1) - (sqrt(4k^2+4k-7) - 3) = (2k+1) - sqrt(4k^2+4k-7)  ~ 2/(2k+1)")
    print("ratio    = fraction of the target side that Oler alone already certifies;")
    print("           an exhaustion must exceed this ratio to add anything at all.")
    if args.out:
        with open(args.out, "w") as fh:
            json.dump({"schema": "eoex-gap/1", "rows": rows, "meta": _meta()}, fh, indent=1)
    return 0


def cmd_levels(args) -> int:
    """Resolution theorem (README §3): the level a cell method needs to reach ratio rho.

    A COST ESTIMATE, not a proof input: it uses the conjectured d(T(k)-1) = 2(k-1).
    """
    print(f"{'k':>3} {'n':>5} {'rho':>9} {'d':>10} {'level L':>8} {'cells 4^L':>12}")
    for k in range(3, args.kmax + 1):
        n = k * (k + 1) // 2 - 1
        dn = Fraction(2 * (k - 1))
        for rho in args.ratios:
            r = Fraction(rho)
            if r >= 1:
                print(f"{k:>3} {n:>5} {float(r):>9.5f} {'-':>10} {'infinite':>8} {'-':>12}")
                continue
            d = r * dn
            # need h = d/2**L < sqrt(3)*(1-rho); use a rational LOWER bound for sqrt(3)
            lo, _ = sqrt_lo_hi(3, 10**25)
            thresh = lo * (1 - r)
            L = 0
            while d / (1 << L) >= thresh:
                L += 1
                if L > 40:
                    break
            print(f"{k:>3} {n:>5} {float(r):>9.5f} {float(d):>10.5f} {L:>8} {4**L:>12}")
    return 0


def cmd_sweep(args) -> int:
    """Push d upward for the Erdos-Oler case n = T(k)-1 and record where it stops."""
    k = args.k
    n = k * (k + 1) // 2 - 1
    target = Fraction(2 * (k - 1))
    results = []
    best = None
    for num in args.ratios:
        d = Fraction(num) * target
        ml = args.max_level
        p = Prover(n, d, ml, max_cited=args.max_cited,
                   use_oler_caps=not args.no_oler_caps,
                   use_oler_hull=not args.no_oler_hull,
                   oler_hull_max_level=args.oler_hull_max_level,
                   symmetry=not args.no_symmetry)
        res = p.run(time_limit=args.time_limit, node_limit=args.node_limit)
        row = {"k": k, "n": n, "d": str(d), "d_float": float(d),
               "ratio": float(Fraction(num)), "max_level": ml,
               "status": res.status, "nodes": res.nodes,
               "elapsed_s": round(res.elapsed, 3)}
        results.append(row)
        print(json.dumps(row))
        sys.stdout.flush()
        if res.status == "proved":
            best = row
        if args.out:
            with open(args.out, "w") as fh:
                json.dump({"schema": "eoex-sweep/1", "k": k, "n": n,
                           "target_d": str(target), "rows": results,
                           "best_proved": best, "meta": _meta()}, fh, indent=1)
    print(f"\nbest proved for k={k} (n={n}, target d={target}): "
          f"{best['d'] if best else 'none'}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="eoex")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(q):
        q.add_argument("--max-cited", type=int, default=15)
        q.add_argument("--no-oler-caps", action="store_true")
        q.add_argument("--no-oler-hull", action="store_true")
        q.add_argument("--oler-hull-max-level", type=int, default=3)
        q.add_argument("--no-symmetry", action="store_true")
        q.add_argument("--time-limit", type=float, default=None)
        q.add_argument("--node-limit", type=int, default=None)
        q.add_argument("--out", default=None)

    q = sub.add_parser("prove")
    q.add_argument("--n", type=int, required=True)
    q.add_argument("--d", required=True)
    q.add_argument("--max-level", type=int, default=6)
    common(q)
    q.set_defaults(func=cmd_prove)

    q = sub.add_parser("feasible")
    q.add_argument("--n", type=int, required=True)
    q.add_argument("--d", required=True)
    q.set_defaults(func=cmd_feasible)

    q = sub.add_parser("gap")
    q.add_argument("--kmax", type=int, default=12)
    q.add_argument("--out", default=None)
    q.set_defaults(func=cmd_gap)

    q = sub.add_parser("levels")
    q.add_argument("--kmax", type=int, default=7)
    q.add_argument("--ratios", nargs="+", required=True)
    q.set_defaults(func=cmd_levels)

    q = sub.add_parser("sweep")
    q.add_argument("--k", type=int, required=True)
    q.add_argument("--ratios", nargs="+", required=True)
    q.add_argument("--max-level", type=int, default=6)
    common(q)
    q.set_defaults(func=cmd_sweep)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
