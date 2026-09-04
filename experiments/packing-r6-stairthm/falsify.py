"""FALSIFICATION SEARCH at n = 60: is there a packing better than 16 + 4 sqrt3?

The staircase law predicts s(60) <= 16 + 4*sqrt3, i.e. d(60) <= 16 + 2*sqrt3
= 19.46410161513775...  If a search finds a FEASIBLE 60-point packing with a
strictly smaller d, the "law" is not a law and that is the headline finding.

Normalisation used here (search only).  Put n points in the UNIT equilateral
triangle A=(0,0), B=(1,0), C=(1/2, sqrt3/2) and maximise
      m = min over pairs of |p_i - p_j| .
Scaling by 2/m turns this into a separation-2 packing in a triangle of side
      d = 2/m .
So beating the law needs  m > 2/(16+2 sqrt3) = 0.10275268...

FLOATS ARE USED FOR SEARCH GUIDANCE ONLY.  Any candidate that appears to beat the
law is re-examined exactly; nothing here can accept a packing on its own.

Method: repulsion relaxation ("inflate and shove") with random restarts plus
perturbation restarts from the incumbent.  Deterministic given the seed.
"""
import numpy as np, sys, time, json, os

SQ3 = np.sqrt(3.0)
V = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, SQ3 / 2]])
D_LAW = 16 + 2 * SQ3
M_LAW = 2.0 / D_LAW


# --- containment: nearest point of the closed triangle ----------------------
def _proj_seg(P, a, b):
    ab = b - a
    t = np.clip(((P - a) @ ab) / (ab @ ab), 0.0, 1.0)
    return a + t[:, None] * ab


def project(P):
    """Project every point onto the closed unit triangle (exact nearest point)."""
    # barycentric test
    v0 = V[1] - V[0]; v1 = V[2] - V[0]
    d00 = v0 @ v0; d01 = v0 @ v1; d11 = v1 @ v1
    v2 = P - V[0]
    d20 = v2 @ v0; d21 = v2 @ v1
    den = d00 * d11 - d01 * d01
    u = (d11 * d20 - d01 * d21) / den
    v = (d00 * d21 - d01 * d20) / den
    inside = (u >= 0) & (v >= 0) & (u + v <= 1)
    if inside.all():
        return P
    out = P.copy()
    idx = ~inside
    Q = P[idx]
    best = None
    for (a, b) in ((V[0], V[1]), (V[1], V[2]), (V[2], V[0])):
        R = _proj_seg(Q, a, b)
        dd = ((R - Q) ** 2).sum(1)
        if best is None:
            best, bd = R, dd
        else:
            m = dd < bd
            best[m] = R[m]; bd[m] = dd[m]
    out[idx] = best
    return out


def min_pair(P):
    D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
    np.fill_diagonal(D, np.inf)
    return D.min(), D


def relax(P, t, iters=300):
    n = len(P)
    for _ in range(iters):
        d = P[:, None, :] - P[None, :, :]
        D = np.linalg.norm(d, axis=2)
        np.fill_diagonal(D, np.inf)
        bad = D < t
        if not bad.any():
            P = project(P)
            break
        with np.errstate(invalid="ignore", divide="ignore"):
            w = np.where(bad, (t - D) / np.maximum(D, 1e-12), 0.0)
        disp = (w[:, :, None] * d).sum(axis=1) * 0.5
        P = project(P + disp)
    return P


def grow(P, rng, rounds=45):
    """Push the achievable min distance up as far as the relaxation can take it."""
    m, _ = min_pair(P)
    step = 0.02 * m + 1e-4
    for _ in range(rounds):
        t = m + step
        Q = relax(P.copy(), t, iters=160)
        mq, _ = min_pair(Q)
        if mq > m + 1e-12:
            P, m = Q, mq
            step *= 1.4
        else:
            step *= 0.45
            if step < 1e-10:
                break
    return P, m


def random_start(n, rng):
    a = rng.random((n, 2))
    m = a.sum(1) > 1
    a[m] = 1 - a[m]
    return a[:, 0:1] * V[1] + a[:, 1:2] * V[2]


def construction_start():
    """The staircase configuration itself, scaled into the unit triangle."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import gen
    pts = gen.points(8)
    d = gen.d_of(8).f()
    return np.array([[p[0].f() / d, p[1].f() / d] for p in pts])


def main(n=60, budget_s=900, seed=20260826):
    rng = np.random.default_rng(seed)
    t0 = time.time()
    print("n = %d   law: d = 16 + 2 sqrt3 = %.15f   m_law = %.15f" % (n, D_LAW, M_LAW))

    P0 = construction_start()
    m0, _ = min_pair(P0)
    print("sanity: the construction itself scores m = %.15f  (d = %.12f, law %.12f)"
          % (m0, 2 / m0, D_LAW))
    P0g, m0g = grow(P0.copy(), rng)
    print("        relaxation started AT the construction reaches m = %.15f -> d = %.12f"
          % (m0g, 2 / m0g))

    best_m, best_P = m0, P0
    tries = 0
    hist = []
    while time.time() - t0 < budget_s * 0.6:
        tries += 1
        P = random_start(n, rng)
        P, m = grow(P, rng)
        if m > best_m:
            best_m, best_P = m, P
        hist.append(m)
    print("random restarts: %d, best m = %.15f -> d = %.12f (law %.12f)"
          % (tries, best_m, 2 / best_m, D_LAW))
    if hist:
        h = np.sort(np.array(hist))[::-1]
        print("   top-10 random-restart m: %s" % np.array2string(h[:10], precision=9))

    # perturbation restarts from the incumbent
    pert = 0
    while time.time() - t0 < budget_s:
        pert += 1
        scale = 10 ** rng.uniform(-3, -1.2)
        P = project(best_P + rng.normal(0, scale, best_P.shape))
        P, m = grow(P, rng)
        if m > best_m + 1e-13:
            best_m, best_P = m, P
    print("perturbation restarts: %d, best m = %.15f -> d = %.12f" % (pert, best_m, 2 / best_m))

    gap = 2 / best_m - D_LAW
    print()
    print("BEST FOUND d = %.12f   LAW d = %.12f   (best - law) = %+.3e" % (2 / best_m, D_LAW, gap))
    if gap < -1e-7:
        print("*** SEARCH CLAIMS TO BEAT THE LAW.  Candidate written to out/n60_candidate.json.")
        print("*** This is a FLOAT result and certifies nothing; it must be re-checked exactly.")
        json.dump({"n": n, "d_float": 2 / best_m, "points_unit_triangle": best_P.tolist(),
                   "seed": seed},
                  open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "out", "n60_candidate.json"), "w"), indent=1)
    else:
        print("No packing better than the law was found.  The law SURVIVES this search.")
        print("(A failed search is evidence, never a lower bound: it does NOT show")
        print(" s(60) = 16 + 4 sqrt3.  Optimality at n = 60 remains open.)")
    return best_m


if __name__ == "__main__":
    b = int(sys.argv[1]) if len(sys.argv) > 1 else 900
    main(budget_s=b)
