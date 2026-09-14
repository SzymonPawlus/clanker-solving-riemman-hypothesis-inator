# Twenty explicit cores are obstructed at every integer scale

Status: `sketch`; author exact checks and independent same-family checks
pass. Claude or human review remains required. This extends the frozen
four-core result without assuming any classification of maximal covers.

For each of the following eight-speed sets `P`, for every positive integer
`c`, and for any set of at most six additional positive integer speeds below
`c max(P)`, there is one common rational time at which all speeds in the
combined set have distance at least `1/15` from an integer. This is a
fourteen-moving-runner / fifteen-total-runner statement.

| Tag | P | Total weight |
|---|---|---:|
| p18 | 1,5,6,7,9,11,13,18 | 6011/1000 |
| p18-6-14 | 1,5,6,9,11,13,14,18 | 6019/1000 |
| p18-12-7 | 1,5,7,9,11,12,13,18 | 1507/250 |
| p18-12-14 | 1,5,9,11,12,13,14,18 | 759/125 |
| p24-1 | 1,5,7,8,11,12,13,24 | 1521/250 |
| p24-2 | 1,5,7,8,12,13,22,24 | 3041/500 |
| p24-3 | 1,5,7,11,12,13,16,24 | 6053/1000 |
| p24-4 | 1,5,7,12,13,16,22,24 | 3041/500 |
| p24-5 | 1,8,10,11,12,13,14,24 | 6083/1000 |
| p24-6 | 1,8,10,12,13,14,22,24 | 1213/200 |
| p24-7 | 1,10,11,12,13,14,16,24 | 6083/1000 |
| p24-8 | 1,10,12,13,14,16,22,24 | 761/125 |
| p30-1 | 1,6,7,10,11,13,15,30 | 152/25 |
| p30-2 | 1,6,7,11,13,15,20,30 | 6077/1000 |
| p30-3 | 1,7,10,11,12,13,15,30 | 243/40 |
| p30-4 | 1,7,10,11,13,15,18,30 | 243/40 |
| p30-5 | 1,7,10,11,13,15,24,30 | 6077/1000 |
| p30-6 | 1,7,11,12,13,15,20,30 | 6077/1000 |
| p30-7 | 1,7,11,13,15,18,20,30 | 3039/500 |
| p30-8 | 1,7,11,13,15,20,24,30 | 60067/10000 |

## Universal rational-measure lemma

Let `P` be any finite set of positive integers, with maximum `M`, and let
`(x_i,z_i)` be finitely many pairs with rational `0<=x_i<1`, rational `z_i>0`,
and `||v x_i||>=1/15` for every `v in P`. Suppose

```text
6 < T=sum_i z_i <= 61/10.
```

For `1<=n<=30`, check every integer `1<=q<Mn` coprime to `n`; when `n=1`,
exclude the fixed speeds `q in P`. Define

```text
C_i(n,q) = #{k in {0,...,n-1}: ||q(k+x_i)/n|| < 1/15}.
```

Suppose `sum_i z_i C_i(n,q) <= n` in every such case. Then for all `c>=1`,
any six arbitrary additional integer speeds below `Mc` leave a common
witness for `cP` and those speeds.

**Proof.** Give `(k+x_i)/c` weight `z_i/c`, for `0<=k<c`. Every such time is
good for the fixed subsystem `cP`. For an extra speed `w`, put
`d=gcd(c,w)`, `n=c/d`, `q=w/d`. Its weight load is exactly
`sum_i z_i C_i(n,q)/n` because its hit pattern repeats `d` times. The finite
assumption handles `n<=30`. For `n>=31`, multiplication by `q` permutes the
`n` equally spaced points, so each `C_i` is at most `ceil(2n/15)`. Therefore

```text
load <= (61/10)(2n+14)/(15n) <= 1,
```

the final inequality being `854<=28n`. Six speeds together kill weight at
most six, strictly less than the total `T`, so some single supported rational
time is good for all speeds. This union-bound proof uses strict forbidden
arcs; equality remains a witness. Fixed or repeated additions only remove
constraints, and signs can be replaced by absolute values. QED.

The points need not be anchor endpoints. This flexibility matters: restricting
the weights to lower endpoints gave numerical optimum below six for ten of
the twenty cores. Adding quarter points inside exact intervals already good
for the primitive core produced feasible measures with mass above six for
all ten. The discovery grid has no role in completeness: the final rational
atoms are checked directly.

## Exact artifacts and remaining scope

[all-twenty-cores.json](./issue-304/all-twenty-cores.json) contains every
pattern and every rational `(x_i,z_i)` pair. It removes zero weights and
combines duplicate atoms. The [author checker](./issue-304/check_all_cores.py)
uses only exact integer and rational arithmetic, validates every atom's
fixed-core safety, checks the mass interval, and checks every finite column.
Its [audit output](./issue-304/all-twenty-author-audits.json) binds the manifest
with SHA-256 and records every denominator's maximum. There are 4,996,
6,664, or 8,332 finite column checks per core, according as `M=18,24,30`.

The helper independently implemented literal residue counting from the
mathematical specification. All twenty certificates passed its finite
checks; it also compared literal lifts at small scales with the reduced
counts. This is same-family checking and does not confer `verified:review`.

These twenty cores are **not** a complete classification. During this cycle
the manager found, and the helper checked, primitive inclusion-minimal
seven-row maximal covers such as

```text
2,12,15,18,26,28,33,36
2,11,13,16,20,24,28,48
2,7,10,11,12,18,26,36.
```

They are not integer-scaled copies of the twenty patterns above. Thus the
earlier suggested completeness claim is false. The universal-measure lemma
and each explicitly certified family remain valid; the next structural task
is to understand the larger family of seven-row maximal covers.

Clock-confirmed checkpoint: 2026-09-14 20:10:34 UTC. Research continues after
this frozen result; neither the conjecture nor the full one-hour work cycle
is finished.
