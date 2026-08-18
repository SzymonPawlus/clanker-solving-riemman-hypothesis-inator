# Tau-3 saturation does not force source-sink connectivity

Status: **refuted** by an explicit finite witness, with exact computational verification retained
as `numerical`.

## Definitions

For a nonempty proper vertex set `U`, `delta+(U)` is a **dicut** when it is nonempty and no arc
enters `U`. A **dijoin** meets every dicut, and `tau(D)` is the minimum dicut cardinality. A simple
DAG in a fixed topological order is **tau-saturated** when adding any missing forward arc strictly
raises `tau`. It is **source-sink connected** when every source has a directed path to every sink.

These conventions give the expected tiny sanity checks. A nontrivial directed path has its
prefix dicuts and is source-sink connected. A directed cycle has no dicut. In the near-miss DAG
with arcs `s1->t1, s2->t1, s2->t2`, the shore `{s1}` is a dicut, but source `s1` cannot reach
sink `t2`, so the DAG is not source-sink connected. In particular, a dicut shore must have no
entering arc; merely having a nonempty outgoing boundary is insufficient.

The candidate implication from issue #55 was:

> Every tau-saturated simple DAG with `tau=3` is source-sink connected.

It is false.

## Counterexample

Take vertices `0,...,9` in their displayed topological order. Put in every forward arc internal to
each of

```text
A = (0,2,3,4,8),       B = (1,5,6,7,9),
```

and add the three cross-arcs

```text
1->2,  1->4,  6->8.
```

The full 23-arc list is committed as
[`witness.json`](../../../../experiments/woodalls-tau3-saturation/witness.json).

- `B={1,5,6,7,9}` is an ideal shore, and its outgoing cut is exactly
  `{1->2,1->4,6->8}`. Exact enumeration shows this is the unique minimum dicut, so `tau=3`.
- The sources are `0,1` and the sinks are `8,9`. Vertex `0` reaches only vertices in `A`, hence it
  cannot reach sink `9`; the DAG is not source-sink connected.
- Exactly 22 forward arcs are missing. Adding `0->9` raises `tau` to 5; adding any other missing
  forward arc raises `tau` to 4. Thus the DAG is tau-saturated in this order.

`verify_witness.py` checks all three bullets from the definitions, recomputing every `tau` twice:
direct enumeration of no-entering shores and a separate predecessor-bitset oracle. This is a
finite refutation of the structural implication, not a proof step toward Woodall and not a
counterexample to Woodall itself.

## Why the tempting signature lemma was insufficient

For a missing forward arc `x->y`, an old minimum dicut remains unchanged if one of its minimum
shores contains both endpoints or neither. Therefore saturation forces every minimum shore to
separate the endpoints of every missing arc. This necessary condition was the promising route:
two sources (or two sinks) then have complementary membership signatures across all minimum
shores.

The witness shows that this constraint is consistent. It has one minimum shore, precisely `B`;
every missing arc crosses between `A` and `B`, while all same-side forward pairs are already arcs.
The three cross-arcs make the underlying graph connected and give the sole minimum cut size 3.
There is no contradiction to extract from minimum-cut signatures alone.

## Exact bounded checkpoint

Before constructing the witness, the signature condition and the target implication were checked
against the exact census from PR #52. Rerunning its unchanged command enumerated all 33,867
fixed-order arc subsets through `n=6` (not modulo isomorphism), cross-checked the two `tau` oracles
through `n=5`, and again found 55 tau-saturated instances with `tau>=3`, all source-sink connected.
Thus the census does not refute the local signature condition or the target implication; the first
refutation found here has ten vertices. Both statements are bounded `numerical` observations only.

## Mandatory filters

- **Schrijver filter:** no packing equality is asserted. The refuted implication and its verifier
  use unweighted cardinality `tau` only.
- **Lucchesi-Younger filter:** no min-dijoin/max-dicut duality is used in either direction.
- **Easy-direction filter:** no bound on the number of disjoint dijoins is presented as an
  existence proof. This attack stops at refuting a proposed reduction.

## Outcome

The issue kill criterion fires at the first exact witness. Tau-preserving arc saturation remains a
valid reduction from PR #52, but saturation does **not** funnel the `tau=3` case into the cited
source-sink-connected theorem. Any continuation needs an additional invariant stronger than
minimum-cut-shore signatures; this issue does not broaden into that new attack.
