# Woodall packings are closed under one-vertex sums

**Status:** `sketch`, proposed for independent cross-examination.

This is a non-computational reduction.  It proves that a counterexample to
Woodall's conjecture can be sought block by block: gluing two positive
instances at one vertex cannot create a counterexample.  In particular, every
weakly connected counterexample has a counterexample among the blocks of its
underlying undirected multigraph, and a block-minimal counterexample has no cut
vertex.

## 1. Definitions and conventions

Let `D=(V,A)` be a finite directed multigraph.  Parallel arcs are retained;
loops may be deleted because they cross no vertex cut.  For `U subset V`, let

```text
delta+(U) = {xy in A : x in U, y notin U},
delta-(U) = {xy in A : x notin U, y in U}.
```

A **dicut** is a nonempty set `delta+(U)` with `U` a nonempty proper shore and
`delta-(U)=empty`.  A **dijoin** is an arc set meeting every dicut.  If `D` has
at least one dicut, `tau(D)` is its minimum dicut cardinality.  We say `D` has
the **Woodall property** if it has `tau(D)` pairwise arc-disjoint dijoins.  If
`D` has no dicut, we declare the property vacuous; the empty set is then a
dijoin, and arbitrarily many empty indexed dijoins may be supplied when a
gluing argument asks for them.

A **one-vertex sum** is a union

```text
D = D1 union D2
```

such that the arc sets are disjoint, the vertex sets meet in exactly one
vertex `z`, and every arc of `D` belongs to one factor.  There are no other
cross-arcs, since a cross-arc would belong to neither factor.

Sanity checks:

- a directed path has singleton prefix dicuts and `tau=1`;
- a directed cycle has no dicuts;
- the two-branch source--sink diamond has `tau=2` and its two paths are
  disjoint dijoins;
- gluing two diamonds at one vertex still has `tau=2`; pairing the two path
  dijoins colour by colour gives the packing predicted below.

## 2. Restricting a global dicut

**Lemma 1 (restriction).**  Let `D=D1 union D2` be a one-vertex sum.  If
`C=delta+_D(U)` is a dicut of `D` and `Ui=U intersection V(Di)`, then

```text
C = delta+_D1(U1) disjoint-union delta+_D2(U2).
```

Every nonempty term on the right is a dicut of the corresponding factor.

**Proof.**  Every arc belongs to exactly one factor, so membership in the
global boundary is the same as membership in the appropriate restricted
boundary.  This proves the displayed disjoint union.  Moreover
`delta-_Di(Ui)` is a subset of `delta-_D(U)` and is therefore empty.  If the
outgoing restricted boundary is nonempty, then `Ui` is automatically neither
empty nor all of `V(Di)`.  It is consequently a legal dicut shore in `Di`.
At least one restricted term is nonempty because `C` is nonempty.  QED.

The last sentence is where the convention matters.  An empty restricted
boundary is not called a dicut and contributes no lower bound; the global
boundary nevertheless has a nonempty component somewhere.

## 3. Lifting a factor dicut without changing its arcs

**Lemma 2 (lifting).**  Every dicut of either factor is exactly a dicut of
`D` after a canonical choice of global shore.

**Proof.**  It is enough to treat `D1`.  Let `delta+_D1(S)` be a dicut.

- If `z notin S`, use the global shore `U=S`.
- If `z in S`, use the global shore `U=S union V(D2)`.

In the first case no vertex of `D2` except the excluded common vertex can
touch `S`.  In the second case all of `D2` lies on the same side as `z`.
Thus no arc of `D2` crosses the chosen global shore in either case.  The arcs
of `D1` crossing `U` are exactly those crossing `S`, with the same directions.
Hence

```text
delta+_D(U) = delta+_D1(S),   delta-_D(U) = empty.
```

The shore remains nonempty and proper: in the second case, propriety follows
because `S` was proper in `V(D1)`.  The argument for `D2` is symmetric.  QED.

## 4. The minimum dicut and the packing theorem

For a factor having dicuts, write `tau_i=tau(Di)`; for a dicut-free factor use
the bookkeeping value `tau_i=infinity`.

**Proposition 3.**  If `D` has a dicut, then

```text
tau(D) = min(tau_1,tau_2).
```

**Proof.**  Lemma 2 lifts every factor dicut unchanged, proving
`tau(D)<=tau_i` for each finite `tau_i`.  Conversely, Lemma 1 decomposes every
global dicut into at least one factor dicut.  If only one term is nonempty its
size is at least the relevant `tau_i`; if both are nonempty, each term already
has that property.  In all cases the global size is at least
`min(tau_1,tau_2)`.  QED.

**Theorem 4 (one-vertex-sum closure).**  If `D1` and `D2` have the Woodall
property, then their one-vertex sum `D` has the Woodall property.

