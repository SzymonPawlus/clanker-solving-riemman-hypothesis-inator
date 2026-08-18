"""Render the checkpoints in ``out/`` as the markdown table used in the attack writeup.

    uv run table.py [--min N] [--max N]

Reads only what is on disk, so it works on a partial or killed run.
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib

import reference as ref

OUT = pathlib.Path(__file__).parent / "out"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=int, default=1)
    ap.add_argument("--max", type=int, default=99)
    args = ap.parse_args()

    print("| $n$ | best found $m$ | published $d(n)$ | agreement | best found $s$ | "
          "published $s$ | verdict |")
    print("|---:|---|---|---:|---|---|:--|")
    for path in sorted(OUT.glob("n*.json")):
        row = json.loads(path.read_text())
        n = row["n"]
        if not (args.min <= n <= args.max):
            continue
        m = row["m_min_pairwise_distance_unit_triangle"]
        s = row["s_side_for_unit_circles"]
        rm = row["reference_m"]
        if rm is None:
            print(f"| {n} | {m:.15f} | — | — | {s:.12f} | — | no published value |")
            continue
        rs = ref.s_from_m(rm)
        digits = ref.agreement_digits(m, rm)
        if m > rm * (1 + 1e-9):
            verdict = "**apparently beats — treat as a bug until proven otherwise**"
        elif digits >= 10:
            verdict = "matches"
        elif digits >= 6:
            verdict = "close, not resolved"
        else:
            verdict = "**MISS**"
        stage = "" if row.get("stage") == "final" else " *(partial run)*"
        ds = "exact" if math.isinf(digits) else f"{digits:.1f} digits"
        print(f"| {n} | {m:.15f} | {rm:.15f} | {ds} | {s:.12f} | {rs:.12f} | {verdict}{stage} |")


if __name__ == "__main__":
    main()
