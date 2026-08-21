# Kill-criterion — Erdős–Oler counterexample hunt

Written **before any code was run** (repo `RULES.md` §6.2), author `claude` (Claude Opus 5),
2026-08-21, branch `claude/circle-equklatetal-problem-sa7tx7`.

## What is being attacked

Erdős–Oler at $k \ge 7$, from the **refutation** side. Separation-1 normalisation: $n$ points at
pairwise distance $\ge 1$ in the closed equilateral triangle $T_a$ of side $a$;
$\Delta(k) = k(k+1)/2$. EO($k$) asserts $\Delta(k)-1$ points do not fit in $T_a$ for $a < k-1$.

Search normalisation (the one the optimiser uses): place $n$ points in the **unit** equilateral
triangle maximising the minimum pairwise distance $m$. Then $a_n = 1/m(n)$, so

> **EO($k$) is false iff $m(\Delta(k)-1) > \dfrac{1}{k-1}$ for some $k \ge 7$.**

Targets: $k = 7,8,9,10$, i.e. $n = 27, 35, 44, 54$, against thresholds
$1/6, 1/7, 1/8, 1/9$.

The repo's certificate convention is separation 2 and side $d = 2a$; the factor 2 is the single
likeliest place to fool oneself and every number in this attack is stated in the separation-1
$(a, m)$ normalisation unless it says otherwise.

## Success criterion

A configuration with $m > 1/(k-1)$ at some $n = \Delta(k)-1$, **exactified**: rational (or exact
algebraic) coordinates with all $\binom n2$ squared distances $\ge$ the squared separation and all
three containment inequalities verified in exact arithmetic, by a checker written for this attack
and then by a second checker built from scratch. Until both pass, it is a *candidate*, reported to
the manager for the `RULES.md` §7 procedure — never written up as a result, never announced.

## Kill-criterion (the honest expected outcome)

Stop, and report the negative result quantitatively, when **either**:

- **K1 (budget).** The planned solve budget below is spent with no local optimum exceeding
  $1/(k-1) + 10^{-12}$ at any target $k$. The deliverable is then the measured landscape: best $m$
  per $k$, the distribution of local optima, the runner-up gap, and what was not covered.
- **K2 (structural).** The distribution of local optima at $k = 7$ shows the lattice value $1/6$
  attained by many independent seeds and a clear gap below it, with **no** basin between the
  runner-up and $1/6$ that a further order of magnitude of solves would plausibly cross. That is
  evidence about fragility, not a proof, and will be labelled `numerical`.

Neither kill is a proof of EO. "No counterexample found" is evidence that this search did not find
one, and nothing more (problem `RULES.md` §1).

**Abort-and-verify trigger.** Any local solve returning $m > 1/(k-1) + 10^{-9}$ halts the sweep
immediately; the configuration goes to the exact gate before anything else is run.

## Budget and how it was estimated

Repo `RULES.md` §6 caps unattended compute at one hour. The cost model is one SLSQP solve on
$2n+1$ variables with $\binom n2 + 3n$ dense constraint rows. Measured single-solve cost is taken
from a benchmark run *before* the sweep (recorded in `out/bench.json`); the sweep sizes are then
chosen so that the four target $k$ plus validation fit inside ~45 minutes of wall clock on 4 cores,
leaving margin. If the benchmark contradicts the estimate the sweep sizes are cut, not the budget
raised.

## Validation gate (before any target run)

The pipeline must first reproduce the **proven** cases: $n = \Delta(k)-1$ for $k = 2,\dots,6$
($n = 2, 5, 9, 14, 20$) must return $m = 1/(k-1)$ to $\ge 10$ digits and must **not** exceed it —
those cases are settled in the literature, so an optimiser that "beats" them is broken. A failure
here stops the attack.

## Ownership

This attack writes only `problems/circle-packing-equilateral-triangle/attacks/eo-counterexample-hunt/**`,
`experiments/packing-eo-hunt/**`, and `notebook/claude/2026-08-21-eo-hunt.md`.
