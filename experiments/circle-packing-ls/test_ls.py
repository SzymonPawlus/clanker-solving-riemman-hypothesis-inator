"""Tests for the LS billiard.

The order here is deliberate and mirrors the advice in the issue: **the walls are tested
in isolation, before growth is coupled to them.**  Reflection off three edges meeting at
60 degrees is where triangle billiards go wrong, and a wall bug that only shows up as
"the packing is a bit worse than it should be" is invisible.

Run with ``uv run pytest -q`` (or ``python -m pytest -q``).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

import ls
from certificate import build_certificate, exact_feasible

SQRT3 = math.sqrt(3.0)


# ===================================================================================== #
# 1. Geometry primitives
# ===================================================================================== #


def test_vertices_are_on_all_the_walls_they_should_be():
    slack = ls.wall_slack(ls.VERTICES)
    assert slack.shape == (3, 3)
    # every vertex is in the closed triangle
    assert (slack >= -1e-15).all()
    # A=(0,0) is on walls 0 and 1; B=(1,0) on 0 and 2; C on 1 and 2.
    on = np.abs(slack) < 1e-15
    assert list(np.flatnonzero(on[0])) == [0, 1]
    assert list(np.flatnonzero(on[1])) == [0, 2]
    assert list(np.flatnonzero(on[2])) == [1, 2]


def test_wall_normals_are_unit_and_outward():
    assert np.allclose(np.linalg.norm(ls.WALL_N, axis=1), 1.0)
    centroid = ls.VERTICES.mean(axis=0)
    # centroid is strictly interior on all three
    assert (ls.wall_slack(centroid[None, :]) > 0.1).all()


def test_uniform_sample_lands_inside():
    rng = np.random.default_rng(0)
    p = ls.sample_uniform(500, rng)
    assert ls.inside(p, tol=1e-15)


# ===================================================================================== #
# 2. Wall reflection, in isolation (gamma = 0, n = 1: no growth, no pairs)
# ===================================================================================== #


def _single_particle(x, v, seed=0):
    rng = np.random.default_rng(seed)
    sim = ls.Billiard(np.array([x], dtype=float), rng)
    sim.V = np.array([v], dtype=float)  # overwrite the thermostatted random velocity
    return sim


def test_wall_event_time_and_reflection_bottom_edge():
    sim = _single_particle([0.5, 0.5], [0.0, -1.0])
    tau, i, k = sim._next_wall_event()
    assert i == 0 and k == 0
    assert tau == pytest.approx(0.5, abs=1e-15)
    sim.X = sim.X + sim.V * tau
    sim._resolve_wall(0, 0)
    assert sim.V[0] == pytest.approx([0.0, 1.0], abs=1e-15)


def test_wall_event_time_and_reflection_left_edge():
    # Head straight at the left edge along its outward normal.
    n1 = ls.WALL_N[1]
    x = np.array([0.5, 0.2])
    sim = _single_particle(x, n1)
    tau, i, k = sim._next_wall_event()
    assert k == 1
    expected = float(ls.WALL_C[1] - x @ n1)  # normals are unit, so slack == distance
    assert tau == pytest.approx(expected, rel=1e-13)
    sim.X = sim.X + sim.V * tau
    sim._resolve_wall(0, 1)
    assert sim.V[0] == pytest.approx(-n1, abs=1e-13)


def test_wall_event_time_and_reflection_right_edge():
    n2 = ls.WALL_N[2]
    x = np.array([0.5, 0.2])
    sim = _single_particle(x, n2)
    tau, i, k = sim._next_wall_event()
    assert k == 2
    assert tau == pytest.approx(float(ls.WALL_C[2] - x @ n2), rel=1e-13)
    sim.X = sim.X + sim.V * tau
    sim._resolve_wall(0, 2)
    assert sim.V[0] == pytest.approx(-n2, abs=1e-13)


def test_reflection_preserves_speed_and_tangential_component():
    rng = np.random.default_rng(7)
    for _ in range(200):
        k = int(rng.integers(3))
        n = ls.WALL_N[k]
        t = np.array([-n[1], n[0]])
        x = ls.sample_uniform(1, rng)[0]
        v = rng.normal(size=2)
        if v @ n <= 0:
            v = -v
        sim = _single_particle(x, v)
        tau, _, kk = sim._next_wall_event()
        sim.X = sim.X + sim.V * tau
        sim._resolve_wall(0, kk)
        nn = ls.WALL_N[kk]
        tt = np.array([-nn[1], nn[0]])
        assert np.linalg.norm(sim.V[0]) == pytest.approx(np.linalg.norm(v), rel=1e-13)
        assert sim.V[0] @ tt == pytest.approx(v @ tt, rel=1e-11, abs=1e-13)
        assert sim.V[0] @ nn == pytest.approx(-(v @ nn), rel=1e-11, abs=1e-13)


def test_billiard_stays_inside_over_a_long_wall_only_run():
    """No growth, no pairs: a pure triangle billiard must never leave the triangle."""
    rng = np.random.default_rng(11)
    sim = ls.Billiard(ls.sample_uniform(1, rng), rng)
    sim.run_stage(gamma=0.0, max_events=20_000, stall_window=10**9)
    assert sim.events >= 5_000, "wall-only run produced suspiciously few events"
    assert ls.inside(sim.X, tol=1e-12)
    assert np.linalg.norm(sim.V[0]) == pytest.approx(1.0, rel=1e-9)


def test_wall_only_billiard_is_time_reversible():
    """The strongest wall test available: billiards are reversible.

    Run forward, flip the velocity, run the same number of events again; a correct
    specular reflection returns the particle to where it started.  A wrong normal, a
    wrong offset, or a mishandled corner all break this immediately, and unlike a
    containment test it also pins the *geometry* of each bounce, not just its sign.
    """
    rng = np.random.default_rng(3)
    x0 = np.array([[0.31, 0.17]])
    v0 = np.array([[0.7137, 0.5219]])
    v0 = v0 / np.linalg.norm(v0)

    def advance(sim, T):
        """Free flight for exactly ``T`` of simulated time, bouncing on the way."""
        remaining = T
        for _ in range(10_000):
            tau, i, k = sim._next_wall_event()
            if not math.isfinite(tau) or tau >= remaining:
                sim.X = sim.X + sim.V * remaining
                return
            sim.X = sim.X + sim.V * tau
            sim._resolve_wall(i, k)
            remaining -= tau
        raise AssertionError("too many wall events")

    T = 37.0  # ~40 bounces across a triangle of side 1 at unit speed
    sim = ls.Billiard(x0.copy(), rng)
    sim.V = v0.copy()
    advance(sim, T)
    assert ls.inside(sim.X, tol=1e-12)

    sim.V = -sim.V
    advance(sim, T)

    assert sim.X[0] == pytest.approx(x0[0], abs=1e-9)
    assert sim.V[0] == pytest.approx(-v0[0], abs=1e-9)


def test_corner_does_not_eject_the_particle():
    """Aim at a 60 degree vertex; the fixup must keep the particle inside."""
    rng = np.random.default_rng(5)
    for vertex in ls.VERTICES:
        start = ls.VERTICES.mean(axis=0)
        v = vertex - start
        v = v / np.linalg.norm(v)
        sim = ls.Billiard(np.array([start]), rng)
        sim.V = np.array([v])
        sim.run_stage(gamma=0.0, max_events=3_000, stall_window=10**9)
        assert ls.inside(sim.X, tol=1e-11), f"escaped near vertex {vertex}"


# ===================================================================================== #
# 3. Collision prediction, in isolation
# ===================================================================================== #


def test_smallest_positive_root_matches_numpy_roots():
    rng = np.random.default_rng(2)
    for _ in range(500):
        A, B, C = rng.normal(size=3) * rng.choice([1.0, 1e-3, 1e3])
        got = float(ls.smallest_positive_root(A, B, C))
        want = [r.real for r in np.roots([A, 2 * B, C]) if abs(r.imag) < 1e-12 and r.real > 0]
        if not want:
            assert not math.isfinite(got)
        else:
            assert got == pytest.approx(min(want), rel=1e-7, abs=1e-12)


def test_smallest_positive_root_linear_branch():
    # A = 0 exactly: 2Bt + C = 0 -> t = -C/(2B)
    assert float(ls.smallest_positive_root(0.0, -1.0, 4.0)) == pytest.approx(2.0)
    assert not math.isfinite(float(ls.smallest_positive_root(0.0, 1.0, 4.0)))


def test_pair_contact_time_head_on_no_growth():
    """Two particles closing at relative speed 2 from separation 1, exclusion 0.4."""
    rng = np.random.default_rng(0)
    sim = ls.Billiard(np.array([[0.3, 0.2], [0.7, 0.2]]), rng)
    sim.V = np.array([[1.0, 0.0], [-1.0, 0.0]])
    sim.D = 0.1
    tau, i, j = sim._next_pair_event(gamma=0.0)
    # separation 0.4, closes at 2 per unit time, contact when separation == 0.1
    assert tau == pytest.approx((0.4 - 0.1) / 2.0, rel=1e-13)


def test_pair_contact_time_with_growth_when_stationary():
    """Stationary pair, exclusion diameter catching up with them."""
    rng = np.random.default_rng(0)
    sim = ls.Billiard(np.array([[0.3, 0.2], [0.7, 0.2]]), rng)
    sim.V = np.zeros((2, 2))
    sim.D = 0.1
    gamma = 0.05
    tau, _, _ = sim._next_pair_event(gamma)
    assert tau == pytest.approx((0.4 - 0.1) / gamma, rel=1e-12)


def test_pair_resolution_reverses_the_gap_rate():
    rng = np.random.default_rng(0)
    sim = ls.Billiard(np.array([[0.0, 0.0], [0.5, 0.0]]), rng)
    sim.V = np.array([[1.0, 0.3], [-1.0, 0.3]])
    gamma = 0.02
    u = np.array([-1.0, 0.0])  # (x_0 - x_1)/|.|
    g_before = float((sim.V[0] - sim.V[1]) @ u)
    sim._resolve_pair(0, 1, gamma)
    g_after = float((sim.V[0] - sim.V[1]) @ u)
    assert g_after - gamma == pytest.approx(-(g_before - gamma), rel=1e-13)


def test_pair_resolution_conserves_momentum():
    rng = np.random.default_rng(0)
    sim = ls.Billiard(np.array([[0.0, 0.0], [0.4, 0.1]]), rng)
    sim.V = np.array([[1.0, 0.3], [-0.4, -0.9]])
    before = sim.V.sum(axis=0).copy()
    sim._resolve_pair(0, 1, 0.03)
    assert sim.V.sum(axis=0) == pytest.approx(before, abs=1e-14)


def test_pair_resolution_is_a_no_op_when_already_separating():
    """The guard that stops a jammed contact oscillating forever."""
    rng = np.random.default_rng(0)
    sim = ls.Billiard(np.array([[0.0, 0.0], [0.4, 0.0]]), rng)
    sim.V = np.array([[-1.0, 0.0], [1.0, 0.0]])  # flying apart
    before = sim.V.copy()
    sim._resolve_pair(0, 1, 0.01)
    assert sim.V == pytest.approx(before)


def test_two_body_no_growth_conserves_energy():
    rng = np.random.default_rng(4)
    sim = ls.Billiard(ls.sample_uniform(2, rng), rng)
    sim.D = 0.2
    e0 = float((sim.V**2).sum())
    sim.run_stage(gamma=0.0, max_events=5_000, stall_window=10**9, thermostat_every=10**9)
    assert float((sim.V**2).sum()) == pytest.approx(e0, rel=1e-8)
    assert ls.inside(sim.X, tol=1e-11)


# ===================================================================================== #
# 4. Coupled runs: invariants that must hold whatever the packing quality
# ===================================================================================== #


@pytest.mark.parametrize("n", [2, 5, 12, 25])
def test_run_output_is_contained_and_not_overlapping(n):
    rng = np.random.default_rng(100 + n)
    res = ls.ls_run(n, rng, schedule=(1e-2, 1e-3), max_events_per_stage=20_000)
    assert ls.inside(res.points, tol=1e-12)
    # the achieved exclusion diameter never exceeds the measured minimum distance by
    # more than round-off: D is a *lower* bound for what the configuration realises
    assert res.d_jam <= res.m + 1e-9
    assert res.m > 0.0


def test_growth_actually_compacts():
    """A trivially checkable ceiling: n points in T cannot all be far apart.

    For n = 3 the optimum is the three vertices, m = 1.  LS must land near it and must
    never exceed it.
    """
    rng = np.random.default_rng(42)
    best = max(ls.ls_run(3, rng).m for _ in range(5))
    assert best <= 1.0 + 1e-12
    assert best > 0.99


# ===================================================================================== #
# 5. Known optima  (the validation gate: RULES.md SS6 "validate on a tiny instance")
# ===================================================================================== #

#: Exact optimal ``m`` for the triangular numbers n = T(k): the k-row lattice, m = 1/(k-1).
TRIANGULAR = {3: 1.0, 6: 0.5, 10: 1.0 / 3.0, 15: 0.25}


@pytest.mark.parametrize("n,m_exact", sorted(TRIANGULAR.items()))
def test_reproduces_triangular_lattice_optima(n, m_exact):
    """LS + polish must recover the exactly-known packings, and must never beat them.

    Beating a *proved* optimum is the signature of an infeasible configuration, so the
    upper assertion is the one that matters most.
    """
    from polish import polish

    rng = np.random.default_rng(2026 + n)
    best = 0.0
    for _ in range(6):
        res = ls.ls_run(n, rng)
        _, m = polish(res.points)
        best = max(best, m)
    assert best <= m_exact + 1e-9, "claims to beat a known optimum -- infeasible"
    assert best >= m_exact - 1e-9, f"failed to reach the known optimum: {best} vs {m_exact}"


# ===================================================================================== #
# 6. Certificate emission
# ===================================================================================== #


def test_certificate_of_a_known_packing_is_exactly_feasible():
    """The rational snap must produce something an exact checker accepts."""
    from polish import polish

    rng = np.random.default_rng(77)
    res = ls.ls_run(6, rng)
    pts, m = polish(res.points)
    cert = build_certificate(6, pts, note="test")
    ok, why = exact_feasible(cert)
    assert ok, why


def test_certificate_side_length_is_an_honest_upper_bound():
    """Snapping to rationals may only ever *inflate* the reported side length."""
    from polish import polish

    rng = np.random.default_rng(78)
    res = ls.ls_run(10, rng)
    pts, m = polish(res.points)
    cert = build_certificate(10, pts, note="test")
    ok, why = exact_feasible(cert)
    assert ok, why
    s_float = 2.0 / m + 2.0 * SQRT3
    assert cert["_s_float"] >= s_float - 1e-9


def _bare_cert(coords, d):
    """Minimal hand-built certificate, so the exact check is exercised on inputs whose
    feasibility is obvious by hand rather than on optimiser output."""
    return {
        "n": len(coords),
        "claim": "construction",
        "side_length": f"{d} + 2*sqrt(3)",
        "coordinates": [[str(a), str(b)] for a, b in coords],
        "coordinate_type": "rational",
        "verified_by": "test",
        "status": "numerical",
        "beats_record": "no",
        "_d_rational": str(d),
    }


def test_exact_check_accepts_distance_exactly_two():
    """Non-strict: touching is feasible.  A strict check would reject every optimum."""
    ok, why = exact_feasible(_bare_cert([(0, 0), (2, 0)], 2))
    assert ok, why


def test_exact_check_rejects_an_overlap_no_float_could_represent():
    """There is no tolerance.  1e-40 below contact must be rejected, not rounded away.

    ``2 - 1e-40`` is exactly ``2.0`` in double precision, so a float checker cannot even
    represent this input, let alone reject it.  This is the failure the problem's
    ``RULES.md`` SS0 is about.
    """
    from fractions import Fraction

    eps = Fraction(1, 10**40)
    ok, why = exact_feasible(_bare_cert([(Fraction(0), Fraction(0)), (2 - eps, Fraction(0))], 2))
    assert not ok and "distance < 2" in why


def test_exact_check_rejects_a_point_just_outside_each_edge():
    from fractions import Fraction

    eps = Fraction(1, 10**40)
    # below edge AB (y < 0)
    assert not exact_feasible(_bare_cert([(Fraction(1), -eps), (Fraction(4), Fraction(0))], 4))[0]
    # left of edge AC: the point (x, y) needs 3x^2 >= y^2; take x tiny, y = 1
    assert not exact_feasible(
        _bare_cert([(Fraction(1, 10), Fraction(1)), (Fraction(4), Fraction(0))], 4)
    )[0]
    # right of edge BC: mirror of the above
    assert not exact_feasible(
        _bare_cert([(Fraction(39, 10), Fraction(1)), (Fraction(0), Fraction(0))], 4)
    )[0]


def test_exact_check_rejects_a_shrunk_side_length():
    """An honest packing with ``d`` reported one part in 1e40 too small must fail."""
    from fractions import Fraction

    d = Fraction(2) - Fraction(1, 10**40)
    ok, why = exact_feasible(_bare_cert([(Fraction(0), Fraction(0)), (Fraction(2), Fraction(0))], d))
    assert not ok and "edge BC" in why
