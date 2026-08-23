# `packing-n16-budget` — the area budget with the per-side counts pinned to 3/9/3

Companion code for
[`problems/circle-packing-equilateral-triangle/attacks/n16-budget/`](../../problems/circle-packing-equilateral-triangle/attacks/n16-budget/).

Recomputes the covering-area budget of
[`../../problems/circle-packing-equilateral-triangle/attacks/n16-covering-limit/`](../../problems/circle-packing-equilateral-triangle/attacks/n16-covering-limit/)
(Lemma S) with the per-side piece counts $(k_1,k_2,k_3)$ **pinned to $(3,3,3)$** by the class
structure of
[`../../problems/circle-packing-equilateral-triangle/attacks/n16-structure/`](../../problems/circle-packing-equilateral-triangle/attacks/n16-structure/)
§3.1, against a slab-LP bound on $f$ that is **re-derived here**, not imported.

| file | what it does |
|---|---|
| `exact.py` | certified rational enclosures of $\pi$ (Machin cross-checked against Euler), $\sqrt{\cdot}$, $\arcsin$ (cross-checked by $\sin$) |
| `fupper.py` | certified **upper** bound on $f(\ell)$: slab LP, value re-derived from an exactly verified rational dual certificate |
| `flower.py` | certified **lower** bounds on $f(\ell)$: the cut disk, and the lens $f(1)=\pi/3-\sqrt3/4$ via monotonicity |
| `budget.py` | Lemma S′ (pinned) and Lemma S (unpinned) at the same $f$ grid, and the ceiling of each — exact rational bisection on $a$ |

```sh
sh run.sh
```

No value of $s(n)$, $d(n)$, $a_n$, no repo packing and no covering number is an input anywhere
(kill-criterion B4). The only imported mathematics is the isodiametric (Bieberbach) inequality.
