# `packing-n16-limit` — how large can $a$ be if $T_a$ is covered by 15 sets of diameter $<1$?

Companion code for
[`problems/circle-packing-equilateral-triangle/attacks/n16-covering-limit/`](../../problems/circle-packing-equilateral-triangle/attacks/n16-covering-limit/).

This is the **upper**-bound side of the covering route to $n = 16$: it bounds
$A_{15} = \sup\{a : T_a$ is coverable by 15 sets of diameter $<1\}$ from above, which is the
largest $a_{16}$ any covering argument of that shape could ever certify.

| file | what it does |
|---|---|
| `exactconst.py` | certified rational enclosures of $\pi$ (Machin, cross-checked against Euler's $\arctan\frac12+\arctan\frac13$), $\sqrt{\cdot}$, $\arcsin$ |
| `fbound.py` | certified **upper** bound on the edge-piece area $f(\ell)$: slab LP solved numerically, then re-derived from an exact rational dual certificate |
| `f_lower.py` | `numerical` lower bounds on $f(\ell)$ (star polygons) — slack measurement only |
| `ceiling.py` | certified **lower** bound on $f(\ell)$ (explicit cut-disk), hence the ceiling of the whole method |
| `outer.py` | the structure lemma → the bound on $A_{15}$, exact rational bisection |

```sh
sh run.sh          # ~7 min cold, ~35 s with out/f_grid.json cached
```

No value of $s(n)$, $d(n)$ or $a_n$ from the literature or from `results/` is an input anywhere
(kill-criterion K2).
