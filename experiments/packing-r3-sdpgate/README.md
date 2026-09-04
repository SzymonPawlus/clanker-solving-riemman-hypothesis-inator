# `packing-r3-sdpgate` — the Lasserre/moment strength gate

**These are computations, not proofs.** Everything produced here is `numerical`, and the SDP
values are floating-point solver output: *a lower bound read off a float SDP is a hypothesis
about a bound, never a bound* (`problems/circle-packing-equilateral-triangle/RULES.md` §0).
Nothing here is rationally rounded, so nothing here may be quoted as a bound on $d(n)$ or $s(n)$.

## The question

Round-3 proposal **X**
(`problems/circle-packing-equilateral-triangle/attacks/r3-approaches/README.md`) claimed that
after $S_n$-symmetry reduction the Lasserre relaxation of the packing problem is *small*, thereby
reversing round 1's approach **C**, which had retired the direction on expected SDP size. Two
questions follow, in this order:

1. **Is the size claim right?** (`symmetry_sizes.py`)
2. **Does size matter — i.e. is the relaxation any good?** (`moment_gate.py`, `elementary_bound.py`)

## Formulation

Point formulation, repo conventions: $A = (0,0)$, $B = (1,0)$, $C = (1/2, \sqrt3/2)$ — the
**unit** triangle, so no side parameter appears. Write

$$f(n) \;=\; \max_{p_1,\dots,p_n \in T_1}\ \min_{i<j}\ \lVert p_i - p_j\rVert^2 .$$

Because a packing at separation $\ge 2$ fits in $T_d$ exactly when $d^2 f(n) \ge 4$,

$$d(n) \;=\; 2/\sqrt{f(n)},$$

so an *upper* bound $f_L \ge f(n)$ from a level-$L$ moment relaxation gives a *lower* bound
$d_L = 2/\sqrt{f_L} \le d(n)$. The polynomial program is approach C's, verbatim — maximise $t$
subject to $\lVert p_i-p_j\rVert^2 - t \ge 0$, three half-plane containments per point, and
$0 \le t \le 1$ (valid for $n \ge 2$: the diameter of $T_1$ is $1$). $t$ is a decision variable,
so $N = 2n+1$.

## Files

| file | what it does |
|---|---|
| `symmetry_sizes.py` | independent re-derivation of the $S_n$-isotypic block structure: Murnaghan–Nakayama via beta-sets, exact `Fraction` arithmetic, self-checking on $\sum_\lambda m_\lambda \dim\lambda = \binom{N+L}{L}$ |
| `moment_gate.py` | builds and solves the **dense** level-$L$ moment relaxation with `cvxpy`; `--selftest` validates on instances with closed-form answers |
| `elementary_bound.py` | the trivial mean-pairwise-squared-distance bound $f(n) \le 2n/(3(n-1))$, for comparison |
| `extra_test.py` | tests the "you under-built the relaxation" objection: re-solves level 2 with redundant *valid* inequalities added |
| `make_table.py` | renders the slack table as markdown from the JSON (presentation only, computes nothing) |
| `results_*.json`, `*.log` | solver output, checked in as the record of the runs |

## Reproduce

Single command, from this directory:

```bash
bash reproduce.sh
```

That runs, in order: the symmetry derivation (including the reduced-size scan to level 5 at
$n = 16$), the self-tests, the elementary bound, and the level-2 sweep over
$n = 4,5,6,7,8,10,12$. Expect **20–60 minutes** depending on machine load; the SDPs at
$n = 10, 12$ dominate. Everything is deterministic — there are **no random seeds anywhere** in
this experiment.

The two optional extras are not in `reproduce.sh` because each takes another 10–20 minutes:

```bash
python3 moment_gate.py --sweep --level 3 --ns 4 --tcap 1.0 --solver SCS --eps 1e-5 --max-seconds 240
python3 extra_test.py
```

## Environment (pinned)

Python 3.11.15; `numpy` 2.4.6, `scipy` 1.17.1, `sympy` 1.14.0 (preinstalled);
`cvxpy` 1.9.2 with `clarabel` 0.11.1 and `scs` 3.2.11 (installed by `pip install cvxpy`).
4 cores, 15 GB RAM.

## Result, in one line

The size claim is **confirmed** (and then some — even the *reduced* level-5 SDP at $n=16$ is
small). The relaxation is **useless**: level 2 returns exactly the elementary mean-distance bound
$2n/(3(n-1))$, whose $d$-value tends to $\sqrt6 = 2.449\ldots$ while $d(n)$ grows like
$\sqrt{8n}$. Measured slack against the published exact $d(n)$: **38.8 % to 68.6 %**. See
`problems/circle-packing-equilateral-triangle/attacks/r3-sdpgate/README.md`.
