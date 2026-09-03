# Symmetric four-edge first variation and rational improvement

**Status:** exact support-envelope certificate `sketch`; optimizer analysis
`numerical`.  The area interpretation remains conditional on the
finite-polygon mixed-area/common-fan bridge.  Nothing here is assumable until
cross-family review approves that dependency and this certificate.

The frozen Issue #178 parameters are not locally optimal even within the
three-parameter symmetric family.  Write the edge half-angle parameters as

```text
-t_beta, -t_alpha, t_alpha, t_beta
```

and their lengths as `p,1/2-p,1/2-p,p`.  The exploratory script recomputes all
maximal balanced allocations and triangle-orientation floors at every point.
It identifies three active angular wells:

1. the endpoint `phi=0`;
2. the outer `A=C` crossing;
3. the central `S=B` crossing.

At an interior maximin stationary point their three values equioscillate.  If
their gradients are `g0,g1,g2`, nonsmooth first-order stationarity requires
nonnegative weights with

```text
lambda0*g0+lambda1*g1+lambda2*g2=0,
lambda0+lambda1+lambda2=1.
```

Solving the two equioscillation equations together with
`det(g0,g1,g2)=0` numerically gives

```text
t_alpha = 0.01886026338...
t_beta  = 0.80050851850...
p       = 0.34141264635...
floor   = 0.23518745715...
```

with positive approximate KKT weights `(0.49085,0.43742,0.07173)`.  This is
numerical evidence for stationarity, not a local-optimality proof.

## Exact nearby witness

A deliberately simpler rational point is

```text
t_alpha=1/53, t_beta=313/391,
p=169/495, q=157/990.
```

The four positive lengths `p,q,q,p` sum exactly to one, and the rational
half-angle map gives four exact unit directions.  The exact checker proves
strict convex winding-one hull order, closure, every allocation capacity,
allocated and residual balance, and all triangle support minima.

The full direct-motion support envelope is covered analytically by `C,A,S,B`
on the half-angle intervals cut at

```text
0, 4487/20000, 1/3, 74597/100000, 1.
```

Every residual projection sign is checked at both ends of its cell.  Each
resulting formula has nonnegative sine/cosine coefficients, hence is concave,
and both exact endpoints strictly exceed

```text
11759/50000 = 0.23518.
```

The surface/allocation involution covers the second half-turn without
reflecting the worm, and the mirrored triangle floor is recomputed exactly.
Thus this is a strict exact support-envelope improvement over the frozen
Issue #178 and PR #186 witnesses, subject to the same bridge limitation.

Replay:

```text
python problems/moser-convex-worm/attacks/four-edge-stationarity/certify_rational_improvement.py
python -O problems/moser-convex-worm/attacks/four-edge-stationarity/certify_rational_improvement.py
python problems/moser-convex-worm/attacks/four-edge-stationarity/explore_symmetric.py
```
