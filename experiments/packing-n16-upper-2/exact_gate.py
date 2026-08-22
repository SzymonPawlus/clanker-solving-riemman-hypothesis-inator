"""Exact feasibility checker for point-formulation certificates (problem RULES.md section 2).

Pure-integer arithmetic via fractions.Fraction — no floats anywhere in a decision.

Checks, for a certificate with rational coordinates and side d given by "p/q + 2*sqrt(3)":
  1. all C(n,2) pairwise squared distances >= 4              (separation 2, non-strict);
  2. containment in the CLOSED triangle A=(0,0), B=(d,0), C=(d/2, d*sqrt3/2):
        y >= 0;   sqrt3*x - y >= 0;   sqrt3*(d - x) - y >= 0,
     decided exactly via  (x >= 0 and 3*x^2 >= y^2)  etc., valid since y >= 0 is checked first;
  3. tightness report: the exact minimal enclosing d for these points with this fixed placement
     is d_min = max_i (x_i + y_i/sqrt3), an element of Q(sqrt3); the gap d - d_min is reported
     and its sign decided exactly in Q(sqrt3).

Also runs two negative controls (must both be REJECTED, else the gate itself is broken):
  A. one coordinate moved so one pairwise distance falls below 2 by ~1e-12;
  B. one boundary point pushed outside the triangle by ~1e-12.

Usage: python3 exact_gate.py out/n16-certificate.json
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction


def parse_side(expr: str) -> Fraction:
    """Accept exactly the form 'p/q + 2*sqrt(3)' and return d = p/q."""
    head, tail = expr.split("+")
    if tail.strip() != "2*sqrt(3)":
        raise ValueError(f"side_length not in the required form: {expr!r}")
    p, q = head.strip().split("/")
    return Fraction(int(p), int(q))


def sqrt3_sign(r: Fraction, t: Fraction) -> int:
    """Exact sign of r + t*sqrt(3) for rationals r, t."""
    if t == 0:
        return (r > 0) - (r < 0)
    if r == 0:
        return (t > 0) - (t < 0)
    if r > 0 and t > 0:
        return 1
    if r < 0 and t < 0:
        return -1
    # opposite signs: sign(r + t*sqrt3) = sign(r^2 - 3 t^2) * sign(r)
    disc = r * r - 3 * t * t
    s = (disc > 0) - (disc < 0)
    return s * ((r > 0) - (r < 0))


def check(points: list[tuple[Fraction, Fraction]], d: Fraction) -> dict:
    n = len(points)
    failures = []
    min_sq = None
    for i in range(n):
        for j in range(i + 1, n):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            sq = dx * dx + dy * dy
            if min_sq is None or sq < min_sq:
                min_sq = sq
            if sq < 4:
                failures.append(f"pair ({i},{j}): squared distance {sq} < 4")
    for i, (x, y) in enumerate(points):
        if y < 0:
            failures.append(f"point {i}: y = {y} < 0")
            continue
        if x < 0 or 3 * x * x < y * y:
            failures.append(f"point {i}: left of edge AC (sqrt3*x < y)")
        if d - x < 0 or 3 * (d - x) * (d - x) < y * y:
            failures.append(f"point {i}: right of edge BC (sqrt3*(d-x) < y)")
    # exact minimal enclosing d for this fixed placement: d_min = max_i (x_i + y_i/sqrt3);
    # comparison of x_i + y_i*sqrt3/3 terms done exactly in Q(sqrt3).
    best = None  # (r, t) meaning r + t*sqrt3
    for (x, y) in points:
        cand = (x, y / 3)
        if best is None or sqrt3_sign(cand[0] - best[0], cand[1] - best[1]) > 0:
            best = cand
    gap_sign = sqrt3_sign(d - best[0], -best[1])  # sign of d - d_min
    return {
        "feasible": not failures,
        "failures": failures,
        "min_squared_distance": str(min_sq),
        "min_sq_minus_4_float": float(min_sq - 4),
        "d": str(d),
        "d_min_exact": f"{best[0]} + ({best[1]})*sqrt(3)",
        "tight": gap_sign == 0,
        "d_minus_dmin_sign": gap_sign,
        "d_minus_dmin_float": float(d - best[0]) - float(best[1]) * 3 ** 0.5,
    }


def main(path: str) -> None:
    with open(path) as fh:
        cert = json.load(fh)
    if cert.get("coordinate_type") != "rational":
        raise SystemExit("this gate only handles coordinate_type = rational")
    d = parse_side(cert["side_length"])
    pts = []
    for xs, ys in cert["coordinates"]:
        px, qx = xs.split("/"); py, qy = ys.split("/")
        pts.append((Fraction(int(px), int(qx)), Fraction(int(py), int(qy))))
    if len(pts) != cert["n"]:
        raise SystemExit("n mismatch")

    rep = check(pts, d)
    print("== certificate ==")
    print(json.dumps(rep, indent=1))

    # negative control A: shrink the first contact pair below distance 2 by ~1e-12
    bad = [list(p) for p in pts]
    # move point 0 toward point of its nearest neighbour
    import itertools
    nn = min(((bad[0][0] - p[0]) ** 2 + (bad[0][1] - p[1]) ** 2, k)
             for k, p in enumerate(bad) if k != 0)[1]
    dx = bad[nn][0] - bad[0][0]
    dy = bad[nn][1] - bad[0][1]
    # squared distance currently >= 4; pull point 0 along (dx,dy) by rational lambda ~ 1e-12
    lam = Fraction(1, 10 ** 12) / 2
    bad[0][0] += dx * lam
    bad[0][1] += dy * lam
    repA = check([tuple(p) for p in bad], d)
    print("== negative control A (overlap ~1e-12): feasible =", repA["feasible"],
          "(must be False)")

    # negative control B: push a bottom-edge point below y = 0 by 1e-12
    bad = [list(p) for p in pts]
    kmin = min(range(len(bad)), key=lambda k: bad[k][1])
    bad[kmin][1] -= Fraction(1, 10 ** 12) + bad[kmin][1]  # y := -1e-12
    repB = check([tuple(p) for p in bad], d)
    print("== negative control B (outside by 1e-12): feasible =", repB["feasible"],
          "(must be False)")

    ok = rep["feasible"] and not repA["feasible"] and not repB["feasible"]
    print("GATE:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1])
