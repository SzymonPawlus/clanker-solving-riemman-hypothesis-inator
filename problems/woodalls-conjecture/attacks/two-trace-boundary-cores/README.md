# Joint two-trace realization from minimum boundary cores

**Issue:** #248. **Status:** `sketch`, targeting `verified:review`.

This supplies a noncomputational joint-realization theorem for the exact
two-trace profile inequalities of PR #246.  If every local trace family has a
common boundary core whose size equals that family's minimum boundary, its
core arcs are singleton covers.  The two cores can be coloured jointly so
that the smaller colour support is contained in the larger one.  At
`tau=3`, the global cut inequalities then force all four profile-intersection
inequalities automatically.

The theorem covers the crossed four-arc fixture from PR #243 and a broad
class with arbitrarily many shores per trace.  Its exact residual obstruction
is coreless cut variation: a trace family whose common intersection is
strictly smaller than its minimum member.

## Directed setup and conventions

For a finite digraph, a **dicut** is a nonempty outgoing boundary
`delta+(U)` with no arc entering `U`.  A **dijoin** meets every dicut.

Let `D=D1 union D2`, with disjoint arc sets and common vertex separator `S`.
Assume exactly two global traces `R_0,R_1` are relevant, both are optional in
both pieces (all their realizable local boundaries are nonempty), and there
are no relevant forced traces.

For piece `i` and trace `R_t`, let `B_it` be its family of local boundaries
and set

```text
mu_it = min{|B| : B in B_it},
C_it  = intersection of all B in B_it.                    (1)
```

Incoming-closed local shores with the same trace unite to a global
incoming-closed shore, with boundary the disjoint union of the two local
boundaries.  Conversely every global dicut restricts this way.

The no-entering hypothesis is essential.  A directed path has prefix
dicuts, a directed cycle has no dicut, and
`s1->t1, s2->t1, s2->t2` has singleton-source dicuts despite lacking one
source-to-sink path.  No arbitrary directed cut is used below.

## Core-complete trace families

Call a local trace family **core-complete** when

```text
|C_it| = mu_it.                                           (2)
```

Since a minimum member of `B_it` has size `mu_it` and contains the common
core, condition (2) says that every minimum boundary is exactly the core.
More importantly, every arc `a in C_it` belongs to every boundary of that
trace.  The singleton set `{a}` is therefore a trace cover.  Distinct core
arcs give pairwise arc-disjoint singleton covers.

Thus (2) is stronger than the full fixed-trace packing theorem: it makes the
packing atomic and leaves complete freedom to align its colours with another
trace family.

## A two-set colour-support lemma

**Lemma 1.**  Let `A,B` be finite sets and put

```text
a=min(3,|A|),  b=min(3,|B|).
```

Their elements can be assigned to three disjoint slots so that exactly `a`
slots meet `A`, exactly `b` slots meet `B`, and exactly `min(a,b)` slots meet
both.  Equivalently, the colour support of the smaller set can be made a
subset of the colour support of the larger set.

**Proof.**  Suppose `a<=b`.  Choose `a` distinct elements `A'` of `A` and
give them distinct colours `1,...,a`.  If some chosen element also lies in
`B`, retain its colour for `B`.  If `r=|A' intersection B|`, choose
`b-r` further elements of `B-A'`; enough exist because
`|B-A'|=|B|-r>=b-r`.  Assign them the still-missing colours among
`1,...,b`.  Put equally coloured elements in one slot and leave unchosen
elements unused.  Then `A` uses colours `1,...,a` and `B` uses
`1,...,b`.  The case `b<=a` is symmetric.  No element is assigned twice.
QED

Applied to `A=C_i0` and `B=C_i1`, every nonempty slot is a singleton or a
two-arc set and covers precisely the indicated trace or traces.  Additional
accidental coverage only strengthens the resulting profile.

## Joint realization theorem at `tau=3`

For each piece define capped local ranks

```text
a_it = min(3,mu_it).
```

Lemma 1 constructs three pairwise arc-disjoint slots whose trace-coverage
counts are at least

```text
both traces: min(a_i0,a_i1),
trace 0:     a_i0,
trace 1:     a_i1,
neither:     3-max(a_i0,a_i1).                           (3)
```

**Theorem 2.**  If `tau(D)=3` and all four local trace families are
core-complete, then `D` has three pairwise arc-disjoint dijoins.

**Proof.**  Choose minimum local boundaries for a fixed trace `R_t` in both
pieces.  Their shores are compatible and their union is a global dicut, so

```text
mu_1t + mu_2t >= 3,  t=0,1.                              (4)
```

Capping each summand at three preserves these inequalities:

