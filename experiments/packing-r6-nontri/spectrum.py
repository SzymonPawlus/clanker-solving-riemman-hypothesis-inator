"""Capacity spectra: numerical a_S(m) = 1/delta_S(m) for every shape family.

Capacity m is SKIPPED by the scaled family {lambda*S} iff a_S(m) == a_S(m+1).
Everything here is `numerical` (search only); the exact statements are in the write-up.
"""
import _deps; _deps.require()   # numpy/scipy are REAL deps here (see pyproject.toml)
import json, sys, time, numpy as np, shapes

MS = list(range(2, 11))

if __name__ == '__main__':
    S = shapes.make_shapes()
    keys = sys.argv[1:] or list(S)
    out = {}
    for k in keys:
        row = {}
        t0 = time.time()
        for m in MS:
            best = -1
            for seed in (11, 202, 3003):
                v, P = shapes.maximin(S[k], m, restarts=25, seed=seed + m)
                if v > best:
                    best, bestP = v, P
            row[m] = dict(delta=best, a=1.0 / best if best > 0 else None,
                          pts=[list(map(float, p)) for p in bestP])
            print(f"{k:10s} m={m:2d} delta={best:.8f} a={1/best:.8f}", flush=True)
        out[k] = row
        print(f"# {k} done in {time.time()-t0:.0f}s", flush=True)
        json.dump(out, open(f'out/spectrum_{"_".join(keys)}.json', 'w'), indent=1)
