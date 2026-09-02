"""Does Lemma A survive under the OTHER convention (empty set is not a dicut)?

C1 counts the empty dicut, so tau>=2 forces weak connectedness.  My checker does
NOT count it, so a weakly disconnected digraph can have tau>=2 for me.  The
question that matters: among tau>=2 instances under MY convention, is any
CONNECTED one bridged?  A connected bridged example would refute Lemma A's
bridgeless half, which is the only place C1 uses tau>=2.
"""
import random, sys
from dicut import dicuts
from robbins import components, has_bridge
from attack_c1 import rand_multidigraph

rng = random.Random(777)
disc = bridged_connected = tot = 0
witness = None
for _ in range(120000):
    n = rng.choice([3, 4, 5, 6])
    arcs = rand_multidigraph(rng, n)
    if len(arcs) < 2: continue
    cs = dicuts(n, arcs)
    if cs and min(len(c) for c in cs) < 2: continue
    tot += 1
    # restrict to vertices that carry an arc
    vs = {v for a in arcs for v in a}
    comps = [c for c in components(n, arcs) if c & vs]
    br = has_bridge(n, arcs)
    if len(comps) > 1:
        disc += 1
        if br is not None and witness is None:
            witness = ('disconnected+bridge', n, arcs, br)
    elif br is not None:
        bridged_connected += 1
        if witness is None or witness[0] != 'CONNECTED+BRIDGE':
            witness = ('CONNECTED+BRIDGE', n, arcs, br)
print(f"tau>=2 (nonempty-dicut convention): {tot}")
print(f"  weakly disconnected (>1 arc-carrying component): {disc}")
print(f"  CONNECTED but with a bridge  -> would refute Lemma A: {bridged_connected}")
print("  witness:", witness)
