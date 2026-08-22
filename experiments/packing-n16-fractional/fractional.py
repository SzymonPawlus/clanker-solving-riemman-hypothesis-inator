#!/usr/bin/env python3
"""Fractional (LP-relaxed) covering lower bounds for point separation in an
equilateral triangle.  Worker F2, issue #97, attack `n16-fractional`.

Lemma F (proved in the attack README).  Work in the chart e1=(1,0),
e2=(1/2,sqrt(3)/2), so |u e1 + v e2|^2 = Q(u,v) = u^2+uv+v^2 and
T_a = {u>=0, v>=0, u+v<=a}.  Let S_1..S_M be sets with diam(S_i) < 1
(strictly), let y_i >= 0 satisfy  sum_{i: x in S_i} y_i >= 1 for every
x in T_a, and let C be a subset of T_a with pairwise distances >= 1.  Then
|C| <= sum_i y_i.  Hence if sum_i y_i < n (an integer), T_a holds at most
n-1 separated points, so a_n >= a; and if max_i diam S_i = D <= 1 the
dilation/limit argument gives a_n >= a/D.

Units: everything lives on an integer grid of 1/64 of the separation
distance.  Pieces are kept at diameter <= 63 units (= 63/64 < 1), so a
verified certificate on T_N (side N units) proves a_n >= N/63 -- more
precisely N/sqrt(Qmax) with Qmax the exact maximal squared diameter.

Every decision that enters the certificate is exact integer or Fraction
arithmetic (numpy int64 is exact at these magnitudes; magnitude asserts are
in place).  Floating point appears only inside scipy's LP solver, which
merely *proposes* weights; the proposal is rounded up to exact rationals
and re-verified from scratch.

CIRCULARITY GUARD: for the open case n=16 the only problem-specific input
is the integer EXCLUDE_POINTS = 16 (the pigeonhole budget: total weight
must be strictly below it).  No quantity derived from any 16-point packing
-- in particular neither 4.6247637 nor 1+2*sqrt(3) -- is an input to any
computation here.  The constant TRIPWIRE below is used only *after* a
bound is computed, to refuse-and-flag suspiciously strong output
(repo RULES.md section 7), never to produce it.
"""

import json
import math
import os
import sys
import time
from fractions import Fraction

import numpy as np
from scipy import sparse
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
CERTDIR = os.path.join(HERE, "certs")

UNIT = 64            # grid units per separation distance
WMAX = 63            # max piece width in units  -> diameter <= 63/64 < 1
QMAX_ALLOWED = WMAX * WMAX   # 3969, in units^2
TRIPWIRE = Fraction(462, 100)  # 4.62; comparison-only, see guard note above.


def Q(dx, dy):
    return dx * dx + dx * dy + dy * dy


# ---------------------------------------------------------------------------
# exact rational polygon helpers
# ---------------------------------------------------------------------------

def clip_halfplane(poly, A, B, C):
    """Keep {(x,y): A*x + B*y <= C}. poly = ccw list of (Fraction,Fraction)."""
    if not poly:
        return []
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp = A * p[0] + B * p[1] - C
        fq = A * q[0] + B * q[1] - C
        if fp <= 0:
            out.append(p)
            if fq > 0:
                t = fp / (fp - fq)
                out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
        elif fq <= 0:
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    # dedupe
    ded = []
    for v in out:
        if not ded or v != ded[-1]:
            ded.append(v)
    if len(ded) > 1 and ded[0] == ded[-1]:
        ded.pop()
    return ded


