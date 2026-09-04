"""One search worker: repeated descents from mixed starts, checkpointing the best.
usage: worker.py a n seed seconds tag
FLOATS ONLY (search stage)."""
import math, json, random, sys, time, os
from opt import Diagram, descend, lattice_init
from honeycomb import area

HERE = os.path.dirname(os.path.abspath(__file__))

def hexstart(a, n, rng):
    d = json.load(open(os.path.join(HERE, "hex_a%g.json" % a)))
    cs = d["centres"]; ar = d["clipped_area"]
    order = sorted(range(len(cs)), key=lambda i: ar[i])
    k = len(cs) - n
    if k <= 0:
        return [list(c) for c in cs] + [[rng.uniform(0, a), rng.uniform(0, a*0.5)] for _ in range(-k)], [0.0]*n
    pool = order[:min(len(cs), k + 8)]
    drop = set(rng.sample(pool, k))
    return [list(c) for i, c in enumerate(cs) if i not in drop], [0.0]*n

def main():
    a = float(sys.argv[1]); n = int(sys.argv[2]); seed = int(sys.argv[3])
    secs = float(sys.argv[4]); tag = sys.argv[5]
    rng = random.Random(seed)
    t0 = time.time()
    best = 1e18; bestcfg = None
    log = open(os.path.join(HERE, "log_%s.txt" % tag), "w")
    it = 0
    while time.time() - t0 < secs:
        it += 1
        r = rng.random()
        if bestcfg is not None and r < 0.55:
            sc = 0.12 * a / math.sqrt(n) * rng.choice([0.3, 1.0, 2.0])
            s0 = [[x + rng.gauss(0, sc), y + rng.gauss(0, sc)] for x, y in bestcfg[0]]
            w0 = [w + rng.gauss(0, sc * a / math.sqrt(n)) for w in bestcfg[1]]
        elif r < 0.8:
            s0, w0 = hexstart(a, n, rng)
            s0 = [[x + rng.gauss(0, 0.05), y + rng.gauss(0, 0.05)] for x, y in s0]
        else:
            s0, w0 = lattice_init(a, n, rng, jitter=0.05)
        try:
            dg = Diagram(a, s0, w0)
            v = descend(dg)
        except Exception as e:
            log.write("err %s\n" % e); log.flush(); continue
        if v < best:
            best = v; bestcfg = ([list(p) for p in dg.s], list(dg.w))
            json.dump({"a": a, "n": n, "max_diam": v, "sites": bestcfg[0], "weights": bestcfg[1]},
                      open(os.path.join(HERE, "best_%s.json" % tag), "w"))
        log.write("it %d  %.9f  best %.9f  t=%.0f\n" % (it, v, best, time.time()-t0)); log.flush()
    log.write("DONE best %.12f\n" % best); log.close()
    print("tag=%s a=%g n=%d BEST %.12f" % (tag, a, n, best))

main()
