#!/usr/bin/env python3
"""Worker F3: cell-partition rationalisation of the record 15-piece cover.

Independent per-face rounding of the seed cover loses too much to cell
granularity (measured: LP 20.4 at N=281 on unit cells, vs 15 needed).  The
right grid object is a PARTITION OF THE UNIT CELLS of T_N into 15 classes
whose convex hulls each have exact squared diameter <= 3969: a class hull
contains every cell of its class by convexity, so the 15 hulls at weight 1
each form a valid fractional (indeed integral) certificate of weight
15 < 16 -- if such a partition exists.  For N <= 281 the continuum cover
(side ratio 281/63 = 4.4603 < A_15 = 1+2 sqrt3) says the SCALED cover
exists; whether a cell-closed version exists at diameter cap 63 is exactly
the granularity question, and this file answers it by local search + exact
audit.

Floats only propose the initial assignment and the repair moves; class
feasibility (hull diameter) is decided in exact integer arithmetic, and the
final object is re-audited from scratch (every cell in exactly one class,
every class hull diam^2 <= 3969) before any certificate is attempted.
"""

import math
import sys

import numpy as np

import fractional as fr
import seeded


def scaled_faces_float(N):
    A15f = 1 + 2 * math.sqrt(3.0)
    mu = min(N / A15f, 63.0)
    out = []
    for face in seeded.FACES:
        out.append([(seeded.q3_float(seeded.VERTS[k][0]) * mu,
                     seeded.q3_float(seeded.VERTS[k][1]) * mu)
                    for k in face])
    return out


def initial_assignment(N, faces):
    """Cell centroids -> nearest containing face (float; proposal only)."""
    cells = fr.unit_cells(N)
    cw = fr.cell_windows(cells)
    cx = cw["VX"].mean(axis=1)
    cy = cw["VY"].mean(axis=1)
    n = len(cells)
    assign = -np.ones(n, dtype=np.int64)
    bestd = np.full(n, 1e18)
    for fi, poly in enumerate(faces):
        # signed distance-ish: min over edges of inside-margin (float)
        m = np.full(n, 1e18)
        k = len(poly)
        for i in range(k):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % k]
            ex, ey = x2 - x1, y2 - y1
            ln = math.hypot(ex, ey) or 1.0
            # ccw polygon: inside has cross >= 0
            cr = (ex * (cy - y1) - ey * (cx - x1)) / ln
            m = np.minimum(m, cr)
        d = np.where(m >= 0, 0.0, -m)      # 0 if inside, else violation
        upd = d < bestd
        assign[upd] = fi
        bestd[upd] = d[upd]
    return cells, assign


def class_points(cells, assign, fi):
    """Unique lattice vertices of the cells in class fi."""
    idx = np.nonzero(assign == fi)[0]
    sub = cells[idx]
    I, J, up = sub[:, 0], sub[:, 1], sub[:, 3].astype(bool)
    pts = set()
    for i, j, u in zip(I, J, up):
        if u:
            pts.update([(int(i), int(j)), (int(i) + 1, int(j)),
                        (int(i), int(j) + 1)])
        else:
            pts.update([(int(i) + 1, int(j)), (int(i), int(j) + 1),
                        (int(i) + 1, int(j) + 1)])
    return pts


def hull_diam(pts):
    """(hull, exact max pairwise Q over hull vertices)."""
    h = fr.hull_int(list(pts))
    if h is None:
        h = list(pts)
    m = 0
    pair = None
    for i in range(len(h)):
        for j in range(i + 1, len(h)):
            q = fr.Q(h[i][0] - h[j][0], h[i][1] - h[j][1])
            if q > m:
                m, pair = q, (h[i], h[j])
    return h, m, pair


def cell_verts(c):
    i, j, r, up = int(c[0]), int(c[1]), int(c[2]), int(c[3])
    if up:
        return [(i, j), (i + 1, j), (i, j + 1)]
    return [(i + 1, j), (i, j + 1), (i + 1, j + 1)]


