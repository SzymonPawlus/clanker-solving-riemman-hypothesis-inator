"""Dependency preflight for this directory.

Unlike the exact certificate lanes in this PR, THIS lane is a floating-point
maximin optimiser.  It genuinely requires numpy and scipy -- there is no
stdlib fallback, and pretending otherwise would be dishonest.  So the
dependency is DECLARED (see pyproject.toml and README.md) rather than made
"optional", and this module turns a bare ImportError traceback into an
actionable message.

Nothing in this directory is exact, and nothing here may be promoted above
`numerical` (repo RULES.md §3, problem RULES.md §0 and §5).
"""
import importlib.util
import sys

# module -> (requirement spec, version this lane was actually run with)
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
    print("", file=e)
    print("These are REAL requirements, not optional diagnostics: this directory is a", file=e)
    print("float optimiser and has no exact fallback.  The exact certificate lanes", file=e)
    print("(packing-r3-qsqrt3, packing-r6-stairthm) are stdlib-only and unaffected.", file=e)
    raise SystemExit(2)
