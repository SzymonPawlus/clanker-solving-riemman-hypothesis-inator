"""Local solver and seed families for the n = 16 upper-bound attack.

The SLSQP formulation and the ``clip_into_triangle`` / ``local_solve`` core are **adapted, with
attribution, from** ``experiments/circle-packing-search/search.py`` (another worker's read-only
directory).  What is new here is the seed families: the structural T(5)+1 enumeration, the
symmetry-reduced ansaetze, the row partitions, and the rattler-aware perturbation off a known
configuration.  Nothing in this module proves anything -- everything it returns is a float
hypothesis for ``exact_gate.py`` to decide.

Formulation (unit triangle T = conv{(0,0), (1,0), (1/2, sqrt(3)/2)}):

    maximise    m
    subject to  |p_i - p_j|^2 - m^2 >= 0,   y_i >= 0,
                sqrt(3) x_i - y_i >= 0,     sqrt(3)(1 - x_i) - y_i >= 0.

The reported value is always the minimum pairwise distance measured **after projecting the
points back into the triangle**, never SLSQP's own ``m``; trusting the latter is how a fake
record is born.
"""

from __future__ import annotations

import math
from itertools import combinations

import numpy as np
from scipy.optimize import minimize

SQRT3 = math.sqrt(3.0)
VERTICES = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, SQRT3 / 2.0]])


# ---------------------------------------------------------------------------- geometry -----


def clip_into_triangle(p: np.ndarray) -> np.ndarray:
    x, y = p[:, 0], p[:, 1]
    l2 = y / (SQRT3 / 2.0)
    l1 = x - y / SQRT3
    l0 = 1.0 - l1 - l2
    lam = np.clip(np.stack([l0, l1, l2], axis=1), 0.0, None)
    s = lam.sum(axis=1, keepdims=True)
    s[s == 0] = 1.0
    lam = lam / s
    return lam @ VERTICES


def bary_to_xy(l1: np.ndarray, l2: np.ndarray) -> np.ndarray:
    """(l1, l2) are the weights on (1,0) and (1/2, sqrt3/2)."""
    return np.stack([l1 + 0.5 * l2, (SQRT3 / 2.0) * l2], axis=1)


def min_pair_distance(p: np.ndarray) -> float:
    n = len(p)
    if n < 2:
        return float("inf")
    d = np.linalg.norm(p[:, None, :] - p[None, :, :], axis=-1)
    d[np.arange(n), np.arange(n)] = np.inf
    return float(d.min())


def sample_uniform(n: int, rng: np.random.Generator) -> np.ndarray:
    r = rng.random((n, 2))
    fold = r.sum(axis=1) > 1.0
    r[fold] = 1.0 - r[fold]
    return bary_to_xy(r[:, 0], r[:, 1])


def tri_lattice(k: int) -> np.ndarray:
    """The T(k) lattice: k(k+1)/2 points, spacing 1/(k-1), spanning the unit triangle."""
    pts = []
    for i in range(k):
        for j in range(k - i):
            pts.append((i / (k - 1), j / (k - 1)))
    a = np.array(pts)
    return bary_to_xy(a[:, 0], a[:, 1])


# ------------------------------------------------------------------------- local solve -----


def _pair_index(n: int):
    iu = np.triu_indices(n, k=1)
    return iu[0], iu[1]


def local_solve(p0: np.ndarray, maxiter: int = 250, ftol: float = 1e-14):
    n = len(p0)
    ii, jj = _pair_index(n)
    npair = len(ii)
    m0 = min_pair_distance(p0)
    if not math.isfinite(m0) or m0 <= 0:
        m0 = 0.1
    z0 = np.concatenate([p0.ravel(), [m0]])

    def unpack(z):
        return z[:-1].reshape(n, 2), z[-1]

    def neg_m(z):
        return -z[-1]

    def neg_m_grad(z):
        g = np.zeros_like(z)
        g[-1] = -1.0
        return g

    def cons_f(z):
        p, m = unpack(z)
        diff = p[ii] - p[jj]
        pair = np.einsum("ij,ij->i", diff, diff) - m * m
        return np.concatenate(
            [pair, p[:, 1], SQRT3 * p[:, 0] - p[:, 1], SQRT3 * (1.0 - p[:, 0]) - p[:, 1]]
        )

    def cons_jac(z):
        p, m = unpack(z)
        J = np.zeros((npair + 3 * n, 2 * n + 1))
        diff = p[ii] - p[jj]
        rows = np.arange(npair)
        J[rows, 2 * ii] = 2.0 * diff[:, 0]
        J[rows, 2 * ii + 1] = 2.0 * diff[:, 1]
        J[rows, 2 * jj] = -2.0 * diff[:, 0]
        J[rows, 2 * jj + 1] = -2.0 * diff[:, 1]
        J[rows, -1] = -2.0 * m
        k = np.arange(n)
        J[npair + k, 2 * k + 1] = 1.0
        J[npair + n + k, 2 * k] = SQRT3
        J[npair + n + k, 2 * k + 1] = -1.0
        J[npair + 2 * n + k, 2 * k] = -SQRT3
        J[npair + 2 * n + k, 2 * k + 1] = -1.0
        return J

    res = minimize(
        neg_m,
        z0,
        jac=neg_m_grad,
        method="SLSQP",
        constraints=[{"type": "ineq", "fun": cons_f, "jac": cons_jac}],
        options={"maxiter": maxiter, "ftol": ftol},
    )
    p, _ = unpack(res.x)
    p = clip_into_triangle(p)
    return p, min_pair_distance(p)


