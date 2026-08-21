"""Generate combinatorial structures (convex subdivisions of T_1 into 15 faces) and run
the SLP minimax optimiser on each.  FLOATS ONLY -- search stage.

Structures come from power diagrams of jittered lattices clipped to T_1 (a rich family:
every power diagram clipped to a convex region is a convex subdivision), plus local
combinatorial moves on the best ones.
"""
import json, math, os, random, sys
import slp
from slp import Struct, plane_to_uv

SQ3 = math.sqrt(3.0)


# ---------- power diagram of the unit triangle, in plane coordinates ----------

def tri1():
    return [(0.0, 0.0), (1.0, 0.0), (0.5, SQ3 / 2)]


def clip(poly, nx, ny, c):
    out = []
    m = len(poly)
    for i in range(m):
        p = poly[i]; q = poly[(i + 1) % m]
        dp = nx * p[0] + ny * p[1] - c
        dq = nx * q[0] + ny * q[1] - c
        if dp <= 0: out.append(p)
        if (dp > 0) != (dq > 0):
            t = dp / (dp - dq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    res = []
    for p in out:
        if not res or abs(res[-1][0] - p[0]) > 1e-13 or abs(res[-1][1] - p[1]) > 1e-13:
            res.append(p)
    if len(res) > 1 and abs(res[0][0] - res[-1][0]) < 1e-13 and abs(res[0][1] - res[-1][1]) < 1e-13:
        res.pop()
    return res


def power_cells(sites, weights):
    T = tri1()
    cells = []
    for i, (xi, yi) in enumerate(sites):
        poly = T
        for j, (xj, yj) in enumerate(sites):
            if i == j: continue
            nx = 2 * (xj - xi); ny = 2 * (yj - yi)
            c = (xj * xj + yj * yj - weights[j]) - (xi * xi + yi * yi - weights[i])
            poly = clip(poly, nx, ny, c)
            if len(poly) < 3: break
        cells.append(poly if len(poly) >= 3 else [])
    return cells


def build_struct(sites, weights, tol=1e-9):
    cells = power_cells(sites, weights)
    if any(len(c) < 3 for c in cells):
        return None
    V = []
    def vid(p):
        for k, q in enumerate(V):
            if abs(q[0] - p[0]) < 1e-7 and abs(q[1] - p[1]) < 1e-7:
                return k
        V.append([p[0], p[1]]); return len(V) - 1
    faces = []
    for c in cells:
        f = []
        for p in c:
            k = vid(p)
            if not f or f[-1] != k: f.append(k)
        if len(f) > 2 and f[0] == f[-1]: f.pop()
        if len(f) < 3: return None
        faces.append(f)
    # split T-junctions
    for _ in range(500):
        changed = False
        for f in faces:
            m = len(f)
            for i in range(m):
                p = V[f[i]]; q = V[f[(i + 1) % m]]
                ex, ey = q[0] - p[0], q[1] - p[1]
                L2 = ex * ex + ey * ey
                if L2 < 1e-18: continue
                for k in range(len(V)):
                    if k in f: continue
                    r = V[k]
                    t = ((r[0] - p[0]) * ex + (r[1] - p[1]) * ey) / L2
                    if not (1e-8 < t < 1 - 1e-8): continue
                    d = abs((r[0] - p[0]) * ey - (r[1] - p[1]) * ex) / math.sqrt(L2)
                    if d < 1e-7:
                        f.insert(i + 1, k); changed = True; break
                if changed: break
            if changed: break
        if not changed: break
    # areas must sum to the triangle's
    tot = 0.0
    for f in faces:
        s = 0.0
        for i in range(len(f)):
            x1, y1 = V[f[i]]; x2, y2 = V[f[(i + 1) % len(f)]]
            s += x1 * y2 - x2 * y1
        tot += abs(s) / 2
    if abs(tot - SQ3 / 4) > 1e-9:
        return None
    uv = [list(plane_to_uv(x, y)) for (x, y) in V]
    try:
        S = Struct(uv, faces)
    except Exception:
        return None
    # every face must be strictly convex to start
    c, _, _, _ = S.cvals(S.x)
    if c.min() <= 1e-12:
        return None
    return S


def lattice_sites(rng, n=15, jitter=0.02):
    cx, cy = 0.5, SQ3 / 6
    area = SQ3 / 4
    s = math.sqrt(2 * area / (SQ3 * n)) * rng.uniform(0.86, 1.14)
    th = rng.uniform(0, math.pi / 3)
    ox, oy = rng.uniform(-s / 2, s / 2), rng.uniform(-s / 2, s / 2)
    e1 = (s * math.cos(th), s * math.sin(th))
    e2 = (s * math.cos(th + math.pi / 3), s * math.sin(th + math.pi / 3))
    pts = []
    R = int(1 / s) + 3
    for i in range(-R, R + 1):
        for j in range(-R, R + 1):
            x = cx + ox + i * e1[0] + j * e2[0]
            y = cy + oy + i * e1[1] + j * e2[1]
            pts.append((x + rng.gauss(0, jitter * s), y + rng.gauss(0, jitter * s)))
    pts.sort(key=lambda q: (q[0] - cx) ** 2 + (q[1] - cy) ** 2)
    return pts[:n], [0.0] * n


def signature(S):
    """combinatorial fingerprint: sorted (face degree, #boundary vertices) multiset"""
    sig = []
    for f in S.faces:
        nb = sum(1 for k in f if S.cls[k] != 'F')
        sig.append((len(f), nb))
    return tuple(sorted(sig))


def main():
    seed0 = int(sys.argv[1]); ntry = int(sys.argv[2])
    out = sys.argv[3]
    rng = random.Random(seed0)
    best = 0.0; seen = {}
    for t in range(ntry):
        sites, w = lattice_sites(rng, 15, jitter=rng.choice([0.0, 0.01, 0.03, 0.07, 0.15]))
        w = [rng.gauss(0, 0.003) for _ in range(15)]
        S = build_struct(sites, w)
        if S is None: continue
        try:
            b = S.run(iters=300)
        except Exception:
            continue
        am = 1.0 / math.sqrt(b)
        sg = signature(S)
        if sg not in seen or am > seen[sg]:
            seen[sg] = am
        if am > best:
            best = am
            S.dump(out, {"seed": seed0, "try": t, "sig": str(sg)})
            print("seed %d try %4d  a_max %.9f  *  sig %s" % (seed0, t, am, sg), flush=True)
        elif t % 50 == 0:
            print("seed %d try %4d  a_max %.9f  (best %.9f)" % (seed0, t, am, best), flush=True)
    print("SEED %d BEST %.9f" % (seed0, best))
    json.dump({str(k): v for k, v in sorted(seen.items(), key=lambda kv: -kv[1])[:40]},
              open(out.replace(".json", "_sigs.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
