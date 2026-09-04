"""Shrink the exact refuting point set to a small unsatisfiable core using
assumption-based core extraction, then re-verify with independent solvers."""
import sys, os, json, time
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refute_exact import in_U, edges, solve

d = os.path.dirname(os.path.abspath(__file__))
P = [(F(x), F(y)) for x, y in json.load(open(os.path.join(d, "refutation_points.json")))["points"]]
print("start |P| =", len(P), flush=True)
assert all(in_U(p) for p in P), "a point is not exactly inside U"

from pysat.solvers import Cadical153


def core_once(pts, k=5):
    n = len(pts); E = edges(pts)
    var = lambda p, c: p * k + c + 1
    sel = lambda p: n * k + p + 1
    cnf = [[-sel(p)] + [var(p, c) for c in range(k)] for p in range(n)]
    for (i, j) in E:
        for c in range(k):
            cnf.append([-var(i, c), -var(j, c)])
    s = Cadical153(bootstrap_with=cnf)
    r = s.solve(assumptions=[sel(p) for p in range(n)])
    assert not r
    core = sorted(abs(l) - n * k - 1 for l in s.get_core())
    s.delete()
    return [pts[i] for i in core]


cur = P
for it in range(12):
    nxt = core_once(cur)
    print(f"  core pass {it}: {len(cur)} -> {len(nxt)}", flush=True)
    if len(nxt) == len(cur):
        break
    cur = nxt

# final greedy one-point deletion pass on the (now small) core
i = 0
while i < len(cur):
    trial = cur[:i] + cur[i + 1:]
    r, dt, ne, cnf, pf = solve(trial, 5)
    if not r:
        cur = trial
    else:
        i += 1
print("minimal core size:", len(cur), flush=True)

r, dt, ne, cnf, pf = solve(cur, 5, proof=True)
print("core is UNSAT:", not r, " edges:", ne, f" ({dt:.3f}s)")
json.dump({"n": len(cur), "edges": ne, "sec": dt,
           "points": [[str(x), str(y)] for x, y in cur]},
          open(os.path.join(d, "refutation_core.json"), "w"), indent=2)
with open(os.path.join(d, "core.drat"), "w") as f:
    f.write("\n".join(pf) + "\n")
nv = max(abs(l) for cl in cnf for l in cl)
with open(os.path.join(d, "core.cnf"), "w") as f:
    f.write(f"p cnf {nv} {len(cnf)}\n")
    for cl in cnf:
        f.write(" ".join(map(str, cl)) + " 0\n")

from pysat.solvers import Glucose42, Minisat22, Lingeling
for S in (Glucose42, Minisat22, Lingeling):
    try:
        s = S(bootstrap_with=cnf)
        print(f"  {S.__name__}: {'SAT' if s.solve() else 'UNSAT'}"); s.delete()
    except Exception as e:
        print(" ", S.__name__, "unavailable:", e)
try:
    import z3
    n = len(cur); E = edges(cur)
    c = [z3.Int(f"c{i}") for i in range(n)]
    sol = z3.Solver()
    for v in c: sol.add(v >= 0, v <= 4)
    for (i, j) in E: sol.add(c[i] != c[j])
    t0 = time.time(); res = sol.check()
    print(f"  z3 (independent integer encoding): {res}  ({time.time()-t0:.2f}s)")
except Exception as e:
    print("  z3 unavailable:", e)
