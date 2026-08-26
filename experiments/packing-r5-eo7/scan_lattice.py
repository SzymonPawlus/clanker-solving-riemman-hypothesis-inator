"""Direct measurement: max number of points of a unit-separation LATTICE (any
translate) inside T(a) for a slightly below the Erdos-Oler threshold.

This is the quantity AE reports as "22" at k = 7.  Reproduced here from scratch.
Floats are used for the SEARCH only; the reported optimum is re-checked in exact
rational arithmetic by `exact_check.py`.  STATUS: numerical.
"""
import numpy as np, math, json, sys

SQ3 = math.sqrt(3.0)


def best_for_shape(phi, x, h, a, ng=48, idx=None):
    """Max over translations of |(Lambda+t) cap T(a)| for the lattice
    v1 = e1(phi), v2 = x*e1 + h*e2 (so lambda_1 = 1 provided |v2|,|v2 +- v1| >= 1)."""
    e1 = np.array([math.cos(phi), math.sin(phi)])
    e2 = np.array([-math.sin(phi), math.cos(phi)])
    v1 = e1
    v2 = x * e1 + h * e2
    if idx is None:
        m = int(a / min(1.0, h)) + 3
        idx = np.array([(i, j) for i in range(-m, m + 1) for j in range(-m, m + 1)])
    P = idx[:, 0:1] * v1[None, :] + idx[:, 1:2] * v2[None, :]        # (K,2)
    ab = np.stack(np.meshgrid(np.arange(ng) / ng, np.arange(ng) / ng, indexing="ij"), -1).reshape(-1, 2)
    T = ab[:, 0:1] * v1[None, :] + ab[:, 1:2] * v2[None, :]           # (G,2)
    X = P[None, :, 0] + T[:, 0:1]
    Y = P[None, :, 1] + T[:, 1:2]
    ok = (Y >= 0) & (SQ3 * X - Y >= 0) & (SQ3 * (a - X) - Y >= 0)
    cnt = ok.sum(axis=1)
    k = int(cnt.argmax())
    return int(cnt[k]), (float(ab[k, 0]), float(ab[k, 1]))


def scan(a, nphi=31, nx=6, nh=24, ng=48):
    best = (-1, None)
    rows = []
    for ip in range(nphi):
        phi = (math.pi / 3.0) * ip / nphi
        for ix in range(nx):
            x = 0.5 * ix / (nx - 1)
            hmin = math.sqrt(max(0.0, 1.0 - x * x))
            for ih in range(nh):
                h = hmin + (a - hmin) * (ih / nh) ** 2
                c, ab = best_for_shape(phi, x, h, a, ng)
                if c > best[0]:
                    best = (c, (phi, x, h, ab))
                    rows.append({"count": c, "phi": phi, "x": x, "h": h, "alpha": ab[0], "beta": ab[1]})
    return best, rows


if __name__ == "__main__":
    a = float(sys.argv[1]) if len(sys.argv) > 1 else 6.0 - 1e-6
    best, rows = scan(a)
    print("a =", a, " max lattice count =", best[0])
    print("  phi=%.6f (deg %.4f) x=%.4f h=%.6f alpha=%.4f beta=%.4f"
          % (best[1][0], math.degrees(best[1][0]), best[1][1], best[1][2], best[1][3][0], best[1][3][1]))
    json.dump({"a": a, "best": best[0], "record": rows[-8:]}, open("out/lattice_scan_%g.json" % a, "w"), indent=1)
