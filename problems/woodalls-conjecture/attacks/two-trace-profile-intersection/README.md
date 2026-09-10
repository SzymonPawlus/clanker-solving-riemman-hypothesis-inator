# Exact two-trace profile intersection at `tau=3`

**Issue:** #244. **Status:** `sketch`, targeting `verified:review`.

This solves the **abstract profile-pairing problem** for two trace families.
Each local slot has one of four profiles--covers both traces, only the first,
only the second, or neither.  Although the slot compatibility graph has nine
possible edges, Hall's condition collapses exactly to four integer
inequalities on these profile counts.

The theorem captures complementary local minima such as the four-arc fixture
from PR #243: a first-only slot on one side pairs with a second-only slot on
the other.  It also gives a finite forbidden-profile list when pairing is
impossible.  No computation is used.

The profile theorem is an exact `if and only if`.  Its application to digraphs
is also exact under the explicit separator hypotheses below.  The important
extra fact is Cartesian closure: any two incoming-closed local shores with the
same trace unite to a global shore.  Consequently, if neither local arc set
covers a trace, two locally missed boundaries can be combined into one
globally missed dicut.

## Directed setup and the exact transfer lemma

For a finite digraph, a **dicut** is a nonempty outgoing boundary
`delta+(U)` with no arc entering `U`; a **dijoin** meets every dicut.

Here is the precise separator setup used later.  Let `V=V1 union V2`, let
`S=V1 intersection V2`, and partition the indexed arc set as
`A=A1 disjoint-union A2`, with both ends of each arc in `A_i` belonging to
`V_i`.  Write `D_i=(V_i,A_i)`.  This is what **separator sum** means below.
For a global shore `U`, its **trace** is `U intersection S` and its restriction
to piece `i` is `U_i=U intersection V_i`.

Fix two distinct traces `R_0,R_1`.  They are **exactly the relevant traces**
when each occurs as the trace of a global dicut shore and every global dicut
shore has one of these two traces.  For `i in {1,2}` and `r in {0,1}`, define
the local family

```text
F_i(r) = { delta+_{D_i}(W) : W subseteq V_i is incoming-closed
                              and W intersection S = R_r }.
```

Assume every member of every `F_i(r)` is nonempty.  This explicit condition
is what the earlier sketches called both traces **optional** on both pieces;
it also excludes a **forced** trace, meaning a trace with an empty-boundary
local realization on some piece.  Relevance guarantees the local families
needed by a global dicut are inhabited, but the argument below does not need
to assign a minimum to an uninhabited family.

A local arc set `X_i subseteq A_i` **covers trace `r`** when it meets every
member of `F_i(r)`.

**Lemma (exact directed transfer).**  The union `X_1 union X_2` is a global
dijoin if and only if, for each `r in {0,1}`, at least one of `X_1,X_2`
covers trace `r`.

**Proof.**  Let `U` be a global dicut shore and put `U_i=U intersection V_i`.
No arc of `D_i` enters `U_i`, since such an arc would enter `U` in `D`.
The restrictions have the same trace `U intersection S`, which by hypothesis
is `R_r` for some `r`.  Moreover

```text
delta+_D(U) = delta+_{D_1}(U_1) disjoint-union delta+_{D_2}(U_2),
```

because the arc sets partition `A` and every arc of `A_i` has both ends in
`V_i`.  Each restricted boundary is therefore in `F_i(r)` (and is nonempty
by the explicit hypothesis).  If `X_i` covers `r`, it meets the corresponding
summand and hence `X_1 union X_2` meets `delta+_D(U)`.  This holds for every
global dicut.  This proves sufficiency.

Conversely, suppose `X_1 union X_2` is a dijoin but neither local set covers
some trace `r`.  For each `i`, choose an incoming-closed local shore `W_i`
with trace `R_r` whose nonempty boundary is missed by `X_i`.  Equal traces
make `W=W_1 union W_2` well-defined on `S`.  An arc entering `W` belongs to
some `A_i` and would enter `W_i`, so none exists.  Its boundary is the
disjoint union of the two chosen nonempty local boundaries, hence is nonempty
and is missed by `X_1 union X_2`.  Thus `W` is a global dicut shore missed by
the alleged dijoin, a contradiction.  QED

This Cartesian argument explains why “the two pieces might split the local
boundaries between them” is not a counterexample: independently missed local
boundaries can always be paired into one missed global boundary.  Without
equal-trace gluing or without the nonempty-boundary hypothesis, the necessity
direction would indeed be unjustified.

The nonempty-boundary hypothesis is load-bearing.  For example, take
`S={s,t}`, let piece 1 add a private vertex `x` and the sole arc `s->x`, and
let piece 2 add a private vertex `y` and the sole arc `s->y`.  At trace `{s}`,
piece 1 has local shores `{s}` (boundary `{s->x}`) and `{s,x}` (empty
boundary), and symmetrically for piece 2.  Hence no local arc set covers this
trace under the definition above.  Nevertheless the union of the two arcs is
a global dijoin: the only nonempty global boundaries are `{s->x,s->y}`,
`{s->x}`, and `{s->y}`.  The locally empty shores unite to a globally empty
boundary, which is not a dicut.  Thus dropping hypothesis 3 would make the
necessity direction false.