```text
a_1t+a_2t>=3.                                            (5)
```

Use Lemma 1 in each piece.  Let `b_i` be the number of both-cover slots and
`e_i` the number covering neither.  Formula (3) gives

```text
b_i >= min(a_i0,a_i1),
e_i <= 3-max(a_i0,a_i1).
```

From (5),

```text
min(a_20,a_21)
  >= min(3-a_10,3-a_11)
   = 3-max(a_10,a_11),
```

so `e_1<=b_2`; symmetrically `e_2<=b_1`.  Equation (5) also says that at
least three slots across the two pieces cover trace 0 and at least three
cover trace 1.

These four inequalities are precisely Hall's condition for the slot graph:
a neither-slot can pair only with a both-slot; a trace-0-only slot pairs with
a trace-1 or both slot; a trace-1-only slot pairs symmetrically; and a
both-slot pairs with anything.  For completeness, a Hall-deficient set can
be reduced to one of: neither slots alone, neither plus trace-0-only, neither
plus trace-1-only, or all non-both slots.  The four inequalities rule out
those cases.  Hence the slot graph has a perfect matching.

Pair the slots along that matching.  Each pair covers both relevant traces,
so its arc-set union meets every global dicut.  The three unions are
arc-disjoint because the local slots and the two piece arc sets are disjoint.
They are the required three global dijoins.  QED

The proof constructs the nontrivial existence direction; `tau=3` is used in
(4), not merely to rule out a fourth dijoin.

## Crossed complementarity is included

In the four-arc fixture, piece 1 has arcs `a1:s->t,b:z->t` and piece 2 has
`a2:s->t,c:s->z`, with traces `{s}` and `{s,z}`.  Its four cores are

```text
C_10={a1},    C_11={a1,b},
C_20={a2,c},  C_21={a2}.
```

All are minimum boundaries.  Lemma 1 produces profiles

```text
piece 1: both {a1}, trace-1-only {b}, neither;
piece 2: both {a2}, trace-0-only {c}, neither.
```

The matching in Theorem 2 returns `{a1},{a2},{b,c}`.  Thus the theorem
captures precisely the complementary third colour missed by using only the
minimum interval rank.

## Broad examples and closure

Core-completeness does not require a trace family to have one shore.  Any
number of larger boundaries may occur, provided they all contain one common
minimum boundary.  Adding arcs which occur in every boundary enlarges the
core and minimum together; adding arbitrary arcs wholly inside or outside
all trace shores changes neither.  Parallel arc bundles and nested
source-closed regions therefore give infinite families.

The property is also inherited after contracting any vertex set which no
trace shore splits, because the corresponding boundary arc sets are
unchanged.  Hence core-complete pieces may contain arbitrary contracted
strong components and forced-in/forced-out regions.

## Exact corrected obstruction

Within the stated two-trace setup, failure of its only additional structural
hypothesis means that at least one local trace family is **coreless**:

```text
|intersection B_it| < min{|B|:B in B_it}.                (6)
```

This is the exact obstruction to the atomic singleton-cover construction,
not an assertion that three global dijoins fail.  Corelessness means every
minimum boundary contains some replaceable arc: no minimum-size set of arcs
is common to all shores.  Flow paths can still give the full single-trace
packing, but different covers must use multi-arc routes and may interfere
with the other trace's routes.

Condition (6) is genuinely possible.  On a directed path with the terminals
pinned at its ends, every prefix boundary is a different singleton.  The
trace minimum is one while the common core is empty.  The entire path is a
valid trace cover, so corelessness does not refute adequacy; it identifies
the precise point where a flow-exchange or locking theorem, rather than
atomic colouring, is needed.

## Mandatory filters

1. **Schrijver filter: passed.**  Core arcs are distinct unit-capacity arcs
   and become actual disjoint singleton covers.  Weighted minimum boundary
   value does not imply a common core of that many usable unit arcs,
   especially with zero-weight structural arcs.  No weighted all-trace
   packing equality is inferred.
2. **Lucchesi--Younger filter: passed.**  No dicut/dijoin min-max role swap is
   used.  Singleton core covers are verified against every local boundary,
   and matched unions are checked directly against both global trace
   families.
3. **Easy-direction filter: passed.**  The proof explicitly colours core
   arcs, finds a perfect matching, and constructs three disjoint global
   dijoins.  It does not replace existence with the minimum-cut upper bound.

## Status and review targets

The argument is elementary and noncomputational.  It remains `sketch` until
independently reviewed.  The highest-risk points are the colour-support lemma
when the two cores overlap, the derivation of the empty-versus-both Hall
inequalities from (5), and the claim that accidental extra trace coverage can
only help the compatibility matching.