# ------------------------------------------------------------------------ seed families -----


def seed_uniform(n, rng):
    return sample_uniform(n, rng)


def seed_lattice_defect(n, rng):
    """T(6) = 21 lattice, drop 5, jitter over two decades of amplitude."""
    pts = tri_lattice(6)
    keep = rng.choice(len(pts), size=n, replace=False)
    p = pts[keep]
    amp = 10 ** rng.uniform(-3, -0.7)
    return clip_into_triangle(p + rng.normal(scale=amp, size=p.shape))


def _t5_sites(rng, mode: str):
    """Candidate positions for the 16th point on top of the T(5) lattice.

    16 = T(5) + 1, so the single most natural structural family is "the 15-point optimum plus one
    more".  The T(5) lattice at spacing 1/4 leaves no room, so the extra point must push the whole
    configuration open; the seed therefore *shrinks* the lattice and inserts the extra point at a
    distinguishable site: a triangle-cell centre (up- or down-pointing), an edge midpoint, a
    vertex neighbourhood, or a random point.
    """
    sites = []
    # up-cell and down-cell centroids of the 1/4-spacing lattice, in barycentric (l1, l2)
    for i in range(4):
        for j in range(4 - i):
            sites.append(((i + 1 / 3) / 4, (j + 1 / 3) / 4))
    for i in range(3):
        for j in range(3 - i):
            sites.append(((i + 2 / 3) / 4, (j + 2 / 3) / 4))
    # edge midpoints of the lattice cells
    for i in range(5):
        for j in range(5 - i):
            if i + j < 4:
                sites.append(((i + 0.5) / 4, j / 4))
                sites.append((i / 4, (j + 0.5) / 4))
                sites.append(((i + 0.5) / 4, (j + 0.5) / 4))
    if mode == "random":
        r = rng.random(2)
        if r.sum() > 1:
            r = 1 - r
        return tuple(r)
    return sites[rng.integers(0, len(sites))]


def seed_t5_plus_one(n, rng, site=None, shrink=None):
    assert n == 16
    lat = tri_lattice(5)
    shrink = shrink if shrink is not None else rng.uniform(0.80, 0.98)
    # shrink the lattice towards the centroid, freeing an interior region
    c = lat.mean(axis=0)
    p = c + shrink * (lat - c)
    if site is None:
        site = _t5_sites(rng, "grid" if rng.random() < 0.8 else "random")
    extra = bary_to_xy(np.array([site[0]]), np.array([site[1]]))
    q = np.vstack([p, extra])
    amp = 10 ** rng.uniform(-3, -1.3)
    return clip_into_triangle(q + rng.normal(scale=amp, size=q.shape))


def seed_rotated_lattice(n, rng):
    """A hexagonal lattice at random spacing / rotation / offset, cropped to the triangle."""
    for _ in range(60):
        sp = rng.uniform(0.18, 0.30)
        th = rng.uniform(0, math.pi / 3)
        off = rng.random(2) * sp
        e1 = sp * np.array([math.cos(th), math.sin(th)])
        e2 = sp * np.array([math.cos(th + math.pi / 3), math.sin(th + math.pi / 3)])
        R = int(3 / sp) + 3
        idx = np.array([(i, j) for i in range(-R, R + 1) for j in range(-R, R + 1)])
        pts = off + idx[:, :1] * e1 + idx[:, 1:2] * e2
        y = pts[:, 1]
        inside = (y >= -1e-12) & (SQRT3 * pts[:, 0] - y >= -1e-12) & (SQRT3 * (1 - pts[:, 0]) - y >= -1e-12)
        pts = pts[inside]
        if len(pts) >= n:
            keep = rng.choice(len(pts), size=n, replace=False)
            return clip_into_triangle(pts[keep] + rng.normal(scale=0.01, size=(n, 2)))
    return sample_uniform(n, rng)


_ROW_PARTITIONS = None


