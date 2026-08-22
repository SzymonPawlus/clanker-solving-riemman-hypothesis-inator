"""Occupancy exhaustion for circle packing in an equilateral triangle.

Worker O2, claude, 2026-08-22, issue #97.  Attack write-up:
problems/circle-packing-equilateral-triangle/attacks/n16-occupancy/.

Normalisation (separation 1): T_a = {(u,v): u>=0, v>=0, u+v<=a} in the lattice
basis e1=(1,0), e2=(1/2, sqrt3/2), where |u*e1+v*e2|^2 = u^2+u*v+v^2 is rational.

Mechanism: cover T_a by N >= n convex pieces of diameter STRICTLY < 1 (exact).
n points at pairwise distance >= 1 then occupy n distinct pieces.  Enumerate the
C(N,n) occupancy patterns; refute each by
  (a) pair pruning     : two occupied pieces with exact max mutual distance < 1;
  (b) capacity pruning : k occupied cells inside an equilateral triangle of side
                         s with s < a_k (cited, k <= CAP_MAX_INDEX only);
  (c) refinement       : split an occupied cell in two closed halves that cover
                         it, branch on which half holds the point, re-prune.
All patterns refuted  =>  a_n >= a.

SOUNDNESS RULES USED THROUGHOUT
 - every REFUTATION is decided by exact Fraction arithmetic;
 - floats appear only as pre-filters and branching heuristics: a float may stop
   us from *attempting* a prune (losing power, never soundness) and may choose
   *which* cell to split, but never decides a reported inequality;
 - CIRCULARITY GUARD: the capacity table refuses every index above
   CAP_MAX_INDEX; runs at n = 16 set CAP_MAX_INDEX = 15, controls at n = m set
   m - 1.  No value of a_16 / d(16) / s(16), and no property of any 16-point
   packing, is an input anywhere in this file.
"""

from fractions import Fraction as F
import json
import time

# ----------------------------------------------------------------------------
# exact metric and polygon primitives (lattice coordinates, Fractions)
# ----------------------------------------------------------------------------

def Q2(du, dv):
    """Exact squared Euclidean length of du*e1 + dv*e2."""
    return du * du + du * dv + dv * dv


def q2f(du, dv):
    return du * du + du * dv + dv * dv


def diam2_exact(verts):
    m = len(verts)
    best = F(0)
    for i in range(m):
        ui, vi = verts[i]
        for j in range(i + 1, m):
            d = Q2(ui - verts[j][0], vi - verts[j][1])
            if d > best:
                best = d
    return best


def diam2_float(fverts):
    best = 0.0
    m = len(fverts)
    for i in range(m):
        ui, vi = fverts[i]
        for j in range(i + 1, m):
            d = q2f(ui - fverts[j][0], vi - fverts[j][1])
            if d > best:
                best = d
    return best


def maxdist2_exact(va, vb):
    best = F(0)
    for ua, wa in va:
        for ub, wb in vb:
            d = Q2(ua - ub, wa - wb)
            if d > best:
                best = d
    return best


def maxdist2_float(fa, fb):
    best = 0.0
    for ua, wa in fa:
        for ub, wb in fb:
            d = q2f(ua - ub, wa - wb)
            if d > best:
                best = d
    return best


def area2(verts):
    """Twice the (chart) shoelace area, exact; sign per orientation."""
    s = F(0)
    m = len(verts)
    for i in range(m):
        u1, v1 = verts[i]
        u2, v2 = verts[(i + 1) % m]
        s += u1 * v2 - u2 * v1
    return s


def clip(verts, cu, cv, rhs):
    """Exact Sutherland-Hodgman: keep {cu*u + cv*v <= rhs}. Returns vertex list
    (possibly empty / degenerate). Closed halfplane, exact intersections."""
    if not verts:
        return []
    out = []
    m = len(verts)
    vals = [cu * u + cv * v - rhs for (u, v) in verts]
    for i in range(m):
        j = (i + 1) % m
        pi, pj = verts[i], verts[j]
        fi, fj = vals[i], vals[j]
        if fi <= 0:
            out.append(pi)
        if (fi < 0 < fj) or (fj < 0 < fi):
            tden = fi - fj
            tnum = fi
            t = tnum / tden          # in (0,1)
            out.append((pi[0] + t * (pj[0] - pi[0]),
                        pi[1] + t * (pj[1] - pi[1])))
    # dedup consecutive
    ded = []
    for p in out:
        if not ded or p != ded[-1]:
            ded.append(p)
    if len(ded) > 1 and ded[0] == ded[-1]:
        ded.pop()
    return ded


