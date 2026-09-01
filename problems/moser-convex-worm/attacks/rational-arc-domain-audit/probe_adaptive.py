#!/usr/bin/env python3
"""Deterministic exact-coverage probe for one contained-fan pruning predicate."""

import json
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from math import factorial


TARGET = Q(232239, 1000000)
D = Q(107267, 100000)
PX, PY = Q(91, 625), Q(312, 625)


class I:
    def __init__(self, lo, hi=None):
        self.lo, self.hi = Q(lo), Q(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    def __add__(self, other):
        other = other if isinstance(other, I) else I(other)
        return I(self.lo+other.lo, self.hi+other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        other = other if isinstance(other, I) else I(other)
        values = (self.lo*other.lo, self.lo*other.hi,
                  self.hi*other.lo, self.hi*other.hi)
        return I(min(values), max(values))

    __rmul__ = __mul__


def atan_inv(n, terms):
    total = Q(0)
    for k in range(terms):
        term = Q(1, (2*k+1)*Q(n)**(2*k+1))
        total += term if k % 2 == 0 else -term
    k = terms
    nxt = Q(1, (2*k+1)*Q(n)**(2*k+1))
    following = total + (nxt if k % 2 == 0 else -nxt)
    return I(min(total, following), max(total, following))


PI = 16*atan_inv(5, 45) + -4*atan_inv(239, 15)


@lru_cache(maxsize=None)
def point_trig(degrees, cosine):
    radians = I(Q(degrees)*PI.lo/180, Q(degrees)*PI.hi/180)
    x2 = radians*radians
    power = I(1) if cosine else radians
    total = I(0)
    last = 0
    for k in range(14):
        degree = 2*k if cosine else 2*k+1
        total += (1 if k % 2 == 0 else -1)*power*Q(1, factorial(degree))
        power = power*x2
        last = degree
    radius = max(abs(radians.lo), abs(radians.hi))
    rem = radius**(last+2)/factorial(last+2)
    return I(total.lo-rem, total.hi+rem)


def sin_range(angle):
    lo, hi = point_trig(angle.lo, False), point_trig(angle.hi, False)
    upper = Q(1) if angle.lo <= 90 <= angle.hi else max(lo.hi, hi.hi)
    return I(min(lo.lo, hi.lo), upper)


def cos_range(angle):
    # Cosine is decreasing on the entire certified [0,180] gauge.
    low, high = point_trig(angle.hi, True), point_trig(angle.lo, True)
    return I(low.lo, high.hi)


def fan_height(ty, theta):
    return ty + PX*sin_range(theta) + PY*cos_range(theta)


def choose_split(ty, theta):
    # Upper bounds on contribution to output uncertainty. The theta score is
    # the derivative bound (|PX|+|PY|)*delta radians.
    ty_score = ty.hi-ty.lo
    theta_score = (PX+PY)*(theta.hi-theta.lo)*PI.hi/180
    return "ty" if ty_score >= theta_score else "theta"


def build(ty, theta, depth, max_depth, stats):
    stats["nodes"] += 1
    height = fan_height(ty, theta)
    if height.lo > 0 and height.lo/2 >= TARGET:
        stats["pruned"] += 1
        return {"kind": "fan_prune", "ty": pair(ty), "theta": pair(theta)}
    if depth == max_depth:
        stats["unresolved"] += 1
        return {"kind": "unresolved", "ty": pair(ty), "theta": pair(theta)}
    axis = choose_split(ty, theta)
    stats[f"split_{axis}"] += 1
    source = ty if axis == "ty" else theta
    mid = (source.lo+source.hi)/2
    first, second = I(source.lo, mid), I(mid, source.hi)
    children = ([build(first, theta, depth+1, max_depth, stats),
                 build(second, theta, depth+1, max_depth, stats)] if axis == "ty" else
                [build(ty, first, depth+1, max_depth, stats),
                 build(ty, second, depth+1, max_depth, stats)])
    return {"kind": "split", "axis": axis, "mid": str(mid), "children": children}


def pair(interval):
    return [str(interval.lo), str(interval.hi)]


def verify_cover(node, ty, theta):
    if node["kind"] in ("fan_prune", "unresolved"):
        if node["ty"] != pair(ty) or node["theta"] != pair(theta):
            raise AssertionError("leaf domain mismatch")
        if node["kind"] == "fan_prune":
            height = fan_height(ty, theta)
            if height.lo <= 0 or height.lo/2 < TARGET:
                raise AssertionError("unsound fan prune")
        return
    axis, mid = node["axis"], Q(node["mid"])
    source = ty if axis == "ty" else theta
    if not source.lo < mid < source.hi or len(node["children"]) != 2:
        raise AssertionError("invalid split coverage")
    halves = I(source.lo, mid), I(mid, source.hi)
    if axis == "ty":
        verify_cover(node["children"][0], halves[0], theta)
        verify_cover(node["children"][1], halves[1], theta)
    else:
        verify_cover(node["children"][0], ty, halves[0])
        verify_cover(node["children"][1], ty, halves[1])


def main():
    stats = Counter()
    root_ty, root_theta = I(-D, D), I(0, 180)
    max_depth = 10
    tree = build(root_ty, root_theta, 0, max_depth, stats)
    verify_cover(tree, root_ty, root_theta)
    leaves = stats["pruned"]+stats["unresolved"]
    report = {
        "scope": "arc_vertical_fan_probe_only",
        "max_depth": max_depth,
        "stats": dict(stats),
        "leaf_acceptance_rate": f"{stats['pruned']}/{leaves}",
        "coverage_verified": True,
        "global_claim": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
