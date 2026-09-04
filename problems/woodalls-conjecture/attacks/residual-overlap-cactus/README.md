# Exact state theorem for forest and cactus residual overlaps

**Issue:** #241. **Status:** `sketch`; non-computational compatibility
theorem.

After the five bow-tie arcs receive their forced three colours, every dicut
produces an internal residual set `R` and a set `C(R) subseteq {1,2,3}` of
colours still required in `R`. The task is to colour each internal arc at most
once so every residual contains all its demanded colours.

This note solves that task exactly for linear families with a forest overlap
graph, and extends the construction to cactus overlap graphs. “Linear” means
that an internal arc lies in at most two distinct residual sets. This makes
the intersection atoms honest disjoint capacity resources rather than hidden
three-way identifications.

## Atom decomposition

Index the distinct residual demands by vertices `v` and write them as
`(R_v,C_v)`. Let `H` be their overlap graph: `uv` is an edge exactly when
`R_u intersection R_v` is nonempty. Put

```text
I_uv=R_u intersection R_v,  s_uv=|I_uv|,
K_v=R_v \ union_{uv in E(H)} I_uv,  k_v=|K_v|.         (1)
```

Linearity implies that all edge atoms `I_uv` and private atoms `K_v` are
pairwise disjoint. They partition the union of the residual sets.

For an atom containing `m` arcs, its exact **presence state** can be any
`X subseteq {1,2,3}` with `|X|<=m`: put its distinct colours on distinct arcs
and leave the rest uncoloured.

## Global atom criterion

The residual system is colourable if and only if there are states `X_uv` for
the edge atoms and `Z_v` for the private atoms such that

```text
|X_uv|<=s_uv, |Z_v|<=k_v,
C_v subseteq Z_v union union_{uv in E(H)} X_uv          (2)
```

for every vertex `v`.

Necessity follows by recording the colours actually present on each disjoint
atom. For sufficiency, realize every state on distinct arcs of its atom.
Disjointness prevents colour conflicts, and (2) meets every demand. This
criterion is exact for any linear overlap graph; the forest/cactus hypotheses
make it recursively constructive with constant-size messages.

## Forest: eight-state messages

Suppose `H` is a forest and root each component. For an oriented tree edge
`vp`, define `M_{v->p}` to be the states `X subseteq {1,2,3}` that can be
placed on `I_vp` while satisfying every demand in the component below `v`.

The exact bottom-up recurrence is

```text
X in M_{v->p}
iff |X|<=s_vp and there exist
    Z subseteq {1,2,3}, |Z|<=k_v,
    Y_w in M_{w->v} for every child w,
such that C_v subseteq X union Z union union_w Y_w.     (3)
```

A root `r` is feasible when the same condition holds without the parent state
`X`. The whole forest is feasible exactly when every root is feasible.

Proof is induction from the leaves. Restricting a colouring gives the states
in (3); conversely, recurrence witnesses colour pairwise disjoint atoms and
child subtrees. Every message is a subset of an eight-element state space,
independent of the number of residual demands.

An inclusion-minimal vertex with an empty outgoing message is an exact local
obstruction certificate: every combination of feasible child states leaves
more distinct colours of `C_v` unsupplied than `K_v` and the parent atom can
jointly carry.

## Cactus: cycle-block transfer

Suppose `H` is a cactus, so every edge lies in at most one cycle. Its block-cut
incidence graph is a tree whose blocks are bridges or simple cycles. Process
that tree from its leaves.

- A bridge block sends exactly the message (3).
- For a cycle block, fix a state on the adhesion to its parent articulation.
  Enumerate the eight possible presence states on each cycle edge in cyclic
  order. At each non-parent cycle vertex retain exactly those consecutive edge
  states which, together with its private state and already processed child-
  block messages, cover `C_v`. Closing the cycle tests the final pair at the
  parent articulation and records the exact colour subset contributed there.

This is a transfer relation on pairs of eight states, not a graph-size search.
Necessity comes from restricting a valid atom colouring around the cycle;
sufficiency comes from realizing the retained disjoint edge/private atoms.
Induction over the block-cut tree is therefore an exact necessary-and-
sufficient construction for every linear cactus residual family.

Equivalently, failure is witnessed by the first bridge message or cycle
transfer relation that becomes empty. No uncrossing of residual arc sets is
assumed.

## Natural capacity condition guaranteeing feasibility

The exact recurrences have a useful direct corollary. Call an overlap edge
**full** when `s_uv>=3`. Assume every demand-bearing vertex `v` satisfies at
least one of

```text
k_v>=|C_v|, or v is incident with a full overlap edge.  (4)
```

Then the system is feasible, for a forest, cactus, or indeed any linear
overlap graph.

Colour every full edge atom with all three colours. Every incident vertex now
has all possible demands supplied. At each remaining demand-bearing vertex,
use `|C_v|` distinct private arcs, permitted by (4). All chosen atoms are
disjoint, so these assignments coexist. This gives three explicit internal
colour classes and hence, after adjoining the forced bow-tie classes, three
arc-disjoint dijoins.

At `tau=3`, every demand set has at most three colours, and a residual missing
all three boundary colours is itself a dicut and therefore has at least three
arcs. Condition (4) identifies where that total capacity must sit to make
multiple crossings harmless: either privately at the demand or in a shared
three-slot atom.

## Sharpness of total-size reasoning

Knowing only `|R_v|>=|C_v|` does not suffice, even for a linear overlap tree.
Let a centre residual be `{x,y}`, with leaf residuals `{x}` and `{y}`. Demand
colour 2 at the centre and colour 1 at both leaves. Every residual has at least
as many arcs as demanded colours, but the leaf constraints force both `x,y`
to colour 1, leaving no representative of colour 2 at the centre. Recurrence
(3) returns an empty root state and detects the obstruction exactly.

Thus a proof based only on `tau=3` cut sizes cannot settle multiple crossing
demands. It must either establish a capacity placement such as (4), or rule
out the explicit empty-message patterns by directed-shore structure.

## Mandatory filters

1. **Schrijver filter.** Every state capacity counts distinct unit arcs, each
   usable in at most one colour. Weighted cut values and zero-weight arcs do
   not provide these one-use atom slots. No weighted Edmonds--Giles conclusion
   is claimed.
2. **Lucchesi--Younger filter.** No dicut/dijoin min-max theorem is used. The
   state witnesses directly assign arcs so every demanded colour meets every
   residual dicut.
3. **Easy-direction filter.** Feasible messages reconstruct three explicit
   colour classes, which become three disjoint dijoins after the forced
   boundary arcs are restored. The theorem is necessary and sufficient, not
   the trivial packing upper bound.
