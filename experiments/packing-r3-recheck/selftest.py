#!/usr/bin/env python3
"""Self-tests for the Q(sqrt 3) arithmetic and the parser in recheck.py.

The sign() routine is the single point on which every accept/reject decision
rests, so it is tested against high-precision mpmath (1000 dps) on random
inputs, and the parser is tested on the shapes that appear in certificates
plus shapes it must reject.
"""
import random
from fractions import Fraction

from mpmath import mp, mpf, sqrt

from recheck import Q3, ParseError, parse_q3

mp.dps = 1000
R = sqrt(mpf(3))


def test_sign():
    random.seed(20260823)
    bad = 0
    for _ in range(20000):
        a = Fraction(random.randint(-50, 50), random.randint(1, 12))
        b = Fraction(random.randint(-50, 50), random.randint(1, 12))
        got = Q3(a, b).sign()
        ref = mpf(a.numerator) / a.denominator + (mpf(b.numerator) / b.denominator) * R
        exp = 0 if ref == 0 else (1 if ref > 0 else -1)
        if got != exp:
            bad += 1
            print("  MISMATCH", a, b, got, exp)
    print(f"  sign(): 20000 random cases, {bad} mismatches vs mpmath 1000 dps")
    return bad == 0


def test_arith():
    ok = True
    # (1 + sqrt3)^2 = 4 + 2 sqrt3
    ok &= Q3(1, 1) * Q3(1, 1) == Q3(4, 2)
    # sqrt3 * sqrt3 = 3
    ok &= Q3(0, 1) * Q3(0, 1) == Q3(3, 0)
    # (a + b r)*r / r == a + b r
    ok &= Q3(Fraction(5, 2), Fraction(-3, 7)).mul_sqrt3().div_sqrt3() == Q3(Fraction(5, 2), Fraction(-3, 7))
    # exact zero only when both parts vanish
    ok &= Q3(3, -Fraction(3, 1)).sign() != 0 and Q3(0, 0).sign() == 0
    # 2 - sqrt3 > 0 (4 > 3), 1 - sqrt3 < 0 (1 < 3)
    ok &= Q3(2, -1).sign() == 1 and Q3(1, -1).sign() == -1
    # sqrt(12) = 2 sqrt3: (0,2)^2 = 12
    ok &= Q3(0, 2) * Q3(0, 2) == Q3(12, 0)
    print(f"  arithmetic identities: {'OK' if ok else 'FAILED'}")
    return ok


def test_parser():
    good = {
        "0": Q3(0, 0),
        "4": Q3(4, 0),
        "5/2": Q3(Fraction(5, 2), 0),
        "sqrt(3)": Q3(0, 1),
        "2*sqrt(3)": Q3(0, 2),
        "4 + 2*sqrt(3)": Q3(4, 2),
        "4+2*sqrt(3)": Q3(4, 2),
        "  3 + 3*sqrt(3) ": Q3(3, 3),
        "-1 + 3*sqrt(3)": Q3(-1, 3),
        "1 - 2*sqrt(3)": Q3(1, -2),
        "3/2*sqrt(3)": Q3(0, Fraction(3, 2)),
    }
    ok = True
    for s, want in good.items():
        try:
            got = parse_q3(s)
        except ParseError as e:
            print(f"  FAILED to parse {s!r}: {e}")
            ok = False
            continue
        if got != want:
            print(f"  MISPARSE {s!r}: got {got}, want {want}")
            ok = False
    bad = ["12.928203230275514", "1.0", "sqrt(2)", "2 sqrt(3)", "", "x", "1e3", "sqrt(3)/3", "2**sqrt(3)", "(1+2)*sqrt(3)"]
    for s in bad:
        try:
            v = parse_q3(s)
            print(f"  ACCEPTED what it must reject: {s!r} -> {v}")
            ok = False
        except ParseError:
            pass
    print(f"  parser: {'OK' if ok else 'FAILED'} ({len(good)} accepted shapes, {len(bad)} rejected shapes)")
    return ok


if __name__ == "__main__":
    print("selftest.py -- Q(sqrt 3) arithmetic and parser")
    r = all([test_arith(), test_sign(), test_parser()])
    print("ALL SELF-TESTS PASS" if r else "SELF-TESTS FAILED")
    raise SystemExit(0 if r else 1)
