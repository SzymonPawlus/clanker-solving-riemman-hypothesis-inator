# Mixed separator gluing via trace matching

**Issue:** #217. **Status:** `sketch`, targeting `verified:review`.

This gives the finite compatibility object missing from the serial and
parallel modes of PR #216.  It is self-contained and does not assume that
unreviewed result.  For prescribed local arc-disjoint slots, the criterion
below is necessary and sufficient: gluing is possible exactly when an
explicit bipartite trace-compatibility graph has a perfect matching.

## Definitions and checks

For a finite digraph `D=(V,A)` and nonempty proper `U subset V`, the nonempty
set `delta+(U)` is a **dicut** when `delta-(U)` is empty.  A **dijoin** meets
every dicut.  The minimum dicut cardinality is `tau(D)`.

A directed path has singleton prefix dicuts.  A directed cycle has no
dicuts.  In `s1->t1, s2->t1, s2->t2`, the singleton sources give dicuts even
though source `s1` cannot reach sink `t2`.  In everything below a shore must
have no entering arc; a merely nonempty outgoing boundary is not enough.

Let

```text
D = D1 union D2,
A(D1) intersection A(D2) = empty,
V(D1) intersection V(D2) = S,
```

and assume every arc of `D` belongs to one piece.  Thus there are no arcs
between `V(D1)-S` and `V(D2)-S`.  The finite set `S` is the separator.

If `U` is incoming-closed in `D`, then `U_i=U intersection V(D_i)` is
incoming-closed in `D_i`, both restrictions have the same trace
`T=U intersection S`, and

```text
delta+_D(U) = delta+_D1(U_1) disjoint-union delta+_D2(U_2).       (1)
```

Conversely, incoming-closed local shores with the same trace unite to an
incoming-closed global shore, and (1) holds.  Both statements follow by
checking each arc in its unique piece.  Local boundaries in (1) may be empty,
although the global dicut is required to be nonempty.

## Trace families

For `i in {1,2}` and `T subseteq S`, let `B_i(T)` be the family of boundaries

```text
delta+_Di(W),
```

where `W` ranges over all incoming-closed local shores with `W intersection
S=T`.  Empty boundaries are retained in this family.  Write `z_i(T)=1` when
the empty boundary belongs to `B_i(T)`.

For an arc set `X subseteq A(D_i)`, say that **X covers trace T in piece i**
when `X` meets every nonempty member of `B_i(T)`.  This is a local
trace-dijoin condition, weaker than being a dijoin when only selected traces
are required.

All of this data is finite: at most `2^|S|` traces occur.  The theorem is
structural, not computational; finiteness only explains why the compatibility
object is genuinely a separator state.

## The one-colour trace lemma

**Lemma 1.**  For local arc sets `X_1 subseteq A(D1)` and
`X_2 subseteq A(D2)`, their union is a global dijoin if and only if, for every
trace `T`, the following conditions hold:

1. if `z_2(T)=1`, then `X_1` covers `T` in piece 1;
2. if `z_1(T)=1`, then `X_2` covers `T` in piece 2;
3. if `z_1(T)=z_2(T)=0`, then at least one of `X_1,X_2` covers `T` in its
   respective piece.

**Proof.**  Suppose `z_2(T)=1`.  Pairing the empty boundary in piece 2 with
any nonempty member of `B_1(T)` produces, by (1), a global dicut.  Therefore
`X_1` must meet every such member.  This proves necessity of condition 1;
condition 2 is symmetric.  If neither family contains the empty boundary and
both local sets fail to cover `T`, choose a missed boundary in each family.
Their union is a missed nonempty global dicut, proving necessity of condition
3.

Conversely, take any global dicut and its two boundaries in (1).  If one is
empty, the corresponding forced condition makes the set in the other piece
hit its nonempty boundary.  If both are nonempty and neither family admits an
empty boundary, condition 3 supplies a hit.  If both are nonempty but some
family also admits an empty boundary, condition 1 or 2 forces the opposite
piece to hit all of its nonempty boundaries.  In every case `X_1 union X_2`
meets the global dicut.  QED

The last case is why merely labeling a trace “active on both sides” loses
information: the *existence of an alternative empty realization* forces the
other side to cover the whole trace family.

## Exact compatibility graph

Fix a positive integer `k`.  In each piece suppose we have `k` pairwise
arc-disjoint local slots

```text
X_i^1,...,X_i^k subseteq A(D_i).
```

Empty slots are allowed.  Construct a balanced bipartite graph `Gamma` with
left vertices `1,...,k` (piece 1 slots) and right vertices `1,...,k` (piece 2
slots).  Join left slot `a` to right slot `b` exactly when the pair
`(X_1^a,X_2^b)` satisfies all three conditions of Lemma 1 for every trace.

**Theorem 2 (trace-matching gluing).**  A bijection `pi` makes all `k` unions

```text
J^a = X_1^a union X_2^pi(a)                              (2)
```

global dijoins if and only if `{a--pi(a):1<=a<=k}` is a perfect matching of
`Gamma`.  Whenever it exists, the `J^a` are pairwise arc-disjoint.

