# Kill-criterion, recorded before any computation

Attack: `eo-subinteger-relaxation` — refine the **integer**-threshold corner-occupancy relaxation of
[`../eo-corner-squeeze/`](../eo-corner-squeeze/) §5 to **sub-integer** thresholds, recompute every
capacity exactly for the finer regions, and see whether the refinement bites.
Author: `claude` (Claude Opus 5), 2026-08-21, worker W4. Repo [`RULES.md`](../../../../RULES.md)
§6.2 requires this in writing before `experiments/packing-eo-subinteger/` exists.

## Normalisation, asserted up front

**Oler normalisation: minimum separation 1, containing equilateral triangle of side $a$.** The
repo's certificates use separation 2 and side $d = 2a$; every certificate coordinate is halved on
load. Corner coordinates $u_A,u_B,u_C \in [0,a]$ with $u_A+u_B+u_C = 2a$ (Viviani), normalised so
$\Delta_V(t) = \{u_V \le t\}$ is the closed corner triangle of side $t$ at $V$. Erdős–Oler at level
$k$: $n = T(k)-1$ points at separation $\ge 1$ force $a \ge k-1$.

## What is being built

A partition of $T_a$ into cells indexed by **sub-integer** thresholds (multiples of $a/M$ with
$M > k-1$, so cells are strictly finer than the integer cells of the predecessor), a capacity
$\mathrm{cap}(R)$ for every corner-coordinate box $R$, and the linear relaxation

$$\textstyle\max \sum_c z_c \quad\text{s.t.}\quad z \ge 0,\ \sum_{c \subseteq R} z_c \le \mathrm{cap}(R)\ \ \forall R .$$

Its optimum is the best upper bound on the number of separation-1 points in $T_a$ that this region
family can produce. Erdős–Oler at level $k$ is decided by the family iff that optimum is
$\le T(k)-2$; Oler's inequality alone gives $\lfloor \mathrm{Oler}(a)\rfloor = T(k)-1$ for
$a \in (a_0(k), k-1)$, so **the target is exactly one point below the incumbent**.

## K1 — primary (the control the brief demands)

> Run the refined relaxation at $k = 4$, $k = 5$ and $k = 6$, where Erdős–Oler is `cited`-true.
> **If the refined LP optimum is still $\ge T(k)-1$ at any of those $k$** — i.e. the refinement
> still cannot exhibit the contradiction in a case where one certainly exists — then the refined
> family is still too weak, the coarseness gap named in `../eo-corner-squeeze/` §7 is (for this
> family) a **red herring**, and I report that and **stop**. I do not proceed to $k = 7$ and
> report a feasible system there as if it meant anything, and I do not re-scope into
> "add one more constraint family until it works".

## K2 — circularity guard (the trap named for this lane)

> **Every capacity must be derived from geometry**, never from the table of known optimal $d(n)$.
> The primary run uses only: (i) exact diameter tests, (ii) exact finite-cover / independent-set
> bounds on a rational grid, (iii) Oler's inequality (`cited`, and *not* a statement about any
> particular $n$) applied to a convex region. **No $d(n)$ value from `../../README.md` enters any
> capacity in the primary run.**
> If the system ever reports infeasible, the first action is to extract the binding constraints —
> the dual certificate, i.e. the explicit fractional cover — and check each capacity in it against
> that list. A binding capacity that traces to $d(T(k)-1) = k-1$, or to any $d(n)$ at all, voids
> the run (this is exactly `FINDINGS.md`, 2026-08-21, "A `cited` input contained the conclusion").

## K3 — correctness control (capacities must be validated, not trusted)

> Before any conclusion: (a) every exact certificate in `problems/**/results/` is loaded, halved,
> re-checked for separation and containment, and its counts tested against **every** computed
> capacity — a configuration exceeding a capacity means the capacity function is wrong;
> (b) the pipeline must **prove** Erdős–Oler at $k = 3$ ($n = 5$ needs $a \ge 2$), which is
> reachable by a two-line subdivision argument. A method that cannot prove $k = 3$ has no power at
> all and nothing downstream means anything.
> (c) Lemma P of `../eo-corner-squeeze/` §3 is `sketch` and is re-verified here independently
> before any use, per `RULES.md` §3.

## K4 — the $a \to (k-1)^-$ guard

> Infeasibility at one convenient $a$ (e.g. $a = k-1-10^{-2}$) is **not** Erdős–Oler at level $k$;
> the conjecture is the statement for *every* $a < k-1$. Capacities are monotone in $a$, so a
> verdict at $a_1$ transfers to all $a \le a_1$ but not upward. Any infeasibility claim must be
> established for $a$ arbitrarily close to $k-1$ — in practice, by a *uniform* argument valid for
> all $a < k-1$, or it is reported as "infeasible at this $a$ only", which decides nothing.

## The trap, named in advance (`RULES.md` §7)

Infeasibility at $k = 7$ would prove an open case. It is a bug or a circularity until the binding
constraints have been extracted one by one and each checked against K2 and K4. Such an outcome is
reported as **suspect**, gets `extraordinary-claim` handling, and is not announced.

## What counts as success short of the goal

Any of: a rigorous statement that sub-integer refinement of this family does not bite (K1 met);
an exactly-certified capacity function that is strictly stronger than $\lfloor\mathrm{Oler}\rfloor$
on named regions, with the strictness quantified; a counting proof of a *proven* case ($k=3$, $k=4$)
that is verifiably non-circular; or a measurement, in the $\varepsilon$-scale of the one missing
point, of how much of it the refinement closes.
