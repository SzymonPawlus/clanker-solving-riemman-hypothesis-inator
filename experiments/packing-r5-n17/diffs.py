import json, os
from fractions import Fraction as F
from q3 import Q3
from parse_exact import parse
import checker as ck
import famgen

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CERTDIR = os.path.join(REPO, "experiments", "packing-r3-qsqrt3", "certificates")


def load_cert(n):
    with open(os.path.join(CERTDIR, "n%03d-r3-qsqrt3.json" % n)) as fh:
        c = json.load(fh)
    return c, [(parse(a), parse(b)) for a, b in c["coordinates"]], parse(c["side_length"])


def key(p):
    return ((p[0].a, p[0].b), (p[1].a, p[1].b))


def show(p):
    return "(%s, %s)" % (p[0].sexpr(), p[1].sexpr())


def mobility(pts, i, s):
    """Exact classification of how point i can move, holding the others fixed.
    Returns (n_contacts, wall_contacts, free_radius_bracket, slide_dirs)."""
    d = s - Q3(0, 2)
    n = len(pts)
    cts = [j for j in range(n) if j != i and ck.sqdist(pts[i], pts[j]) == Q3(4, 0)]
    w = ck.walls(pts[i], d)
    won = [k for k, v in w.items() if v.is_zero()]
    lo, hi = ck.free_radius_bracket(pts, i, d)
    return cts, won, (lo, hi)


for n, j in ((17, 3), (24, 4), (31, 5)):
    print("=" * 78)
    cert, A, s = load_cert(n)
    B = famgen.generate(j)
    lab = famgen.labelled(j)
    kA, kB = set(map(key, A)), set(map(key, B))
    onlyA = [p for p in A if key(p) not in kB]
    onlyB = [(a, p) for (a, r, x, p) in lab if key(p) not in kA]
    print("n = %d   |A\\B| = %d   |B\\A| = %d" % (n, len(onlyA), len(onlyB)))
    if onlyA:
        print("  in r3-qsqrt3 cert only:")
        for p in sorted(onlyA, key=lambda p: (p[1].a, p[1].b, p[0].a, p[0].b)):
            i = A.index(p)
            cts, won, (lo, hi) = mobility(A, i, s)
            print("    %-34s contacts=%d walls=%s free_r~%s"
                  % (show(p), len(cts), won or "-", float(lo)))
    if onlyB:
        print("  in r4-famcert generator only:")
        for (g, p) in sorted(onlyB, key=lambda t: (t[1][1].a, t[1][1].b, t[1][0].a, t[1][0].b)):
            i = B.index(p)
            cts, won, (lo, hi) = mobility(B, i, s)
            print("    %-34s grain=%-3s contacts=%d walls=%s free_r~%s"
                  % (show(p), g, len(cts), won or "-", float(lo)))

    # zero-contact points in each
    for tag, P in (("cert", A), ("gen", B)):
        zc = []
        for i in range(len(P)):
            cts, won, (lo, hi) = mobility(P, i, s)
            if not cts:
                zc.append((i, P[i], won, lo, hi))
        print("  %s: points with ZERO contacts: %d" % (tag, len(zc)))
        for (i, p, won, lo, hi) in zc:
            print("     idx %-3d %-30s wall-contacts=%s free_radius in [%.9f, %.9f]"
                  % (i, show(p), won or "-", float(lo), float(hi)))
    # contact degree distribution
    for tag, P in (("cert", A), ("gen", B)):
        rep = ck.check(P, s)
        from collections import Counter
        print("  %s degree histogram: %s   contacts=%d  boundary=%d"
              % (tag, sorted(Counter(rep["contact_degree"]).items()),
                 rep["n_contacts"], rep["n_boundary"]))
