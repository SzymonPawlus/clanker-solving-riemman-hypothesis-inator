"""Produce or replay an exact projected triangle branch tree.

This is a local, conditional certificate: the square placement ranges over the
``alternate`` rational box.  It proves that every triangle placement compatible
with hull diameter < 1073/1000 has a guarded fan of area > 0.232239.  The worm
is irrelevant to this projected lower envelope.

All certificate arithmetic uses ``fractions.Fraction``.  A certificate is a
JSON list of prefix-free binary leaf paths and rejection witnesses.  Replay
reconstructs every rational box from its path and independently checks that the
paths are a complete binary cover of each half-angle chart.
"""
from dataclasses import dataclass
from fractions import Fraction as F
import argparse
import copy
import json


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
        other = iv(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -iv(other)

    def __rsub__(self, other):
        return iv(other) - self

    def __mul__(self, other):
        other = iv(other)
        p = (self.lo * other.lo, self.lo * other.hi,
             self.hi * other.lo, self.hi * other.hi)
        return I(min(p), max(p))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = iv(other)
        if other.lo <= 0 <= other.hi:
            raise ZeroDivisionError("interval divisor contains zero")
        return self * I(min(1 / other.lo, 1 / other.hi),
                        max(1 / other.lo, 1 / other.hi))


def iv(x):
    return x if isinstance(x, I) else I(x)


def squared(x):
    if x.lo <= 0 <= x.hi:
        return I(0, max(x.lo * x.lo, x.hi * x.hi))
    return I(min(x.lo * x.lo, x.hi * x.hi),
             max(x.lo * x.lo, x.hi * x.hi))


def rotation(t, epsilon):
    d = 1 + squared(t)
    return epsilon * (1 - squared(t)) / d, epsilon * 2 * t / d


def place(poly, x, y, t, epsilon):
    c, s = rotation(t, epsilon)
    return [(x + a * c - b * s, y + a * s + b * c) for a, b in poly]


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def midpoint(p):
    return tuple((q.lo + q.hi) / 2 for q in p)


def cross(a, b, c):
    return det(sub(b, a), sub(c, a))


def midpoint_hull(points):
    """Exact monotone-chain hull of rational interval midpoints."""
    p = [midpoint(q) for q in points]
    order = sorted(range(len(p)), key=lambda i: p[i])
    lower = []
    for i in order:
        while len(lower) >= 2 and cross(p[lower[-2]], p[lower[-1]], p[i]) <= 0:
            lower.pop()
        lower.append(i)
    upper = []
    for i in reversed(order):
        while len(upper) >= 2 and cross(p[upper[-2]], p[upper[-1]], p[i]) <= 0:
            upper.pop()
        upper.append(i)
    return lower[:-1] + upper[:-1]


SQ3 = I(F(1732050807568877, 10**15), F(1732050807568878, 10**15))
if not SQ3.lo * SQ3.lo < 3 < SQ3.hi * SQ3.hi:
    raise RuntimeError("bad sqrt(3) enclosure")
SEG = [(I(0), I(0)), (I(1), I(0))]
TRI = [(I(0), I(0)), (I(F(1, 2)), I(0)),
       (I(F(1, 4)), SQ3 * F(1, 4))]
SQUARE = [(I(0), I(0)), (I(F(1, 3)), I(0)),
          (I(F(1, 3)), I(F(1, 3))), (I(0), I(F(1, 3)))]
TARGET = F(232239, 1_000_000)
DIAMETER = F(1073, 1000)
SQUARE_CENTER = tuple(map(F, (
    "0.5785139974844686", "-0.011665626530321464",
    "0.034819624673572754")))


def square_points(radius):
    box = [I(c - radius, c + radius) for c in SQUARE_CENTER]
    return place(SQUARE, *box, 1)


def points(box, epsilon, square):
    x = I(box[0], box[1])
    y = I(box[2], box[3])
    t = I(box[4], box[5])
    return SEG + square + place(TRI, x, y, t, epsilon)


def diameter_witness(p):
    """Return a vertex/endpoint pair forced farther apart than DIAMETER."""
    for i in range(6, 9):
        for endpoint in range(2):
            dx, dy = sub(p[i], SEG[endpoint])
            if (squared(dx) + squared(dy)).lo > DIAMETER * DIAMETER:
                return [i, endpoint]
    return None


def checked_fan(p, cycle):
    anchor = p[cycle[0]]
    rays = [sub(p[i], anchor) for i in cycle[1:]]
    # The supplied integer direction puts every ray in one open half-plane.
    direction = cycle[-1]
    ux, uy = DIRECTIONS[direction]
    rays = rays[:-1]
    if any((ux * r[0] + uy * r[1]).lo <= 0 for r in rays):
        return None
    ds = [det(rays[i], rays[i + 1]) for i in range(len(rays) - 1)]
    if not ds or any(d.lo <= 0 for d in ds):
        return None
    area = sum(ds, I(0)) / 2
    return area.lo if area.lo > TARGET else None


DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1),
              (1, 1), (1, -1), (-1, 1), (-1, -1))


