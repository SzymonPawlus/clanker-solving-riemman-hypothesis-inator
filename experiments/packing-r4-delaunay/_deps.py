"""Dependency preflight for this directory.

WHY THESE ARE DECLARED AND NOT MADE "OPTIONAL".

`framework.py` is stdlib-only (`fractions.Fraction`, `math.isqrt`) and carries
STEP 0, the exact configuration self-checks.  Everything that follows is not.
STEP 1 (the Oler control), STEP 2 (the reduced LP), STEP 3 (the full per-shape
LP) and STEP 4 (the verdict against the kill-criterion) are all decided by
`scipy.optimize.linprog`, a floating-point LP solver.  There is no stdlib
fallback and no exact fallback: the *result* of this directory IS the LP
optimum.  Skipping the LP would not leave a reduced-but-honest pipeline, it
would leave STEP 0 and no finding at all.

So the dependency is DECLARED (see pyproject.toml and the attack README) rather
than dressed up as an optional diagnostic, and this module turns a bare
ImportError traceback into an actionable message with exit code 2.

Contrast ../packing-r3-qsqrt3 and ../packing-r6-stairthm, which really are
stdlib-only and whose third-party imports really are optional second opinions.

Nothing in this directory may be promoted above `numerical` (repo RULES.md §3):
an LP optimum from a float solver is a hypothesis about the family, not a bound.
"""
import importlib.util
import sys

# module -> (requirement spec, version this lane was actually re-run with)
REQUIRED = {
    "numpy": ("numpy>=1.26", "2.5.2"),
    "scipy": ("scipy>=1.11", "1.18.1"),
}


def require():
    missing = [(m, spec, tested) for m, (spec, tested) in REQUIRED.items()
               if importlib.util.find_spec(m) is None]
    if not missing:
        return
    e = sys.stderr
    print("This lane requires dependencies that are not installed.", file=e)
    print("", file=e)
    for m, spec, tested in missing:
        print("  missing: %-6s  required: %-14s  tested with: %s" % (m, spec, tested), file=e)
    print("", file=e)
    print("  python3 -m venv .venv", file=e)
    print("  .venv/bin/pip install %s"
          % " ".join("'%s'" % spec for _, spec, _ in missing), file=e)
    print("  .venv/bin/python experiments/packing-r4-delaunay/run.py", file=e)
    print("", file=e)
    print("These are REAL requirements, not optional diagnostics: STEPS 1-4 of this", file=e)
    print("lane are decided by scipy.optimize.linprog and have no exact fallback.", file=e)
    print("The exact certificate lanes (packing-r3-qsqrt3, packing-r6-stairthm) are", file=e)
    print("stdlib-only and unaffected.", file=e)
    raise SystemExit(2)
