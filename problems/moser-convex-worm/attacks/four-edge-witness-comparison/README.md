# Exact comparison of two rational four-edge witnesses

**Issue:** #194. **Status:** `sketch`; exact comparison of the finite support
envelopes, conditional on the same mixed-area/common-fan bridge as the source
witnesses.

This is a clean-room comparison of the rational witnesses introduced in PRs
#191 and #192.  It does not import either producer checker.  Starting from the
balanced-load equations and the equilateral-triangle fan formula, the verifier
reconstructs the triangle constants and residual segment bounds using a new
exact `Q(sqrt(3))` implementation.

Write the symmetric directions as `(-beta,-alpha,alpha,beta)` and lengths as
`(p,q,q,p)`.  The two data sets are

| witness | `tan(beta/2)` | `tan(alpha/2)` | `p` | `q` |
|---|---:|---:|---:|---:|
| PR #191 | `313/391` | `1/53` | `169/495` | `157/990` |
| PR #192 | `19999/25000` | `3/200` | `683/2000` | `317/2000` |

## Strict result

For the PR #191 data, let `C,A,S,B` be respectively the inner circuit, crossed
circuit, zero allocation (all segment), and outer circuit.  In the direct
first-quadrant coordinate `u=tan(phi/2)`, use

```text
C: [0,4487/20000]
A: [4487/20000,1/3]
S: [1/3,74597/100000]
B: [74597/100000,1].
```

For every row, the exact checker proves that no nonzero residual crosses a
projection wall in the interval.  The row's bound is therefore

`tau + A sin(phi) + B cos(phi)`

with nonnegative residual widths, hence is concave.  It also proves at both
endpoints, in exact `Q(sqrt(3))` arithmetic, that the value is strictly above

```text
117593/500000 = 0.235186.                         (1)
```

The direction/length reversal involution gives the other half-turn by direct
rotation, without identifying a reflection.  Thus the four-bound envelope for
the PR #191 witness has global floor strictly above (1).

For the PR #192 data, exact evaluation at `phi=0` shows that `C` is the largest
of the same four bounds and that its value is strictly below (1).  Consequently
the minimum of that four-bound envelope is below (1).  Combining the two sides
gives the strict comparison

```text
floor(PR #191 finite envelope) > 0.235186
                                > floor(PR #192 finite envelope).
```

This comparison concerns the displayed finite allocation envelopes.  It does
not claim that no larger envelope could be obtained by adding coupled balanced
allocations, and it does not upgrade the conditional universal-cover status.

Replay with and without assertions:

```text
python problems/moser-convex-worm/attacks/four-edge-witness-comparison/verify_strict_comparison.py
python -O problems/moser-convex-worm/attacks/four-edge-witness-comparison/verify_strict_comparison.py
```

`explore.py` is non-rigorous reconnaissance only.  It reconstructs the fan
minimum directly and samples the resulting envelopes; it is not used by the
proof.
