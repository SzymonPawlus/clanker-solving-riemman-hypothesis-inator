# The first crossing residual module is always feasible at `tau=3`

**Issue:** #236. **Status:** `sketch`; non-computational compatibility
theorem.

In the five-arc bow tie, write the forced boundary colour classes as

```text
Q1={a,d}, Q2={b,e}, Q3={c}.
```

A dicut `F` has residual `R(F)=F\{a,b,c,d,e}` and demands precisely the
colours

```text
M(F)={j: F intersection Qj is empty}.                  (1)
```

This note solves the first nonlaminar case: two residual demands that cross.
Two bare crossing demands are always compatible when `tau=3`. With laminar
descendant demands attached inside their atoms, an exact finite-state module
gives the necessary-and-sufficient remaining obstruction.

## Exact two-set criterion

Let `R,S` be two crossing subsets of an internal arc ground set. Put

```text
I=R intersection S, P=R\S, Q=S\R,
i=|I|, p=|P|, q=|Q|.                                  (2)
```

All three sizes are positive. Let `A,B subseteq {1,2,3}` be the colours
demanded by `R,S` respectively. We seek a colouring of `R union S`, with each
arc receiving at most one colour, such that `R` contains every colour of `A`
and `S` every colour of `B`.

**Two-set criterion.** Such a colouring exists if and only if there is a set
`X subseteq {1,2,3}` satisfying

```text
|X|<=i, |A\X|<=p, |B\X|<=q.                           (3)
```

Necessity: take `X` to be the distinct colours actually used on the
intersection atom. Every colour of `A\X` needs a distinct arc of `P`, and
every colour of `B\X` a distinct arc of `Q`.

Sufficiency: put the colours of `X` on distinct arcs of `I`, those of `A\X`
on distinct arcs of `P`, and those of `B\X` on distinct arcs of `Q`. The
atoms are disjoint, so this is a valid colouring.

The condition has an equivalent scalar form. Define

```text
d_A=max(0,|A|-p), d_B=max(0,|B|-q), h=|A intersection B|.
```

At least `d_A` colours of `A` and `d_B` colours of `B` must use `I`. The
minimum possible number of distinct intersection colours is

```text
m=max(d_A,d_B,d_A+d_B-h).                              (4)
```

The third term accounts for the fact that at most `h` required colours can
serve both demands. Choosing common colours first attains (4). Hence (3) is
equivalent to `i>=m`.

## `tau=3` forces feasibility for a bare crossing pair

Now let `R=R(F),S=R(G)` come from two bow-tie dicuts, and set
`A=M(F),B=M(G)`. Then

```text
|R|>=|A| and |S|>=|B|.                                (5)
```

Indeed, crossing gives `|R|,|S|>=2`, which proves (5) when the demanded set
has at most two colours. If all three colours are demanded, the dicut contains
no quotient arc at all, so its residual is the whole dicut and has size at
least `tau=3`.

Equation (5) gives `d_A<=i` and `d_B<=i`. It remains to bound the third term
in (4). If one deficit is zero, it is bounded by the other. If both are
positive, `p,q>=1` gives

```text
d_A+d_B-h <= (|A|-1)+(|B|-1)-h
            = |A union B|-2 <= 1 <= i.                (6)
```

Thus `i>=m`, and the exact criterion constructs a compatible colouring.

> Two crossing residual demands, by themselves, can never obstruct the
> forced bow-tie colouring at `tau=3`.

This eliminates crossing as a bare local obstruction. Any failure needs
additional demands that constrain how colours may be supplied inside the
three atoms.

## Exact module with laminar descendants

Suppose all other residual demands below `R,S` lie wholly inside one of the
three atoms `I,P,Q`, and within each atom form a laminar system. For an atom
`T`, let `Sigma_T subseteq 2^{\{1,2,3\}}` be the exact feasible colour-presence
states after satisfying all descendant demands in `T`. These state sets are
obtained by the standard bottom-up laminar recurrence: combine disjoint child
states with colours placed on private elements and retain precisely the states
meeting the node's demand.

The crossing module's exact state set is

```text
Sigma_cross = {
  X union Y union Z:
  X in Sigma_I, Y in Sigma_P, Z in Sigma_Q,
  A subseteq X union Y,
  B subseteq X union Z
}.                                                       (7)
```

Formula (7) is necessary because any colouring restricts to one feasible
state on each disjoint atom. It is sufficient because three atom colourings
realizing the chosen states have disjoint ground sets and unite to meet both
crossing demands. There are at most `8^3=512` state triples, a fixed theorem
independent of graph size.

If every residual set outside the module is either disjoint from `R union S`
or contains `R union S`, replace the crossing pair by one virtual node with
state set `Sigma_cross`. The remaining inclusion forest is laminar, so the
ordinary eight-state recurrence above the module is again exact. Therefore a
residual family with precisely one crossing pair has a complete necessary-
and-sufficient finite-state construction.

An irreducible obstruction is now explicit: `Sigma_cross` is empty, or an
ancestor's state set becomes empty after the module is substituted. The bare
`tau=3` theorem proves that emptiness cannot arise merely from the two labels
`A,B` and the atom cardinalities; it must be forced by descendant state
restrictions.

## Check against the first nonlaminar fixture

The nested-shore fixture has crossing colour-1 residuals

```text
R={f,g,h}, S={g,h,i}.
```

Here `I={g,h}`, `P={f}`, `Q={i}`, and `A=B={1}`. Thus both deficits in (4)
are zero, and the criterion is feasible without using an intersection arc for
colour 1; assigning colour 1 to `f,i` is exactly the explicit packing found
there. The example remains a valid refutation of naive residual laminarity,
but it is correctly accepted by the crossing module.

## Mandatory filters

1. **Schrijver filter.** The proof uses three unit-capacity colour slots and
   counts distinct arcs in `I,P,Q`. A weighted cut value does not supply these
   one-use representatives, and zero-weight arcs break (5). No weighted
   Edmonds--Giles theorem follows.
2. **Lucchesi--Younger filter.** No cut/dijoin min-max theorem is used. The
   criterion directly colours arcs so every demanded colour hits its dicut.
3. **Easy-direction filter.** Equations (3) and (7) construct the colour
   classes. When all residual demands are accepted by the final state
   recurrence, adjoining `Q1,Q2,Q3` explicitly yields three disjoint dijoins.
