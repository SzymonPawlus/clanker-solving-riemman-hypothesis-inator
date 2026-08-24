"""Emit a DRAT proof for each named refutation and check it with drat-trim."""
import json, sys, time
from fractions import Fraction as F
from gridmis.lattice import build_graph
from gridmis.satproof import solve_with_proof

CASES = [
    # (n, g, d)  -- each must be a refutation (UNSAT)
    (12, "1/4", "62/10"),
    (12, "1/6", "68/10"),
    (12, "1/8", "7"),
    (16, "1/4", "8"),
]

if __name__ == "__main__":
    cases = CASES
    if len(sys.argv) > 1:
        cases = [tuple(c.split(":")) for c in sys.argv[1].split(",")]
        cases = [(int(a), b, c) for a, b, c in cases]
    rows = []
    for (n, gstr, dstr) in cases:
        tag = "n%d_g%s_d%s" % (n, gstr.replace("/", "-"), dstr.replace("/", "-"))
        t = time.time()
        G = build_graph(F(dstr), F(gstr))
        out = solve_with_proof(G.adj, n, "out", tag, timeout=1800)
        row = dict(n=n, g=gstr, d=dstr, V=G.n_vertices, E=G.n_edges,
                   result=out["result"], nv=out["nv"], nclauses=out["nclauses"],
                   proof_lines=out.get("proof_lines"), drat_verified=out.get("checked"),
                   secs=round(time.time() - t, 1), tag=tag)
        rows.append(row)
        print(json.dumps(row), flush=True)
        print((out.get("checker_output") or "").strip()[-400:], flush=True)
        json.dump(rows, open("out/proofs.json", "w"), indent=1)
