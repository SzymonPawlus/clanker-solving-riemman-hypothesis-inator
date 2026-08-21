"""Counterexample hunt for the Erdos-Oler conjecture, k >= 7.

Status of everything this module produces: ``numerical`` (problem ``RULES.md`` SS1). A float
configuration is a *hypothesis*. Nothing here certifies anything; ``exact_check.py`` is the gate.

Normalisation (separation 1)
----------------------------
Place ``n`` points in the unit equilateral triangle

    T = conv{ (0,0), (1,0), (1/2, sqrt(3)/2) }

maximising the minimum pairwise distance ``m``. Rescaling by ``1/m`` gives ``n`` points at
pairwise distance >= 1 in a triangle of side ``a = 1/m``. With ``Delta(k) = k(k+1)/2``:

    Erdos-Oler(k) is FALSE  <=>  m(Delta(k) - 1) > 1/(k-1).

The repo's certificate convention uses separation 2 and side ``d = 2a``; conversion is
``d = 2/m`` and ``s = d + 2*sqrt(3)``. Every number produced here is in the separation-1
``(a, m)`` normalisation.

Provenance
----------
The SLSQP local step is the same formulation used by ``experiments/circle-packing-search``
(issue #9, author ``claude``): maximise ``m`` over ``(p, m)`` subject to
``|p_i - p_j|^2 >= m^2`` and the three half-plane containments, with analytic Jacobians, and
re-measure the achieved ``m`` after projecting into ``T`` rather than trusting the solver's own
``m``. That convention is copied deliberately -- trusting the solver's ``m`` is how a fake record
is born. The seeding families, the local-optimum census and the whole counterexample-hunt driver
are new here.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

SQRT3 = math.sqrt(3.0)
HALF_SQRT3 = SQRT3 / 2.0
VERTICES = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, HALF_SQRT3]])


def tri(k: int) -> int:
    return k * (k + 1) // 2


# ---------------------------------------------------------------------------------------------
# geometry
# ---------------------------------------------------------------------------------------------


def clip_into_triangle(p: np.ndarray) -> np.ndarray:
    """Project into T by clamping barycentric coordinates and renormalising.

    The output is a convex combination of the vertices, hence *exactly* inside T up to the
    rounding of one matrix product. Points are therefore contained by construction and the only
    thing left to measure is the separation."""
    x, y = p[:, 0], p[:, 1]
    l2 = y / HALF_SQRT3
    l1 = x - y / SQRT3
    l0 = 1.0 - l1 - l2
    lam = np.clip(np.stack([l0, l1, l2], axis=1), 0.0, None)
    s = lam.sum(axis=1, keepdims=True)
    s[s == 0.0] = 1.0
    lam = lam / s
    return lam @ VERTICES


def min_pair_distance(p: np.ndarray) -> float:
    n = len(p)
    if n < 2:
        return float("inf")
    d = np.linalg.norm(p[:, None, :] - p[None, :, :], axis=-1)
    d[np.arange(n), np.arange(n)] = np.inf
    return float(d.min())


def inside_mask(p: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    return (
        (p[:, 1] >= -tol)
        & (SQRT3 * p[:, 0] - p[:, 1] >= -tol)
        & (SQRT3 * (1.0 - p[:, 0]) - p[:, 1] >= -tol)
    )


def containment_slack(p: np.ndarray) -> float:
    return float(
        min(
            p[:, 1].min(),
            (SQRT3 * p[:, 0] - p[:, 1]).min() / 2.0,
            (SQRT3 * (1.0 - p[:, 0]) - p[:, 1]).min() / 2.0,
        )
    )


def corner_counts(p: np.ndarray, m: float, jmax: int = 5) -> list[list[int]]:
    """Occupancy of the three corner sub-triangles at integer scales, in separation-1 units.

    Rescaled by 1/m the configuration sits in a triangle of side a = 1/m at separation 1. The
    closed corner triangle of side j at vertex V is {barycentric coordinate of V >= 1 - j/a}.
    Returns ``[[count at j=1..jmax] for each of A, B, C]``.

    This is the diagnostic for the necessary conditions on a k = 7 counterexample recorded in
    ``attacks/eo-hull-deficit`` SS9 (status ``sketch`` there, so used here only as a *search
    heuristic and reporting statistic*, never as an assumption)."""
    a = 1.0 / m if m > 0 else float("inf")
    x, y = p[:, 0], p[:, 1]
    l2 = y / HALF_SQRT3
    l1 = x - y / SQRT3
    l0 = 1.0 - l1 - l2
    lam = [l0, l1, l2]
    out = []
    for v in range(3):
        row = []
        for j in range(1, jmax + 1):
            row.append(int(np.sum(lam[v] >= 1.0 - j / a - 1e-12)))
        out.append(row)
    return out


# ---------------------------------------------------------------------------------------------
# local solve
# ---------------------------------------------------------------------------------------------


def _pair_index(n: int):
    iu = np.triu_indices(n, k=1)
    return iu[0], iu[1]


_PAIR_CACHE: dict[int, tuple[np.ndarray, np.ndarray]] = {}


def local_solve(p0: np.ndarray, maxiter: int = 250, ftol: float = 1e-14):
    n = len(p0)
    if n not in _PAIR_CACHE:
        _PAIR_CACHE[n] = _pair_index(n)
    ii, jj = _PAIR_CACHE[n]
    npair = len(ii)

    m0 = min_pair_distance(p0)
    if not math.isfinite(m0) or m0 <= 0:
        m0 = 1e-3
    z0 = np.concatenate([p0.ravel(), [m0]])

    def neg_m(z):
        return -z[-1]

    def neg_m_grad(z):
        g = np.zeros_like(z)
        g[-1] = -1.0
        return g

    def cons_f(z):
        p = z[:-1].reshape(n, 2)
        m = z[-1]
        diff = p[ii] - p[jj]
        pair = np.einsum("ij,ij->i", diff, diff) - m * m
        return np.concatenate(
            [pair, p[:, 1], SQRT3 * p[:, 0] - p[:, 1], SQRT3 * (1.0 - p[:, 0]) - p[:, 1]]
        )

    def cons_jac(z):
        p = z[:-1].reshape(n, 2)
        m = z[-1]
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
    p = clip_into_triangle(res.x[:-1].reshape(n, 2))
    return p, min_pair_distance(p)


def polish(p: np.ndarray, rounds: int = 3, maxiter: int = 250):
    """Warm-restart the local solve from its own output; buys the last several digits."""
    best_p, best_m = p, min_pair_distance(p)
    for _ in range(rounds):
        q, mq = local_solve(best_p, maxiter=maxiter)
        if mq > best_m:
            best_p, best_m = q, mq
        else:
            break
    return best_p, best_m


# ---------------------------------------------------------------------------------------------
# seed families
# ---------------------------------------------------------------------------------------------


def seed_uniform(n: int, rng) -> np.ndarray:
    r = rng.random((n, 2))
    fold = r.sum(axis=1) > 1.0
    r[fold] = 1.0 - r[fold]
    return r @ (VERTICES[1:] - VERTICES[0]) + VERTICES[0]


def _full_lattice(k: int) -> np.ndarray:
    """The T(k) triangular lattice inscribed in the unit triangle (spacing 1/(k-1))."""
    pts = []
    for row in range(k):
        for col in range(row + 1):
            a = row / (k - 1) if k > 1 else 0.0
            b = col / (k - 1) if k > 1 else 0.0
            pts.append((1 - a) * VERTICES[0] + (a - b) * VERTICES[1] + b * VERTICES[2])
    return np.array(pts)


def seed_lattice_defect(n: int, k: int, rng, jitter_scale: float | None = None) -> np.ndarray:
    """T(k) lattice minus (T(k) - n) points, jittered. The incumbent's own basin, and its
    neighbourhood at a range of jitter amplitudes."""
    pts = _full_lattice(k)
    keep = rng.choice(len(pts), size=n, replace=False)
    pts = pts[keep]
    if jitter_scale is None:
        jitter_scale = 10.0 ** rng.uniform(-2.5, -0.5)
    pts = pts + rng.normal(scale=jitter_scale / max(k - 1, 1), size=pts.shape)
    return clip_into_triangle(pts)


def seed_rotated_lattice(n: int, k: int, rng) -> np.ndarray:
    """A hexagonal lattice at a random spacing/rotation/offset, cropped to T.

    This is the structured competitor that a purely random multi-start is worst at finding:
    several known optimal packings in a triangle are rotated or shifted lattice fragments
    (n = 13, 26, ...), so if the T(k)-1 lattice is beatable at all, a differently oriented
    lattice fragment is the most likely shape of the beater."""
    base = 1.0 / (k - 1)
    s = base * rng.uniform(0.92, 1.20)
    th = rng.uniform(0.0, math.pi / 3.0)
    c, sn = math.cos(th), math.sin(th)
    R = np.array([[c, -sn], [sn, c]])
    off = seed_uniform(1, rng)[0]
    rad = int(math.ceil(2.5 / s)) + 2
    ij = np.array([(i, j) for i in range(-rad, rad + 1) for j in range(-rad, rad + 1)])
    v = s * np.stack([ij[:, 0] + 0.5 * ij[:, 1], HALF_SQRT3 * ij[:, 1]], axis=1)
    q = v @ R.T + off
    q = q[inside_mask(q, tol=1e-9)]
    if len(q) >= n:
        idx = rng.choice(len(q), size=n, replace=False)
        return q[idx]
    extra = seed_uniform(n - len(q), rng)
    return np.vstack([q, extra]) if len(q) else extra


def seed_rows(n: int, k: int, rng) -> np.ndarray:
    """A random row structure: r horizontal rows of equally spaced points at random heights.

    Many optimal triangle packings are row structures with row counts that are *not* the lattice's
    k, k-1, ..., 1 -- this family samples that combinatorial space directly."""
    r = int(rng.integers(max(2, k - 3), k + 3))
    counts = np.ones(r, dtype=int)
    left = n - r
    if left < 0:
        return seed_uniform(n, rng)
    w = rng.random(r)
    w = w / w.sum()
    add = np.floor(w * left).astype(int)
    counts = counts + add
    while counts.sum() < n:
        counts[rng.integers(0, r)] += 1
    ys = np.sort(rng.random(r)) * HALF_SQRT3
    if rng.random() < 0.5:
        ys = np.linspace(0.0, HALF_SQRT3 * rng.uniform(0.85, 1.0), r)
    pts = []
    for y, cnt in zip(ys, counts):
        xlo = y / SQRT3
        xhi = 1.0 - y / SQRT3
        if cnt == 1:
            xs = np.array([0.5 * (xlo + xhi)])
        else:
            xs = np.linspace(xlo, xhi, cnt)
        jit = rng.normal(scale=0.02 / (k - 1), size=(cnt, 2))
        pts.append(np.stack([xs, np.full(cnt, y)], axis=1) + jit)
    p = np.vstack(pts)
    if len(p) > n:
        p = p[rng.choice(len(p), size=n, replace=False)]
    elif len(p) < n:
        p = np.vstack([p, seed_uniform(n - len(p), rng)])
    return clip_into_triangle(p)


def seed_corner_dense(n: int, k: int, rng) -> np.ndarray:
    """Force lattice-density at all three corners, randomise the interior.

    ``attacks/eo-hull-deficit`` SS9 (status ``sketch``) records that a k = 7 counterexample must
    have, at every corner V and every integer j <= 5, at least T(j) points inside the open corner
    triangle of side j. Whatever the status of that derivation, it is a legitimate place to *look*:
    this seed pins the three corner clusters of the lattice at scale ``jc`` and scatters the rest.
    """
    jc = int(rng.integers(2, min(4, k - 2) + 1))
    lat = _full_lattice(k)
    x, y = lat[:, 0], lat[:, 1]
    l2 = y / HALF_SQRT3
    l1 = x - y / SQRT3
    l0 = 1.0 - l1 - l2
    lam = np.stack([l0, l1, l2], axis=1)
    thr = 1.0 - jc / (k - 1) - 1e-9
    sel = (lam >= thr).any(axis=1)
    cluster = lat[sel]
    if len(cluster) > n:
        cluster = cluster[rng.choice(len(cluster), size=n, replace=False)]
    rest = n - len(cluster)
    pts = cluster + rng.normal(scale=0.05 / (k - 1), size=cluster.shape)
    if rest > 0:
        pts = np.vstack([pts, seed_uniform(rest, rng)])
    return clip_into_triangle(pts)


SEED_FAMILIES = ("uniform", "lattice_defect", "rotated_lattice", "rows", "corner_dense")


def make_seed(family: str, n: int, k: int, rng) -> np.ndarray:
    if family == "uniform":
        return seed_uniform(n, rng)
    if family == "lattice_defect":
        return seed_lattice_defect(n, k, rng)
    if family == "rotated_lattice":
        return seed_rotated_lattice(n, k, rng)
    if family == "rows":
        return seed_rows(n, k, rng)
    if family == "corner_dense":
        return seed_corner_dense(n, k, rng)
    raise ValueError(family)


# ---------------------------------------------------------------------------------------------
# basin-hopping moves
# ---------------------------------------------------------------------------------------------


def perturb(p: np.ndarray, m: float, rng) -> np.ndarray:
    n = len(p)
    q = p.copy()
    kind = rng.random()
    if kind < 0.35:
        c = 1 + rng.integers(0, max(1, n // 3))
        idx = rng.choice(n, size=int(c), replace=False)
        q[idx] = seed_uniform(int(c), rng)
    elif kind < 0.60:
        d = np.linalg.norm(q[:, None, :] - q[None, :, :], axis=-1)
        d[np.arange(n), np.arange(n)] = np.inf
        loose = np.where(d.min(axis=1) > m * (1.0 + 1e-6))[0]
        if len(loose) == 0:
            loose = rng.choice(n, size=1)
        q[loose] = seed_uniform(len(loose), rng)
    elif kind < 0.80:
        q = q + rng.normal(scale=rng.uniform(0.05, 0.5) * m, size=q.shape)
    else:
        # swap-and-slide: take one point out and re-insert it at the emptiest spot found by
        # sampling. Targeted at "which point do you delete from the lattice" -- the exact degree
        # of freedom Erdos-Oler is about.
        i = int(rng.integers(0, n))
        cand = seed_uniform(64, rng)
        others = np.delete(q, i, axis=0)
        d = np.linalg.norm(cand[:, None, :] - others[None, :, :], axis=-1).min(axis=1)
        q[i] = cand[int(np.argmax(d))]
    return clip_into_triangle(q)


# ---------------------------------------------------------------------------------------------
# census
# ---------------------------------------------------------------------------------------------


@dataclass
class Census:
    """Histogram of local-optimum values. The point of the hunt is not only the best value but
    the *shape of the top of the landscape*: how many distinct near-optimal basins there are and
    how far below the lattice value the runner-up sits."""

    n: int
    k: int
    threshold: float
    counts: dict = None
    best_m: float = -1.0
    best_p: np.ndarray = None
    solves: int = 0
    by_family: dict = None
    hits_threshold: int = 0
    over_threshold: list = None
    runner_up: float = -1.0
    runner_up_p: np.ndarray = None

    def __post_init__(self):
        if self.counts is None:
            self.counts = {}
        if self.by_family is None:
            self.by_family = {}
        if self.over_threshold is None:
            self.over_threshold = []

    def offer(self, p, m, family):
        if not math.isfinite(m) or m <= 0.0:
            return
        self.solves += 1
        key = round(m, 9)
        self.counts[key] = self.counts.get(key, 0) + 1
        fam = self.by_family.setdefault(family, {"solves": 0, "best": -1.0, "hits": 0})
        fam["solves"] += 1
        if m > fam["best"]:
            fam["best"] = m
        if m > self.threshold - 1e-9:
            self.hits_threshold += 1
            fam["hits"] += 1
        if m > self.threshold + 1e-9:
            self.over_threshold.append((m, p.copy(), family))
        if m > self.best_m:
            self.best_m, self.best_p = m, p.copy()
        # runner-up = best local optimum strictly below the lattice threshold
        if m < self.threshold - 1e-9 and m > self.runner_up:
            self.runner_up, self.runner_up_p = m, p.copy()
