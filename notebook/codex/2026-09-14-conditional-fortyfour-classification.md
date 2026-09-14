# Conditional classification of seven-row maximal-anchor covers

Status: `sketch`, requiring Claude or human review. Independent internal
enumerations by helper and manager agree, but both are Codex-family work.

## Statement and scope

At threshold 1/15, suppose seven smaller positive integer speeds form an
inclusion-minimal cover of every lower endpoint of their maximal speed M.
Assume that reduced periods 2 and 3 both occur. After one common gcd
normalization, the eight-speed tuple is one of exactly 44 tuples in
`helper-fortyfour-primitive-cores.json`. Their maximal speeds and counts are

    M=18:4, M=24:8, M=30:8, M=36:16, M=48:4, M=72:4.

This concerns maximal-anchor covers, not no-witness certificates for all
fourteen moving velocities. Period-2/3 necessity is not assumed proved here.
The ambient Lonely Runner target is fourteen moving velocities, fifteen
total runners, at threshold 1/15. A common-time witness includes equality;
all forbidden tests below are strict.

## Finite reduction

For each reduced row (h,a), 0<a<h and gcd(h,a)=1, its bad set is

    B(h,a)={j modulo h: rho_(15h)(a(15j+1))<h}.

The period-2 and period-3 rows are respectively the multiples of 2 and 3,
so the residual is {1,5} modulo 6. The independently audited conditional
charge table has nineteen reduced pairs capable of covering at least 1/15
of the entire index space. Their periods are 5,10,12,18,20,24,30.
The tail estimate Q<=2/45+2/h shows that every such pair has h<=90, so this
is a complete table, not a numerical truncation.

Five rows remain, and they must cover residual mass 1/3, so one has charge
at least 1/15. Adding it gives joint period

    L3 in {12,18,24,30,60}.

If a current residual is a union of classes modulo L, a candidate period
h has relative multiplier n=h/gcd(h,L), and its conditional coverage is at
most ceil(2n/15)/n. Thus with r rows left, at least one candidate has
n in E_r={n>=1:r ceil(2n/15)>=n}. The remaining multiplier sets are

    E4={1,2,3,4,8}, E3={1,2,3}, E2={1,2}, E1={1}.

Inclusion-minimality keeps every proper selected subcover incomplete. After
all rows are added the final lcm equals the normalized maximal speed M.
Therefore M=L3*n4*n3*n2, which gives exactly these 37 candidate anchors:

    12,18,24,30,36,48,54,60,72,90,96,108,120,144,162,180,192,
    216,240,270,288,324,360,384,432,480,540,576,720,768,864,960,
    1080,1152,1440,1920,2880.

The independent search includes M=12; the conditional divisibility theorem
also excludes it analytically. No arbitrary anchor cutoff is used.

## Exhaustive search and its necessary pruning conditions

For each candidate M, enumerate all actual smaller positive speeds
w=1,...,M-1 and compute their literal M-bit forbidden masks. Seed the search
with w=M/2 and w=M/3. The alternative w=2M/3 has the same row mask and the
same gcd with M. A minimal cover cannot contain both copies. Each final
solution therefore restores both choices, producing two distinct physical
speed tuples without losing any cover.

A state records selected rows, their union, their current lcm L, r slots
left, and still-available rows. The following conditions are necessary:

1. Every selected row must retain a private residue relative to the selected
   rows. Losing it can never be repaired by adding rows, so such branches
   cannot yield an inclusion-minimal cover.
2. The sum of the r largest available new-coverage counts must be at least
   the residual cardinality.
3. The final primitive lcm must equal M. Since some completion has a greedy
   ordering with multipliers E_r,...,E1, the ratio M/L must belong to the
   exact finite product set E_r*...*E1.
4. Some row in any completion covers at least a 1/r fraction of the current
   residual. The next branch row must meet this integer threshold, have
   multiplier in E_r, and leave a feasible final-lcm product for r-1 slots.

To partition covers without duplicates, order the currently eligible
high-coverage rows. In a branch choosing one row, exclude only earlier
eligible alternatives in that state. Any fixed completion has a unique
first eligible member, so it belongs to one branch; repeating this argument
proves exhaustive coverage. No globally increasing velocity order is
imposed, which would be invalid for this greedy argument.

The helper search inspected 1,673 states across all 37 anchors, with no
timeouts, and returned exactly 44 primitive tuples. Every tuple includes
direct private-residue certificates for all seven rows. The manager then
wrote a separate implementation from the mathematical specification, without
reading the helper implementation; it inspected 2,127 states and returned
the identical set of 44 physical tuples. The original literal subset
enumeration through M=240 also returned those same 44 primitive tuples and
no others in its bounded domain.

## Replay

Run `helper_conditional_core_census.py` with its default 37 anchors and an
output path. The emitted JSON binds the checker source by SHA-256 and marks
every individual anchor complete or incomplete. The recorded accepted run
is `helper-conditional-core-census.json`; no incomplete run is used here.
The manager replay is recorded separately in its issue-297 workspace.
