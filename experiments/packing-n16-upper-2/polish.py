"""High-precision polish of the n = 16 maximin configuration.

Takes the float solution from search.py, extracts the active set (20 pair contacts + 13 wall
incidences on the 15 jammed points; point 13 is a rattler and is held fixed), and runs
Gauss-Newton in mpmath (dps 60) on the overdetermined-but-consistent system

    ||p_i - p_j||^2 = m^2          for each contact (20 eqs)
    y_i = 0 / sqrt3*x_i - y_i = 0 / sqrt3*(1-x_i) - y_i = 0   for each wall incidence (13 eqs)

in the 31 unknowns (30 core coordinates + m).  At the optimum all 33 equations hold exactly, so
Gauss-Newton converges quadratically; the final residual norm is reported and bounds the
truncation error of the printed coordinates.

Output: out/n16-polished.json with 50-digit coordinate strings, m, a = 1/m, s = 2/m + 2*sqrt3.
"""
from __future__ import annotations

import json

from mpmath import mp, mpf, matrix, sqrt, lu_solve, norm, nstr

mp.dps = 60

RATTLER = 13


def load(path: str):
    with open(path) as fh:
        d = json.load(fh)
    pts = [[mpf(repr(c)) for c in p] for p in d["points_unit_triangle"]]
    m = mpf(repr(d["best_m"]))
    return pts, m


def active_set(pts, m, tol=mpf("1e-7")):
    n = len(pts)
    contacts, walls = [], []
    s3 = sqrt(mpf(3))
    for i in range(n):
        if i == RATTLER:
            continue
        for j in range(i + 1, n):
            if j == RATTLER:
                continue
            dist2 = (pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2
            if abs(sqrt(dist2) - m) < tol:
                contacts.append((i, j))
        x, y = pts[i]
        if abs(y) < tol:
            walls.append((i, "bottom"))
        if abs(s3 * x - y) < tol:
            walls.append((i, "left"))
        if abs(s3 * (1 - x) - y) < tol:
            walls.append((i, "right"))
    return contacts, walls


def gauss_newton(pts, m, contacts, walls, iters=12):
    s3 = sqrt(mpf(3))
    core = [i for i in range(len(pts)) if i != RATTLER]
    pos = {p: k for k, p in enumerate(core)}          # point -> slot
    nu = 2 * len(core) + 1                            # unknowns
    ne = len(contacts) + len(walls)

    def unpack(u):
        P = {i: (u[2 * pos[i]], u[2 * pos[i] + 1]) for i in core}
        return P, u[nu - 1]

    u = matrix(nu, 1)
    for i in core:
        u[2 * pos[i]] = pts[i][0]
        u[2 * pos[i] + 1] = pts[i][1]
    u[nu - 1] = m

    for it in range(iters):
        P, mm = unpack(u)
        F = matrix(ne, 1)
        J = matrix(ne, nu)
        r = 0
        for (i, j) in contacts:
            dx = P[i][0] - P[j][0]
            dy = P[i][1] - P[j][1]
            F[r] = dx * dx + dy * dy - mm * mm
            J[r, 2 * pos[i]] = 2 * dx
            J[r, 2 * pos[i] + 1] = 2 * dy
            J[r, 2 * pos[j]] = -2 * dx
            J[r, 2 * pos[j] + 1] = -2 * dy
            J[r, nu - 1] = -2 * mm
            r += 1
        for (i, w) in walls:
            x, y = P[i]
            if w == "bottom":
                F[r] = y
                J[r, 2 * pos[i] + 1] = 1
            elif w == "left":
                F[r] = s3 * x - y
                J[r, 2 * pos[i]] = s3
                J[r, 2 * pos[i] + 1] = -1
            else:
                F[r] = s3 * (1 - x) - y
                J[r, 2 * pos[i]] = -s3
                J[r, 2 * pos[i] + 1] = -1
            r += 1
        res = norm(F)
        # normal equations
        JT = J.T
        A = JT * J
        b = JT * F
        try:
            delta = lu_solve(A, b)
        except ZeroDivisionError:
            print("singular normal matrix at iter", it)
            break
        u = u - delta
        print(f"iter {it}: |F| = {nstr(res, 5)}  |delta| = {nstr(norm(delta), 5)}  m = {nstr(u[nu-1], 30)}")
        if res < mpf("1e-55"):
            break
    P, mm = unpack(u)
    out = [list(pts[i]) if i == RATTLER else [P[i][0], P[i][1]] for i in range(len(pts))]
    return out, mm, res


def main():
    pts, m0 = load("out/n16.json")
    contacts, walls = active_set(pts, m0)
    print(f"active set: {len(contacts)} contacts, {len(walls)} wall incidences, "
          f"unknowns = {2 * (len(pts) - 1) + 1}")
    pts2, m, res = gauss_newton(pts, m0, contacts, walls)
    # verify full configuration at high precision: min pairwise distance and containment
    s3 = sqrt(mpf(3))
    mind = mpf(10)
    for i in range(16):
        for j in range(i + 1, 16):
            dd = sqrt((pts2[i][0] - pts2[j][0]) ** 2 + (pts2[i][1] - pts2[j][1]) ** 2)
            mind = min(mind, dd)
    viol = min(min(p[1] for p in pts2),
               min(s3 * p[0] - p[1] for p in pts2),
               min(s3 * (1 - p[0]) - p[1] for p in pts2))
    print("min pairwise distance :", nstr(mind, 40))
    print("m (system)            :", nstr(m, 40))
    print("worst containment slack (>=0 required, up to residual):", nstr(viol, 5))
    print("a = 1/m               :", nstr(1 / m, 40))
    print("s = 2/m + 2*sqrt3     :", nstr(2 / m + 2 * s3, 40))
    with open("out/n16-polished.json", "w") as fh:
        json.dump({
            "dps": mp.dps,
            "m": nstr(m, 50),
            "a": nstr(1 / m, 50),
            "s": nstr(2 / m + 2 * s3, 50),
            "final_residual": nstr(res, 5),
            "rattler": RATTLER,
            "contacts": contacts,
            "walls": walls,
            "points_unit_triangle": [[nstr(p[0], 50), nstr(p[1], 50)] for p in pts2],
        }, fh, indent=1)


if __name__ == "__main__":
    main()
