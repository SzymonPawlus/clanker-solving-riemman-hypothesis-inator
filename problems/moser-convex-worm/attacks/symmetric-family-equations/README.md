# Exact active-well equations for symmetric four-edge worms

**Status:** `sketch`. This is a family-level analytic reduction, not a proof
of global or local optimality. Its support-to-area interpretation has the same
unresolved mixed-area/common-fan dependency as the existing certificates.

Let the four edge directions have angles `-beta,-alpha,alpha,beta`, let their
lengths be `p,q,q,p`, and impose `p+q=1/2`. Write

```text
ca=cos(alpha), sa=sin(alpha), cb=cos(beta), sb=sin(beta).
```

In the open regime `0<alpha<beta<pi/2`, with the same four maximal balanced
allocations as the certified rational witnesses, the three empirically active
wells have the following exact form.

## Triangle floors and support formulas

Direct balance and exhaustive triangle support-switch comparison give

```text
qC = q*ca*sqrt(3)/4,
qA = q*(sa+ca*sqrt(3))/8,
qB = p*sb/4.
```

On the relevant first-quadrant sign cells,

```text
C(phi) = qC + (p*cb/2) sin(phi) + (p*sb/2) cos(phi),

A(phi) = qA
       + [p*cb/2 + q*ca/2 - q*sa*cb/(2*sb)] sin(phi)
       + (p*sb/2) cos(phi),

S(phi) = (p*cb/2+q*ca) sin(phi) + (p*sb/2) cos(phi),

B(phi) = qB + q*ca sin(phi).
```

These identities explain two cancellations that were obscured in the
instance-specific fractions.

## Three algebraic wells

The endpoint well is

```text
E = C(0) = q*ca*sqrt(3)/4 + p*sb/2.
```

The `A=C` cosine terms cancel. Its unique crossing has

```text
yo := sin(phi_o)
    = sb*(ca*sqrt(3)-sa)/(4*sin(beta-alpha)),
zo := sqrt(1-yo^2),
O  := q*ca*sqrt(3)/4 + (p/2)*(cb*yo+sb*zo).
```

Thus the outer crossing angle depends only on `alpha,beta`, not on `p,q`.

Likewise

```text
S(phi)-B(phi)
 = (p/2)*(cb sin(phi)+sb cos(phi)-sb/2).
```

The central crossing is independent of `alpha,p,q`. In half-angle coordinate
`u=tan(phi_c/2)`, it is the positive root

```text
3*sb*u^2 - 4*cb*u - sb = 0,
u = (2*cb+sqrt(3+cb^2))/(3*sb).
```

With `yc=2u/(1+u^2)`, the central well is

```text
M = p*sb/4 + q*ca*yc.
```

Evaluation at these three angles gives the unconditional family upper bound

```text
envelope_floor(alpha,beta,p) <= min(E,O,M)
```

whenever the displayed allocations remain legal. If the four concavity cells
are also endpoint-dominated as in the certified neighborhood, equality holds.

## Stationarity system

At a smooth interior maximin optimum with precisely these three active wells,

```text
E=O=M.
```

Let `gE,gO,gM` be their gradients with respect to any nonsingular parameter
chart, for example rational half-angles `(ta,tb,p)`. Nonsmooth first-order
stationarity is exactly the existence of

```text
lambdaE,lambdaO,lambdaM >= 0,
lambdaE+lambdaO+lambdaM=1,
lambdaE*gE+lambdaO*gO+lambdaM*gM=0.
```

Equivalently, in three variables,

```text
det(gE,gO,gM)=0
```

together with the two equioscillation equations, followed by the positivity
check on the normalized null vector. Introducing variables `yo,zo,u` and the
relations

```text
yo^2+zo^2=1,
4*sin(beta-alpha)*yo=sb*(ca*sqrt(3)-sa),
3*sb*u^2-4*cb*u-sb=0
```

makes the complete system algebraic over `Q(sqrt(3))`; the half-angle formulas
make `ca,sa,cb,sb` rational functions. This is the appropriate system for an
exact resultant or interval-Newton isolation.

Numerical isolation currently gives

```text
ta in (0.01886026337,0.01886026340),
tb in (0.80050851848,0.80050851852),
p  in (0.34141264633,0.34141264637),
L  in (0.23518745714,0.23518745716),
```

with positive approximate multipliers
`(0.49085,0.43742,0.07173)`. The one-dimensional tangent to the two
equioscillation constraints is numerically proportional to

```text
(0.98971277,0.14110395,-0.02362861),
```

and implicit second differentiation of those constraints gives common-well
curvature about `-0.28933` along the normalized tangent. Thus every transverse
direction is killed to first order by the positive KKT combination, and the
only first-order-flat direction bends downward numerically. This is strong
evidence for a strict local maximum, but not an interval proof.

These decimal boxes and derivative signs are numerical only; a
directed exact interval-Newton proof and exclusion of other family regimes
remain open.
