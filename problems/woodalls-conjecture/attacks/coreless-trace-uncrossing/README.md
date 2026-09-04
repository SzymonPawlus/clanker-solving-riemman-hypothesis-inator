# Coreless trace boundaries: exact uncrossing and sharp limits

**Issue:** #250. **Status:** `sketch`, targeting `verified:review`.

This attack tests whether the coreless residual case from PR #249 can be
removed by uncrossing minimum fixed-trace boundaries.  The hoped-for boundary
structure is false: a four-arc directed diamond has a minimum fixed-trace
boundary family which has empty common core and is neither laminar nor a
sunflower.  Thus uncrossing cannot justify the atomic colouring used in
PR #249.

There is nevertheless an exact positive replacement.  Outgoing-boundary
cardinality is modular, not merely submodular, on incoming-closed shores.
Consequently, minimum shores for two comparable traces can always be chosen
nested.  This is the strongest conclusion supplied by elementary uncrossing:
the *shores* can be laminarized, while their boundary arc sets need not be
laminar and need not contain any common arc.

Finally, a four-element abstract example shows that the single-trace packing
theorems and all global cut-size inequalities alone do not force compatible
two-trace profiles.  It is deliberately recorded only as a set-system
obstruction: simultaneous realization of its two crossed families as traces
of one directed piece is not asserted.

## Reference status of the PRs cited below (checked 2026-09-04)

**PRs #239, #246 and #249 are all open and unmerged.**  None of their content is
on `main`, so a reader here cannot check any of it, and under `RULES.md` §3
nothing in this file may rest on it.  Where each is named:

- **#249** ("Jointly realize two-trace profiles from boundary cores") is the
  attack whose hoped-for boundary structure this file refutes.  The terms
  *atomic colouring* and *atomic singleton-cover method* are undefined on `main`;
  they are names for #249's method and appear here only to say which method the
  directed diamond (3) rules out.  Nothing below uses them as a hypothesis.
- **#239** ("Pack every fixed-trace dicut family by max flow") is named once, to
  record that corelessness does *not* obstruct it.  That is a negative remark
  about a result this file does not use.
- **#246** ("Characterize two-trace profile intersection at tau=3") supplied, in
  the version of this file first written, the two Hall inequalities used to
  close the final section.  That gap is now closed inside this file: the
  inequalities needed are stated and proved from scratch as Lemma 3, for the
  two-piece abstract system only.  #246 is retained as a pointer to the general
  form, which this file neither states nor uses.

Status is unaffected: everything here is and remains `sketch`.

## Directed definitions

For a finite digraph `D=(V,A)`, a **dicut** is a nonempty outgoing boundary
`delta+(X)` of a shore `X` with `delta-(X)=empty`.  Such a shore is called
**incoming-closed**.  A **dijoin** meets every dicut.

A **separator** is the shared vertex set `S=V(D_1) intersection V(D_2)` of a
decomposition of `D` into two pieces with disjoint arc sets, in the sense of
`attacks/serial-parallel-separator-composition`.  No separating property of `S`
is used in this file: Lemma 1 and Theorem 2 below hold verbatim for an arbitrary
vertex subset `S subseteq V`, and the reader may take `S` that way.

Fix such an `S`.  The **trace** of a shore `X` is `X intersection S`.  A
fixed-trace boundary family consists of the sets `delta+(X)` over
incoming-closed shores with `X intersection S=R`, for one fixed trace
`R subseteq S`.  Its minimum boundary size is denoted `mu(R)`.  A trace
`R subseteq S` is **realizable** when at least one incoming-closed shore has
trace `R` — equivalently, when its fixed-trace family is nonempty, so that
`mu(R)` is defined.  Realizability is exactly the hypothesis Theorem 2 uses, and
all it uses.

These are genuine dicuts, not arbitrary directed cuts.  On a directed path,
the proper nonempty prefixes are incoming-closed and give singleton dicuts.
A directed cycle has no dicut.  In a DAG with two sources, each source shore
may give a dicut independently.

Two further words are used in the abstract sections below.  Consider a ground
set `E` carrying two families `F_0,F_1` indexed by two traces.  A **slot** is one
of the pairwise disjoint subsets of `E` making up a candidate packing — the
abstract stand-in for one colour class of a dijoin packing.  The **profile** of a
slot `T` is the set of traces it covers,

```text
profile(T) = { t in {0,1} : T meets every member of F_t }.
```

A slot has a **nonempty profile** when it covers at least one of the two
families.  Throughout, `b` counts the slots of profile `{0,1}` ("both") and `e`
counts the slots of profile `empty` ("neither").

## Exact modularity on incoming-closed shores

**Lemma 1 (modular boundary identity).**  If `X` and `Y` are incoming-closed,
then `X intersection Y` and `X union Y` are incoming-closed and

```text
|delta+(X)|+|delta+(Y)|
  = |delta+(X intersection Y)|+|delta+(X union Y)|.       (1)
```

**Proof.**  Closure under intersection and union is immediate.  There is no
arc between `X-Y` and `Y-X`: in either orientation it would enter one of the
two incoming-closed shores.  Now classify each arc by the four regions

