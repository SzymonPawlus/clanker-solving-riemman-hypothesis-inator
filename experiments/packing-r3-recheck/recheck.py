#!/usr/bin/env python3
"""Independent exact checker for circle-packing certificates in Q(sqrt 3).

Written from the problem statement in
  problems/circle-packing-equilateral-triangle/README.md
and the fixed conventions in
  problems/circle-packing-equilateral-triangle/RULES.md  (sections 2 and 3),
without reading, importing, or adapting any other checker in this repo.

Specification, restated in my own words (this is what the code below implements):

  Point formulation.  Packing n unit circles in an equilateral triangle of side s
  is equivalent to placing n points at pairwise distance >= 2 in an equilateral
  triangle of side d = s - 2*sqrt(3).  A certificate reports s (field
  `side_length`), never d.

  Fixed placement (no search over rigid motions):
      A = (0, 0),  B = (d, 0),  C = (d/2, d*sqrt(3)/2).
  The closed triangle is the intersection of three closed half planes:
      (H1)  y >= 0                          [edge AB]
      (H2)  sqrt(3)*x - y >= 0              [edge AC, interior on the right]
      (H3)  sqrt(3)*d - sqrt(3)*x - y >= 0  [edge BC]
  (H2): the line through (0,0) and (d/2, d*sqrt(3)/2) is y = sqrt(3) x; the
  interior point (d/2, d*sqrt(3)/6) (the centroid) gives sqrt(3)*d/2 - d*sqrt(3)/6 > 0,
  fixing the sign.  (H3): the line through (d,0) and (d/2, d*sqrt(3)/2) is
  sqrt(3)*x + y = sqrt(3)*d; the centroid gives sqrt(3)*d/2 + d*sqrt(3)/6 < sqrt(3)*d,
  fixing the sign.

  Minimal enclosing side, in this fixed placement.  d appears in (H3) only, and
  (H3) is equivalent to d >= x + y/sqrt(3) = x + y*sqrt(3)/3.  Hence, provided
  (H1) and (H2) hold for every point (they do not involve d),
      d_min = max_i ( x_i + y_i*sqrt(3)/3 ),
  and the certificate is TIGHT iff the declared d equals d_min, LOOSE (a valid
  but inflated upper bound) iff d > d_min, and INVALID iff d < d_min.

  All inequalities are non-strict.  Decimal strings are banned in exact fields.

All accept/reject decisions below are made in exact arithmetic over Q(sqrt 3):
a number is a pair of `fractions.Fraction`s (a, b) meaning a + b*sqrt(3).  There
is no float anywhere in this file except in the purely cosmetic `approx()` used
for printing.
"""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

# --------------------------------------------------------------------------
# Exact arithmetic in Q(sqrt 3):  x = a + b*sqrt(3),  a, b in Q.
# --------------------------------------------------------------------------


