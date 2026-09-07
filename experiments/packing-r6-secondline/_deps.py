"""Dependency preflight for this directory.

numpy was already DECLARED here (pyproject.toml, and §6 of the attack README),
and correctly so: this lane is a floating-point scan over line-family
orientations, offsets and rotations, with no exact fallback.

What was missing is the other half of the contract.  Declaring a dependency in
a pyproject.toml does not stop a bare interpreter from producing a raw
`ModuleNotFoundError` traceback at exit 1, which is what every numpy-importing
script here did.  This module makes the failure actionable and exits 2 instead.

`witness28.py` is deliberately NOT guarded: it is the exact-rational 28-point
witness, uses `fractions.Fraction` and the stdlib alone, and runs green on a
bare interpreter.  That is the intended shape -- the exact certificate does not
need the float stack.

Nothing here may be promoted above `numerical` (repo RULES.md §3); the
comparative reading in the write-up is `refuted`.
"""
import importlib.util
import sys

# module -> (requirement spec, version this lane was actually run with)
REQUIRED = {
    "numpy": ("numpy>=1.26", "2.5.2"),
}


def require(script):
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
    print("  cd experiments/packing-r6-secondline", file=e)
    print("  python3 -m venv .venv", file=e)
    print("  .venv/bin/pip install %s"
          % " ".join("'%s'" % spec for _, spec, _ in missing), file=e)
    print("  .venv/bin/python %s" % script, file=e)
    print("", file=e)
    print("This is a REAL requirement, not an optional diagnostic: this lane is a", file=e)
    print("float scan over line-family orientations and offsets, with no exact", file=e)
    print("fallback.  See attacks/r6-secondline/README.md §6.", file=e)
    print("", file=e)
    print("`python3 witness28.py` needs NONE of this -- the exact-rational 28-point", file=e)
    print("witness runs on the stdlib alone.", file=e)
    raise SystemExit(2)
