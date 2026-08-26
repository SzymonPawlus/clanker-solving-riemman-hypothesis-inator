"""r5-n17 audit: are the r3-qsqrt3 certificate and the r4-famcert generator output
the same packing at n = 17, 24, 31?

Everything exact in Q(sqrt 3).  Run: python3 audit.py
"""
import json, os, sys
from fractions import Fraction as F
from q3 import Q3
from parse_exact import parse
import checker as ck
import famgen
from symmetry import maps

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CERTDIR = os.path.join(REPO, "experiments", "packing-r3-qsqrt3", "certificates")
OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def load_cert(n):
    with open(os.path.join(CERTDIR, "n%03d-r3-qsqrt3.json" % n)) as fh:
        c = json.load(fh)
    pts = [(parse(a), parse(b)) for a, b in c["coordinates"]]
    return c, pts, parse(c["side_length"])


def key(p):
    return ((p[0].a, p[0].b), (p[1].a, p[1].b))


def report(tag, rep):
    print("  %-18s ok=%-5s tight=%-5s minsq=%-4s contacts=%-4d bdry=%-3d d_min=%s"
          % (tag, rep["ok"], rep["tight"], rep["min_sq_distance"],
             rep["n_contacts"], rep["n_boundary"], rep["d_min"]))
    for f in rep["failures"][:6]:
        print("       *** FAIL:", f)


results = {}
for n, j in ((17, 3), (24, 4), (31, 5)):
    print("=" * 78)
    print("n = %d   (famcert j = %d)" % (n, j))
    cert, A, sA = load_cert(n)
    B = famgen.generate(j)
    sB = famgen.s_of(j)
    print("  declared s: cert %-16s generator %-16s equal=%s"
          % (sA.sexpr(), sB.sexpr(), sA == sB))

    repA = ck.check(A, sA, cert["n"])
    repB = ck.check(B, sB, famgen.law_n(j))
    report("r3-qsqrt3 cert", repA)
    report("r4-famcert gen", repB)

    kA, kB = set(map(key, A)), set(map(key, B))
    assert len(kA) == len(A) and len(kB) == len(B), "duplicate points!"
    shared = len(kA & kB)
    print("  IDENTICAL POINT SETS: %s   (shared %d / %d)" % (kA == kB, shared, n))

    # symmetry test
    d = sA - Q3(0, 2)
    sym_hit = []
    for name, f in maps(d):
        img = set(key(f(p)) for p in A)
        if img == kB:
            sym_hit.append(name)
    print("  related by a triangle symmetry: %s" % (sym_hit if sym_hit else "NO (all 6 tested)"))

    # rattlers
    ratA = ck.rattlers(A, sA)
    ratB = ck.rattlers(B, sB)
    print("  rattlers  cert: %d   generator: %d" % (len(ratA), len(ratB)))
    for tag, rl in (("cert", ratA), ("gen", ratB)):
        for r in rl:
            print("     %-4s idx %-3d at (%s, %s)  free radius in [%s, %s]  min nbr sq %s  min wall %s"
                  % (tag, r["index"], r["point"][0], r["point"][1],
                     F(r["free_radius_lo"]).limit_denominator(10**6),
                     F(r["free_radius_hi"]).limit_denominator(10**6),
                     r["min_nbr_sqdist"], r["min_wall"]))

    results[n] = {
        "j": j, "s": sA.sexpr(),
        "cert": {k: repA[k] for k in ("ok", "tight", "min_sq_distance", "n_contacts",
                                      "n_boundary", "d_min", "pairs_checked", "failures")},
        "gen": {k: repB[k] for k in ("ok", "tight", "min_sq_distance", "n_contacts",
                                     "n_boundary", "d_min", "pairs_checked", "failures")},
        "identical_point_sets": kA == kB,
        "shared_points": shared,
        "symmetry_related": sym_hit,
        "rattlers_cert": ratA,
        "rattlers_gen": ratB,
        "cert_declared_contacts": cert.get("_contacts_at_distance_exactly_2"),
        "cert_declared_boundary": cert.get("_points_on_the_boundary"),
    }

with open(os.path.join(OUT, "audit.json"), "w") as fh:
    json.dump(results, fh, indent=1)
print("\nwrote", os.path.join(OUT, "audit.json"))
