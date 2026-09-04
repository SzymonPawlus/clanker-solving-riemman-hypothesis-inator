import sys, time
from search_eg_exact import minimal_2covers
from dicut import dicuts
from twocol import two_colourable
n=7
pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
P=len(pairs); ndig=tested=0; found=[]; t0=time.time()
for mask in range(1<<P):
    arcs=[pairs[k] for k in range(P) if mask>>k&1]
    if len(arcs)<2: continue
    cs=dicuts(n,arcs)
    if not cs: continue
    if any(len(c)<2 for c in cs): continue
    ndig+=1
    for S in minimal_2covers(cs,len(arcs)):
        tested+=1
        if two_colourable([c&S for c in cs]) is None:
            found.append((arcs,sorted(S))); print("CEX",arcs,sorted(S)); sys.stdout.flush()
    if mask % 100000 == 0:
        print(f"progress mask={mask}/{1<<P} admissible-digraphs={ndig} supports={tested} cex={len(found)} t={time.time()-t0:.0f}s"); sys.stdout.flush()
print(f"DONE n=7: {ndig} DAGs all of whose dicuts have size>=2, {tested} minimal supports, {len(found)} counterexamples")
