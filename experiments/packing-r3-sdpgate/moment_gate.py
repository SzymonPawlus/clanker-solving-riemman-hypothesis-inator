#!/usr/bin/env python3
"""Dense Lasserre/moment relaxation of the equilateral-triangle point-packing
problem, measured against KNOWN optima (round-3 proposal X, "the strength gate").

STATUS OF EVERYTHING THIS PRODUCES: `numerical`.  An SDP solved in floating point
is a HYPOTHESIS about a bound, never a bound (problem RULES.md).  Nothing here is
rationally rounded and nothing here is asserted as a proof of anything.

Formulation (approach C of ../../problems/.../attacks/candidate-approaches, verbatim):

    maximise  t
    s.t.      ||p_i - p_j||^2 - t >= 0        for all i < j
              p_i in the closed unit equilateral triangle T_1
              0 <= t <= TCAP

with A=(0,0), B=(1,0), C=(1/2, sqrt3/2) -- the repo's fixed triangle placement,
scaled to side 1.  `t` is a decision variable of the polynomial program, so the
program has N = 2n + 1 variables.

Scaling.  Write f(n) = max over configurations in T_1 of the minimum squared
pairwise distance.  A packing at pairwise distance >= 2 fits in T_d iff
d^2 f(n) >= 4, so the exact relation is

    d(n) = 2 / sqrt(f(n)).

A level-L moment relaxation returns an UPPER bound f_L >= f(n), hence a LOWER
bound d_L = 2/sqrt(f_L) <= d(n).  Comparing d_L against the published exact d(n)
is the slack measurement.

t <= 1 is a valid constraint for every n >= 2 (the diameter of T_1 is 1), so it
is legitimate to include; --tcap lets you loosen it to check whether the
relaxation is doing anything beyond returning that trivial cap.

Run:  python3 moment_gate.py --selftest
      python3 moment_gate.py --n 5 --level 2
      python3 moment_gate.py --sweep
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
import time

import numpy as np
import scipy.sparse as sp
import cvxpy as cp

SQRT3 = math.sqrt(3.0)

# published exact optima, point formulation d(n) = s(n) - 2*sqrt(3)
# (problems/circle-packing-equilateral-triangle/README.md, status `cited` there)
KNOWN_D = {
    2: 2.0,
    3: 2.0,
    4: 2 * SQRT3,
    5: 4.0,
    6: 4.0,
    7: 2 + 2 * SQRT3,
    8: 2 + 2 * math.sqrt(33) / 3,
    9: 6.0,
    10: 6.0,
    11: 4 + 4 * math.sqrt(6) / 3,
    12: 4 + 2 * SQRT3,
    13: 4 + 2 * math.sqrt(6) / 3 + 4 * SQRT3 / 3,
    14: 8.0,
    15: 8.0,
}
KNOWN_D_EXPR = {  # LaTeX, for the write-up table
    2: r"2", 3: r"2", 4: r"2\sqrt3", 5: r"4", 6: r"4", 7: r"2+2\sqrt3",
    8: r"2+\tfrac{2\sqrt{33}}{3}", 9: r"6", 10: r"6",
    11: r"4+\tfrac{4\sqrt6}{3}", 12: r"4+2\sqrt3",
    13: r"4+\tfrac{2\sqrt6}{3}+\tfrac{4\sqrt3}{3}", 14: r"8", 15: r"8",
}


# ------------------------------------------------------------ polynomial algebra
# A monomial is a sorted tuple of variable indices (with repetition).
def monomials_upto(nvars, deg):
    out = []
    for k in range(deg + 1):
        out.extend(itertools.combinations_with_replacement(range(nvars), k))
    return out


def mmul(a, b):
    return tuple(sorted(a + b))


def poly_mul(p, q):
    r = {}
    for ma, ca in p.items():
        for mb, cb in q.items():
            m = mmul(ma, mb)
            r[m] = r.get(m, 0.0) + ca * cb
    return {m: c for m, c in r.items() if abs(c) > 1e-14}


def poly_add(*ps):
    r = {}
    for p in ps:
        for m, c in p.items():
            r[m] = r.get(m, 0.0) + c
    return {m: c for m, c in r.items() if abs(c) > 1e-14}


def poly_scale(p, s):
    return {m: c * s for m, c in p.items()}


# ------------------------------------------------------------------- the program
def build_problem(n, tcap=1.0):
    """Return (nvars, objective_poly, list_of_constraint_polys, labels)."""
    nv = 2 * n + 1
    T = 2 * n  # index of the variable t

    def X(i):
        return {(i,): 1.0}

    def Y(i):
        return {(n + i,): 1.0}

    one = {(): 1.0}
    t = {(T,): 1.0}

    cons, labels = [], []
    for i, j in itertools.combinations(range(n), 2):
        dx = poly_add(X(i), poly_scale(X(j), -1.0))
        dy = poly_add(Y(i), poly_scale(Y(j), -1.0))
        g = poly_add(poly_mul(dx, dx), poly_mul(dy, dy), poly_scale(t, -1.0))
        cons.append(g)
        labels.append(f"sep({i},{j})")
    for i in range(n):
        # y_i >= 0
        cons.append(Y(i)); labels.append(f"edgeAB({i})")
        # sqrt3 x_i - y_i >= 0        (edge AC)
        cons.append(poly_add(poly_scale(X(i), SQRT3), poly_scale(Y(i), -1.0)))
        labels.append(f"edgeAC({i})")
        # sqrt3 (1 - x_i) - y_i >= 0  (edge BC)
        cons.append(poly_add({(): SQRT3}, poly_scale(X(i), -SQRT3),
                             poly_scale(Y(i), -1.0)))
        labels.append(f"edgeBC({i})")
    cons.append(t); labels.append("t>=0")
    cons.append(poly_add({(): float(tcap)}, poly_scale(t, -1.0)))
    labels.append(f"t<={tcap}")
    return nv, t, cons, labels


def poly_degree(p):
    return max(len(m) for m in p)


# ------------------------------------------------------------------- relaxation
def build_sdp(nv, obj, cons, level, verbose=False):
    """Assemble the level-`level` dense moment relaxation as a cvxpy problem."""
    D = 2 * level
    moms = monomials_upto(nv, D)
    midx = {m: k for k, m in enumerate(moms)}
    M = len(moms)
    yv = cp.Variable(M)

    def block(basis, poly):
        """Sparse matrix A with reshape(A @ y, (m,m)) = localizing matrix."""
        m = len(basis)
        rows, cols, vals = [], [], []
        for a_i, a in enumerate(basis):
            for b_i, b in enumerate(basis):
                r = a_i * m + b_i
                ab = mmul(a, b)
                for mon, c in poly.items():
                    rows.append(r)
                    cols.append(midx[mmul(ab, mon)])
                    vals.append(c)
        A = sp.csr_matrix((vals, (rows, cols)), shape=(m * m, M))
        return cp.reshape(A @ yv, (m, m), order="C"), m

    constraints = [yv[midx[()]] == 1.0]
    basisL = monomials_upto(nv, level)
    Mmat, mm = block(basisL, {(): 1.0})
    constraints.append(Mmat >> 0)
    sizes = [mm]
    for g in cons:
        dg = poly_degree(g)
        ord_g = level - (dg + 1) // 2
        assert ord_g >= 0
        bg = monomials_upto(nv, ord_g)
        Lg, sz = block(bg, g)
        constraints.append(Lg >> 0)
        sizes.append(sz)

    objective = cp.Maximize(sum(c * yv[midx[m]] for m, c in obj.items()))
    prob = cp.Problem(objective, constraints)
    if verbose:
        print(f"    moment vars M = {M:,}; PSD blocks: 1 of {sizes[0]}, "
              f"{len(sizes)-1} of {sizes[1]}", flush=True)
    return prob, M, sizes


def solve(n, level, tcap=1.0, solver=None, verbose=True, max_seconds=600, eps=1e-7):
    nv, obj, cons, _ = build_problem(n, tcap)
    t0 = time.time()
    prob, M, sizes = build_sdp(nv, obj, cons, level, verbose)
    build_s = time.time() - t0
    kw = {}
    if solver is None:
        solver = "SCS" if sizes[0] > 200 else "CLARABEL"
    if solver == "SCS":
        kw = dict(eps=eps, max_iters=200000, time_limit_secs=max_seconds)
    t0 = time.time()
    try:
        prob.solve(solver=solver, verbose=False, **kw)
    except Exception as e:  # noqa: BLE001
        return dict(n=n, level=level, status=f"solver-error: {e}",
                    build_s=build_s, solve_s=time.time() - t0, M=M, sizes=sizes)
    solve_s = time.time() - t0
    return dict(n=n, level=level, status=prob.status, value=prob.value,
                build_s=build_s, solve_s=solve_s, M=M, sizes=sizes,
                solver=solver, tcap=tcap)


# ------------------------------------------------------------------- self-tests
def selftest():
    """Validate the machinery on instances with answers known in closed form."""
    ok = True

    # (1) textbook 1-D POP: max x s.t. 1 - x^2 >= 0  ->  1
    nv, obj, cons = 1, {(0,): 1.0}, [{(): 1.0, (0, 0): -1.0}]
    for L in (1, 2):
        prob, _, _ = build_sdp(nv, obj, cons, L)
        prob.solve(solver="CLARABEL")
        print(f"  [selftest] max x s.t. 1-x^2>=0, level {L}: {prob.value:.9f} "
              f"(exact 1)")
        ok &= abs(prob.value - 1.0) < 1e-6

    # (2) max x1*x2 s.t. x1,x2 in [0,1], x1+x2<=1  -> 1/4
    nv = 2
    obj = {(0, 1): 1.0}
    cons = [{(0,): 1.0}, {(1,): 1.0},
            {(): 1.0, (0,): -1.0}, {(): 1.0, (1,): -1.0},
            {(): 1.0, (0,): -1.0, (1,): -1.0}]
    prob, _, _ = build_sdp(nv, obj, cons, 2)
    prob.solve(solver="CLARABEL")
    print(f"  [selftest] max x1*x2 on the simplex, level 2: {prob.value:.9f} "
          f"(exact 0.25)")
    ok &= abs(prob.value - 0.25) < 1e-6

    # (3) the packing program itself at n = 2: f(2) = 1 exactly (the triangle's
    #     diameter is its side).  Run it with a deliberately LOOSE cap t <= 4 so
    #     the cap cannot supply the answer.
    r = solve(2, 2, tcap=4.0, verbose=False)
    print(f"  [selftest] packing n=2, level 2, loose cap t<=4: "
          f"f_2 = {r['value']:.9f} (exact f(2) = 1)")
    ok &= abs(r["value"] - 1.0) < 1e-5

    # (4) n = 3 with a loose cap: f(3) = 1 exactly as well.
    r = solve(3, 2, tcap=4.0, verbose=False)
    print(f"  [selftest] packing n=3, level 2, loose cap t<=4: "
          f"f_2 = {r['value']:.9f} (exact f(3) = 1)")
    ok &= abs(r["value"] - 1.0) < 1e-4

    print("  [selftest]", "PASS" if ok else "FAIL")
    return ok


# --------------------------------------------------------------------- reporting
def row(res):
    n = res["n"]
    if res.get("value") is None or res["status"] not in ("optimal",
                                                         "optimal_inaccurate"):
        return dict(n=n, level=res["level"], status=res["status"])
    f_ub = res["value"]
    d_lb = 2.0 / math.sqrt(f_ub) if f_ub > 0 else float("inf")
    d_true = KNOWN_D[n]
    return dict(n=n, level=res["level"], status=res["status"],
                f_relax=float(f_ub), f_true=float(4.0 / d_true ** 2),
                d_true=float(d_true), d_relax=float(d_lb),
                abs_gap=float(d_true - d_lb), rel_gap=float((d_true - d_lb) / d_true),
                cap_active=bool(abs(f_ub - res["tcap"]) < 1e-6),
                solve_s=float(res["solve_s"]), M=int(res["M"]), block=int(res["sizes"][0]))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int)
    ap.add_argument("--level", type=int, default=2)
    ap.add_argument("--tcap", type=float, default=1.0)
    ap.add_argument("--solver", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--ns", type=str, default="4,5,6,7,8,10,12")
    ap.add_argument("--out", type=str, default="results.json")
    ap.add_argument("--max-seconds", type=int, default=600)
    ap.add_argument("--eps", type=float, default=1e-7)
    args = ap.parse_args()

    if args.selftest:
        sys.exit(0 if selftest() else 1)

    if args.sweep:
        ns = [int(v) for v in args.ns.split(",")]
        rows = []
        for n in ns:
            print(f"[n={n}] level {args.level}, cap t<={args.tcap}", flush=True)
            res = solve(n, args.level, args.tcap, args.solver,
                        max_seconds=args.max_seconds, eps=args.eps)
            r = row(res)
            rows.append(r)
            print("   ", json.dumps(r), flush=True)
            with open(args.out, "w") as fh:
                json.dump(rows, fh, indent=2)
        print("\n" + fmt_table(rows))
        return

    res = solve(args.n, args.level, args.tcap, args.solver,
                max_seconds=args.max_seconds, eps=args.eps)
    print(json.dumps(row(res), indent=2))


def fmt_table(rows):
    hdr = (f"| {'n':>3} | {'known d(n)':>12} | {'level-2 bound':>13} | "
           f"{'abs gap':>9} | {'rel gap':>8} | {'cap?':>4} |")
    sep = "|" + "|".join(["-" * (len(c) + 2) for c in
                          ["  n", "  known d(n) ", " level-2 bound", "  abs gap",
                           " rel gap", " cap"]]) + "|"
    out = [hdr, sep]
    for r in rows:
        if "d_relax" not in r:
            out.append(f"| {r['n']:>3} | {'':>12} | {r['status']:>13} | "
                       f"{'':>9} | {'':>8} | {'':>4} |")
            continue
        out.append(f"| {r['n']:>3} | {r['d_true']:>12.6f} | {r['d_relax']:>13.6f} | "
                   f"{r['abs_gap']:>9.4f} | {100*r['rel_gap']:>7.2f}% | "
                   f"{'yes' if r['cap_active'] else 'no':>4} |")
    return "\n".join(out)


if __name__ == "__main__":
    main()
