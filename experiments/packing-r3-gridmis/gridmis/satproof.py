"""SAT encoding of the independent-set decision, with an external DRAT proof.

The CNF says: "there exist >= target vertices, no two adjacent".  If a solver
reports UNSAT and an *independent* checker (drat-trim) validates the emitted
DRAT/DRUP proof, then alpha(G) < target is established without trusting the
SAT solver -- only the encoder (this file) and the checker.

The encoder is deliberately trivial so it can be audited by eye:
  * one variable per vertex,
  * one binary clause per edge,
  * one cardinality constraint  sum_v x_v >= target  from pysat.card.
"""

import os
import subprocess

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

__all__ = ["build_cnf", "solve_with_proof"]


def build_cnf(adj, target, card_enc=EncType.kmtotalizer):
    n = len(adj)
    pool = IDPool(start_from=n + 1)
    clauses = []
    for u in range(n):
        m = adj[u] >> (u + 1)
        v = u + 1
        while m:
            if m & 1:
                clauses.append([-(u + 1), -(v + 1)])
            m >>= 1
            v += 1
    card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=target,
                           vpool=pool, encoding=card_enc)
    clauses.extend([list(c) for c in card.clauses])
    nv = max(n, pool.top, max((abs(l) for c in clauses for l in c), default=n))
    return clauses, nv


def write_dimacs(path, clauses, nv):
    with open(path, "w") as f:
        f.write("p cnf %d %d\n" % (nv, len(clauses)))
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


def solve_with_proof(adj, target, workdir, tag, solver_name="glucose4",
                     drat_trim="drat-trim", check=True, timeout=None):
    """Returns dict with keys: result, cnf, proof, checked, checker_output."""
    os.makedirs(workdir, exist_ok=True)
    clauses, nv = build_cnf(adj, target)
    cnf_path = os.path.join(workdir, "%s.cnf" % tag)
    write_dimacs(cnf_path, clauses, nv)

    s = Solver(name=solver_name, bootstrap_with=clauses, with_proof=True)
    sat = s.solve()
    out = {"cnf": cnf_path, "nv": nv, "nclauses": len(clauses)}
    if sat:
        model = s.get_model()
        chosen = [v for v in range(len(adj)) if model[v] > 0]
        s.delete()
        out["result"] = "SAT"
        out["witness"] = chosen
        return out
    proof = s.get_proof()
    s.delete()
    proof_path = os.path.join(workdir, "%s.drat" % tag)
    with open(proof_path, "w") as f:
        f.write("\n".join(proof) + "\n")
        if not proof or proof[-1].strip() != "0":
            f.write("0\n")   # pysat omits the terminating empty clause
    out["result"] = "UNSAT"
    out["proof"] = proof_path
    out["proof_lines"] = len(proof)
    out["checked"] = None
    if check:
        try:
            cp = subprocess.run([drat_trim, cnf_path, proof_path],
                                capture_output=True, text=True, timeout=timeout)
            out["checker_output"] = cp.stdout[-2000:]
            out["checked"] = "s VERIFIED" in cp.stdout
        except subprocess.TimeoutExpired:
            out["checker_output"] = "TIMEOUT"
            out["checked"] = False
    return out
