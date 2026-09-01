#!/usr/bin/env python3
"""Five-dimensional probe adding square-arc contained-triangle pruning."""

import json
from collections import Counter
from fractions import Fraction as Q

import probe_adaptive as base
import probe_portfolio as portfolio


ROOTS = dict(portfolio.ROOTS)
ROOTS["square_ty"] = base.I(-base.D, base.D)
ORDER = ("square_g", "triangle_h", "rectangle_width_f", "arc_fan",
         "mixed_square_arc")


def sqrt2_interval():
    hi = Q(2)
    for _ in range(10):
        hi = (hi+2/hi)/2
    return base.I(2/hi, hi)


RADIUS = sqrt2_interval()*Q(1, 6)


def arc_point(ty, theta):
    sin_t, cos_t = base.sin_range(theta), base.cos_range(theta)
    return (base.PX*cos_t - base.PY*sin_t,
            ty + base.PX*sin_t + base.PY*cos_t)


def square_point(square_ty, alpha):
    # The square centre is (0,square_ty); alpha is the radial vertex angle.
    return (RADIUS*base.cos_range(alpha),
            square_ty + RADIUS*base.sin_range(alpha))


def mixed_margin(box):
    sx, sy = square_point(box["square_ty"], box["alpha"])
    ax, ay = arc_point(box["ty"], box["theta"])
    determinant = sx*ay - sy*ax
    if determinant.lo > 0:
        lower = determinant.lo/2
    elif determinant.hi < 0:
        lower = -determinant.hi/2
    else:
        return Q(-1)
    return lower-base.TARGET


def margins(box):
    old = portfolio.margins(box)
    old["mixed_square_arc"] = mixed_margin(box)
    return old


def pairs(box):
    return {key: base.pair(value) for key, value in box.items()}


def choose_split(box):
    priority = {name: index for index, name in enumerate(
        ("alpha", "beta", "theta", "ty", "square_ty"))}
    axis = max(box, key=lambda key: (
        (box[key].hi-box[key].lo)/(ROOTS[key].hi-ROOTS[key].lo), -priority[key]))
    return axis


def build(box, depth, limit, stats):
    stats["nodes"] += 1
    bounds = margins(box)
    passing = [name for name in ORDER if bounds[name] >= 0]
    if passing:
        name = passing[0]
        stats[f"pruned_{name}"] += 1
        stats[f"weight_{name}"] += Q(1, 2**depth)
        return {"kind": "prune", "predicate": name, "box": pairs(box)}
    if depth == limit:
        stats["unresolved"] += 1
        stats["weight_unresolved"] += Q(1, 2**depth)
        return {"kind": "unresolved", "box": pairs(box)}
    axis = choose_split(box)
    stats[f"split_{axis}"] += 1
    source = box[axis]
    mid = (source.lo+source.hi)/2
    children = []
    for part in (base.I(source.lo, mid), base.I(mid, source.hi)):
        child = dict(box); child[axis] = part
        children.append(build(child, depth+1, limit, stats))
    return {"kind": "split", "axis": axis, "mid": str(mid), "children": children}


def verify(node, box):
    if node["kind"] in ("prune", "unresolved"):
        if node["box"] != pairs(box):
            raise AssertionError("leaf box mismatch")
        if node["kind"] == "prune" and margins(box)[node["predicate"]] < 0:
            raise AssertionError("uncertified predicate selection")
        return
    axis, mid = node["axis"], Q(node["mid"])
    source = box[axis]
    if not source.lo < mid < source.hi:
        raise AssertionError("coverage gap")
    for child_node, part in zip(node["children"],
                                (base.I(source.lo, mid), base.I(mid, source.hi))):
        child = dict(box); child[axis] = part
        verify(child_node, child)


def main():
    stats = Counter()
    tree = build(dict(ROOTS), 0, 7, stats)
    verify(tree, dict(ROOTS))
    prunes = {key.removeprefix("pruned_"): value for key, value in stats.items()
              if key.startswith("pruned_")}
    leaves = sum(prunes.values())+stats["unresolved"]
    print(json.dumps({"scope": "five_dimensional_mixed_probe_only",
                      "fixed_coordinate": "square_tx=0", "global_claim": False,
                      "coverage_verified": True,
                      "stats": {key: str(value) for key, value in stats.items()},
                      "prunes_by_predicate": prunes,
                      "leaf_acceptance_rate": f"{sum(prunes.values())}/{leaves}"},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
