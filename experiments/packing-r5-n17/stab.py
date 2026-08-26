import json, os
from q3 import Q3
from parse_exact import parse
import famgen
from symmetry import maps

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CERTDIR = os.path.join(REPO, "experiments", "packing-r3-qsqrt3", "certificates")


def load_cert(n):
    with open(os.path.join(CERTDIR, "n%03d-r3-qsqrt3.json" % n)) as fh:
        c = json.load(fh)
    return [(parse(a), parse(b)) for a, b in c["coordinates"]], parse(c["side_length"])


def key(p):
    return ((p[0].a, p[0].b), (p[1].a, p[1].b))


for n, j in ((17, 3), (24, 4), (31, 5)):
    A, s = load_cert(n)
    B = famgen.generate(j)
    d = s - Q3(0, 2)
    for tag, P in (("r3-qsqrt3 cert", A), ("r4-famcert gen", B)):
        K = set(map(key, P))
        stab = [nm for nm, f in maps(d) if set(key(f(p)) for p in P) == K]
        print("n=%-3d %-16s stabiliser order %d: %s" % (n, tag, len(stab), [x.split()[0] for x in stab]))
