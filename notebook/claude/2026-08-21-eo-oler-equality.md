# 2026-08-21 — the equality case of Oler's inequality (Prover D)

Attack: [`problems/circle-packing-equilateral-triangle/attacks/eo-oler-equality/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-oler-equality/).
Code: [`experiments/packing-eo-equality/`](../../experiments/packing-eo-equality/).
Kill-criteria written before any computation:
[`KILL-CRITERION.md`](../../problems/circle-packing-equilateral-triangle/attacks/eo-oler-equality/KILL-CRITERION.md).
Branch `claude/circle-equklatetal-problem-sa7tx7`. No git operations performed (per brief).

## Brief

Four routes died today. What survived was the equality/stability case of Oler's inequality,
in three tiers: (A) full equality characterisation, (B) quantitative stability, (C) equality
when the hull is the whole triangle. Told to take the highest tier I can actually hold.

## What I held: (C), partially. And (A) is not the right target.

Order of the day, as it actually went:

1. **Read first.** `RULES.md`, problem `RULES.md`, `oler-lower-bound` §5.2, `oler-slack-analysis`,
   and — crucially — `eo-boundary-counting` and `eo-hull-deficit`. That last step saved the
   session: two of my first three "results" were already in the repo.
2. **Wrote the kill-criteria.** K1 correctness of the base case, K2 scope of the target, K3 the
   candidate extremal class, K4 duplication.
3. **Computed.** Then wrote up.

## The one thing worth remembering

I nearly spent the session on the wrong target. Within twenty minutes I had a chain that looked
like it closed $k=7$:

- face-excess nonnegativity, restricted to "hull is an equilateral triangle, all three corners
  occupied", plus
- $b\le3\lfloor a\rfloor$ (which follows in that case from three per-side counts),
- gives $n\le\frac{a^2}2+\frac{3\lfloor a\rfloor}2+1<T(k)-\frac32$ for $a<k-1$, i.e. Erdős–Oler
  **for every $k$**.

`RULES.md` §7 is the reason I did not write that up: a chain that proves the whole conjecture in
twenty minutes is a chain with a false step, and the base rate is not close. So I went looking for
the counterexample instead of the write-up, and found it in ten minutes: take the $T(k)$ lattice
and push its three **corner** points outward along the bisectors. Separations only increase, the
hull stays an equilateral triangle, all three corners stay occupied — and $b$ collapses from
$3(k-1)$ to $3$, so the face excess drops to $\approx-\frac{3(k-2)}2$ while the total Oler slack
stays $O(\delta)$. At $k=7$, $\delta=10^{-3}$: face excess $-7.494$, slack $0.0075$.

Then the duplication check: that is `eo-boundary-counting` §4 (**W1**), found this morning by a
different construction. Their construction pushes the *edge* points inward; mine pushes the
*corner* points outward. Same conclusion. Priority theirs, credited, not reclaimed — but two
independent constructions killing the same hypothesis is worth having on the record, because that
hypothesis is the natural first idea and it will be reached for again.

**The general lesson, for me:** the fastest way to check "have I just proved a famous conjecture"
is to look for the counterexample, not to reread the proof. Rereading a fluent argument returns
"it's fine" every time.

## Kill-criteria

- **K1 — not met.** Lemma T ($n=3$ Oler with equality) survived. 155 120 triangles checked with
  exact rational decisions, zero violations, exactly the two predicted equality triples.
  So I proved it. It is the base case the repo did not have.
- **K2 — MET.** This is the finding that matters. An equality theorem, granted in full, excludes
  exactly one side length at $k=7$, namely $a^\*=\frac{-3+\sqrt{217}}2$; the open window
  $[a^\*,6)$ survives. Measured in points — the unit `eo-boundary-counting` §2 rightly insists on
  — the required gain is $1$ and an equality theorem delivers $0^+$. So I dropped from (A) to (C)
  and said so in the first line of the write-up rather than re-scoping to make the target look met.
- **K3 — not met**, but it surfaced an error in the existing statement of the target: (R2) of
  `oler-lower-bound` §5.2 says equality forces $E\subseteq\Lambda$. That is necessary and **not
  sufficient** — a lattice-convex 4-point set with one hull edge of length $\sqrt3$ has slack
  $\frac{\sqrt3-1}2\ne0$. The right class is $E=\Lambda\cap P$ with $P$ tiled by unit equilateral
  lattice triangles.
- **K4** — three of my derivations were already in the repo (O1, W1, and the totals in
  `oler-slack-analysis` §1). All credited in §6 of the write-up.

## What is actually new

- **Lemma T** with its equality classification, proved. Two equality cases: the unit equilateral
  triangle and the degenerate $(2,1,1)$ — and both are unit-lattice configurations, which is the
  first evidence for the shape of the general characterisation coming from inside a proof rather
  than from examples.
- **The $\tau$-identity** $\operatorname{slack}=\sum_f\tau(f)-\sum_{\rm int}(\ell_e-1)$, and the
  equality theorem it yields when a triangulation has all interior edges of length 1 — which is
  also a proof of Oler's inequality for that class not using Oler.
- **The extremal class, exactly** (Pick's theorem), correcting (R2).
- **Theorem T4**: equality with equilateral hull and no interior points forces $a\in\{1,2\}$ and
  the lattice. Complete, four lines, no machinery.
- **The $\varepsilon$-scale**: report progress on this route as the $\varepsilon$ in
  "deficit $\ge\varepsilon$", where $a_\varepsilon=\frac{-3+\sqrt{217+8\varepsilon}}2$ and the
  conjecture is exactly $\varepsilon=1$. The whole repo, this file included, is at $\varepsilon=0$.
- **The answer to the manager's closing question**: lattice-forcing would close $k=7$ with five
  points to spare — a grid search says $\max_\Lambda|\Lambda\cap T(a)|=22$ across the entire open
  window, jumping to $28$ exactly at $a=6$. So the counting half is free; all the difficulty is in
  the forcing, and by K2 the forcing must hold up to deficit $1$, not merely at deficit $0$.

## A structural point I want on the record

Target (B), stated as "the deficit is $\ge1$", is **equivalent** to Erdős–Oler at $k$ — one line of
monotonicity, since Oler's RHS is strictly increasing and equals $T(k)$ exactly at $a=k-1$. It is
not a reduction, it is a restatement. Calling it "the remaining route" makes it sound like a lemma;
it is the conjecture with different words on it. The genuinely intermediate object is the
$\varepsilon$-scale.

And the brief's suggestion that the slack decomposition makes the equality characterisation
concrete — "equality $\iff$ every face excess and every boundary-edge excess vanishes" — does not
follow from the identity: that step needs $\mathrm{FE}\ge0$, which is the refuted hypothesis H.
Worse, the split is discontinuous, so there is no stability version of it either. The
characterisation may still be true; the identity is just not a route to it.

## Manager retraction, handled mid-flight

The manager retracted "every partition refinement of Oler is strictly worse than Oler, so
cell/strip/row schemes are dead", correctly: the identity forbids *Oler-per-piece*, not
*true-capacity-per-piece*. One sentence of my §4 leaned on it; corrected. I then measured the live
version rather than take a position on it: a hexagonal diameter-$<1$ covering of $T(a)$, $a<6$,
needs $34$ pieces and the uniform sub-triangle scheme needs $36$, against a requirement of $26$.
Neither closes $k=7$ — but the isodiametric floor is only $\ge20$, so the route is not excluded,
and the $a=1.999$ row ($6$ hexagons vs $4$ medial triangles) shows why: boundary-adapted pieces
beat isotropic ones badly, which is exactly the freedom the scheme has left.

Three propagated errors from the manager today. Their own instruction — test the constraint rather
than accept it — is the right one and I have started applying it to my own inputs too.

## Least-certain step

Step 3 of Lemma T: that $\min\alpha\beta\gamma$ over the polytope is attained at a vertex, and that
for $S\in(3,4)$ the only vertices are the permutations of $(S-2,S-2,4-S)$. The concavity argument
is routine, the conclusion is checked exactly on a grid, and it is still the one sentence carrying
real weight. Second: the gluing induction in Corollary T2.1.

## Not done

(A), (B), and (C) in the form asked for. Equality with an equilateral hull **and interior points**
is open; the write-up says exactly where it breaks (no upper bound on the interior count, and the
natural local repair is W1-false).
