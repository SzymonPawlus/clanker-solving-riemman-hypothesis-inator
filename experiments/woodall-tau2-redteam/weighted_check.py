"""Sharpness check on the sketch's Schrijver-filter discharge.

The sketch locates the ONLY weighted failure at the packing constraint
chi^{J+} + chi^{J-} <= w, which bites exactly at weight-zero arcs.  That has a
falsifiable consequence:

    if w(a) >= 1 for EVERY arc and tau_w(D,w) = 2, a w-packing of two dijoins
    must exist.

A strictly-positive-weight instance with tau_w = 2 and no w-packing would show
the argument breaks somewhere else too, i.e. the sketch's located failure point
is wrong.  This also exercises the sketch's reduction step (replace a weight-k
arc by k parallel weight-one copies), which it takes on citation.

Space (stated exactly): every simple digraph on n = 4 labelled vertices with
2..8 arcs, crossed with EVERY weight vector in {1,2,3}^A (exhaustive); plus
every simple digraph on n = 5 with 2..7 arcs crossed with 40 random weight
vectors in {1,2,3}^A, seed 4242.
"""
import itertools, random, sys, time
from dicut import dicuts
from twocol import two_colourable

def wpack2(n, arcs, w):
    exp = []
    for i, a in enumerate(arcs):
        exp.extend([a] * w[i])
    cs = dicuts(n, exp)
    return True if not cs else (two_colourable(cs) is not None)

def sweep(n, lo, hi, exhaustive_weights, nrand, rng):
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    pairs += [(v, u) for (u, v) in pairs]
    tested = 0; bad = []
    for mask in range(1 << len(pairs)):
        arcs = [pairs[k] for k in range(len(pairs)) if mask >> k & 1]
        if not (lo <= len(arcs) <= hi):
            continue
        cs = dicuts(n, arcs)
        if not cs:
            continue
        ws = (itertools.product((1, 2, 3), repeat=len(arcs)) if exhaustive_weights
              else [tuple(rng.choice((1, 2, 3)) for _ in arcs) for _ in range(nrand)])
        for w in ws:
            if min(sum(w[i] for i in c) for c in cs) != 2:
                continue
            tested += 1
            if not wpack2(n, arcs, list(w)):
                bad.append((n, arcs, w))
    return tested, bad

rng = random.Random(4242); t0 = time.time()
t1, b1 = sweep(4, 2, 8, True, 0, rng)
print(f"n=4 exhaustive weights: {t1} strictly-positive instances with tau_w=2, "
      f"{len(b1)} with NO w-packing of 2 dijoins  [{time.time()-t0:.0f}s]")
for b in b1[:5]: print("   ", b)
sys.stdout.flush()
t2, b2 = sweep(5, 2, 7, False, 40, rng)
print(f"n=5 random weights:     {t2} strictly-positive instances with tau_w=2, "
      f"{len(b2)} with NO w-packing of 2 dijoins  [{time.time()-t0:.0f}s]")
for b in b2[:5]: print("   ", b)
