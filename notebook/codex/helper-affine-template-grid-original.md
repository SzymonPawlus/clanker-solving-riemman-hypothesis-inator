# Affine templates: complete endpoint orbits and the positive-interval case

Status: `sketch`, pending Claude or human review. This conditional lemma is
self-contained and assumes no unreviewed short-relation theorem. Applying
it to a particular template requires supplying the displayed integer data.
It deliberately leaves empty and isolated-point safe sets unresolved.

## Exact hypotheses and sanity filters

Let eight positive integer speeds `w_0,...,w_7<M` cover all lower endpoints
`t_j=(j+1/15)/M`, for `j` modulo `M`, with strict bad distance `<1/15`.
These are eight covering rows and a ninth fixed maximal anchor, inside the
fourteen-moving/fifteen-total-runner problem. All coordinates use the same
endpoint. Equality is safe. Assume this nine-speed core is primitive:

```
gcd(M,w_0,...,w_7)=1.
```

Common normalization of the entire nine-speed core preserves endpoint
coverage: before normalization its indices simply repeat the primitive
endpoint pattern. No separate coordinate is rescaled.

Suppose integers `P_i != 0`, `Q_i>0`, and `R_i` satisfy

```
Q_i*w_i=P_i*w_0+R_i*M.
```

Include the pivot row explicitly as `(P_0,Q_0,R_0)=(1,1,0)`. Put

```
L=lcm_i Q_i,
b_i=L*P_i/Q_i, c_i=L*R_i/Q_i,
B=gcd_i |b_i|, P=lcm_i |P_i|, H=15*(L/B)*P.
```

The pivot gives `b_0=L`, so `B|L` and `H` is a positive integer. Omitting
the pivot when computing `B` could lose its circle constraint and is not
permitted. All `b_i/B` are nonzero integer frequencies.

For every `r=0,...,L-1`, define the closed safe subset of the circle

```
S_r={y modulo 1:
     ||(b_i/B)*y+R_i*(15r+1)/(15Q_i)|| >=1/15 for every i}.
```

These sets depend only on the template, not on `M` or `w_0/M`.

## Full orbits, not truncated progressions

Write `x=w_0/M` and `g=gcd(M,L)`. The identity

```
b_i*w_0=L*w_i-c_i*M
```

shows `g|b_i*w_0` for every `i`, hence `g|B*w_0` by the gcd identity.
Let `d=gcd(M,B*w_0)` and `q=M/d`; then `g|d`.

For fixed `r`, take indices `j=L*k+r` with `0<=k<M/g`, reducing them
modulo `M` when needed. They are legitimate anchor indices and traverse
the complete residue class `r` modulo `g`. Set

```
y_k=B*x*k+(B/L)*x*(r+1/15) modulo 1.
```

Direct substitution gives

```
w_i*t_(Lk+r) = (b_i/B)*y_k + R_i*(15r+1)/(15Q_i) modulo 1.
```

The omitted term is the integer `c_i*k`. The step `B*w_0/M` has reduced
denominator `q`. Since `M/g=q*(d/g)`, the sampled `y_k` visit one complete
coset of the `q` equally spaced circle points, exactly `d/g` times. Using
only `0<=k<floor(M/L)` would not justify this complete-orbit assertion.

Put `d_0=gcd(M,w_0)`. The equations imply `d_0|L*w_i` for every `i`, and
also `d_0|L*M`. Primitivity and Bezout's identity therefore give `d_0|L`.
Consequently

```
d=gcd(M,B*w_0) <= B*d_0 <= B*L,
q >= M/(B*L).
```

## A uniform grid for every safe-set boundary

Solving one constraint's boundary equation gives

```
y = [15Q_i*k +/- Q_i - R_i*(15r+1)] / [15L*P_i/B].
```

Its denominator in absolute value divides `H=15(L/B)P`. Thus every
boundary of every `S_r` lies on the circle grid of spacing `1/H`.
The safe set is closed and is a finite union of intervals and points.
If it has nonempty interior, it contains an entire closed grid interval
of length `1/H`.

A coset of the `q` equally spaced points meets every closed interval of
length at least `1/q`. Hence if `q>=H`, one sampled `y_k` lies in `S_r`,
and its anchor endpoint is allowed by all eight rows. This contradicts
coverage. Endpoint equality is essential to this closed-interval argument.

Therefore, if at least one `S_r` has nonempty interior, every primitive
cover satisfying the template obeys

```
q < H,
M < B*L*H = 15*L^2*P.
```

This is a finite primitive-maximum bound for the positive-interval case.
It is not a finite reduction for every affine template: if all `S_r`
are empty or contain only isolated points, the argument gives no bound.
Those cases require exact circle-cover and congruence analysis. In
particular, a discrete endpoint grid can miss isolated safe points.

## Audit status

The prover independently checked the full-orbit, gcd, and boundary-grid
algebra in messages on 2026-09-14. The explicit pivot requirement was
confirmed separately. This is same-family checking only. Numerical
fixtures may support the implementation of these formulas but cannot
replace the quantified argument above or resolve its degenerate cases.
