"""Independent exact checker for equilateral-triangle packing certificates (issue #74).

Reimplemented from the problem statement in
problems/circle-packing-equilateral-triangle/README.md and the certificate conventions in that
directory's RULES.md 2. No other checker in this repo was read, imported, or adapted.

Conventions taken verbatim from RULES.md 2 and NOT reinterpreted:
  * point formulation: n points, pairwise distance >= 2, in the closed triangle of side
    d = s - 2*sqrt(3);
  * triangle placed at A = (0,0), B = (d,0), C = (d/2, d*sqrt(3)/2); no search over rigid motions;
  * `side_length` in a certificate is s, never d;
  * every inequality is non-strict;
  * decimal strings are refused in exact fields.

Containment, derived once here rather than copied: with A, B, C as above (counter-clockwise), a
point P = (x,y) lies in the closed triangle iff

    y >= 0,        y <= sqrt(3) * x,        y <= sqrt(3) * (d - x).

Only the third constraint involves d, and it is increasing in d, so the exact minimal enclosing
side for a fixed point set in this fixed position is

    d_min = max_i ( x_i + y_i / sqrt(3) ),

which is what "tight" is measured against (RULES.md 2, "Consistency of side_length").

Usage:
    python3 exact_check.py cert1.json cert2.json ...
    python3 exact_check.py --dir some/directory
"""

from __future__ import annotations

import argparse
import ast
import json
import pathlib
import sys
from fractions import Fraction

from quadfield import QF, Q, sqrt

SQRT3 = sqrt(3)


# ---------------------------------------------------------------- parsing
class ExactParseError(ValueError):
    pass


_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
}


def parse_exact(text: str) -> QF:
    """Parse a restricted arithmetic expression over Z, +, -, *, /, integer powers and sqrt(int).

    Floats are rejected outright: a decimal literal in an exact field is nearly always truncated
    optimiser output wearing a disguise (RULES.md 2, "Decimal strings are banned").
    """
    if not isinstance(text, str):
        raise ExactParseError(f"exact field must be a string, got {type(text).__name__}")
    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError as exc:
        raise ExactParseError(f"cannot parse {text!r}: {exc}") from exc

    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(node.value, int):
                raise ExactParseError(f"only integer literals allowed, found {node.value!r}")
            return Q(node.value)
        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -ev(node.operand)
            if isinstance(node.op, ast.UAdd):
                return ev(node.operand)
            raise ExactParseError("unsupported unary operator")
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Pow):
                exp = node.right
                if not (isinstance(exp, ast.Constant) and isinstance(exp.value, int) and exp.value >= 0):
                    raise ExactParseError("exponent must be a non-negative integer literal")
                return ev(node.left) ** exp.value
            fn = _BINOPS.get(type(node.op))
            if fn is None:
                raise ExactParseError("unsupported binary operator")
            return fn(ev(node.left), ev(node.right))
        if isinstance(node, ast.Call):
            if not (isinstance(node.func, ast.Name) and node.func.id == "sqrt"):
                raise ExactParseError("the only callable allowed is sqrt")
            if len(node.args) != 1 or node.keywords:
                raise ExactParseError("sqrt takes exactly one positional argument")
            arg = node.args[0]
            if not (isinstance(arg, ast.Constant) and isinstance(arg.value, int) and not isinstance(arg.value, bool)):
                raise ExactParseError("sqrt argument must be a non-negative integer literal")
            return sqrt(arg.value)
        raise ExactParseError(f"disallowed syntax node {type(node).__name__}")

    return ev(tree)


def parse_point(entry) -> tuple[QF, QF]:
    if not (isinstance(entry, (list, tuple)) and len(entry) == 2):
        raise ExactParseError(f"a coordinate must be a 2-element list, got {entry!r}")
    return parse_exact(entry[0]), parse_exact(entry[1])


# ---------------------------------------------------------------- checking
class Report:
    def __init__(self, path):
        self.path = path
        self.lines: list[str] = []
        self.ok = True
        self.tight = None

    def check(self, cond: bool, msg: str):
        self.ok &= bool(cond)
        self.lines.append(("  PASS  " if cond else "  FAIL  ") + msg)
        return cond


def check_certificate(cert: dict, path="<inline>") -> Report:
    rep = Report(path)
    n = cert["n"]
    pts = [parse_point(p) for p in cert["coordinates"]]
    rep.check(len(pts) == n, f"coordinate count is n = {n}")

    s = parse_exact(cert["side_length"])
    d = s - 2 * SQRT3
    if "point_triangle_side" in cert:
        d_decl = parse_exact(cert["point_triangle_side"])
        rep.check(d_decl == d, f"declared point_triangle_side agrees with s - 2*sqrt(3): {d}")
    rep.check(d >= Q(0), f"d = s - 2*sqrt(3) >= 0   (d = {d} ~ {d.approx():.12f})")
    rep.check(cert.get("claim") == "construction", "claim is 'construction' (upper bound only)")

    # containment
    bad = []
    for i, (x, y) in enumerate(pts):
        if not (y >= Q(0) and y <= SQRT3 * x and y <= SQRT3 * (d - x)):
            bad.append(i)
    rep.check(not bad, f"all {n} points lie in the closed triangle (violations: {bad})")

    # pairwise separation, exact: squared distance >= 4
    worst = None
    viol = []
    for i in range(n):
        for j in range(i + 1, n):
            dx = pts[i][0] - pts[j][0]
            dy = pts[i][1] - pts[j][1]
            q = dx * dx + dy * dy
            if q < Q(4):
                viol.append((i, j))
            if worst is None or q < worst:
                worst = q
    if n >= 2:
        rep.check(not viol, f"all {n*(n-1)//2} squared distances >= 4 (violations: {viol})")
        rep.lines.append(f"  info  min squared distance = {worst} ~ {worst.approx():.12f}")
        rep.check(worst >= Q(4), "min squared distance >= 4")

    # tightness: exact minimal enclosing d for these points in this position
    inv3 = Q(1) / SQRT3
    d_min = Q(0)
    for x, y in pts:
        v = x + y * inv3
        if v > d_min:
            d_min = v
    rep.lines.append(f"  info  exact minimal enclosing d = {d_min} ~ {d_min.approx():.12f}")
    rep.tight = bool(d_min == d)
    rep.lines.append(("  PASS  " if rep.tight else "  note  ") +
                     ("certificate is TIGHT: minimal enclosing d equals the declared d"
                      if rep.tight else
                      f"certificate is NOT tight: declared d exceeds minimal enclosing d by {d - d_min}"))
    if cert.get("tight") is not None:
        rep.check(bool(cert["tight"]) == rep.tight, f"declared tightness matches ({rep.tight})")
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description="exact checker for triangle-packing certificates")
    ap.add_argument("certs", nargs="*", type=pathlib.Path)
    ap.add_argument("--dir", type=pathlib.Path, default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    paths = list(args.certs)
    if args.dir:
        paths += sorted(args.dir.glob("*.json"))
    if not paths:
        ap.error("no certificates given")

    all_ok = True
    for p in paths:
        cert = json.loads(p.read_text())
        rep = check_certificate(cert, p)
        all_ok &= rep.ok
        head = "OK  " if rep.ok else "FAIL"
        print(f"[{head}] {p.name}: n={cert['n']} s={cert['side_length']} "
              f"~{parse_exact(cert['side_length']).approx():.12f} tight={rep.tight}")
        if not args.quiet or not rep.ok:
            for line in rep.lines:
                print(line)
    print("\nALL CERTIFICATES PASS" if all_ok else "\nSOME CERTIFICATES FAILED")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
