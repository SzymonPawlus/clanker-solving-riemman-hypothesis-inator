from fractions import Fraction as F
import relax as R, time, pickle, json
k = 7
a = F(6) - F(1, 100)
t = time.time()
cells, cc, cl, info = R.build(k, a)
print('built %d cells %d boxes in %.0fs' % (info['ncells'], info['nbox'], time.time() - t), flush=True)
t = time.time()
z, tr = R.find_feasible_random(cells, cc, cl, info['n'], tries=300000)
print('random: %s after %d restarts %.0fs' % ('FOUND' if z else 'none', tr, time.time() - t), flush=True)
if z:
    print('viol:', R.check_solution(cells, cl, z), flush=True)
    print('witness:', [(cells[i], z[i]) for i in range(len(cells)) if z[i]], flush=True)
    json.dump([[list(cells[i]), z[i]] for i in range(len(cells)) if z[i]], open('out/witness_k7.json', 'w'))
t = time.time()
z2, nodes = R.feasible(cells, cc, cl, info['n'], node_limit=200000000)
print('exhaustive k=7 -> %s (nodes=%d, %.0fs)' % ('FEASIBLE' if isinstance(z2, list) else str(z2), nodes, time.time() - t), flush=True)
if isinstance(z2, list):
    print('viol:', R.check_solution(cells, cl, z2), flush=True)
    print('witness2:', [(cells[i], z2[i]) for i in range(len(cells)) if z2[i]], flush=True)
