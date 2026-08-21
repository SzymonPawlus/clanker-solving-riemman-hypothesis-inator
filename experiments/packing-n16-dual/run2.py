"""Production driver.

  python3 run2.py <m> <seconds> [seed]

Pipeline per start:
  random / structured sites  ->  p-centre (pcenter.py)  ->  Voronoi  ->
  target-shrinking minimax refinement (dual.refine)  ->  keep the best.
Then basin hopping: perturb the incumbent's vertices and re-refine.
Finally freeze the incumbent as an EXACT rational certificate and report
    a* = a / diam_max  (dilation is free bound: see manager note, 2026-08-22).
"""
import sys, os, math, json, random, time, itertools
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dual import (power_cells, assemble, classify, validate, max_diam2, refine,
                  project, snap, certify, q_d2, SQ3)
import pcenter as PC
from run import rows_sites, row_partitions, enemy_sites, rand_sites

HERE = os.path.dirname(os.path.abspath(__file__))


def build(sites, m):
    cells = power_cells(1.0, sites)
    if any(len(c) < 3 for c in cells): return None
    R = assemble(cells, 1.0)
    if R is None: return None
    V, faces = R
    if len(faces) != m: return None
    if validate(V, faces, 1.0, tol=1e-7): return None
    return V, faces, classify(V, 1.0)


def lattice_sites(m, rnd, tries=400):
    """exactly m points of a triangular lattice (spacing h, offset o) inside T_1.
    In the triangular basis the lattice is simply {(i*h+ou, j*h+ov)}, so nearest
    neighbours are at distance h and the Voronoi cells are regular hexagons of
    diameter 2h/sqrt3 -- the shape the bulk of an optimal covering wants."""
    for _ in range(tries):
        h = 0.16 + 0.16*rnd.random()
        ou = h*rnd.random(); ov = h*rnd.random()
        P = []
        for i in range(-2, 12):
            for j in range(-2, 12):
                u = i*h + ou; v = j*h + ov
                if u > 1e-4 and v > 1e-4 and u+v < 1-1e-4: P.append((u, v))
        if len(P) == m:
            return [PC.clampT(1.0, (u+0.5*v, v*SQ3/2)) for (u, v) in P]
        if m < len(P) <= m+3:
            rnd.shuffle(P); P = P[:m]
            return [PC.clampT(1.0, (u+0.5*v, v*SQ3/2)) for (u, v) in P]
    return None


def seed_sites(m, rnd, kind):
    if kind == "lattice":
        return lattice_sites(m, rnd)
    if kind == "rand":
        C = []
        while len(C) < m:
            x = rnd.random(); y = rnd.random()*SQ3/2
            if PC.inside(1.0, (x, y)): C.append((x, y))
        return C
    if kind == "rows":
        rows = rnd.choice(row_partitions(m))
        S = rows_sites(rows)
        return [PC.clampT(1.0, (u+0.5*v, v*SQ3/2)) for (u, v) in S]
    if kind == "enemy" and m in (15, 16):
        S = enemy_sites(rnd.randrange(16) if m == 15 else -1)
        return [PC.clampT(1.0, (u+0.5*v, v*SQ3/2)) for (u, v) in S]
    return None


