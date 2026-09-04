"""Sweep with both engines: exact B&B (`mis.decide`) and SAT (glucose4).

For each g, walk d upward until the instance stops being refutable.
Everything is checkpointed to JSON after every instance.
"""
import json, math, sys, time
from fractions import Fraction as F
from gridmis.lattice import build_graph
from gridmis.mis import decide
from gridmis.satproof import build_cnf
from pysat.solvers import Solver


def one(n, d, g, tb, engines=("bnb", "sat")):
    t0 = time.time()
    G = build_graph(d, g)
    row = dict(n=n, g=str(g), d=str(d), d_float=float(d), V=G.n_vertices,
               E=G.n_edges, rho=float(G.rho),
               rho_eff=math.sqrt(float(G.rho_eff_sq())),
               build_secs=round(time.time() - t0, 2))
    verdict = None
    if "bnb" in engines:
        t = time.time()
        res = decide(G.adj, n, time_budget=tb)
        row["bnb"] = res[0]
        row["bnb_nodes"] = res[1] if res[0] != "SAT" else None
        row["bnb_secs"] = round(time.time() - t, 2)
        if res[0] == "SAT":
            row["witness"] = [G.verts[v] for v in res[1]]
        verdict = res[0]
    if "sat" in engines and verdict != "SAT":
        t = time.time()
        cl, nv = build_cnf(G.adj, n)
        s = Solver(name="glucose4", bootstrap_with=cl)
        s.conf_budget(int(4e7))
        r = s.solve_limited(expect_interrupt=False)
        s.delete()
        row["sat_clauses"] = len(cl)
        row["sat"] = {True: "SAT", False: "UNSAT", None: "UNKNOWN"}[r]
        row["sat_secs"] = round(time.time() - t, 2)
        if verdict != "UNSAT":
            verdict = row["sat"]
    row["verdict"] = verdict
    return row


if __name__ == "__main__":
    n = int(sys.argv[1]); tb = float(sys.argv[2]); out = sys.argv[3]
    gs = sys.argv[4].split(","); ds = sys.argv[5].split(",")
    engines = tuple(sys.argv[6].split(",")) if len(sys.argv) > 6 else ("bnb", "sat")
    rows = []
    for gstr in gs:
        for dstr in ds:
            row = one(n, F(dstr), F(gstr), tb, engines)
            rows.append(row)
            print(json.dumps(row), flush=True)
            with open(out, "w") as f:
                json.dump(rows, f, indent=1)
            if row["verdict"] != "UNSAT":
                break
