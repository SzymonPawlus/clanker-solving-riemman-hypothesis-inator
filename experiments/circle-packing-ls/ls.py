"""Lubachevsky-Stillinger billiard in an equilateral triangle.

STATUS: ``numerical``.  This module is a *generator*.  It proposes candidate
configurations; it proves nothing.  See ``README.md`` and
``problems/circle-packing-equilateral-triangle/RULES.md`` SS0-SS1.

FORMULATION
-----------
We work in the **point formulation** used by the rest of this repo, expressed on the
*unit* equilateral triangle

    T = conv{ (0,0), (1,0), (1/2, sqrt(3)/2) }.

The task is to place ``n`` points in T maximising the minimum pairwise distance ``m``.
Rescaling by ``2/m`` gives ``n`` points at pairwise distance ``>= 2`` in a triangle of
side ``D = 2/m``, hence an upper bound

    s(n) <= 2/m + 2*sqrt(3).

The Lubachevsky-Stillinger mapping is then: ``n`` point particles fly ballistically
inside T, reflecting specularly off the three edges, and carry a shared **exclusion
diameter** ``D(t)`` that grows at a constant rate ``gamma``.  Whenever two particles
reach separation exactly ``D(t)`` they collide elastically.  As ``D`` grows the system
jams, and ``D`` at jamming is a lower bound for the ``m`` this basin can reach.

Note the one place this differs from LS for *disks in a container*: here the particles
are points, so there is **no radius offset at the wall**.  A point may sit exactly on
an edge of T, and in every known optimum several do.  Getting this wrong (insetting the
walls by ``D/2``) silently solves a different problem.

COLLISION PREDICTION
--------------------
For a pair with separation ``dX = x_i - x_j`` and relative velocity ``dV = v_i - v_j``,
contact at time ``tau`` from now solves ``|dX + dV*tau| = D + gamma*tau``, i.e.

    A tau^2 + 2 B tau + C = 0,
    A = |dV|^2 - gamma^2,   B = dX.dV - D*gamma,   C = |dX|^2 - D^2.

We take the smallest positive root.  ``A`` may be negative (growth outruns the relative
speed); the stable-quadratic helper below handles that, and the linear case ``A ~ 0``.

For a wall with outward unit normal ``nk`` and offset ``ck`` (interior: ``nk.x <= ck``),
the crossing time is ``(ck - nk.x) / (nk.v)`` when ``nk.v > 0``.

COLLISION RESOLUTION
--------------------
Let ``u`` be the unit separation vector and ``g = dV.u`` the rate of change of ``|dX|``.
The *gap* is ``|dX| - D`` and closes at ``g - gamma``.  Elastic reflection off the
growing exclusion surface reverses the gap rate, so the new ``g'`` satisfies
``g' - gamma = -(g - gamma)``, i.e. ``g' = 2*gamma - g``.  Equal masses give

    v_i += (gamma - g) * u,      v_j -= (gamma - g) * u.

With ``gamma = 0`` this is the textbook elastic rule.  Energy is *injected* by the
growth, which is correct: the growing exclusion surface does work.  A thermostat
rescales velocities back to unit RMS speed periodically, which is what keeps the
dimensionless compression rate ``gamma / v_rms`` — the only parameter that actually
matters — under control.

WHY THERE IS NO EVENT QUEUE
---------------------------
Textbook LS keeps a priority queue of predicted events plus invalidation bookkeeping,
because it targets ``n`` in the thousands.  Here ``n <= 40``.  A full rescan of the
``C(n,2)`` pairs and ``3n`` wall candidates after every event costs ~700 vectorised
NumPy operations and removes the single largest source of bugs in LS implementations
(stale events surviving a collision).  It is still exactly event-driven: no time
stepping, no discretisation error in the trajectories.  This is a deliberate
correctness-over-throughput trade, and it is why this file is short enough to audit.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

SQRT3 = math.sqrt(3.0)

#: Vertices of the unit equilateral triangle, in the repo's canonical orientation.
VERTICES = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, SQRT3 / 2.0]])

#: Outward unit normals and offsets of the three edges; interior is ``n . x <= c``.
#: w0 = edge (0,0)-(1,0);  w1 = edge (0,0)-(1/2,sqrt3/2);  w2 = edge (1,0)-(1/2,sqrt3/2).
WALL_N = np.array(
    [
        [0.0, -1.0],
        [-SQRT3 / 2.0, 0.5],
        [SQRT3 / 2.0, 0.5],
    ]
)
WALL_C = np.array([0.0, 0.0, SQRT3 / 2.0])


# ----------------------------------------------------------------------------------- #
# geometry helpers
# ----------------------------------------------------------------------------------- #


def wall_slack(p: np.ndarray) -> np.ndarray:
    """Signed slack ``c_k - n_k . x`` for every point and wall; shape ``(n, 3)``.

    Non-negative on all three walls exactly when the point is in the closed triangle.
    Because the normals are unit vectors this is a true Euclidean distance to the edge
    line, which is what makes the epsilons below dimensionally meaningful.
    """
    return WALL_C[None, :] - p @ WALL_N.T


def inside(p: np.ndarray, tol: float = 0.0) -> bool:
    return bool((wall_slack(p) >= -tol).all())


def clip_into_triangle(p: np.ndarray) -> np.ndarray:
    """Project points into T by clamping barycentric coordinates and renormalising."""
    x, y = p[:, 0], p[:, 1]
    l2 = y / (SQRT3 / 2.0)
    l1 = x - y / SQRT3
    l0 = 1.0 - l1 - l2
    lam = np.clip(np.stack([l0, l1, l2], axis=1), 0.0, None)
    lam = lam / lam.sum(axis=1, keepdims=True)
    return lam @ VERTICES


def min_pair_distance(p: np.ndarray) -> float:
    n = len(p)
    if n < 2:
        return float("inf")
    d = np.linalg.norm(p[:, None, :] - p[None, :, :], axis=-1)
    d[np.arange(n), np.arange(n)] = np.inf
    return float(d.min())


def sample_uniform(n: int, rng: np.random.Generator) -> np.ndarray:
    """``n`` points uniform on T, via the folded-barycentric (reflected square) trick."""
    u = rng.random((n, 2))
    fold = u.sum(axis=1) > 1.0
    u[fold] = 1.0 - u[fold]
    return u[:, 0:1] * VERTICES[1] + u[:, 1:2] * VERTICES[2]


# ----------------------------------------------------------------------------------- #
# stable smallest-positive-root of  A t^2 + 2 B t + C = 0
# ----------------------------------------------------------------------------------- #


def smallest_positive_root(A, B, C, tiny: float = 1e-14):
    """Vectorised smallest strictly-positive root; ``inf`` where there is none.

    Written in the ``2B`` convention that the collision quadratic naturally produces, so
    the roots are ``(-B +- sqrt(B^2 - A C)) / A``.  The usual cancellation-avoiding form
    is used (compute the root that does not cancel, get the other from the product
    ``C/A``), because ``B^2 >> A C`` is the common case for a nearly-grazing pair and
    naive subtraction there loses most of the mantissa.

    ``A`` may be negative: growth outrunning the relative speed makes contact certain,
    and the quadratic then has one positive and one negative root.  ``A ~ 0`` degenerates
    to the linear equation ``2 B t + C = 0``.
    """
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    C = np.asarray(C, dtype=float)
    out = np.full(np.broadcast(A, B, C).shape, np.inf, dtype=float)

    lin = np.abs(A) <= tiny
    # linear branch: 2 B t + C = 0
    if lin.any():
        Bl, Cl = np.broadcast_to(B, out.shape)[lin], np.broadcast_to(C, out.shape)[lin]
        t = np.full(Bl.shape, np.inf)
        ok = np.abs(Bl) > 0.0
        t[ok] = -Cl[ok] / (2.0 * Bl[ok])
        t[~np.isfinite(t) | (t <= 0.0)] = np.inf
        out[lin] = t

    quad = ~lin
    if quad.any():
        Aq = np.broadcast_to(A, out.shape)[quad]
        Bq = np.broadcast_to(B, out.shape)[quad]
        Cq = np.broadcast_to(C, out.shape)[quad]
        disc = Bq * Bq - Aq * Cq
        t = np.full(Aq.shape, np.inf)
        real = disc >= 0.0
        if real.any():
            sq = np.sqrt(disc[real])
            Br, Ar, Cr = Bq[real], Aq[real], Cq[real]
            sgn = np.where(Br >= 0.0, 1.0, -1.0)
            q = -(Br + sgn * sq)
            r1 = np.where(np.abs(Ar) > 0.0, q / Ar, np.inf)
            r2 = np.where(np.abs(q) > 0.0, Cr / q, np.inf)
            r1 = np.where(r1 > 0.0, r1, np.inf)
            r2 = np.where(r2 > 0.0, r2, np.inf)
            t[real] = np.minimum(r1, r2)
        out[quad] = t

    out[~np.isfinite(out)] = np.inf
    return out


# ----------------------------------------------------------------------------------- #
# the simulation
# ----------------------------------------------------------------------------------- #


@dataclass
class LSResult:
    points: np.ndarray
    m: float  # measured min pairwise distance of ``points``
    d_jam: float  # exclusion diameter reached by the simulation
    events: int
    stages: list = field(default_factory=list)
    stop_reason: str = ""

    @property
    def s(self) -> float:
        """Upper-bound side length for unit circles implied by ``m`` (hypothesis only)."""
        return 2.0 / self.m + 2.0 * SQRT3


class Billiard:
    """One LS run.  Mutates in place; read ``X`` and ``D`` after ``run_stage``."""

    #: Distance below which a point counts as "on" a wall for the corner fixup.
    WALL_EPS = 1e-12
    #: A predicted event closer than this in time is treated as simultaneous with now.
    TIME_EPS = 1e-15

    def __init__(self, points: np.ndarray, rng: np.random.Generator):
        self.X = np.array(points, dtype=float)
        self.n = len(self.X)
        self.rng = rng
        self.V = rng.normal(size=self.X.shape)
        self.D = 0.0
        self.t = 0.0
        self.events = 0
        self.iu, self.ju = np.triu_indices(self.n, k=1)
        self._thermostat()

    # -- thermostat ------------------------------------------------------------------
    def _thermostat(self) -> None:
        """Rescale to unit RMS speed and remove any net drift.

        Growth injects energy at every collision, so without this the speeds diverge and
        the *dimensionless* compression rate ``gamma / v_rms`` silently falls to zero —
        the run would look like it was still annealing when it had actually frozen.
        Removing the mean velocity stops the whole cloud translating, which in a closed
        triangle is harmless but wastes events on the walls.
        """
        if self.n > 1:
            # With a single particle the mean IS the velocity, so removing it would stop
            # the particle dead and the rescale below would divide by zero.
            self.V -= self.V.mean(axis=0, keepdims=True)
        speed = math.sqrt(float((self.V**2).sum()) / self.n)
        if speed > 0.0:
            self.V /= speed
        else:  # pathological; re-seed
            self.V = self.rng.normal(size=self.X.shape)
            self._thermostat()

    # -- event prediction ------------------------------------------------------------
    def _next_pair_event(self, gamma: float):
        if self.n < 2:
            return math.inf, -1, -1
        dX = self.X[self.iu] - self.X[self.ju]
        dV = self.V[self.iu] - self.V[self.ju]
        A = (dV * dV).sum(axis=1) - gamma * gamma
        B = (dX * dV).sum(axis=1) - self.D * gamma
        C = (dX * dX).sum(axis=1) - self.D * self.D
        tau = smallest_positive_root(A, B, C)

        # A pair that is already at or inside contact (``C <= 0``) needs separate
        # handling, and getting this wrong deadlocks the whole simulation.  Note
        # ``d/dt (|dX|^2 - D^2) = 2B``, so ``B`` is the sign of "is the violation
        # getting worse".
        #
        #   * ``C <= 0`` and ``B < 0``  -- in contact and still closing: collide NOW.
        #   * ``C <= 0`` and ``B >= 0`` -- in contact but already separating: there is
        #     no event.  The quadratic's small root is negative in exact arithmetic, but
        #     with ``C`` at -1e-17 round-off flips it to a tiny *positive* number, so
        #     leaving it in makes the pair re-collide at ``tau ~ 1e-17`` every event.
        #     Simulated time then stops advancing, ``D`` freezes, and the run reports a
        #     confident "jammed" at a third of the density it should reach.  It looks
        #     like a physics result and it is a sign error.
        contact = C <= 0.0
        tau = np.where(contact, np.where(B < 0.0, 0.0, np.inf), tau)

        k = int(np.argmin(tau))
        return float(tau[k]), int(self.iu[k]), int(self.ju[k])

    def _next_wall_event(self):
        slack = wall_slack(self.X)  # (n, 3), >= 0 inside
        rate = self.V @ WALL_N.T  # (n, 3), > 0 means approaching that wall
        with np.errstate(divide="ignore", invalid="ignore"):
            tau = np.where(rate > 0.0, slack / rate, np.inf)
        tau = np.where(np.isfinite(tau), tau, np.inf)
        tau = np.where(tau < 0.0, 0.0, tau)  # drifted outside: reflect immediately
        k = int(np.argmin(tau))
        return float(tau.flat[k]), k // 3, k % 3

    # -- event resolution ------------------------------------------------------------
    def _resolve_pair(self, i: int, j: int, gamma: float) -> None:
        dX = self.X[i] - self.X[j]
        r = float(np.linalg.norm(dX))
        if r == 0.0:  # exactly coincident: push apart along a random direction
            u = self.rng.normal(size=2)
            u /= np.linalg.norm(u)
        else:
            u = dX / r
        g = float((self.V[i] - self.V[j]) @ u)
        if g >= gamma:
            # Already separating at least as fast as the exclusion surface grows: the
            # gap is opening, so there is nothing to resolve.  Applying the impulse here
            # would turn a separating pair back into an approaching one.
            return
        imp = (gamma - g) * u
        self.V[i] = self.V[i] + imp
        self.V[j] = self.V[j] - imp

    def _resolve_wall(self, i: int, k: int) -> None:
        """Specular reflection, then a corner fixup.

        The 60 degree corners are where this goes wrong: a particle can be on two edges
        at once, and reflecting off only one of them leaves it still flying outwards, so
        the next event has ``tau = 0`` and the run stalls burning events at a vertex.
        After the reflection we therefore re-reflect off any wall the particle is
        currently on *and* still moving into, up to three times (a corner of a triangle
        touches at most two edges, so two passes suffice; the third is slack).
        """
        nk = WALL_N[k]
        self.V[i] = self.V[i] - 2.0 * float(self.V[i] @ nk) * nk
        # Snap onto the edge line if we drifted outside it.  With slack
        # ``s = c_k - x.n_k`` the point ``x + s*n_k`` satisfies ``x'.n_k = c_k`` exactly,
        # so this is a projection onto the edge line along the normal.
        s = WALL_C[k] - float(self.X[i] @ nk)
        if s < 0.0:
            self.X[i] = self.X[i] + s * nk

        for _ in range(3):
            slack = WALL_C - self.X[i] @ WALL_N.T
            rate = self.V[i] @ WALL_N.T
            bad = (slack <= self.WALL_EPS) & (rate > 0.0)
            if not bad.any():
                break
            for kk in np.flatnonzero(bad):
                nkk = WALL_N[kk]
                self.V[i] = self.V[i] - 2.0 * float(self.V[i] @ nkk) * nkk

        # last-ditch containment: never let a point leave T
        slack = WALL_C - self.X[i] @ WALL_N.T
        if (slack < 0.0).any():
            self.X[i] = clip_into_triangle(self.X[i][None, :])[0]

    # -- driver ----------------------------------------------------------------------
    def run_stage(
        self,
        gamma: float,
        max_events: int,
        stall_window: int = 2000,
        stall_rel: float = 1e-10,
        thermostat_every: int = 200,
    ) -> tuple[str, int]:
        """Grow at rate ``gamma`` until the exclusion diameter stalls.

        Stalling, not a fixed event count, is the termination criterion: as the packing
        jams the collision rate diverges, so simulated time — and therefore ``D`` — stops
        advancing while events keep being processed.  We declare a jam when ``D`` gains
        less than ``stall_rel`` in relative terms over ``stall_window`` events.
        """
        start_events = self.events
        last_D = self.D
        since_check = 0
        reason = "max_events"
        zero_dt_run = 0

        while self.events - start_events < max_events:
            tp, i, j = self._next_pair_event(gamma)
            tw, wi, wk = self._next_wall_event()
            dt = min(tp, tw)
            if not math.isfinite(dt):
                reason = "no_event"
                break
            if dt < 0.0:
                dt = 0.0

            if dt <= self.TIME_EPS:
                zero_dt_run += 1
                if zero_dt_run > 50 * self.n:
                    # Degenerate cluster of simultaneous events. Re-randomise velocities
                    # rather than spin: the configuration is kept, only the dynamics is
                    # perturbed, so nothing about the candidate is invented here.
                    self.V = self.rng.normal(size=self.X.shape)
                    self._thermostat()
                    zero_dt_run = 0
            else:
                zero_dt_run = 0

            self.X = self.X + self.V * dt
            self.t += dt
            self.D += gamma * dt

            if tp <= tw:
                self._resolve_pair(i, j, gamma)
            else:
                self._resolve_wall(wi, wk)

            self.events += 1
            since_check += 1

            if self.events % thermostat_every == 0:
                self._thermostat()

            if since_check >= stall_window:
                gain = self.D - last_D
                if gain <= stall_rel * max(self.D, 1e-300):
                    reason = "jammed"
                    break
                last_D = self.D
                since_check = 0

        return reason, self.events - start_events


DEFAULT_STALL_WINDOW = 500
"""Events between stall checks.  A stage always costs at least two windows, so this is
also the floor on the price of a stage; 500 was the smallest value at which the
quality-per-second measurement in ``README.md`` stopped improving."""

DEFAULT_SCHEDULE: tuple[float, ...] = (5e-2, 5e-3)
"""Compression rates, run in order.  Each is *dimensionless* because the thermostat pins
``v_rms = 1``, so ``gamma`` is growth per unit of typical travel.  Fast first to reach a
dense basin cheaply, then a slower pass to let the jammed structure relax — the
compression-rate annealing Graham-Lubachevsky describe.

