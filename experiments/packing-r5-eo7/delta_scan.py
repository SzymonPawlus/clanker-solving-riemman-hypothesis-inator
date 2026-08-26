"""How much thickening delta can the line bound absorb before it exceeds the EO(k) target?

If a configuration is only within delta of a line family (rather than exactly on it), the
per-strip count bound becomes ceil( ell^delta_j / sqrt(1 - 4 delta^2) ), where
ell^delta_j = sup_{|t - s_j| <= delta} ell(t) is the u-extent of the slab.  This is the
robustness the conditional theorem of the write-up needs, and it is measured -- not
certified -- here.  STATUS: numerical (float scan, evidence only).
"""
import math, sys, json
from geometry import tent, chord, SQRT3


def bound_delta(phi, h, theta, a, delta, tol=1e-12):
    d1, w, Lstar = tent(phi, a)
    r = math.sqrt(max(1e-12, 1.0 - 4.0 * delta * delta))
    total, j = 0, 0
    while True:
        s = (theta + j) * h
        if s - delta > w + tol:
            break
        lo, hi = max(0.0, s - delta), min(w, s + delta)
        if hi < lo:
            j += 1
            continue
        L = max(chord(phi, lo, a), chord(phi, hi, a),
                Lstar if lo <= d1 <= hi else 0.0)
        total += max(1, math.ceil(L / r - tol))
        j += 1
    return total


def scan(a, delta, nphi=181, nh=121, nth=181, hmax=None):
    hmax = hmax or a + 0.6
    best = 0
    for i in range(nphi):
        phi = (math.pi / 3.0) * i / (nphi - 1)
        for jh in range(nh):
            h = SQRT3 / 2 + (hmax - SQRT3 / 2) * jh / (nh - 1)
            for kt in range(nth):
                v = bound_delta(phi, h, kt / nth, a, delta)
                if v > best:
                    best = v
    return best


if __name__ == "__main__":
    a = float(sys.argv[1]) if len(sys.argv) > 1 else 6.0
    tgt = int(sys.argv[2]) if len(sys.argv) > 2 else 26
    rows = []
    for delta in (0.0, 0.001, 0.003, 0.01, 0.02, 0.03, 0.05):
        v = scan(a, delta)
        rows.append({"delta": delta, "max_bound": v, "ok": v <= tgt})
        print(json.dumps(rows[-1]), flush=True)
        if v > tgt:
            break
    json.dump({"a": a, "target": tgt, "rows": rows}, open("out/delta_scan.json", "w"), indent=1)
