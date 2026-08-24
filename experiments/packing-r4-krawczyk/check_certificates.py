"""Re-read the emitted certificate FILES from disk and verify them from scratch.

CONSTRUCTION SIDE ONLY.  This is a *self*-check: it guards against emission and
string-formatting bugs (the objects verified in run_all.py are in memory; these are the bytes
on disk).  It is NOT an independent checker in the sense of problem RULES.md §3 -- for that see
out/recheck-crosscheck.txt, produced by ../packing-r3-recheck/recheck.py.

Run:  python3 check_certificates.py
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys
from fractions import Fraction
from math import isqrt

DEN = 10 ** 60
S3_LO = Fraction(isqrt(3 * DEN * DEN), DEN)
S3_HI = S3_LO + Fraction(1, DEN)

ALG = re.compile(r"^(-?\d+(?:/\d+)?)?(?:\*?sqrt\(3\))?$")


def parse_q3(s: str) -> tuple[Fraction, Fraction]:
    """Parse 'a + b*sqrt(3)' style exact expressions into (a, b).  Decimal strings rejected."""
    if "." in s:
        raise ValueError(f"decimal string banned in an exact field: {s!r}")
    a = Fraction(0)
    b = Fraction(0)
    for tok in re.findall(r"[+-]?[^+-]+", s.replace(" ", "")):
        if "sqrt(3)" in tok:
            c = tok.replace("sqrt(3)", "").rstrip("*")
            if c in ("", "+"):
                c = "1"
            elif c == "-":
                c = "-1"
            b += Fraction(c)
        else:
            a += Fraction(tok)
    return a, b


def q3_bounds(a: Fraction, b: Fraction) -> tuple[Fraction, Fraction]:
    if b >= 0:
        return a + b * S3_LO, a + b * S3_HI
    return a + b * S3_HI, a + b * S3_LO


def check_algebraic(cert) -> list[str]:
    """Exact check in Q(sqrt 3): coordinates are (p, q*sqrt(3)) so everything closes."""
    errs = []
    n = cert["n"]
    pts = []
    for sx, sy in cert["coordinates"]:
        ax, bx = parse_q3(sx)
        ay, by = parse_q3(sy)
        if bx != 0 or ay != 0:
            errs.append("coordinate outside the expected (rational, rational*sqrt(3)) shape")
            return errs
        pts.append((ax, by))          # x = ax,  y = by*sqrt(3)
    if len(pts) != n:
        errs.append("coordinate count != n")
        return errs
    sa, sb = parse_q3(cert["side_length"])
    if sb != 2:
        errs.append("side_length is not of the form rational + 2*sqrt(3)")
    d = sa                            # d = s - 2*sqrt(3)
    m2 = None
    for i in range(n):
        for j in range(i + 1, n):
            q = (pts[i][0] - pts[j][0]) ** 2 + 3 * (pts[i][1] - pts[j][1]) ** 2
            m2 = q if m2 is None or q < m2 else m2
            if q < 4:
                errs.append(f"pair {i},{j} closer than 2")
    for x, u in pts:
        if u < 0:
            errs.append("point below edge AB")
        if x - u < 0:
            errs.append("point outside edge AC")
        if d - x - u < 0:
            errs.append("point outside edge BC")
    d_min = max(x + u for x, u in pts)
    tight = d == d_min
    if d < d_min:
        errs.append("declared side smaller than the minimal enclosing side")
    if cert.get("_tight") != tight:
        errs.append(f"_tight field says {cert.get('_tight')}, recomputed {tight}")
    return errs


def check_interval(cert) -> list[str]:
    """Universally quantified check: every selection from the boxes must be feasible."""
    errs = []
    n = cert["n"]
    boxes = []
    for (xl, xh), (yl, yh) in cert["coordinates"]:
        for s in (xl, xh, yl, yh):
            if "." in s or "sqrt" in s:
                errs.append("interval endpoints must be exact rationals")
                return errs
        boxes.append((Fraction(xl), Fraction(xh), Fraction(yl), Fraction(yh)))
    if len(boxes) != n:
        errs.append("box count != n")
        return errs
    sa, sb = parse_q3(cert["side_length"])
    if sb != 2:
        errs.append("side_length is not of the form rational + 2*sqrt(3)")
    d = sa
    for i in range(n):
        for j in range(i + 1, n):
            dxlo = boxes[i][0] - boxes[j][1]
            dxhi = boxes[i][1] - boxes[j][0]
            dx2 = 0 if dxlo <= 0 <= dxhi else min(abs(dxlo), abs(dxhi)) ** 2
            dylo = boxes[i][2] - boxes[j][3]
            dyhi = boxes[i][3] - boxes[j][2]
            dy2 = 0 if dylo <= 0 <= dyhi else min(abs(dylo), abs(dyhi)) ** 2
            if dx2 + dy2 < 4:
                errs.append(f"pair {i},{j} can be closer than 2")
    for xlo, xhi, ylo, yhi in boxes:
        if ylo < 0:
            errs.append("box crosses edge AB")
        if xlo < 0 or 3 * xlo * xlo < yhi * yhi:
            errs.append("box crosses edge AC")
        if d - xhi < 0 or 3 * (d - xhi) ** 2 < yhi * yhi:
            errs.append("box crosses edge BC")
    return errs


def main():
    here = os.path.join(os.path.dirname(__file__), "certificates")
    bad = 0
    for path in sorted(glob.glob(os.path.join(here, "*.json"))):
        cert = json.load(open(path))
        if cert["coordinate_type"] == "algebraic":
            errs = check_algebraic(cert)
        elif cert["coordinate_type"] == "interval":
            errs = check_interval(cert)
        else:
            errs = [f"unexpected coordinate_type {cert['coordinate_type']!r}"]
        name = os.path.basename(path)
        if errs:
            bad += 1
            print(f"FAIL {name}: {errs[:3]}")
        else:
            print(f"pass {name} ({cert['coordinate_type']}, n={cert['n']})")
    print(f"\n{bad} failures")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