```text
X intersection Y,  X-Y,  Y-X,  V-(X union Y).
```

With arcs between the two middle regions excluded, its total incidence in
the two boundaries on the left of (1) equals its total incidence in the two
boundaries on the right.  Summing over arcs proves (1).  QED

The exclusion of entering arcs is essential.  For arbitrary shores, arcs
between the two symmetric differences give only submodularity and the exact
identity can fail.

## Comparable traces have nested minimum shores

**Theorem 2 (exact trace uncrossing).**  Let `R subseteq T` be two realizable
traces.  There are minimum incoming-closed shores `X_R,X_T` for the two trace
families such that

```text
X_R subseteq X_T.                                       (2)
```

More strongly, if `X` is any minimum shore of trace `R` and `Y` any minimum
shore of trace `T`, then `X intersection Y` is a minimum shore of trace `R`
and `X union Y` is a minimum shore of trace `T`.

**Proof.**  Since `R subseteq T`, the two uncrossed shores have traces

```text
(X intersection Y) intersection S = R,
(X union Y) intersection S = T.
```

They are incoming-closed by Lemma 1.  Hence their boundary sizes are at least
`mu(R)` and `mu(T)`, respectively.  Lemma 1 says their sum equals
`|delta+(X)|+|delta+(Y)|=mu(R)+mu(T)`.  Both lower bounds must therefore be
equalities.  Taking the intersection and union gives the nested pair (2).
QED

Repeatedly applying Theorem 2 laminarizes a chosen minimum-shore pair for two
comparable traces.  It does **not** laminarize the corresponding boundary arc
sets.  In particular, nesting `X subseteq Y` still allows an arc to leave
both shores, or different arcs to leave the inner and outer shore.

## Directed obstruction to boundary cores, laminarity, and sunflowers

Consider the directed diamond

```text
        1       2
     s ---> u ---> t
        3       4
     s ---> v ---> t
```

Pin `s` inside and `t` outside.  The four incoming-closed shores and their
boundaries are

```text
{s}:       {1,3},
{s,u}:     {2,3},
{s,v}:     {1,4},
{s,u,v}:   {2,4}.                                       (3)
```

All have size two, so all are minimum.  Their total intersection is empty.
They are not a sunflower: for example `{1,3}` meets `{1,4}` in `{1}`, but
meets `{2,4}` in the empty set.  They are not laminar: `{1,3}` and `{1,4}`
intersect and neither contains the other.

Thus a fixed-trace directed-cut family need not have a minimum boundary core,
a sunflower of minimum boundaries, or laminar minimum boundary sets.  The
minimum *shores* in this example form the Boolean diamond and can be uncrossed
by intersection and union, exactly as Theorem 2 says.  Shore uncrossing does
not create arcs common to all boundaries.

The family still has two disjoint covers, `{1,2}` and `{3,4}`.  Corelessness
therefore does not obstruct the single-trace max-flow theorem of PR #239; it
obstructs only the atomic singleton-cover method of PR #249.

## Exact abstract obstruction to profile-only reasoning

Let the ground set be `E={1,2,3,4}` and define two boundary families

```text
F_0 = { {1,3}, {1,4}, {2,3}, {2,4} },
F_1 = { {1,2}, {1,4}, {2,3}, {3,4} }.                   (4)
```

A set covers `F_0` exactly when it contains `{1,2}` or `{3,4}`; it covers
`F_1` exactly when it contains `{1,3}` or `{2,4}`.  Hence both minimum
transversal numbers are two, and every set covering both families has at
least three elements.

Classify three pairwise disjoint slots by their profiles, as defined in
*Directed definitions* above, and let `b` and `e` count the both-cover and
neither-cover slots.  (The open PR #246 studies this classification in general;
nothing from it is used, here or below.)  Every such triple satisfies

```text
e > b.                                                   (5)
```

Indeed, there cannot be two both-covers because each uses at least three of
the four elements.  If `b=1`, at most one element remains, so the other two
slots cover neither trace and `e>=2`.  If `b=0` and all three slots had a
nonempty profile, each would use at least two elements, impossible on a
four-element ground set; hence `e>=1`.

### The two-piece system

Take two disjoint copies of (4) as abstract pieces.  Concretely, let `E_1` and
`E_2` be disjoint four-element ground sets, each carrying its own copy
`F_0^i,F_1^i` of the two families in (4).  Global boundaries are formed by the
disjoint union of one same-trace boundary from each copy: for a trace
`t in {0,1}`,

```text
G_t = { B_1 union B_2 : B_1 in F_t^1, B_2 in F_t^2 }.    (6)
```

A **global transversal** is a set `T subseteq E_1 union E_2` meeting every
member of `G_0` and every member of `G_1`.  Every global boundary has size four,
in particular at least three.

**Observation (splitting).**  `T` meets every member of `G_t` if and only if
`T intersection E_1` covers `F_t^1` or `T intersection E_2` covers `F_t^2`.

