#!/usr/bin/env python3
"""Direction (A): can any 15-piece covering beat a = 1+2sqrt3?  Worker C5.

Float SEARCH ONLY -- decides nothing (problem RULES.md section 5).  Seeded.

Representation: the exact record subdivision of n16-covering-2 (15 convex
faces, 31 vertices, triangular (u,v) chart, side a0 = 1+2sqrt3), rescaled to a
test side a.  Vertices move; face combinatorics fixed; boundary vertices slide
along their side; corners pinned.  Objective: minimise the maximum squared
vertex-pair distance within any face (= max squared piece diameter, since a
convex polygon's diameter is attained at vertices).  If the minimum at side a
is < 1, a covering above the record exists (would then need exact freeze +
verification per KILL-CRITERION K6).

Asymmetric restarts: random jitter of every free coordinate before descent,
so nothing constrains the optimum to the record's 3-fold symmetry.

Control (K4): at a = 4.40 < 1+2sqrt3 the scaled record already has
max diam = a/a0 < 1; the optimiser must report <= that.
"""

import math
import random
import sys

R3 = math.sqrt(3.0)
A0 = 1.0 + 2.0 * R3

# record faces, (u,v) chart, coordinates p + q*sqrt3 as (p, q) pairs
r = R3
F_ = [
    [(0,0),(1,0),(r/3,r/3),(0,1)],
    [(r/3,1+r/3),(0,r),(0,1),(r/3,r/3),(1,1)],
    [(r/3,4*r/3),(0,1+r),(0,r),(r/3,1+r/3),(1,r)],
    [(r/3,1+4*r/3),(0,2*r),(0,1+r),(r/3,4*r/3),(1,2.5)],
    [(1,2*r),(0,1+2*r),(0,2*r),(r/3,1+4*r/3)],
    [(1,0),(r,0),(1+r/3,r/3),(1,1),(r/3,r/3)],
    [(1.5,1.5),(1,r),(r/3,1+r/3),(1,1),(1+r/3,r/3),(r,1)],
    [(1+r/3,4*r/3),(1,2.5),(r/3,4*r/3),(1,r),(1.5,1.5),(r,r)],
    [(r,1+r),(1,2*r),(r/3,1+4*r/3),(1,2.5),(1+r/3,4*r/3)],
    [(r,0),(1+r,0),(4*r/3,r/3),(r,1),(1+r/3,r/3)],
    [(4*r/3,1+r/3),(r,r),(1.5,1.5),(r,1),(4*r/3,r/3),(2.5,1)],
    [(1+r,r),(r,1+r),(1+r/3,4*r/3),(r,r),(4*r/3,1+r/3)],
    [(1+r,0),(2*r,0),(1+4*r/3,r/3),(2.5,1),(4*r/3,r/3)],
    [(2*r,1),(1+r,r),(4*r/3,1+r/3),(2.5,1),(1+4*r/3,r/3)],
    [(2*r,0),(1+2*r,0),(2*r,1),(1+4*r/3,r/3)],
]

EPS = 1e-9

def build():
    """Dedupe vertices; classify: 0=fixed corner, 1=side v=0, 2=side u=0,
    3=side u+v=a0, 4=free interior. Returns verts, classes, faces(indices)."""
    verts, faces = [], []
    for f in F_:
        idx = []
        for (u, v) in f:
            for i, (u2, v2) in enumerate(verts):
                if abs(u - u2) < 1e-7 and abs(v - v2) < 1e-7:
                    idx.append(i); break
            else:
                verts.append((u, v)); idx.append(len(verts) - 1)
        faces.append(idx)
    cls = []
    for (u, v) in verts:
        onv0 = abs(v) < EPS
        onu0 = abs(u) < EPS
        ond = abs(u + v - A0) < 1e-7
        n = onv0 + onu0 + ond
        cls.append(0 if n >= 2 else (1 if onv0 else 2 if onu0 else 3 if ond else 4))
    return verts, cls, faces


def sqd(p, q):
    du, dv = p[0] - q[0], p[1] - q[1]
    return du * du + du * dv + dv * dv     # |u e1 + v e2|^2 = u^2+uv+v^2


def maxdiam2(verts, faces):
    m, arg = -1.0, None
    for fi, f in enumerate(faces):
        for i in range(len(f)):
            for j in range(i + 1, len(f)):
                d = sqd(verts[f[i]], verts[f[j]])
                if d > m:
                    m, arg = d, (fi, f[i], f[j])
    return m, arg