def main():
    m = int(sys.argv[1]); secs = float(sys.argv[2])
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20260822
    rnd = random.Random(seed)
    out = os.path.join(HERE, "best_m%d.json" % m)
    best = None
    if os.path.exists(out):
        d = json.load(open(out))
        best = (d["delta2"], [list(p) for p in d["V"]], d["faces"], d["cls"])
        print("resume: delta=%.8f a*=%.7f" % (math.sqrt(best[0]), 1/math.sqrt(best[0])))
    t0 = time.time(); n = 0
    kinds = ["rand", "rows", "lattice", "lattice", "lattice"] + (["enemy"] if m in (15, 16) else [])
    while time.time() - t0 < secs:
        n += 1
        if best is not None and rnd.random() < 0.6:
            V = [row[:] for row in best[1]]; faces = best[2]; cls = best[3]
            amp = 0.10 * rnd.random()**2
            for k in range(len(V)):
                if cls[k] != 4:
                    V[k][0] += amp*(rnd.random()-0.5); V[k][1] += amp*(rnd.random()-0.5)
            project(V, cls, 1.0)
            if validate(V, faces, 1.0, tol=1e-9): continue
        else:
            S = seed_sites(m, rnd, rnd.choice(kinds))
            if S is None: continue
            S = [PC.clampT(1.0, (x+0.06*(rnd.random()-0.5), y+0.06*(rnd.random()-0.5)))
                 for (x, y) in S]
            r, Cb = PC.pcenter(1.0, S, iters=rnd.choice([5, 20, 60, 150]))
            B = build([PC.to_uv(*p) for p in Cb], m)
            if B is None: continue
            V, faces, cls = B
        val = refine(V, faces, cls, 1.0, rounds=rnd.choice([200, 400]))
        if validate(V, faces, 1.0, tol=1e-9): continue
        if best is None or val < best[0] - 1e-15:
            best = (val, [row[:] for row in V], faces, cls)
            print("  [%6.1fs #%d] delta=%.9f  a*=%.8f" %
                  (time.time()-t0, n, math.sqrt(val), 1/math.sqrt(val)), flush=True)
            json.dump({"delta2": best[0], "V": best[1], "faces": best[2],
                       "cls": best[3], "seed": seed}, open(out, "w"))
    print("starts: %d in %.0fs" % (n, time.time()-t0))
    print("FLOAT  m=%d  delta=%.9f  a*=%.8f" % (m, math.sqrt(best[0]), 1/math.sqrt(best[0])))
    freeze(m, best)


def freeze(m, best, dens=(10**6, 10**7, 10**8)):
    val, V, faces, cls = best
    bestcert = None
    for den in dens:
        Vq = snap(V, cls, den)
        fq = [[Vq[i] for i in f] for f in faces]
        md = F(0)
        for f in fq:
            for p, q in itertools.combinations(f, 2):
                x = q_d2(p, q)
                if x > md: md = x
        if md == 0: continue
        lim = math.sqrt(1.0/float(md))
        a_q = None
        for dec in (9, 8, 7, 6, 5):
            c = F(int(lim*10**dec), 10**dec)
            if c*c*md < 1: a_q = c; break
        if a_q is None: continue
        fa = [[(a_q*p[0], a_q*p[1]) for p in f] for f in fq]
        ok, md_a, rep = certify(fa, a_q, verbose=False)
        if ok and (bestcert is None or a_q > bestcert[1]):
            bestcert = (ok, a_q, md_a, fa, den, rep)
    print("--- exact certificate ---")
    if bestcert is None:
        print("  no snapping denominator produced a valid exact certificate"); return
    ok, a_q, md_a, fa, den, rep = bestcert
    for line in rep: print("   " + line)
    print("  denominator 10^%d" % round(math.log10(den)))
    print("  CERTIFIED a* = %s = %.10f    (a = a_snap / diam_max, dilation applied)"
          % (a_q, float(a_q)))
    json.dump({"m": m, "a_numer": a_q.numerator, "a_denom": a_q.denominator,
               "a_float": float(a_q),
               "max_sq_diameter": [md_a.numerator, md_a.denominator],
               "basis": "e1=(1,0), e2=(1/2,sqrt3/2); |u e1+v e2|^2 = u^2+uv+v^2",
               "triangle": "T_a = {u>=0, v>=0, u+v<=a}",
               "faces_uv": [[[str(p[0]), str(p[1])] for p in f] for f in fa]},
              open(os.path.join(HERE, "cert_m%d.json" % m), "w"), indent=1)
    print("  wrote cert_m%d.json" % m)


if __name__ == "__main__":
    main()
