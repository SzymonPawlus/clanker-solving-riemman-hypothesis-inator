"""Sub-integer corner-coordinate relaxation for Erdos-Oler.   `numerical`/`sketch`.

Usage:  python3 run.py [k ...]

NORMALISATION: separation 1, triangle side a  (Oler).  Repo certificates use
separation 2 and side 2a and are halved on load.  Erdos-Oler at level k:
n = T(k)-1 points at separation >= 1 force a >= k-1.

The relaxation.  Fix a rational a < k-1 and a threshold set Theta.  Cells are the
corner-coordinate boxes cut out by consecutive thresholds; every box R with
endpoints in Theta carries the constraint  sum_{c subset R} z_c <= cap(R), with
cap computed from geometry alone (geom.capacity; kill-criterion K2).  The LP
optimum is the best point-count upper bound this family can give; Erdos-Oler at
level k is decided iff it is <= T(k)-2, against floor(Oler(a)) = T(k)-1.
"""

import sys, time, json
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import geom, lp

T = lambda m: m * (m + 1) // 2


def thresholds(a, kind, k):
    """Threshold sets.  'int' reproduces the predecessor's integer thresholds;
    'sub<M>' is the sub-integer refinement at multiples of a/M."""
    if kind == "int":
        th = [F(0)] + [F(j) for j in range(1, k - 1)] + [a]
        return sorted(set(t for t in th if 0 <= t <= a))
    M = int(kind[3:])
    return [a * F(i, M) for i in range(M + 1)]


def build(a, Theta, mu=F(1), verbose=True):
    """Cells = boxes cut by consecutive thresholds; constraints = every corner box
    with endpoints in Theta whose capacity is below the summed capacity of the
    cells it contains.  Capacities are cached by congruence class: the box
    {lo <= u <= hi} is congruent to {v >= 0, sum v = S, v_V <= g_V} with
    S = 2a - sum(lo) and g_V = min(hi_V - lo_V, S), up to the 6 symmetries of T."""
    L = len(Theta) - 1
    tot = 2 * a
    cells = []
    for iA in range(L):
        for iB in range(L):
            for iC in range(L):
                lo = (Theta[iA], Theta[iB], Theta[iC])
                hi = (Theta[iA + 1], Theta[iB + 1], Theta[iC + 1])
                if sum(lo) < tot < sum(hi):
                    cells.append((iA, iB, iC))
    NC = len(cells)
    cache = {}

    def cap_of(lo, hi):
        S = tot - sum(lo)
        if S < 0:
            return 0, "empty"
        g = tuple(sorted(min(hi[V] - lo[V], S) for V in range(3)))
        key = (S, g)
        if key not in cache:
            cache[key] = geom.capacity(S, [F(0)] * 3, list(g), mu)
        return cache[key]

    cellcap = []
    for c in cells:
        lo = (Theta[c[0]], Theta[c[1]], Theta[c[2]])
        hi = (Theta[c[0] + 1], Theta[c[1] + 1], Theta[c[2] + 1])
        cellcap.append(cap_of(lo, hi)[0])

    # bitmask of cells with p <= i_V <= q, per coordinate
    masks = [[[0] * L for _ in range(L)] for _ in range(3)]
    for V in range(3):
        for p in range(L):
            for q in range(p, L):
                m = 0
                for idx, c in enumerate(cells):
                    if p <= c[V] <= q:
                        m |= 1 << idx
                masks[V][p][q] = m

    cols, caps, meta = [], [], []
    seen = {}
    for pA in range(L):
        for qA in range(pA, L):
            mA = masks[0][pA][qA]
            if mA == 0:
                continue
            for pB in range(L):
                for qB in range(pB, L):
                    mAB = mA & masks[1][pB][qB]
                    if mAB == 0:
                        continue
                    for pC in range(L):
                        for qC in range(pC, L):
                            mm = mAB & masks[2][pC][qC]
                            if mm == 0:
                                continue
                            lo = (Theta[pA], Theta[pB], Theta[pC])
                            hi = (Theta[qA + 1], Theta[qB + 1], Theta[qC + 1])
                            cp, why = cap_of(lo, hi)
                            inside = []
                            t = mm
                            tot_cc = 0
                            while t:
                                b = (t & -t).bit_length() - 1
                                inside.append(b)
                                tot_cc += cellcap[b]
                                t &= t - 1
                            if len(inside) > 1 and cp >= tot_cc:
                                continue
                            if mm in seen:
                                j = seen[mm]
                                if cp < caps[j]:
                                    caps[j] = cp
                                    meta[j] = (lo, hi, why)
                                continue
                            seen[mm] = len(cols)
                            cols.append(inside)
                            caps.append(cp)
                            meta.append((lo, hi, why))
    return cells, cols, caps, meta, cache


