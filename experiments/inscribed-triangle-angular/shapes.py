"""Exact rational polygon families used by the angular lane's own tests and hunts.

Everything is built from Fractions or from Q(sqrt3) constants; nothing here is a float.
The seeded generators use `random.Random(seed)` from the standard library only.
"""

from __future__ import annotations

import random
from fractions import Fraction as F

from q3 import Q3
from angular import V, is_simple, is_convex

R3 = Q3(0, 1)


def equilateral():
    return [V(0, 0), V(1, 0), (Q3(F(1, 2)), Q3(0, F(1, 2)))]


def t30_30_120():
    return [V(-1, 0), V(1, 0), (Q3(0), Q3(0, F(1, 3)))]


def unit_square():
    return [V(0, 0), V(1, 0), V(1, 1), V(0, 1)]


def rectangle(w, h):
    return [V(0, 0), V(w, 0), (Q3.of(w), Q3.of(h)), (Q3(0), Q3.of(h))]


def ell():
    return [V(0, 0), V(3, 0), V(3, 1), V(1, 1), V(1, 3), V(0, 3)]


def cstrip(h):
    """The sibling's C-shape: three sides of a 10x10 frame, free end tapered to the origin."""
    h = F(h)
    return [V(0, 0), (Q3.of(10), Q3.of(-h)), V(10, -10), V(-10, -10), V(-10, 10),
            V(10, 10), (Q3.of(10), Q3.of(h))]


def spikes(k, tip, width, inner, seed=None):
    """A `k`-pointed star with rational vertices: tips at radius `tip` on a rational
    parametrisation of the circle, valleys at radius `inner`, tip half-width `width`.

    Built with the rational circle parametrisation ((1-t^2)/(1+t^2), 2t/(1+t^2)) so every
    coordinate is rational; simplicity is CHECKED, not assumed.
    """
    pts = []
    for i in range(k):
        t = F(i, k)
        for (rad, off) in ((inner, F(0)), (tip, width)):
            u = t + off
            x, y = _circ(u)
            pts.append((Q3(F(rad) * x), Q3(F(rad) * y)))
    return pts


def _circ(u):
    """A rational point of the unit circle at parameter u in [0,1) (angle 2*pi*u is only
    approximated -- what matters is that the map is injective and monotone in u)."""
    u = F(u) % 1
    # split the circle into four rational arcs so the parametrisation is monotone all round
    q, r = divmod(u * 4, 1)
    q = int(q)
    t = F(r)
    x = (1 - t * t) / (1 + t * t)
    y = 2 * t / (1 + t * t)
    for _ in range(q):
        x, y = -y, x
    return x, y


def random_star(rng, n, scale=1000):
    """A random star-shaped (hence simple) rational polygon: n distinct rational directions
    in cyclic order, each at a random rational radius."""
    us = sorted(rng.sample(range(scale), n))
    pts = []
    for u in us:
        x, y = _circ(F(u, scale))
        r = F(rng.randint(1, 100), rng.randint(1, 8))
        pts.append((Q3(r * x), Q3(r * y)))
    return pts


def random_spiky(rng, k, scale=4000):
    """Alternating long thin spikes and short valleys -- the shape most likely to produce
    boundary points with a narrow angular view of the curve."""
    pts = []
    us = sorted(rng.sample(range(scale), 3 * k))
    for i in range(k):
        a, b, c = us[3 * i], us[3 * i + 1], us[3 * i + 2]
        for (u, r) in ((a, F(rng.randint(1, 4), rng.randint(1, 3))),
                       (b, F(rng.randint(20, 400), 1)),
                       (c, F(rng.randint(1, 4), rng.randint(1, 3)))):
            x, y = _circ(F(u, scale))
            pts.append((Q3(r * x), Q3(r * y)))
    return pts


NAMED = {
    "ctl-equilateral": equilateral,
    "ctl-30-30-120": t30_30_120,
    "ctl-square": unit_square,
    "ell": ell,
    "cstrip-h1_4": lambda: cstrip(F(1, 4)),
    "cstrip-h1_20": lambda: cstrip(F(1, 20)),
    "star6": lambda: spikes(6, 10, F(1, 24), 3),
    "star3-thin": lambda: spikes(3, 40, F(1, 200), 1),
    "rect-10x1": lambda: rectangle(10, 1),
}
