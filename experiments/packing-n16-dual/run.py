"""Driver: search for an m-piece convex partition of T_1 of least max diameter,
then freeze the best one as an EXACT rational certificate at a = a*.

  python3 run.py control        # m = 3 and m = 8, where the answer is known
  python3 run.py m15 [seconds]  # the real thing
"""
import sys, os, time, math, json, random, itertools
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dual import (d2, power_cells, assemble, classify, optimise, validate,
                  max_diam2, snap, certify, SQ3, to_xy)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


# ------------------------------------------------------------------ seeds
def rows_sites(rows, a=1.0, jitter=0.0, rnd=None):
    """rows[i] sites on the i-th horizontal band of T_a (v increasing)."""
    k = len(rows); out = []
    for i, ni in enumerate(rows):
        v = a * (i + 0.5) / k
        w = a - v
        for j in range(ni):
            u = w * (j + 0.5) / ni
            if jitter and rnd:
                u += jitter*a*(rnd.random()-0.5); v2 = v + jitter*a*(rnd.random()-0.5)
            else:
                v2 = v
            out.append((max(u, 1e-6), max(v2, 1e-6)))
    return out

def row_partitions(m, maxk=8):
    """non-increasing row profiles summing to m."""
    res = []
    def rec(rem, last, cur):
        if rem == 0:
            if len(cur) >= 2: res.append(tuple(cur)); return
        for x in range(min(rem, last), 0, -1):
            if len(cur) < maxk: rec(rem-x, x, cur+[x])
    rec(m, m, [])
    return res

def rand_sites(m, a=1.0, rnd=None):
    out = []
    while len(out) < m:
        u = rnd.random()*a; v = rnd.random()*a
        if u+v <= a: out.append((u, v))
    return out

def enemy_sites(drop):
    """the near-optimal 16-point configuration with one point deleted, rescaled
    to the unit triangle.  DESIGN HEURISTIC ONLY (KILL-CRITERION K5)."""
    src = os.path.join(ROOT, "experiments", "circle-packing-search", "out", "n16.json")
    d = json.load(open(src))
    pts = []
    for (x, y) in d["unit_triangle_points"]:
        u, v = x - y/SQ3, 2.0*y/SQ3
        pts.append((min(max(u, 1e-6), 1-1e-6), min(max(v, 1e-6), 1-1e-6)))
    return [p for i, p in enumerate(pts) if i != drop]


def try_sites(sites, m, seed, iters, a=1.0):
    cells = power_cells(a, sites)
    if any(len(c) < 3 for c in cells): return None
    r = assemble(cells, a)
    if r is None: return None
    V, faces = r
    if len(faces) != m: return None
    if validate(V, faces, a, tol=1e-7): return None
    cls = classify(V, a)
    val = optimise(V, faces, cls, a, iters=iters, seed=seed)
    if validate(V, faces, a, tol=1e-9): return None
    return (max_diam2(V, faces), V, faces, cls)


def search(m, seconds, target=None, seed=12345, iters=6000, verbose=True):
    rnd = random.Random(seed)
    t0 = time.time()
    best = None
    seeds = []
    for rows in row_partitions(m):
        seeds.append(("rows%s" % (rows,), rows_sites(rows)))
    if m == 15:
        for k in range(16):
            seeds.append(("enemy-drop%d" % k, enemy_sites(k)))
    if m == 16:
        seeds.append(("enemy-all", enemy_sites(-1)))
    tried = 0
    for name, S in seeds:
        if time.time()-t0 > seconds*0.5: break
        r = try_sites(S, m, rnd.randrange(1 << 30), iters)
        tried += 1
        if r and (best is None or r[0] < best[0]):
            best = r
            if verbose:
                print("   [%6.1fs] %-18s  delta=%.7f  a*=%.6f"
                      % (time.time()-t0, name, math.sqrt(r[0]), 1/math.sqrt(r[0])))
    # random restarts + perturbations of the incumbent
    while time.time()-t0 < seconds:
        tried += 1
        if best is not None and rnd.random() < 0.55:
            V0 = [row[:] for row in best[1]]
            amp = 0.02*rnd.random()
            for k, c in enumerate(V0):
                if best[3][k] != 4:
                    c[0] += amp*(rnd.random()-0.5); c[1] += amp*(rnd.random()-0.5)
            from dual import project
            project(V0, best[3], 1.0)
            faces = best[2]; cls = best[3]
            if validate(V0, faces, 1.0, tol=1e-9): continue
            optimise(V0, faces, cls, 1.0, iters=iters, seed=rnd.randrange(1 << 30))
            if validate(V0, faces, 1.0, tol=1e-9): continue
            r = (max_diam2(V0, faces), V0, faces, cls)
        else:
            base = rnd.choice(seeds)[1] if rnd.random() < 0.5 else rand_sites(m, 1.0, rnd)
            S = [(max(1e-6, u+0.10*(rnd.random()-0.5)), max(1e-6, v+0.10*(rnd.random()-0.5)))
                 for (u, v) in base]
            S = [(u, v) for (u, v) in S if u+v < 1-1e-6]
            if len(S) != m: continue
            r = try_sites(S, m, rnd.randrange(1 << 30), iters)
        if r and (best is None or r[0] < best[0]):
            best = r
            if verbose:
                print("   [%6.1fs] restart#%-5d      delta=%.7f  a*=%.6f"
                      % (time.time()-t0, tried, math.sqrt(r[0]), 1/math.sqrt(r[0])))
    if verbose:
        print("   tried %d topologies in %.1fs" % (tried, time.time()-t0))
    return best


