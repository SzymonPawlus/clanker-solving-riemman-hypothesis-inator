import json, numpy as np, mobility
res = {}
for sep, tag in ((1.0 + 1e-6, 'eps1e-6'), (1.01, 'eps1e-2')):
    for seed in (1, 2, 3):
        r = mobility.run(sep=sep, seed=seed, steps=3_000_000, step=0.04)
        r.pop('trail')
        k = f"{tag}_s{seed}"
        res[k] = r
        print(k, 'acc=%.3f' % r['acc_rate'], 'wander=', ['%.3f' % v for v in r['bbox_diag']], flush=True)
        json.dump(res, open('out/mobility_long.json', 'w'), indent=1)
