"""Float search driver for N=15 pieces in T_a.  FLOATS ONLY -- decides nothing.
Checkpoints the best configuration found to disk after every basin."""
import sys, json, math, os
import fopt

a0 = 4.5
n = 15
seed = int(sys.argv[1]); tries = int(sys.argv[2])
out = "opt_n15_seed%d.json" % seed
best = 1e18; bestcfg = None
import random
rng = random.Random(seed)
for t in range(tries):
    b, cfg = fopt.basin(a0, n, seed*1000 + t, tries=3, verbose=False)
    if b < best:
        best, bestcfg = b, cfg
        json.dump({"a": a0, "n": n, "max_diam": best, "a_max": a0/best,
                   "sites": bestcfg[0], "weights": bestcfg[1]}, open(out, "w"))
    print("seed %d basin %d: %.9f  best %.9f  a_max %.6f" % (seed, t, b, best, a0/best), flush=True)
print("SEED %d FINAL %.9f a_max %.6f" % (seed, best, a0/best))
