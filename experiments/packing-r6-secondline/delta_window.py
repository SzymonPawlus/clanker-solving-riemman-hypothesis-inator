"""The delta-window of the ONE-family count, measured honestly at side a < 6.

r5-eo7 §7 runs its delta scan at a = 6 with the cap ceil(ell^delta / sqrt(1 - 4 delta^2)).
The 1 under the square root is the separation, i.e. it sets sep = 1.  But ceil(.) is only a
valid cap when the separation is STRICTLY > 1, which is what a' < 6 buys after rescaling by
6/a'.  So the delta = 0 row and the delta > 0 rows use different separations, and the jump
between them is that inconsistency, not a property of the counting step.

Here delta is measured against the one parameter it must be compared with: eta = 6 - a.
Cap: floor(ell^delta / sqrt(1 - 4 delta^2)) + 1, separation >= 1, at side a = 6 - eta.  This
is valid for every eta >= 0 and is what a 1-separated set in T(6-eta) actually obeys.

STATUS: numerical (float scan; evidence only).  Nothing here is assumable.
"""
import json, math
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _deps

_deps.require('delta_window.py')   # fail fast, before the numpy import below

import numpy as np
import one_family as OF

TGT = 26
ETAS = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4]

COARSE = dict(nphi=91, nh=61, nth=91)
FINE = dict(nphi=181, nh=121, nth=181)

if __name__ == "__main__":
    rows = []
    for eta in ETAS:
        a = 6.0 - eta
        b0, arg = OF.scan(a, 0.0, cap="floor", hmax=a + 0.6, **FINE)
        d0, _ = OF.window(a, cap="floor", tgt=TGT, hi=0.4, iters=14, hmax=a + 0.6, **COARSE)
        # confirm the window endpoint on the fine grid
        bin_, _ = OF.scan(a, d0, cap="floor", hmax=a + 0.6, **FINE)
        bout, _ = OF.scan(a, min(0.4, d0 * 1.25 + 1e-9), cap="floor", hmax=a + 0.6, **FINE)
        rows.append({"eta": eta, "a": a, "bound_delta0": b0, "loss_at_delta0": max(0, b0 - TGT),
                     "delta_window": d0, "delta_window_over_eta": d0 / eta,
                     "fine_bound_at_window": bin_, "fine_bound_at_1.25x_window": bout})
        print(json.dumps(rows[-1]), flush=True)
        json.dump({"target": TGT, "cap": "floor(L/sqrt(1-4d^2))+1", "grid_coarse": COARSE,
                   "grid_fine": FINE, "rows": rows},
                  open("out/delta_window_one_family.json", "w"), indent=1)
