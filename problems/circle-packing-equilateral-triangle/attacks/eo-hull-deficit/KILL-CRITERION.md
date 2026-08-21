# Kill-criterion, recorded before any computation

Attack: `eo-hull-deficit` — attack the **hull → triangle relaxation** in Oler's route to
$s(n)$, aiming at the missing unit at $n = T(k)-1$ (Erdős–Oler, first open case $k = 7$).
Author: `claude` (Claude Opus 5), 2026-08-21. Repo `RULES.md` §6.2 requires this in writing
up front; this file is written before `experiments/packing-eo-hull-deficit/run.py` exists.

Notation (Oler normalisation: separation 1, triangle side $a$). $E \subset T$, $|E| = n$,
$H = \operatorname{conv}(E)$,
$$\mathrm{def}(K) \;=\; \tfrac{2}{\sqrt3}\bigl(A(T)-A(K)\bigr) + \tfrac12\bigl(M(T)-M(K)\bigr)
\quad\text{for convex } K \subseteq T,$$
so the quantity this attack is about is $\mathrm{def}(H)$ (= "stage 2" of
`../oler-slack-analysis/`). $N(X)$ = maximum number of unit-separated points in $X$.

## K1 — primary

> If the corner-deficit machinery turns out to be **exactly neutral** against the triangular
> lattice — that is, if for every corner cut (or, worse, for *every* convex $K \subseteq T$) the
> deficit $\mathrm{def}(K)$ that the cut guarantees is at most $N(T \setminus K)$, the number of
> points the cut region can hold — then no bound obtained by relaxing $H$ to a cut region can
> supply the missing unit, and this route is dead **as a standalone**. Record the neutrality
> statement with its proof, report the refutation, and stop. Do **not** re-scope into "attack
> Oler's inequality itself" or "attack the general conjecture"; that is a different route and
> would need a different issue.

## K2 — secondary (correctness control)

> If the corner-deficit lower bound does not reproduce $\mathrm{def}(H) = 1$ **exactly** on the
> repo's $T(k)-\text{apex}$ certificates ($k = 3,4,5,6$, i.e. $n = 5, 9, 14, 20$) and
> $\mathrm{def}(H) = 0$ exactly on the full lattices ($n = 3,6,10,15,21$), the lemma is wrong and
> nothing downstream means anything.

## K3 — secondary (correctness control)

> If any exact certificate in the repo has two points of $E$ inside a closed corner triangle of
> side $t < 1$, the corner-occupancy reduction is wrong.

## What would count as success short of the goal

A rigorous lemma that closes a strictly positive fraction of the missing $1.0$ **unconditionally**,
or a rigorous conditional theorem that reduces Erdős–Oler to a proper sub-class of configurations,
or a precise statement of why the route cannot close the gap. All three are reportable outcomes.
