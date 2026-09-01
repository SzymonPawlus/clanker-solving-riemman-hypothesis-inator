"""Numerically challenge the exact 10/13 half-angle candidate; not a proof."""
from fractions import Fraction as F
import math
import numpy as np

from explore_zigzag import SEG, TRI, SQUARE, hull_area, place

# Turn cosine/sine are 69/269 and 260/269; applying the turn twice gives
# -62839/72361 and 35880/72361.
WORM_Q = [
    (F(0), F(0)),
    (F(1, 3), F(0)),
    (F(338, 807), F(260, 807)),
    (F(9361, 72361), F(105820, 217083)),
]
WORM = np.array([[float(x), float(y)] for x, y in WORM_Q])
for p, q in zip(WORM_Q, WORM_Q[1:]):
    assert (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 == F(1, 9)

START = np.array([
    0.7537508572601075, 0.435600524430752, 4.178334550744703,
    0.7665063578814811, 0.44201657861761084, 3.579327925972086,
    0.9158463782906203, -0.0002529366842701458, 1.8312950482517278,
])

def objective(v):
    return hull_area([SEG, place(TRI, *v[:3]), place(SQUARE, *v[3:6]),
                      place(WORM, *v[6:9])])

def challenge(seed, steps=100_000):
    rng = np.random.default_rng(seed)
    best, value = START.copy(), objective(START)
    for k in range(steps):
        phase = k % 20_000
        sigma = .03 * (1 - phase / 20_000) + 1e-8
        trial = best.copy()
        mode = k % 10
        if mode < 5:
            j = rng.integers(9); trial[j] += rng.normal(0, sigma)
        elif mode < 9:
            j = 3 * rng.integers(3); trial[j:j + 3] += rng.normal(0, sigma, 3)
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
    for seed in (1013, 1014, 1015):
        print(challenge(seed))
