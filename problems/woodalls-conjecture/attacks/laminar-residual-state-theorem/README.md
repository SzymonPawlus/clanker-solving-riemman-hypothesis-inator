# Exact eight-state theorem for laminar bow-tie residual demands

**Issue:** #233. **Status:** `sketch`; non-computational necessary-and-
sufficient construction.

For the five-arc `tau=3` bow tie, the four canonical minimum cuts force three
boundary colour classes, up to permutation:

```text
Q1={a,d}, Q2={b,e}, Q3={c}.
```

For each dicut `F`, delete the five quotient arcs and call the remaining
internal arc set `R(F)`. Let `M(F)` be the colours whose `Qi` misses `F`.
Extending the boundary precolouring means assigning every internal arc at
most one colour so that every `R(F)` contains every colour in `M(F)`.

This note completely solves that extension problem when the distinct
nonempty residual sets are jointly laminar. It replaces the sufficient
private-kernel inequality by an exact recursion with only eight states per
residual set.

## Why the earlier private bound is not necessary

For a laminar residual set `R`, let its children be its maximal proper
residual subsets and let its private kernel be the elements outside those
children. Requiring the private kernel to have one fresh element for every
colour demanded at `R` is sufficient, but descendants may already provide
those colours.

For example, take a parent `{x,y}` with children `{x}` and `{y}`. If the
children demand colours 1 and 2 respectively and the parent also demands
`{1,2}`, the parent has empty private kernel but needs no fresh arc: the child
assignments already satisfy it. Thus “private-kernel deficiency” alone is not
an obstruction.

In contrast, if both singleton children demand colour 1 while the parent
demands colour 2, no colouring exists. Both elements are forced to colour 1.
The exact theorem below distinguishes these cases.

## Laminar forest and demands

Let `Omega` be a finite ground set, here the internal arcs. Let `L` be a
laminar family of nonempty subsets of `Omega`. If several dicuts have the same
residual `R`, combine their requirements as

```text
C(R)=union{M(F): R(F)=R}.                              (1)
```

Order `L` by inclusion. Its maximal sets are roots, and the maximal proper
subsets of a node `R` are its children. Children are pairwise disjoint. Put

```text
K(R)=R \ union{S: S is a child of R},  m(R)=|K(R)|.   (2)
```

The kernels over all nodes are pairwise disjoint.

## Exact eight-state recursion

For each node `R`, define `P(R)` to be the collection of subsets of
`{1,2,3}` that can occur as the **exact set of colours present in R** under a
colouring of the elements in the subtree of `R` that satisfies every demand
in that subtree. Elements may remain uncoloured.

The following bottom-up recurrence computes `P(R)` exactly. Choose one state
`S_T in P(T)` for every child `T`, and choose a set `Z subseteq {1,2,3}` with

```text
|Z| <= m(R).                                           (3)
```

Then include

```text
S = Z union union_T S_T                                (4)
```

in `P(R)` exactly when

```text
C(R) subseteq S.                                       (5)
```

Repeated copies of the same resulting state are ignored. Since there are
three colours, every `P(R)` is a subset of an eight-element state space.

### Proof of exactness

For sufficiency, realize each chosen child state recursively. The child
ground sets are disjoint. Assign one distinct element of `K(R)` to each colour
in `Z`; (3) permits this. Equations (4)--(5) give the stated presence set and
satisfy the demand at `R`.

For necessity, restrict any valid colouring to every child. Its exact colour
set belongs to that child's `P(T)` by induction. The distinct colours used on
`K(R)` form a set `Z` of size at most `m(R)`. The exact presence set is then
(4), and validity at `R` forces (5). These are all possibilities.

Thus the recurrence neither loses nor invents a colouring.

## Necessary-and-sufficient extension theorem

Assume no dicut has empty residual while missing a boundary colour. Assume
also that the distinct residual sets form a jointly laminar family `L`. Then
the forced bow-tie boundary colouring extends to three pairwise arc-disjoint
dijoins if and only if

```text
P(R) is nonempty for every root R of the laminar forest. (6)
```

If (6) holds, choose a state at each root and follow the stored recurrence
witnesses downward. The resulting disjoint internal colour classes, united
with `Q1,Q2,Q3`, meet every dicut by (1) and (5). Conversely, any three-dijoin
extension restricts to a state in every root by the necessity half above.

An exact obstruction certificate is therefore a node `R` for which `P(R)` is
empty. Choose an inclusion-minimal such node, so all child state sets are
nonempty. Then, equivalently, for every choice of feasible child states,

```text
|C(R) \ union_T S_T| > m(R):                           (7)
```

too many still-missing colours compete for the private elements of `R`.
This is the corrected form of private-kernel deficiency: it charges only
colours not already supplied below.

The proof is a finite induction, not a computational search or bounded
census. “Eight-state” describes the theorem's fixed combinatorial state
space; no instance enumeration is used.

## Crossing residuals remain a genuine separate branch

Shore uncrossing does not imply residual laminarity. The exact `tau=3`
fixture with internal arcs

```text
f:z->w, g:z->B, h:z->B, i:w->B
```

inside the bow-tie `B` region has nested dicut shores `{z}` and `{z,w}` but
crossing colour-1 residuals `{f,g,h}` and `{g,h,i}`. Its ten dicuts have sizes
three or six: incoming-closedness says `C` requires `A`, `w` requires `z`,
`B` requires `A,z,w`, and `E` requires `A,B,C`, which gives the ten shores by
direct case separation. The colouring

```text
colour 1: a,d,f,i
colour 2: b,e,g
colour 3: c,h
```

is rainbow on all of them. Hence crossing residuals can be harmless, but they
fall outside the laminar recursion and cannot be silently uncrossed as arc
sets.

After this theorem, a bow-tie obstruction has only two honest forms:

1. an empty residual demand or a crossing residual family; or
2. in the jointly laminar branch, an explicit empty-state certificate (7).

Mere private-kernel deficiency has been eliminated as a false positive.

## Mandatory filters

1. **Schrijver filter.** The state construction is unit-capacity: one internal
   arc receives at most one of three colours, and `m(R)` counts distinct usable
   arcs. Weighted cut values and zero-weight arcs do not imply these colour
   slots. No weighted Edmonds--Giles conclusion is drawn.
2. **Lucchesi--Younger filter.** No cut/dijoin duality is invoked. The proof
   expands the definition “each colour meets every dicut” and constructs the
   colour classes directly.
3. **Easy-direction filter.** When (6) holds, recurrence witnesses explicitly
   build three disjoint dijoins. The theorem is an iff characterization, not
   the trivial upper bound on their number.
