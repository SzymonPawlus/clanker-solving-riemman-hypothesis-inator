"""Deterministic numerical challenge for an exact rational three-edge worm.

This is exploratory evidence only.  It does not prove a global lower bound.
"""
from fractions import Fraction as F
import math
import numpy as np

from explore_zigzag import SEG, TRI, SQUARE, hull_area, place

# Successive edge directions are (1,0), (7/25,24/25), and
# (-527/625,336/625).  Each is an exact rational unit vector.
WORM_Q = [
    (F(0), F(0)),
    (F(1, 3), F(0)),
    (F(32, 75), F(8, 25)),
    (F(91, 625), F(312, 625)),
]
WORM = np.array([[float(x), float(y)] for x, y in WORM_Q])
for p, q in zip(WORM_Q, WORM_Q[1:]):
    assert (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 == F(1, 9)

# A basin inherited from the nearby constant-75-degree screen.
START = np.array([
    0.7512607985326297, 0.4341169204420069, 4.184365441062473,
    0.9181826649858131, 0.14408271866609054, 2.0177823169328044,
    0.9307664017466011, 0.00000006568424793481033, 1.85459072914034,
])

def objective(v):
    return hull_area([
        SEG, place(TRI, *v[:3]), place(SQUARE, *v[3:6]),
        place(WORM, *v[6:9]),
    ])

def challenge(seed, steps=100_000):
    rng = np.random.default_rng(seed)
    best, value = START.copy(), objective(START)
    for k in range(steps):
        phase = k % 20_000
        sigma = .03 * (1 - phase / 20_000) + 1e-8
        trial = best.copy()
        mode = k % 10
        if mode < 5:
            j = rng.integers(9)
            trial[j] += rng.normal(0, sigma)
        elif mode < 9:
            j = 3 * rng.integers(3)
            trial[j:j + 3] += rng.normal(0, sigma, 3)
        else:
            trial += rng.normal(0, sigma, 9)
        trial[2::3] %= 2 * math.pi
        candidate = objective(trial)
        if candidate < value:
            best, value = trial, candidate
    return {"status": "numerical", "seed": seed, "area": float(value),
            "pose": best.tolist()}

if __name__ == "__main__":
    print({"exact_vertices": [[str(x), str(y)] for x, y in WORM_Q]})
    for seed in (137257, 137258, 137259):
        print(challenge(seed))
