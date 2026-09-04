#!/usr/bin/env python3
"""
Independent exact checker for circle-packing-in-an-equilateral-triangle certificates.

Written from scratch by worker V5 (claude / Opus 5) from
  problems/circle-packing-equilateral-triangle/README.md   (the statement + reduction)
  problems/circle-packing-equilateral-triangle/RULES.md    (section 2, the certificate format)
without reading, importing or adapting any other checker in this repository.

Everything that decides a reported result is exact: Fraction, or Q(sqrt 3) built on Fraction.
Floats appear only in the human-readable printout, never in a decision.

Usage:  python3 check_v5.py <certificate.json> [--quiet]
Exit status 0 iff every gate passes.
"""

import json
import re
import sys
from fractions import Fraction
from itertools import combinations

# --------------------------------------------------------------------------
# Q(sqrt 3):  a + b*sqrt(3), a, b in Q.  Exact ordered field arithmetic.
# --------------------------------------------------------------------------


class Q3:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    def __add__(self, o):
        o = _q3(o)
        return Q3(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        o = _q3(o)
        return Q3(self.a - o.a, self.b - o.b)

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __mul__(self, o):
        o = _q3(o)
        # (a1 + b1 r)(a2 + b2 r) = a1a2 + 3 b1b2 + (a1b2 + a2b1) r,  r^2 = 3
        return Q3(self.a * o.a + 3 * self.b * o.b, self.a * o.b + o.a * self.b)

    __radd__ = __add__
    __rmul__ = __mul__

    def __rsub__(self, o):
        return _q3(o) - self

    def is_rational(self):
        return self.b == 0

    def sign(self):
        """Exact sign of a + b*sqrt(3).  No floats, no sqrt.

        sqrt(3) is irrational, so a + b*sqrt(3) == 0 iff a == b == 0.
        Same-sign parts: the sign is immediate.  Opposite signs: compare squares
        of two non-negative quantities, which is where the only real work is.
        """
        a, b = self.a, self.b
        if a == 0 and b == 0:
            return 0
        if a >= 0 and b >= 0:
            return 1
        if a <= 0 and b <= 0:
            return -1
        if a > 0 > b:
            # a + b r > 0  <=>  a > (-b) r,  both sides > 0  <=>  a^2 > 3 b^2
            d = a * a - 3 * b * b
            return 1 if d > 0 else -1          # d == 0 impossible (sqrt 3 irrational)
        # a < 0 < b:  a + b r > 0  <=>  b r > -a,  both sides > 0  <=>  3 b^2 > a^2
        d = 3 * b * b - a * a
        return 1 if d > 0 else -1

    def cmp(self, o):
        return (self - _q3(o)).sign()

    def __float__(self):
        # printout only -- never used in a decision
        return float(self.a) + float(self.b) * 1.7320508075688772935

    def __repr__(self):
        return f"({self.a} + {self.b}*sqrt3)"


def _q3(x):
    return x if isinstance(x, Q3) else Q3(x, 0)


SQRT3 = Q3(0, 1)


def dec(v, k=22):
    """Decimal rendering of a Q(sqrt3) value to ~k places.  DISPLAY ONLY.

    Python floats have ~16 significant digits, which is not enough to print an
    s ~ 12.7 that we care about to 1e-14.  Uses integer isqrt, no floats, but no
    gate ever consults this.
    """
    from math import isqrt
    v = _q3(v)
    r = Fraction(isqrt(3 * 10 ** (2 * k + 40)), 10 ** (k + 20))   # sqrt3 to k+20 places
    val = v.a + v.b * r
    sgn = "-" if val < 0 else ""
    val = abs(val)
    ip = val.numerator // val.denominator
    fr = val - ip
    digits = (fr.numerator * 10 ** k) // fr.denominator
    return f"{sgn}{ip}.{str(digits).zfill(k)}"


def _selftest_q3():
    """sign() is the load-bearing primitive; test it against known facts."""
    assert Q3(0, 0).sign() == 0
    assert Q3(1, 0).sign() == 1 and Q3(-1, 0).sign() == -1
    assert Q3(0, 1).sign() == 1 and Q3(0, -1).sign() == -1
    # 1.7320508 < sqrt3 < 1.7320509
    assert Q3(Fraction(-17320508, 10**7), 1).sign() == 1
    assert Q3(Fraction(-17320509, 10**7), 1).sign() == -1
    assert Q3(Fraction(17320508, 10**7), -1).sign() == -1
    assert Q3(Fraction(17320509, 10**7), -1).sign() == 1
    # (a+b r)(a-b r) = a^2 - 3b^2
    x = Q3(Fraction(5, 7), Fraction(-11, 13))
    y = Q3(Fraction(5, 7), Fraction(11, 13))
    p = x * y
    assert p.b == 0 and p.a == Fraction(25, 49) - 3 * Fraction(121, 169)
    # sqrt3^2 = 3
    assert (SQRT3 * SQRT3).a == 3 and (SQRT3 * SQRT3).b == 0
    # transitivity spot-check on a grid
    vals = [Q3(Fraction(i, 3), Fraction(j, 5)) for i in range(-4, 5) for j in range(-4, 5)]
    fl = sorted(vals, key=float)
    for u, v in zip(fl, fl[1:]):
        assert u.cmp(v) <= 0, (u, v)


# --------------------------------------------------------------------------
# Strict parsing of exact fields.  Decimal strings are banned (RULES.md s2).
# --------------------------------------------------------------------------

RAT_RE = re.compile(r"^[+-]?\d+(?:/\d+)?$")


class ParseError(ValueError):
    pass


def parse_rational(tok, where):
    tok = tok.strip()
    if not RAT_RE.match(tok):
        raise ParseError(
            f"{where}: {tok!r} is not an exact integer or integer/integer "
            f"(decimal strings are banned in exact fields)"
        )
    return Fraction(tok)


# side_length may legitimately be irrational: s = d + 2*sqrt(3).  Accept a sum of
# terms, each either a rational or rational*sqrt(3).  Nothing else.
TERM_RE = re.compile(r"^([+-]?\d+(?:/\d+)?)(\*sqrt\(3\))?$")


def parse_q3(expr, where):
    e = "".join(expr.split())
    if not e:
        raise ParseError(f"{where}: empty")
    # split on + / - that are not the leading sign
    parts, cur = [], ""
    for i, ch in enumerate(e):
        if ch in "+-" and i > 0:
            parts.append(cur)
            cur = ch
        else:
            cur += ch
    parts.append(cur)
    tot = Q3(0, 0)
    for p in parts:
        m = TERM_RE.match(p)
        if not m:
            raise ParseError(f"{where}: term {p!r} is not <rational> or <rational>*sqrt(3)")
        c = Fraction(m.group(1))
        tot = tot + (Q3(0, c) if m.group(2) else Q3(c, 0))
    return tot


# --------------------------------------------------------------------------
# The geometry, derived from README.md, not copied from anyone.
#
#   Reduction (README.md):  n unit circles in an equilateral triangle of side s
#   <=> n points at pairwise distance >= 2 in an equilateral triangle of side
#       d = s - 2*sqrt(3).                       <-- separation TWO, not one
#
#   Placement (RULES.md s2, fixed, no search over rigid motions):
#       A = (0,0),  B = (d,0),  C = (d/2, d*sqrt(3)/2).
#
#   Closed-triangle containment.  Each edge gives a half-plane; orient it by the
#   opposite vertex.
#     edge AB: line y = 0.        C has y = d*sqrt3/2 > 0   =>   y >= 0
#     edge AC: through (0,0) and (d/2, d*sqrt3/2), i.e. y = sqrt3*x.
#              At B=(d,0): sqrt3*d - 0 > 0                  =>   sqrt3*x - y >= 0
#     edge BC: through (d,0) and (d/2, d*sqrt3/2), i.e. y = sqrt3*(d - x).
#              At A=(0,0): sqrt3*d - 0 > 0                  =>   sqrt3*(d-x) - y >= 0
#   All non-strict (RULES.md s2): optima put points exactly on edges.
#
#   Minimal enclosing side at this FIXED placement.  Only the BC constraint
#   involves d:  sqrt3*(d - x_i) >= y_i  <=>  d >= x_i + y_i/sqrt3.  The other two
#   are d-free.  Hence, provided y_i >= 0 and sqrt3*x_i >= y_i for all i,
#       d_min = max_i ( x_i + y_i/sqrt3 ),        y/sqrt3 = (y/3)*sqrt3.
#   and the certificate is TIGHT iff d == d_min.
# --------------------------------------------------------------------------


def containment_q3(x, y, d):
    """Exact Q(sqrt3) containment.  Returns (ok, per-constraint signs)."""
    c1 = _q3(y)                       # y >= 0
    c2 = SQRT3 * x - y                # sqrt3*x - y >= 0
    c3 = SQRT3 * (_q3(d) - x) - y     # sqrt3*(d-x) - y >= 0
    s = [c1.sign(), c2.sign(), c3.sign()]
    return all(v >= 0 for v in s), s


def containment_squared(x, y, d):
    """The squaring encoding, for rational x, y, d only.

    sqrt3*x >= y  <=>  x >= 0 AND 3x^2 >= y^2, GIVEN y >= 0.
      (=>) y >= 0 and sqrt3*x >= y >= 0 force x >= 0; squaring two non-negatives
           preserves the order, so 3x^2 >= y^2.
      (<=) x >= 0 and 3x^2 >= y^2 give sqrt3*x = sqrt(3x^2) >= sqrt(y^2) = |y| >= y.
    The (<=) direction needs no hypothesis on y, so the encoding never ACCEPTS an
    outside point; the (=>) direction needs y >= 0, so without that gate it could
    REJECT a legitimate one (e.g. x = -1, y = -5).  y >= 0 is checked first, so on
    the conjunction the two encodings are equivalent.  check_encoding_equivalence()
    exercises exactly this.
    """
    if not (isinstance(x, Fraction) and isinstance(y, Fraction) and isinstance(d, Fraction)):
        return None
    ok1 = y >= 0
    ok2 = (x >= 0) and (3 * x * x >= y * y)
    u = d - x
    ok3 = (u >= 0) and (3 * u * u >= y * y)
    return ok1 and ok2 and ok3, [ok1, ok2, ok3]


def check_encoding_equivalence(trials=4000, seed=20260822):
    """Confirm the squaring step really is an equivalence -- and find where it is not."""
    import random

    rng = random.Random(seed)
    d = Fraction(9, 2)
    agree = disagree_reject = disagree_accept = 0
    for _ in range(trials):
        x = Fraction(rng.randint(-600, 600), rng.choice([1, 2, 3, 7, 100]))
        y = Fraction(rng.randint(-600, 600), rng.choice([1, 2, 3, 7, 100]))
        a = containment_q3(Q3(x, 0), Q3(y, 0), d)[0]
        b = containment_squared(x, y, d)[0]
        if a == b:
            agree += 1
        elif a and not b:
            disagree_reject += 1
        else:
            disagree_accept += 1
    # The unguarded lemma (drop y >= 0) must fail in the reject direction only.
    bad_accept = 0
    for _ in range(trials):
        x = Fraction(rng.randint(-600, 600), rng.choice([1, 2, 3, 7]))
        y = Fraction(rng.randint(-600, 600), rng.choice([1, 2, 3, 7]))
        true_ac = (SQRT3 * Q3(x, 0) - Q3(y, 0)).sign() >= 0
        sq_ac = (x >= 0) and (3 * x * x >= y * y)
        if sq_ac and not true_ac:
            bad_accept += 1
    return agree, disagree_reject, disagree_accept, bad_accept


# --------------------------------------------------------------------------
# The checker
# --------------------------------------------------------------------------


def check(path, verbose=True):
    raw = open(path).read()
    cert = json.loads(raw)
    log, fail = [], []

    def gate(name, ok, detail=""):
        log.append((name, "PASS" if ok else "FAIL", detail))
        if not ok:
            fail.append(name)
        return ok

    # ---- G0  schema and exact-field hygiene -------------------------------
    n = cert["n"]
    coords_raw = cert["coordinates"]
    gate("G0.1 n matches coordinate count", len(coords_raw) == n, f"n={n}, got {len(coords_raw)}")
    gate("G0.2 claim is a construction", cert.get("claim") == "construction", repr(cert.get("claim")))

    ctype = cert.get("coordinate_type")
    gate("G0.3 coordinate_type is one of rational|algebraic|interval",
         ctype in ("rational", "algebraic", "interval"), repr(ctype))

    # every coordinate must parse as an exact rational, matching coordinate_type
    pts = []
    parse_ok = True
    for i, (xs, ys) in enumerate(coords_raw):
        try:
            pts.append((parse_rational(xs, f"coord[{i}].x"), parse_rational(ys, f"coord[{i}].y")))
        except ParseError as e:
            parse_ok = False
            log.append((f"G0.4 parse coord[{i}]", "FAIL", str(e)))
            fail.append(f"G0.4 parse coord[{i}]")
    gate("G0.4 all coordinates are exact rationals, no decimal strings",
         parse_ok and len(pts) == n)
    gate("G0.5 coordinate_type matches the actual encoding",
         ctype == "rational" and parse_ok,
         "declared 'rational'; every coordinate parsed as p/q with no decimal point, "
         "no exponent, no radical")
    if not parse_ok:
        return log, fail, {}

    # side_length: exact expression in Q(sqrt3), no decimal strings
    s = parse_q3(cert["side_length"], "side_length")
    gate("G0.6 side_length is an exact Q(sqrt3) expression, no decimal strings", True,
         f"s = {s}")

    # ---- the reduction:  d = s - 2*sqrt(3)  (README.md) -------------------
    d = s - Q3(0, 2)
    gate("G1.0 d = s - 2*sqrt(3) is rational (fixed placement is then rational)",
         d.is_rational(), f"d = {d}")
    dq = d.a
    gate("G1.1 d > 0", dq > 0, f"d = {dq} ~ {float(dq):.18f}")

    # ---- G2  pairwise separation >= 2  (SEPARATION IS 2, NOT 1) ----------
    worst = None
    npairs = 0
    for i, j in combinations(range(n), 2):
        npairs += 1
        dx = pts[i][0] - pts[j][0]
        dy = pts[i][1] - pts[j][1]
        q = dx * dx + dy * dy
        if worst is None or q < worst[0]:
            worst = (q, i, j)
    gate("G2.0 all C(n,2) pairs examined", npairs == n * (n - 1) // 2, f"{npairs} pairs")
    gate("G2.1 every squared distance >= 4 (separation 2)", worst[0] >= 4,
         f"min at pair ({worst[1]},{worst[2]}): dist^2 - 4 = {float(worst[0] - 4):.6e}")

    # ---- G3  containment in the CLOSED triangle, two independent encodings
    bad_q3, bad_sq, mismatch = [], [], []
    for i, (x, y) in enumerate(pts):
        ok_a, sgn = containment_q3(Q3(x, 0), Q3(y, 0), dq)
        ok_b, _ = containment_squared(x, y, dq)
        if not ok_a:
            bad_q3.append((i, sgn))
        if not ok_b:
            bad_sq.append(i)
        if ok_a != ok_b:
            mismatch.append(i)
    gate("G3.1 all points in the closed triangle (exact Q(sqrt3) half-planes)",
         not bad_q3, f"{len(bad_q3)} violations" + (f": {bad_q3}" if bad_q3 else ""))
    gate("G3.2 same verdict from the independent squared encoding",
         not bad_sq and not mismatch,
         f"{len(bad_sq)} violations, {len(mismatch)} encoding mismatches")

    ag, dr, da, bad_accept = check_encoding_equivalence()
    gate("G3.3 squaring step is an equivalence under y >= 0 (randomised)",
         dr == 0 and da == 0,
         f"{ag} agree / {dr} spurious-reject / {da} spurious-accept over 4000 random points")
    gate("G3.4 unguarded squaring never ACCEPTS an outside point",
         bad_accept == 0, f"{bad_accept} false accepts in 4000 random points")

    # ---- G4  minimal enclosing side at the fixed placement, and tightness --
    dmin = None
    argmax = None
    for i, (x, y) in enumerate(pts):
        # x + y/sqrt3 = x + (y/3)*sqrt3
        v = Q3(x, y / 3)
        if dmin is None or v.cmp(dmin) > 0:
            dmin, argmax = v, i
    gap = Q3(dq, 0) - dmin
    gate("G4.1 reported side_length is a valid upper bound (d >= d_min)",
         gap.sign() >= 0,
         f"d - d_min = {dec(gap, 20)}, argmax point {argmax}")
    tight = gap.sign() == 0
    smin = dmin + Q3(0, 2)

    stats = {
        "n": n,
        "d": dq,
        "s": s,
        "min_sq_dist": worst[0],
        "min_pair": (worst[1], worst[2]),
        "d_min": dmin,
        "s_min": smin,
        "gap": gap,
        "argmax": argmax,
        "tight": tight,
        "pts": pts,
    }

    if verbose:
        w = max(len(k) for k, _, _ in log)
        print(f"=== independent exact check (V5) of {path} ===")
        for k, v, det in log:
            print(f"  [{v}] {k.ljust(w)}  {det}")
        print()
        print(f"  n                        {n}")
        print(f"  d (point-formulation)    {dq}")
        print(f"                        ~= {dec(dq)}")
        print(f"  s = d + 2*sqrt(3)     ~= {dec(s)}")
        print(f"  min pairwise dist^2      {worst[0]}")
        print(f"                        ~= 4 + {float(worst[0] - 4):.6e}")
        print(f"  exact minimal enclosing d_min = {dmin}")
        print(f"                        ~= {dec(dmin)}")
        print(f"  exact minimal enclosing s_min ~= {dec(smin)}")
        print(f"  d - d_min             ~= {dec(gap, 20)}   -> "
              f"{'TIGHT' if tight else 'NOT TIGHT (honest upper bound)'}")
        print()
        print("  VERDICT:", "ALL GATES PASS" if not fail else f"FAILED: {fail}")
    return log, fail, stats


if __name__ == "__main__":
    _selftest_q3()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    p = args[0] if args else (
        "problems/circle-packing-equilateral-triangle/attacks/n16-upper-2/n16-certificate.json")
    _, failures, _ = check(p, verbose="--quiet" not in sys.argv)
    sys.exit(1 if failures else 0)