def repair(N, cap=fr.QMAX_ALLOWED, max_rounds=3000, verbose=True):
    """Tabu search over cell reassignments.  The move unit is a VERTEX
    EVICTION: take an endpoint v of an over-cap class's exact diameter pair
    and move every cell of that class incident to v into other classes
    (each cell to the target minimising the resulting excess).  Objective:
    sum over classes of max(0, diam^2 - cap).  Exact integer diameters
    throughout; floats only in the initial assignment."""
    faces = scaled_faces_float(N)
    cells, assign = initial_assignment(N, faces)
    ncls = len(faces)

    # per-class vertex multiset (vertex -> number of incident cells)
    vcount = [dict() for _ in range(ncls)]
    for ci in range(len(cells)):
        fi = int(assign[ci])
        for v in cell_verts(cells[ci]):
            vcount[fi][v] = vcount[fi].get(v, 0) + 1
    info = [hull_diam(set(vcount[fi])) for fi in range(ncls)]

    vmap = {}
    for ci in range(len(cells)):
        for v in cell_verts(cells[ci]):
            vmap.setdefault(v, []).append(ci)

    def neighbors(ci):
        i, j, r, up = (int(x) for x in cells[ci])
        out = []
        for v in cell_verts(cells[ci]):
            out.extend(vmap.get(v, []))
        return set(out) - {ci}

    def remove_cell(ci, fi):
        for v in cell_verts(cells[ci]):
            vcount[fi][v] -= 1
            if vcount[fi][v] == 0:
                del vcount[fi][v]

    def add_cell(ci, fi):
        for v in cell_verts(cells[ci]):
            vcount[fi][v] = vcount[fi].get(v, 0) + 1

    def excess(q):
        return max(0, q - cap)

    tabu = {}                     # (ci, class) -> round until forbidden
    obj = sum(excess(info[fi][1]) for fi in range(ncls))
    best_obj = obj
    for rnd in range(max_rounds):
        if obj == 0:
            break
        worst = max(range(ncls), key=lambda k: excess(info[k][1]))
        _, q, pair = info[worst]
        options = []
        for v in pair:
            v = (int(v[0]), int(v[1]))
            group = [ci for ci in vmap.get(v, []) if assign[ci] == worst]
            if not group:
                continue
            # simulate: evict all of `group` from `worst`
            touched = {worst}
            plan = []
            for ci in group:
                remove_cell(ci, worst)
            for ci in group:
                tgt_cands = {int(assign[cj]) for cj in neighbors(ci)
                             if int(assign[cj]) != worst} - \
                            {g for (c, g), until in tabu.items()
                             if c == ci and until > rnd}
                best = None
                for gj in tgt_cands:
                    add_cell(ci, gj)
                    _, qj, _ = hull_diam(set(vcount[gj]))
                    remove_cell(ci, gj)
                    if best is None or excess(qj) < best[0]:
                        best = (excess(qj), gj, qj)
                if best is None:
                    plan = None
                    break
                gj = best[1]
                add_cell(ci, gj)
                touched.add(gj)
                plan.append((ci, gj))
            if plan is None:
                for ci in group:      # roll back
                    add_cell(ci, worst)
                for ci, gj in []:
                    pass
                continue
            newinfo = {t: hull_diam(set(vcount[t])) for t in touched}
            new_obj = obj
            for t in touched:
                new_obj += excess(newinfo[t][1]) - excess(info[t][1])
            options.append((new_obj, v, group, plan, newinfo, touched))
            # roll back the simulation
            for ci, gj in plan:
                remove_cell(ci, gj)
            for ci in group:
                add_cell(ci, worst)
        if not options:
            if verbose:
                print(f"  stuck at round {rnd}: class {worst} q={q}, "
                      f"no admissible eviction")
            return None
        options.sort(key=lambda o: o[0])
        new_obj, v, group, plan, newinfo, touched = options[0]
        # commit
        for ci in group:
            remove_cell(ci, worst)
        for ci, gj in plan:
            add_cell(ci, gj)
            assign[ci] = gj
            tabu[(ci, worst)] = rnd + 40      # don't come straight back
        for t in touched:
            info[t] = newinfo[t]
        obj = new_obj
        best_obj = min(best_obj, obj)
        if verbose and (rnd % 25 == 0 or obj == 0):
            print(f"  round {rnd}: obj={obj} worst_q="
                  f"{max(info[k][1] for k in range(ncls))}")
    if obj != 0:
        if verbose:
            print(f"  round limit reached, obj={obj}")
        return None

    # ---- exact audit from scratch (no reuse of the search's state) ----
    assert (assign >= 0).all()
    fresh = [class_points(cells, assign, fi) for fi in range(ncls)]
    hulls = []
    for fi in range(ncls):
        h, q, _ = hull_diam(fresh[fi])
        assert q <= cap, f"audit: class {fi} diam2 {q} > {cap}"
        hulls.append(h)
    # every cell in exactly one class, and inside its class hull: containment
    # is by convexity (hull of a superset of the cell's vertices), but check
    # anyway with exact halfplane tests via fractional.Poly on a sample-free
    # full pass below through certify(); here check the partition property.
    counts = np.bincount(assign, minlength=ncls)
    assert counts.sum() == len(cells)
    if verbose:
        print(f"  PARTITION OK at N={N}: 15 classes, sizes "
              f"{counts.tolist()}, max diam2 = "
              f"{max(hull_diam(f)[1] for f in fresh)}")
    return hulls


