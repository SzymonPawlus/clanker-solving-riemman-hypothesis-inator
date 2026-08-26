"""Brute-force exact validation of the theorem's conclusion, member by member,
and emission of the n = 60 (j = 8) certificate.

CONSTRUCTION (upper bound) only.

Order matters: the checker is validated on proven optima and negative controls
FIRST (checker.selftest), then the generator is cross-checked, then and only then
is anything new checked.
"""
import sys, json, os, time
from q3 import E
import gen, checker

HERE = os.path.dirname(os.path.abspath(__file__))
CERTDIR = os.path.join(HERE, "certificates")


def cert_dict(j, rep):
    pts = gen.points(j)
    return {
        "n": gen.n_of(j),
        "claim": "construction",
        "side_length": gen.s_of(j).s(),
        "coordinates": [[x.s(), y.s()] for (x, y) in pts],
        "coordinate_type": "algebraic",
        "verified_by": "experiments/packing-r6-stairthm/checker.py (and theorem.py for all j)",
        "status": "numerical",
        "beats_record": ("no -- no record is claimed. The published Graham-Lubachevsky table "
                         "stops at n = 34; Amore (2022, arXiv:2212.12287) reports triangle "
                         "numerics to N = 400 and is behind this environment's egress block, "
                         "so no comparison is possible from here. This is an exact upper bound "
                         "only."),
        "family": "four-grain staircase, j = %d, n(j) = Delta(j+2) + floor(j/2) + 1" % j,
        "tight": rep["tight"],
        "d_min_exact": rep["d_min_exact"],
        "min_sq_distance": rep["min_sq_distance"],
        "contacts_at_distance_exactly_2": rep["contacts"],
        "points_on_boundary": rep["points_on_boundary"],
    }


def main(JMAX=14, emit=(8,)):
    print("=" * 78)
    print("0. CHECKER VALIDATION (before any new claim is checked)")
    checker.selftest()
    print()
    print("=" * 78)
    print("1. Brute-force exact check of every family member, j = 0..%d" % JMAX)
    print("%-3s %-5s %-16s %-8s %-6s %-6s %-22s %-9s %-6s %s"
          % ("j", "n", "s", "pairs", "feas", "tight", "min sq dist", "contacts", "bdry", "sec"))
    rows = []
    for j in range(JMAX + 1):
        t0 = time.time()
        pts = gen.points(j)
        n = gen.n_of(j)
        assert len(pts) == n, (j, len(pts), n)
        rep = checker.check(n, gen.s_of(j), pts)
        dt = time.time() - t0
        print("%-3d %-5d %-16s %-8d %-6s %-6s %-22s %-9d %-6d %.1f"
              % (j, n, gen.s_of(j).s(), rep["pairs_checked"], rep["ok"], rep["tight"],
                 rep["min_sq_distance"], rep["contacts"], rep["points_on_boundary"], dt))
        assert rep["ok"] and rep["tight"] and rep["min_sq_distance_is_exactly_4"], (j, rep["failures"][:5])
        rows.append((j, n, rep))
        if j in emit:
            os.makedirs(CERTDIR, exist_ok=True)
            path = os.path.join(CERTDIR, "n%03d-r6-stairthm.json" % n)
            with open(path, "w") as f:
                json.dump(cert_dict(j, rep), f, indent=2)
            print("      -> certificate written: %s" % os.path.relpath(path, HERE))
    print()
    print("All %d members feasible, contained and TIGHT in exact Q(sqrt3)." % len(rows))
    print("This is a brute-force CONFIRMATION of theorem.py, not a substitute for it:")
    print("theorem.py covers every j, this covers j = 0..%d pair by pair." % JMAX)
    return rows


if __name__ == "__main__":
    JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    main(JMAX)
