"""Plausibility probe for the forcing hypothesis (H3) of the write-up.

(H3) claims: every 1-separated 27-point set in T(a), a close to 6, lies within delta of
some family of equally spaced parallel lines with spacing h >= sqrt3/2.  The certified
counting theorem consumes exactly that hypothesis.  Here we MEASURE the line defect

    delta(P) = min over unit normal n, spacing h >= sqrt3/2, offset tau
               of  max_p  dist( <p,n>, tau + h Z ),

on 27-point 1-separated configurations in T(6) -- which exist, unlike at a < 6, so the
hypothesis has non-vacuous content there.  Large observed defects REFUTE (H3) for small
delta.  Floats; STATUS: numerical, evidence only.
"""
import numpy as np, math, json, sys

SQ3 = math.sqrt(3.0)
rng = np.random.default_rng(20260824)


def inside(P, a):
    X, Y = P[:, 0], P[:, 1]
    return (Y >= -1e-12) & (SQ3 * X - Y >= -1e-12) & (SQ3 * (a - X) - Y >= -1e-12)


def project_in(P, a):
    """Push points back into T(a) (used inside the relaxation)."""
    P = P.copy()
    for _ in range(30):
        Y = P[:, 1]; X = P[:, 0]
        P[:, 1] = np.maximum(Y, 0.0)
        d = (SQ3 * P[:, 0] - P[:, 1]) / 2.0
        bad = d < 0
        P[bad, 0] -= d[bad] * SQ3 / 2; P[bad, 1] += d[bad] / 2
        d = (SQ3 * (a - P[:, 0]) - P[:, 1]) / 2.0
        bad = d < 0
        P[bad, 0] += d[bad] * SQ3 / 2; P[bad, 1] += d[bad] / 2
    return P


def relax(P, a, iters=4000):
    """Push apart until 1-separated (or give up)."""
    n = len(P)
    for _ in range(iters):
        D = P[:, None, :] - P[None, :, :]
        d = np.linalg.norm(D, axis=2) + np.eye(n)
        viol = 1.0 - d
        if viol.max() <= 1e-9:
            return project_in(P, a), True
        w = np.clip(viol, 0, None) / d
        step = (D * w[:, :, None]).sum(axis=1) * 0.35
        P = project_in(P + step, a)
    D = P[:, None, :] - P[None, :, :]
    d = np.linalg.norm(D, axis=2) + np.eye(n)
    return P, d.min() >= 1 - 1e-9


def line_defect(P, nang=360, nh=400):
    best = 1e9; arg = None
    for ia in range(nang):
        th = math.pi * ia / nang
        z = P[:, 0] * (-math.sin(th)) + P[:, 1] * math.cos(th)
        z = z - z.min()
        span = z.max()
        for ih in range(nh):
            h = SQ3 / 2 + (max(span, SQ3 / 2 + 1e-9) - SQ3 / 2) * ih / nh
            # best offset for this h: minimise max distance to tau + hZ
            f = np.sort((z / h) % 1.0)
            # largest gap on the circle gives the best centring
            gaps = np.diff(np.concatenate([f, [f[0] + 1.0]]))
            g = gaps.max()
            d = h * (1.0 - g) / 2.0
            if d < best:
                best = d; arg = (th, h)
    return best, arg


def lattice27(a=6.0):
    pts = []
    for j in range(7):
        for i in range(7 - j):
            pts.append((i + j / 2.0, j * SQ3 / 2.0))
    P = np.array(pts)                      # 28 points, the T(7) lattice in T(6)
    return P


if __name__ == "__main__":
    a = 6.0
    out = {"a": a, "trials": []}
    L = lattice27(a)
    d0, arg0 = line_defect(np.delete(L, 27, axis=0))
    print("control: T(7) lattice minus apex, 27 pts, line defect = %.3e (expect 0)" % d0)
    out["control_lattice_defect"] = d0
    ok = 0
    for trial in range(int(sys.argv[1]) if len(sys.argv) > 1 else 40):
        P = np.column_stack([rng.uniform(0, a, 60), rng.uniform(0, a * SQ3 / 2, 60)])
        P = P[inside(P, a)][:27]
        if len(P) < 27:
            continue
        P, good = relax(P, a)
        D = P[:, None, :] - P[None, :, :]
        dmin = (np.linalg.norm(D, axis=2) + np.eye(27)).min()
        if dmin < 1 - 1e-7 or not inside(P, a).all():
            continue
        ok += 1
        d, arg = line_defect(P)
        out["trials"].append({"min_sep": float(dmin), "line_defect": float(d),
                              "theta": float(arg[0]), "h": float(arg[1])})
        print("feasible 27-pt config #%d: min sep %.6f, line defect %.4f" % (ok, dmin, d), flush=True)
    if out["trials"]:
        ds = [t["line_defect"] for t in out["trials"]]
        print("n=%d  defect: min %.4f  median %.4f  max %.4f" %
              (len(ds), min(ds), float(np.median(ds)), max(ds)))
        out["summary"] = {"n": len(ds), "min": min(ds), "median": float(np.median(ds)), "max": max(ds)}
    json.dump(out, open("out/forcing_probe.json", "w"), indent=1)


def stress(a=6.0, trials=200, amps=(0.05, 0.1, 0.2, 0.35, 0.5)):
    """Deliberate falsification attempt for (H3): jitter the lattice-minus-a-point,
    relax back to feasibility, and see how large a line defect survives."""
    L = lattice27(a)
    best = []
    for amp in amps:
        bd = 0.0; bcfg = None
        for _ in range(trials):
            drop = rng.integers(0, 28)
            P = np.delete(L, drop, axis=0) + rng.normal(0, amp, (27, 2))
            P, good = relax(P, a, iters=2500)
            D = P[:, None, :] - P[None, :, :]
            dmin = (np.linalg.norm(D, axis=2) + np.eye(27)).min()
            if dmin < 1 - 1e-7 or not inside(P, a).all():
                continue
            d, _ = line_defect(P, nang=180, nh=200)
            if d > bd:
                bd = d; bcfg = (float(dmin), float(d))
        best.append({"amp": amp, "max_line_defect": bd, "cfg": bcfg})
        print("jitter %.2f -> max sustained line defect %.4f" % (amp, bd), flush=True)
    return best