**Proof.**  In (6) the two parts `B_1 subseteq E_1` and `B_2 subseteq E_2` are
chosen independently, and `T intersection (B_1 union B_2)` is empty exactly when
`T intersection B_1` and `T intersection B_2` are both empty.  So `T` misses
some member of `G_t` if and only if `T intersection E_1` misses some member of
`F_t^1` **and** `T intersection E_2` misses some member of `F_t^2`.  Negating
both sides gives the claim.  QED

Writing `P_i(T)` for the profile of the slot `T intersection E_i` in piece `i`,
that is

```text
P_i(T) = { t in {0,1} : T intersection E_i covers F_t^i },
```

the observation says that `T` is a global transversal if and only if

```text
P_1(T) union P_2(T) = {0,1}.                             (7)
```

**Lemma 3 (empty-versus-both inequalities for this system).**  Let
`T^1,T^2,T^3` be pairwise disjoint global transversals.  For `i in {1,2}` let
`b_i` be the number of indices `j` with `P_i(T^j)={0,1}` and `e_i` the number of
indices `j` with `P_i(T^j)=empty`.  Then

```text
e_1 <= b_2,  e_2 <= b_1.                                 (8)
```

**Proof.**  Fix `j` with `P_1(T^j)=empty`.  By (7) the union
`P_1(T^j) union P_2(T^j)` is `{0,1}`, so `P_2(T^j)={0,1}`.  Hence the identity
map on indices sends every index counted by `e_1` to an index counted by `b_2`,
injectively, giving `e_1 <= b_2`.  Exchanging the roles of the two pieces gives
`e_2 <= b_1`.  QED

Now the three sets `T^j intersection E_i`, `j=1,2,3`, are pairwise disjoint
subsets of the four-element ground set `E_i`, whose two families are a copy of
(4).  So (5) applies inside each piece and gives `e_i>b_i` for `i=1,2`.  Adding
the two inequalities of (8),

```text
e_1+e_2 <= b_2+b_1 < e_1+e_2,
```

a contradiction.  Thus three disjoint global transversals do not exist in this
abstract boundary system, despite the single-family packing property and the
global boundary lower bound.

**Dependency note.**  (8) is the empty-versus-both Hall inequality that the open
PR #246 states in a general setting.  That general statement is not on `main`
and is *not* used here: Lemma 3 proves only what this section needs, for this
two-piece system, from (6), (7) and the definitions above.  #246 is retained
solely as a pointer to the general form.  Consequently this section depends on
nothing beyond (4), (5) and Lemma 3, all of which are in this file — and, being
an agent's own argument, it stays `sketch` (`RULES.md` §3) rather than
inheriting a status from unmerged work.

Each family in (4) is separately isomorphic to the genuine directed diamond
family (3).  However, this attack does not realize the two crossed families
simultaneously as two traces in one directed piece.  Therefore (4) is an
exact obstruction to any proof using only abstract family minima and
single-trace packing, **not** a counterexample to Woodall's conjecture.
Directed incidence and the interaction between the two trace families are
the additional structure a successful exchange theorem must use.

## Corrected conclusion and next target

The proposed implication

```text
fixed-trace directed boundaries
  => minimum boundaries have a core / sunflower / laminar form
```

is false.  Its correct uncrossing replacement is Theorem 2:

```text
comparable traces => nested minimum shores,
```

with no corresponding common-arc conclusion.  The abstract example proves
that a general transversal or polymatroid argument based only on the two
individual boundary families is also insufficient.

The remaining viable target is therefore a directed exchange theorem that
uses the shared vertex-and-arc incidence of both auxiliary flows.  For
comparable traces, Theorem 2 supplies nested extremal shores around which
such an exchange can be localized.  Any claimed theorem must exploit more
than their cut values: (4) shows those numerical data alone admit a sharp
Hall obstruction.

## Mandatory filters

1. **Schrijver filter: passed.**  The modular identity and directed diamond
   concern actual unweighted arc sets.  The positive result only selects
   minimum shores; it does not infer a weighted or unweighted dijoin packing.
   The abstract obstruction explicitly shows why cut values alone are
   insufficient.
2. **Lucchesi--Younger filter: passed.**  No dicut/dijoin min-max equality is
   assumed.  The diamond covers are checked directly, and the abstract
   nonpacking statement is a direct disjointness count.
3. **Easy-direction filter: passed.**  This is a structural theorem and a
   refutation of a proposed proof route, not a claim that a cut upper-bounds
   a packing.  Where nonexistence is asserted, (5) supplies the explicit Hall
   obstruction.

## Status and review targets

The result is noncomputational.  It remains `sketch` until independently
reviewed.  The highest-risk points are the arcwise modular identity, trace
preservation under intersection and union, the characterization of the two
abstract transversal families, the splitting observation and Lemma 3 in the
two-piece system, and the careful separation between an abstract profile
obstruction and a simultaneously realizable directed two-trace obstruction.

A reviewer should note that no statement in this file rests on unmerged work:
#239, #246 and #249 are open at the time of writing and are cited only as
pointers, as recorded near the top.
