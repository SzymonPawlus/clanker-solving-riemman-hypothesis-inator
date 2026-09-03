# Exact two-trace profile intersection at `tau=3`

**Issue:** #244. **Status:** `sketch`, targeting `verified:review`.

This solves the cross-piece pairing problem for two relevant optional traces.
Each local slot has one of four profiles--covers both traces, only the first,
only the second, or neither.  Although the slot compatibility graph has nine
possible edges, Hall's condition collapses exactly to four integer
inequalities on these profile counts.

The theorem captures complementary local minima such as the four-arc fixture
from PR #243: a first-only slot on one side pairs with a second-only slot on
the other.  It also gives a finite forbidden-profile list when pairing is
impossible.  No computation is used.

## Directed setup

For a finite digraph, a **dicut** is a nonempty outgoing boundary
`delta+(U)` with no arc entering `U`; a **dijoin** meets every dicut.

Let `D=D1 union D2`, with disjoint arc sets and common vertex separator `S`.
Assume the only relevant global separator traces are two traces `R_0,R_1`,
both optional: in each piece every realizable local boundary at either trace
is nonempty.  Assume there are no relevant forced traces.

Incoming-closed local shores with equal trace unite to an incoming-closed
global shore, and their boundaries unite disjointly.  Conversely every global
dicut restricts this way.  Hence a union of two local arc sets is a global
dijoin exactly when, for each of `R_0,R_1`, at least one local set covers that
trace.

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

## Exact profile-intersection theorem

**Theorem 1.**  The two local triples can be bijectively paired into three
pairwise arc-disjoint global dijoins if and only if all four inequalities hold:

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
Hall supplies a perfect matching.  Every matched pair is a global dijoin by
the directed restriction argument, and distinct pairs use distinct
arc-disjoint slots in each arc-disjoint piece.  QED

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

For each trace separately, the fixed-trace max-flow theorem of PR #239 shows
that its local minimum boundary is the maximum number of disjoint covers.
For adjacent traces, PR #243 similarly supplies the maximum possible number
of both-covers from one interval flow.  Theorem 1 states exactly what a
simultaneously realized choice of those local resources must satisfy to glue.
It does not assume that independently chosen maximum flows are automatically
compatible.

**Corollary 2.**  A `tau=3` two-piece separator sum with exactly two relevant
optional traces and no forced trace satisfies Woodall whenever its pieces
admit local arc-disjoint triples whose rank profiles satisfy (3).

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

## Mandatory filters

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