def valid(verts, faces):
    """Faces stay convex ccw (subdivision integrity): cross products > -tol
    in the Euclidean image (shear-invariant sign)."""
    for f in faces:
        n = len(f)
        for k in range(n):
            a, b, c = verts[f[k]], verts[f[(k+1) % n]], verts[f[(k+2) % n]]
            # Euclidean cross of (b-a, c-b); chart shear preserves sign
            abu, abv = b[0]-a[0], b[1]-a[1]
            bcu, bcv = c[0]-b[0], c[1]-b[1]
            if abu * bcv - abv * bcu < -1e-8:
                return False
    return True


def project(verts, cls, scale):
    out = []
    for (u, v), c in zip(verts, cls):
        if c == 1: v = 0.0
        elif c == 2: u = 0.0
        elif c == 3:
            s = u + v - A0 * scale
            u -= s / 2; v -= s / 2
        out.append((u, v))
    return out


def descend(verts, cls, faces, scale, iters, rng, step0=0.02):
    """Soft-minimax subgradient descent on the max face diameter."""
    verts = project(verts, cls, scale)
    best = list(verts); bestval, _ = maxdiam2(best, faces)
    val = bestval
    for it in range(iters):
        step = step0 * (1.0 - 0.9 * it / iters)
        # softmax weights over top pairs
        m, _ = maxdiam2(verts, faces)
        grads = [[0.0, 0.0] for _ in verts]
        t = 250.0
        for f in faces:
            for i in range(len(f)):
                for j in range(i + 1, len(f)):
                    a, b = f[i], f[j]
                    d = sqd(verts[a], verts[b])
                    w = math.exp(t * (d - m))
                    if w < 1e-6: continue
                    du = verts[a][0] - verts[b][0]
                    dv = verts[a][1] - verts[b][1]
                    # grad of u^2+uv+v^2 wrt (du,dv): (2du+dv, du+2dv)
                    gu, gv = (2*du+dv) * w, (du+2*dv) * w
                    grads[a][0] += gu; grads[a][1] += gv
                    grads[b][0] -= gu; grads[b][1] -= gv
        gn = math.sqrt(sum(g[0]*g[0] + g[1]*g[1] for g in grads)) or 1.0
        cand = [(u - step * g[0] / gn, v - step * g[1] / gn)
                for (u, v), g in zip(verts, grads)]
        # pin corners back
        cand = [verts[i] if cls[i] == 0 else cand[i] for i in range(len(cand))]
        cand = project(cand, cls, scale)
        if valid(cand, faces):
            verts = cand
            val, _ = maxdiam2(verts, faces)
            if val < bestval:
                bestval, best = val, list(verts)
    return bestval, best


def run(a_test, restarts, iters, seed):
    rng = random.Random(seed)
    verts0, cls, faces = build()
    scale = a_test / A0
    base = [(u * scale, v * scale) for (u, v) in verts0]
    m0, _ = maxdiam2(base, faces)
    results = []
    v, _ = descend(base, cls, faces, scale, iters, rng)
    results.append(v)
    for k in range(restarts):
        jit = 0.02 + 0.10 * rng.random()
        cand = []
        for (u, vv), c in zip(base, cls):
            if c == 0:
                cand.append((u, vv)); continue
            cand.append((u + rng.uniform(-jit, jit), vv + rng.uniform(-jit, jit)))
        cand = project(cand, cls, scale)
        if not valid(cand, faces):
            continue
        v, _ = descend(cand, cls, faces, scale, iters, rng)
        results.append(v)
    return m0, min(results), len(results)


def main():
    seed = 20260822
    print(f"# seed={seed}; scaled-record baseline maxdiam = (a/a0)^2, a0=1+2sqrt3={A0:.9f}")
    for a_test, restarts, iters in [(4.40, 6, 300), (4.47, 20, 400), (4.50, 20, 400)]:
        m0, best, n = run(a_test, restarts, iters, seed)
        ratio = a_test / A0
        print(f"a={a_test}: baseline maxdiam^2={m0:.9f} (scaled record {(ratio*ratio):.9f}), "
              f"best after {n} descents: {best:.9f}  -> maxdiam={math.sqrt(best):.9f} "
              f"{'< 1  ***COVERING?***' if best < 1.0 else '>= 1'}")


if __name__ == "__main__":
    main()
