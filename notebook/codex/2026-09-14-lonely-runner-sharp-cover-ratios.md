# Sharp speed ratios for covers by one through seven rows

Status: `sketch / exact complete certificates`, requiring independent
cross-family or human review. This is a new unified statement. The separate
six-row 13/12 certificate remains frozen and is included unchanged.

## Sharp theorem candidate

Let u be a positive integer anchor. If at most q positive integer speeds
cover all lower endpoints (15j+1)/(15u), j modulo u, with forbidden distance
strictly below 1/15, then the largest killer speed is at least R_q*u, where:

| q | R_q | Sharp anchor u | Sharp killer speeds |
|---|---|---|---|
| 1 | 15 | 1 | 15 |
| 2 | 15/2 | 2 | 1,15 |
| 3 | 15/4 | 4 | 2,13,15 |
| 4 | 13/6 | 6 | 2,3,11,13 |
| 5 | 11/6 | 12 | 4,6,7,13,22 |
| 6 | 13/12 | 12 | 4,5,6,7,11,13 |
| 7 | 1/2 | 30 | 1,6,7,10,11,13,15 |

Every sharp example covers all endpoint indices and has a private index for
every listed row. The example data and direct integer checks are recorded
in `issue-297/sharp-cover-ratio-fixtures.json`.

This is an all-anchor statement: killer speeds may exceed the anchor. In a
fourteen-speed tuple of maximum M, any anchor u>M/R_q needs more than q
killers if all its endpoints are covered. For q=1,...,6, these high-anchor
cutoffs are respectively M/15, 2M/15, 4M/15, 6M/13, 6M/11, and 12M/13.
For q=7 the bound instead says a seven-row cover needs a killer of speed at
least u/2; the corresponding cutoff 2M lies beyond the tuple.

The target motivating these obligations is fourteen moving velocities,
fifteen total runners, at 1/15. All rows use one common endpoint family.
Equality at 1/15 is safe. Signs can be removed and common scaling is valid;
no coordinatewise scaling is used. These ratios do not by themselves
exclude all-anchor covers of a fourteen-speed tuple.

## Self-contained finite reduction

Reduce a row w to h=u/gcd(u,w), a=w/gcd(u,w). For h>=2 the bad indices are

    B(h,a)={j modulo h: min(s,15h-s)<h},
    s=a(15j+1) mod15h, gcd(a,h)=1.

Under a strict trial bound w<Ru, every positive numerator a<Rh must be
included, even when a>h. When h=1, a is an integer, and the row kills every
endpoint exactly if 15 divides a; otherwise it kills none. Thus R<=15
removes every nonempty h=1 row. This also proves the q=1 lower bound,
because a row with h>=2 has density at most 1/2.

For any numerator, a row of period h has at most ceil((2h-1)/15) bad
residues: its centered strict phase representatives form one class modulo
15 in the 2h-1 integers from -h+1 to h-1. In particular its density is at
most 2/15+13/(15h). If q<=7 rows cover, some row density is at least 1/q,
so the smallest physical row period p satisfies

    p<=H_q=floor(13q/(15-2q)).

For q=2,3,4,5,7 these bounds are 2,4,7,13,91. For q=6 the formula gives
26; at periods 25 and 26 the exact ceiling is four, less than h/6, so the
sharper bound p<=24 is valid. No minimum-period-sixteen theorem or earlier
seven-row classification is assumed in this argument.

For each possible p, enumerate every nonempty initial row with 0<a<Rp,
gcd(a,p)=1. Its complement is a periodic residual set Rset, with q-1 rows
remaining. Each subsequent physical period must be at least p, even if the
residual itself has a smaller period.

At a state with r rows remaining and residual period L, put
n=h/gcd(h,L) for a candidate row. Its bad arc meets each equally spaced
n-grid in at most ceil(2n/15) points. Any completion contains a row covering
at least 1/r of the residual; that row satisfies

    n in E_r={n>=1: r ceil(2n/15)>=n}.

Since r<=6, (15-2r)n<=14r makes every E_r finite. The complete sets are

    E6={1,2,3,4,5,6,8,9,10,11,12,16,17,18,23,24},
    E5={1,2,3,4,5,8,9,10}, E4={1,2,3,4,8},
    E3={1,2,3}, E2={1,2}, E1={1}.

For every n in E_r enumerate all h>=p dividing Ln with h/gcd(h,L)=n,
and all positive unit numerators a<Rh. Lift to Ln, retain exactly those
rows with r*hits>=n*|Rset|, subtract their bad sets, reduce to the actual
smallest residual period, and decrement r. Equal resulting states may be
merged. Every hypothetical completion supplies at least one retained child,
so finite induction on r proves completeness. Empty residuals would be
reported as covers; none occurs at any of the strict bounds in the table.

## Exact certificates

| q | Strict excluded ratio | Initial roots | States | Edges | Largest residual period |
|---|---|---|---|---|---|
| 2 | 15/2 | 1 | 1 | 0 | 2 |
| 3 | 15/4 | 4 | 5 | 1 | 4 |
| 4 | 13/6 | 13 | 16 | 4 | 7 |
| 5 | 11/6 | 72 | 96 | 30 | 24 |
| 6 | 13/12 | 169 | 279 | 151 | 180 |
| 7 | 1/2 | 1264 | 1541 | 330 | 1020 |

For q=2,3,4,5,7 the generator is
`issue-297/upper_anchor_threshold_search.py`; the frozen q=6 generator is
`issue-297/upper_anchor_six_search.py`. Each ratio has a JSON summary and
`.graph.json` certificate under `issue-297/upper-anchor-*`. The combined
fixture manifest binds these inputs by SHA-256.

An independent checker must reconstruct every physical initial numerator,
all distinct exact children and each representative row; check strict
numerator bounds by integer arithmetic; preserve the physical lower period
bound separately; reject empty residuals, incomplete runs and malformed
edges; and verify every edge decreases the remaining-row count.

The q=7 conclusion also follows from the separately proposed compulsory
period-two theorem and is attained by known seven-row cores. The standalone
1,541-state exclusion here deliberately supplies its own complete proof
obligation, including all initial periods through 91, rather than assuming
that earlier sketch. At q=8 the initial density bound has nonpositive
denominator, so this finite scheme does not extend automatically.
