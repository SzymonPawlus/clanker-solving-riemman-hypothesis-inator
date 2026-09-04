# packing-eo-covering

Constructions and exact certificates for the attack
[`problems/circle-packing-equilateral-triangle/attacks/eo-covering-construct/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-covering-construct/README.md):
partitions of the equilateral triangle $T_a$ (side $a$, separation-1 normalisation) into convex
sets of diameter $\le 1$.

**Reproduce every exact claim with one command:**

```
python3 experiments/packing-eo-covering/run.py
```

Standard library only. Exact $\mathbb{Q}(\sqrt3)$ / $\mathbb{Q}$ arithmetic in the triangular
basis $e_1=(1,0)$, $e_2=(1/2,\sqrt3/2)$, where $|ue_1+ve_2|^2=u^2+uv+v^2$ is rational. Exits
non-zero if any check fails.

| file | role |
|---|---|
| `exact.py` | the verifier: $\mathbb{Q}(\sqrt3)$ field with exact sign, exact polygon clipping, Voronoi/power cells, and `verify()` (containment, convexity, squared diameters, pairwise separation, exact area sum) |
| `build28.py` | the lattice construction: $\Delta(p)$ sites of spacing $\sqrt3/2$ centred in $T_a$ |
| `run.py` | all exact checks, including the lattice lemma for $p=2..10$ |
| `cert26/27/28/28opt.json` | exact rational certificates (sites + weights of a power diagram) |
| `rows.py` | the staggered-row accounting of README §4 (floats, accounting only) |
| `search.py`, `opt.py`, `worker.py`, `greedy.py`, `drive.py`, `addsite.py`, `honeycomb.py`, `hexinit.py` | the float search that *found* the certificates. Decides nothing |
| `mkcert.py`, `rationalise.py` | freeze a float configuration into an exact rational certificate |
| `packcheck.py` | self-check only: an explicit packing optimiser, used to test the resulting $a_n$ bounds for contradictions |

Floats appear only in the search. No float decides any claim.
