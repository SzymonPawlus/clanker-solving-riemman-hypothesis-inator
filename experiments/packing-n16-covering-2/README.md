# `packing-n16-covering-2` — 15-piece covering lower bound for $n=16$, round 2

Attack write-up:
[`problems/circle-packing-equilateral-triangle/attacks/n16-covering-2/`](../../problems/circle-packing-equilateral-triangle/attacks/n16-covering-2/).

Everything here is Python 3.11 + `numpy` 2.4.6 + `scipy` 1.17.1 (used **only** in the float
search) and the standard library `fractions` (used for **every** decision).

## Reproduce the result — one command each, no seeds, no network

```bash
python3 exact_1p2r3.py        # the exact Q(sqrt3) certificate at a = 1 + 2*sqrt3   (~1 s)
python3 verify_c1.py cert_rational.json   # the purely rational strict certificate  (~1 s)
python3 selftest.py           # 10 adversarial corruptions, all must be REJECTed    (~2 s)
```

## Files

| file | role |
|---|---|
| `q3.py` | exact arithmetic in $\mathbb{Q}(\sqrt3)$, written for this attack; every comparison decided by an exact sign test |
| `verify_c1.py` | **independent exact certifier**, written from the problem statement without reading either predecessor certifier. Works over `Fraction` or `Q3`. Five checks, including a from-first-principles covering proof |
| `selftest.py` | adversarial tests: 10 corruptions the certifier must reject |
| `exact_1p2r3.py` | the extremal configuration at $a=1+2\sqrt3$, exact, plus the dilation argument |
| `rational_cert.py`, `cert_rational.json` | the same configuration with $\sqrt3$ replaced by a rational and dilated back under diameter 1 — a self-contained **rational, strict** certificate |
| `freeze.py`, `cert_hex.json` | float subdivision $\to$ exact rational certificate (earlier, coarser route) |
| `slp.py` | the sequential-LP minimax optimiser (floats; the reason this round moved) |
| `comb.py` | combinatorial structures + Tutte barycentric embedding |
| `moves.py`, `beam.py`, `anneal.py` | search over combinatorial structures (flips, contraction, beam/annealing) |
| `gen.py`, `patterns.py` | structure generators from power diagrams and from explicit site layouts |
| `sub_*.json`, `opt_n15_*.json` | the predecessor's frozen search states (`experiments/packing-n16-covering/`), kept as inputs so "all five converge to $1+2\sqrt3$" is reproducible |
| `st_*.json` | SLP optima of those structures |
| `pt_*.log` | pattern-search traces |

## Reproducing the search claims

```bash
for f in sub_s1 sub_s2 sub_s6 sub_s7 sub_seed2; do python3 slp.py $f.json /tmp/o.json 500; done
python3 patterns.py 21 3000 /tmp/pt.json     # ~25 min; never exceeds 4.464101615
python3 beam.py st_hex.json /tmp/b.json 2 6 3  # flip neighbourhood of the optimum
```
