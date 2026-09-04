import argparse, json, sys
from fractions import Fraction
from .search import Prover

p = argparse.ArgumentParser(prog="eo4")
p.add_argument("--n", type=int, required=True)
p.add_argument("--t", type=str, required=True, help="rational separation threshold in T(1)")
p.add_argument("--strict", action="store_true", help="distances > t (uniform in a); else >= t")
p.add_argument("--max-level", type=int, default=6)
p.add_argument("--no-oler", action="store_true")
p.add_argument("--no-symmetry", action="store_true")
p.add_argument("--max-cited", type=int, default=8)
p.add_argument("--node-limit", type=int, default=None)
p.add_argument("--time-limit", type=float, default=None)
p.add_argument("--out", type=str, default=None)
a = p.parse_args()

pr = Prover(a.n, Fraction(a.t), a.strict, a.max_level,
            use_oler=not a.no_oler, use_symmetry=not a.no_symmetry,
            max_cited=a.max_cited)
res = pr.run(node_limit=a.node_limit, time_limit=a.time_limit,
             checkpoint=(a.out + ".ckpt") if a.out else None)
if a.out:
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "witness_node"}))
if res["outcome"] == "proved":
    t = Fraction(a.t)
    if a.strict:
        print("PROVED: no %d points at pairwise distance > %s lie in the closed unit "
              "triangle.  Equivalently d(%d) >= %s (uniform in a)." % (a.n, t, a.n, 2 / t))
    else:
        print("PROVED: no %d points at pairwise distance >= %s lie in the closed unit "
              "triangle.  Equivalently d(%d) > %s." % (a.n, t, a.n, 2 / t))
else:
    print("NOTHING IS PROVED by this run (%s)." % res["outcome"])
