# Kill-criteria — constructing a small-diameter covering of $T_a$, $a<6$

Written **before any computation**, per repo `RULES.md` §6.2. Author: `claude` (W1, Constructor),
2026-08-21, branch `claude/circle-equklatetal-problem-sa7tx7`.

## Normalisation (asserted in code, never only in prose)

Separation **1**. $T_a$ = closed equilateral triangle of side $a$, corners $(0,0)$, $(a,0)$,
$(a/2, a\sqrt3/2)$. A *piece* is a set of diameter $<1$. The repo's `results/` certificates use
separation 2 and side $d=2a$; **nothing here reads or writes them**, so no conversion occurs
anywhere in this attack.

**Scale-free restatement used throughout.** If $T_6$ (side exactly 6) can be partitioned into $N$
sets of diameter $\le 1$, then for every $a<6$ the scaled copy partitions $T_a$ into $N$ sets of
diameter $a/6 < 1$. So the target is:

> **Partition $T_6$ into 26 sets of diameter $\le 1$.**

That would give Erdős–Oler at $k=7$: 27 points of $T_a$ ($a<6$) at pairwise distance $\ge 1$ cannot
be distributed among 26 sets of diameter $<1$.

## Target and current state

| | value |
|---|---|
| needed | $N \le 26$ |
| uniform sub-triangles ($m=6$) | 36 |
| hexagon tiling (`eo-oler-equality` §8) | 34 |
| isodiametric area floor | $\ge 20$ |
| separated-point floor (`eo-small-cases` §3.3) | $\ge \max\{n : a_n < 6\}$, expected 26 |

## Kill-criteria (what makes me stop)

> **K1 (primary).** If my best verified scheme is $\ge 30$ pieces and I can state the structural
> reason for the shortfall, I record it and stop. I do not re-scope into lower bounds (that is
> W2's lane) or into attacking Erdős–Oler by another route.

> **K2 (density accounting).** The best known plane partition into diameter-1 sets is the regular
> hexagon tiling, $0.6495$ area per piece. If the *measured* interior density of my best scheme is
> already at that ceiling and the remaining gap to 26 exceeds the total boundary waste I can
> possibly remove, stop: the deficit is then structural, not effort-limited.

> **K3 (budget).** One hour of unattended compute (`RULES.md` §6.6). Checkpoint every run.

## §7 guard

A 26-piece partition of $T_6$ would settle an open case of a 1960s conjecture. Prior: I have a
piece of diameter slightly over 1, or a sliver the union misses. Therefore **every reported
scheme is verified by exact rational arithmetic** — all coordinates in the triangular-lattice
basis $e_1=(1,0)$, $e_2=(1/2,\sqrt3/2)$, where $|ue_1+ve_2|^2 = u^2+uv+v^2 \in \mathbb{Q}$ — with
three independent checks: (i) every piece's squared diameter $\le 1$; (ii) pieces have pairwise
disjoint interiors; (iii) the sum of piece areas equals the area of $T_6$ **exactly**. (iii) plus
(ii) plus closedness is what rules out a missed sliver: finitely many closed sets whose union has
full measure in $T_6$ leave a relatively open null set, i.e. nothing. Floats guide the search and
decide nothing.

Anything at $N \le 26$ is reported to the manager as a **candidate**, not a result.
