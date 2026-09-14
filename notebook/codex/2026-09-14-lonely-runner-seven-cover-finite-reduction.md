# A finite reduction for primitive minimal seven-row maximal covers

Status: `sketch`, requiring cross-family or human review. No novelty claim is
made. This argument is self-contained and does not assume the earlier
twenty-pattern classification, the claimed seven-row lower bound, or any
Lonely Runner preprint.

## Theorem

Let M and w1,...,w7 be positive integers with 0<wi<M. Suppose the seven
speeds wi form an **inclusion-minimal** cover of all lower endpoints

```
t_j=(15j+1)/(15M),  j in Z/MZ,
```

using the strict bad condition `||wi t_j||<1/15`. If
g=gcd(M,w1,...,w7), then

```
M/g <= 1,048,320.
```

Consequently every such minimal seven-row cover is an integer scaling of a
finite primitive core: normalize by g, take an integer maximum at most the
displayed bound, and choose seven distinct smaller positive speeds. This is
a proved reduction to a finite candidate set, not a completed search of that
set or a classification of the candidates that actually cover.

Inclusion-minimality is essential to this formulation. Adding irrelevant
speeds to an already covering family may change its gcd without changing the
cover. The proof below must select all seven rows before the residual set
becomes empty.

## Reduced rows and the first period

For a row w put

```
h=M/gcd(M,w), a=w/gcd(M,w), gcd(a,h)=1.
```

Its bad indices depend only on j modulo h. The map
`j -> a(15j+1) mod15h` bijects j modulo h with the residues congruent to a
modulo15. The centered bad representatives are precisely the integers
e in `[-h+1,h−1]` with e congruent to a modulo15. Thus the row has at most

```
ceil((2h−1)/15)
```

bad residues modulo h. Seven rows cover the whole index space, so at least
one has density at least1/7. Choose it first. Since

```
ceil((2h−1)/15) <= (2h+13)/15,
```

the inequality `7 ceil((2h−1)/15)>=h` forces h<=91. The lcm L of the first
selected period therefore satisfies L<=91. The sharper centered-integer
bound is needed here: the generic grid bound used next would permit h=98.

## Residual-fiber lemma

Let L be the lcm of the already selected row periods. The uncovered indices
are the lift of some nonempty set R in Z/LZ. Consider an unselected row of
period h and put

```
d=gcd(h,L), n=h/d.
```

For one uncovered residue j0 modulo L, its compatible indices modulo
lcm(L,h)=Ln are j0+sL for 0<=s<n. Under multiplication by a in the row
phase, these points are n equally spaced residues on the circle. Indeed
L/d is coprime to n, and a is coprime to h and hence to n, so their product
permutes the n positions.

An open danger arc of length2/15 contains at most ceil(2n/15) members of any
such equally spaced n-grid. This bound remains valid when a grid point is
exactly on an endpoint, because equality is safe and can only reduce the
number counted. The row therefore hits at most

```
ceil(2n/15)/n
```

of the indices in each residual fiber and hence of the entire residual set.
The argument does not assume coprimality with15.

## Greedy lcm growth

Suppose p rows remain. They cover the nonempty residual set, so at least one
hits at least1/p of it. The residual-fiber lemma forces its multiplier n to
belong to

```
E_p={n>=1 : p ceil(2n/15)>=n}.
```

Selecting this row replaces L by exactly Ln. The necessary multiplier sets
for the six successive choices are:

| Remaining rows p | E_p | Maximum |
| --- | --- | --- |
| 6 | 1,2,3,4,5,6,8,9,10,11,12,16,17,18,23,24 | 24 |
| 5 | 1,2,3,4,5,8,9,10 | 10 |
| 4 | 1,2,3,4,8 | 8 |
| 3 | 1,2,3 | 3 |
| 2 | 1,2 | 2 |
| 1 | 1 | 1 |

This is a tiny exact table, not an unbounded experimental cutoff. Since
ceil(2n/15)<=(2n+14)/15, membership in E_p implies
`(15−2p)n<=14p`. For p<=6 this bounds n by28 or less; substitution then
gives every entry in the table.

Inclusion-minimality ensures that every proper subset of the seven rows
leaves a nonempty residual, regardless of the ordering just chosen. Thus
the construction selects all seven rows and yields

```
lcm(h1,...,h7) <= 91*24*10*8*3*2*1 = 1,048,320.
```

Finally, checking prime exponents gives the exact identity

```
lcm_i(M/gcd(M,wi)) = M/gcd(M,w1,...,w7).
```

This proves the theorem.

## A smaller exact candidate domain

The actual multipliers constrain the maximum more strongly than the product
of their maxima. Define

```
H7={2<=h<=91 : 7 ceil((2h−1)/15)>=h}.
```

The argument shows that the primitive maximum belongs to the multiplicative
set `H7 E6 E5 E4 E3 E2 E1`. There are48 possible first periods and4324
distinct products. Removing maxima2,...,7, which cannot support seven
distinct smaller positive speeds, leaves exactly4318 candidate maxima.
Of these1746 are not divisible by18,24, or30. Their existence in this
necessary domain does not imply that they admit covers; it identifies the
remaining finite exclusion obligation for the old divisibility conjecture.

The solver-free checker regenerates the domain and optionally writes its
complete list to a supplied output path. The preserved list is
`issue-297/seven-cover-candidate-maxima.json`. It is a finite necessary
domain, not a claim that a search over its many velocity choices has been
completed.

## Relation to the fifteen-runner attack

The ambient target has fourteen moving velocities and fifteen total runners,
with one common witness time at threshold1/15. This theorem concerns a
specific endpoint-cover subproblem. It does not show that every fourteen-speed
tuple contains a minimal seven-row maximal cover; minimal covers with eight
or more rows are outside its scope. It also does not establish the actual
list of primitive seven-row covers within the finite bound.

Signs may first be removed because `||(-w)t||=||wt||`. Common normalization
by g preserves all row periods and endpoint incidences. No coordinatewise
scaling is used. All forbidden inequalities are strict and all eventual
witness inequalities are nonstrict.

The checker `issue-297/check_seven_cover_reduction.py` reconstructs the entire
multiplier table by exact integer arithmetic, checks the product, compares
the reduced-row counts with their centered-residue bounds, and checks the
conditional grid bound in a finite diagnostic range including numerators
divisible by3 or5. Those diagnostics support the implementation; the
unbounded claims follow from the displayed proofs, not from that finite range.
