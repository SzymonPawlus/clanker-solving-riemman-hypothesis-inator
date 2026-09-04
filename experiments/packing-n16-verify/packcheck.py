#!/usr/bin/env python3
"""Independent exact checker for packing certificates in this problem's format.

Written from problems/circle-packing-equilateral-triangle/RULES.md section 2 alone.
It does not import, read or adapt any other agent's checker.

Conventions (RULES.md section 2, taken verbatim, not reinterpreted):
  * point formulation: n points, pairwise distance >= 2, in the CLOSED equilateral
    triangle of side d = s - 2*sqrt(3) placed as A=(0,0), B=(d,0), C=(d/2, d*sqrt3/2);
  * `side_length` is s, never d;
  * every inequality is NON-STRICT;
  * no search over rigid motions;
  * tightness: the certificate is tight iff d equals the exact minimal enclosing side
    for the given points in that fixed placement, i.e.
        d_min = max_i ( x_i + y_i/sqrt(3) )        [given y_i >= 0 and sqrt3*x_i >= y_i]
    which is the smallest d for which all three closed half-plane constraints hold.

Usage:  python3 packcheck.py <certificate.json> [...]
        python3 packcheck.py --selftest
"""

import itertools
import json
import sys

import sympy as sp

S3 = sp.sqrt(3)


def parse_scalar(v):
    """Exact parse.  Rejects bare decimal strings in exact fields (RULES.md section 2)."""
    if isinstance(v, str):
        if any(c.isdigit() for c in v) and "." in v:
            raise ValueError(f"decimal string in an exact field: {v!r}")
        return sp.nsimplify(sp.sympify(v, rational=True), rational=False)
    if isinstance(v, int):
        return sp.Integer(v)
    raise ValueError(f"non-exact scalar {v!r} (floats are banned in exact fields)")


def parse_point(pt, ctype):
    if ctype == "interval":
        (xl, xh), (yl, yh) = pt
        return ("iv", (parse_scalar(xl), parse_scalar(xh)),
                (parse_scalar(yl), parse_scalar(yh)))
    return ("pt", parse_scalar(pt[0]), parse_scalar(pt[1]))


def sgn(e):
    """Exact sign of a sympy algebraic real."""
    r = sp.simplify(sp.radsimp(e))
    s = r.is_positive, r.is_negative, r.is_zero
    if s[2]:
        return 0
    if s[0]:
        return 1
    if s[1]:
        return -1
    # fall back to interval arithmetic at high precision, then force a decision
    v = sp.N(r, 60)
    if abs(v) < sp.Float("1e-40"):
        raise ValueError(f"cannot decide sign of {r}")
    return 1 if v > 0 else -1


class Report:
    def __init__(self):
        self.fail = []
        self.n = 0

    def ck(self, cond, label):
        self.n += 1
        if not cond:
            self.fail.append(label)
        return cond


