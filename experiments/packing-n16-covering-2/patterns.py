"""Targeted structure generator: build the FORCED 3 corner + 9 edge + 3 interior layout
from explicit site patterns, vary the arrangement of the three interior pieces (which is
the one genuinely free choice), take the power diagram, and run the SLP on each.

FLOATS ONLY -- search stage.
"""
import math, random, sys, json
import gen, comb, slp

SQ3 = math.sqrt(3.0)
CX, CY = 0.5, SQ3 / 6


def sites(dc, de, p1, p2, p3, rho, th, jit, rng):
    """3 corner sites, 9 edge sites (3 per side), 3 interior sites on a circle"""
    A = (0.0, 0.0); B = (1.0, 0.0); C = (0.5, SQ3 / 2)
    S = []
    for (P, Q, R) in ((A, B, C), (B, C, A), (C, A, B)):
        # corner site: along the bisector from P towards the incentre
        bx, by = (Q[0] + R[0]) / 2 - P[0], (Q[1] + R[1]) / 2 - P[1]
        L = math.hypot(bx, by)
        S.append((P[0] + dc * bx / L, P[1] + dc * by / L))
    for (P, Q) in ((A, B), (B, C), (C, A)):
        ex, ey = Q[0] - P[0], Q[1] - P[1]
        nx, ny = CX - (P[0] + Q[0]) / 2, CY - (P[1] + Q[1]) / 2
        nl = math.hypot(nx, ny)
        for s in (p1, p2, p3):
            S.append((P[0] + s * ex + de * nx / nl, P[1] + s * ey + de * ny / nl))
    if th >= 0:
        for k in range(3):
            ang = th + 2 * math.pi * k / 3
            S.append((CX + rho * math.cos(ang), CY + rho * math.sin(ang)))
    else:
        # asymmetric placement of the three interior sites (e.g. in a row)
        for k in range(3):
            r = rho * rng.uniform(0.0, 1.6)
            ang = rng.uniform(0, 2 * math.pi)
            S.append((CX + r * math.cos(ang), CY + r * math.sin(ang)))
    return [(x + rng.gauss(0, jit), y + rng.gauss(0, jit)) for (x, y) in S]


def main():
    seed = int(sys.argv[1]); ntry = int(sys.argv[2]); out = sys.argv[3]
    rng = random.Random(seed)
    best = 0.0; seen = {}
    for it in range(ntry):
        dc = rng.uniform(0.10, 0.30)
        de = rng.uniform(0.06, 0.22)
        p1 = rng.uniform(0.14, 0.30); p3 = 1.0 - p1 + rng.gauss(0, 0.02)
        p2 = 0.5 + rng.gauss(0, 0.05)
        rho = rng.uniform(0.02, 0.24)
        th = rng.uniform(0, 2 * math.pi / 3) if rng.random() > 0.4 else -1.0
        jit = rng.choice([0.0, 0.0, 0.004, 0.015])
        w = [rng.gauss(0, 0.002) for _ in range(15)]
        S = gen.build_struct(sites(dc, de, p1, p2, p3, rho, th, jit, rng), w)
        if S is None:
            continue
        sg = gen.signature(S)
        try:
            v = S.run(iters=300, abort_below=1.0 / 4.40 ** 2, abort_at=70)
        except Exception:
            continue
        am = 1.0 / math.sqrt(v)
        if sg not in seen or am > seen[sg]:
            seen[sg] = am
        if am > best:
            best = am
            S.dump(out, {"seed": seed, "it": it, "sig": str(sg),
                         "params": [dc, de, p1, p2, p3, rho, th]})
            print("it %5d  a_max %.9f  *  th=%.3f rho=%.3f  sig %s"
                  % (it, am, th, rho, sg), flush=True)
        elif it % 200 == 0:
            print("it %5d  a_max %.9f (best %.9f)" % (it, am, best), flush=True)
    print("SEED %d BEST %.9f  distinct structures %d" % (seed, best, len(seen)))
    top = sorted(seen.items(), key=lambda kv: -kv[1])[:25]
    json.dump([[str(k), v] for k, v in top], open(out.replace(".json", "_sigs.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