def find_fan(p):
    """Deterministically search guarded subfans of the exact midpoint hull."""
    hull = midpoint_hull(p)
    mids = [midpoint(q) for q in p]
    for d, (ux, uy) in enumerate(DIRECTIONS):
        start = min(range(len(hull)),
                    key=lambda k: ux * midpoint(p[hull[k]])[0]
                    + uy * midpoint(p[hull[k]])[1])
        ordered = hull[start:] + hull[:start]
        anchor, rest = ordered[0], ordered[1:]
        for mask in range(1 << len(rest)):
            selected = [rest[k] for k in range(len(rest)) if mask >> k & 1]
            if len(selected) < 2:
                continue
            # Exact midpoint arithmetic is only a search filter.  Rejection
            # still depends solely on checked_fan's full interval guards.
            arays = [sub(mids[j], mids[anchor]) for j in selected]
            if any(ux * r[0] + uy * r[1] <= 0 for r in arays):
                continue
            adets = [det(arays[k], arays[k + 1])
                     for k in range(len(arays) - 1)]
            if (not adets or min(adets) <= 0
                    or sum(adets, F(0)) / 2 <= TARGET):
                continue
            witness = selected + [d]
            cycle = [anchor] + witness
            if checked_fan(p, cycle) is not None:
                return cycle
    return None


ROOT = (F(1) - DIAMETER, DIAMETER, -DIAMETER, DIAMETER, F(-1), F(1))
SCALES = (2 * DIAMETER - 1, 2 * DIAMETER, F(2))


def descend(path):
    box = list(ROOT)
    for token in path:
        axis, side = map(int, token)
        i = 2 * axis
        middle = (box[i] + box[i + 1]) / 2
        if side == 0:
            box[i + 1] = middle
        else:
            box[i] = middle
    return tuple(box)


def split_axis(box):
    widths = [(box[2 * k + 1] - box[2 * k]) / SCALES[k] for k in range(3)]
    return max(range(3), key=lambda k: widths[k])


def produce(epsilon, square):
    stack = [(ROOT, "")]
    leaves = []
    while stack:
        box, path = stack.pop()
        p = points(box, epsilon, square)
        witness = diameter_witness(p)
        if witness is not None:
            leaves.append({"p": path, "d": witness})
            continue
        cycle = find_fan(p)
        if cycle is not None:
            leaves.append({"p": path, "f": cycle})
            continue
        axis = split_axis(box)
        i = 2 * axis
        middle = (box[i] + box[i + 1]) / 2
        left, right = list(box), list(box)
        left[i + 1], right[i] = middle, middle
        # Each path token records both split axis and child side.
        stack.append((tuple(right), path + str(axis) + "1"))
        stack.append((tuple(left), path + str(axis) + "0"))
    return leaves


def coverage_trie(leaves):
    trie = {}
    for leaf in leaves:
        node = trie
        path = leaf["p"]
        if len(path) % 2:
            raise RuntimeError("odd path length")
        for j in range(0, len(path), 2):
            if "leaf" in node:
                raise RuntimeError("leaf is a prefix of another leaf")
            token = path[j:j + 2]
            if token[0] not in "012" or token[1] not in "01":
                raise RuntimeError("bad path token")
            node = node.setdefault(token, {})
        if node:
            raise RuntimeError("another leaf is a prefix of this leaf")
        node["leaf"] = True

    def complete(node):
        if node.get("leaf"):
            return True
        keys = sorted(node)
        if len(keys) != 2 or keys[0][0] != keys[1][0] or {k[1] for k in keys} != {"0", "1"}:
            return False
        return all(complete(node[k]) for k in keys)

    if not complete(trie):
        raise RuntimeError("leaf paths do not form a complete binary cover")


