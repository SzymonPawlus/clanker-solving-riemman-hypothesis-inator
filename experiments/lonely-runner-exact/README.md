# Exact fixed-vector Lonely Runner checker

This directory implements a clean-room, exact decision procedure for one
integer velocity vector `(v_1, ..., v_k)`. It decides whether there is a time

```
t in [0, 1)  with  ||t v_i|| >= 1/(k+1)  for every i,
```

where `||x||` is distance to the nearest integer. The implementation uses only
Python standard-library arbitrary-precision integers and `fractions.Fraction`;
there is no floating-point arithmetic or numerical tolerance.

## Method

Put `delta = 1/(k+1)`. For a nonzero velocity of absolute value `m`, the
allowed times are exactly the closed intervals

```
[(j + delta)/m, (j + 1 - delta)/m],  j = 0, ..., m-1.
```

This follows by writing `j <= m t <= j+1` on each period and imposing
`delta <= m t-j <= 1-delta`. Sign does not matter because `||-x|| = ||x||`.
The checker intersects these finite unions using exact rational comparisons.
Endpoint equality is retained, because the requested inequality is non-strict.
A zero velocity has no allowed time (the target separation is positive).

The output intervals themselves are a directly inspectable certificate. The
first left endpoint is returned as a canonical witness.

## Run

From this directory:

```
python3 lonely_runner_exact.py 1 2 3
python3 -m unittest -v test_lonely_runner_exact.py
```

The tests cover closed endpoint contact, zero velocity, sign and permutation
invariance, positive gcd scaling, hand-derived small cases, and a deterministic
random cross-check that independently samples every boundary and every cell
between consecutive boundaries.

## Scope and non-claim

This tool decides the stated question for each supplied finite vector only.
Checking any finite list of velocity vectors does **not** prove the universal
Lonely Runner conjecture unless it is paired with a proved finite-reduction
theorem covering all remaining vectors. No such reduction is established here.
Likewise, a purported counterexample should not be claimed from this tool alone:
issue #299 requires confirmation by a second independent implementation.
