# 2026-08-30 — IET, the PROVE side of the count clash (`polygon-count-closure`)

Worker journal. Lane: prove `|E(P)| <= 2` for simple polygons, or localise the failure.
Deliverable: [`problems/inscribed-equilateral-triangle/attacks/polygon-count-closure/README.md`](../../problems/inscribed-equilateral-triangle/attacks/polygon-count-closure/README.md).
Files I own and touched: that README and this journal. Nothing else. I did not run any git command;
the dispatcher commits.

A concurrent lane, `attacks/three-exceptional-hunt/`, is trying to build a polygon with three
exceptional vertices. **I did not read its files and did not contact it.** That was the design.

## Verdict

**Did not close `|E(P)| <= 2`.** Found a genuine replacement for the metric argument (Theorem A,
branch trapping) and then **refuted my own route with an exact five-vertex integer pentagon**.
Reporting the refutation as the result, per repo `RULES.md` §0.

## What actually happened, in order

1. Read repo `RULES.md` §0/§3/§7, the problem `RULES.md` in full, the problem README (including the
   provenance warning: every `cited` there is provisional, no source text read anywhere in this
   project), and the three attack READMEs the brief named. Also read the placeholder README of my
   own lane and its `KILL-CRITERION.md` — written by an earlier worker, killed mid-task, and **not
   edited by me**.

2. Wrote an independent exact decider from scratch (`Q(√3)`, my own sign algorithm, my own Cramer
   segment solve with an explicit parallel/collinear branch). Ran the K1 gate before anything else:
   four controls matched, then 400 random polygons / 3 078 vertices cross-checked against the
   committed decider with **zero disagreements**, then the four published witnesses (17-gon spiral,
   `C2`, `C3`, tuning fork) reproduced exactly. Only after that did I compute anything new.

3. **The idea that worked.** Both the wedge argument and the criterion are "one circle at a time".
   The escape is not to compare different circles but to *propagate one comparison along a
   continuous family of them*. Concretely: if two branches `p(r), q(r)` of `J` at radius `r` about
   an exceptional `O` merge at one end of their common interval, then `h(r) = |p−q|² − r²` is
   continuous, never zero (a zero *is* an inscribed equilateral triangle at `O`, by the criterion in
   metric form), and tends to `−c² < 0` at the merge. So `h < 0` throughout. One line, no
   regularity, and — the part I care about — **no continuous lift of any argument anywhere**.

   The decision to state the criterion metrically (`|Op| = |Oq| = |pq| > 0`) rather than angularly
   is what made this work twice over: the proof needs no lifts, and the numerical test is a
   *rational* sign test (`|pq|²` versus `r²`), so no `√3` and no angle enters the instrument.

4. Corollaries: the **channel lemma** (below the first pinch radius the two walls are `< 60°` apart
   at every radius) and **leaf trapping** (every component of `{f>r}` containing a single local
   maximum, and every component of `{f<r}` containing a single local minimum, has its endpoints
   `< r` apart). Together they cover every mechanism recorded in this directory: the spiral tip and
   the 17-gon by the channel half, the tuning fork by the leaf half. Neither implies the other —
   measured, not asserted.

5. Built the branch instrument the way the killed worker prescribed: **partition by critical radii,
   never sample**. All critical squared radii are rational and computed completely (vertex distances
   plus interior perpendicular feet); one rational midpoint per interval; square roots held as
   certified rational brackets refined until a sign is *proved*. Not one sign came back undecided.

6. **The falsification.** Measured how much of `good` the new conditions explain: on 440 sharp
   vertices, the 177 exceptional ones violated the conditions **zero** times (the falsifiable half —
   a single violation would mean my proof is wrong), but **171 of 263 good sharp vertices satisfy
   both conditions anyway**. Then the decisive test: can three vertices of one polygon satisfy
   everything I proved? Yes — up to five did, and the smallest example is a **five-vertex integer
   pentagon** `(18,15), (−5,5), (−19,7), (−2,−5), (1,−21)` with three condition-passing vertices and
   `|E| = 1`. Both deciders agree on all five vertices. So the route provably cannot close the count,
   and I stopped, which is what its own kill-criterion K3 instructs.

## The thing I would tell the next worker

The sharpest output is not Theorem A, it is **Proposition J**: the *only* mutual constraint that
three exceptional points impose on one another through the criterion is that they do not form an
equilateral triangle. Everything else in this repository — wedge, interior angle, half-density,
no-sweep, and now branch trapping — is a condition on the **pair** `(J, O)`. A bound on `|E(J)|`
needs a condition on a **triple**, and the criterion supplies exactly one, the weakest imaginable.
The one joint resource left is that `J` is a single simple closed curve through all three points; I
could not turn it into an inequality, and §8 of the README explains why the purely topological form
of it cannot produce a *constant* at all (the space of inscribed triangles degenerates onto the
diagonal exactly at the vertices with edge-angle `≤ 60°` — I computed that family explicitly,
`d² = (4 − s²)/3`, and verified an exact `Q(√3)` instance inside the `30`-`30`-`120` triangle).

## Things I got wrong or nearly got wrong

- **First cross-check run reported thousands of disagreements.** Cause: the committed
  `decide_good` returns a dict, not a bool, so `bool != dict` every time. My code, not the
  mathematics — the seventh checker failure of the session and the same shape as the previous six.
  Suspect your code first, always.
- I spent time developing a **gap-tree with additivity at splits** (`δ_parent = Σ δ_children`,
  requiring continuous lifts of the argument and a lemma that the total turning about `O` equals the
  interior angle). It is true as far as I checked, but it is strictly more machinery than the result
  needs: the merge-endpoint sign argument gives every consequence I actually use with no lift at
  all. I cut it, and the README states only the lift-free version. Recording it here because the
  temptation to keep the elaborate version was real and it would have added three unchecked steps
  for no theorem.
- I briefly believed a compactness argument showed `E(P)` is open, hence empty — which contradicts
  the `30`-`30`-`120` witness. The error was assuming no small inscribed triangles accumulate at a
  sharp vertex. They do; that is Proposition T, and running the candidate argument against the
  §3.1 witness *before* writing it up is what caught it. That is the filter working exactly as the
  problem `RULES.md` says it should.

## Compute

A few minutes of wall clock total; nothing backgrounded, nothing left running. Scripts live in the
session scratch directory and are **not committed** — `experiments/` belongs to another lane and
`RULES.md` §2 forbids me writing there. The README says so plainly and does not claim the §4
"single command" bar; every explicit witness in it is reproducible from the file itself, and §13's
two code blocks were executed as printed.
