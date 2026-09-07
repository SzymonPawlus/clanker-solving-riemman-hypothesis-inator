"""Dependency preflight for this directory.

WHY THESE ARE DECLARED AND NOT MADE "OPTIONAL".

This lane is a semidefinite-programming instrument.  theta'(G) is computed by
`theta_prime_repaired`, which builds a cvxpy SDP over a numpy matrix and solves
it with CLARABEL/SCS; `alpha_exact` is a scipy `milp`; `chi_bar_f` is a scipy
`linprog` over networkx cliques; `mpmath` at 60 dps decides the exact
distance-2 ties that define the conflict graph's edge set.

There is no stdlib fallback for any of that, and none should be invented: an
SDP solver and an exact-tie test are precisely the components a hand-rolled
substitute would get subtly wrong.  The self-test's whole job is to check the
instrument against known values (theta'(C5) = sqrt5, theta'(Petersen) = 4, the
sandwich alpha <= theta' <= chi-bar_f), so an instrument that did not run has
nothing to self-test.

So the dependencies are DECLARED (see pyproject.toml and the attack README §5)
rather than dressed up as optional diagnostics, and this module turns a bare
ImportError traceback into an actionable message with exit code 2.

`analyse_p1.py` is the exception and is deliberately NOT guarded: it only reads
the committed results_p1.json with the stdlib, so the tables of the write-up can
be regenerated on a bare interpreter.

Nothing here may be promoted above `numerical` (repo RULES.md §3): a relaxation
value from a float SDP solver is a hypothesis about a bound, never a bound.
"""
import importlib.util
import sys

# module -> (requirement spec, version this lane was actually re-run with)
REQUIRED = {
    "numpy": ("numpy>=1.26", "2.5.2"),
    "scipy": ("scipy>=1.11", "1.18.1"),
    "cvxpy": ("cvxpy>=1.4", "1.9.2"),
    "networkx": ("networkx>=3.0", "3.6.1"),
    "mpmath": ("mpmath>=1.3.0", "1.3.0"),
}


def require(script="theta2_core.py --selftest"):
    missing = [(m, spec, tested) for m, (spec, tested) in REQUIRED.items()
               if importlib.util.find_spec(m) is None]
    if not missing:
        return
    e = sys.stderr
    print("This lane requires dependencies that are not installed.", file=e)
    print("", file=e)
    for m, spec, tested in missing:
        print("  missing: %-9s  required: %-16s  tested with: %s" % (m, spec, tested), file=e)
    print("", file=e)
    print("  cd experiments/packing-r5-theta2", file=e)
    print("  python3 -m venv .venv", file=e)
    print("  .venv/bin/pip install %s"
          % " ".join("'%s'" % spec for _, spec, _ in missing), file=e)
    print("  .venv/bin/python %s" % script, file=e)
    print("", file=e)
    print("These are REAL requirements, not optional diagnostics: theta' here is a", file=e)
    print("cvxpy SDP, alpha is a scipy MILP, and mpmath decides the exact distance-2", file=e)
    print("ties of the conflict graph.  There is no stdlib fallback.", file=e)
    print("", file=e)
    print("`python3 analyse_p1.py` needs NONE of these -- it regenerates the tables of", file=e)
    print("the write-up from the committed results_p1.json using the stdlib alone.", file=e)
    print("The exact certificate lanes (packing-r3-qsqrt3, packing-r6-stairthm) are", file=e)
    print("stdlib-only and unaffected.", file=e)
    raise SystemExit(2)
