# Every integer affine open-cell cover lifts along powers of three

Status: `sketch`; self-contained conditional theorem. Root, manager, and
helper have independently checked the valuation mechanism. No qualifying
eight-row template has been found, so this is not an asserted counterexample
to the small-period proposal or to Lonely Runner.

This is separate from the frozen prime-lift note: it removes the extra
fifteenth-grid condition by changing the integer anchor sequence.

## Statement

Take eight distinct integer pairs `(a_i,b_i)` with each `a_i` nonzero.
Suppose a nonempty open interval `I` inside `(0,1)` satisfies

```text
0<a_i*x+b_i<1 for all i and all x in I.
```

Suppose the eight strict bad sets

```text
C_i={z mod1 : ||a_i*z+b_i/15||<1/15}
```

cover every open cell cut out by their rational endpoints. Equivalently,
their safe complement `E` is finite; it may contain every fifteenth-grid
point. Then there are primitive inclusion-minimal eight-row maximal-anchor
covers with arbitrarily large reduced periods, all powers of three.

This statement concerns eight smaller speeds and their ninth, maximal
anchor, within the fourteen-moving/fifteen-total-runner program at threshold
`1/15`. All conditions concern the same time. Forbidden arcs are strict;
equality is success. Common gcd normalization is the only scaling step.

## Construction and exact boundary avoidance

Let `s=max_i v_3(|a_i|)` and `e=min_i v_3(|a_i|)`. For a sufficiently large
integer `n>s`, put `M=3^n` and choose an integer `q` with

```text
q/M in I, 3 does not divide q.
```

Such a `q` exists for every sufficiently large `n`, because the length of
`M*I` tends to infinity. Define `w_i=a_i*q+b_i*M`. The strip condition
puts all `w_i` strictly between zero and `M`. They are distinct once
`M>2 max|a_i|`: equality of two speeds would imply
`M|(a_i-a_j)` since `q` is a unit modulo `M`, forcing equality of both
integer pairs.

The sampled phases are

```text
z_j=q(15j+1)/(15M) mod1, 0<=j<M.
```

They form a complete equally spaced `M`-point grid with a common offset.
Multiplying the maximal lower endpoint by `w_i` gives

```text
w_i*(15j+1)/(15M) = a_i*z_j+b_i/15 mod1.
```

Every endpoint of a set `C_i` has reduced denominator dividing `15|a_i|`.
Its denominator therefore has 3-adic valuation at most `s+1`. Every sampled
phase `z_j`, in contrast, has reduced denominator with 3-adic valuation
exactly `n+1`: its numerator `q(15j+1)` is coprime to three, whereas its
denominator is `15*3^n`. Reduction modulo one does not change that fact.
Thus no sampled phase equals any endpoint, and in particular none lies in
the finite safe set `E`. Every maximal lower endpoint is covered strictly.

## Primitive normalization, large periods, and minimality

Since `q` is a unit modulo `3^n`,

```text
gcd(M,w_1,...,w_8)=gcd(M,a_1,...,a_8)=3^e,
M/gcd(M,w_i)=3^(n-v_3(|a_i|)).
```

Divide all nine speeds, including the anchor, by `3^e`. The new core is
primitive. Its bad-index row patterns have the same reduced periods as
before, so endpoint coverage survives and every reduced period tends to
infinity with `n`.

To see the normalization directly, for a common divisor `g` the reduced
endpoint index `j` corresponds to the original index `j` modulo `M/g`;
each original row mask repeats with that period. Dividing all speeds and
the anchor by `g` gives exactly the same strict residue condition.

Finally, each selected row has a positive private interval in the `z`
circle. Removing that row leaves seven bad sets with total measure at most
`14/15`; their safe complement has positive measure and contains an interval.
Except for the finite set `E`, the removed row covers that interval. The
uniform sampled grid meets every private interval for all sufficiently
large `n`. Consequently every row has a private endpoint, and the normalized
eight-row cover is inclusion-minimal.

There is also an explicit sufficient size. The private set of every row
has measure at least `1/15`. All eight boundary lists partition the circle
into at most `2 sum_i|a_i|` open cells, so that row has a private open cell
of length at least `1/[30 sum_i|a_i|]`. Hence one may choose any `n` with

```text
n>s, 3^n>2 max_i|a_i|,
3^n*length(I)>3, 3^n>30 sum_i|a_i|.
```

The interval condition supplies an integer `q` not divisible by three;
the grid-spacing condition supplies a private endpoint for every row.
Thus the construction and its eventual minimality are effective, without
an unspecified density or equidistribution assumption.

## Consequence for the current structural search

An integer affine open-cell cover satisfying the positive strip would
refute the proposal that every eight-row maximal cover has a reduced period
at most three, producing infinitely many primitive examples. A complete
search must therefore allow isolated safe endpoints; requiring a full
open-circle cover or a covered fifteenth point could miss the relevant
templates.

For slopes `1<=|a|<=24`, the discovery program has tested all 180 floor
chambers with `b=-floor(a*x)` and found no open-cell cover with eight rows.
Those discovery outputs alone are numerical. The helper is independently
replaying the complete bounded family using exact set-cover decisions;
its conclusion will be recorded separately. No general exclusion for
unbounded slopes is claimed.
