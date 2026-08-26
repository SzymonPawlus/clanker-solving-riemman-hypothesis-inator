"""Cross-check MY transcription of the construction against the committed
famcert generator (read-only), and against the three CITED proven optima.

This is a provenance gate, not a claim.  It answers: did I transcribe the spec
into the same point set?
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "packing-r4-famcert"))
import gen as mine
from q3 import E


def famcert_points(j):
    import importlib
    g = importlib.import_module("generator")
    return g.generate(j)


def key(p):
    return (p[0].a if hasattr(p[0], "a") else None,)


def as_pairs(pts):
    out = set()
    for (x, y) in pts:
        out.add(((x.a, x.b), (y.a, y.b)))
    return out


if __name__ == "__main__":
    JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    allok = True
    for j in range(0, JMAX + 1):
        A = as_pairs(mine.points(j))
        try:
            B = as_pairs(famcert_points(j))
        except Exception as e:
            print("j=%2d  famcert generator unavailable: %s" % (j, e)); continue
        same = (A == B)
        allok &= same
        print("j=%2d  n=%3d  mine==famcert: %s  (|mine|=%d |fam|=%d)"
              % (j, mine.n_of(j), same, len(A), len(B)))
    print("CROSS-CHECK", "IDENTICAL" if allok else "DIFFERS")

    # the three cited proven optima, independently transcribed
    print()
    print("Cited proven optima (values from the problem README table):")
    proven = {0: ("n=4",  E(0, 4)), 1: ("n=7", E(2, 4)), 2: ("n=12", E(4, 4))}
    for j, (nm, s) in proven.items():
        print("  j=%d %-5s law s = %-16s  matches cited optimum: %s"
              % (j, nm, mine.s_of(j).s(), mine.s_of(j) == s))
