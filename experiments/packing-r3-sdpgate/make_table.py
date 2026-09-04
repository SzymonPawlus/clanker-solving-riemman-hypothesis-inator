#!/usr/bin/env python3
"""Render the slack table (markdown) from the results_*.json produced by
moment_gate.py.  Presentation only -- it computes nothing new."""
import json
import sys
from fractions import Fraction


def main(paths):
    rows = []
    seen = set()
    for p in paths:
        for r in json.load(open(p)):
            if "d_relax" not in r or r["n"] in seen:
                continue
            seen.add(r["n"])
            rows.append(r)
    rows.sort(key=lambda r: r["n"])
    print("| $n$ | known $d(n)$ (exact) | known $d(n)$ | level-2 $d_2$ | abs gap | "
          "rel gap | $2n/(3(n-1))$ | cap active? |")
    print("|---:|---|---:|---:|---:|---:|---|:--|")
    from moment_gate import KNOWN_D_EXPR
    for r in rows:
        n = r["n"]
        f = Fraction(2 * n, 3 * (n - 1))
        print(f"| {n} | ${KNOWN_D_EXPR[n]}$ | {r['d_true']:.6f} | "
              f"{r['d_relax']:.6f} | {r['abs_gap']:.4f} | "
              f"**{100*r['rel_gap']:.1f}%** | ${f.numerator}/{f.denominator}"
              f" = {float(f):.7f}$ vs $f_2 = {r['f_relax']:.7f}$ | "
              f"{'YES' if r['cap_active'] else 'no'} |")


if __name__ == "__main__":
    main(sys.argv[1:])
