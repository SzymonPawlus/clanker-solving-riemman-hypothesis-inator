"""Perturbation-restart driver.  FLOATS ONLY; checkpoints the best config to JSON.

usage: drive.py <per_gap> <seed> <out.json> <seconds>
per_gap = 0 -> control (the record's convex partition, one group per face)
per_gap = k -> k extra arc vertices in every gap of every corner group
"""
import sys, os, math, json, time, random, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seed import load_record, build_from_faces
from refine import refine, triangulate
from tri_group import Cover

pg = int(sys.argv[1]); sd = int(sys.argv[2]); out = sys.argv[3]
budget = float(sys.argv[4]) if len(sys.argv) > 4 else 300.0
rng = random.Random(sd)

a, faces = load_record()
if pg == 0:
    V, tris, grp = build_from_faces(a, faces)
else:
    nf, bites = refine(a, faces, per_gap=pg)
    V, tris, grp = triangulate(a, nf, bites)

C = Cover(a, V, tris, grp)
assert C.all_ok()
SCHED = (4., 20., 120., 800., 5000., 30000.)
best = C.maxd(); bestV = [list(p) for p in C.V]      # the seed is already valid
v0 = C.descend(ps=SCHED, step0=0.02)
if v0 < best and C.all_ok():
    best = v0; bestV = [list(p) for p in C.V]
print("start  max^2 %.12f  a_max %.8f" % (best, a / math.sqrt(best)), flush=True)

def save():
    json.dump({"a": a, "per_gap": pg, "seed": sd, "V": bestV,
               "tris": [list(t) for t in C.tris], "grp": C.grp,
               "max_diam2": best, "a_max": a / math.sqrt(best)}, open(out, "w"))
save()

t0 = time.time(); r = 0
while time.time() - t0 < budget:
    r += 1
    sig0 = a * 0.02 * (0.15 + rng.random())
    C2 = None
    for att in range(8):                       # shrink until the perturbation is legal
        sig = sig0 / (2.0 ** att)
        T = Cover(a, [list(p) for p in bestV], C.tris, C.grp)
        for k in range(len(T.V)):
            c, si = T.cls[k]
            if c == "pin":
                continue
            if c == "free":
                T.V[k][0] += rng.gauss(0, sig); T.V[k][1] += rng.gauss(0, sig)
            else:
                t = rng.gauss(0, sig)
                if si == 0:   T.V[k][1] += t
                elif si == 1: T.V[k][0] += t
                else:         T.V[k][0] += t; T.V[k][1] -= t
        if T.all_ok():
            C2 = T
            break
    if C2 is None:
        continue
    C2.refresh()
    v = C2.descend(ps=SCHED, step0=0.02)
    if v < best - 1e-14 and C2.all_ok():
        best = v; bestV = [list(p) for p in C2.V]; save()
        print("round %4d  max^2 %.12f  a_max %.8f  *" % (r, v, a / math.sqrt(v)), flush=True)
    elif r % 25 == 0:
        print("round %4d  (best a_max %.8f)  %.0fs" % (r, a / math.sqrt(best), time.time()-t0), flush=True)
print("FINAL per_gap=%d seed=%d  a_max %.8f  rounds %d" % (pg, sd, a / math.sqrt(best), r))
