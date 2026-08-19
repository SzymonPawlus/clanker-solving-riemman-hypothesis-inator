"""CLI.

    python -m cpbnb prove   --n 12 --d 7.4 --max-level 6
    python -m cpbnb sweep   --n 12 --targets d12 --max-level 7 --time-limit 600
    python -m cpbnb validate

``--d`` accepts an exact rational only ("7.4", "37/5"); the value is parsed with
``fractions.Fraction`` and used exactly.  A decimal string *is* exact here (unlike in a
certificate, where problem ``RULES.md`` §2 bans them because they usually hide truncated
optimiser output) -- it names the rational side length that gets proved impossible.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import platform
import sys
import time
from fractions import Fraction

from .caps import D_ENCLOSURE
from .search import CheckpointError, Prover, load_frontier

HERE = pathlib.Path(__file__).resolve().parent.parent


def _meta() -> dict:
    return {
        "python": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "note": "search is exact integer arithmetic; no seeds, fully deterministic",
    }


def cmd_prove(args: argparse.Namespace) -> int:
    d = Fraction(args.d)
    symmetry = not args.no_symmetry
    prover = Prover(args.n, d, args.max_level, args.max_cited, symmetry=symmetry)

    frontier = None
    if args.resume:
        # Fail closed.  A checkpoint is untrusted input to a program whose entire output is
        # a claim that something was exhaustively ruled out, so a rejected checkpoint must
        # end the run -- never fall back to a fresh search, which would silently answer a
        # different question than the one the user asked.
        try:
            frontier = load_frontier(
                args.resume,
                n=args.n,
                d=d,
                max_level=args.max_level,
                max_cited=args.max_cited,
                symmetry=symmetry,
            )
        except (CheckpointError, OSError) as exc:
            print(f"error: refusing to resume: {exc}", file=sys.stderr)
            return 2

    result = prover.run(
        time_limit=args.time_limit,
        node_limit=args.node_limit,
        checkpoint_path=args.checkpoint,
        initial_stack=frontier,
    )
    if frontier is not None:
        # Provenance: a resumed result rests on the checkpoint file as well as on this
        # run's arithmetic.  Record that in the output rather than letting a resumed
        # "proved" read identically to one produced from scratch.
        result["resumed_from"] = {
            "path": args.resume,
            "frontier_nodes": len(frontier),
            "note": "validated against this run's (n, d, max_level, max_cited, symmetry); "
                    "coverage of the frontier is inherited from the run that wrote it",
        }
    result["meta"] = _meta()
    if args.out:
        pathlib.Path(args.out).write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    if result["status"] == "proved":
        print(
            f"\nPROVED: no {args.n} points at mutual distance >= 2 lie in the closed "
            f"equilateral triangle of side {d} = {float(d):.9f}."
            f"\n  => d({args.n}) > {d},  s({args.n}) > {d} + 2*sqrt(3) "
            f"= {float(d) + 3.4641016151377544:.9f}"
        )
        if frontier is not None:
            print(
                f"  (resumed from {args.resume}: this conclusion also rests on that file "
                f"covering the branches the interrupted run had not yet refuted)"
            )
    return 0


def cmd_sweep(args: argparse.Namespace) -> int:
    """Push ``d`` up towards the target until the search stops closing."""
    target = Fraction(args.target)
    rows = []
    out_path = pathlib.Path(args.out) if args.out else None
    for eps_str in args.epsilons:
        eps = Fraction(eps_str)
        d = target - eps
        for level in range(args.min_level, args.max_level + 1):
            prover = Prover(args.n, d, level, args.max_cited, symmetry=not args.no_symmetry)
            res = prover.run(time_limit=args.time_limit, node_limit=args.node_limit)
            rows.append(
                {
                    "eps": str(eps),
                    "d": str(d),
                    "d_float": float(d),
                    "max_level": level,
                    "status": res["status"],
                    "nodes": res["nodes"],
                    "elapsed_seconds": res["elapsed_seconds"],
                }
            )
            print(
                f"eps={float(eps):<10.6f} d={float(d):<12.7f} L={level:<2} "
                f"{res['status']:<10} nodes={res['nodes']:<12} "
                f"{res['elapsed_seconds']:.2f}s",
                flush=True,
            )
            if out_path:
                out_path.write_text(json.dumps({"n": args.n, "target": str(target),
                                                "rows": rows, "meta": _meta()}, indent=2))
            if res["status"] == "proved":
                break
            if res["status"] == "timeout":
                break
    return 0


VALIDATION = [
    # (n, d, expected status, max_level, max_cited)
    #
    # The mandatory "reproduce a known answer first" gate (repo RULES.md SS6).  Every d is
    # measured against the *cited* optimum d(n) = s(n) - 2*sqrt(3):
    #
    #   d < d(n)  -- a packing does not exist, so the exhaustion must close ("proved");
    #   d >= d(n) -- a packing exists, so it must NOT close.  These rows are the ones that
    #                catch an over-pruning bug, which is the only kind that would make the
    #                emitted bounds wrong.
    #
    # All rows use --max-cited 2, i.e. no literature input beyond "two points at distance
    # 2 need side 2"; otherwise the cited d(n-1) would settle most of them in zero nodes.
    (3, "19/10", "proved", 4, 2),        # d(3)  = 2
    (3, "2", "unresolved", 6, 2),
    (4, "17/5", "proved", 7, 2),         # d(4)  = 2*sqrt(3)  = 3.46410161...
    (4, "3.4642", "unresolved", 7, 2),
    (6, "39/10", "proved", 6, 2),        # d(6)  = 4
    (6, "4", "unresolved", 7, 2),
    (7, "53/10", "proved", 7, 2),        # d(7)  = 2 + 2*sqrt(3) = 5.46410161...
    (10, "6", "unresolved", 6, 2),       # d(10) = 6
    (12, "6.5", "proved", 5, 2),         # d(12) = 4 + 2*sqrt(3) = 7.46410161...
    (16, "7.999", "proved", 6, 2),       # d(16) >= d(15) = 8; best known 9.2495...
]


def cmd_validate(args: argparse.Namespace) -> int:
    ok = True
    t0 = time.time()
    for n, dtxt, expect, level, max_cited in VALIDATION:
        d = Fraction(dtxt)
        res = Prover(n, d, level, max_cited).run(time_limit=args.time_limit)
        good = res["status"] == expect
        ok &= good
        print(
            f"{'ok ' if good else 'FAIL'} n={n:<3} d={float(d):<12.7f} L={level} "
            f"expect={expect:<11} got={res['status']:<11} nodes={res['nodes']:<10} "
            f"{res['elapsed_seconds']:.2f}s",
            flush=True,
        )
    print(f"\n{'all expectations met' if ok else 'VALIDATION FAILED'} "
          f"({time.time() - t0:.0f}s)")
    return 0 if ok else 1


def cmd_constants(args: argparse.Namespace) -> int:
    for k in sorted(D_ENCLOSURE):
        iv = D_ENCLOSURE[k]
        print(f"d({k:>2}) in [{iv.lo!r}, {iv.hi!r}]  width={iv.width():.3e}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="cpbnb")
    sub = ap.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--max-cited", type=int, default=2,
                        help="largest k whose cited d(k) may be used as a capacity bound "
                             "(2 = no literature beyond the trivial two-point case)")
    common.add_argument("--no-symmetry", action="store_true")
    common.add_argument("--time-limit", type=float, default=None)
    common.add_argument("--node-limit", type=int, default=None)
    common.add_argument("--out", default=None)

    p = sub.add_parser("prove", parents=[common])
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--d", required=True)
    p.add_argument("--max-level", type=int, required=True)
    p.add_argument("--checkpoint", default=None)
    p.add_argument("--resume", default=None)
    p.set_defaults(func=cmd_prove)

    p = sub.add_parser("sweep", parents=[common])
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--target", required=True, help="exact rational upper bound for d(n)")
    p.add_argument("--epsilons", nargs="+", required=True)
    p.add_argument("--min-level", type=int, default=2)
    p.add_argument("--max-level", type=int, required=True)
    p.set_defaults(func=cmd_sweep)

    p = sub.add_parser("validate", parents=[common])
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("constants", parents=[common])
    p.set_defaults(func=cmd_constants)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
