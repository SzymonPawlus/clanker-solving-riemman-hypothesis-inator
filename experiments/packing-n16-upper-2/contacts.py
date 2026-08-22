"""Contact-graph / rattler / isostaticity analysis of a maximin configuration.

Reads a search.py output JSON, prints: contact pairs (distance within tol of m), wall contacts,
per-point contact counts, rattler identification, and the constraint-vs-dof count for the jammed
subset. Independent implementation for attack n16-upper-2; written without reading the
n16-structure lane's code.
"""
from __future__ import annotations

import json
import math
import sys

SQRT3 = math.sqrt(3.0)


def analyse(path: str, tol: float = 1e-9) -> dict:
    with open(path) as fh:
        d = json.load(fh)
    pts = d["points_unit_triangle"]
    n = len(pts)
    m = d["best_m"]
    contacts = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
            if dist <= m * (1 + tol):
                contacts.append((i, j, dist))
    walls = []  # (point, wall) with wall in {bottom,left,right}
    for i, (x, y) in enumerate(pts):
        if y <= m * tol:
            walls.append((i, "bottom", y))
        g = (SQRT3 * x - y) / 2.0  # true distance to left edge
        if g <= m * tol:
            walls.append((i, "left", g))
        g = (SQRT3 * (1 - x) - y) / 2.0
        if g <= m * tol:
            walls.append((i, "right", g))
    deg = [0] * n
    for i, j, _ in contacts:
        deg[i] += 1
        deg[j] += 1
    wdeg = [0] * n
    for i, _, _ in walls:
        wdeg[i] += 1
    total_deg = [deg[i] + wdeg[i] for i in range(n)]
    # rattler = point that could be removed without changing the jammed core: heuristically,
    # a point whose removal leaves every remaining point with >= 3 total contacts and which
    # itself has too few contacts to be pinned (< 3 non-collinear constraints).
    rattlers = [i for i in range(n) if total_deg[i] < 3]
    core = [i for i in range(n) if i not in rattlers]
    core_contacts = [(i, j) for i, j, _ in contacts if i in core and j in core]
    core_walls = [(i, w) for i, w, _ in walls if i in core]
    report = {
        "n": n, "m": m,
        "contacts": [(i, j, f"{dist:.15f}") for i, j, dist in contacts],
        "n_contacts": len(contacts),
        "walls": [(i, w, f"{g:.2e}") for i, w, g in walls],
        "n_walls": len(walls),
        "degrees(pair+wall)": total_deg,
        "rattlers": rattlers,
        "rattler_degrees": {i: (deg[i], wdeg[i]) for i in rattlers},
        "core_size": len(core),
        "core_constraints": len(core_contacts) + len(core_walls),
        "core_dof": 2 * len(core),
        "isostatic_core": len(core_contacts) + len(core_walls) == 2 * len(core),
    }
    return report


if __name__ == "__main__":
    rep = analyse(sys.argv[1], tol=float(sys.argv[2]) if len(sys.argv) > 2 else 1e-9)
    print(json.dumps(rep, indent=1))