**Proof.**  If `D` has no dicut there is nothing to prove.  Otherwise put
`k=tau(D)=min(tau_1,tau_2)` using Proposition 3.  From every factor with
finite `tau_i`, choose `k` members from a packing

```text
J_i^1,...,J_i^tau_i.
```

For a dicut-free factor put `J_i^r=empty` for `1<=r<=k`.  Define

```text
J^r = J_1^r union J_2^r,       1<=r<=k.
```

The sets `J^r` are pairwise arc-disjoint because the factor arc sets are
disjoint and each factor packing is pairwise disjoint.  Let `C` be any global
dicut.  By Lemma 1, some restriction `C_i` is a nonempty dicut of `Di`.
Therefore `J_i^r` meets `C_i` for every `r`, and hence `J^r` meets `C` for
every `r`.  Thus the `J^r` are `k=tau(D)` pairwise disjoint dijoins.  QED.

Unused arcs can be distributed arbitrarily among the `J^r` if a partition of
the full arc set is desired, since a superset of a dijoin is again a dijoin.

## 5. Block reduction

Delete loops and take the ordinary block decomposition of the underlying
undirected multigraph of a weakly connected digraph.  Each nontrivial block
inherits precisely the arcs represented by its undirected edges.  Distinct
blocks are arc-disjoint and meet only at cut vertices.  A leaf block can be
peeled from the block--cut tree as a one-vertex sum.  Repeated application of
Theorem 4 gives the following.

**Corollary 5 (blockwise reduction).**  If every directed block has the
Woodall property, then the whole weakly connected digraph has the Woodall
property.  Consequently, if a weakly connected digraph is a counterexample,
at least one of its directed blocks is itself a counterexample.  In
particular, a counterexample minimal under deletion of whole leaf blocks has
2-vertex-connected underlying undirected multigraph (apart from the standard
two-vertex bridge blocks, which have `tau=1` and are positive).

This extends any known positive class blockwise.  For example, a digraph whose
nontrivial directed blocks are each source--sink connected satisfies Woodall,
even when the whole digraph is not source--sink connected.  The cited
source--sink-connected theorem is applied only inside each block; Theorem 4
then performs the gluing.

## 6. Edge cases and attempted failure modes

1. **The common vertex lies on a dicut shore.**  Lemma 2 includes the entire
   other factor with the shore, so no unwanted arc is created at the glue.
2. **The common vertex lies off the shore.**  The other factor stays entirely
   off the shore, again creating no crossing arc.
3. **A global dicut restricts trivially to one factor.**  Lemma 1 uses only a
   nonempty restriction; the other restriction is deliberately ignored.
4. **A factor has no dicuts.**  It imposes no transversal condition and is
   handled by empty indexed dijoins.  A directed-cycle factor is the basic
   test.
5. **Parallel arcs.**  They are separate members of one factor's arc set, so
   cardinalities and disjointness are unchanged.  No simplicity assumption is
   used.
6. **Loops.**  They occur in no dicut and may be deleted before decomposition
   or assigned arbitrarily afterward.

None of the issue's kill conditions fires: restriction always finds a
nonempty factor dicut, lifting produces exactly the original factor boundary,
and colourwise union meets every global dicut.

## 7. Mandatory filters

- **Schrijver filter: passed with a scope warning.**  This argument is a
  conditional closure theorem, not a proof that every digraph has the Woodall
  property.  It does not infer the false weighted Edmonds--Giles conjecture.
  In fact the same separation proof has a conditional capacitated analogue:
  if both factors already possess the required feasible weighted packings,
  their disjoint capacities can be glued.  Schrijver's counterexample merely
  supplies a nonpositive block and therefore cannot be eliminated by this
  reduction.  The specifically unweighted corollary uses cardinality
  `tau(D)` and pairwise arc-disjoint `{0,1}` incidence sets, exactly the
  unweighted Woodall formulation.
- **Lucchesi--Younger filter: passed.**  No min-dijoin/max-disjoint-dicuts
  duality is invoked, and the roles of dicuts and dijoins are never exchanged.
- **Easy-direction filter: passed.**  The proof explicitly constructs
  `tau(D)` dijoins and verifies that each meets an arbitrary global dicut.  It
  does not merely show that a packing has size at most `tau(D)`.

## 8. Dependency and review boundary

The one-vertex-sum theorem itself is elementary and self-contained.  The
example class in Corollary 5 additionally depends on the cited
source--sink-connected theorem recorded in the problem README.  No census,
solver, or computational evidence is used.

The most useful independent attacks are:

1. reconstruct Lemma 2 in the case where the glue vertex belongs to the
   factor shore;
2. search for a global dicut whose two restrictions are both empty;
3. verify the block--cut-tree induction for multigraph bridge blocks;
4. check whether the statement is already standard in the dijoin literature.