def replay(leaves, epsilon, square):
    coverage_trie(leaves)
    counts = {"diameter": 0, "fan": 0}
    for leaf in leaves:
        box = descend([leaf["p"][j:j + 2] for j in range(0, len(leaf["p"]), 2)])
        p = points(box, epsilon, square)
        if "d" in leaf:
            if diameter_witness(p) != leaf["d"]:
                raise RuntimeError("invalid diameter leaf")
            counts["diameter"] += 1
        elif "f" in leaf:
            if checked_fan(p, leaf["f"]) is None:
                raise RuntimeError("invalid fan leaf")
            counts["fan"] += 1
        else:
            raise RuntimeError("leaf has no rejection witness")
    return counts


def document(radius, charts):
    return {"format": 2, "radius": str(radius), "diameter": str(DIAMETER),
            "target": str(TARGET), "charts": charts}


def replay_document(certificate, radius):
    expected_keys = {"format", "radius", "diameter", "target", "charts"}
    if set(certificate) != expected_keys:
        raise RuntimeError("unexpected top-level fields")
    if (certificate["format"] != 2 or F(certificate["radius"]) != radius
            or F(certificate["diameter"]) != DIAMETER
            or F(certificate["target"]) != TARGET):
        raise RuntimeError("certificate parameters do not match")
    if set(certificate["charts"]) != {"1", "-1"}:
        raise RuntimeError("certificate does not contain exactly two charts")
    square = square_points(radius)
    results = []
    for epsilon in (1, -1):
        leaves = certificate["charts"][str(epsilon)]
        results.append({"epsilon": epsilon, "leaves": len(leaves),
                        **replay(leaves, epsilon, square)})
    return results


def must_reject(certificate, radius, label):
    try:
        replay_document(certificate, radius)
    except (KeyError, RuntimeError, ValueError):
        return
    raise RuntimeError("adversarial mutation was accepted: " + label)


def adversarial_tests(certificate, radius):
    # A missing leaf destroys cover completeness.
    mutant = copy.deepcopy(certificate)
    mutant["charts"]["1"].pop()
    must_reject(mutant, radius, "missing leaf")

    # Exact duplicates and an explicit ancestor both violate prefix-freeness.
    mutant = copy.deepcopy(certificate)
    mutant["charts"]["1"].append(copy.deepcopy(mutant["charts"]["1"][0]))
    must_reject(mutant, radius, "duplicate leaf")
    mutant = copy.deepcopy(certificate)
    leaf = max(mutant["charts"]["1"], key=lambda q: len(q["p"]))
    ancestor = {"p": leaf["p"][:-2], "d": [6, 0]}
    mutant["charts"]["1"].append(ancestor)
    must_reject(mutant, radius, "prefix overlap")

    # Changing one child's recorded split axis leaves unmatched siblings.
    mutant = copy.deepcopy(certificate)
    path = mutant["charts"]["1"][0]["p"]
    old = path[:2]
    mutant["charts"]["1"][0]["p"] = str((int(old[0]) + 1) % 3) + old[1] + path[2:]
    must_reject(mutant, radius, "wrong split axis")

    # Header values are proof parameters, not advisory metadata.
    mutant = copy.deepcopy(certificate)
    mutant["diameter"] = str(DIAMETER - F(1, 1000))
    must_reject(mutant, radius, "inward diameter")
    mutant = copy.deepcopy(certificate)
    mutant["target"] = str(TARGET + F(1, 10**6))
    must_reject(mutant, radius, "changed target")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--radius", default="1/500")
    parser.add_argument("--write", help="produce certificate JSON")
    parser.add_argument("--replay", help="replay certificate JSON")
    parser.add_argument("--self-test", action="store_true",
                        help="also require six damaged certificates to fail")
    args = parser.parse_args()
    radius = F(args.radius)
    if args.write:
        square = square_points(radius)
        charts = {}
        for epsilon in (1, -1):
            leaves = produce(epsilon, square)
            charts[str(epsilon)] = leaves
            print({"epsilon": epsilon, "leaves": len(leaves),
                   **replay(leaves, epsilon, square)})
        certificate = document(radius, charts)
        with open(args.write, "w", encoding="ascii") as handle:
            json.dump(certificate, handle, separators=(",", ":"), sort_keys=True)
    elif args.replay:
        with open(args.replay, encoding="ascii") as handle:
            certificate = json.load(handle)
        for result in replay_document(certificate, radius):
            print(result)
    else:
        parser.error("choose --write or --replay")
    if args.self_test:
        adversarial_tests(certificate, radius)
        print({"adversarial_tests": "PASS", "mutations_rejected": 6})


if __name__ == "__main__":
    main()
