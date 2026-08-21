"""Structure-space search: mutate the combinatorial subdivision, repair, SLP, keep gains.
FLOATS ONLY -- search stage; every hit is frozen as an exact rational certificate."""
import json, math, random, sys, time
import slp, moves
from slp import Struct

src = sys.argv[1]; out = sys.argv[2]
seed = int(sys.argv[3]); budget = float(sys.argv[4])       # seconds
rng = random.Random(seed)

S = slp.from_struct_json(src) if src.endswith(".json") and "st_" in src else slp.from_plane_json(src)
best = S.run(iters=400)
bestS = S
bam = 1.0 / math.sqrt(best)
print("start a_max %.9f  (%d faces, %d verts)" % (bam, len(S.faces), len(S.uv)), flush=True)
S.dump(out, {"seed": seed})

t0 = time.time(); n = 0; nok = 0
cur = bestS; curv = best
while time.time() - t0 < budget:
    n += 1
    T = moves.mutate(cur, rng)
    if T is None: continue
    if len(T.faces) != 15: continue
    if not moves.repair(T): continue
    try:
        v = T.run(iters=300)
    except Exception:
        continue
    nok += 1
    am = 1.0 / math.sqrt(v)
    if v < best - 1e-13:
        best = v; bam = am; bestS = T
        T.dump(out, {"seed": seed, "iter": n})
        print("[%6.0fs] n=%d  a_max %.9f  *  degs %s" %
              (time.time() - t0, n, am, sorted(len(f) for f in T.faces)), flush=True)
    # simulated-annealing style acceptance on the current point
    if v < curv + 2e-4 * rng.random():
        cur, curv = T, v
    if n % 200 == 0:
        print("[%6.0fs] n=%d ok=%d  best %.9f  cur %.9f" %
              (time.time() - t0, n, nok, bam, 1.0 / math.sqrt(curv)), flush=True)
print("FINAL best a_max %.9f   (%d mutations, %d evaluated)" % (bam, n, nok))
