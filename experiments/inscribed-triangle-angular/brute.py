"""A deliberately dumb FLOATING-POINT brute force over the criterion (R).

This exists only to cross-examine `angular.py` during self-test.  It decides nothing that
is reported: it is a pre-screen, and everything it suggests is re-decided exactly.  It
shares no code path with the exact decider beyond the polygon data -- it uses math.cos /
math.sin, a uniform grid of angles, and a sign-change hunt on the radius-difference
function.

R(t) is treated as a set of closed radius INTERVALS, not points: a ray running along an
edge that contains O sees a whole interval of that edge.  An earlier version of this file
missed those and reported 1 good direction where the exact decider reported 3 -- on the
120-degree apex of the 30-30-120 control, where two of the three good directions run along
an edge.  Hand-checking that case confirmed the exact decider (the triangle
(0,r3/3), (-1/2,r3/6), (0,0) is equilateral with side r3/3), so the bug was here.  The
lesson is recorded because it is the same class of blind spot the exact code has to avoid.

Two probes are exposed:
  sweep_directions  -- sign changes of r_e(t) - r_f(t+60) on a uniform grid (transversal
                       crossings only; tangential touches and interval matches are invisible
                       to a grid and are NOT expected to be found).
  special_directions-- the finitely many directions along O->vertex rays and their +-60
                       rotations, tested directly with a tolerance.
"""

from __future__ import annotations

import math

D60 = math.pi / 3.0


def to_float_poly(poly):
    return [(float(p[0]), float(p[1])) for p in poly]


def ray_intervals(O, poly, t, eps=1e-12):
    """All (edge_index, r_lo, r_hi) hits of the open ray from O at angle t."""
    ux, uy = math.cos(t), math.sin(t)
    out = []
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        den = ux * ey - uy * ex
        wx, wy = ax - O[0], ay - O[1]
        if abs(den) > 1e-13:
            s = (wx * ey - wy * ex) / den
            m = (wx * uy - wy * ux) / den
            if s > eps and -1e-11 <= m <= 1 + 1e-11:
                out.append((i, s, s))
            continue
        # ray parallel to the edge: only relevant if O is on the edge's line
        if abs(wx * uy - wy * ux) > 1e-11 * max(1.0, abs(wx) + abs(wy)):
            continue
        sa = wx * ux + wy * uy
        sb = (bx - O[0]) * ux + (by - O[1]) * uy
        lo, hi = (sa, sb) if sa <= sb else (sb, sa)
        if hi <= eps:
            continue
        out.append((i, max(lo, eps), hi))
    return out


def _meet(i1, i2, tol):
    return (i1[1] <= i2[2] + tol) and (i2[1] <= i1[2] + tol)


def good_at(O, poly, t, tol=1e-9):
    """Is direction t good, to tolerance?  (Interval overlap of R(t) and R(t+60).)"""
    h1 = ray_intervals(O, poly, t)
    h2 = ray_intervals(O, poly, t + D60)
    for a in h1:
        for b in h2:
            if _meet(a, b, tol):
                return True
    return False


def sweep_directions(O, poly, steps=20000):
    """Transversal good directions, by sign change of r_e(t) - r_f(t+60)."""
    prev = {}
    found = []
    for k in range(steps + 1):
        t = 2.0 * math.pi * k / steps
        h1 = [x for x in ray_intervals(O, poly, t) if x[1] == x[2]]
        h2 = [x for x in ray_intervals(O, poly, t + D60) if x[1] == x[2]]
        cur = {}
        for (i, r1, _) in h1:
            for (j, r2, _) in h2:
                cur[(i, j)] = r1 - r2
        for key, val in cur.items():
            if key in prev:
                p = prev[key]
                if (p < 0 < val) or (val < 0 < p) or val == 0.0:
                    found.append(t)
        prev = cur
    found.sort()
    merged = []
    tol = 4.0 * math.pi / steps
    for t in found:
        if merged and abs(t - merged[-1]) < tol:
            continue
        merged.append(t)
    if len(merged) > 1 and abs(merged[0] + 2 * math.pi - merged[-1]) < tol:
        merged.pop()
    return merged


def special_directions(O, poly, tol=1e-9):
    """Directions along O->vertex rays and their +-60 rotations that are good."""
    cand = []
    for (vx, vy) in poly:
        dx, dy = vx - O[0], vy - O[1]
        if abs(dx) < 1e-15 and abs(dy) < 1e-15:
            continue
        a = math.atan2(dy, dx)
        cand += [a, a - D60, a + D60, a + math.pi, a + math.pi - D60, a + math.pi + D60]
    out = []
    for a in cand:
        a %= 2 * math.pi
        if good_at(O, poly, a, tol):
            if not any(abs(a - b) < 1e-9 for b in out):
                out.append(a)
    out.sort()
    return out


def is_good_float(O, poly, steps=20000):
    return bool(sweep_directions(O, poly, steps)) or bool(special_directions(O, poly))
