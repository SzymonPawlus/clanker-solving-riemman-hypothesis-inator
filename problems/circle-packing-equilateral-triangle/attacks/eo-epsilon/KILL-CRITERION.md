# Kill-criteria, recorded before any computation

Attack: `eo-epsilon` — **get the Erdős–Oler deficit at $k=7$ off $\varepsilon = 0$.**
Author: `claude` (Claude Opus 5), 2026-08-21. Written before
`experiments/packing-eo-epsilon/verify.py` exists.

**Normalisation, asserted in code.** Separation $1$; $E$ finite with pairwise distances $\ge 1$;
$n = |E| = 27$; $E \subseteq T(a)$, the closed equilateral triangle of side $a$, with $a < 6$;
$P = \operatorname{conv}(E)$; $A, M$ area and perimeter; $b = |E \cap \partial P|$.

$$\operatorname{slack}(E) = \tfrac2{\sqrt3}A(P) + \tfrac12 M(P) + 1 - n,\qquad
\operatorname{def}(a,n) = \tfrac{a^2+3a+2}{2} - n .$$

"Deficit $\ge \varepsilon$ at $n=27$" $\iff$ $d(27) \ge a_\varepsilon = \frac{-3+\sqrt{217+8\varepsilon}}2$;
$\varepsilon = 1$ *is* Erdős–Oler at $k=7$ (`eo-oler-equality` §5, S2). The repo's certificates use
separation $2$ and side $d = 2a$; nothing here reads them, and the conversion is asserted in code.

The brief's programme: **(1)** quantify Lemma T; **(2)** force some face far from both equality
shapes; **(3)** control the interior-edge correction $-\sum_{e\ \mathrm{int}}(\ell_e-1)$.

## K1 — correctness of the imported base (`RULES.md` §3: Lemma T and T2 are `sketch`)

> Lemma T and identity T2 are **not** assumable. I re-derive both. If an exactly-checked triangle
> with all sides $\ge 1$ violates $\frac2{\sqrt3}A + \frac p2 \ge 2$, or a third equality triple
> exists, or the Euler counts behind T2 fail on any exactly-checked configuration, the base is
> broken: I report the refutation and stop. If I cannot verify Lemma T's Step 3 (the vertex
> minimisation, flagged by its author as load-bearing) I say so and mark everything downstream
> conditional.

## K2 — correctness of my own quantitative bound

> If any exactly-checked triangle with sides $\ge 1$ violates my quantitative lower bound on
> $\tau$, the bound is wrong. I fix it once; if the second version also breaks, I abandon the
> bound rather than patch it a third time. Adversarial scans must include: near-$(1,1,1)$,
> near-$(2,1,1)$, exactly degenerate, thin slivers with a long side, and very large $S$.

## K3 — the decisive scope test (this is the one I expect to fire)

> **If a lower bound $\tau(f) \ge \Psi(f)$ depending only on the face's own shape can be shown to
> yield, through T2, an inequality no stronger than the target itself, then step (1) of the
> programme is *vacuous* and cannot produce $\varepsilon > 0$ however sharp $\Psi$ is.** In that
> case I must say so in the first line, report the explicit $\varepsilon$ I actually proved
> (possibly $0$), and **not** re-scope "quantitative Lemma T" into a claim of progress.
> Specifically forbidden: presenting a sharp $\Psi$ as an advance when the $\varepsilon$ it
> delivers is $0$.

## K4 — non-explicit is not explicit

> If a route delivers $\varepsilon > 0$ without an explicit value (e.g. via compactness plus an
> equality characterisation), I report it as **non-explicit** in the first line and give the
> explicit $\varepsilon$ separately as $0$. Reporting an unquantified $\varepsilon>0$ as "the
> $\varepsilon$ I proved" is the failure this criterion exists to prevent. The brief already
> classifies equality theorems as delivering $0^+$; if that is all I get, that is what I say.

## K5 — dependency honesty

> Any step resting on a `sketch` (mine or another agent's) makes the conclusion conditional and
> must be labelled so. Any step resting on a source whose body this repo has not read is `cited`
> only to the extent the read part supports it, and the gap is named.

## K6 — duplication (`RULES.md` §6.1)

> Already in the repo and not to be reclaimed: the window $[a^*,6)$ (`eo-boundary-counting` §2),
> the refutation of face-excess nonnegativity (`oler-slack-analysis` §4, `eo-boundary-counting`
> §4), the Barrier Theorem for convex cuts (`eo-hull-deficit` §6), the $\varepsilon$-scale
> (`eo-oler-equality` §5), Lemma T / T2 / T3 / T4 (`eo-oler-equality` §§1–4). If my line reduces
> to one of these, that is a dead end, not a result.

## What counts as success short of the goal

An explicit $\varepsilon > 0$ is the goal. Short of it: a **proved** no-go that tells the next
worker which of steps (1)–(3) cannot carry the argument, a reusable quantitative lemma, or a
correction to a dependency the repo currently mis-states. A hand-wave at $\varepsilon$ is not.
