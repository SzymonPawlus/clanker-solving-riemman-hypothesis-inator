# A universal phase dual excludes six additions to one scaled core

Status: `sketch`, exact finite certificate supplied; independent review required.
Issue: #304. Author: Codex. Work cycle began 2026-09-14 19:56:40 UTC.
This statement is self-contained and does not assume the earlier seven-row
classification, scaling-density ledger, or any pending PR.

## Claim and sanity filters

Let `P={1,5,6,7,9,11,13,18}`. For every positive integer `c`, and every set
`W` of at most six positive integers below `18c` outside `cP`, there is a
single real `t` such that

```text
||tv|| >= 1/15  for every v in cP union W.
```

This concerns at most fourteen moving velocities and fifteen total runners.
All velocities in the claim use the same time. Signs can be replaced by
absolute values because `||-x||=||x||`, and repeated absolute values impose
the same condition. The only scaling performed is common scaling of the
fixed subsystem: each extra speed remains arbitrary. Forbidden arcs are
strict (`<1/15`); equality succeeds. In particular `P` has speed `1`, and
its endpoint `1/15` is allowed for speed `1`: the strict count below is zero
at `(n,q,u,r)=(1,1,1,0)`.

This proves a special family of the `k=14` target, not the full conjecture.
It does not classify seven-row maximal covers or establish that an arbitrary
counterexample contains this subsystem.

## Fixed endpoint types and weights

For `u in P`, use `x_(u,r)=(15r+1)/(15u)`, `0<=r<u`. Retain a pair `(u,r)`
exactly when all fixed speeds other than `u` have distance at least `1/15`
at this time. The following table lists all retained pairs and a positive
integer weight numerator. Every denominator is `1000`.

```text
u    r: numerator
1    0:134
5    1:111  2:294
6    2:364  3:149  4:164
7    2:52   4:163  6:375
9    1:431  7:184  8:316
11   1:141  4:285  7:452  8:399  10:359
13   1:114  3:221  4:191  6:90   8:282  9:489  12:251
18   no retained pairs
```

The 24 weights sum to `6011/1000`, strictly greater than six. The machine-
readable certificate is [p18-weights.tsv](./issue-304/p18-weights.tsv).
All times are allowed by the complete fixed subsystem, including their own
anchor (where equality holds). The table can be reconstructed using only
the integer test

```text
s = v(15r+1) mod 15u;
min(s,15u-s) >= u  for each v in P\{u}.
```

## Uniform lifting and exact finite reduction

At scale `c`, give each time `(k+x_(u,r))/c`, `0<=k<c`, weight `z_(u,r)/c`.
It is still allowed by every speed in `cP`, since multiplying by `cv` gives
`v(k+x_(u,r))`. Total weight remains `T=6011/1000`.

For any extra speed `w`, write `d=gcd(c,w)`, `n=c/d`, `q=w/d`. Then
`gcd(n,q)=1`, `1<=q<18n`. The hit pattern repeats `d` times. Multiplication
by `q` permutes the residues modulo `n`, so the bad weight collected from
one primitive type is exactly

```text
(z_(u,r)/n) C(n,q,u,r),
C(n,q,u,r) = #{m in Z : -n/15-y < m < n/15-y},
y = {q(15r+1)/(15u)}.
```

This integer-interval count is also the number of bad points among the `n`
equally spaced translates. If `n=1`, the excluded fixed speeds mean
`q notin P`. If `n>1`, all coprime `q<18n` must be checked; no further
exclusion is made. Thus a single table of primitive weights controls every
scaling factor `c`, including arbitrarily large and composite ones.

For exact evaluation put `a=q(15r+1) mod 15u` and `N=15u`. The count is

```text
C(n,q,u,r) = -floor((a-nu)/N) - floor((-nu-a)/N) - 1.
```

Both endpoints of the interval are open. This formula, unlike floating
distance sampling, preserves isolated endpoint witnesses exactly.

Every interval of length `2n/15` contains at most `ceil(2n/15)` integers
when its endpoints are excluded. Since

```text
ceil(2n/15) <= (2n+14)/15,
T(2n+14)/(15n) <= 1  whenever 84154 <= 2978n,
```

every `n>=29` is controlled without any further computation. It remains to
check only `1<=n<=28` and the stated finite ranges of `q`. The exact maximum
loads and one attaining `q` are:

```text
n   maximum load      q
1   499/500           17
2   1997/2000         13
3   749/750           53
4   3993/4000         3
5   624/625           67
6   471/500           65
7   6011/7000         120
8   93/100            21
9   8861/9000         91
10  2451/2500         91
11  1302/1375         54
12  3719/4000         91
13  11649/13000       2
14  6011/7000         57
15  6011/7500         269
16  1821/2000         195
17  15609/17000       195
18  1007/1125         319
19  2086/2375         319
20  4447/5000         143
21  17981/21000       205
22  18033/22000       375
23  9731/11500        21
24  6961/8000         91
25  11123/12500       312
26  22507/26000       385
27  5849/6750         275
28  6011/7000         429
```

Every load is at most `749/750<1`. The author additionally checked every
denominator through `83`; that larger table is unnecessary for the proof.

## Common witness and significance

Each of the at most six extra speeds kills weight at most one. By the union
bound, together they kill weight at most six, while the lifted measure has
weight `6011/1000`. Positive weight, at least `11/1000`, therefore survives
all extra speeds at one of its finitely many rational times. Every such time
already obeys every fixed speed, proving the claim.

Earlier exploration attempted to preserve dual value seven at every scale
and obtained only a partial collection of scaling families. The sufficient
threshold is strictly greater than six. A single universal measure meeting
that weaker threshold handles all positive scales without a recursive
certificate family. The LP used to discover the weights has no logical role
in the theorem: positivity, the displayed sum, the finite integer checks,
and the analytic tail are the complete obligations.

## Work log

- 19:56:40 UTC: began cycle, read root and problem rules and three prior
  sketch notes; inspected the failure of fixed weights to retain value seven.
- 20:00:30 UTC: clock-confirmed checkpoint; reconstructed a universal dual
  with rational total `6011/1000` and exact full-table maximum `749/750`.
  Sent only mathematical specification and weights to the helper for an
  independent checker. The certificate is frozen while other primitive
  patterns are investigated separately.