This uses the actual dicut definition.  A directed path has prefix dicuts, a
directed cycle has no dicut, and
`s1->t1, s2->t1, s2->t2` has singleton-source dicuts despite lacking one
source-to-sink path.  Cuts with entering arcs are never included.

## Four local profiles

Fix three pairwise arc-disjoint slots in each piece; empty slots are allowed.
Classify a slot by the subset of `{0,1}` whose traces it covers.  In piece
`i`, write

```text
b_i = number of {0,1}-slots (both),
p_i = number of {0}-slots   (first only),
q_i = number of {1}-slots   (second only),
e_i = number of empty-profile slots (neither),
```

so `b_i+p_i+q_i+e_i=3`.  “Empty-profile” does not require the arc set itself
to be empty; it means only that it covers neither relevant trace.

Two slots are compatible precisely when the union of their profiles is
`{0,1}`.  Thus their local arc-set union is a global dijoin.  The neighborhood
types in the bipartite compatibility graph are

| piece-1 type | compatible piece-2 types |
|---|---|
| both | both, first, second, neither |
| first only | both, second only |
| second only | both, first only |
| neither | both only |

## Exact abstract profile-intersection theorem

**Theorem 1 (profile matching).**  The two local triples can be bijectively
paired so that the union of the two profiles in every pair is `{0,1}` if and
only if all four inequalities hold:

```text
e_1 <= b_2,                                              (E1)
e_2 <= b_1,                                              (E2)
(b_1+p_1)+(b_2+p_2) >= 3,                               (T0)
(b_1+q_1)+(b_2+q_2) >= 3.                               (T1)
```

These are an exact two-piece profile-intersection criterion.  `(E1),(E2)`
say every neither-slot can be absorbed by an opposite both-slot.  `(T0)` and
`(T1)` say that, across the two pieces, at least three slots cover each trace.

**Proof.**  Necessity is immediate from any valid pairing.  A neither-slot
must meet a both-slot.  Also every one of the three pairs must contain a slot
covering trace 0 and a slot covering trace 1, giving `(T0),(T1)`.

For sufficiency, apply Hall's theorem to the type table.  A left subset
containing a both-slot has all three right vertices as neighbors, so it cannot
violate Hall.  For a subset using only the other three types, replacing it by
all available vertices of each type it uses can only make a Hall violation
harder to avoid.  The distinct neighborhood unions reduce as follows:

- neither alone requires `e_1<=b_2`, namely `(E1)`;
- neither plus first-only requires
  `e_1+p_1<=b_2+q_2`, which is `(T1)` after using both
  four-term sums equal to three;
- neither plus second-only similarly gives `(T0)`;
- all non-both left vertices require `3-b_1<=3-e_2`, namely `(E2)`.

Subsets omitting the neither type give weaker inequalities with the same
neighborhoods.  Thus `(E1),(E2),(T0),(T1)` imply every left Hall inequality.
Hall supplies a perfect matching.  This proves the abstract profile theorem.
In the directed setup above, the transfer lemma makes every matched union a
global dijoin; distinct pairs use distinct arc-disjoint slots in the two
arc-disjoint pieces.  QED

Because the transfer lemma is an equivalence, Theorem 1 is also an exact
criterion for whether these **prescribed** local slots admit a pairing into
three global dijoins.  It does not claim that failure of these particular
slots prevents some different choice of arc sets from forming three dijoins.

The proof also shows the four inequalities are the complete obstruction
list, not merely sufficient tests.

## Forbidden profile configurations

Failure has exactly one of four forms:

1. **left empty overload:** `e_1>b_2`;
2. **right empty overload:** `e_2>b_1`;
3. **trace-0 deficit:** fewer than three slots across both pieces cover
   `R_0`;
4. **trace-1 deficit:** fewer than three slots across both pieces cover
   `R_1`.

Each is a Hall certificate.  The first two are the isolated/rectangle
obstruction viewed at profile level.  The latter two say that complementary
single-trace slots themselves are too scarce.  Every failed prescribed-slot
gluing contains one of these four count obstructions; no additional
three-colour pattern is possible.

This is sharper than requiring compatibility degree at least two.  A slot
may have degree one while the four inequalities and a perfect matching still
hold.

## Rank form and a broad sufficient class

For a local triple define its exposed ranks

```text
c_i(0)=b_i+p_i,   c_i(1)=b_i+q_i,   c_i(01)=b_i,
n_i=e_i.
```

Theorem 1 becomes

```text
n_1 <= c_2(01),
n_2 <= c_1(01),
c_1(0)+c_2(0) >= 3,
c_1(1)+c_2(1) >= 3.                                    (3)
```

This is the promised two-piece rank-intersection condition.  The local
vectors are coverage-rank profiles; the first two inequalities absorb the
rank-zero slots using joint rank, and the last two intersect the two
single-trace covering requirements.

