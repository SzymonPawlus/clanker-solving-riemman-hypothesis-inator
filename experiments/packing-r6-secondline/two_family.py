"""The TWO-family count: M(a) = max over unit-separation lattices of |(L+t) cap T(a)|.

This is the count r5-eo7's relaxation throws away.  Its one-family bound is
    B(a) = max over (phi, h, theta) of  sum_j cap(ell_j),
i.e. each strip is allowed its own worst offset.  For a lattice the strip offsets are NOT
independent: with a Lagrange-reduced basis v1 (along the lines) and v2 = beta*|v1|*u + h*n,
the offset of strip j is  x_j = x_0 + j*beta  (mod 1).  An arithmetic progression.  So

    B(a)  =  offsets free per strip           (one family)
    M(a)  =  offsets forced into an AP        (two families)

and B(a) - M(a) is EXACTLY the inter-strip interaction that the one-family count is blind to.

Written independently of experiments/packing-r5-eo7/scan_lattice.py.
STATUS: numerical (float grid measurement).  Nothing here is assumable.
"""
import json, math, sys, time
import numpy as np
from geom2 import SQRT3, in_triangle


def lattice_points(v1, v2, a, margin=2.5):
    """All i*v1 + j*v2 landing in a disc that covers T(a) plus a fundamental domain."""
    cen = np.array([a / 2.0, a / (2.0 * SQRT3)])
    R = a / SQRT3 + margin + np.linalg.norm(v1) + np.linalg.norm(v2)
    M = np.array([v1, v2]).T
    Minv = np.linalg.inv(M)
    # bound the index box
    B = int(math.ceil(np.abs(Minv).sum(axis=1).max() * (R + np.linalg.norm(cen)) + 2))
    ii, jj = np.meshgrid(np.arange(-B, B + 1), np.arange(-B, B + 1), indexing="ij")
    V = ii.ravel()[:, None] * v1[None, :] + jj.ravel()[:, None] * v2[None, :]
    keep = ((V - cen) ** 2).sum(axis=1) <= R * R
    return V[keep]


def count_max_over_t(v1, v2, a, nt=32):
    """max over translations t of |(L + t) cap T(a)|, measured on an nt x nt grid of t."""
    V = lattice_points(v1, v2, a)
    s = np.arange(nt) / nt          # includes 0: the exactly-aligned translate matters
    S, U = np.meshgrid(s, s, indexing="ij")
    Tg = S.ravel()[:, None] * v1[None, :] + U.ravel()[:, None] * v2[None, :]
    best, arg = 0, None
    CH = max(1, int(4e6 // max(1, len(V))))
    for st in range(0, len(Tg), CH):
        P = V[None, :, :] + Tg[st:st + CH, None, :]
        c = in_triangle(P, a, tol=1e-9).sum(axis=1)
        k = int(c.argmax())
        if c[k] > best:
            best, arg = int(c[k]), Tg[st + k].copy()
    return best, arg


def refine_t(v1, v2, a, t0, rounds=3, nt=17, span=None):
    """Local refinement of the translation, and a boundary snap."""
    span = span if span is not None else 0.5 * (np.linalg.norm(v1) + np.linalg.norm(v2))
    V = lattice_points(v1, v2, a)
    best, arg = 0, t0
    for _ in range(rounds):
        g = np.linspace(-span, span, nt)
        X, Y = np.meshgrid(g, g, indexing="ij")
        Tg = arg[None, :] + np.stack([X.ravel(), Y.ravel()], axis=1)
        P = V[None, :, :] + Tg[:, None, :]
        c = in_triangle(P, a, tol=1e-9).sum(axis=1)
        k = int(c.argmax())
        if c[k] >= best:
            best, arg = int(c[k]), Tg[k].copy()
        span /= 6.0
    return best, arg


def sweep(a, nphi=46, nbeta=11, nh=18, hmax=2.6, nt=32, log=None):
    best, arg = 0, None
    t0 = time.time()
    for ip in range(nphi):
        p = (np.pi / 3.0) * ip / (nphi - 1)
        u = np.array([math.cos(p), math.sin(p)])
        n = np.array([-math.sin(p), math.cos(p)])
        for ib in range(nbeta):
            beta = 0.5 * ib / (nbeta - 1)
            hmin = math.sqrt(max(0.75, 1.0 - beta * beta))
            for ih in range(nh):
                h = hmin + (hmax - hmin) * ih / (nh - 1)
                v1, v2 = u, beta * u + h * n
                c, t = count_max_over_t(v1, v2, a, nt=nt)
                if c > best:
                    best, arg = c, (p, beta, h, t)
                    if log:
                        print(json.dumps({"a": a, "count": c, "phi_deg": math.degrees(p),
                                          "beta": beta, "h": h, "t": list(map(float, t)),
                                          "sec": round(time.time() - t0, 1)}), flush=True)
    # refine the winner
    p, beta, h, t = arg
    u = np.array([math.cos(p), math.sin(p)]); n = np.array([-math.sin(p), math.cos(p)])
    r, tr = refine_t(u, beta * u + h * n, a, t)
    return max(best, r), {"phi_deg": math.degrees(p), "beta": beta, "h": h,
                          "t_refined": list(map(float, tr)), "count_refined": r}


if __name__ == "__main__":
    aa = [float(x) for x in sys.argv[1:]] or [6.0, 5.999999, 5.9]
    rows = []
    for a in aa:
        c, info = sweep(a, log=True)
        rows.append({"a": a, "M_measured": c, **info})
        print(json.dumps(rows[-1]), flush=True)
        json.dump(rows, open("out/two_family_M.json", "w"), indent=1)
