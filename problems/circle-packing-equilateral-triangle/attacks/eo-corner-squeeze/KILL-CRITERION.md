# Kill-criterion, recorded before any computation

Attack: `eo-corner-squeeze` — take the corner-occupancy constraints that Prover A's conditional
Erdős–Oler (`../eo-hull-deficit/` §4, §9, status `sketch`) forces on any $k = 7$ counterexample,
and squeeze them against the global count of 27 until they break or prove something.
Author: `claude` (Claude Opus 5), 2026-08-21. Repo `RULES.md` §6.2 requires this in writing up
front; this file is written before `experiments/packing-eo-corner-squeeze/run.py` exists.

Notation (Oler normalisation: separation 1, side $a$; the repo's certificates use separation 2
and side $2a$). For a corner $V$ let $u_V(p) \in [0,a]$ be the corner coordinate, normalised so
that $\Delta_V(t) = \{u_V \le t\}$ is the closed corner triangle of side $t$ and
$u_A + u_B + u_C = 2a$ (Viviani). $S_j^{(V)} = |\{p \in E : u_V(p) < j\}|$.
$N(t)$ = max number of unit-separated points in a closed equilateral triangle of side $t$;
$N(j^-) = \lim_{t \to j^-} N(t)$.

The object under attack, for $n = T(k)-1$ points in $T$ of side $a < k-1$:

$$\textbf{(CIO-}j\textbf{)}\qquad S_j^{(V)} \;\ge\; T(j)\quad\text{for every corner } V
\text{ and every integer } 1 \le j \le k-2 .$$

## K1 — primary

> If the **corner-occupancy relaxation** — the constraint system consisting of (CIO-$j$) at all
> corners and scales, the region capacities $N(\cdot)$, the Viviani floor constraint, and any
> further capacity bound I can prove for a region defined by corner coordinates — turns out to be
> **feasible at $k = 6$** (where Erdős–Oler is `cited`-true, so the *geometric* system is
> infeasible), then the relaxation provably cannot decide Erdős–Oler, and it cannot decide $k = 7$
> either. Record the explicit feasible witness at $k = 6$, report the refutation, and stop. Do
> **not** re-scope into "strengthen CIO", "prove the equality theorem", or "attack Oler itself".

## K2 — secondary (correctness control)

> If Prover A's Corollary 4 / (CIO-$j$) cannot be independently re-derived here, or if it is
> contradicted by an explicit unit-separated configuration in the repo's certificates, then the
> whole task premise is void: report that and stop. Concretely — every exact certificate with
> $n = T(k)$ at $a = k-1$ must satisfy $S_j^{(V)} = T(j)$ exactly, and every certificate must
> satisfy $S_j^{(V)} \le N(j^-)$.

## K3 — secondary (correctness control)

> If any configuration I build to witness feasibility fails the exact separation check, or if any
> capacity bound I compute is contradicted by an explicit configuration exceeding it, the
> computation is wrong and nothing downstream means anything.

## The trap, named in advance (`RULES.md` §7, problem `RULES.md` §4)

If the relaxation comes out **infeasible at $k = 7$ and also at $k = 4,5,6$**, that is not a proof
of Erdős–Oler; it is a bug until exhaustively verified, and the first place to look is whether a
capacity bound was computed for the wrong region (the pair region $\{u_A \ge j, u_B \ge j\}$ is a
**rhombus**, not a triangle — I have already made that error once in scratch and caught it).
Any such outcome gets `extraordinary-claim` handling and is reported as suspect, not as success.

## What would count as success short of the goal

A rigorous no-go statement for the corner-occupancy route (K1), an independent re-proof of
(CIO-$j$) at some scale by a method that does not depend on a `sketch`, or an explicit description
of the configuration that survives every corner constraint. All three are reportable outcomes.