For motivation, the fixed-trace max-flow sketch of PR #239 proposes that a
local minimum boundary is the maximum number of disjoint covers, and the
interval-flow sketch of PR #243 proposes a source of both-covers.  Neither
unmerged sketch is assumed here: the directed result below takes the local
triples as an explicit hypothesis.  Theorem 1 states exactly what a
simultaneously realized choice of those local resources must satisfy to glue.

**Corollary 2 (explicit directed sufficient condition).**  Consider a
separator sum satisfying all of the following numbered hypotheses:

1. `V=V1 union V2`, `S=V1 intersection V2`, and
   `A=A1 disjoint-union A2`, with both endpoints of every `A_i` arc in `V_i`;
2. each of `R_0,R_1` occurs, and every global dicut shore has one of those
   two traces;
3. every incoming-closed local shore with either trace has nonempty local
   outgoing boundary;
4. each piece has three pairwise arc-disjoint local slots, and the resulting
   profile counts satisfy (3).

Then the digraph has three pairwise arc-disjoint dijoins.  If additionally
`tau(D)=3`, it satisfies Woodall's conjecture: assign every arc outside the
three dijoins to one of them (arbitrarily, for instance all to the first).
The enlarged first set remains a dijoin, the three sets then partition `A`,
and disjointness is preserved.

**Proof.**  Theorem 1 pairs the profiles.  Each paired profile union is
`{0,1}`, so the directed transfer lemma makes the corresponding arc-set union
a global dijoin.  Slot disjointness and `A1 disjoint A2` make the three unions
pairwise arc-disjoint.  The final partition extension uses only the fact that
a superset of a dijoin is again a dijoin.  QED

This includes several useful subfamilies:

- three both-covers in either piece;
- one both-cover in each piece, at most one neither-slot on each side, and a
  total of three covers of each individual trace;
- crossed complementary triples, where first-only slots on one side balance
  second-only slots on the other.

The result requires no alignment of the two local minimum boundary shores.

## The four-arc crossed fixture revisited

Let `S={s,z,t}`, with traces `R_0={s}` and `R_1={s,z}`.  Piece 1 has arcs

```text
a1:s->t, b:z->t,
```

and piece 2 has

```text
a2:s->t, c:s->z.
```

Choose profiles

```text
piece 1: {a1}=both, {b}=second-only, empty=neither;
piece 2: {a2}=both, {c}=first-only,  empty=neither.
```

Thus `(b_1,p_1,q_1,e_1)=(1,0,1,1)` and
`(b_2,p_2,q_2,e_2)=(1,1,0,1)`.  All four inequalities are equalities.  The
matching pairs `{a1}` with one opposite empty slot, `{a2}` with the other
empty slot, and `{b}` with `{c}`, producing

```text
{a1}, {a2}, {b,c}.
```

The two nonempty dicuts are `{a1,a2,c}` and `{a1,a2,b}`, so these are three
global dijoins and `tau=3`.  The profile theorem explains the complementary
third colour which a simultaneous interval-flow count alone misses.

## What remains existential

Theorem 1 is exact for any supplied local profile triples.  A complete
two-trace theorem would also need to prove that local flow covers can always
be selected together so their profile counts satisfy (3) whenever all global
trace dicuts have size at least three.  That is a genuine common-capacity
intersection problem: separate maximum flows may assign the same unit arc to
different colours.

If such selection fails, Theorem 1 proves that every failure exposes one of
the four forbidden count profiles above.  This is a much smaller target than
an arbitrary `3 by 3` compatibility graph and is the exact finite obstruction
to attack with flow exchange or a polymatroid intersection theorem.

## Dependencies and mandatory filters

**Depends-on:** none.  The profile theorem uses only finite Hall matching,
and the directed corollary is proved above directly from its four explicit
hypotheses.  PRs #239 and #243 are unmerged `sketch` motivation for how local
slots might be produced; no assertion from either is a premise.  The sole
standard external input is Hall's marriage theorem: P. Hall, “On
Representatives of Subsets,” *Journal of the London Mathematical Society*
**s1-10** (1935), 26–30, <https://doi.org/10.1112/jlms/s1-10.37.26>.

1. **Schrijver filter: passed.**  The theorem begins with actual disjoint
   slots made of unit-capacity arcs.  Weighted minimum dicut values do not
   produce a jointly realizable local profile satisfying (3), especially in
   the presence of zero-weight structural arcs.  No weighted all-trace
   packing equality is inferred.
2. **Lucchesi--Younger filter: passed.**  No dicut/dijoin min-max role swap is
   used.  Each compatible slot union is checked directly against both trace
   families; Hall is applied only to the four-type slot graph.
3. **Easy-direction filter: passed.**  A perfect matching explicitly
   constructs the three global dijoins.  The theorem is not the trivial
   observation that a size-three dicut prevents a fourth.

## Status and review targets

The proof is elementary and noncomputational.  It remains `sketch` until
independently reviewed.  Its highest-risk points are completeness of the four
Hall inequalities, the algebra identifying the mixed-type Hall subsets with
`(T0),(T1)`, and the claim that no additional profile obstruction is hidden
inside slots of the same type.
