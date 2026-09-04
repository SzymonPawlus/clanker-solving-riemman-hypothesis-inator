# Woodall tau=3 chain: cross-family review of #249, #253, #255, #238, #242

**Date:** 2026-09-04. **Reviewer:** Claude (Opus 5), @SzymonPawlus.
**Author of all five PRs:** Codex (@Flow-25). Reviewer-only task; no `problems/**` files written.

Continues the review started by an earlier Claude worker on #239, #243, #246, #251, #257
(see PR #258). #251 and #257 have since merged to `main`.

## Verdicts

All five: **changes requested**. No approvals, no merges.

| PR | Content | Math as reconstructed | Blocking defect |
|---|---|---|---|
| #249 | boundary cores | Theorem 2 correct (conditional on core-completeness) | inverted inequality in (3); Lemma 1 proof incomplete; undefined `relevant`/`forced` |
| #253 | adjacent-trace augmentation | **all steps correct**, incl. the previously unreviewed augmentation | Theorem 3's hypothesis not stateable from anything in the repo |
| #255 | comparable chains | **all steps correct**; strongest file of the five | no forward pointer to #257, which refutes its local hypothesis; undefined vocabulary |
| #238 | crossing residual module | abstract criteria correct | bow-tie forcedness asserted as fact, absent from `main`; title overclaims |
| #242 | forest/cactus overlaps | forest half correct | cactus cycle-block transfer unfollowable as written; bow-tie framing |

## The definitional-dependency finding: it holds for all five

Re-ran the grep on current `main` (now including #215, #251, #257, #210):

```
git grep -i "separator sum" origin/main -- problems/woodalls-conjecture/   -> 0
git grep -i "optional trace" ...                                          -> 0
git grep -i "bow-tie" / "bow tie" / "quotient arc" / "residual demand"     -> 0
```

Confirmed. Every `tau=3` corollary in this chain states its hypothesis in vocabulary that
exists only in unmerged Codex sketches (#211, #216, #220, #221, #224, #226, #227, #230,
#231, #234, #235).

**The prior reviewer's characterisation survives: the violation is definitional, not
inferential.** I traced every step in all five files and found no case where an unmerged
sketch is used as a load-bearing *proof step*. Each file's derivations are internally
complete from the definitions it states; what is imported from `sketch` material is the
*meaning* of the hypotheses, not any inference. That matters practically — the repair is a
definitions section, not a re-proof.

One refinement worth recording. The severity is not uniform:

- #249 is best: it glosses "optional" inline ("all their realizable local boundaries are
  nonempty"). Only `relevant` and `forced` are undefined.
- #253 and #255 give no gloss at all.
- **#238 is qualitatively worse than the other four.** It does not merely use undefined
  terms in a hypothesis; it *asserts a mathematical fact* — that `Q1={a,d}, Q2={b,e},
  Q3={c}` are the forced boundary colour classes of the five-arc bow tie — with no proof
  and no citation, and titles the note as a `tau=3` result that stands or falls on it.
  Still definitional rather than inferential (the internal derivation from the stated
  definitions is sound), but a reader is far more likely to be misled.

## What I reconstructed, and how

Not by reading for agreement. Each load-bearing step was re-derived, then attacked numerically.

**#253 Lemma 1 — terminal-preserving augmentation** (the flagged open step). Analytically:
simple augmenting paths never re-enter `alpha`, so flow on each `alpha->x` is
non-decreasing; and arc-disjoint trace-0 covers must use distinct arcs of a *minimum*
trace-0 boundary, so at most `mu_0` exist. Upper and lower bound meet.

Numerically: reimplemented from the statement — brute-force enumeration of all
incoming-closed shores to get `mu_t` and the full families `B_0,B_1`, an independent
parallel-arc max-flow (so guards stay distinguishable from forward unit copies), then the
procedure followed literally and each retained arc set tested for coverage against every
boundary. **532 instances: 0 violations of claim (4). 727 instances: 0 violations of
profile (5)**, including pairwise arc-disjointness.

*Self-inflicted false alarm worth remembering.* My first run reported 320 "violations" of
(4). My bug: I had filtered empty boundaries out of the shore enumeration, which silently
made Codex's "contains no empty boundary" hypothesis vacuous — so my checker was testing a
statement the author never made. Keeping empty boundaries and discarding those instances as
the hypothesis requires took the count to zero. This is the `corrections-overshoot` pattern
from the other direction: **a reviewer's harness bug reads exactly like an author's error**,
and the fluent-and-wrong failure mode of §0 applies to the checker too. Always confirm the
author's hypotheses are non-vacuous in your own reimplementation before reporting a
counterexample.

**Hall step (#249 and #253 share it).** Checked exhaustively rather than trusting the case
list: all 64 profile pairs with `a_it in {1,2,3}` satisfying `a_1t+a_2t>=3` admit a perfect
matching. Also confirmed `tau=3` is load-bearing and not decorative — 17 profile pairs
*violating* that inequality have no matching. That is a real test of the easy-direction
filter, which passes in both files.

**#255 Lemma 1 (polychromatic interval colouring).** Proved the representative invariant
myself (a replaced interval cannot contain a later point, so colour classes containing a
point are exactly the live representatives), then reimplemented the sweep from the prose:
**107,626 random k-fold interval covers, 0 sweep failures, 0 statement failures**.

**#238 criteria.** Brute-forced every actual colouring of `I ⊔ P ⊔ Q` against criterion (3)
and scalar form (4) over all `A,B ⊆ {1,2,3}`, `i,p,q <= 3`: **0 mismatches for both**. The
`tau=3` bare-crossing corollary: **0 failures** over all `i,p,q in {1..4}` satisfying (5).

**#255's `(2,1,2)` example** and **#242's sharpness example**: both verified by hand,
both correct.

## Repo-specific error hunt

The two most frequent errors here (`failed-search-as-proof`, inverted inequalities):

- **Failed search as proof of nonexistence: absent from all five.** #255's `(2,1,2)` and
  #242's three-vertex sharpness example are explicit finite constructions with exhaustive
  arguments, not unsuccessful hunts. #242's "a proof using only `|R_v|>=|C_v|` cannot work"
  is a valid impossibility-of-technique argument in Schrijver-filter style and does not
  need the pattern to be digraph-realisable.
- **Inverted inequalities: one found.** #249's (3) is introduced as "coverage counts are
  **at least**" but its `neither: 3-max(a_i0,a_i1)` row is an upper bound — as the author
  correctly uses two lines later (`e_i <= ...`). Usage right, statement wrong. Every other
  `>=`/`<=` in all five files checked out.
- **Empty-dicut convention:** correct (`delta- = empty`) in all five. #253's guard
  encoding is the nicest instance — a capacity-`M` guard `v->u` is uncrossable by a
  sub-`M` cut *precisely because* `delta-(X)=empty`, so the convention is load-bearing
  rather than decorative.

## Steps I could not follow

1. **#242's cactus cycle-block transfer.** Four sentences of prose; the transfer relation's
   arguments are undefined, the parent articulation vertex (incident to two cycle edges, so
   constrained at both ends of the sweep) is handled by assertion, and "records the exact
   colour subset contributed there" does not say what is recorded. Plausible, but §5 says
   plausible is not a review. This is half the title.
2. **The hypotheses of #249/#253/#255 Theorem 2/3/2, and #238's and #242's bow-tie setup.**
   Not because they are hard, but because they are not written down anywhere reachable.

## #249 after #251 — asked to answer plainly

**#249 still claims something true.** #251 refutes the *removal* of the coreless case (the
directed diamond has a minimum fixed-trace boundary family with empty core, neither laminar
nor a sunflower, so uncrossing cannot justify atomic colouring). It does not touch
Theorem 2, which is explicitly conditional on core-completeness and is correct.

**The abstract does not read as closing the regime**, which I checked specifically. #249
says outright that corelessness "does not refute adequacy; it identifies the precise point
where a flow-exchange or locking theorem, rather than atomic colouring, is needed". That is
honest and is a good §0 record of a bounded method. Asked only for a forward pointer to
#251 so the boundary is visible from the file.

Same shape at #255: correct conditional reduction, and #257 (merged) shows its local
hypothesis is false. #255 cannot have known, but merging it without a pointer to #257 sends
the next reader down a documented dead end, which §6.1 exists to prevent.

## Process note

**None of the five carries a required `tier:` label** (§1). Asked Codex to add one to each.
For contrast, the three currently-open non-Woodall PRs (#259, #261, #262) all carry
`tier:non-claim`, so this is specific to this chain.

## Suggestion for the chain

Six PRs in this chain now have changes requested for substantially the same reason. Rather
than six separate definitions sections, one merged file on `main` defining trace, separator
sum, relevant/optional/forced trace, and the bow-tie reduction with its forced colour
classes would unblock all of them at once — and would be the natural place to *prove* the
bow-tie forcedness that #238 and #242 currently assume. Worth an issue.
