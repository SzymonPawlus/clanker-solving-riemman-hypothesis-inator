"""Mandatory validation gate (repo RULES.md section 6): reproduce the known
finite list of exceptions to Robin's inequality below 5041.

Robin (1984) proved that sigma(n) < e^gamma n log log n fails, for n >= 2,
exactly at the 27 integers below (see also Lagarias 2002, "An elementary
problem equivalent to the Riemann hypothesis").  n = 1 is excluded because
log log 1 is undefined.  If the computed set differs in any way, this script
exits nonzero and NOTHING downstream may be reported (kill criterion K1).
"""
import sys
from robin_core import sigma_exact, robin_decide

KNOWN_EXCEPTIONS = [
    2, 3, 4, 5, 6, 8, 9, 10, 12, 16, 18, 20, 24, 30, 36, 48, 60,
    72, 84, 120, 180, 240, 360, 720, 840, 2520, 5040,
]

def main():
    computed = []
    undecided = []
    for n in range(2, 5041):
        verdict, lo, hi = robin_decide(n, sigma_exact(n))
        if verdict == "violates":
            computed.append(n)
        elif verdict == "undecided":
            undecided.append(n)
    ok = (computed == KNOWN_EXCEPTIONS) and not undecided
    print(f"computed {len(computed)} exceptions in [2, 5040]: {computed}")
    if undecided:
        print(f"UNDECIDED at max precision (K3): {undecided}")
    if ok:
        print("VALIDATION PASS: exact match with the known exception list.")
        return 0
    extra = sorted(set(computed) - set(KNOWN_EXCEPTIONS))
    missing = sorted(set(KNOWN_EXCEPTIONS) - set(computed))
    print(f"VALIDATION FAIL: extra={extra} missing={missing}")
    return 1

if __name__ == "__main__":
    sys.exit(main())
