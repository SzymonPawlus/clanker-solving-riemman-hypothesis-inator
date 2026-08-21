"""Tests for the exact arithmetic and the checker (issue #74).

The negative tests matter more than the positive ones: a checker that accepts everything would
pass every certificate in this directory too. Run: python3 test_exact.py
"""
from __future__ import annotations

import json
import pathlib
import sys
from fractions import Fraction

from quadfield import Q, sqrt
from exact_check import ExactParseError, check_certificate, parse_exact

FAILURES = []


def ok(cond, name):
    print(("PASS  " if cond else "FAIL  ") + name)
    if not cond:
        FAILURES.append(name)


# ------------------------------------------------------------------ arithmetic
def test_arithmetic():
    ok(sqrt(3) * sqrt(3) == Q(3), "sqrt(3)^2 == 3 exactly")
    ok(sqrt(12) == 2 * sqrt(3), "sqrt(12) reduces to 2*sqrt(3)")
    ok(sqrt(33) == sqrt(3) * sqrt(11), "sqrt(33) == sqrt(3)*sqrt(11)")
    ok(sqrt(0) == Q(0), "sqrt(0) == 0")
    ok((sqrt(2) + sqrt(3) - sqrt(5)).sign() > 0, "sqrt2+sqrt3 > sqrt5 (sign test on a small value)")
    ok(not (sqrt(2) + sqrt(3) == sqrt(5)), "sqrt2+sqrt3 != sqrt5 (the classic near-miss)")
    # a genuinely tiny nonzero quantity: sqrt(1000001) - 1000 ~ 5e-4, and an exact zero
    ok((sqrt(1000001) - 1000).sign() > 0, "sign test resolves a small positive value")
    ok((sqrt(4) - 2).is_zero(), "exact zero is detected syntactically, not numerically")
    x = 1 + sqrt(2) + sqrt(3) + sqrt(11)
    ok(x * x.inverse() == Q(1), "inverse in a 3-generator multiquadratic field")
    ok((Q(1) / sqrt(3)) * sqrt(3) == Q(1), "1/sqrt(3) is exact")
    # the sign test must never disagree with a high-precision float
    v = sqrt(11) / 2 - sqrt(3) / 6
    ok(abs(v.approx() - 1.369637260582887) < 1e-12, "approx() agrees with the numeric solve")


# ------------------------------------------------------------------ parser
def test_parser():
    ok(parse_exact("2 + 2*sqrt(3)") == 2 + 2 * sqrt(3), "parses '2 + 2*sqrt(3)'")
    ok(parse_exact("1/2 + sqrt(33)/6") == Q(Fraction(1, 2)) + sqrt(33) / 6, "parses fractions")
    ok(parse_exact("(1+sqrt(3))**2") == 4 + 2 * sqrt(3), "parses integer powers")
    for bad in ["10.928", "1.0", "__import__('os')", "x + 1", "cos(3)", "sqrt(3.0)", "2**0.5"]:
        try:
            parse_exact(bad)
            ok(False, f"rejects {bad!r}")
        except (ExactParseError, ValueError, TypeError):
            ok(True, f"rejects {bad!r}")


# ------------------------------------------------------------------ checker
BASE_N3 = {
    "n": 3, "claim": "construction", "side_length": "2 + 2*sqrt(3)",
    "coordinates": [["0", "0"], ["2", "0"], ["1", "sqrt(3)"]],
    "coordinate_type": "algebraic",
}


def test_checker_negative():
    good = check_certificate(dict(BASE_N3))
    ok(good.ok and good.tight, "control: the exact n=3 corner packing passes and is tight")

    # (a) overlapping points: shrink one coordinate so a distance drops just below 2
    bad = dict(BASE_N3)
    bad["coordinates"] = [["0", "0"], ["199/100", "0"], ["1", "sqrt(3)"]]
    ok(not check_certificate(bad).ok, "rejects a packing with a pairwise distance < 2")

    # (b) a point just outside the triangle
    bad = dict(BASE_N3)
    bad["coordinates"] = [["0", "-1/1000"], ["2", "0"], ["1", "sqrt(3)"]]
    ok(not check_certificate(bad).ok, "rejects a point outside the closed triangle")

    # (c) an INFLATED side length: still feasible, so it must pass but be reported NOT tight.
    #     This is the check that stops an honest-looking certificate from overstating s(n).
    inflated = dict(BASE_N3)
    inflated["side_length"] = "3 + 2*sqrt(3)"
    rep = check_certificate(inflated)
    ok(rep.ok and rep.tight is False, "an inflated side length passes feasibility but is NOT tight")

    # (d) a declared tightness that lies
    lying = dict(inflated)
    lying["tight"] = True
    ok(not check_certificate(lying).ok, "rejects a certificate whose declared tightness is false")

    # (e) an under-stated side length must fail containment outright
    under = dict(BASE_N3)
    under["side_length"] = "1 + 2*sqrt(3)"
    ok(not check_certificate(under).ok, "rejects a side length too small to contain the points")

    # (f) declared point_triangle_side inconsistent with s - 2*sqrt(3)
    incons = dict(BASE_N3)
    incons["point_triangle_side"] = "3"
    ok(not check_certificate(incons).ok, "rejects d inconsistent with s - 2*sqrt(3)")


# ------------------------------------------------------------------ published values
# Taken from the `cited` table in problems/circle-packing-equilateral-triangle/README.md.
# Reproducing these is the validation gate of issue #74; they are a target, not an output.
PUBLISHED = {
    1: "2*sqrt(3)", 2: "2 + 2*sqrt(3)", 3: "2 + 2*sqrt(3)", 4: "4*sqrt(3)",
    5: "4 + 2*sqrt(3)", 6: "4 + 2*sqrt(3)", 7: "2 + 4*sqrt(3)",
    8: "2 + 2*sqrt(3) + 2*sqrt(33)/3", 9: "6 + 2*sqrt(3)", 10: "6 + 2*sqrt(3)",
    14: "8 + 2*sqrt(3)", 15: "8 + 2*sqrt(3)",
    20: "10 + 2*sqrt(3)", 21: "10 + 2*sqrt(3)",
}


def test_certificates(cert_dir: pathlib.Path):
    seen = set()
    for p in sorted(cert_dir.glob("*.json")):
        cert = json.loads(p.read_text())
        n = cert["n"]
        seen.add(n)
        rep = check_certificate(cert, p)
        ok(rep.ok, f"n={n}: certificate passes the exact checker")
        ok(rep.tight, f"n={n}: certificate is tight")
        if n in PUBLISHED:
            ok(parse_exact(cert["side_length"]) == parse_exact(PUBLISHED[n]),
               f"n={n}: exact s equals the published value {PUBLISHED[n]}")
    ok(set(PUBLISHED) <= seen, "a certificate exists for every n in the published-value table")
    # the validation gate of issue #74, called out explicitly
    ok({2, 3, 4, 5, 6} <= seen, "VALIDATION GATE: n = 2,3,4,5,6 reproduced exactly")


if __name__ == "__main__":
    here = pathlib.Path(__file__).resolve().parent
    cert_dir = here / ".." / ".." / "problems" / "circle-packing-equilateral-triangle" / \
        "attacks" / "exact-algebraic-constructions" / "certificates"
    test_arithmetic()
    test_parser()
    test_checker_negative()
    test_certificates(cert_dir.resolve())
    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S):")
        for f in FAILURES:
            print("  -", f)
        sys.exit(1)
    print("ALL TESTS PASS")