def prune(cols, caps, meta, ncells):
    """Drop constraints implied by another: (P,c) is implied by (P',c') whenever
    P subset P' and c' <= c."""
    masks = []
    for cl in cols:
        m = 0
        for i in cl:
            m |= 1 << i
        masks.append(m)
    order = sorted(range(len(cols)), key=lambda j: (-len(cols[j]), caps[j]))
    keep = []
    for j in order:
        dominated = False
        for i in keep:
            if caps[i] <= caps[j] and (masks[j] & ~masks[i]) == 0:
                dominated = True
                break
        if not dominated:
            keep.append(j)
    return [cols[j] for j in keep], [caps[j] for j in keep], [meta[j] for j in keep]


def run_level(k, kind, delta, report):
    a = F(k - 1) - delta
    n = T(k) - 1
    oler = a * a / 2 + 3 * a / 2 + 1
    Theta = thresholds(a, kind, k)
    t0 = time.time()
    cells, cols, caps, meta, cache = build(a, Theta)
    cols, caps, meta = prune(cols, caps, meta, len(cells))
    tb = time.time() - t0
    report(f"k={k}  n={n}  a={a} ({float(a):.6f})  thresholds={kind} ({len(Theta)} values)")
    report(f"  floor(Oler(a)) = {int(oler)}   [target: LP <= {n-1} decides Erdos-Oler at k={k}]")
    report(f"  cells={len(cells)}  binding boxes={len(cols)}  distinct shapes={len(cache)}  build {tb:.1f}s")
    t0 = time.time()
    val, y = lp.solve_cover(cols, caps, len(cells))
    report(f"  LP fractional-cover optimum = {val:.6f}   ({time.time()-t0:.1f}s)")
    verdict = None
    if val is not None and val < n - 1e-6:
        # exact certification: round every weight UP to a rational
        ysupp = {}
        for j, v in enumerate(y):
            if v > 1e-9:
                ysupp[j] = F(v).limit_denominator(10000)
                if ysupp[j] < F(v):
                    ysupp[j] = F(v).limit_denominator(10000) + F(1, 10000)
        ok, bad, cost = lp.verify_cover_exact(ysupp, cols, caps, len(cells))
        report(f"  EXACT certificate: covering={ok}, uncovered cells={len(bad)}, exact cost={cost} = {float(cost):.6f}")
        if ok and cost < n:
            verdict = "INFEASIBLE (counting proof)"
            report(f"  ==> at most {float(cost):.6f} < {n} points fit: Erdos-Oler at k={k} DECIDED by this family")
            report("  binding boxes in the certificate (lo | hi | cap | weight | source of cap):")
            for j, w in sorted(ysupp.items(), key=lambda kv: -float(kv[1])):
                lo, hi, why = meta[j]
                report(f"    lo={[str(x) for x in lo]} hi={[str(x) for x in hi]} cap={caps[j]} w={w} via {why}")
        else:
            verdict = "float LP said < n but exact certificate failed"
            report("  " + verdict)
    else:
        verdict = "FEASIBLE (no counting proof from this family)"
        report(f"  ==> LP optimum {val:.4f} >= {n}: this family does NOT decide Erdos-Oler at k={k}")
    return verdict, val


def main():
    ks = [int(x) for x in sys.argv[1:]] or [3, 4]
    out = open(__file__.rsplit('/', 1)[0] + "/out/report.txt", "a")

    def report(s):
        print(s)
        out.write(s + "\n")
        out.flush()

    report("=" * 78)
    report("sub-integer corner-coordinate relaxation, run at " + time.strftime("%Y-%m-%d %H:%M:%S"))
    for k in ks:
        for kind in ["int", "sub%d" % (3 * (k - 1) if k <= 5 else 3 * (k - 1))]:
            for delta in [F(1, 100), F(1, 1000)]:
                try:
                    run_level(k, kind, delta, report)
                except Exception as e:
                    report(f"  k={k} {kind} delta={delta}: FAILED {type(e).__name__}: {e}")
                report("")
    out.close()


if __name__ == "__main__":
    main()
