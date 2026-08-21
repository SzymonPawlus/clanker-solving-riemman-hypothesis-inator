# `packing-eo-equality` — exact checks for the Oler equality-case attack

Supports [`problems/circle-packing-equilateral-triangle/attacks/eo-oler-equality/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-oler-equality/).
Python standard library only; no dependencies, no seeds beyond the one pinned below.

```bash
cd experiments/packing-eo-equality
python3 run.py             # -> out/report.txt        (exact; ~40 s)
python3 lattice_probe.py   # -> out/lattice_probe.txt (numerical; ~4 min)
python3 capacity_probe.py  # -> out/capacity_probe.txt (numerical; ~3 min)
```

Tested with CPython 3.11. `run.py` imports `../packing-oler-slack/exact.py` (the
$\mathbb Q(\sqrt3,\sqrt{11})$ field and outward-rounded rational intervals) read-only; every other
line here is written for this attack.

**Normalisation: separation 1, Oler's own.** Nothing in this directory reads the repo's
certificates (which use separation 2 and side $d=2a$), so no conversion is performed anywhere.

## What each script decides

| script | section | arithmetic | what it decides |
|---|---|---|---|
| `run.py` | 1 | exact over $\mathbb Q$ | Lemma T on 155 120 triangles: no violation, exactly two equality triples $(1,1,1)$ and $(1,1,2)$ |
| | 2 | exact over $\mathbb Q$ | the polynomial identity and the vertex-minimisation step inside the proof of Lemma T |
| | 3 | exact in $\mathbb Q(\sqrt3)$, rigorous rational enclosures for perimeters | the Oler slack of 12 lattice-convex and near-lattice configurations |
| | 4 | same | the $\tau$-identity on 7 configurations with hand-given triangulations, plus $F=2n-b-2$, $\lvert\mathcal E_{\rm int}\rvert=3n-2b-3$, $\sum A_f=A(P)$ |
| | 5 | exact over $\mathbb Q$ | the arithmetic of Theorem T4 |
| | 6 | exact over $\mathbb Q$ | Oler's RHS $=T(k)$ at $a=k-1$; the $k=7$ window; the $\varepsilon$-scale |
| | 7 | exact in $\mathbb Q(\sqrt3)$ | face excess at a lattice with its corners pushed out (control on `eo-boundary-counting` W1) |
| `lattice_probe.py` | — | **floats** | $\max_\Lambda\lvert\Lambda\cap T(a)\rvert$ by grid search — `numerical`, evidence only |
| `capacity_probe.py` | — | **floats** | size of a hexagonal diameter-$<1$ covering of $T(a)$ — `numerical`, evidence only |

Exactness matters in exactly one place and it is worth naming: with rational side lengths
$16A^2$ is rational (Heron), so the sign of $\frac2{\sqrt3}A+\frac p2-2$ is decided by a single
rational comparison. No decision in `run.py` is ever taken on a float.

`run.py` §1(b) is randomised: `random.Random(20260821)`, 200 000 draws, of which 142 714 are
triangles. The other three scans in §1 are deterministic.

The two probe scripts are float-only and are labelled `numerical` in the attack write-up. They
measure constructions; they prove nothing. `lattice_probe.py`'s "translation-robust" rows use an
outward margin $\mu$ exceeding half the translation-grid spacing, which makes the tabulated count
dominate every translation — but the orientation is still sampled, not covered.