# ------------------------------------------------------------------ freeze
def freeze(best, den=10**7, verbose=True):
    """snap to rationals at a=1, then scale to the largest nice a* with max d2 < 1."""
    val, V, faces, cls = best
    Vq = snap(V, cls, den)
    faces_q = [[Vq[i] for i in f] for f in faces]
    md = max(max((q_d2 := None) or 0 for _ in [0]) for _ in [0])  # placeholder
    from dual import q_d2 as QD2
    md = F(0)
    for f in faces_q:
        for p, q in itertools.combinations(f, 2):
            x = QD2(p, q)
            if x > md: md = x
    # largest a with a^2 * md < 1 : a < 1/sqrt(md).  Round DOWN to 6 decimals.
    lim = math.sqrt(1.0/float(md))
    for dec in (6, 5, 4):
        a_q = F(int(lim*10**dec) , 10**dec)
        if a_q*a_q*md < 1: break
    faces_a = [[(a_q*p[0], a_q*p[1]) for p in f] for f in faces_q]
    ok, md_a, _ = certify(faces_a, a_q, verbose=verbose)
    return ok, a_q, md_a, faces_a


def report(tag, best, known=None):
    d = math.sqrt(best[0]); astar = 1.0/d
    line = "%-10s m=%2d  float delta=%.8f  a*=%.7f" % (tag, len(best[2]), d, astar)
    if known: line += "   known a_{m+1}=%.7f   ratio=%.5f" % (known, astar/known)
    print(line)
    return astar


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "control"
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0
    if mode == "control":
        print("=== CONTROL m=3   (target a_4 = sqrt3 = %.7f) ===" % math.sqrt(3))
        b3 = search(3, secs, seed=1)
        report("control3", b3, math.sqrt(3))
        print("=== CONTROL m=8   (target a_9 = 3) ===")
        b8 = search(8, secs, seed=2)
        report("control8", b8, 3.0)
        json.dump({"m3": {"delta2": b3[0], "V": b3[1], "faces": b3[2], "cls": b3[3]},
                   "m8": {"delta2": b8[0], "V": b8[1], "faces": b8[2], "cls": b8[3]}},
                  open(os.path.join(HERE, "control.json"), "w"))
    else:
        m = int(mode[1:]) if mode[0] == "m" else 15
        print("=== m=%d  (ceiling a_16 = 4.6247636) ===" % m)
        b = search(m, secs, seed=7)
        report("m%d" % m, b, 4.6247636 if m == 15 else None)
        json.dump({"delta2": b[0], "V": b[1], "faces": b[2], "cls": b[3]},
                  open(os.path.join(HERE, "best_m%d.json" % m), "w"))
        print("--- exact certificate ---")
        ok, a_q, md, faces_a = freeze(b)
        print("certified: %s   a* = %s = %.7f" % (ok, a_q, float(a_q)))
        if ok:
            json.dump({"a": [a_q.numerator, a_q.denominator],
                       "faces": [[[str(p[0]), str(p[1])] for p in f] for f in faces_a]},
                      open(os.path.join(HERE, "cert_m%d.json" % m), "w"), indent=1)