class Q3:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    # ---- ring operations -------------------------------------------------
    def __add__(self, o):
        return Q3(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        return Q3(self.a - o.a, self.b - o.b)

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __mul__(self, o):
        # (a1 + b1 r)(a2 + b2 r) = (a1 a2 + 3 b1 b2) + (a1 b2 + a2 b1) r,  r^2 = 3
        return Q3(self.a * o.a + 3 * self.b * o.b, self.a * o.b + o.a * self.b)

    def __eq__(self, o):
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    # ---- exact sign ------------------------------------------------------
    def sign(self) -> int:
        """Exact sign of a + b*sqrt(3).  No floats: sqrt(3) is irrational, so
        a + b*sqrt(3) == 0 iff a == b == 0 (a, b rational)."""
        a, b = self.a, self.b
        if a == 0 and b == 0:
            return 0
        if a >= 0 and b >= 0:
            return 1
        if a <= 0 and b <= 0:
            return -1
        # mixed signs: compare a^2 against 3 b^2
        if a > 0 > b:
            # a + b r > 0  <=>  a > -b r = |b| r  <=>  a^2 > 3 b^2
            return 1 if a * a > 3 * b * b else (0 if a * a == 3 * b * b else -1)
        # a < 0 < b:  a + b r > 0  <=>  b r > |a|  <=>  3 b^2 > a^2
        return 1 if 3 * self.b * self.b > a * a else (0 if 3 * b * b == a * a else -1)

    def __lt__(self, o):
        return (self - o).sign() < 0

    def __le__(self, o):
        return (self - o).sign() <= 0

    def __gt__(self, o):
        return (self - o).sign() > 0

    def __ge__(self, o):
        return (self - o).sign() >= 0

    # ---- misc ------------------------------------------------------------
    def mul_sqrt3(self):
        """(a + b r) * r = 3b + a r."""
        return Q3(3 * self.b, self.a)

    def div_sqrt3(self):
        """(a + b r) / r = (a + b r) * r / 3 = b + (a/3) r."""
        return Q3(self.b, Fraction(self.a, 3))

    def __repr__(self):
        if self.b == 0:
            return str(self.a)
        if self.a == 0:
            return f"{self.b}*sqrt(3)"
        return f"{self.a} + {self.b}*sqrt(3)"

    def approx(self) -> float:
        """COSMETIC ONLY -- never used in an accept/reject decision."""
        return float(self.a) + float(self.b) * 1.7320508075688772


ZERO = Q3(0, 0)
ONE = Q3(1, 0)
SQRT3 = Q3(0, 1)
FOUR = Q3(4, 0)
TWO_SQRT3 = Q3(0, 2)


# --------------------------------------------------------------------------
# Parsing exact Q(sqrt 3) expression strings.
# --------------------------------------------------------------------------

_TERM = re.compile(
    r"""^\s*
        (?:(?P<num>\d+(?:/\d+)?)\s*(?P<star>\*)?\s*)?   # optional rational coefficient
        (?P<rad>sqrt\(3\))?                             # optional sqrt(3)
        \s*$""",
    re.X,
)


class ParseError(Exception):
    pass


def parse_q3(text) -> Q3:
    """Parse strings of the shape  '4 + 2*sqrt(3)', 'sqrt(3)', '5/2', '0',
    '-1 + 3*sqrt(3)'.  Rejects decimal strings (problem RULES.md section 2
    bans them in exact fields) and anything else it does not fully understand:
    reject rather than guess."""
    if not isinstance(text, str):
        raise ParseError(f"exact field must be a string, got {type(text).__name__}: {text!r}")
    s = text.strip()
    if s == "":
        raise ParseError("empty exact field")
    if "." in s:
        raise ParseError(f"decimal string in exact field (banned by RULES.md section 2): {text!r}")
    if "e" in s.lower().replace("sqrt", "").replace("3", ""):
        raise ParseError(f"unexpected character in exact field: {text!r}")

    # split into signed terms at top level (no parentheses other than sqrt(3))
    depth = 0
    terms, cur, sign = [], "", 1
    i = 0
    # leading sign
    while i < len(s) and s[i] in "+- ":
        if s[i] == "-":
            sign = -sign
        i += 1
    start_sign = sign
    sign = start_sign
    while i < len(s):
        c = s[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth < 0:
                raise ParseError(f"unbalanced parentheses: {text!r}")
        if depth == 0 and c in "+-":
            terms.append((sign, cur))
            cur = ""
            sign = 1 if c == "+" else -1
            i += 1
            # absorb any further signs
            while i < len(s) and s[i] in "+- ":
                if s[i] == "-":
                    sign = -sign
                i += 1
            continue
        cur += c
        i += 1
    if depth != 0:
        raise ParseError(f"unbalanced parentheses: {text!r}")
    terms.append((sign, cur))

    total = Q3(0, 0)
    for sg, t in terms:
        m = _TERM.match(t)
        if not m:
            raise ParseError(f"cannot parse term {t!r} of {text!r}")
        num, star, rad = m.group("num"), m.group("star"), m.group("rad")
        if num is None and rad is None:
            raise ParseError(f"empty term in {text!r}")
        if num is not None and rad is not None and star is None:
            raise ParseError(f"missing '*' between coefficient and radical in {t!r}")
        coeff = Fraction(num) if num is not None else Fraction(1)
        coeff *= sg
        if rad is None:
            total = total + Q3(coeff, 0)
        else:
            total = total + Q3(0, coeff)
    return total


# --------------------------------------------------------------------------
# The check itself.
# --------------------------------------------------------------------------


class Report:
    def __init__(self, label):
        self.label = label
        self.lines = []
        self.ok = True

    def item(self, ok, name, detail=""):
        self.lines.append((bool(ok), name, detail))
        if not ok:
            self.ok = False

    def show(self):
        print(f"--- {self.label}")
        for ok, name, detail in self.lines:
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {name}" + (f"  {detail}" if detail else ""))
        print(f"  => {'ACCEPT' if self.ok else 'REJECT'}: {self.label}")
        return self.ok


def check_points(pts, d, label, expect_tight=None, verbose=True):
    """pts: list of (Q3, Q3).  d: Q3, the side of the POINT triangle (= s - 2 sqrt 3).
    Returns (Report, d_min)."""
    r = Report(label)
    n = len(pts)

    # ---- separation: all C(n,2) squared distances >= 4 --------------------
    worst = None
    contacts = 0
    bad = []
    for (i, (xi, yi)), (j, (xj, yj)) in combinations(list(enumerate(pts)), 2):
        dx = xi - xj
        dy = yi - yj
        d2 = dx * dx + dy * dy
        if worst is None or d2 < worst[0]:
            worst = (d2, i, j)
        c = (d2 - FOUR).sign()
        if c < 0:
            bad.append((i, j, d2))
        elif c == 0:
            contacts += 1
    r.item(
        not bad,
        f"separation: all {n*(n-1)//2} pairwise squared distances >= 4",
        f"min = {worst[0]} (~{worst[0].approx():.12f}) at pair ({worst[1]},{worst[2]}); "
        f"{contacts} exact contacts"
        + ("" if not bad else f"; VIOLATIONS: {[(i, j, str(v)) for i, j, v in bad[:5]]}"),
    )

    # ---- containment in the CLOSED triangle -------------------------------
    # (H1) y >= 0   (H2) sqrt(3) x - y >= 0   (H3) sqrt(3) d - sqrt(3) x - y >= 0
    v1, v2, v3 = [], [], []
    on_boundary = 0
    for i, (x, y) in enumerate(pts):
        h1 = y
        h2 = x.mul_sqrt3() - y
        h3 = d.mul_sqrt3() - x.mul_sqrt3() - y
        if h1.sign() < 0:
            v1.append((i, h1))
        if h2.sign() < 0:
            v2.append((i, h2))
        if h3.sign() < 0:
            v3.append((i, h3))
        if h1.sign() == 0 or h2.sign() == 0 or h3.sign() == 0:
            on_boundary += 1
    r.item(not v1, "containment (H1) y >= 0", "" if not v1 else f"violated at {[(i, str(v)) for i, v in v1]}")
    r.item(
        not v2,
        "containment (H2) sqrt(3)x - y >= 0",
        "" if not v2 else f"violated at {[(i, str(v)) for i, v in v2]}",
    )
    r.item(
        not v3,
        "containment (H3) sqrt(3)x + y <= sqrt(3)d",
        "" if not v3 else f"violated at {[(i, str(v)) for i, v in v3]}",
    )
    r.item(True, "points on the triangle boundary", f"{on_boundary} of {n}")

    # ---- distinctness (a repeated point would be a distance-0 pair, already
    #      caught by separation, but say it explicitly) ---------------------
    r.item(len(set((p[0].a, p[0].b, p[1].a, p[1].b) for p in pts)) == n, "points are pairwise distinct")

    # ---- minimal enclosing side, exact ------------------------------------
    d_min = None
    argmax = None
    for i, (x, y) in enumerate(pts):
        val = x + y.div_sqrt3()  # x + y/sqrt(3)
        if d_min is None or val > d_min:
            d_min = val
            argmax = i
    r.item(True, "exact minimal enclosing d (fixed placement)", f"d_min = {d_min} (~{d_min.approx():.12f}) attained at point {argmax}")
    cmp = (d - d_min).sign()
    tight = cmp == 0
    if cmp < 0:
        r.item(False, "declared d >= d_min", f"declared d = {d} < d_min = {d_min}: the certificate does NOT fit its own declared triangle")
        r.item(True, "tightness", "N/A -- certificate already invalid")
    elif tight:
        r.item(True, "tightness", "TIGHT (declared d == d_min exactly)")
    else:
        r.item(True, "tightness", f"NOT TIGHT: declared d = {d} > d_min = {d_min} (valid but inflated upper bound)")
    return r, d_min, tight


def check_certificate(path, verbose=True):
    cert = json.loads(Path(path).read_text())
    label = f"{path}"
    n_declared = cert["n"]

    pre = Report(f"{label} [structure]")
    try:
        s = parse_q3(cert["side_length"])
        pre.item(True, "side_length parses exactly", f"s = {s} (~{s.approx():.12f})")
    except ParseError as e:
        pre.item(False, "side_length parses exactly", str(e))
        pre.show()
        return False, None
    coords = cert["coordinates"]
    pre.item(len(coords) == n_declared, "len(coordinates) == n", f"{len(coords)} vs n = {n_declared}")
    pts = []
    parse_ok = True
    for i, c in enumerate(coords):
        try:
            if not (isinstance(c, (list, tuple)) and len(c) == 2):
                raise ParseError(f"coordinate {i} is not a 2-list: {c!r}")
            pts.append((parse_q3(c[0]), parse_q3(c[1])))
        except ParseError as e:
            pre.item(False, f"coordinate {i} parses exactly", str(e))
            parse_ok = False
    if parse_ok:
        pre.item(True, "all coordinates parse exactly, no decimal strings", f"{len(pts)} points in Q(sqrt 3)")
    if not parse_ok or not pre.ok:
        pre.show()
        return False, None

    # d = s - 2 sqrt(3), by the reduction in README.md
    d = s - TWO_SQRT3
    pre.item(True, "derived d = s - 2*sqrt(3)", f"d = {d} (~{d.approx():.12f})")
    if "_d" in cert:
        try:
            d_field = parse_q3(cert["_d"])
            pre.item(d_field == d, "informational `_d` field agrees with s - 2*sqrt(3)", f"_d = {d_field}")
        except ParseError as e:
            pre.item(False, "informational `_d` field parses", str(e))
    pre.item(cert.get("claim") == "construction", "claim is 'construction' (upper bound)", f"claim = {cert.get('claim')!r}")
    pre.item(
        cert.get("status") in ("numerical", "verified:review", "verified:lean"),
        "status field is one of the allowed values",
        f"status = {cert.get('status')!r}",
    )
    pre.show()

    r, d_min, tight = check_points(pts, d, f"{label} [n = {n_declared}, s = {s}]")
    ok = r.show() and pre.ok
    return ok, tight


# --------------------------------------------------------------------------
# Control 1: triangular-lattice cases with known optimal s = 2(k-1) + 2 sqrt(3).
# --------------------------------------------------------------------------


def triangular_lattice(k):
    """n = k(k+1)/2 points, rows j = 0..k-1, row j has k-j points.
    Point (i, j) = (2i + j, j*sqrt(3)).  Side d = 2(k-1)."""
    pts = []
    for j in range(k):
        for i in range(k - j):
            pts.append((Q3(2 * i + j, 0), Q3(0, j)))
    return pts, Q3(2 * (k - 1), 0)


def run_positive_controls():
    print("=" * 78)
    print("CONTROL A -- known-optimal triangular cases n = k(k+1)/2, s = 2(k-1) + 2*sqrt(3)")
    print("  (status `cited` in problems/.../README.md, Oler 1961). The checker must")
    print("  ACCEPT these and report them TIGHT.")
    print("=" * 78)
    all_ok = True
    for k in (2, 3, 4, 5, 6):
        n = k * (k + 1) // 2
        pts, d = triangular_lattice(k)
        assert len(pts) == n
        s = d + TWO_SQRT3
        r, d_min, tight = check_points(pts, d, f"triangular lattice k={k}, n={n}, s = {s}")
        ok = r.show() and tight
        print(f"      expected s(n) = 2*{k-1} + 2*sqrt(3) = {s}; tight = {tight}")
        all_ok = all_ok and ok
    return all_ok


# --------------------------------------------------------------------------
# Control 2: negative controls -- deliberately corrupted certificates.
# --------------------------------------------------------------------------


def run_negative_controls(path):
    print("=" * 78)
    print(f"CONTROL B -- negative controls on {path}")
    print("  A checker that accepts everything proves nothing.")
    print("=" * 78)
    cert = json.loads(Path(path).read_text())
    s = parse_q3(cert["side_length"])
    d = s - TWO_SQRT3
    pts = [(parse_q3(c[0]), parse_q3(c[1])) for c in cert["coordinates"]]
    results = {}

    # B1: break separation -- nudge point 0 towards its nearest neighbour by 1/1000.
    # Find the nearest neighbour of point 0 exactly, then move point 0 along x
    # by a small rational in whichever direction shrinks that pair.
    p = list(pts)
    x0, y0 = p[0]
    best = None
    for j in range(1, len(p)):
        dx = x0 - p[j][0]
        dy = y0 - p[j][1]
        d2 = dx * dx + dy * dy
        if best is None or d2 < best[0]:
            best = (d2, j)
    j = best[1]
    eps = Q3(Fraction(1, 1000), 0)
    cand_a = (x0 + eps, y0)
    cand_b = (x0 - eps, y0)

    def sep2(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return dx * dx + dy * dy

    p[0] = cand_a if sep2(cand_a, p[j]) < sep2(cand_b, p[j]) else cand_b
    r, _, _ = check_points(p, d, f"B1 corrupted: point 0 moved by 1/1000 toward point {j} (must REJECT)")
    results["B1 separation broken"] = not r.show()

    # B2: break containment -- push the point attaining d_min outside edge BC.
    p = list(pts)
    dmi, arg = None, None
    for i, (x, y) in enumerate(p):
        v = x + y.div_sqrt3()
        if dmi is None or v > dmi:
            dmi, arg = v, i
    p[arg] = (p[arg][0] + Q3(Fraction(1, 1000), 0), p[arg][1])
    r, _, _ = check_points(p, d, f"B2 corrupted: point {arg} pushed 1/1000 outside edge BC (must REJECT)")
    results["B2 containment broken"] = not r.show()

    # B2b: push a point below edge AB (y < 0).
    p = list(pts)
    low = min(range(len(p)), key=lambda i: (p[i][1].a, p[i][1].b))
    p[low] = (p[low][0], p[low][1] - Q3(Fraction(1, 1000), 0))
    r, _, _ = check_points(p, d, f"B2b corrupted: point {low} pushed 1/1000 below edge AB (must REJECT)")
    results["B2b y<0 broken"] = not r.show()

    # B3: deflate the declared s by 1/1000 -- containment must now FAIL.
    d_small = d - Q3(Fraction(1, 1000), 0)
    r, _, _ = check_points(pts, d_small, "B3 corrupted: declared s deflated by 1/1000 (must REJECT)")
    results["B3 deflated s"] = not r.show()

    # B4: inflate the declared s by 1/1000 -- must be ACCEPTED but NOT TIGHT.
    d_big = d + Q3(Fraction(1, 1000), 0)
    r, _, tight = check_points(pts, d_big, "B4 corrupted: declared s inflated by 1/1000 (must ACCEPT, NOT TIGHT)")
    accepted = r.show()
    results["B4 inflated s -> accept but not tight"] = accepted and not tight

    # B5: a decimal string in an exact field must be rejected by the parser.
    try:
        parse_q3("12.928203230275514")
        results["B5 decimal string rejected"] = False
    except ParseError:
        results["B5 decimal string rejected"] = True

    print()
    print("  negative-control summary (True = the checker behaved as required):")
    for k, v in results.items():
        print(f"    {'OK  ' if v else 'BAD '} {k}: {v}")
    return all(results.values())


# --------------------------------------------------------------------------
# Control C: external consistency with the `cited` triangular values.
#
# s(n) is non-decreasing in n (delete a circle from a packing of n to get one
# of n-1), and s(Delta(k)) = 2(k-1) + 2 sqrt(3) is `cited` (Oler 1961) in
# problems/circle-packing-equilateral-triangle/README.md.  So for the largest
# triangular Delta(k) <= n and the smallest Delta(k') >= n,
#     2(k-1) + 2 sqrt(3)  <=  s(n)  <=  2(k'-1) + 2 sqrt(3).
# The LOWER bracket is a hard validity test on the certificate: a claimed s
# below it would contradict a cited optimality result.  It is exactly the test
# that catches the worst available convention error -- reporting d in the
# `side_length` field instead of s -- because d is smaller than s by 2 sqrt(3)
# and drops out of the bracket.
# --------------------------------------------------------------------------


def run_frontier_consistency(paths):
    print("=" * 78)
    print("CONTROL C -- consistency with the `cited` triangular values (exact)")
    print("=" * 78)
    ok_all = True
    for p in paths:
        cert = json.loads(Path(p).read_text())
        n = cert["n"]
        s = parse_q3(cert["side_length"])
        klo = max(k for k in range(1, 40) if k * (k + 1) // 2 <= n)
        khi = min(k for k in range(1, 40) if k * (k + 1) // 2 >= n)
        lo = Q3(2 * (klo - 1), 2)
        hi = Q3(2 * (khi - 1), 2)
        ok_lo = s >= lo
        ok_hi = s <= hi
        ok_all = ok_all and ok_lo
        print(f"  n = {n}: claimed s = {s} (~{s.approx():.12f})")
        print(
            f"    [{'PASS' if ok_lo else 'FAIL'}] s >= s(Delta({klo}) = {klo*(klo+1)//2}) = {lo} "
            f"(~{lo.approx():.12f})   [hard: cited optimum]"
        )
        print(
            f"    [{'PASS' if ok_hi else 'note'}] s <= s(Delta({khi}) = {khi*(khi+1)//2}) = {hi} "
            f"(~{hi.approx():.12f})   [soft: else the construction is worse than a known one]"
        )
        # what the certificate would look like if `side_length` had been filled
        # with d instead of s -- the error this control exists to catch
        d = s - TWO_SQRT3
        print(
            f"    (if `side_length` had held d = {d} (~{d.approx():.12f}) instead, the hard "
            f"bracket would {'still hold' if d >= lo else 'FAIL -- so this error would be caught'})"
        )
    return ok_all


# --------------------------------------------------------------------------
# Diagnostic (NOT part of any accept/reject decision, and FLOATS are used):
# is the fixed-placement minimal enclosing side also minimal over rotations?
#
# The repo convention fixes the placement, so d_min above is *the* specified
# quantity and this scan can never make a certificate pass or fail.  Its only
# purpose is to notice a would-be finding: if some rotated copy of the point
# set fitted in a strictly smaller equilateral triangle, the same points would
# witness a better upper bound than the one claimed, which is worth flagging
# loudly (it would then have to be re-verified exactly, in the fixed placement).
#
# For outward unit normals u_k(t) = (cos(t + 2 pi k/3), sin(t + 2 pi k/3)),
# the smallest equilateral triangle with those edge normals containing the
# points has side  (2/sqrt 3) * sum_k max_i <p_i, u_k>.
# --------------------------------------------------------------------------


def min_enclosing_over_rotations(pts_float, samples=20000):
    import math

    def side(t):
        tot = 0.0
        for k in range(3):
            a = t + 2 * math.pi * k / 3
            ux, uy = math.cos(a), math.sin(a)
            tot += max(px * ux + py * uy for px, py in pts_float)
        return tot * 2.0 / math.sqrt(3.0)

    best_t, best = None, None
    for i in range(samples):
        t = 2 * math.pi / 3 * i / samples
        v = side(t)
        if best is None or v < best:
            best, best_t = v, t
    # local refinement (ternary search on the sampled bracket)
    lo, hi = best_t - 2 * math.pi / 3 / samples, best_t + 2 * math.pi / 3 / samples
    for _ in range(200):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if side(m1) < side(m2):
            hi = m2
        else:
            lo = m1
    t = (lo + hi) / 2
    return min(best, side(t)), t


def run_orientation_diagnostic(paths):
    import math

    print("=" * 78)
    print("DIAGNOSTIC (floats, NOT load-bearing, cannot pass or fail anything)")
    print("  Would a rotated copy of the same points fit a strictly smaller triangle?")
    print("=" * 78)
    for p in paths:
        cert = json.loads(Path(p).read_text())
        s = parse_q3(cert["side_length"])
        d = (s - TWO_SQRT3).approx()
        pts = [(parse_q3(c[0]).approx(), parse_q3(c[1]).approx()) for c in cert["coordinates"]]
        # self-test of the support formula at the repo's fixed orientation
        # (bottom-edge outward normal (0,-1), i.e. t = -pi/2)
        tot = 0.0
        for k in range(3):
            a = -math.pi / 2 + 2 * math.pi * k / 3
            ux, uy = math.cos(a), math.sin(a)
            tot += max(px * ux + py * uy for px, py in pts)
        fixed = tot * 2.0 / math.sqrt(3.0)
        best, t = min_enclosing_over_rotations(pts)
        print(
            f"  {Path(p).name}: declared d = {d:.12f}; support formula at the fixed "
            f"orientation = {fixed:.12f}; min over rotations = {best:.12f} at t = {t:.6f} rad"
        )
        if best < d - 1e-9:
            print("    *** FLAG: a rotated copy appears to fit a strictly smaller triangle. ***")
        else:
            print("    no rotation improves on the fixed placement (to float tolerance)")


def main(argv):
    root = Path(__file__).resolve().parents[2]
    certs = [
        root / "experiments/packing-r3-qsqrt3/certificates/n017-r3-qsqrt3.json",
        root / "experiments/packing-r3-qsqrt3/certificates/n024-r3-qsqrt3.json",
        root / "experiments/packing-r3-qsqrt3/certificates/n031-r3-qsqrt3.json",
    ]
    if len(argv) > 1:
        certs = [Path(a) for a in argv[1:]]

    pos = run_positive_controls()
    print()
    print("=" * 78)
    print("MAIN -- the three certificates under test")
    print("=" * 78)
    summary = []
    for c in certs:
        ok, tight = check_certificate(str(c))
        summary.append((c.name, ok, tight))
        print()
    neg = run_negative_controls(str(certs[0]))
    print()
    frontier = run_frontier_consistency([str(c) for c in certs])
    print()
    run_orientation_diagnostic([str(c) for c in certs])

    print()
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"  positive controls (triangular lattices n = 3,6,10,15,21): {'ALL PASS' if pos else 'FAILED'}")
    print(f"  control C  (consistency with cited triangular values):    {'ALL PASS' if frontier else 'FAILED'}")
    print(f"  negative controls (corrupted certificates rejected):      {'ALL PASS' if neg else 'FAILED'}")
    for name, ok, tight in summary:
        print(f"  {name}: {'ACCEPT' if ok else 'REJECT'}, tight = {tight}")
    return 0 if (pos and neg and frontier and all(o for _, o, _ in summary)) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
