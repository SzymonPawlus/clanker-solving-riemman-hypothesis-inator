"""Beam search over the COMBINATORIAL structure of the subdivision.

For each candidate structure the geometry is regenerated from scratch by a Tutte
embedding and then driven to ITS optimum by the SLP (which is a convex program once
the structure is fixed).  So each structure is scored by its true optimal max-diameter,
and the search is a clean discrete search rather than a coupled geometry/topology one.

FLOATS ONLY -- search stage.
"""
import json, math, os, sys, time
from multiprocessing import Pool
import comb, slp


def score(faces):
    S = comb.embed(faces)
    if S is None:
        return None
    try:
        v = S.run(iters=300, abort_below=1.0 / 4.42 ** 2, abort_at=70)
    except Exception:
        return None
    return (v, [list(f) for f in S.faces], [list(p) for p in S.uv], list(S.cls))


def score_safe(faces):
    try:
        return score(faces)
    except Exception:
        return None


def main():
    src, out, depth, width = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    nproc = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    S0 = slp.from_struct_json(src)
    base = [list(f) for f in S0.faces]
    r = score_safe(base)
    beam = [(r[0], base)]
    best = (r[0], base, r[2], r[3])
    seen = {comb.key(base)}
    print("start a_max %.9f" % (1 / math.sqrt(r[0])), flush=True)
    pool = Pool(nproc)
    for d in range(depth):
        cands = []
        for _, fs in beam:
            for nf in comb.all_flips(fs):
                k = comb.key(nf)
                if k in seen:
                    continue
                seen.add(k)
                cands.append(nf)
        if not cands:
            break
        t0 = time.time()
        res = pool.map(score_safe, cands, chunksize=4)
        scored = [(r2[0], cands[i], r2[2], r2[3]) for i, r2 in enumerate(res) if r2]
        scored.sort(key=lambda z: z[0])
        print("depth %d: %d candidates, %d embeddable, %.0fs; best a_max %.9f"
              % (d, len(cands), len(scored), time.time() - t0,
                 1 / math.sqrt(scored[0][0]) if scored else 0), flush=True)
        if scored and scored[0][0] < best[0]:
            best = scored[0]
            json.dump({"a": 1.0, "uv": best[2], "faces": best[1], "cls": best[3],
                       "max_diam": math.sqrt(best[0]), "a_max": 1 / math.sqrt(best[0]),
                       "depth": d},
                      open(out, "w"))
            print("   *** new best a_max %.9f  degs %s"
                  % (1 / math.sqrt(best[0]), sorted(len(f) for f in best[1])), flush=True)
        beam = [(z[0], z[1]) for z in scored[:width]]
    pool.close()
    print("FINAL a_max %.9f" % (1 / math.sqrt(best[0])))


if __name__ == "__main__":
    main()