Chosen by the measurement in ``README.md``: longer schedules give a slightly better
packing *per run* but fewer runs per second, and at a fixed wall clock the extra basin
coverage wins.  This is a throughput choice, not a physics one."""


def ls_run(
    n: int,
    rng: np.random.Generator,
    schedule: tuple[float, ...] = DEFAULT_SCHEDULE,
    max_events_per_stage: int = 60_000,
    start: np.ndarray | None = None,
    stall_window: int = DEFAULT_STALL_WINDOW,
    stall_rel: float = 1e-9,
) -> LSResult:
    """One complete LS run: random start, annealed growth, return the jammed packing."""
    p0 = sample_uniform(n, rng) if start is None else np.array(start, dtype=float)
    sim = Billiard(p0, rng)
    stages = []
    for gamma in schedule:
        reason, used = sim.run_stage(
            gamma,
            max_events=max_events_per_stage,
            stall_window=stall_window,
            stall_rel=stall_rel,
        )
        stages.append({"gamma": gamma, "events": used, "stop": reason, "D": sim.D})

    pts = clip_into_triangle(sim.X)
    return LSResult(
        points=pts,
        m=min_pair_distance(pts),
        d_jam=sim.D,
        events=sim.events,
        stages=stages,
        stop_reason=stages[-1]["stop"] if stages else "no_stage",
    )
