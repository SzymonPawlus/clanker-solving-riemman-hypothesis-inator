"""One command reproduces everything in attacks/r5-n17/README.md.

    cd experiments/packing-r5-n17 && python3 run_all.py

Deterministic, exact, stdlib + sympy (parser only), no network, no seeds.
"""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("0. parser self-test (accepts Q(sqrt3), rejects decimals/other fields)", "parse_exact.py"),
    ("1. checker validation: 4 proven instances + 5 negative controls", "selftest.py"),
    ("2. main audit: cert vs generator at n = 17, 24, 31", "audit.py"),
    ("3. structural diff (which points differ, mobility, degree histograms)", "diffs.py"),
    ("4. exact infinitesimal rigidity ranks and slide intervals", "rigid_run.py"),
    ("5. symmetry stabilisers", "stab.py"),
    ("6. exact free-region endpoints", "n31_seg.py"),
    ("7. independent re-run of the famcert Gate-1/Gate-2 table, j = 0..7", "famtable.py"),
]
for title, script in STEPS:
    print("\n" + "#" * 78 + "\n# " + title + "\n" + "#" * 78)
    r = subprocess.run([sys.executable, script], cwd=HERE)
    if r.returncode != 0:
        sys.exit("step failed: " + script)