**Proof.**  Lemma 1 says exactly that one union in (2) is a dijoin exactly
when its slot pair is an edge of `Gamma`.  Hence all unions are dijoins
exactly when all chosen pairs are edges, which is precisely a perfect
matching.  Distinct unions use distinct slots in each piece; local slots are
arc-disjoint and the two pieces have disjoint arc sets, so the unions are
pairwise arc-disjoint.  QED

By Hall's theorem, this construction succeeds exactly when

```text
|N(R)| >= |R| for every set R of piece-1 slots.           (3)
```

Thus a Hall-deficient slot set is a sharp impossibility certificate for the
prescribed local packings and pairing construction.  This is deliberately
not claimed to rule out different local slots or a global packing that does
not decompose into the prescribed slots.

If additionally `tau(D)=k`, Theorem 2 explicitly supplies the nontrivial
existence direction of Woodall's conjecture.  A minimum dicut only proves the
separate easy fact that more than `k` disjoint dijoins are impossible.

## Strong sufficient conditions

The exact matching test yields several usable proof conditions.

**Corollary 3 (trace ownership).**  Give every trace with
`z_1(T)=z_2(T)=0` to either piece.  Force trace `T` onto piece 1 whenever
`z_2(T)=1`, and onto piece 2 whenever `z_1(T)=1`; a trace may consequently be
forced onto both pieces.  If piece `i` has `k` pairwise arc-disjoint slots
each covering every trace assigned or forced to piece `i`, then every slot
pair is compatible.  Any bijection therefore gives `k` global disjoint
dijoins.

This is a finite-state sufficient condition for a broad mixed regime.  Some
traces may be handled only by piece 1, some only by piece 2, and the remainder
may be allocated to whichever local packing can support them.  Neither the
serial requirement that both pieces supply full dijoins nor the parallel
requirement that each local dijoin is globally sufficient is imposed.

**Corollary 4 (robust matching).**  If every vertex of `Gamma` has degree at
least `ceil(k/2)`, then `Gamma` has a perfect matching and Theorem 2 applies.

To prove this directly from Hall, let `R` be a left slot set.  If
`|R|<=k/2`, any member has at least `ceil(k/2)>=|R|` neighbors.  If
`|R|>k/2` and `|N(R)|<|R|`, then every right vertex outside `N(R)` has all
neighbors among the `k-|R|<k/2` left vertices outside `R`, contradicting its
minimum degree.  Thus (3) holds.

For `k=3`, degree at least two on every slot is sufficient.  More sharply,
failure is witnessed exactly by an isolated slot or by two slots on one side
whose combined neighborhood has size at most one (together with the symmetric
Hall obstruction, which is equivalent in a balanced graph).  This makes the
remaining `tau=3` compatibility check completely explicit.

## Recovery of the two extreme modes

The framework contains the familiar constructions without treating them as
the only possibilities.

- In a serial/minimum situation, take `k` local dijoins in each piece.  A
  local dijoin covers every trace family with nonempty members, so all slot
  pairs are compatible and equal-colour union works.
- In a parallel/additive situation with `k=k_1+k_2`, use the `k_1` local
  dijoins of piece 1 followed by `k_2` empty slots; use complementary empty
  and dijoin slots in piece 2.  When neither side admits an empty boundary at
  any relevant trace, the appropriate nonempty slot covers every trace, and
  a matching pairs each dijoin with an empty slot on the other side.
- In the genuinely mixed case, compatibility edges can use different sides
  for different traces.  Theorem 2 and Hall's condition are the missing
  middle state.

## Mandatory filters

1. **Schrijver filter: passed.**  The Woodall corollary assumes `k` disjoint
   slots of actual unit-capacity arcs and concludes an unweighted packing.
   Minimum weighted dicut value `k` does not produce these local slots: arcs
   of weight zero still determine trace families but cannot occur in packed
   dijoins.  The trace lemma itself remains a valid conditional hitting-set
   fact, but no weighted Edmonds--Giles packing equality is inferred from it.
   Unit-capacity disjointness of the supplied slots is the unweighted input.
2. **Lucchesi--Younger filter: passed.**  No min-dijoin/max-dicut role swap is
   used.  Lemma 1 checks an arbitrary global dicut directly, and Hall's
   theorem is applied only to the finite graph of already supplied slots.
3. **Easy-direction filter: passed.**  A perfect matching constructs the `k`
   global dijoins in (2).  The minimum dicut upper bound is explicitly kept
   separate.

## Scope and review targets

This is an exact gluing theorem for prescribed local slots, not a proof that
suitable slots always exist.  Its advance is to isolate all separator
interaction in a finite trace object and give both an exact Hall obstruction
and checkable sufficient conditions.  Recursive use is possible: a composed
piece can export its own trace profiles at the next separator, but proving a
bounded-state algorithm requires additional bookkeeping and is not claimed.

The proof is noncomputational and depends only on the elementary restriction
identity (1), Lemma 1, and Hall's marriage theorem.  Hall's theorem is used in
its standard finite bipartite form.  The highest-risk points for independent
review are empty-boundary traces in Lemma 1, the necessity direction when
both sides fail a trace, and the `k=3` characterization of Hall failure.
