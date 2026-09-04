# Red-team and exact bottleneck for the analytic four-edge envelope

**Status:** `sketch`; same-family independent reconstruction of frozen commit
`c40527d`.  Nothing here grants `verified:review`.  The support-to-area step
still depends on the mixed-area/common-fan bridge identified by Issues #170
and #176.

## Audit outcome

The claimed support floor

```text
1175341/5000000 = 0.2350682
```

survives.  The checker reconstructs rather than imports the audited formulas:

- the half-angle directions, positive edge lengths, closure, and exact unit
  open-worm length;
- strict local turns plus a monotone unwrapped edge-direction order of total
  turn `2*pi`, excluding a winding-two star;
- all four maximal balanced three-load allocations, their capacity bounds,
  and balance of both allocated and residual surface measures;
- every triangle support-switch orientation in `Q(sqrt(3))`, giving the four
  stated triangle minima;
- the `C,A,S,B` sinusoidal coefficients directly from residual loads and
  exact projection signs;
- all eight endpoint margins and the `A <-> D` direct-motion pairing.

No binary floating point enters an accepted predicate, and validity checks use
explicit exceptions rather than removable Python assertions.

## Exact global bottleneck

The audit gives a stronger description than the rational floor.  Put

```text
y = -180/25753 + (25915/103012)*sqrt(3).
```

This lies in `(sin(alpha),3/5)`.  It is the unique `A=C` crossing because the
two bounds have the same cosine coefficient and their difference is affine
and strictly increasing in `sin(phi)`.  Define

```text
L* = (399091/9955200)*sqrt(3)
     + (489/13120)*y
     + (163/984)*sqrt(1-y^2).
```

Exact rational isolating intervals prove

```text
0.235068284611 < L* < 0.235068284612.
```

On the four intervals cut at the algebraic crossing, `1/3`, and `3/4`, the
respective `C,A,S,B` bounds are nonnegative sinusoids and hence concave.  Their
endpoint values are at least `L*`.  At the crossing, exact interval evaluation
proves `A=C=L*` while `S`, `B`, and `D` are strictly smaller.  Therefore `L*`
is not merely a lower bound: it is the exact minimum of the pointwise maximum
of all five legal support allocations.

A simpler strengthened rational corollary uses the nearby cut
`tan(phi/2)=17183/76284` and proves

```text
max(S,A,B,C,D) >= 5876707/25000000 = 0.23506828
```

over the complete direct-motion domain.  This remains conditional on the
same bridge and is not yet an assumable Moser area bound.

Replay:

```text
python problems/moser-convex-worm/attacks/four-edge-analytic-redteam/check_analytic.py
python -O problems/moser-convex-worm/attacks/four-edge-analytic-redteam/check_analytic.py
python -m unittest discover \
  -s problems/moser-convex-worm/attacks/four-edge-analytic-redteam \
  -p 'test_*.py' -v
```
