# Rational witness near the symmetric KKT point

**Status:** `sketch`, verification-critical. The support-envelope statement is
exact; its convex-area interpretation remains conditional on the separately
reviewed finite-polygon mixed-area/common-fan bridge.

The three-well first-variation system numerically predicts an interior
maximin point near

```text
(t_alpha,t_beta,p)=(0.01886026338,0.80050851850,0.34141264635).
```

Here the endpoint, `A=C`, and `S=B` wells equioscillate, and finite-difference
gradients admit positive KKT weights approximately
`(0.49085,0.43742,0.07173)`. This stationarity calculation remains numerical.

The nearby exact rational parameters

```text
t_alpha=929/49257, t_beta=43133/53882, p=7381/21619,
q=1/2-p
```

define a rational unit open four-edge worm. A self-contained exact
`Q(sqrt(3))` checker reconstructs winding-one hull geometry, all maximal
balanced allocations and residuals, every triangle support-switch minimum,
four projection-sign cells, concavity, strict endpoints, and the complete
direct-motion mirror. It proves

```text
support envelope > 23518745713/100000000000 = 0.23518745713.
```

This strictly improves PR #191's `0.23518` certificate without modifying or
assuming that frozen PR.

Replay:

```text
python problems/moser-convex-worm/attacks/symmetric-kkt-rational/certify.py
python -O problems/moser-convex-worm/attacks/symmetric-kkt-rational/certify.py
```
