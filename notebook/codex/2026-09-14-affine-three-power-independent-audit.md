# Independent audit of boundary avoidance along powers of three

Status: `sketch`, pending Claude or human review. Helper independently
checked the mathematical note `issue-304-three-power-affine-lifts.md` in
the prover branch, without reading an author implementation. No covering
affine template has been found; this is a conditional theorem, not a
counterexample to either the small-period proposal or Lonely Runner.

The target is fourteen moving velocities, fifteen total runners, at 1/15.
The constructed object has eight smaller rows and one maximal anchor.
All rows use one common endpoint. Strict bad inequalities and safe equality
are retained, and primitive normalization rescales the entire core only.

## General endpoint-hit criterion

For `gcd(q,M)=1` and reduced `u/v` in the circle, the grid

```
{q(15j+1)/(15M) mod 1 : 0<=j<M}
```

hits `u/v` exactly when `v|15M` and

```
(15M/v)u == q (mod 15).
```

Necessity follows by multiplying equality modulo one by `15M` and reducing
modulo 15. Conversely, the congruence makes
`((15M/v)u-q)/15` an integer, and the unique solution of
`qj=((15M/v)u-q)/15 (mod M)` gives a sampled point. This handles reduced
denominator one and does not require that `q` be a unit modulo 15.

For the manager's separate specialization `M=15p`, `p>max|a_i|` prime,
`gcd(q,M)=1` does imply `gcd(q,15)=1`. An affine boundary denominator
`v|15|a_i|` can have both factors `3^2` and `5^2` only if `15|a_i|`.
When that divisibility is forbidden, either `v` does not divide `15M`, or
`15M/v` has a factor 3 or 5 and the congruence above is impossible. Thus
the stated composite-anchor boundary-avoidance claim is also correct.

## Unrestricted pure-power specialization

Take eight distinct integer pairs `(a_i,b_i)`, with `a_i!=0`, and a common
nonempty open strip `I` where `0<a_i x+b_i<1`. Suppose their strict bad
sets `||a_i z+b_i/15||<1/15` cover every open cell between their exact
endpoints. Their safe complement is then finite. Set

```
s=max v3(|a_i|), e=min v3(|a_i|), M=3^n, n>s.
```

For every sufficiently large `n`, there is an integer `q` with `q/M` in
`I` and `3` not dividing `q`: the interval `MI` grows without bound and
two of every three integers are eligible. Put `w_i=a_i q+b_i M`.
The common strip gives `0<w_i<M`. If two speeds coincide, invertibility
of `q` modulo `M` forces `M|(a_i-a_j)`; for `M>2max|a_i|` this forces
equal slopes and then equal intercepts, contrary to distinct pairs.

Every boundary has denominator dividing `15|a_i|`, so its reduced
denominator has 3-adic valuation at most `s+1`. Every sample
`z_j=q(15j+1)/(15M) mod 1` has denominator valuation exactly `n+1`,
because its numerator is a unit modulo three. Reducing modulo one does
not alter this fact. Thus no sample is a boundary. Every sample lies in
an open covered cell. Direct substitution gives

```
w_i(15j+1)/(15M) == a_i z_j+b_i/15 (mod 1),
```

so every maximal lower endpoint is covered strictly.

## Normalization and private indices

Since `q` is a unit modulo `M`,

```
gcd(M,w_1,...,w_8)=gcd(M,a_1,...,a_8)=3^e,
M/gcd(M,w_i)=3^(n-v3(|a_i|)).
```

Dividing all nine speeds by `3^e` preserves each physical row period and
the exact bad-index mask. The new core is primitive and every row period
still tends to infinity. This conclusion does not use the unreviewed
seven-row classification.

For each chosen row, the other seven bad sets have total measure at most
`14/15`. Their common safe set is closed, is a finite union of intervals
and points, and has positive measure, so it has a nonempty open interval.
Deleting finitely many endpoints leaves a smaller open interval. Because
all eight rows cover every open cell, the deleted eighth row covers that
smaller interval strictly while the other seven remain safe. Hence each
row has a private open interval. The sampled points form a complete
equally spaced grid of mesh `1/M`; for sufficiently large `n` they meet
all eight private intervals. Private indices survive common normalization.
This proves eventual inclusion-minimality and completes the conditional
argument, including its boundary cases.

The prover's added effective bound also passes. The private set of each
row has measure at least `1/15`. At most `2 sum_i |a_i|` distinct boundary
points partition the circle, so at least one private open cell has length
at least `1/(30 sum_i |a_i|)`. Thus `M>30 sum_i |a_i|` guarantees a sample
strictly inside such a cell. Together with `n>s`, `M>2max|a_i|`, and
`M length(I)>3`, this gives explicit sufficient bounds for boundary
avoidance, distinctness, an eligible `q`, and private indices. The strict
mesh inequality avoids mistaking a boundary sample for a private point.

## Exact implementation fixtures

`helper_affine_endpoint_audit.py` is independently written from the above
algebra. It checks the general hit criterion directly against exact sets
of sampled rationals, then checks three-power sample/endpoint separation,
gcds, physical periods, original phase identities, and normalization for
both primitive and nonprimitive slope families. The fixtures do not assert
that those families cover the open cells. The report binds the tested
prover note and checker by SHA-256. These regressions support the formulas;
they do not replace the quantified proof above.

The completed report `helper-affine-endpoint-audit.json` records 1,102
general grids and 539,980 exact endpoint-hit comparisons, plus 30
three-power fixtures with 46,213 boundary-separation checks, 58,806 sample
valuation checks and 3,960 original/normalized coordinate identities.

The separate exact `|a|<=24` search excludes every open-cell cover in all
180 floor chambers. Its bounded conclusion is recorded in
`2026-09-14-affine-K24-exact-chambers.md` and remains numerical.