def certify_partition(N, label):
    hulls = repair(N)
    if hulls is None:
        print(f"  N={N}: no feasible 15-partition found (granularity)")
        return None
    pieces = [fr.Poly([(fr.Fraction(x), fr.Fraction(y)) for x, y in h],
                      tag=f"part{i}") for i, h in enumerate(hulls)]
    for p in pieces:
        assert p.diam2_upper() <= fr.QMAX_ALLOWED
    r = fr.run_case(label, 16, N, pieces=pieces, r_bulk=1, fine_band=8,
                    corner_rad=75)
    print(f"  N={N}: {r['status']} lp={r.get('lp_value')} "
          f"total={r.get('total_weight')} bound={r.get('bound_decimal_lower')}")
    return r


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 281
    label = sys.argv[2] if len(sys.argv) > 2 else f"n16part"
    certify_partition(N, label)


# ---------------------------------------------------------------------------
# F3, second construction: per-face hull VARIANTS for the LP to mix.
# A variant of face fi is the convex hull of the lattice vertices of all
# unit cells that lie (vertex-exactly) inside face fi offset by off_e along
# each edge e (off_e > 0 extends outward, < 0 retracts).  Hulls of cells
# inside T_N have integer vertices inside T_N, so containment in T_N is
# automatic; each variant is kept only if its EXACT squared diameter is
# <= 3969.  The LP can then share weight between variants that extend at
# one seam and retract at another -- the fractional move a single
# diameter-63 piece cannot make.
# ---------------------------------------------------------------------------

