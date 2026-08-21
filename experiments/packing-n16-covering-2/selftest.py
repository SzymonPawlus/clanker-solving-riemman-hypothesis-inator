"""Adversarial self-test of verify_c1.py: every corruption below MUST be rejected.

A certifier that only ever says PASS has not been tested.  Each case names the failure
mode it simulates; the interesting ones are (c) the Lemma-L failure (a piece of diameter
exactly 1 under the strict test) and (f) an overlap paired with a hole of equal area,
which passes the area identity while leaving part of T_a uncovered.
"""
import copy, os, sys
from fractions import Fraction as F
import verify_c1 as V

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cert_rational.json")


def run(name, a, faces, expect_pass=False, strict=True):
    ok, _ = V.check(a, faces, do_cover=True, verbose=False, strict=strict)
    good = (ok == expect_pass)
    print("  %-58s %-8s %s" % (name, "PASS" if ok else "REJECT",
                               "ok" if good else "*** WRONG ***"))
    return good


def main():
    a, faces = V.load(SRC)
    allgood = run("(0) untouched certificate  [must PASS]", a, faces, True)

    f = copy.deepcopy(faces)
    f[3][0] = (f[3][0][0] + F(1, 10), f[3][0][1])
    allgood &= run("(a) one vertex nudged outward (piece leaves T_a / overlaps)", a, f)

    f = copy.deepcopy(faces)
    f[7] = f[7][:-1]
    allgood &= run("(b) one vertex deleted from a piece (hole of positive area)", a, f)

    f = copy.deepcopy(faces)
    mu = F(1000001, 1000000)
    f = [[(u * mu, w * mu) for (u, w) in g] for g in f]
    allgood &= run("(c) dilated until a piece has squared diameter >= 1 (Lemma-L mode)",
                   a * mu, f)

    f = copy.deepcopy(faces)[:-1]
    allgood &= run("(d) one of the 15 pieces removed entirely", a, f)

    f = copy.deepcopy(faces)
    f[2] = f[2][::-1]
    allgood &= run("(e) one piece given clockwise orientation", a, f)

    # (f) overlap + equal-area hole: shift a shared edge so piece 5 eats into piece 6
    # and piece 6 is shrunk by the same amount elsewhere -- area identity still holds.
    f = copy.deepcopy(faces)
    p = f[5][0]
    f[5][0] = (p[0] + F(1, 100), p[1])
    q = f[6][0]
    f[6][0] = (q[0] - F(1, 100), q[1])
    allgood &= run("(f) overlap plus a hole of equal area", a, f)

    f = copy.deepcopy(faces)
    f[9][1], f[9][2] = f[9][2], f[9][1]
    allgood &= run("(g) two vertices of a piece transposed (non-convex)", a, f)

    # (h) the exact Q(sqrt3) configuration under the STRICT test: diameter is exactly 1
    import exact_1p2r3 as E
    ef = [[E.P[k] for k in g] for g in E.FACES]
    allgood &= run("(h) exact a=1+2sqrt3 configuration under the STRICT test", E.A, ef,
                   expect_pass=False, strict=True)
    allgood &= run("(i) same configuration under the non-strict test [must PASS]",
                   E.A, ef, expect_pass=True, strict=False)

    print("\n  self-test: %s" % ("ALL CORRECT" if allgood else "*** A CASE MISBEHAVED ***"))
    return 0 if allgood else 1


if __name__ == "__main__":
    sys.exit(main())
