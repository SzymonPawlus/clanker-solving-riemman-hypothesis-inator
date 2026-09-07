#!/usr/bin/env python3
"""Four-dimensional adaptive probe with independently derived area predicates."""

import json
from collections import Counter
from fractions import Fraction as Q

import probe_adaptive as base


TARGET = base.TARGET
PREDICATE_ORDER = ("square_g", "triangle_h", "rectangle_width_f", "arc_fan")


def sqrt2_lower():
    hi = Q(2)
    for _ in range(10):
        hi = (hi+2/hi)/2
    lo = 2/hi
    if not lo*lo <= 2 <= hi*hi:
        raise AssertionError("sqrt2 enclosure")
    return lo


SQRT2_LO = sqrt2_lower()


def cosine_abs_lower(interval):
    """Lower bound cosine on an interval contained in [-90,90] degrees."""
    radius = max(abs(interval.lo), abs(interval.hi))
    if radius > 90:
        raise AssertionError("cosine guard outside [-90,90]")
    return base.point_trig(radius, True).lo


def margins(box):
    ty, theta, alpha, beta = (box[k] for k in ("ty", "theta", "alpha", "beta"))
    arc_height = base.fan_height(ty, theta)
    arc = arc_height.lo/2 if arc_height.lo > 0 else Q(-1)

    # sin increases on the square gauge [45,90].
    g = SQRT2_LO*base.point_trig(alpha.lo, False).lo/6

    # Each h branch is independently sound. Taking their maximum preserves a
    # lower bound for max(h_plus,h_minus).
    hp = base.sin_range(base.I(beta.lo+30, beta.hi+30)).lo/4
    hm = base.sin_range(base.I(beta.lo-30, beta.hi-30)).lo/4
    h = max(hp, hm)

    first_arg = base.I(alpha.lo-beta.hi+15, alpha.hi-beta.lo+15)
    second_arg = base.I(alpha.lo-45, alpha.hi-45)
    f = (cosine_abs_lower(first_arg)/2 + cosine_abs_lower(second_arg))/6
    return {"square_g": g-TARGET, "triangle_h": h-TARGET,
            "rectangle_width_f": f-TARGET, "arc_fan": arc-TARGET}


ROOTS = {"ty": base.I(-base.D, base.D), "theta": base.I(0, 180),
         "alpha": base.I(45, 90), "beta": base.I(60, 120)}


def choose_split(box):
    root_width = {k: ROOTS[k].hi-ROOTS[k].lo for k in ROOTS}
    order = {name: index for index, name in enumerate(("alpha", "beta", "theta", "ty"))}
    axis = max(box, key=lambda k: ((box[k].hi-box[k].lo)/root_width[k], -order[k]))
    return (box[axis].hi-box[axis].lo)/root_width[axis], axis


def build(box, depth, max_depth, stats):
    stats["nodes"] += 1
    certified = margins(box)
    passing = [name for name in PREDICATE_ORDER if certified[name] >= 0]
    if passing:
        name = passing[0]  # deterministic incremental-coverage priority
        stats[f"pruned_{name}"] += 1
        return {"kind": "prune", "predicate": name, "box": pairs(box)}
    if depth == max_depth:
        stats["unresolved"] += 1
        return {"kind": "unresolved", "box": pairs(box)}
    _, axis = choose_split(box)
    stats[f"split_{axis}"] += 1
    source = box[axis]
    mid = (source.lo+source.hi)/2
    children = []
    for part in (base.I(source.lo, mid), base.I(mid, source.hi)):
        child = dict(box)
        child[axis] = part
        children.append(build(child, depth+1, max_depth, stats))
    return {"kind": "split", "axis": axis, "mid": str(mid), "children": children}


def pairs(box):
    return {key: base.pair(value) for key, value in box.items()}


def verify(node, box):
    if node["kind"] in ("prune", "unresolved"):
        if node["box"] != pairs(box):
            raise AssertionError("leaf box mismatch")
        if node["kind"] == "prune" and margins(box)[node["predicate"]] < 0:
            raise AssertionError("selected predicate lacks certified margin")
        return
    axis, mid = node["axis"], Q(node["mid"])
    source = box[axis]
    if not source.lo < mid < source.hi:
        raise AssertionError("split does not cover parent")
    for child_node, part in zip(node["children"],
                                (base.I(source.lo, mid), base.I(mid, source.hi))):
        child = dict(box)
        child[axis] = part
        verify(child_node, child)


def main():
    stats = Counter()
    tree = build(dict(ROOTS), 0, 10, stats)
    verify(tree, dict(ROOTS))
    prunes = {k.removeprefix("pruned_"): v for k, v in stats.items()
              if k.startswith("pruned_")}
    leaves = sum(prunes.values())+stats["unresolved"]
    print(json.dumps({"scope": "four_dimensional_predicate_probe_only",
                      "coverage_verified": True, "global_claim": False,
                      "stats": dict(stats), "prunes_by_predicate": prunes,
                      "leaf_acceptance_rate": f"{sum(prunes.values())}/{leaves}"},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