def _row_partitions(n=16, maxrows=7):
    """All ways to write n as an ordered list of row counts, rows weakly decreasing bottom-up
    is *not* imposed -- the point of this family is row structures that are NOT the lattice's
    5,4,3,2,1 pattern."""
    global _ROW_PARTITIONS
    if _ROW_PARTITIONS is None:
        out = []

        def rec(rem, rows):
            if rem == 0 and 2 <= len(rows) <= maxrows:
                out.append(tuple(rows))
                return
            if rem <= 0 or len(rows) >= maxrows:
                return
            for c in range(1, min(rem, 7) + 1):
                rec(rem - c, rows + [c])

        rec(n, [])
        _ROW_PARTITIONS = out
    return _ROW_PARTITIONS


def seed_rows(n, rng):
    parts = _row_partitions(n)
    rows = parts[rng.integers(0, len(parts))]
    nr = len(rows)
    pts = []
    for r, cnt in enumerate(rows):
        # row r sits at height fraction t; width of the triangle there is (1 - t)
        t = r / max(nr - 1, 1) * rng.uniform(0.75, 1.0)
        width = 1.0 - t
        if cnt == 1:
            xs = [0.5 * width]
        else:
            xs = [width * i / (cnt - 1) for i in range(cnt)]
        for x in xs:
            pts.append((x + 0.0, t))
    a = np.array(pts)
    p = bary_to_xy(a[:, 0], a[:, 1])
    return clip_into_triangle(p + rng.normal(scale=0.02, size=p.shape))


def seed_symmetric(n, rng):
    """C_3 and mirror ansaetze, sampled *in addition to* the unconstrained families.

    Problem ``RULES.md`` SS5 forbids restricting the search to symmetric configurations and then
    reporting the result as optimal.  This does not restrict: it only makes symmetric starts
    reachable, since random seeding hits them with probability zero.  16 = 3*5 + 1 admits a C_3
    orbit decomposition with one fixed (centroid) point; a mirror ansatz splits as 2k + b with b
    points on the axis.
    """
    if rng.random() < 0.5:
        # C_3 with a centre point: 5 free orbits
        c = np.array([0.5, SQRT3 / 6.0])
        base = sample_uniform(5, rng) - c
        pts = [c]
        for k in range(3):
            th = 2 * math.pi * k / 3
            R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
            pts.extend(list(c + base @ R.T))
        p = np.array(pts)
    else:
        # mirror about the vertical axis x = 1/2
        b = int(rng.integers(0, 5)) * 2  # points on the axis, same parity as n
        b = b if (n - b) % 2 == 0 else b + 1
        k = (n - b) // 2
        free = sample_uniform(k, rng)
        free[:, 0] = 0.5 - np.abs(free[:, 0] - 0.5)
        mirrored = free.copy()
        mirrored[:, 0] = 1.0 - mirrored[:, 0]
        axis = np.stack([np.full(b, 0.5), rng.random(b) * (SQRT3 / 2)], axis=1)
        p = np.vstack([free, mirrored, axis]) if b else np.vstack([free, mirrored])
    return clip_into_triangle(p + rng.normal(scale=0.01, size=p.shape))


def perturb(p: np.ndarray, m: float, rng: np.random.Generator) -> np.ndarray:
    """Basin-hopping move.  Four flavours; the fourth (delete-and-reinsert at the emptiest site)
    is the move a plain shake is least likely to make."""
    n = len(p)
    q = p.copy()
    kind = rng.random()
    if kind < 0.35:
        k = 1 + int(rng.integers(0, max(1, n // 3)))
        idx = rng.choice(n, size=k, replace=False)
        q[idx] = sample_uniform(k, rng)
    elif kind < 0.6:
        d = np.linalg.norm(q[:, None, :] - q[None, :, :], axis=-1)
        d[np.arange(n), np.arange(n)] = np.inf
        loose = np.where(d.min(axis=1) > m * (1.0 + 1e-6))[0]
        if len(loose) == 0:
            loose = rng.choice(n, size=1)
        q[loose] = sample_uniform(len(loose), rng)
    elif kind < 0.82:
        q = q + rng.normal(scale=0.35 * m, size=q.shape)
    else:
        # delete one point, re-insert it at the emptiest site on a fine grid
        drop = int(rng.integers(0, n))
        rest = np.delete(q, drop, axis=0)
        cand = sample_uniform(400, rng)
        dd = np.linalg.norm(cand[:, None, :] - rest[None, :, :], axis=-1).min(axis=1)
        q = np.vstack([rest, cand[int(np.argmax(dd))][None, :]])
    return clip_into_triangle(q)


SEED_FAMILIES = {
    "uniform": seed_uniform,
    "lattice_defect": seed_lattice_defect,
    "t5_plus_one": seed_t5_plus_one,
    "rotated_lattice": seed_rotated_lattice,
    "rows": seed_rows,
    "symmetric": seed_symmetric,
}
