"""Search for dense packings of n equal circles in an equilateral triangle.

Everything this module produces is a **construction hypothesis** with status ``numerical``
(see ``problems/circle-packing-equilateral-triangle/RULES.md`` SS1). It is floating point; it is
not a proof of anything, and in particular a converged configuration is a *best found*
configuration, never "the optimum".

Formulation
-----------
Work in the point formulation. Fix the unit equilateral triangle

    T = conv{ (0, 0), (1, 0), (1/2, sqrt(3)/2) }

and place n points in T maximising the minimum pairwise distance m. Rescaling by 2/m turns this
into n points at pairwise distance >= 2 in a triangle of side D = 2/m, i.e. n unit circles in an
equilateral triangle of side s = D + 2*sqrt(3). Maximising m therefore minimises s.

The NLP solved at each local step, over variables (p_0, ..., p_{n-1}, m) in R^{2n+1}:

    maximise    m
    subject to  |p_i - p_j|^2 - m^2 >= 0            for all i < j
                y_i                 >= 0            (bottom edge)
                sqrt(3) x_i - y_i   >= 0            (left edge)
                sqrt(3)(1 - x_i) - y_i >= 0         (right edge)

This is nonconvex, so a local solve is only ever a local optimum; the global search on top is
multi-start plus basin hopping.

Why this method
---------------
``RULES.md`` SS5 of the problem directory points at Lubachevsky-Stillinger billiard simulation as
the standard generator. LS is an event-driven molecular-dynamics code: it produces excellent
*basins* but terminates at the collision-resolution tolerance, not at machine precision, so it
still needs a polish stage. The formulation above is that polish stage, and it turns out to be a
serviceable generator on its own at these sizes (n <= 34 is 561 pair constraints, milliseconds
per solve). We therefore use random multi-start + basin hopping to explore basins and SLSQP to
descend them, which is the "random restarts plus local perturbation" workhorse the same section
names. No symmetry is imposed at any point -- several known optima are asymmetric.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import minimize

SQRT3 = math.sqrt(3.0)
VERTICES = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, SQRT3 / 2.0]])


# --------------------------------------------------------------------------------------------
# geometry helpers
# --------------------------------------------------------------------------------------------


def sample_uniform(n: int, rng: np.random.Generator) -> np.ndarray:
    """n points uniform on the unit equilateral triangle, via the folded-barycentric trick."""
    r = rng.random((n, 2))
    fold = r.sum(axis=1) > 1.0
    r[fold] = 1.0 - r[fold]
    return r @ (VERTICES[1:] - VERTICES[0]) + VERTICES[0]


def sample_lattice(n: int, rng: np.random.Generator) -> np.ndarray:
    """A perturbed subset of a k-row triangular lattice, k the smallest row count with T(k) >= n.

    Triangular-lattice starts are a *prior*, not a constraint: they are mixed in with uniform
    starts and are always jittered, so the optimiser is free to walk away from the symmetry.
    """
    k = 1
    while k * (k + 1) // 2 < n:
        k += 1
    pts = []
    for row in range(k):
        for col in range(row + 1):
            a = row / (k - 1) if k > 1 else 0.0
            b = col / (k - 1) if k > 1 else 0.0
            # barycentric (1-a, a-b, b) over the three vertices
            pts.append((1 - a) * VERTICES[0] + (a - b) * VERTICES[1] + b * VERTICES[2])
    pts = np.array(pts)
    keep = rng.choice(len(pts), size=n, replace=False)
    pts = pts[keep]
    jitter = 0.25 / max(k - 1, 1)
    pts = pts + rng.normal(scale=jitter, size=pts.shape)
    return clip_into_triangle(pts)


def clip_into_triangle(p: np.ndarray) -> np.ndarray:
    """Project points back inside T by clamping barycentric coordinates. Cheap and good enough:
    SLSQP enforces containment properly, this only keeps the *start* feasible."""
    x, y = p[:, 0], p[:, 1]
    # barycentric wrt (v0, v1, v2)
    l2 = y / (SQRT3 / 2.0)
    l1 = x - y / SQRT3
    l0 = 1.0 - l1 - l2
    lam = np.clip(np.stack([l0, l1, l2], axis=1), 0.0, None)
    lam /= lam.sum(axis=1, keepdims=True)
    return lam @ VERTICES


def min_pair_distance(p: np.ndarray) -> float:
    n = len(p)
    if n < 2:
        return float("inf")
    d = np.linalg.norm(p[:, None, :] - p[None, :, :], axis=-1)
    d[np.arange(n), np.arange(n)] = np.inf
    return float(d.min())


def containment_slack(p: np.ndarray) -> float:
    """Smallest signed distance-like slack to the three edges; negative means outside."""
    return float(
        min(
            p[:, 1].min(),
            (SQRT3 * p[:, 0] - p[:, 1]).min() / 2.0,
            (SQRT3 * (1.0 - p[:, 0]) - p[:, 1]).min() / 2.0,
        )
    )


# --------------------------------------------------------------------------------------------
# local solve
# --------------------------------------------------------------------------------------------


def _pair_index(n: int) -> tuple[np.ndarray, np.ndarray]:
    iu = np.triu_indices(n, k=1)
    return iu[0], iu[1]


def local_solve(p0: np.ndarray, maxiter: int = 300, ftol: float = 1e-14) -> tuple[np.ndarray, float]:
    """One SLSQP descent from ``p0``. Returns (points, min pairwise distance)."""
    n = len(p0)
    ii, jj = _pair_index(n)
    npair = len(ii)

    m0 = min_pair_distance(p0)
    if not math.isfinite(m0):
        m0 = 1.0
    z0 = np.concatenate([p0.ravel(), [max(m0, 1e-6)]])

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
        bottom = p[:, 1]
        left = SQRT3 * p[:, 0] - p[:, 1]
        right = SQRT3 * (1.0 - p[:, 0]) - p[:, 1]
        return np.concatenate([pair, bottom, left, right])

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
    # Report the *achieved* minimum distance, not the solver's m: SLSQP is allowed to sit a
    # hair outside the feasible set, and trusting its m is exactly how a fake record is born.
    p = clip_into_triangle(p)
    return p, min_pair_distance(p)


# --------------------------------------------------------------------------------------------
# global search
# --------------------------------------------------------------------------------------------


@dataclass
class SearchResult:
    n: int
    m: float
    points: np.ndarray
    seed: int
    restarts: int
    hops: int
    elapsed: float
    history: list[tuple[float, float]] = field(default_factory=list)  # (elapsed, m)

    @property
    def s(self) -> float:
        return 2.0 / self.m + 2.0 * SQRT3

    @property
    def d_side(self) -> float:
        return 2.0 / self.m


def search(
    n: int,
    seed: int,
    time_budget: float = 10.0,
    restarts: int = 200,
    hop_batch: int = 40,
    lattice_fraction: float = 0.35,
    maxiter: int = 300,
    on_improve=None,
) -> SearchResult:
    """Multi-start SLSQP with basin hopping. Deterministic given ``seed`` and the iteration
    caps; ``time_budget`` (seconds) can cut a run short, which makes wall-clock-limited runs
    *not* reproducible -- so pass a generous budget when reproducibility matters."""
    rng = np.random.default_rng(seed)
    t0 = time.perf_counter()

    best_p: np.ndarray | None = None
    best_m = -1.0
    history: list[tuple[float, float]] = []
    n_restarts = 0
    n_hops = 0

    def offer(p: np.ndarray, m: float) -> bool:
        nonlocal best_p, best_m
        # SLSQP can fail outright and hand back coincident points (m == 0) or NaN. Such a
        # "solution" must never become the incumbent: m == 0 divides by zero downstream, and
        # NaN silently poisons every later comparison (NaN > x is False, so it would instead
        # freeze the search on whatever came before it).
        if not math.isfinite(m) or m <= 0.0:
            return False
        if m > best_m:
            best_m, best_p = m, p.copy()
            history.append((time.perf_counter() - t0, m))
            if on_improve is not None:
                on_improve(best_m, best_p)
            return True
        return False

    # ---- stage 1: multi-start ----------------------------------------------------------
    for _ in range(restarts):
        if time.perf_counter() - t0 > time_budget * 0.5:
            break
        n_restarts += 1
        p0 = sample_lattice(n, rng) if rng.random() < lattice_fraction else sample_uniform(n, rng)
        p, m = local_solve(p0, maxiter=maxiter)
        offer(p, m)

    while best_p is None:  # pathological: every restart degenerate or the budget was zero
        p0 = sample_uniform(n, rng)
        p, m = local_solve(p0, maxiter=maxiter)
        offer(p, m)

    # ---- stage 2: basin hopping on the incumbent ---------------------------------------
    while time.perf_counter() - t0 < time_budget:
        for _ in range(hop_batch):
            if time.perf_counter() - t0 > time_budget:
                break
            n_hops += 1
            p0 = _perturb(best_p, best_m, rng)
            p, m = local_solve(p0, maxiter=maxiter)
            offer(p, m)

    return SearchResult(
        n=n,
        m=best_m,
        points=best_p,
        seed=seed,
        restarts=n_restarts,
        hops=n_hops,
        elapsed=time.perf_counter() - t0,
        history=history,
    )


def _perturb(p: np.ndarray, m: float, rng: np.random.Generator) -> np.ndarray:
    """One basin-hopping move. Three flavours, chosen at random:

    * **teleport**  -- move a random subset to fresh uniform positions;
    * **rattler kick** -- relocate the points that are *not* tight (their nearest neighbour is
      strictly further than m). Rattlers are legitimate and we do not "fix" them in the output,
      but they are free variables, so re-rolling them is a cheap way to sample a new basin;
    * **shake**     -- Gaussian jitter on everything.
    """
    n = len(p)
    q = p.copy()
    kind = rng.random()
    if kind < 0.45:
        k = 1 + rng.integers(0, max(1, n // 3))
        idx = rng.choice(n, size=int(k), replace=False)
        q[idx] = sample_uniform(int(k), rng)
    elif kind < 0.75:
        d = np.linalg.norm(q[:, None, :] - q[None, :, :], axis=-1)
        d[np.arange(n), np.arange(n)] = np.inf
        loose = np.where(d.min(axis=1) > m * (1.0 + 1e-6))[0]
        if len(loose) == 0:
            loose = rng.choice(n, size=1)
        q[loose] = sample_uniform(len(loose), rng)
    else:
        q = q + rng.normal(scale=0.35 * m, size=q.shape)
    return clip_into_triangle(q)
