# Independent exact affine floor-chamber decisions through slope 24

Status: `numerical`. This is an exhaustive bounded family, not an
unbounded exclusion of affine templates or eight-row covers. Helper used
only the mathematical specification supplied by the prover; no author
solver or checker was read, imported, or translated.

For every nonzero integer `a` with `|a|<=24`, let `b=-floor(a x)`. Partition
`0<x<1` at all reduced rational cuts `k/n`, `1<=n<=24`, `0<=k<=n`.
There are exactly 180 open chambers. The 48 pairs `(a,b)` are constant
in each chamber and satisfy `0<a x+b<1`. An exact rational midpoint
represents each chamber. If a selected collection is valid at a cut, none
of its own `a x` is integral, so its floors persist in a neighboring
chamber. Thus valid boundary choices introduce no missing selected sets.

The stronger question is whether at most eight pairs from one chamber
have strict bad sets

```
||a z+b/15||<1/15
```

covering every open circle cell. All endpoints are the exact rationals
`(15k-b+/-1)/(15a) mod 1`; each open cell is represented by its exact
midpoint. This question deliberately leaves individual endpoints free.
The original weaker scan also required at least one chosen row to be bad
at some `ell/15`; its negative result is preserved separately.

## Exact decision and sound pruning

The full finite universe consists of all open cells between endpoints
from all 48 possible rows. A row's literal rational test is constant on
each cell. A recursive state contains only the uncovered cell bitset and
remaining row budget. The complete original row universe is available at
every state. Branching on an uncovered cell tries every row containing
that cell, so every completion has a represented branch. A previously
selected row has zero residual gain and cannot be selected again.

Failed-state memoization uses only `(residual, remaining)`. There are no
history-dependent private-residue constraints or sibling row exclusions.
The sum of the largest `r` row gains bounds how many cells `r` rows can
cover. Separately, every nonzero integer-frequency bad row has measure
exactly `2/15`: if remaining cell lengths total more than `2r/15`, no
completion exists. Cell lengths and this comparison use a common exact
integer denominator. Both pruning implications are independent of the
chosen prefix and so are compatible with the memo key.

`helper_affine_open_chambers.py` completes all 180 stronger decisions in
1,460 visited states, finding no cover and leaving no unfinished chamber.
Its hash-bound report is `helper-affine-K24-open-chambers.json`.
`helper_affine_chamber_decision.py` preserves the earlier eligibility-bit
version: all 180 decisions complete, 1,480 visited states, no cover;
report `helper-affine-K24-chambers.json`. These scripts derive independently
from the same helper implementation, not two independent implementations.

Positive and negative exact circle fixtures are included. The positive
eight-row fixture covers all open cells while leaving several endpoints
safe, so the cell-only condition is not silently strengthened to a
closed-circle cover. No common floor chamber is claimed for that fixture.

The motivation is the fourteen-moving/fifteen-total problem. Each decision
uses one common phase, every bad inequality is strict, equality is safe,
and no coordinate is scaled separately. The finite results exclude only
the stated 48-row universes and cannot be inferred beyond `|a|<=24`.

```
python3 helper_affine_open_chambers.py --K 24 --seconds 3 --output helper-affine-K24-open-chambers.json
```
