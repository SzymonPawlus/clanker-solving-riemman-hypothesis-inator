"""Focused SAT-only push: for one (n, g), test a list of d values, checkpointing."""
import json, math, sys, time
from fractions import Fraction as F
from gridmis.lattice import build_graph
from gridmis.satproof import build_cnf
from pysat.solvers import Solver

n = int(sys.argv[1]); gstr = sys.argv[2]; out = sys.argv[3]
ds = sys.argv[4].split(",")
rows = []
for dstr in ds:
    g, d = F(gstr), F(dstr)
    t = time.time()
    G = build_graph(d, g)
    cl, nv = build_cnf(G.adj, n)
    tb = time.time()
    s = Solver(name="glucose4", bootstrap_with=cl)
    r = s.solve()
    s.delete()
    row = dict(n=n, g=gstr, d=dstr, d_float=float(d), V=G.n_vertices, E=G.n_edges,
               rho_eff=math.sqrt(float(G.rho_eff_sq())),
               scaled_side=2 * (float(d) + 2 * math.sqrt(3) * float(G.r)) / math.sqrt(float(G.rho_eff_sq())),
               clauses=len(cl), sat="SAT" if r else "UNSAT",
               solve_secs=round(time.time() - tb, 1), total_secs=round(time.time() - t, 1))
    rows.append(row); print(json.dumps(row), flush=True)
    json.dump(rows, open(out, "w"), indent=1)
