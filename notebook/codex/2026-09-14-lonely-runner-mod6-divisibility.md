# Conditional divisibility of a seven-row maximal cover

Status: `sketch`, requiring independent cross-family review. The assumptions
below are explicit and are not supplied by the current bounded census.

## Statement

Suppose seven smaller positive speeds cover every lower endpoint of a maximal
speed M at threshold1/15. Suppose two of their reduced row periods are2 and3.
Then at least one of18,24,30 divides M.

This proves the divisibility clause of the inherited conjecture **conditional
on the period2 and period3 rows being present**. It does not prove their
presence in every seven-row cover, nor classify all covers. The ambient
target remains fourteen moving velocities / fifteen total runners.

## Exact conditional row charge

Rows of period2 or3 kill precisely the multiples of2 or3, respectively, when
they are nonempty at a maximal anchor. The residual set is therefore
E={j : j mod6 is1 or5}, of density1/3. Write a further row as reduced data
(h,a), with0<a<h and gcd(a,h)=1. Define the consecutive integer interval

```
K=[−floor((h−1+a)/15), floor((h−1−a)/15)].
```

The centered equation a(15j+1)=a+15k modulo15h gives
j=a^(-1)k modulo h. Put d=gcd(h,6). Because the unit residue classes modulo6
are preserved by multiplication by a unit, the row's whole-space charge
Q(h,a) on E is exactly

| d | Q(h,a) |
| --- | --- |
| 1 | #K/(3h) |
| 2 | 2 #{k in K: k odd}/(3h) |
| 3 | #{k in K: 3 does not divide k}/(2h) |
| 6 | #{k in K: k mod6 is1 or5}/h |

Counting the indicated arithmetic progressions gives, respectively, the
upper bounds

```
ceil(2h/15)/(3h),
2ceil(h/15)/(3h),
ceil(2h/45)/h,
2ceil(h/45)/h.
```

In all four cases Q(h,a)<=2/45+2/h. Hence Q>=1/15 forces h<=90. Direct exact
substitution of the short K interval for2<=h<=90 yields precisely these
possibilities:

| h | Numerators a with Q>=1/15 | Q |
| --- | --- | --- |
| 5 | 1,2,3,4 | 1/15 |
| 10 | 7,9 | 1/15 |
| 12 | 5,7,11 | 1/12 |
| 18 | 1 | 1/9 |
| 20 | 1,3 | 1/15 |
| 24 | 1,5,7 | 1/12 |
| 30 | 1,7,11,13 | 1/15 |

This finite table has19 rows before equal residue sets are identified; no
deduplication is used in the implication.

## Excluding every other divisibility class

The five remaining rows cover E, so one has whole-space charge at least1/15.
If none of18,24,30 divides M, the displayed table permits only h=12:
6 already divides M; a period carrying factor5 would force30|M, while
period18 or24 would directly contradict the assumption.

After selecting this period12 row, the current joint period is12. Moreover
the hypothetical maximum has exactly2-adic valuation2 and3-adic valuation1;
otherwise24 or18 would divide M. In particular, M/12 is coprime to6.

For completeness, the needed residual-grid implication can be rederived
without assuming any earlier sketch. On a residual class modulo a current
joint period L, a new row of period h sees an equally spaced grid of
n=h/gcd(h,L) points. Its conditional fraction is at most ceil(2n/15)/n.
If p remaining rows cover a nonempty residual, some row therefore has
p ceil(2n/15)>=n. For p=4,3,2,1 the possible n are respectively

```
{1,2,3,4,8}, {1,2,3}, {1,2}, {1}.
```

Every nontrivial multiplier in these sets contains factor2 or3. But h divides
M and gcd(M/12,6)=1, so none can enlarge the joint period12. Thus each newly
chosen row must itself have period dividing12.

No maximal-anchor row with period dividing12 kills an index congruent to11
modulo12. This can be seen from the short list h=2,3,4,6,12. The first four
have only the residue0 when nonempty. At period12, the four allowed reduced
numerators1,5,7,11 give bad sets {0},{0,7},{0,5},{0,1}. All miss11.

Consequently the residual containing11 modulo12 remains nonempty at every
selection step, and the greedy argument exhausts all five remaining rows
without covering it. This contradiction proves the conditional theorem.

All danger inequalities are strict; equality1/15 is safe. The argument uses
common normalization and reduced periods only, with no coordinatewise
scaling. It makes no claim about eight-row or larger minimal covers.

The executable mathematical table is
`issue-297/mod6_conditional_rows.py`. Its exact conditional formula has been
compared against literal residue enumeration through period120; the table
needed by this proof ends at90, and the displayed analytic bound covers the
entire remaining tail.

