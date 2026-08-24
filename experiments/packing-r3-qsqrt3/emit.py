"""Emit certificates in the schema of
problems/circle-packing-equilateral-triangle/RULES.md §2.

CONSTRUCTION (upper bound) only.  No optimality is claimed anywhere.
Certificates are written to ./certificates/ and NOT to problems/*/results/ --
that directory takes only assumable claims (repo RULES.md §4) and these are
`numerical` until a second agent reimplements the checker (problem RULES.md §3).
"""
import json, os
from qsqrt3 import Q3
import configs
from check import check

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "certificates")

PUBLISHED = {
    17: "Graham-Lubachevsky, Electron. J. Combin. 2 (1995) #A1, as tabulated in "
        "experiments/circle-packing-search/reference.py: m(17) = 0.211324865405187, "
        "i.e. s(17) = 12.928203230275514",
    24: "Graham-Lubachevsky, Electron. J. Combin. 2 (1995) #A1, as tabulated in "
        "experiments/circle-packing-search/reference.py: m(24) = 0.174457630187010, "
        "i.e. s(24) = 14.928203230275472",
    31: "Graham-Lubachevsky, Electron. J. Combin. 2 (1995) #A1, as tabulated in "
        "experiments/circle-packing-search/reference.py: m(31) = 0.148543145110506, "
        "i.e. s(31) = 16.928203230275471",
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for n in (17, 24, 31):
        d = getattr(configs, "D%d" % n)
        pts = getattr(configs, "P%d" % n)
        rep = check(n, d, pts, verbose=False)
        assert rep["ok"] and rep["tight"], "n=%d failed its own check" % n
        cert = {
            "n": n,
            "claim": "construction",
            "side_length": (d + Q3(0, 2)).sexpr(),
            "coordinates": [[x.sexpr(), y.sexpr()] for (x, y) in pts],
            "coordinate_type": "algebraic",
            "verified_by": "experiments/packing-r3-qsqrt3/check.py (exact Q(sqrt 3) "
                           "arithmetic, stdlib Fraction only, no floats in any decision). "
                           "SELF-CHECKED ONLY. Under "
                           "problems/circle-packing-equilateral-triangle/RULES.md §3 this "
                           "earns verified:review only from an independently written checker "
                           "by an agent of a different model family; that has not happened.",
            "status": "numerical",
            "beats_record": "no. This exactly reproduces the published best-known value; it "
                            "does not improve it. Published record: " + PUBLISHED[n],
            "_field_semantics": "side_length is s = d + 2*sqrt(3); coordinates are in the "
                                "point formulation, triangle A=(0,0), B=(d,0), "
                                "C=(d/2, d*sqrt(3)/2), pairwise distances >= 2.",
            "_d": d.sexpr(),
            "_claim_precise": "s(%d) <= %s. This is an UPPER BOUND (a construction). It is NOT "
                              "a claim that %s is optimal; n = %d is open."
                              % (n, (d + Q3(0, 2)).sexpr(), (d + Q3(0, 2)).sexpr(), n),
            "_tight": True,
            "_tightness_witness": "the exact minimal enclosing side for this point set in this "
                                  "fixed placement is d_min = max_i (x_i + y_i*sqrt(3)/3) = "
                                  + rep["d_min_exact"] + ", equal to the declared d.",
            "_min_squared_distance": rep["min_sq_distance"],
            "_contacts_at_distance_exactly_2": rep["n_contacts"],
            "_points_on_the_boundary": rep["n_on_boundary"],
            "_provenance": "float configuration from experiments/circle-packing-ls/out/n%d.json "
                           "(LS billiard + SLSQP, seed 20260818), snapped to Q(sqrt 3) by "
                           "experiments/packing-r3-qsqrt3/snap.py; rattlers placed by "
                           "rattler.py. Only the exact check in check.py is load-bearing." % n,
        }
        path = os.path.join(OUT, "n%03d-r3-qsqrt3.json" % n)
        with open(path, "w") as fh:
            json.dump(cert, fh, indent=2)
            fh.write("\n")
        print("wrote %s   s(%d) <= %s   tight=%s   contacts=%d"
              % (os.path.relpath(path, HERE), n, cert["side_length"], rep["tight"],
                 rep["n_contacts"]))
    # guard: no decimal strings may appear in the exact fields
    import re
    for n in (17, 24, 31):
        with open(os.path.join(OUT, "n%03d-r3-qsqrt3.json" % n)) as fh:
            c = json.load(fh)
        blob = json.dumps([c["side_length"], c["coordinates"], c["_d"]])
        assert not re.search(r"\d\.\d", blob), "decimal string leaked into an exact field"
    print("guard: no decimal strings in any exact field.")


if __name__ == "__main__":
    main()
