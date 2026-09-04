"""How much of the missing point does the refinement close, on the a-scale?

Oler alone forces a >= a0(k) = (-3 + sqrt(8T(k)-7))/2 for n = T(k)-1 points;
the truth is a >= k-1.  This script finds a*(k, M) = the largest a at which the
sub-integer relaxation on the a/M grid still certifies "fewer than n points fit",
by bisection, and reports the fraction of the [a0, k-1] gap that closes."""
import sys, time
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/',1)[0])
import run as R, lp
T = lambda m: m*(m+1)//2

def lpval(k, M, a):
    Th = [a*F(i,M) for i in range(M+1)]
    cells, cols, caps, meta, cache = R.build(a, Th)
    cols, caps, meta = R.prune(cols, caps, meta, len(cells))
    val, y = lp.solve_cover(cols, caps, len(cells))
    return val

if __name__ == "__main__":
    k = int(sys.argv[1]); M = int(sys.argv[2])
    n = T(k)-1
    import math
    a0 = (-3 + math.sqrt(8*T(k)-7))/2
    lo, hi = F(0), F(k-1)          # LP < n at lo, LP >= n at hi (to be established)
    v = lpval(k, M, hi - F(1,1000))
    print(f"k={k} n={n} M={M} a0(Oler)={a0:.5f} truth={k-1}   LP at a=(k-1)-1e-3: {v}", flush=True)
    if v is not None and v < n - 1e-6:
        print("  closes the whole gap at this M", flush=True)
        sys.exit()
    for it in range(9):
        mid = (lo+hi)/2
        v = lpval(k, M, mid)
        ok = (v is not None and v < n - 1e-6)
        print(f"  a={float(mid):.5f} LP={v} -> {'certifies' if ok else 'does not'}", flush=True)
        if ok: lo = mid
        else: hi = mid
    frac = (float(lo)-a0)/((k-1)-a0)
    print(f"  a*(k={k},M={M}) in [{float(lo):.5f}, {float(hi):.5f}]; Oler alone gives {a0:.5f}", flush=True)
    print(f"  fraction of the a-gap closed: {frac:.3f}", flush=True)
