"""One command reproduces everything in attacks/r5-n17/README.md.

    cd experiments/packing-r5-n17 && python3 run_all.py

Deterministic, exact, no network, no seeds.

REQUIRES `sympy` (>=1.12; run with 1.14.0).  This is a REAL dependency, declared
in pyproject.toml, not an optional diagnostic: parse_exact.py is deliberately an
INDEPENDENT parser built on a different engine from the hand-written Q(sqrt3)
parser in ../packing-r3-qsqrt3/run_all.py, and audit.py, diffs.py, rigid_run.py,
stab.py and n31_seg.py all consume it.  Reimplementing it on stdlib would remove
the decorrelation that is the whole reason it exists, so it is declared rather
than made skippable.

    python3 -m venv .venv && .venv/bin/pip install 'sympy>=1.12'
    .venv/bin/python run_all.py
"""
import importlib.util, subprocess, sys, os


def _preflight():
    """Fail fast, before any step, with an actionable message."""
    if importlib.util.find_spec("sympy") is not None:
        return
    e = sys.stderr
    print("packing-r5-n17 requires sympy, which is not installed.", file=e)
    print("", file=e)
    print("  required: sympy>=1.12        tested with: 1.14.0", file=e)
    print("", file=e)
    print("  python3 -m venv .venv", file=e)
    print("  .venv/bin/pip install 'sympy>=1.12'", file=e)
    print("  .venv/bin/python run_all.py", file=e)
    print("", file=e)
    print("This is a REAL dependency (see pyproject.toml): parse_exact.py is an", file=e)
    print("independent exact-field parser and five other steps consume it.  The", file=e)
    print("stdlib-only exact lanes are ../packing-r3-qsqrt3 and", file=e)
    print("../packing-r6-stairthm; neither needs anything installed.", file=e)
    raise SystemExit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("0. parser self-test (accepts Q(sqrt3), rejects decimals/other fields)", "parse_exact.py"),
    ("1. checker validation: 4 proven instances + 5 negative controls", "selftest.py"),
    ("1b. transcription check: my generator vs the r4-famcert generator, j = 0..5", "xcheck_generator.py"),
    ("2. main audit: cert vs generator at n = 17, 24, 31", "audit.py"),
    ("3. structural diff (which points differ, mobility, degree histograms)", "diffs.py"),
    ("4. exact infinitesimal rigidity ranks and slide intervals", "rigid_run.py"),
    ("5. symmetry stabilisers", "stab.py"),
    ("6. exact free-region endpoints", "n31_seg.py"),
    ("7. independent re-run of the famcert Gate-1/Gate-2 table, j = 0..7", "famtable.py"),
]
_preflight()

for title, script in STEPS:
    print("\n" + "#" * 78 + "\n# " + title + "\n" + "#" * 78)
    sys.stdout.flush()   # child writes straight to the fd; flush so the header
                         # is not printed after the output it labels
    r = subprocess.run([sys.executable, script], cwd=HERE)
    if r.returncode != 0:
        sys.exit("step failed: " + script)
