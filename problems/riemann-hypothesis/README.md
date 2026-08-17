# The Riemann Hypothesis

**Status:** open since 1859. Nothing in this directory changes that.

Shared conventions for problem directories are in [`../README.md`](../README.md); the claim
status taxonomy is in [`../../RULES.md`](../../RULES.md) §3.

## Statement

For $\operatorname{Re}(s) > 1$ define

$$\zeta(s) = \sum_{n=1}^{\infty} n^{-s},$$

and extend $\zeta$ by analytic continuation to $\mathbb{C} \setminus \{1\}$ (simple pole at
$s = 1$, residue $1$). The continuation satisfies the functional equation

$$\pi^{-s/2}\,\Gamma(s/2)\,\zeta(s) \;=\; \pi^{-(1-s)/2}\,\Gamma\!\left(\tfrac{1-s}{2}\right)\zeta(1-s).$$

The functional equation forces *trivial* zeros at $s = -2, -4, -6, \dots$ All other zeros lie in
the **critical strip** $0 \le \operatorname{Re}(s) \le 1$.

> **Riemann Hypothesis.** Every non-trivial zero of $\zeta$ satisfies $\operatorname{Re}(s) = \tfrac{1}{2}$.

## Why this problem

RH is a good stress test for the workflow precisely because it is saturated with
plausible-looking dead ends. An agent that fools itself here gets caught by the verifier rather
than by a reviewer's patience — and the failure is instructive either way.

It is also, obviously, a joke. Both things are true.

## Landscape

Load-bearing results an agent may assume, with attribution. Do not add to this table without a
citation.

| Result | Source |
|---|---|
| $\zeta(s) \ne 0$ on $\operatorname{Re}(s) = 1$; equivalent to the Prime Number Theorem | Hadamard; de la Vallée Poussin (1896) |
| Classical zero-free region $\sigma > 1 - c/\log\lvert t\rvert$ | de la Vallée Poussin |
| Infinitely many zeros lie on the critical line | Hardy (1914) |
| A positive proportion of zeros lie on the line (>1/3, later >2/5) | Levinson (1974); Conrey (1989) |
| First $\sim 10^{13}$ zeros verified on the line numerically | Gourdon (2004) |
| RH for function fields / the Weil conjectures — the analogue **is** a theorem | Weil; Deligne (1974) |

Known equivalent reformulations, worth reading before inventing a new one: Robin's criterion,
Lagarias' criterion, the Nyman–Beurling criterion, Li's criterion, and Weil's explicit-formula
positivity criterion.

De Branges' operator-theoretic programme is the most-cited failed approach; it belongs in
`attacks/` marked `refuted` if anyone proposes it.

<!-- The proportions and the 10^13 figure above are from memory and are not yet pinned to a
     citation. Treat as unverified until someone checks them. -->

## Lean

Mathlib states RH (`RiemannHypothesis`) and carries a substantial analytic number theory
library, so classical lemmas here are plausible formalisation targets. Confirm the exact
Mathlib declaration names before depending on them — do not guess API from memory.
