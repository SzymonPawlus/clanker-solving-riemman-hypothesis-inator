# A period-2 seven-row cover must contain period 3

Status: `sketch / exact finite certificate`, pending independent cross-family
or human review. This is a separate frozen attack; it does not modify or
assume the earlier conditional forty-four-core census.

## Statement and sanity filters

Let M be positive. Suppose at most seven smaller positive speeds cover all
lower maximal-anchor endpoints t_j=(15j+1)/(15M), j modulo M, using the
strict forbidden condition ||w t_j||<1/15. If one row has reduced period 2,
then some row has reduced period 3. Minimality of the cover is not assumed.

The target motivating this subproblem is fourteen moving velocities,
fifteen total runners, at threshold 1/15. This theorem is an endpoint-cover
obstruction, not a proof of the full Lonely Runner Conjecture. Its
quantifiers concern one common family of endpoints for all speeds. Equality
at 1/15 is safe. Only common gcd normalization and exact periodic lifts are
used; coordinatewise scaling is not used. The code sanity fixture (h,a,j)
=(16,1,1) has phase 16/240=1/15 and is correctly excluded from the bad set.

## Exact state semantics

Write a row as reduced data h=M/gcd(M,w), a=w/gcd(M,w), with 0<a<h and
(a,h)=1. Its bad residues are

    B(h,a)={j modulo h: min(a(15j+1) mod 15h,
                            15h-(a(15j+1) mod 15h))<h}.

The period-2 row is exactly the even residues, so the remaining rows must
cover the odds. The root state is (p,L,R)=(6,2,{1}), where R is the remaining
residue set modulo L and p is the number of available rows. All candidates
have physical reduced period h other than 3. This exclusion refers to the
row's reduced speed data, even if its Boolean bad set has a smaller period.

After choosing a row of period h, let d=gcd(h,L), n=h/d, and T=Ln. Lift R and
B to residues modulo T, subtract B, and replace the resulting set by its
smallest exact period. This replacement is valid because it represents
exactly the same infinite periodic subset of the integers. It does not
alter any speed or select a new phase origin.

If p rows cover a nonempty R, at least one covers at least 1/p of R. On each
residue class modulo L, a row of period h sees n equally spaced circle
points. An open arc of length 2/15 contains at most ceil(2n/15) of them.
Therefore that high-gain row must have

    n in E_p={n>=1: p ceil(2n/15)>=n}.

For p<=6, the inequality ceil(2n/15)<=(2n+14)/15 gives
n<=14p/(15-2p)<=28. Exact integer evaluation yields

| p | E_p |
|---|---|
| 6 | 1,2,3,4,5,6,8,9,10,11,12,16,17,18,23,24 |
| 5 | 1,2,3,4,5,8,9,10 |
| 4 | 1,2,3,4,8 |
| 3 | 1,2,3 |
| 2 | 1,2 |
| 1 | 1 |

For each n in E_p, the search enumerates every h dividing Ln with
h/gcd(h,L)=n, excluding h=1 and h=3, and every unit numerator 0<a<h. Thus
there is no unproved period cutoff. Rows are retained exactly when their
integer gain satisfies p*gain>=n*|R|. At least one member of any hypothetical
completing family must be among those retained rows.

A nonempty state with no rows remaining is impossible. An empty residual is
a found cover. The remaining-row count strictly decreases along each edge,
so recursively checking every retained child is a finite proof by induction.
Memoization merges only an identical (p,L,R). Equal bad masks at a fixed h
and equal resulting child states may be merged, since only existence of a
cover is at issue; no classification of the original numerators is inferred.

## Certificate and result

The complete search has 1,093 distinct nonterminal states and 2,022 distinct
child edges after equal child states are merged. No empty residual occurs.
The largest minimized residual period is 340. State counts by remaining rows
are p=6:1, p=5:38, p=4:341, p=3:490, p=2:213, and p=1:10.

The implementation is `issue-297/no_period3_search.py`. The frozen summary
and directed acyclic graph are `issue-297/no-period3-complete.json` and
`issue-297/no-period3-complete.graph.json`. The graph lists the exact residue
mask, remaining-row count, candidate count, and all distinct children for
every state. The summary binds both graph and generator by SHA-256. The
actual run reached no time or node limit and completed in about 1.75 seconds.
A resource-limited run would instead report `complete:false` and could not
support the statement.

An independent checker should regenerate candidate rows from the direct
strict residue definition above, reconstruct all distinct child states,
compare them to the graph, and verify that every reachable child is either
a certified nonempty zero-row leaf or another certified state. It must also
verify that graph masks are nonempty, indices are in range, and all edges
strictly reduce p. No floating-point decision is needed. The implementation
uses exact rational gain sorting only to choose traversal order.

This finite state result proves the displayed necessity statement conditional
on validation of the enumerator and finite certificate. It does not prove
that period 2 occurs in every seven-row cover; that is a separate attack.
The forty-four-core census remains conditional until both necessary periods
have been justified and independently reviewed.