def check_cert(path, rep, verbose=True):
    cert = json.load(open(path))
    n = cert["n"]
    ctype = cert.get("coordinate_type", "algebraic")
    coords = cert["coordinates"]
    rep.ck(len(coords) == n, f"{path}: coordinate count == n")

    s = parse_scalar(cert["side_length"])
    d = sp.simplify(s - 2 * S3)
    if "point_triangle_side" in cert:
        d2 = parse_scalar(cert["point_triangle_side"])
        rep.ck(sgn(d - d2) == 0, f"{path}: point_triangle_side == side_length - 2*sqrt(3)")
        d = d2

    if ctype == "interval":
        raise NotImplementedError("interval certificates: extend parse below before use")

    P = [parse_point(p, ctype) for p in coords]
    P = [(x, y) for (_, x, y) in P]

    # --- containment in the CLOSED triangle, all three edges, non-strict
    for i, (x, y) in enumerate(P):
        rep.ck(sgn(y) >= 0, f"{path}: point {i} above AB (y >= 0)")
        rep.ck(sgn(S3 * x - y) >= 0, f"{path}: point {i} right of AC")
        rep.ck(sgn(S3 * (d - x) - y) >= 0, f"{path}: point {i} left of BC")

    # --- all C(n,2) pairwise squared distances >= 4
    mind2 = None
    argmin = None
    for i, j in itertools.combinations(range(n), 2):
        q = sp.expand((P[i][0] - P[j][0]) ** 2 + (P[i][1] - P[j][1]) ** 2)
        rep.ck(sgn(q - 4) >= 0, f"{path}: pair ({i},{j}) squared distance >= 4")
        if mind2 is None or sgn(q - mind2) < 0:
            mind2, argmin = q, (i, j)
    npairs = n * (n - 1) // 2

    # --- tightness: exact minimal enclosing side in the fixed placement
    dmin = None
    for (x, y) in P:
        e = sp.simplify(x + y / S3)
        if dmin is None or sgn(e - dmin) > 0:
            dmin = e
    tight = sgn(d - dmin) == 0

    if verbose:
        print(f"  {path}")
        print(f"    n={n}  pairs checked={npairs}")
        if mind2 is None:
            mind2, argmin = sp.oo, None
        print(f"    s = {sp.simplify(s)} = {float(sp.N(s,30)):.15f}")
        print(f"    d = {sp.simplify(d)} = {float(sp.N(d,30)):.15f}")
        print(f"    min squared distance = {sp.simplify(mind2)}  at pair {argmin}")
        print(f"    exact minimal enclosing d_min = {sp.simplify(dmin)} "
              f"= {float(sp.N(dmin,30)):.15f}")
        print(f"    TIGHT: {tight}   (d - d_min = {sp.simplify(d - dmin)})")
        if "tight" in cert:
            ok = (bool(cert["tight"]) == tight)
            rep.ck(ok, f"{path}: certificate's own `tight` field agrees with my computation")
            print(f"    certificate claims tight={cert['tight']}: {'AGREES' if ok else 'DISAGREES'}")
    return {"n": n, "s": s, "d": d, "mind2": mind2, "dmin": dmin, "tight": tight}


def selftest():
    rep = Report()
    print("=== self-test on the repo's existing exact certificates ===")
    base = "../../problems/circle-packing-equilateral-triangle/"
    paths = [base + "attacks/exact-algebraic-constructions/certificates/n00%d-exact.json" % k
             for k in (1, 2, 3, 4, 5, 6)]
    paths += [base + "results/n003-lean-corners.json", base + "results/n006-lean-t3-lattice.json"]
    for p in paths:
        try:
            check_cert(p, rep)
        except FileNotFoundError:
            print("  (missing)", p)

    print("\n=== negative controls (both MUST be rejected) ===")
    import tempfile, os
    good = json.load(open(base + "attacks/exact-algebraic-constructions/certificates/n004-exact.json"))
    # (a) shrink the triangle by a hair: a point must fall outside
    bad = dict(good)
    bad["side_length"] = "4*sqrt(3) - 1/1000"
    bad["point_triangle_side"] = "2*sqrt(3) - 1/1000"
    # (b) move two points together
    bad2 = json.loads(json.dumps(good))
    bad2["coordinates"][3] = ["sqrt(3)", "1 + 1/1000"]
    for name, c in (("shrunk triangle", bad), ("overlapping pair", bad2)):
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(c, f)
        f.close()
        r2 = Report()
        try:
            check_cert(f.name, r2, verbose=False)
        except Exception as e:
            print(f"  {name}: raised {e}")
        rejected = len(r2.fail) > 0
        rep.ck(rejected, f"negative control '{name}' is rejected")
        print(f"  {name}: rejected={rejected}  ({len(r2.fail)} failing checks)")
        os.unlink(f.name)

    print(f"\n{rep.n} checks, {len(rep.fail)} failures")
    for f in rep.fail:
        print("  FAILED:", f)
    return 1 if rep.fail else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    rep = Report()
    for p in sys.argv[1:]:
        check_cert(p, rep)
    print(f"\n{rep.n} checks, {len(rep.fail)} failures")
    for f in rep.fail:
        print("  FAILED:", f)
    sys.exit(1 if rep.fail else 0)
