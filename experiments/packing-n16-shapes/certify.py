"""Turn a drive.py float configuration into an EXACT rational certificate and check it.

The certificate is 15 convex polygons with exact rational vertices in the triangular
basis.  Nothing about the triangulation is trusted: coverage is verified DIRECTLY by
exact rational polygon difference (T_a minus the pieces must be empty), which is the
only sound check when pieces overlap.

usage:  certify.py <config.json> [denominator ...]
"""
import sys, os, json, math
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom

def classify(V, a, tol):
    cls = []
    for (u, v) in V:
        on = []
        if abs(u) < tol: on.append(0)
        if abs(v) < tol: on.append(1)
        if abs(u + v - a) < tol: on.append(2)
        cls.append(on)
    return cls


def snap(V, a_f, Q, tol=1e-7):
    """Round to denominator Q, snapping boundary vertices exactly onto their side."""
    A = F(round(a_f * Q), Q)
    cls = classify(V, a_f, tol * max(1.0, a_f))
    out = []
    for (u, v), on in zip(V, cls):
        ru = F(round(u * Q), Q); rv = F(round(v * Q), Q)
        if 0 in on: ru = F(0)
        if 1 in on: rv = F(0)
        if 2 in on: rv = A - ru
        out.append((ru, rv))
    return A, out


def certify(cfg, Q):
    a_f = cfg["a"]
    A, V = snap(cfg["V"], a_f, Q)
    grp = cfg["grp"]; tris = cfg["tris"]
    ng = max(grp) + 1
    gv = [set() for _ in range(ng)]
    for t, g in zip(tris, grp):
        gv[g].update(t)
    pieces = [geom.hull([V[k] for k in sorted(s)]) for s in gv]
    rep = {}
    rep["n_pieces"] = len(pieces)
    rep["all_convex"] = all(geom.is_convex_ccw(P) for P in pieces)
    rep["inside_T"] = all(p[0] >= 0 and p[1] >= 0 and p[0] + p[1] <= A
                          for P in pieces for p in P)
    S = max(geom.diam2(P) for P in pieces)
    rep["max_sq_diam"] = S
    rem = geom.cover_remainder(geom.tri(A), pieces)
    rep["uncovered_pieces"] = len(rem)
    rep["uncovered_uv_area"] = sum(geom.area_uv(r) for r in rem)
    rep["a"] = A
    rep["pieces"] = pieces
    return rep


def main():
    cfg = json.load(open(sys.argv[1]))
    Qs = [int(x) for x in sys.argv[2:]] or [10**5, 10**6, 10**7]
    best = None
    for Q in Qs:
        rep = certify(cfg, Q)
        S = rep["max_sq_diam"]
        astar = float(rep["a"]) / math.sqrt(float(S))
        good = (rep["all_convex"] and rep["inside_T"] and rep["uncovered_pieces"] == 0
                and S < 1 * S.denominator / S.denominator)   # placeholder, see below
        good = (rep["all_convex"] and rep["inside_T"] and rep["uncovered_pieces"] == 0)
        print("Q=%-10d convex %s  inside %s  uncovered %d (uv-area %s)  "
              "max_sq_diam=%.12f  a* = %.9f  %s"
              % (Q, rep["all_convex"], rep["inside_T"], rep["uncovered_pieces"],
                 rep["uncovered_uv_area"], float(S), astar, "OK" if good else "REJECT"))
        if good and (best is None or astar > best[0]):
            best = (astar, Q, rep)
    if best is None:
        print("no admissible certificate"); return
    astar, Q, rep = best
    S = rep["max_sq_diam"]
    print()
    print("BEST  Q = %d" % Q)
    print("  a           = %s" % rep["a"])
    print("  max_sq_diam = %s" % S)
    print("  a* = a / sqrt(max_sq_diam) = %.12f" % astar)
    # a rational lower bound for a*, safe to quote
    lo = F(int(astar * 10**9) - 1, 10**9)
    assert lo * lo * S <= rep["a"] * rep["a"], "rational lower bound check"
    print("  certified rational lower bound  a_16 >= %s = %.12f" % (lo, float(lo)))
    out = os.path.splitext(sys.argv[1])[0] + "_cert.json"
    json.dump({"a": [str(rep["a"].numerator), str(rep["a"].denominator)],
               "max_sq_diam": str(S),
               "a_star_rational_lower_bound": str(lo),
               "pieces_uv": [[[str(p[0]), str(p[1])] for p in P] for P in rep["pieces"]]},
              open(out, "w"), indent=1)
    print("  written %s" % out)

main()
