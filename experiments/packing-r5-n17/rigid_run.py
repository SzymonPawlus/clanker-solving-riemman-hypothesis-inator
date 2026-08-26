import json, os
from fractions import Fraction as F
from q3 import Q3
from parse_exact import parse
import checker as ck, famgen, rigidity as rg

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CERTDIR = os.path.join(REPO, "experiments", "packing-r3-qsqrt3", "certificates")


def load_cert(n):
    with open(os.path.join(CERTDIR, "n%03d-r3-qsqrt3.json" % n)) as fh:
        c = json.load(fh)
    return [(parse(a), parse(b)) for a, b in c["coordinates"]], parse(c["side_length"])


# sanity on a rigid solved case: n = 6 lattice in d = 4 should be rigid (kernel 0)
pts6 = [(Q3(2 * i + r), Q3(0, r)) for r in range(3) for i in range(3 - r)]
rows, lab, nc = rg.rigidity_matrix(pts6, Q3(4, 2))
print("control n=6 lattice: rows=%d cols=%d rank=%d kernel=%d" % (len(rows), nc, rg.rank(rows, nc), nc - rg.rank(rows, nc)))
# control: a single free point in a big triangle -> kernel 2
print("control 1 free point: kernel=%d" % (2 - rg.rank(*rg.rigidity_matrix([(Q3(3), Q3(1))], Q3(10, 2))[:1], 2) if False else 2 - rg.rank(rg.rigidity_matrix([(Q3(3), Q3(1))], Q3(10, 2))[0], 2)))

for n, j in ((17, 3), (24, 4), (31, 5)):
    A, s = load_cert(n)
    B = famgen.generate(j)
    print("=" * 70)
    for tag, P in (("r3-qsqrt3 cert", A), ("r4-famcert gen", B)):
        rows, lab, nc = rg.rigidity_matrix(P, s)
        rk = rg.rank(rows, nc)
        print("n=%-3d %-16s rows=%-4d cols=%-4d rank=%-4d kernel=%-2d  (%d contact rows, %d wall rows)"
              % (n, tag, len(rows), nc, rk, nc - rk,
                 sum(1 for l in lab if l[0] == "contact"), sum(1 for l in lab if l[0] == "wall")))
    # slide intervals for zero-contact points
    for tag, P in (("cert", A), ("gen", B)):
        for i in range(len(P)):
            if not any(ck.sqdist(P[i], P[k]) == Q3(4, 0) for k in range(len(P)) if k != i):
                for dname, dvec in (("x", (Q3(1), Q3(0))), ("y", (Q3(0), Q3(1)))):
                    iv = rg.slide_interval(P, i, s, dvec)
                    print("   %s idx %d (%s, %s) slide along %s: [%.9f, %.9f]"
                          % (tag, i, P[i][0].sexpr(), P[i][1].sexpr(), dname, float(iv[0]), float(iv[1])))
