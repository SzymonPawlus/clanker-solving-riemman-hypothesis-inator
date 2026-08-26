# `packing-r5-exhaust4` — scale-invariant exact exhaustion for Erdős–Oler

**Claim kind: optimality / lower bound.** Status **`numerical`** for every run, **`sketch`** for
every derivation. Nothing here is assumable (repo `RULES.md` §3). Write-up and the mathematics:
[`problems/circle-packing-equilateral-triangle/attacks/r5-exhaust4/`](../../problems/circle-packing-equilateral-triangle/attacks/r5-exhaust4/README.md).

**The question.** Round-4 proposal AF: can the repo's exhaustion machinery mechanically reconstruct
EO(4), $d(9)=6$ — a result **already proved** by Melissen (1993)? Answer: no, and §4 of the
write-up proves it cannot at any resolution.

## The one command that reproduces everything

```sh
cd experiments/packing-r5-exhaust4 && ./run.sh          # ~12 min, 1 core, stdlib only
```

Python 3.11, standard library only (`fractions`, `math`), no seeds (the search is deterministic),
no floating point in any accept/reject decision.

## What it computes

The container is the **unit** equilateral triangle $A=(0,0)$, $B=(1,0)$, $C=(1/2,\sqrt3/2)$,
closed, and the parameter is a rational separation threshold $t$:

* `--strict` refutes *n points at pairwise distance $> t$*. By Proposition 1 of the write-up this
  is equivalent to "no $n$ points at separation $\ge 1$ in $T(a)$ **for every** $a < 1/t$" — an
  argument **uniform in the side**, which is what `attacks/eo-exhaustion/` §1.2(a) says a finite
  computation has to produce.
* without `--strict`, it refutes *pairwise distance $\ge t$*, equivalent to the single statement
  $d(n) > 2/t$ at one rational side.

```sh
python3 -m eo4 --n 5  --t 1/2  --strict --max-level 4 --max-cited 4   # EO(3), uniform in a
python3 -m eo4 --n 10 --t 1/3  --strict --max-level 3 --max-cited 4   # Oler, Delta(4)
python3 -m eo4 --n 9  --t 20/59 --max-level 8                          # d(9) > 5.9
python3 -m eo4 --n 9  --t 1/3  --strict --max-level 6                  # EO(4): never closes
python3 nontermination.py 12 out/nontermination.json                   # why it never closes
python3 analyse.py 9 1/3 1 5 out/an-n9-L5.json 900                     # survivor localisation
```

`proved` is the only outcome that establishes anything. `unresolved`, `timeout` and `nodelimit`
**prove nothing at all**, and the CLI says so in words.

## Soundness of each rule (details in the write-up §2)

| rule | why it is sound | exactness |
|---|---|---|
| branching | children are closed and cover the parent (derived in `geom.children`, sampled in `run.sh`) | integer lattice |
| pair | squared distance is convex, so `maxsep` is attained at a vertex pair | integer comparison $q^2\max(a^2{+}ab{+}b^2) \le p^2 4^L$ |
| capacity | rescaling by the actual minimum separation; strictness buys the boundary case | rational, or certified enclosures that **fail closed** |
| Oler-hull | Oler (1961) `cited`, on $\operatorname{conv}(E)$, relaxed to the hull of the cells | area exactly rational ($\sqrt3$ cancels); perimeter **over**-estimated, so the rule fires less often, and perfect squares are exact |
| $D_3$ at the root | the group permutes the three level-1 corner cells as $S_3$ | — |

**Circularity guard.** `eo4/caps.py` carries $a(m)=d(m)/2$ only for $m \le 8$. $a(9)=3$ *is* the
statement being reconstructed and $a(10)=3$ is Oler's $\Delta(4)$ theorem; neither is available to
any run. `--max-cited 4` removes $a(5),\dots,a(8)$ as well, and the EO(3) and Oler validation rows
are run that way so that no row assumes its own conclusion.

## Validation, run before anything else

`run.sh` executes these first and they must all pass:

* $n=3,t=1$; $n=6,t=1/2$; $n=10,t=1/3$; $n=15,t=1/4$ — `proved` at the root (Oler's $\Delta(k)$).
* $n=5$, $t=1/2$, strict, `--max-cited 4` — `proved` in one node: **EO(3) reconstructed
  uniformly in $a$**.
* $n=9$, $t=3/10$ — must come back **unresolved** ($a=10/3>3$: nine points really do fit).
* $n=9$, $t=1/3$, closed — must come back **unresolved** (nine points at separation exactly $1/3$
  really do fit).

## Layout

```
eo4/geom.py    dyadic cells, integer quadratic form, exact hull/area, rational sqrt bounds
eo4/caps.py    cited a(m) table (m <= 8) and the per-cell capacity rule
eo4/search.py  the prover: rules, exhaustive branching, DFS, survivor enumeration
eo4/__main__.py  CLI
nontermination.py  builds the Delta(4)-lattice-minus-one node at each level and asks the
                   prover whether ANY rule fires (it never does)
analyse.py         streams the surviving level-L profiles and reports the supportable region
enumerate_survivors.py  same, but keeps the profiles and their centroids
out/               all results, including checkpoints written during the runs
```