def clean_convex_ccw(verts):
    """Drop collinear middle vertices; verify convex ccw; None if invalid."""
    n = len(verts)
    if n < 3:
        return None
    keep = []
    for i in range(n):
        a, b, c = verts[(i - 1) % n], verts[i], verts[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        if cr < 0:
            return None
        if cr > 0:
            keep.append(b)
    if len(keep) < 3:
        return None
    return keep


def poly_halfplanes_int(verts):
    """ccw convex polygon -> list of integer (A,B,C) with region = {Ax+By<=C}.
    Edge p->q, interior on the left: (q-p) x (x-p) >= 0
    => (qy-py)x - (qx-px)y <= (qy-py)px - (qx-px)py ... sign worked out below."""
    hps = []
    n = len(verts)
    for i in range(n):
        p, q = verts[i], verts[(i + 1) % n]
        # left side: cross(q-p, x-p) >= 0  <=>  -(qy-py)x + (qx-px)y <= -(qy-py)px + (qx-px)py...
        # cross = (qx-px)(y-py) - (qy-py)(x-px) >= 0
        A = q[1] - p[1]
        B = -(q[0] - p[0])
        C = A * p[0] + B * p[1]
        # region: A x + B y <= C
        den = 1
        for z in (A, B, C):
            if isinstance(z, Fraction):
                den = den * z.denominator // math.gcd(den, z.denominator)
        A, B, C = int(A * den), int(B * den), int(C * den)
        g = math.gcd(math.gcd(abs(A), abs(B)), abs(C)) or 1
        hps.append((A // g, B // g, C // g))
    return hps


def poly_diam2(verts):
    """Exact max pairwise Q over vertices (Fraction)."""
    m = Fraction(0)
    n = len(verts)
    for i in range(n):
        for j in range(i + 1, n):
            d = Q(verts[i][0] - verts[j][0], verts[i][1] - verts[j][1])
            if d > m:
                m = d
    return m


def hull_int(points):
    """Andrew monotone chain, integer points, strictly convex ccw hull."""
    pts = sorted(set(points))
    if len(pts) < 3:
        return None

    def half(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and \
                    (h[-1][0] - h[-2][0]) * (p[1] - h[-2][1]) - \
                    (h[-1][1] - h[-2][1]) * (p[0] - h[-2][0]) <= 0:
                h.pop()
            h.append(p)
        return h

    lo = half(pts)
    hi = half(pts[::-1])
    hull = lo[:-1] + hi[:-1]
    return hull if len(hull) >= 3 else None


# ---------------------------------------------------------------------------
# pieces
# ---------------------------------------------------------------------------

class Box:
    """{L1<=u<=U1, L2<=v<=U2, L3<=u+v<=U3}, integer bounds."""
    kind = "box"

    def __init__(self, L1, U1, L2, U2, L3, U3):
        self.b = (L1, U1, L2, U2, L3, U3)

    def diam2_upper(self):
        """Exact upper bound on squared diameter: max of Q over the
        difference polytope {|dx|<=w1,|dy|<=w2,|dx+dy|<=w3} (a superset of
        the true difference body, so this is a safe overestimate).  Q is
        convex, so the max is at a vertex; enumerate all line-pair
        intersections exactly."""
        L1, U1, L2, U2, L3, U3 = self.b
        w1, w2, w3 = U1 - L1, U2 - L2, U3 - L3
        lines = [("x", w1), ("x", -w1), ("y", w2), ("y", -w2),
                 ("s", w3), ("s", -w3)]
        best = 0
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                (t1, c1), (t2, c2) = lines[i], lines[j]
                if t1 == t2:
                    continue
                if {t1, t2} == {"x", "y"}:
                    x = c1 if t1 == "x" else c2
                    y = c1 if t1 == "y" else c2
                elif {t1, t2} == {"x", "s"}:
                    x = c1 if t1 == "x" else c2
                    s = c1 if t1 == "s" else c2
                    y = s - x
                else:
                    y = c1 if t1 == "y" else c2
                    s = c1 if t1 == "s" else c2
                    x = s - y
                if abs(x) <= w1 and abs(y) <= w2 and abs(x + y) <= w3:
                    best = max(best, Q(x, y))
        return Fraction(best)

    def verts(self):
        L1, U1, L2, U2, L3, U3 = self.b
        poly = [(Fraction(L1), Fraction(L2)), (Fraction(U1), Fraction(L2)),
                (Fraction(U1), Fraction(U2)), (Fraction(L1), Fraction(U2))]
        poly = clip_halfplane(poly, Fraction(-1), Fraction(-1), Fraction(-L3))
        poly = clip_halfplane(poly, Fraction(1), Fraction(1), Fraction(U3))
        return poly

    def nonempty(self):
        L1, U1, L2, U2, L3, U3 = self.b
        return L1 <= U1 and L2 <= U2 and L3 <= U3 and \
            L3 <= U1 + U2 and U3 >= L1 + L2

    def contains_mask(self, cw):
        """cw = dict of numpy arrays with cell windows."""
        L1, U1, L2, U2, L3, U3 = self.b
        return ((cw["ulo"] >= L1) & (cw["uhi"] <= U1) &
                (cw["vlo"] >= L2) & (cw["vhi"] <= U2) &
                (cw["slo"] >= L3) & (cw["shi"] <= U3))

    def desc(self):
        return {"kind": "box", "bounds": list(self.b)}


class Poly:
    """Convex ccw polygon with rational vertices; region = intersection of
    the halfplanes derived from the vertices (so region == hull(verts))."""
    kind = "poly"

    def __init__(self, verts, tag=""):
        self.vertsF = [(Fraction(a), Fraction(b)) for a, b in verts]
        self.tag = tag
        self.hps = poly_halfplanes_int(self.vertsF)

    def diam2_upper(self):
        return poly_diam2(self.vertsF)

    def nonempty(self):
        return len(self.vertsF) >= 3

    def bbox(self):
        xs = [v[0] for v in self.vertsF]
        ys = [v[1] for v in self.vertsF]
        return (min(xs), max(xs), min(ys), max(ys))

    def contains_mask(self, cw):
        # bounding-box prefilter, then exact integer halfplane tests on the
        # 3 vertices of each cell.
        x0, x1, y0, y1 = self.bbox()
        m = ((cw["ulo"] >= math.floor(x0)) & (cw["uhi"] <= math.ceil(x1)) &
             (cw["vlo"] >= math.floor(y0)) & (cw["vhi"] <= math.ceil(y1)))
        idx = np.nonzero(m)[0]
        if idx.size == 0:
            return m
        ok = np.ones(idx.size, dtype=bool)
        VX, VY = cw["VX"], cw["VY"]  # int64 [ncells,3]
        for (A, B, C) in self.hps:
            assert abs(A) < 2**20 and abs(B) < 2**20 and abs(C) < 2**40
            val = A * VX[idx] + B * VY[idx]  # int64 exact
            ok &= (val <= C).all(axis=1)
        out = np.zeros_like(m)
        out[idx[ok]] = True
        return out

    def desc(self):
        return {"kind": "poly", "tag": self.tag,
                "verts": [[str(a), str(b)] for a, b in self.vertsF]}


def sigma_poly(piece, N):
    """The rational isometry sigma(u,v) = (N-u-v, u) (rotates T_N's corners
    A->B->C).  It preserves Q: Q(-du-dv, du) = Q(du,dv)."""
    vs = [(Fraction(N) - a - b, a) for a, b in piece.vertsF]
    vs = clean_convex_ccw(vs)
    return Poly(vs, tag=piece.tag + "+s") if vs else None


# ---------------------------------------------------------------------------
# cells (rows).  A generalized cell is a lattice triangle of size r:
# up:   verts (I,J),(I+r,J),(I,J+r)      windows u:[I,I+r] v:[J,J+r] s:[I+J,I+J+r]
# down: verts (I+r,J),(I,J+r),(I+r,J+r)  windows u:[I,I+r] v:[J,J+r] s:[I+J+r,I+J+2r]
# The unit (r=1) up/down cells partition T_N exactly.
# ---------------------------------------------------------------------------

def cell_windows(cells):
    """cells: numpy array [(I,J,r,up)] -> window arrays + vertex arrays."""
    I = cells[:, 0].astype(np.int64)
    J = cells[:, 1].astype(np.int64)
    r = cells[:, 2].astype(np.int64)
    up = cells[:, 3].astype(bool)
    S = I + J
    cw = {
        "ulo": I, "uhi": I + r, "vlo": J, "vhi": J + r,
        "slo": np.where(up, S, S + r), "shi": np.where(up, S + r, S + 2 * r),
    }
    VX = np.empty((len(cells), 3), dtype=np.int64)
    VY = np.empty((len(cells), 3), dtype=np.int64)
    VX[up, 0], VY[up, 0] = I[up], J[up]
    VX[up, 1], VY[up, 1] = I[up] + r[up], J[up]
    VX[up, 2], VY[up, 2] = I[up], J[up] + r[up]
    dn = ~up
    VX[dn, 0], VY[dn, 0] = I[dn] + r[dn], J[dn]
    VX[dn, 1], VY[dn, 1] = I[dn], J[dn] + r[dn]
    VX[dn, 2], VY[dn, 2] = I[dn] + r[dn], J[dn] + r[dn]
    cw["VX"], cw["VY"] = VX, VY
    return cw


def unit_cells(N):
    out = []
    for i in range(N):
        for j in range(N - i):
            out.append((i, j, 1, 1))
            if i + j <= N - 2:
                out.append((i, j, 1, 0))
    return np.array(out, dtype=np.int64)


def lp_rows(N, r_bulk, fine_band, corner_rad):
    """Mixed-resolution row set covering T_N: unit cells within `fine_band`
    of an edge or within `corner_rad` (in Q) of a corner; r_bulk-triangles
    (aligned to multiples of r_bulk) elsewhere; unit cells wherever the
    coarse grid does not reach.  Every point of T_N lies in some row --
    which is all soundness needs; rows may overlap."""
    rows = []
    covered = set()
    rb = r_bulk
    for I in range(0, N, rb):
        for Jj in range(0, N - I, rb):
            if I + Jj + rb > N:
                continue
            # coarse up-triangle fully inside and fully in the bulk?
            def near_edge(x, y):
                if x < fine_band or y < fine_band or (N - x - y) < fine_band:
                    return True
                for (cx, cy) in ((0, 0), (N, 0), (0, N)):
                    if Q(x - cx, y - cy) < corner_rad * corner_rad:
                        return True
                return False
            corners = [(I, Jj), (I + rb, Jj), (I, Jj + rb), (I + rb, Jj + rb)]
            if any(near_edge(x, y) for x, y in corners):
                continue
            rows.append((I, Jj, rb, 1))
            if I + Jj + 2 * rb <= N:
                rows.append((I, Jj, rb, 0))
            for di in range(rb):
                for dj in range(rb):
                    if di + dj < rb:
                        covered.add((I + di, Jj + dj, 1))
                        if di + dj < rb - 1:
                            covered.add((I + di, Jj + dj, 0))
            # the down coarse triangle covers cells too
            if I + Jj + 2 * rb <= N:
                for di in range(rb):
                    for dj in range(rb):
                        if di + dj >= rb - 1:
                            covered.add((I + di, Jj + dj, 0))
                        if di + dj >= rb:
                            covered.add((I + di, Jj + dj, 1))
    for i in range(N):
        for j in range(N - i):
            if (i, j, 1) not in covered:
                rows.append((i, j, 1, 1))
            if i + j <= N - 2 and (i, j, 0) not in covered:
                rows.append((i, j, 1, 0))
    return np.array(rows, dtype=np.int64)


# ---------------------------------------------------------------------------
# family generation
# ---------------------------------------------------------------------------

def gen_family(N, step_bulk=4, step_edge=6, quad_caps=True):
    pieces = []
    W = WMAX
    lo, hi = -W, N + 1
    # boxes: hexagons (three s-offsets), up- and down-triangles
    for L1 in range(lo, hi, step_bulk):
        for L2 in range(lo, hi, step_bulk):
            if L1 + L2 > N or L1 + L2 + 2 * W < 0:
                continue
            for k, styp in ((0, "up"), (W, "down"), (16, "hex"), (32, "hex"), (48, "hex")):
                b = Box(L1, L1 + W, L2, L2 + W, L1 + L2 + k, L1 + L2 + k + W)
                if b.nonempty():
                    pieces.append(b)
    # edge-flush boxes: slide along each edge at step_edge for finer
    # boundary structure (u=0 edge, v=0 edge, hypotenuse)
    for t in range(-W, N + 1, step_edge):
        for k, styp in ((0, "up"), (W, "down"), (32, "hex")):
            pieces.append(Box(t, t + W, 0, W, t + k, t + k + W))          # v=0 flush
            pieces.append(Box(0, W, t, t + W, t + k, t + k + W))          # u=0 flush
            pieces.append(Box(t, t + W, N - W - t - k, N - t - k + 0 + W,
                              N - W, N))                                   # s=N flush
    pieces = [p for p in pieces if p.nonempty()]

    # corner sectors: hull of integer points of the 60-degree wedge within
    # distance 63 of the apex, at each corner (exact images under sigma).
    pts = [(x, y) for x in range(0, W + 1) for y in range(0, W + 1)
           if Q(x, y) <= QMAX_ALLOWED]
    h = hull_int(pts)
    secA = Poly([(Fraction(a), Fraction(b)) for a, b in h], tag="cornerA")
    polys = [secA]
    sB = sigma_poly(secA, N)
    if sB:
        polys.append(sB)
        sC = sigma_poly(sB, N)
        if sC:
            polys.append(sC)

    # edge sectors: apex (c,0) on the bottom edge, three 60-degree wedges
    # (upright, lean-left, lean-right), then sigma-images for other edges.
    base = []
    for wedge in ("upright", "left", "right"):
        ps = []
        for dx in range(-127, 128):
            for dy in range(0, 128):
                if Q(dx, dy) > QMAX_ALLOWED:
                    continue
                if wedge == "upright" and (dx > 0 or dx + dy < 0):
                    continue
                if wedge == "left" and (dx + dy > 0):
                    continue
                if wedge == "right" and (dx < 0):
                    continue
                ps.append((dx, dy))
        h = hull_int(ps)
        if h:
            base.append((wedge, h))
    for c in range(0, N + 1, step_edge):
        for wedge, h in base:
            vs = [(Fraction(c + dx), Fraction(dy)) for dx, dy in h]
            p0 = Poly(vs, tag=f"edge-{wedge}-{c}")
            for p in (p0, sigma_poly(p0, N)):
                if p is None:
                    continue
                polys.append(p)
                p2 = sigma_poly(p, N)
                if p2 is not None:
                    polys.append(p2)

    # corner quads {u,v>=0, 2u+v<=c, u+2v<=c, u+v<=cap}: reach past the
    # sector hull's lattice chord near the diagonal (needed at the n=4
    # control; harmless elsewhere).  Filter by exact diameter.
    if quad_caps:
        for c in range(90, min(2 * W + 20, N + 8) + 1, 1):
            for m in range(2 * c // 3 - 4, 146):
                cap = Fraction(m, 2)
                poly = [(Fraction(0), Fraction(0)), (Fraction(3 * N), Fraction(0)),
                        (Fraction(0), Fraction(3 * N))]
                for (A, B, C) in ((2, 1, c), (1, 2, c), (1, 1, cap)):
                    poly = clip_halfplane(poly, Fraction(A), Fraction(B), Fraction(C))
                poly = clean_convex_ccw(poly)
                if not poly:
                    continue
                if poly_diam2(poly) > QMAX_ALLOWED:
                    continue
                q0 = Poly(poly, tag=f"quad-{c}-{m}")
                polys.append(q0)
                q1 = sigma_poly(q0, N)
                if q1:
                    polys.append(q1)
                    q2 = sigma_poly(q1, N)
                    if q2:
                        polys.append(q2)
    pieces.extend([p for p in polys if p.nonempty()])
    return pieces


# ---------------------------------------------------------------------------
# LP + exact certification
# ---------------------------------------------------------------------------

def membership_matrix(pieces, cw, ncells):
    cols, rows_idx = [], []
    for pi, p in enumerate(pieces):
        m = p.contains_mask(cw)
        idx = np.nonzero(m)[0]
        rows_idx.append(idx)
        cols.append(np.full(idx.size, pi, dtype=np.int64))
    ri = np.concatenate(rows_idx) if rows_idx else np.array([], dtype=np.int64)
    ci = np.concatenate(cols) if cols else np.array([], dtype=np.int64)
    data = np.ones(ri.size, dtype=np.float64)
    return sparse.csr_matrix((data, (ri, ci)), shape=(ncells, len(pieces)))


def certify(N, budget, pieces, verbose=True, r_bulk=3, fine_band=6,
            corner_rad=70, lp_time=None):
    """Try to produce an exact certificate: total weight < budget on T_N.
    Returns dict with lp value, and on success exact data."""
    t0 = time.time()
    rows = lp_rows(N, r_bulk, fine_band, corner_rad)
    cw = cell_windows(rows)
    M = membership_matrix(pieces, cw, len(rows))
    # drop always-empty pieces
    keep = np.asarray((M.sum(axis=0) > 0)).ravel()
    # rows with no piece: LP infeasible
    rowcnt = np.asarray((M.sum(axis=1))).ravel()
    if (rowcnt == 0).any():
        nbad = int((rowcnt == 0).sum())
        if verbose:
            print(f"  N={N}: {nbad} rows covered by no piece -> infeasible")
        return {"N": N, "budget": budget, "status": "infeasible-rows",
                "bad_rows": nbad}
    if verbose:
        print(f"  N={N}: rows={len(rows)} pieces={len(pieces)} "
              f"nnz={M.nnz} build={time.time()-t0:.1f}s")
    c = np.ones(M.shape[1])
    res = linprog(c, A_ub=-M, b_ub=-np.ones(M.shape[0]),
                  bounds=(0, None), method="highs",
                  options={"time_limit": lp_time} if lp_time else None)
    if not res.success:
        if verbose:
            print(f"  N={N}: LP failed: {res.message}")
        return {"N": N, "budget": budget, "status": "lp-failed",
                "message": res.message}
    lpval = float(res.fun)
    if verbose:
        print(f"  N={N}: LP value = {lpval:.4f} (budget {budget}) "
              f"[{time.time()-t0:.1f}s]")
    out = {"N": N, "budget": budget, "lp_value": lpval, "status": "lp-only"}
    if lpval >= budget - 1e-6:
        return out

    # ---- exact rounding + verification ----
    K = 1 << 16
    y = res.x
    sup = np.nonzero(y > 1e-9)[0]
    numers = {int(i): int(math.ceil(y[i] * K)) for i in sup}
    total = sum(numers.values())
    if total >= budget * K:
        out["status"] = "rounding-exceeded"
        return out

    # exact verification on the full unit-cell partition of T_N
    ucells = unit_cells(N)
    ucw = cell_windows(ucells)
    sums = np.zeros(len(ucells), dtype=np.int64)
    sup_list = sorted(numers)
    qmax = Fraction(0)
    for pi in sup_list:
        p = pieces[pi]
        d2 = p.diam2_upper()
        assert d2 <= QMAX_ALLOWED, f"piece {pi} diameter too large: {d2}"
        if d2 > qmax:
            qmax = d2
        m = p.contains_mask(ucw)
        sums[m] += numers[pi]
    bad = np.nonzero(sums < K)[0]
    if bad.size:
        # remedial greedy pass: bump weight on pieces covering deficits
        for _ in range(200):
            bad = np.nonzero(sums < K)[0]
            if bad.size == 0:
                break
            best, bestcnt = None, 0
            deficit = int((K - sums[bad]).max())
            for pi, p in enumerate(pieces):
                m = p.contains_mask(ucw)
                cnt = int(m[bad].sum())
                if cnt > bestcnt:
                    best, bestcnt, bestm = pi, cnt, m
            if best is None:
                break
            numers[best] = numers.get(best, 0) + deficit
            sums[bestm] += deficit
            if best in [pi for pi in sup_list]:
                pass
            d2 = pieces[best].diam2_upper()
            assert d2 <= QMAX_ALLOWED
            if d2 > qmax:
                qmax = d2
        bad = np.nonzero(sums < K)[0]
        if bad.size:
            out["status"] = "verify-failed"
            out["bad_cells"] = int(bad.size)
            return out
    total = sum(numers.values())
    if total >= budget * K:
        out["status"] = "rounding-exceeded"
        out["total"] = f"{total}/{K}"
        return out

    # exact bound: a_n >= N / sqrt(qmax_units)/ (1/UNIT scale cancels)
    # bound^2 = N^2 / qmax ; decimal lower bound via isqrt
    num = N * N * qmax.denominator
    den = qmax.numerator
    scale = 10 ** 12
    bound_floor = math.isqrt(num * scale * scale // den)  # floor(sqrt) => lower bnd
    bound_str = f"{bound_floor // scale}.{bound_floor % scale:012d}"
    out.update({
        "status": "verified",
        "total_weight": f"{total}/{K}",
        "total_float": total / K,
        "qmax": f"{qmax.numerator}/{qmax.denominator}",
        "n_support": len(numers),
        "bound_exact_sq": f"{num}/{den}",
        "bound_decimal_lower": bound_str,
        "seconds": round(time.time() - t0, 1),
    })
    bnd = Fraction(num, den)  # bound^2
    if bnd > TRIPWIRE * TRIPWIRE:
        out["TRIPWIRE"] = ("bound exceeds 4.62 -- RULES.md section 7: do not "
                           "extend, flag for review, suspect an input error")
    out["certificate"] = {
        "N_units": N, "unit": f"1/{UNIT}", "K": K, "budget_points": budget,
        "weights": {str(pi): numers[pi] for pi in sorted(numers)},
        "pieces": {str(pi): pieces[pi].desc() for pi in sorted(numers)},
    }
    return out


def run_case(label, n_points, N, pieces=None, **kw):
    """budget = n_points: total weight < n_points excludes n_points
    separated points, proving a_{n_points} >= N/sqrt(qmax)."""
    if pieces is None:
        pieces = gen_family(N, **{k: v for k, v in kw.items()
                                  if k in ("step_bulk", "step_edge")})
    kw2 = {k: v for k, v in kw.items() if k in ("r_bulk", "fine_band",
                                                "corner_rad", "lp_time")}
    res = certify(N, n_points, pieces, **kw2)
    res["label"] = label
    os.makedirs(CERTDIR, exist_ok=True)
    with open(os.path.join(CERTDIR, "results.jsonl"), "a") as f:
        cert = res.pop("certificate", None)
        f.write(json.dumps(res) + "\n")
        if cert is not None:
            path = os.path.join(CERTDIR, f"cert_{label}_N{N}.json")
            with open(path, "w") as g:
                json.dump({**res, "certificate": cert}, g, indent=1)
            res["certificate"] = cert
            print(f"  wrote {path}")
    return res


# ---------------------------------------------------------------------------
# drivers
# ---------------------------------------------------------------------------

def controls():
    """K1: n=4 (a=sqrt3), n=6 (a=2), n=10 (a=3).  For each: the soundness
    run just above 63*a_n must NOT verify; then certify descending N."""
    print("== controls ==")
    ok = True
    plans = [
        ("n4", 4, [111, 109, 108, 107, 106], 109),   # floor(63*sqrt3)=109
        ("n6", 6, [129, 127, 126, 125, 124], 126),   # 63*2
        ("n10", 10, [192, 190, 189, 188, 187], 189), # 63*3
    ]
    for label, n, Ns, cap in plans:
        best = None
        for N in Ns:
            pieces = gen_family(N, step_bulk=3, step_edge=3)
            r = run_case(label, n, N, pieces=pieces, r_bulk=3, fine_band=8,
                         corner_rad=75)
            if r["status"] == "verified":
                b = r["bound_decimal_lower"]
                print(f"  {label}: N={N} VERIFIED bound {b}")
                if N > cap:
                    print(f"  !!! SOUNDNESS FAILURE: {label} N={N} > cap {cap}")
                    ok = False
                best = N
                break
            else:
                print(f"  {label}: N={N} -> {r['status']} "
                      f"lp={r.get('lp_value')}")
        if best is None or best < cap - 3:
            print(f"  !!! POWER FAILURE: {label} best={best} cap={cap}")
            ok = False
    print("== controls", "PASS" if ok else "FAIL", "==")
    return ok


def sweep16(Ns):
    print("== n=16 sweep ==")
    # CIRCULARITY GUARD: the only input is the pigeonhole budget below.
    EXCLUDE_POINTS = 16
    for N in Ns:
        pieces = gen_family(N, step_bulk=4, step_edge=4)
        r = run_case("n16", EXCLUDE_POINTS, N, pieces=pieces, r_bulk=3,
                     fine_band=8, corner_rad=75, lp_time=600)
        print(f"  n16 N={N}: {r['status']} lp={r.get('lp_value')} "
              f"bound={r.get('bound_decimal_lower')}")
        if r.get("TRIPWIRE"):
            print("  TRIPWIRE HIT -- stopping sweep per KILL-CRITERION K3")
            break


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "control"
    if cmd == "control":
        controls()
    elif cmd == "run":
        n = int(sys.argv[2]); N = int(sys.argv[3])
        r = run_case(f"n{n}", n, N, step_bulk=4, step_edge=4,
                     r_bulk=3, fine_band=8, corner_rad=75)
        print(json.dumps({k: v for k, v in r.items() if k != "certificate"},
                         indent=1))
    elif cmd == "sweep16":
        Ns = [int(x) for x in sys.argv[2:]] or [285, 282, 288]
        sweep16(Ns)
    else:
        print("usage: fractional.py control | run <n> <N> | sweep16 [Ns...]")
