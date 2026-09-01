"""Exact rational local fan certificate for the t=10/13 witness.

This certifies one small placement box only.  It is not a global lower bound.
"""
from dataclasses import dataclass
from fractions import Fraction as F
import argparse


@dataclass(frozen=True)
class I:
    lo: F
    hi: F

    def __init__(self, lo, hi=None):
        lo, hi = F(lo), F(lo if hi is None else hi)
        if lo > hi:
            raise ValueError("empty interval")
        object.__setattr__(self, "lo", lo)
        object.__setattr__(self, "hi", hi)

    def __add__(self, other):
        other = ii(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -ii(other)

    def __rsub__(self, other):
        return ii(other) - self

    def __mul__(self, other):
        other = ii(other)
        products = (self.lo * other.lo, self.lo * other.hi,
                    self.hi * other.lo, self.hi * other.hi)
        return I(min(products), max(products))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = ii(other)
        if other.lo <= 0 <= other.hi:
            raise ZeroDivisionError("interval divisor contains zero")
        reciprocals = (1 / other.lo, 1 / other.hi)
        return self * I(min(reciprocals), max(reciprocals))


def ii(value):
    return value if isinstance(value, I) else I(value)


def squared(value):
    """Exact range of x^2 on one rational interval."""
    if value.lo <= 0 <= value.hi:
        return I(0, max(value.lo * value.lo, value.hi * value.hi))
    endpoints = (value.lo * value.lo, value.hi * value.hi)
    return I(min(endpoints), max(endpoints))


def rotation(t):
    """epsilon=-1 half-angle chart, exactly over rational intervals."""
    denominator = 1 + squared(t)
    return -(1 - squared(t)) / denominator, -(2 * t) / denominator


def place(poly, tx, ty, t):
    c, s = rotation(t)
    return [(tx + x * c - y * s, ty + x * s + y * c) for x, y in poly]


def sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def det(p, q):
    return p[0] * q[1] - p[1] * q[0]


def cross(o, p, q):
    return det(sub(p, o), sub(q, o))


def box(decimal, radius):
    center = F(decimal)
    return I(center - radius, center + radius)


parser = argparse.ArgumentParser()
parser.add_argument("--radius", default="1/100000",
                    help="common rational half-width, such as 1/100000")
parser.add_argument("--summary", action="store_true")
args = parser.parse_args()
RADIUS = F(args.radius)
CENTERS = (
    # Triangle was relocated inside the same fixed five-cycle to avoid the
    # numerically tangent exploratory pose; the fan area is unchanged.
    "0.7482384613885471", "0.43318521035405194", "0.5785074745087493",
    "0.7665063578814811", "0.44201657861761084", "0.22243073361617452",
    "0.9158463782906203", "-0.0002529366842701458", "-0.7683607472878539",
)
VARS = [box(x, RADIUS) for x in CENTERS]

# sqrt(3) enclosure, checked exactly.
SQ3 = I(F(1732050807568877, 10**15), F(1732050807568878, 10**15))
if not SQ3.lo * SQ3.lo < 3 < SQ3.hi * SQ3.hi:
    raise RuntimeError("bad sqrt(3) enclosure")

SEG = [(I(0), I(0)), (I(1), I(0))]
TRI = [(I(0), I(0)), (I(F(1, 2)), I(0)),
       (I(F(1, 4)), SQ3 * F(1, 4))]
SQUARE = [(I(0), I(0)), (I(F(1, 3)), I(0)),
          (I(F(1, 3)), I(F(1, 3))), (I(0), I(F(1, 3)))]
WORM_Q = [(F(0), F(0)), (F(1, 3), F(0)),
          (F(338, 807), F(260, 807)),
          (F(9361, 72361), F(105820, 217083))]
for p, q in zip(WORM_Q, WORM_Q[1:]):
    if (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 != F(1, 9):
        raise RuntimeError("non-unit witness")
WORM = [(I(x), I(y)) for x, y in WORM_Q]

triangle = place(TRI, *VARS[:3])
square = place(SQUARE, *VARS[3:6])
worm = place(WORM, *VARS[6:9])
points = SEG + triangle + square + worm
labels = (["segment0", "segment1"] + [f"triangle{i}" for i in range(3)]
          + [f"square{i}" for i in range(4)] + [f"worm{i}" for i in range(4)])

# Counterclockwise midpoint cycle: segment0, square2, segment1, square0, worm2.
CYCLE = (0, 7, 1, 5, 11)
anchor = points[CYCLE[0]]
rays = [sub(points[i], anchor) for i in CYCLE[1:]]

# u=(1,0): all rays stay in one strict open half-plane.
ray_x_lowers = [ray[0].lo for ray in rays]
fan_dets = [det(rays[i], rays[i + 1]) for i in range(len(rays) - 1)]
area = sum(fan_dets, I(0)) / 2
TARGET = F(232239, 1_000_000)

if min(ray_x_lowers) <= 0:
    raise RuntimeError("fan half-plane guard failed")
if min(value.lo for value in fan_dets) <= 0:
    raise RuntimeError("fan angular-order guard failed")
if area.lo <= TARGET:
    raise RuntimeError("fan area lower bound failed")

# Diagnostic only: containment is not a premise of the fan lower bound.
cycle_edges = list(zip(CYCLE, CYCLE[1:] + CYCLE[:1]))
omitted = [i for i in range(len(points)) if i not in CYCLE]
containment = []
for index in omitted:
    margins = [cross(points[a], points[b], points[index]) for a, b in cycle_edges]
    containment.append((labels[index], min(margin.lo for margin in margins),
                        min(margin.hi for margin in margins)))

result = {
    "status": "PASS_LOCAL_FAN_ONLY",
    "radius_exact": str(RADIUS),
    "cycle": [labels[i] for i in CYCLE],
    "ray_x_lower_exact": [str(x) for x in ray_x_lowers],
    "fan_det_lower_exact": [str(x.lo) for x in fan_dets],
    "area_lower_exact": str(area.lo),
    "area_lower": float(area.lo),
    "target_exact": str(TARGET),
    "omitted_containment_diagnostics": [
        {"vertex": name, "minimum_lower": str(lo), "minimum_upper": str(hi),
         "certified_inside": lo >= 0, "certified_outside_some_edge": hi < 0}
        for name, lo, hi in containment
    ],
}
if args.summary:
    print({"status": result["status"], "radius_exact": str(RADIUS),
           "minimum_ray_x": float(min(ray_x_lowers)),
           "minimum_fan_det": float(min(x.lo for x in fan_dets)),
           "area_lower": float(area.lo),
           "uncertain_omitted": [name for name, lo, hi in containment if lo < 0 <= hi],
           "certified_outside_omitted": [name for name, lo, hi in containment if hi < 0]})
else:
    print(result)
