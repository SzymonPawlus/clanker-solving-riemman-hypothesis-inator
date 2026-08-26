# packing-r5-eo7 — certified line-count bound for Erdős–Oler at k = 7

Write-up and full statement:
[`problems/circle-packing-equilateral-triangle/attacks/r5-eo7/`](../../problems/circle-packing-equilateral-triangle/attacks/r5-eo7/).

**Question.** How many points at pairwise distance $\ge 1$ fit in the closed equilateral
triangle $T(a')$ with $a' < 6$, if they lie on a family of equally spaced parallel lines
with spacing $\ge \sqrt3/2$ (which every unit-separation lattice does)? Erdős–Oler at
$k = 7$ needs the answer to be $\le 26$; 27 would refute it.

**Method.** Exact reduction to a 3-parameter space $(\varphi, \kappa, \rho)$ — line
direction folded by the $D_3$ symmetry of the triangle, spacing $h = \kappa\sqrt3/2$, and
the position of the family relative to the chord-profile peak — then interval
branch-and-bound with four symbolic caps (F1–F4 of the write-up) and exact rational
arithmetic on the slice $\varphi = 0$, where the extremal configuration sits.

**Result.** Certified $\le 25$ at $a = 6$ (target 26), in 175 boxes and under a second.
Matching exact witness: 22 lattice points in $T(5999/1000)$, checked in
$\mathbb{Q}(\sqrt3)$. Validated on the `cited` cases $k = 4, 5, 6$ (all close);
$k = 3$ does not close, because there the relaxation has exactly zero slack.
**The bound is discontinuous at zero perturbation** — see `delta_scan.py` and §7 of the
write-up. This is `numerical` evidence plus a `sketch` reduction; it is **not** a proof
of Erdős–Oler at $k = 7$ and nothing here is assumable.

## Reproduce from scratch

```bash
cd experiments/packing-r5-eo7 && mkdir -p out
python3 run_all.py            # THE headline table: k = 3..7, ~3 minutes
```

Everything else, individually:

```bash
python3 certify.py 6 26 out/bnb_a6_t26.json   # the k = 7 certificate alone (< 1 s)
python3 scan_line.py 6.0                      # float max of the same relaxation (24)
python3 scan_lattice.py 5.999999              # direct measurement of the lattice max (22)
python3 exact_check.py                        # exact Q(sqrt 3) 22-point witness
python3 delta_scan.py 6 26                    # robustness: discontinuous at delta = 0
python3 -c "from probe_forcing import stress; stress(trials=25, amps=(0.1,0.25,0.5))"
```

## Files

| file | what it does |
|---|---|
| `geometry.py` | chord profile of $T(a)$ for a line family; the float line bound |
| `certify.py` | **the certificate** — interval + exact branch-and-bound, checkpointed |
| `run_all.py` | sweeps $k = 3..7$ and writes `out/run_all.json` |
| `scan_line.py` | float scan of the relaxation's true maximum |
| `scan_lattice.py` | direct 5-parameter measurement of $\max_\Lambda\lvert\Lambda\cap T(a)\rvert$ |
| `exact_check.py` | exact $\mathbb{Q}(\sqrt3)$ verification of the 22-point witness |
| `delta_scan.py` | how much perturbation the bound tolerates (answer: none) |
| `probe_forcing.py` | line-defect measurements probing the forcing hypothesis |

## Determinism and environment

Python 3.11.15, `mpmath` 1.3.0 (`iv.dps = 30`), `numpy` 2.4.6, `fractions` from the
stdlib. No external data. `certify.py`, `run_all.py`, `exact_check.py`, `scan_line.py`
and `delta_scan.py` are fully deterministic — no randomness anywhere.
`scan_lattice.py` is a deterministic grid search. `probe_forcing.py` is the only
randomised script and pins `numpy.random.default_rng(20260824)`.

Floats appear only in `scan_*.py`, `delta_scan.py` and `probe_forcing.py`, which are
**measurements**. Every accept/reject decision in `certify.py` and `exact_check.py` is an
interval or exact-rational comparison, per the problem `RULES.md`.
