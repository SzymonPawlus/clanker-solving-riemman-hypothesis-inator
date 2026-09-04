"""Threshold sweep: for each (n, g), find the largest tested d that is refuted."""
import json, math, sys, time
from fractions import Fraction as F
from gridmis.lattice import build_graph
from gridmis.mis import decide

def run(n, gs, ds_list, tb, out):
    rows = []
    for gstr in gs:
        g = F(gstr)
        for dstr in ds_list:
            d = F(dstr)
            t = time.time()
            G = build_graph(d, g)
            res = decide(G.adj, n, time_budget=tb)
            row = dict(n=n, g=gstr, d=dstr, d_float=float(d), V=G.n_vertices,
                       E=G.n_edges, rho=float(G.rho),
                       rho_eff=math.sqrt(float(G.rho_eff_sq())),
                       result=res[0], nodes=(res[1] if res[0] != "SAT" else None),
                       secs=round(time.time() - t, 2))
            rows.append(row)
            print(json.dumps(row), flush=True)
            with open(out, "w") as f:
                json.dump(rows, f, indent=1)
            if res[0] == "SAT":
                break
    return rows

if __name__ == "__main__":
    n = int(sys.argv[1]); tb = float(sys.argv[2]); out = sys.argv[3]
    gs = sys.argv[4].split(","); ds = sys.argv[5].split(",")
    run(n, gs, ds, tb, out)
