# Kill-criteria — lower bounds on the covering number $N^*(a)$

Written **before any computation**, per repo `RULES.md` §6.2. Author: `claude` (W2, Refuter),
2026-08-21, branch `claude/circle-equklatetal-problem-sa7tx7`.

## Normalisation (asserted in code, not in prose)

Separation **1**. $T_a$ = closed equilateral triangle of side $a$, corners
$(0,0),(a,0),(a/2,a\sqrt3/2)$. A *piece* is a set of diameter $<1$ (strict). $N^*(a)$ = least
number of pieces whose union contains $T_a$. Points at distance $\ge 1$ cannot share a piece.
The repo's `results/` certificates use separation 2 and side $d=2a$; **nothing here reads them**,
so there is no conversion anywhere.

## The target

Partner worker W1 is trying to build a covering of $T_a$, $a<6$, with $N\le 26$ pieces; that would
prove Erdős–Oler at $k=7$ ($n=27$, $a<6$), since 27 pairwise-separated points cannot be
distributed among 26 pieces. I attack the other side.

- **Route dead** iff I prove $N^*(a)\ge 27$ for every $a<6$ (equivalently, by monotonicity of
  $N^*$, for $a$ in a left-neighbourhood of 6 — and I must state which).
- **Route alive** otherwise; then the deliverable is the best proved floor $F$ and the exact
  gap $26-F+1$.

Current state of the art in this repo: floor $\ge 20$ (isodiametric), best construction 34.

## Kill-criteria (what makes me stop)

> **K1 (primary, method-level).** If the best floor I can *prove* — over the four listed methods —
> is $\le 26$, I stop and report the floor and the gap. I do **not** re-scope into constructing
> coverings (that is W1's lane) or into attacking Erdős–Oler directly.

> **K2 (separated points).** The separated-point bound $N^*(a)\ge m$ is capped at $m\le 26$ for
> $a<6$ *if Erdős–Oler is true*. So if my best separated set reaches 26, that method is
> **exhausted, not promising**, and I stop pushing it. Reaching 27 would refute Erdős–Oler and is
> therefore, by `RULES.md` §7, a bug in my own work until proved twice; I treat it as an error.

> **K3 ($\chi$-vs-$\omega$ gap, the only method that can reach 27).** For a separated set $P$,
> $|P|=m$, with free region $Z=\{z\in T_a: |z-p|\ge1\ \forall p\in P\}$, the bound is
> $N^*(a)\ge m+\chi(G_Z)$ where $G_Z$ is the distance-$\ge1$ graph on any finite subset of $Z$.
> $m+\alpha(G_Z)\le 26$ is forced by Erdős–Oler, so this method needs a strict chromatic/clique
> gap. **If, over every configuration and every deletion pattern I search, $G_Z$ is always
> $\alpha$-colourable (no gap), I declare the method unproductive here and stop.** Concretely: if
> every $G_Z$ I build is bipartite whenever $\alpha(G_Z)=2$, there is no gap and K3 is met.

> **K4 (LP/area).** If the area–perimeter relaxation, solved exactly, tops out below 27 (which I
> expect: the fractional relaxation of covering-by-diameter-1-sets in the plane has value exactly
> $\text{area}/(\pi/4)$, so the only gains available are boundary/corner terms), I record the
> number and stop optimising it. It cannot reach 27 by itself — recorded here in advance so that a
> later "one more weight function" is visibly a violation of this criterion.

## Circularity guard (the specific trap in this lane)

Two ways this lane can go circular, both flagged in advance:

1. **Using a published/`cited` $a_n$ (or $s(n)$, or $d(n)$) as an input.** The bound
   $N^*(a)\ge\max\{n:a_n\le a\}$ is worthless if the $a_n$ used *is* the statement being derived.
   **Rule adopted: every separated set I use is one I exhibit explicitly and verify with exact
   rational arithmetic. No literature value of $a_n$, $s(n)$ or $d(n)$ is an input to any bound
   in this attack.** Constructions are self-certifying; that is the whole reason to use them.
2. **Assuming Erdős–Oler while bounding $\alpha(G_Z)$.** Erdős–Oler is used *only* as a sanity
   expectation (K2, K3) — never as a step. Any bound that needs $\alpha \le c$ as a hypothesis is
   not a bound.

Exact arithmetic decides everything: rational coordinates, integer/rational comparisons; $\pi$ and
$\arcsin$ enter only through **certified rational enclosures** with the direction of rounding
chosen against me.
