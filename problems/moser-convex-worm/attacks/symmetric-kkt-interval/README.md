# Exact isolation of the symmetric-family KKT point

This attack turns the numerical stationary point from issue #196 into an
exact-rational interval theorem.  Run

```sh
python problems/moser-convex-worm/attacks/symmetric-kkt-interval/certify_kkt.py
python -O problems/moser-convex-worm/attacks/symmetric-kkt-interval/certify_kkt.py
```

The second invocation matters: every check uses explicit exceptions, not
`assert`.

## Statement certified

Let `a=tan(alpha/2)`, `b=tan(beta/2)`, and let `p` be the length of each of
the two equal inner edges (`q=1/2-p` is the length of each outer edge).  For
the three closed-form support wells `E,O,M` derived in issue #196 and PR #199,
form the five KKT equations

```text
E-O = 0,   E-M = 0,
lambda_E grad E + lambda_O grad O + lambda_M grad M = 0,
lambda_M = 1-lambda_E-lambda_O.
```

There is exactly one solution in the printed rational box.  At that solution
all three multipliers are positive, and

```text
0.23518745713 < E=O=M < 0.23518745716.
```

The box is approximately centered at

```text
(a,b,p) = (0.018860263338563645,
           0.80050851848913696,
           0.34141264634940915),
(lambda_E,lambda_O,lambda_M)
        = (0.4908466867025911,
           0.4374218430906998,
           0.0717314702067091).
```

In addition, the gradients of `E-O` and `E-M` are independent throughout
the box.  Their cross product `t` spans the common tangent, and exact interval
arithmetic proves

```text
t^T (lambda_E Hess(E) + lambda_O Hess(O) + lambda_M Hess(M)) t
  in [-0.001422686805015533, -0.001422686805009242].
```

The positive multipliers and negative reduced Hessian give the standard
second-order sufficient condition for a strict local maximum of
`min(E,O,M)`.  Since the full support-envelope floor is at most each of these
three wells, this is also a certified local upper bound for the full floor in
the symmetric three-parameter family.  It is not a global-optimality claim.

## Certificate method

`certify_kkt.py` uses only Python integers and `fractions.Fraction`.  Square
roots receive outward rational enclosures constructed with integer square
root.  A second-order automatic-differentiation type evaluates every well,
gradient, and Hessian over intervals.

For a rational box `X`, midpoint `x0`, and exact inverse `C` of the midpoint
Jacobian, the program evaluates

```text
K(X) = x0 - C F(x0) + (I - C F'(X))(X-x0).
```

It checks `K(X)` is strictly inside `X`, which proves existence and uniqueness
of a zero in `X` by the Krawczyk theorem.  It then checks multiplier signs,
the value enclosure, constraint-gradient independence, and strict negativity
of the reduced weighted Hessian.  All displayed decimals are merely readable
renderings; the decisions themselves compare exact rational endpoints.

## Scope and status

This certificate concerns the reduced symmetric family and the three selected
support wells.  It does not establish that this family contains a global
optimizer for the unrestricted Moser worm problem, nor does it improve the
status of the mixed-area bridge.  The script is the producer's checker and
requires independent review under the problem rules.
