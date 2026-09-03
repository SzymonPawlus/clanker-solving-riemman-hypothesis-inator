# Bow-tie residual demands are not laminar; a corrected extension theorem

**Issue:** #228. **Status:** `sketch`; non-computational refutation and
constructive special case.

The five-arc bow tie forces boundary colour classes

```text
Q1={a,d}, Q2={b,e}, Q3={c},
```

where the quotient arcs are `a:A->B,b:A->C,c:A->E,d:B->E,e:C->E`.
For a dicut `F`, colour `i` still needs an internal representative exactly
when `F intersection Qi` is empty. Its **residual demand** is
`F\{a,b,c,d,e}`.

This note answers two questions. First, ordinary dicut uncrossing does not
make these residual arc families laminar, even at `tau=3`. Second, joint
laminarity plus an explicit private-slack condition does suffice and gives a
direct construction of all three dijoins.

## Exact non-laminar `tau=3` fixture

Take singleton quotient regions `A,C,E`. Replace `B` by vertices `z,w,B` and
add internal arcs

```text
f:z->w, g:z->B, h:z->B, i:w->B,
```

where `g,h` are parallel. Together with the five bow-tie arcs, this is a DAG.
Its complete nonempty incoming-closed shores fall into the following cases:

```text
z absent:       {A}, {A,C};
A absent:       {z}, {z,w};
A,z present,
  w absent:     {A,z}, {A,C,z};
A,z,w present: {A,z,w}, {A,B,z,w},
                {A,C,z,w}, {A,B,C,z,w}.
```

There are no others: `C` requires `A`; `w` requires `z`; `B` requires
`A,z,w`; and `E` requires `A,B,C`, which gives the full shore once `z,w` are
also present. Direct boundary counting gives sizes, in the displayed order,

```text
3,3; 3,3; 6,6; 6,3,6,3.
```

Thus `tau=3` without an exhaustive computer claim.

For colour 1, the shores `{z}` and `{z,w}` avoid `Q1={a,d}` and have residual
demands

```text
R ={f,g,h},
R'={g,h,i}.
```

They cross as sets: their intersection is `{g,h}` and their two differences
are `{f}` and `{i}`. Hence even one colour's residual demand family need not
be laminar. The failure comes from deleting different forced quotient arcs
after shore uncrossing; cut modularity is not inherited by that deletion.

This crossing is not itself an obstruction. The exact arc colouring

```text
colour 1: a,d,f,i
colour 2: b,e,g
colour 3: c,h
```

makes every one of the ten listed cuts rainbow. It explicitly gives three
pairwise arc-disjoint dijoins. The fixture therefore refutes the proposed
laminarity lemma, not Woodall's conjecture.

## A corrected joint-laminar theorem

Here is a sufficient condition that does survive. Let `Omega` be the internal
arcs and let `L` be the set of distinct nonempty residual demands. For each
`R in L`, let

```text
C(R)={i: some dicut with residual R misses boundary colour i}.
```

Assume `L` is **jointly laminar**: any two members are nested or disjoint. For
`R in L`, let `child(R)` be its maximal proper members in `L`, and define its
private kernel

```text
K(R)=R \ union{S: S in child(R)}.                       (1)
```

**Private-slack theorem.** If

```text
|K(R)| >= |C(R)|                                       (2)
```

for every `R`, then the forced bow-tie boundary colouring extends to three
pairwise arc-disjoint dijoins.

Proof. The kernels `K(R)` are pairwise disjoint. For incomparable nodes this
follows from laminarity. If `S` is properly below `R`, then `S` lies in a
child of `R`, so it misses `K(R)`. For each node independently, choose
`|C(R)|` distinct arcs of `K(R)` and assign one to each colour in `C(R)`;
condition (2) permits this, and disjoint kernels prevent colour conflicts.

Now take any dicut `F`. If forced boundary class `Qi` meets it, colour `i` is
already present. Otherwise its residual `R` has `i in C(R)`, and the arc
chosen for `(R,i)` lies in `K(R) subseteq R subseteq F`. Thus every dicut
contains every colour. The three colour classes are the required disjoint
dijoins. QED

Empty residual demands are excluded deliberately: an empty residual that
misses a forced boundary colour is an immediate certificate that the fixed
boundary precolouring cannot extend. Condition (2) is sufficient, not
necessary; a colour already supplied inside a child can also satisfy a parent
demand. Its virtue is that it is local, exact, and constructive.

## Why laminarity alone is insufficient

Even abstractly, a laminar residual family does not solve the disjoint-colour
problem. A singleton residual `{x}` demanded by both colours 1 and 2 is
laminar, but its only arc cannot receive two colours. More generally, nested
nodes can consume all representatives needed by their ancestors. Condition
(2) records precisely the private capacity that the naive laminar argument
omits.

Therefore a bow-tie counterexample escaping this theorem must exhibit at
least one of the following exact obstructions:

1. an empty residual demand;
2. crossing residual sets (which can occur already at `tau=3`, as above); or
3. a laminar node whose private kernel is smaller than its demanded colour
   set.

This trichotomy is a corrected target for further uncrossing: shore
laminarity by itself is not enough, but proving joint residual laminarity and
private slack would exclude the bow tie.

## Mandatory filters

1. **Schrijver filter.** Unit capacities are essential twice: the five
   boundary arcs have forced single colours, and each private internal arc can
   be assigned to at most one dijoin. With weighted or zero-weight arcs,
   cardinality (2) is not the relevant capacity condition. No weighted
   Edmonds--Giles theorem is inferred.
2. **Lucchesi--Younger filter.** No min-max equality or dicut/dijoin role
   reversal is used. Every colour is checked directly against an arbitrary
   dicut.
3. **Easy-direction filter.** The theorem explicitly assigns internal arcs
   and constructs three disjoint dijoins. The fixture likewise lists a
   concrete three-colouring; neither argument merely bounds the packing from
   above.
