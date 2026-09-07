# Automatic local trace adequacy by terminal clamping

**Issue:** #229. **Status:** `sketch`, targeting `verified:review`.

This proves the missing local adequacy property from PR #227 for a meaningful
class.  A fixed separator trace is converted into the complete dicut family
of an auxiliary digraph.  When its two clamped terminal sets become the
unique initial and terminal strong components, the cited
source--sink-connected theorem supplies as many disjoint trace covers as the
minimum local trace boundary has arcs.

No computation is used.

## Definitions and checks

For a finite digraph `D=(V,A)`, a **dicut** is a nonempty outgoing boundary
`delta+(U)` such that no arc enters `U`.  A **dijoin** meets every dicut.

Fix a separator vertex set `S` and a proper nonempty trace `T subset S`.
Let `B_D(T)` be the family of all nonempty boundaries `delta+(U)` where `U`
is incoming-closed in `D` and `U intersection S=T`.  Define

```text
mu_D(T) = min{|B| : B in B_D(T)}.
```

The family is assumed nonempty.  A **T-cover** is an arc set meeting every
member of `B_D(T)`.  Local adequacy at three colours asks for
`min(3,mu_D(T))` pairwise arc-disjoint `T`-covers.

These are genuine dicut boundaries, not arbitrary directed cuts.  On a
directed path, incoming-closed shores are prefixes.  A directed cycle has no
dicut.  The DAG `s1->t1, s2->t1, s2->t2` has singleton-source dicuts although
`s1` cannot reach `t2`.  The condition `delta-(U)=empty` is used throughout.

## The clamped auxiliary digraph

Form `D[T]` from `D` by adding artificial arcs as follows:

- choose one vertex of `T` and add both directions between it and every other
  vertex of `T`;
- choose one vertex of `S-T` and add both directions between it and every
  other vertex of `S-T`.

Parallel copies cause no problem.  The first clamp makes all vertices of `T`
belong to one strong component `C_T`; the second makes all vertices of `S-T`
belong to one strong component `C_barT`.  Original arcs are distinguished
from artificial clamp arcs.

Call `(D,S,T)` **terminal-clampable** when `C_T` and `C_barT` are distinct,
and in the condensation of `D[T]`:

```text
C_T is the unique source, and C_barT is the unique sink.             (TC)
```

This condition is structural and checkable without solving a packing
problem.  Equivalently, every strong component of `D[T]` is reachable from
`C_T` and can reach `C_barT`.

## Exact dicut-family lemma

**Lemma 1.**  If `(D,S,T)` is terminal-clampable, the nonempty dicuts of
`D[T]`, after ignoring artificial arcs, are exactly `B_D(T)`.  No artificial
arc belongs to a dicut, and

```text
tau(D[T]) = mu_D(T).                                      (1)
```

**Proof.**  A dicut shore is a union of strong components: if it split one,
a directed path from an outside vertex to an inside vertex would contain a
first entering arc.  In a finite condensation DAG with a unique source,
every nonempty incoming-closed set contains that source (follow predecessors
from any member).  With a unique sink, every proper incoming-closed set
excludes that sink (every vertex reaches the unique sink, so predecessor
closure of a set containing it is the whole DAG).

Hence every nonempty proper incoming-closed shore of `D[T]` contains `C_T`
and excludes `C_barT`.  Its intersection with `S` is exactly `T`.  Conversely,
an incoming-closed shore of `D` with trace `T` remains incoming-closed after
the clamps: every added arc has both endpoints in `T` or both endpoints in
`S-T`, so no added arc crosses the shore.  Thus the shores, and their original
outgoing boundaries, correspond in both directions.

The same observation shows no artificial arc crosses any dicut.  Taking
minimum cardinalities gives (1).  QED

The distinctness condition in (TC) is essential.  If the clamps merge, no
incoming-closed shore can contain all of `T` while excluding all of `S-T`, so
the intended trace family is empty.

## Automatic adequacy theorem

**Theorem 2.**  If `(D,S,T)` is terminal-clampable, then `D` has
`mu_D(T)` pairwise arc-disjoint `T`-covers.  In particular it has
`min(3,mu_D(T))` such covers.

**Proof.**  The condensation in (TC) has one source and one sink, so it is
source--sink connected.  Apply the cited source--sink-connected dijoin
packing theorem to the unweighted auxiliary digraph `D[T]`.  By (1), it
supplies `mu_D(T)` pairwise arc-disjoint dijoins.

Delete every artificial clamp arc from every packed dijoin.  This preserves
pairwise disjointness.  It also preserves the dijoin property because Lemma 1
shows that artificial arcs lie in no dicut and therefore can never be the
only intersection with one.  Restricting the remaining sets to original arcs
gives `mu_D(T)` disjoint sets meeting every member of `B_D(T)`, exactly the
required `T`-covers.  QED