def variant_polys(N, extend=(1.2, 2.2), retract=1.0, verbose=True):
    faces = scaled_faces_float(N)
    cells = fr.unit_cells(N)
    cw = fr.cell_windows(cells)
    VX, VY = cw["VX"], cw["VY"]          # [ncells, 3] int64
    out, seen = [], set()
    nfail = 0
    for fi, poly in enumerate(faces):
        k = len(poly)
        # edge data: unit-normalised inward margin per cell vertex
        edges = []
        for i in range(k):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % k]
            ex, ey = x2 - x1, y2 - y1
            ln = math.hypot(ex, ey) or 1.0
            marg = (ex * (VY - y1) - ey * (VX - x1)) / ln   # [ncells,3]
            onb = (abs(x1 - round(x1)) < 1e-9 and abs(x2 - round(x2)) < 1e-9
                   and ((round(x1) == 0 and round(x2) == 0)))
            # boundary edge iff both endpoints on the same side of T
            def onside(px, py):
                return (abs(px) < 1e-7, abs(py) < 1e-7,
                        abs(px + py - N * (1 + 2 * math.sqrt(3.0)) /
                            (1 + 2 * math.sqrt(3.0))) < 1e-7)
            b1 = (abs(x1) < 1e-7, abs(y1) < 1e-7, abs(x1 + y1 - N) < 1e-6)
            b2 = (abs(x2) < 1e-7, abs(y2) < 1e-7, abs(x2 + y2 - N) < 1e-6)
            isbnd = any(a and b for a, b in zip(b1, b2))
            edges.append((marg.min(axis=1), isbnd))   # worst vertex margin
        margins = [e[0] for e in edges]
        isbnd = [e[1] for e in edges]
        inner = [i for i in range(k) if not isbnd[i]]

        def build(offs):
            nonlocal nfail
            m = np.ones(len(cells), dtype=bool)
            for i in range(k):
                off = 0.5 if isbnd[i] else offs[i]
                m &= margins[i] >= -off
            idx = np.nonzero(m)[0]
            if idx.size == 0:
                return
            pts = set()
            for t in range(3):
                pts.update(zip(VX[idx, t].tolist(), VY[idx, t].tolist()))
            h = fr.hull_int(list(pts))
            if h is None:
                return
            q = seeded.max_pair_q(h)
            if q > fr.QMAX_ALLOWED:
                nfail += 1
                return
            key = tuple(sorted(h))
            if key in seen:
                return
            seen.add(key)
            out.append(fr.Poly([(fr.Fraction(x), fr.Fraction(y))
                                for x, y in h], tag=f"var{fi}"))

        base = [0.0] * k
        build(base)                          # offset 0
        build([-retract] * k)                # uniform retract
        for j in inner:
            for ext in extend:
                offs = [-retract] * k
                offs[j] = ext
                build(offs)
                # pairs of adjacent interior edges extended together
            offs = [-retract] * k
            offs[j] = extend[0]
            jn = (j + 1) % k
            if jn in inner:
                offs[jn] = extend[0]
                build(offs)
    if verbose:
        print(f"  variants: {len(out)} feasible pieces "
              f"({nfail} rejected by exact diameter cap)")
    return out


def vertex_variants(N, deltas=(1.5, 3.0, 6.0), offs=(0.2, -1.0), verbose=True):
    """Variants built by radially displacing ONE vertex of a face outward
    (from the face centroid) before collecting cells.  The record proves the
    four junction vertices are rattlers with ~0.137 separation units
    (~8.6 grid units) of slack, so such moves can be diameter-feasible; the
    exact cap check filters the ones that are not."""
    faces = scaled_faces_float(N)
    cells = fr.unit_cells(N)
    cw = fr.cell_windows(cells)
    VX, VY = cw["VX"], cw["VY"]
    out, seen, nfail = [], set(), 0

    def build(poly, off):
        nonlocal nfail
        k = len(poly)
        m = np.ones(len(cells), dtype=bool)
        for i in range(k):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % k]
            ex, ey = x2 - x1, y2 - y1
            ln = math.hypot(ex, ey) or 1.0
            marg = ((ex * (VY - y1) - ey * (VX - x1)) / ln).min(axis=1)
            m &= marg >= -off
        idx = np.nonzero(m)[0]
        if idx.size == 0:
            return
        pts = set()
        for t in range(3):
            pts.update(zip(VX[idx, t].tolist(), VY[idx, t].tolist()))
        h = fr.hull_int(list(pts))
        if h is None:
            return
        q = seeded.max_pair_q(h)
        if q > fr.QMAX_ALLOWED:
            nfail += 1
            return
        key = tuple(sorted(h))
        if key in seen:
            return
        seen.add(key)
        out.append(fr.Poly([(fr.Fraction(x), fr.Fraction(y))
                            for x, y in h], tag="vmove"))

    for fi, poly in enumerate(faces):
        k = len(poly)
        cx = sum(p[0] for p in poly) / k
        cy = sum(p[1] for p in poly) / k
        for t in range(k):
            x, y = poly[t]
            dx, dy = x - cx, y - cy
            ln = math.hypot(dx, dy) or 1.0
            for d in deltas:
                moved = list(poly)
                moved[t] = (x + dx / ln * d, y + dy / ln * d)
                for off in offs:
                    build(moved, off)
    if verbose:
        print(f"  vertex variants: {len(out)} feasible "
              f"({nfail} rejected by cap)")
    return out
