# 2026-08-21 — second verification pass over the Erdős–Oler campaign

Role: Verifier, round 2. Branch `claude/circle-equklatetal-problem-sa7tx7`.
Write scope: `attacks/eo-verification-2/**`, `experiments/packing-eo-verify-2/**`, this file.

## What I was asked to do

Two jobs. (1) Finish the list the [first pass](../../problems/circle-packing-equilateral-triangle/attacks/eo-verification/README.md)
explicitly did not examine — the `eo-exhaustion` §5 resolution theorem, `eo-boundary-counting`
(especially T1), `oler-slack-analysis`, `eo-literature`. (2) Attack the four round-2 lanes as they
land.

## Headline

Two substantive disagreements, both of the same shape as the ones the first pass found: **a
correct theorem being read one logical step too broadly.**

1. **`eo-exhaustion` §5.** The resolution theorem is right. Its stated "contrapositive" is the
   **converse**. It proves *fine cells suffice* (a termination guarantee, an upper bound on the
   level needed) and is being used as *fine cells are necessary* (a divergence argument, a lower
   bound on cost). Witness: at $k=3$, $d=3.998$, §5's formula demands level 13 ($6.7\times10^7$
   cells); the method closes at **level 1**, with 4 cells — and that closure is the same file's
   §1.2(a)/§3.2 showcase, two sections earlier.
2. **`eo-boundary-counting` §5 (T1).** The theorem is true; the proof as written is not. Its
   family is fixed at $\lambda = 101/100$, so the hull side is $\approx 1.01(k-1)$, not $\to k-1$;
   the $k^2$ coefficient of the resulting bound is $(1-\lambda^2)/2 < 0$. The bound peaks at
   **56.0999… at $k = 76$** and then falls to $-\infty$. A finite bound does not exclude a $\Phi$.
   Repaired with $\lambda_k = 1+1/k^3$, $\varepsilon_k = 1/(2k^3)$ — separation stays exactly $1$,
   $b$ stays $3$, and the bound $\to (3k-3)/2$.

The brief's carried lesson — *when a file notes an exception to its own general claim, chase it* —
paid for finding (1) directly. I went looking for the exception before I looked for an error.

## Method note

I wrote my own $\mathbb{Q}(\sqrt3)$ field, hull, shoelace and incidence code, my own uniform-level
cell exhaustion (max-clique on the "maxsep $\ge 2$" graph, all in lattice coordinates where
squared distances are rational), and my own symbolic ring $\mathbb{Q}[\sqrt3,\pi]/(\sqrt3^2-3)$
for the Groemer substitution. No author's code was read, imported or rerun.

The thing that actually found finding (2) was refusing to accept "$\to k-1$" as prose and writing
the hull side down as a closed form in $k$. The file's own table (which I reproduce exactly) is
right at every $k$ it prints; the error is entirely in the extrapolation, and it is invisible
unless you push past $k = 10$.

## Round 2

- **`eo-epsilon`** reports **explicit $\varepsilon = 0$ in its first line** and labels its
  non-explicit result as non-explicit. All four of its claims check out (Groemer$\equiv$Oler,
  Theorem E, Theorem Q on 93 366 triangles of my choosing, Proposition V). Its
  Groemer$\equiv$Oler reduction is the most consequential thing produced today: applied to the
  hull of the circles, Groemer's Satz **is** Oler's inequality, $\pi$ terms cancelling
  identically — which answers `eo-literature` §3, undercuts the supporting table in the problem
  README's Groemer section, and means the equality case `eo-oler-equality` was hunting may
  already be `cited`.
- **`eo-covering-construct` / `eo-covering-bound`** produced kill-criteria and search output only.
  I built and negative-control-tested an independent covering verifier in advance
  (`covercheck.py`) so that a claimed $\le 26$ partition can be checked the moment it lands. I
  also recorded the structural point that the target sits on (or essentially on) its own floor:
  $N^\ast \ge \sup_{a<6}\max\{n\}$, which Erdős–Oler at $k=7$ says is $\le 26$. If the conjecture
  is false, no 26-partition exists at all.

## The pattern worth naming

Both of my disagreements, and both of the first pass's, are the same failure: **a correct theorem
read one logical step too broadly.** Not one is an arithmetic error — every table in every file
reproduces exactly. The errors are all in the sentence *after* the arithmetic: a converse sold as a
contrapositive, a fixed-parameter family sold as a limit. That is where I would look first in round
three, and it argues for a house rule: when a file states a corollary in prose, write the corollary
down as a formula and test it at a value the author did not print.

Round 2 itself produced no overclaim. All four lanes fixed kill-criteria before computing and fired
them as written; all four headline a negative or partial result in their first line.

## Standing caveat

I am the same model family as every author here. Per `RULES.md` §5 this grants **no status**;
everything examined stays `sketch`. What this pass buys is error-finding, not certification.
