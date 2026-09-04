"""Pass 2 of the exhaustive attack.

Space A (stated exactly): every SIMPLE digraph on n=5 labelled vertices --
each of the 20 ordered pairs present or not, 2^20 = 1048576 digraphs, all of
them, no isomorphism reduction, no loops.
Space B: 300000 uniformly random digraphs on n=5 with each ordered pair given
multiplicity 0/1/2/3 (probabilities 0.45/0.35/0.15/0.05), to cover parallel
arcs which space A misses.
Same five checks as exhaustive.py.
"""
import itertools, random, sys
from dicut import dicuts, is_dijoin
from twocol import two_dijoins_exact
from robbins import robbins_colouring, components, has_bridge, strongly_connected_on
from exhaustive import check_digraph

n = 5
pairs = [(u, v) for u in range(n) for v in range(n) if u != v]
stats = {'tau2': 0, 'total': 0, 'disconnected_tau2': 0}
fails = []
for mask in range(1 << len(pairs)):
    arcs = [pairs[k] for k in range(len(pairs)) if mask >> k & 1]
    stats['total'] += 1
    if len(arcs) < 2: continue
    check_digraph(n, arcs, stats, fails)
print(f"SPACE A: n=5 simple, all {stats['total']} digraphs; tau=2: {stats['tau2']} "
      f"(disconnected {stats['disconnected_tau2']}); FAILURES: {len(fails)}")
for f in fails[:20]: print("   ", f)

random.seed(20260902)
stats2 = {'tau2': 0, 'total': 0, 'disconnected_tau2': 0}
fails2 = []
for _ in range(300000):
    arcs = []
    for p in pairs:
        r = random.random()
        k = 0 if r < .45 else 1 if r < .80 else 2 if r < .95 else 3
        arcs.extend([p] * k)
    stats2['total'] += 1
    if len(arcs) < 2: continue
    check_digraph(n, arcs, stats2, fails2)
print(f"SPACE B: n=5 random multi, {stats2['total']} digraphs; tau=2: {stats2['tau2']} "
      f"(disconnected {stats2['disconnected_tau2']}); FAILURES: {len(fails2)}")
for f in fails2[:20]: print("   ", f)
