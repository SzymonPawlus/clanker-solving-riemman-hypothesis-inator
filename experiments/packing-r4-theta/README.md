# `packing-r4-theta` — the container-$\vartheta'$ ceiling gate

Worker `r4-theta`, 2026-08-24. Executes proposal **AC** of
`problems/circle-packing-equilateral-triangle/attacks/r3-approaches/README.md`.
Write-up: `problems/circle-packing-equilateral-triangle/attacks/r4-theta/README.md`.

```
claim type: NEITHER construction nor optimality.  No bound on d(n) or s(n) is
            produced or asserted here.
status:     `numerical` for every number this code prints.  SDP output is a
            hypothesis, never a bound (RULES.md §3).
```

## The question

Proposal AC models packing as independent set on the infinite conflict graph
$G_d$ (vertices = points of the closed triangle $T_d$; edges = pairs at distance
$< 2$) and proposes to bound $\alpha(G_d)$ by the Lovász $\vartheta'$ of that graph,
via an SOS problem in 4 variables. Then $\vartheta'(G_d) < n$ would give $d(n) > d$.

**Is $\vartheta'$ strong enough to be worth the trouble — specifically, can it beat
Oler's $d(n) \ge \sqrt{8n+1} - 3$?**

## The method

Not by solving the SOS problem (which was *not* solved here — see the write-up §6).
By a one-sided ceiling test that needs no SOS at all:

> For any **finite** $W \subset T_d$, a feasible kernel for $G_d$ restricts to a feasible
> matrix for the finite graph $G_d[W]$, so $\vartheta'(G_d[W]) \le \vartheta'(G_d)$.
> Hence exhibiting a finite $W$ with $\vartheta'(G_d[W]) \ge n$ proves the $\vartheta'$
> method cannot certify $d(n) > d$ — against **every** kernel, of every degree.

So: take $W$ = a triangular grid in $T_d$ at $d$ below the known $d(n)$, solve one
ordinary SDP, and see whether the value reaches $n$. A value $\ge n$ kills the method at
that $d$; a value $< n$ proves nothing.

Three care points, all in `theta_gate.py`:

* **Adjacency is exact.** For grid points differing by $(a,b)$ the squared distance is
  $h^2(a^2+ab+b^2)$, so "distance $< 2$" is an integer-versus-algebraic comparison decided
  symbolically in `sympy` (corner grid) or a pure integer comparison (anchored grid). Exact
  ties are exactly the distance-2 pairs and are resolved as **non**-edges (all inequalities
  in this problem are non-strict).
* **Two witness families.** The *corner-to-corner* grid (spacing $d/(k-1)$) and the
  *lattice-anchored* grid (spacing exactly $2/r$, anchored at corner $A$). The first has a
  real defect: for generic $d$ its spacing is incommensurate with 2, so it contains no pair
  at distance exactly 2 and its $\alpha$ undershoots $\alpha(T_d)$ — at $d = 7.99$ it found
  10 where the container holds 14. The anchored grid contains the triangular packing and is
  the sharper instrument. Both are admissible witnesses.
* **The reported $\vartheta'$ is a repaired-primal lower bound, not solver output.** The
  solver's $B$ is symmetrised, zeroed on edges, clipped non-negative, shifted by $tI$ to be
  psd, and rescaled to unit trace; the objective is evaluated there. Solver error can only
  shrink this number, never invalidate it — the direction the ceiling lemma needs.

## Result

No ceiling was detected: on every witness and at every $d$ tested, $\vartheta'(G_d[W])$ came
out at or barely above $\alpha(G_d[W])$, never reaching $n$. That is a **null** result — the
instrument is one-sided and can only detect weakness. See `results.json` and the write-up.

What did emerge is a cost argument (write-up §2.4): any feasible kernel has rank
$\ge \alpha(G_d) - 1$, so a kernel of degree $\le m$ per argument needs
$\binom{m+2}{2} \ge \alpha - 1$, i.e. $m \gtrsim \sqrt{2n}$. AC's "size independent of $n$"
is true of the variable count (4) and false of the degree, hence of the SDP size.

## Reproduce

```bash
cd experiments/packing-r4-theta && python3 theta_gate.py --selftest && python3 run_gate.py --all --budget 780 && python3 run_anchored.py && python3 make_table.py
```

Runtime about 20 minutes on 4 idle cores. `run_gate.py` checkpoints to `results.json` after
every solve and honours `--budget` (seconds), so a partial run is still a usable partial
result; `run_anchored.py` appends to the same file. `make_table.py` renders `results.json`
as the markdown tables in the write-up. **Run only one battery at a time** — they append to
the same `results.json`, and competing for cores makes the per-solve cap bite.

`python3 theta_gate.py --selftest` alone takes ~20 s and is the thing to run first: it checks
$\vartheta'$ against $K_5$, $\overline{K_6}$, $C_5$, Petersen, the sandwich
$\alpha \le \vartheta' \le \bar\chi_f$ on random graphs, and — the ones that matter — both
grid conflict graphs against the `cited` exact optima $\Delta(k)$ at $d = 2(k-1)$, including
on grids finer than the packing.

## Files

| file | what |
|---|---|
| `theta_gate.py` | formulation, lemma statements in the docstring, $\vartheta'$ solvers, exact adjacency for both witness families, primal repair, self-tests |
| `run_gate.py` | battery 1 (corner grid): which $(n, d, \text{grid})$ are measured, with checkpointing |
| `run_anchored.py` | battery 2 (anchored grid), the sharper witness |
| `make_table.py` | renders `results.json` to markdown |
| `results.json` | generated; one record per solve |

## Environment

Python 3.11.15, `numpy` 2.4.6, `scipy` 1.17.1, `sympy` 1.14.0, `cvxpy` 1.9.2
(solvers CLARABEL and SCS), `networkx` 3.6.1. SCS is run at `eps = 1e-5` with a per-solve wall-clock cap; CLARABEL is used for the small self-test
graphs. The only seed is `numpy.random.default_rng(20260824)` for the six random self-test
graphs; the grids and the SDPs are deterministic. The one non-reproducible quantity is SCS's
stopping point under the time cap, recorded per row (`status`, `solve_s`), which affects only
how *weak* the reported lower bound is.
