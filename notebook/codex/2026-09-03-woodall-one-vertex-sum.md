# Woodall one-vertex-sum attack — 2026-09-03

Issue: #206. Branch: `codex/206-one-vertex-sums`.

## Selection

Switched deliberately from Moser's worm problem to Woodall's conjecture at
the human's request.  Chose a non-computational structural target: closure of
the Woodall property under an arc-disjoint one-vertex sum.  This is stronger
than the disjoint-union bookkeeping already active elsewhere and yields a
block-minimal-counterexample reduction.

## Result

For `D=D1 union D2` with exactly one common vertex and disjoint arc sets:

1. every global dicut is the disjoint union of its factor restrictions, and
   every nonempty restriction is a factor dicut;
2. a factor dicut lifts unchanged by putting the other factor on the same
   global shore as the common vertex;
3. `tau(D)=min(tau(D1),tau(D2))`, with a dicut-free factor treated as
   `infinity`;
4. colourwise unions of factor dijoin packings give `tau(D)` disjoint global
   dijoins.

Iterating over the block--cut tree proves that every counterexample contains
a directed block that is itself a counterexample.  The proof is elementary
and uses no computation or Lucchesi--Younger duality.

## Remaining work

The write-up is a `sketch` until independent cross-examination.  Review should
focus on shore lifting through the common vertex, dicut-free factors, and the
multigraph block induction.  A literature check should determine whether this
closure lemma is already recorded explicitly.