This is stronger than the three-colour adequacy needed downstream: it packs
the full local trace minimum.

The class is not confined to pieces which were already source--sink
connected.  For example, take four vertices and two arcs

```text
s1->t1,  s2->t2,
S={s1,s2,t1,t2},  T={s1,s2}.
```

The original DAG has two sources and two sinks, and `s1` cannot reach `t2`.
After clamping `s1,s2` together and `t1,t2` together, however, the
condensation has exactly one source block and one sink block.  Its fixed-trace
boundary is the two displayed arcs, so Theorem 2 returns the two singleton
`T`-covers.  Replacing each displayed arc by any number of parallel copies
gives arbitrary local trace minimum.  This small family also makes clear that
the artificial clamp is a proof device, not an assumption that the original
sources can reach every original sink.

## Consequence for a one-optional-trace sum

Consider an arc-disjoint two-piece separator sum with exactly one relevant
optional trace `T`, no relevant forced traces, and global `tau=3`.  Let the
two local trace minima be `mu_1,mu_2`.  Compatible minimum local shores unite
to a global dicut, so

```text
mu_1 + mu_2 >= 3.                                        (2)
```

If both local trace instances are terminal-clampable, Theorem 2 gives at least
`min(3,mu_i)` disjoint covering slots in piece `i`; pad with empty slots to
make triples.  Inequality (2) implies that the total number of covering slots
is at least three.  Pair every noncovering slot with a covering slot on the
other side.  Each union then covers `T`, hence every relevant global dicut.
This explicitly constructs three pairwise arc-disjoint global dijoins.

Thus Woodall's conjecture holds for this separator class.  The conclusion
also remains valid in the presence of forced traces if the same slots cover
all traces forced onto their piece; that simultaneous requirement is stated
rather than silently inferred from Theorem 2.

## Structural obstruction when clamping fails

The proof exposes an exact obstruction to this automatic-adequacy route.
After clamping, one of the following must occur:

1. `C_T=C_barT`, in which case the requested trace family is empty; or
2. the condensation has an initial strong component other than `C_T`; or
3. it has a terminal strong component other than `C_barT`.

Indeed, if the terminal components are distinct and neither 2 nor 3 occurs,
condition (TC) holds and Theorem 2 applies.  Cases 2 and 3 are concrete
directed reachability obstructions: respectively, some component is not
reachable from the clamped trace, or some component cannot reach the clamped
complement.

This is an obstruction to the clamping proof, not a claim that local
adequacy itself fails.  A non-clampable instance may still have the required
trace covers by another argument.  The corrected theorem keeps those two
statements separate.

## Relation to Robbins and why the stronger engine is needed

For local trace minimum two, one might try to repeat the Robbins
agreement/disagreement colouring used for the full `tau=2` case.  Lemma 1
shows the safe way to do so: apply Robbins to the entire auxiliary dicut
family, not just to the underlying graph of the original piece.  Under (TC),
the source--sink-connected theorem already gives the stronger result for all
`mu`, including two.  Without an exact auxiliary-family correspondence,
an orientation edge can cross an artificial contraction cut while being
internal to the intended global shore--the phantom-crossing error.

## Mandatory filters

1. **Schrijver filter: passed.**  The load-bearing external theorem is the
   known source--sink-connected theorem, whose stronger integral-capacity
   form is itself valid.  The Woodall consequence here uses ordinary
   unit-capacity arc copies and disjoint slots.  No claim is made that weighted
   minimum trace value alone supplies usable covers outside the terminally
   clamped class, so Schrijver's counterexample is not contradicted.
2. **Lucchesi--Younger filter: passed.**  No dicut/dijoin min-max role swap is
   used.  The only packing input is the cited source--sink-connected theorem;
   Lemma 1 independently proves that its actual packed dijoins are the needed
   trace covers.
3. **Easy-direction filter: passed.**  Theorem 2 constructs `mu_D(T)`
   disjoint covers, and the separator consequence pairs them to construct
   three global dijoins.  It does not infer existence from the trivial
   minimum-cut upper bound.

## Dependency, scope, and review targets

The external dependency is the cited source--sink-connected capacitated
packing theorem recorded in the problem README: Schrijver, “Min-max relations
for directed graphs,” *Annals of Discrete Mathematics* **16** (1982),
Theorems 4 and 5 and Corollary 5a,
<https://ir.cwi.nl/pub/10048/10048D.pdf>.

The new deductions remain `sketch` pending independent review.  This is a
substantial local class but not a proof of automatic adequacy for every trace
family.  The highest-risk points are the unique-sink predecessor-closure
argument, the converse preservation of every fixed-trace shore after adding
clamp arcs, and deletion of artificial arcs from the packed dijoins.