def hull(points):
    """Exact convex hull (monotone chain), returns CCW vertex list."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def is_convex_ccw(verts):
    m = len(verts)
    if m < 3:
        return True
    for i in range(m):
        o, a, b = verts[i], verts[(i + 1) % m], verts[(i + 2) % m]
        cr = (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        if cr < 0:
            return False
    return True


def fverts_of(verts):
    return [(float(u), float(v)) for (u, v) in verts]


# ----------------------------------------------------------------------------
# capacity table -- cited a_k only, hard circularity guard
# ----------------------------------------------------------------------------
# Entry (k, p, q, m) encodes a_k = p + q*sqrt(m) (p, q rational, q >= 0, m int)
# and licences: enclosing triangle side s < a_k  =>  at most k-1 points.
# Sources: problem README table (cited).  a_13 is deliberately OMITTED (its
# closed form was not re-derived here); the ladder skips from a_12 to a_14,
# which only loses pruning power, never soundness.
_A_TABLE = [
    (2,  F(1), F(0),      1),   # a_2  = 1
    (4,  F(0), F(1),      3),   # a_4  = sqrt(3)
    (5,  F(2), F(0),      1),   # a_5  = 2
    (7,  F(1), F(1),      3),   # a_7  = 1 + sqrt(3)
    (8,  F(1), F(1, 3),  33),   # a_8  = 1 + sqrt(33)/3
    (9,  F(3), F(0),      1),   # a_9  = 3
    (11, F(2), F(2, 3),   6),   # a_11 = 2 + 2*sqrt(6)/3
    (12, F(2), F(1),      3),   # a_12 = 2 + sqrt(3)
    (14, F(4), F(0),      1),   # a_14 = 4
]
_A_FLOAT = [(k, float(p) + float(q) * (m ** 0.5)) for (k, p, q, m) in _A_TABLE]

# The named guard.  Runs at n points must set cap_max_index = n - 1, so that no
# a_k with k >= n (in particular nothing about the open case n = 16 when
# n = 16) can enter the argument.
CAP_MAX_INDEX_FOR = lambda n: n - 1


def lt_radical(s, p, q, m):
    """Exact: is rational s < p + q*sqrt(m) (q >= 0)?"""
    d = s - p
    if d < 0:
        return True
    return d * d < q * q * m


def cap_of_exact(s, cap_max_index):
    """Largest point count certified for enclosing side s (exact rational s),
    or None.  Uses only a_k with k <= cap_max_index."""
    for (k, p, q, m) in _A_TABLE:
        if k > cap_max_index:
            break
        if lt_radical(s, p, q, m):
            return k - 1
    return None


def cap_of_float(s, cap_max_index):
    for (k, val) in _A_FLOAT:
        if k > cap_max_index:
            break
        if s < val - 1e-9:
            return k - 1
    return None


# ----------------------------------------------------------------------------
# cover construction: clipped Voronoi hexagons of a triangular lattice
# ----------------------------------------------------------------------------

_HEXDIRS = [(1, 1), (-1, 2), (-2, 1), (-1, -1), (1, -2), (2, -1)]  # CCW


def hex_cover(a, t, off_u, off_v):
    """Clipped-Voronoi-hexagon cover of T_a.  All Fractions.  The Voronoi cells
    of the lattice {t*(i,j)+off} tile the plane, so their clips cover T_a; the
    verifier below re-checks that exactly and from first principles."""
    pieces = []
    third = t / 3
    lo_i = int(float((F(-1) - off_u) / t)) - 2
    hi_i = int(float((a + 1 - off_u) / t)) + 2
    lo_j = int(float((F(-1) - off_v) / t)) - 2
    hi_j = int(float((a + 1 - off_v) / t)) + 2
    for i in range(lo_i, hi_i + 1):
        for j in range(lo_j, hi_j + 1):
            cu = t * i + off_u
            cv = t * j + off_v
            verts = [(cu + third * du, cv + third * dv) for (du, dv) in _HEXDIRS]
            verts = clip(verts, F(-1), F(0), F(0))   # u >= 0
            verts = clip(verts, F(0), F(-1), F(0))   # v >= 0
            verts = clip(verts, F(1), F(1), a)       # u+v <= a
            if len(verts) >= 3 and area2(verts) != 0:
                pieces.append(verts)
    return pieces


def subdiv_cover(a, L):
    """The 4^L congruent subtriangles of T_a (up/down cells), exact."""
    n = 2 ** L
    h = a / n
    pieces = []
    for j in range(n):
        for i in range(n - j):
            u0, v0 = h * i, h * j
            pieces.append([(u0, v0), (u0 + h, v0), (u0, v0 + h)])
            if i + j < n - 1:
                pieces.append([(u0 + h, v0), (u0 + h, v0 + h), (u0, v0 + h)])
    return pieces


def merge_pass(pieces, verbose=False):
    """Greedily replace two pieces by their convex hull whenever the hull has
    exact squared diameter < 1.  The hull contains the union, so the result is
    still a cover; convexity and diameter are re-verified exactly later."""
    pieces = [hull(p) for p in pieces]
    changed = True
    while changed:
        changed = False
        m = len(pieces)
        best = None
        for i in range(m):
            fi = fverts_of(pieces[i])
            for j in range(i + 1, m):
                fj = fverts_of(pieces[j])
                if maxdist2_float(fi, fj) < 1.0 + 1e-9:
                    h = hull(pieces[i] + pieces[j])
                    if diam2_exact(h) < 1:          # exact gate
                        d = diam2_float(fverts_of(h))
                        if best is None or d < best[0]:
                            best = (d, i, j, h)
        if best is not None:
            _, i, j, h = best
            pieces = [p for k, p in enumerate(pieces) if k not in (i, j)] + [h]
            changed = True
            if verbose:
                print("  merged -> %d pieces" % len(pieces))
    return pieces


# ----------------------------------------------------------------------------
# exact cover verification (written from the problem statement; residual
# subtraction, no area identity, tolerates overlapping pieces)
# ----------------------------------------------------------------------------

def edges_of(verts):
    """Halfplane list (cu, cv, rhs) with piece = {cu*u+cv*v <= rhs} for a CCW
    convex polygon."""
    out = []
    m = len(verts)
    for i in range(m):
        (u1, v1), (u2, v2) = verts[i], verts[(i + 1) % m]
        cu, cv = v2 - v1, u1 - u2
        rhs = cu * u1 + cv * v1
        # for a CCW polygon the interior satisfies cu*u + cv*v <= rhs
        out.append((cu, cv, rhs))
    return out


def verify_cover(a, pieces, verbose=False):
    """Exact: (1) each piece convex with squared diameter STRICTLY < 1;
    (2) union of pieces covers T_a (residual subtraction).  Returns
    (ok, max_diam2)."""
    worst = F(0)
    for k, p in enumerate(pieces):
        if area2(p) < 0:
            p = list(reversed(p))
            pieces[k] = p
        if not is_convex_ccw(p):
            raise AssertionError("piece %d not convex CCW" % k)
        d = diam2_exact(p)
        if d > worst:
            worst = d
        if not (d < 1):
            if verbose:
                print("  piece %d has squared diameter %s >= 1" % (k, d))
            return False, worst
    tri = [(F(0), F(0)), (a, F(0)), (F(0), a)]
    residual = [tri]
    peak = 1
    for p in pieces:
        hp = edges_of(p)
        new_res = []
        for R in residual:
            cur = R
            for (cu, cv, rhs) in hp:
                outside = clip(cur, -cu, -cv, -rhs)   # >= side of the edge
                if len(outside) >= 3 and area2(outside) != 0:
                    new_res.append(outside)
                cur = clip(cur, cu, cv, rhs)
                if len(cur) < 3:
                    break
        residual = new_res
        peak = max(peak, len(residual))
    ok = len(residual) == 0
    if verbose:
        print("  cover verified: %s (peak residual %d), max diam2 = %s < 1: %s"
              % (ok, peak, float(worst), worst < 1))
    return ok, worst


# ----------------------------------------------------------------------------
# the occupancy engine
# ----------------------------------------------------------------------------

class Cell:
    __slots__ = ("pid", "verts", "fverts", "fdiam2")

    def __init__(self, pid, verts):
        self.pid = pid
        self.verts = verts
        self.fverts = fverts_of(verts)
        self.fdiam2 = diam2_float(self.fverts)


def pair_incompatible(ca, cb):
    """True (exact) iff max distance between the two cells is < 1, so they
    cannot hold two points at distance >= 1."""
    if maxdist2_float(ca.fverts, cb.fverts) >= 1.0 + 1e-9:
        return False
    return maxdist2_exact(ca.verts, cb.verts) < 1


_ORDERINGS = (
    lambda ag: ag[3],          # by max(u+v)  asc : corner-A clusters
    lambda ag: -ag[0],         # by min u    desc : corner-B clusters
    lambda ag: -ag[1],         # by min v    desc : corner-C clusters
    lambda ag: -ag[2],         # by min(u+v) desc : edge-BC clusters
    lambda ag: ag[4],          # by max u     asc
    lambda ag: ag[5],          # by max v     asc
)


def _aggf(c):
    us = [p[0] for p in c.fverts]
    vs = [p[1] for p in c.fverts]
    ss = [p[0] + p[1] for p in c.fverts]
    return (min(us), min(vs), min(ss), max(ss), max(us), max(vs))


def capacity_refute(cells, cap_max_index):
    """Look for a subset K of cells whose exact enclosing lattice-aligned
    equilateral triangle has side s with cap(s) < |K|.  Heuristic subset
    generation (sorted prefixes, float); every hit confirmed exactly.
    Returns list of cell indices or None."""
    m = len(cells)
    aggs = [_aggf(c) for c in cells]
    for key in _ORDERINGS:
        order = sorted(range(m), key=lambda i: key(aggs[i]))
        mnu = mnv = mns = 1e18
        mxs = mxu = mxv = -1e18
        for p, idx in enumerate(order, start=1):
            a = aggs[idx]
            mnu = min(mnu, a[0]); mnv = min(mnv, a[1]); mns = min(mns, a[2])
            mxs = max(mxs, a[3]); mxu = max(mxu, a[4]); mxv = max(mxv, a[5])
            if p < 2:
                continue
            side_up = mxs - mnu - mnv          # up-triangle enclosure
            side_dn = mxu + mxv - mns          # down-triangle enclosure
            for side in (side_up, side_dn):
                c = cap_of_float(side, cap_max_index)
                if c is not None and c < p:
                    sub = order[:p]
                    if _cap_confirm(cells, sub, cap_max_index):
                        return sub
    return None


def _cap_confirm(cells, sub, cap_max_index):
    """Exact confirmation of a capacity refutation on cell subset `sub`."""
    mnu = mnv = mns = None
    mxs = mxu = mxv = None
    for i in sub:
        for (u, v) in cells[i].verts:
            s = u + v
            mnu = u if mnu is None or u < mnu else mnu
            mnv = v if mnv is None or v < mnv else mnv
            mns = s if mns is None or s < mns else mns
            mxs = s if mxs is None or s > mxs else mxs
            mxu = u if mxu is None or u > mxu else mxu
            mxv = v if mxv is None or v > mxv else mxv
    p = len(sub)
    for side in (mxs - mnu - mnv, mxu + mxv - mns):
        if side < 0:
            side = F(0)
        c = cap_of_exact(side, cap_max_index)
        if c is not None and c < p:
            return True
    return False


def check_node(cells, cap_max_index, changed=None):
    """Return ('pair', i, j) / ('cap', sub) / None.  Exact refutations only."""
    m = len(cells)
    if changed is None:
        rng = [(i, j) for i in range(m) for j in range(i + 1, m)]
    else:
        rng = [(min(changed, j), max(changed, j))
               for j in range(m) if j != changed]
    for (i, j) in rng:
        if pair_incompatible(cells[i], cells[j]):
            return ("pair", i, j)
    sub = capacity_refute(cells, cap_max_index)
    if sub is not None:
        return ("cap", tuple(sorted(sub)))
    return None


def split_cell(cell):
    """Split into two closed halves that cover the cell, cutting the extent of
    the best of the three lattice functionals at (approximately) its midpoint.
    Cut choice is a float heuristic; the halves themselves are exact."""
    best = None
    for (cu, cv) in ((F(1), F(0)), (F(0), F(1)), (F(1), F(1))):
        vals = [cu * u + cv * v for (u, v) in cell.verts]
        lo, hi = min(vals), max(vals)
        if hi == lo:
            continue
        midf = (float(lo) + float(hi)) / 2.0
        mid = F(midf).limit_denominator(1 << 14)
        if not (lo < mid < hi):
            mid = (lo + hi) / 2
        c1 = clip(cell.verts, cu, cv, mid)
        c2 = clip(cell.verts, -cu, -cv, -mid)
        kids = [Cell(cell.pid, k) for k in (c1, c2) if k]
        w = max((k.fdiam2 for k in kids), default=0.0)
        if best is None or w < best[0]:
            best = (w, kids)
    return best[1] if best else [cell]


def refute_pattern(pieces_cells, cap_max_index, floor_diam2=1e-4,
                   node_cap=200000, time_cap=60.0):
    """BnB on one occupancy pattern.  pieces_cells: list of Cell (one per
    occupied piece; the point of piece i lies in cells[i]).
    Returns dict with status 'refuted' | 'survived' | 'budget'."""
    t0 = time.time()
    nodes = 0
    maxdepth = 0
    root = check_node(pieces_cells, cap_max_index)
    if root is not None:
        return {"status": "refuted", "nodes": 1, "why_root": root[0],
                "depth": 0}
    stack = [(pieces_cells, 0)]
    while stack:
        nodes += 1
        if nodes > node_cap or (nodes % 512 == 0 and time.time() - t0 > time_cap):
            return {"status": "budget", "nodes": nodes, "depth": maxdepth}
        cells, depth = stack.pop()
        maxdepth = max(maxdepth, depth)
        # pick the fattest cell
        bi, bd = -1, -1.0
        for i, c in enumerate(cells):
            if c.fdiam2 > bd:
                bd, bi = c.fdiam2, i
        if bd < floor_diam2:
            centers = [[sum(p[0] for p in c.fverts) / len(c.fverts),
                        sum(p[1] for p in c.fverts) / len(c.fverts)]
                       for c in cells]
            return {"status": "survived", "nodes": nodes, "depth": maxdepth,
                    "witness_centers_uv": centers}
        for kid in split_cell(cells[bi]):
            nc = list(cells)
            nc[bi] = kid
            if check_node(nc, cap_max_index, changed=bi) is None:
                stack.append((nc, depth + 1))
    return {"status": "refuted", "nodes": nodes, "depth": maxdepth}


def enumerate_patterns(pieces, npts):
    """All npts-subsets of pieces that survive pair pruning (i.e. cliques of
    the exact compatibility graph)."""
    N = len(pieces)
    cells = [Cell(i, p) for i, p in enumerate(pieces)]
    compat = [[False] * N for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            ok = not pair_incompatible(cells[i], cells[j])
            compat[i][j] = compat[j][i] = ok
    out = []

    def rec(start, chosen):
        if len(chosen) == npts:
            out.append(tuple(chosen))
            return
        if N - start < npts - len(chosen):
            return
        for j in range(start, N):
            if all(compat[i][j] for i in chosen):
                chosen.append(j)
                rec(j + 1, chosen)
                chosen.pop()

    rec(0, [])
    return out, cells


def run_occupancy(a, pieces, npts, cap_max_index, floor_diam2=1e-4,
                  node_cap=200000, time_cap_per_pattern=60.0,
                  time_cap_total=None, out_path=None, label=""):
    """Full pipeline on a verified cover.  Returns summary dict."""
    assert cap_max_index <= npts - 1, "CIRCULARITY GUARD: cap table may not " \
        "use a_k for k >= n"
    t0 = time.time()
    ok, worst = verify_cover(a, pieces, verbose=True)
    if not ok:
        return {"status": "cover-invalid", "a": str(a)}
    patterns, _ = enumerate_patterns(pieces, npts)
    print("  N=%d pieces, %d patterns survive pair pruning" %
          (len(pieces), len(patterns)))
    results = {"a": str(a), "a_float": float(a), "n": npts,
               "N_pieces": len(pieces), "cap_max_index": cap_max_index,
               "max_piece_diam2": float(worst), "label": label,
               "patterns_total": len(patterns), "patterns": []}
    refuted = 0
    for pi, pat in enumerate(patterns):
        cells = [Cell(i, pieces[i]) for i in pat]
        left = None
        if time_cap_total is not None:
            left = time_cap_total - (time.time() - t0)
            if left <= 0:
                results["patterns"].append({"pattern": list(pat),
                                            "status": "not-attempted"})
                continue
        tc = time_cap_per_pattern if left is None else min(
            time_cap_per_pattern, left)
        r = refute_pattern(cells, cap_max_index, floor_diam2, node_cap, tc)
        r["pattern"] = list(pat)
        results["patterns"].append(r)
        if r["status"] == "refuted":
            refuted += 1
        if out_path and (pi % 20 == 0 or pi == len(patterns) - 1):
            _dump(results, refuted, t0, out_path)
    results["patterns_refuted"] = refuted
    results["all_refuted"] = (refuted == len(patterns))
    results["elapsed_s"] = time.time() - t0
    if out_path:
        _dump(results, refuted, t0, out_path)
    verdict = ("CERTIFIED a_%d >= %s" % (npts, a)) if results["all_refuted"] \
        else ("NOT certified (%d/%d patterns refuted)" %
              (refuted, len(patterns)))
    print("  " + verdict + "  [%.1fs]" % results["elapsed_s"])
    return results


def _dump(results, refuted, t0, out_path):
    results["patterns_refuted"] = refuted
    results["elapsed_s"] = time.time() - t0
    tmp = out_path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(results, fh)
    import os
    os.replace(tmp, out_path)
