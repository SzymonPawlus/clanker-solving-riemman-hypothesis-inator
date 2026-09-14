# Deterministic witness extraction from a uniform-fiber certificate

Status: `sketch`, conditional on the separately frozen issue-304 certificate.
This note does not promote that certificate, claim novelty, or solve the full
fifteen-runner conjecture.

## Statement and scope

Let P be one of the eight-speed primitive cores for which a nonnegative
uniform-fiber certificate of mass greater than six has been established.
For any positive integer c and six additional nonzero integer speeds with
absolute values below c max(P), a common witness can be found using
O(log²(c+1)) exact arithmetic operations. The constants depend on P and its
fixed number of primitive endpoint types. This is an arithmetic-operation
bound, not a unit-cost bit-complexity claim.

The implementation defaults to P={1,5,6,7,9,11,13,18}. Its output is directly
checked against every supplied coordinate with exact nonstrict inequalities.
Signs and duplicate absolute speeds may be removed because they impose the
same constraint. There are fourteen moving velocities, fifteen runners total,
and one common time at threshold 1/15. Common scaling is used throughout;
individual speeds are never rescaled.

## Positive integer scores

For a primitive endpoint x=(15r+1)/(15u) good for P, its c lifts are

```
t_j=(15u j+15r+1)/(15u c),  0<=j<c.
```

For an integer interval I of lift indices define

```
S_x(I)=|I|−sum_(additional w) #{j in I : ||w t_j||<1/15}.
```

The score is additive over disjoint integer intervals. If z_x are the
nonnegative primitive weights of the universal certificate, of total mass
T>6, each additional column has uniformly lifted mass at most one. Hence

```
sum_x z_x S_x([0,c)) >= c(T−6)>0.
```

Some fiber has a positive integer score. Its identity can be found by exact
counting over the fixed finite collection of primitive fibers; no LP or
certificate optimization is run during extraction. Bisect its index interval.
At least one half has positive score because the two scores sum to the
positive parent score. Retain a positive half and repeat.

After at most ceil(log₂c) bisections, a singleton {j} has positive score
1−number_of_bad_extra_coordinates. As this integer is positive, its bad
coordinate count is zero. The selected t_j was already good for cP, giving
the required common witness. Its unreduced denominator is at most
15 max(P)c, so its representation has O(log c) bits.

This extraction only uses the frozen certificate as an existence guarantee.
Every reported time is independently checked by multiplying integers and
testing 15 min(w a mod b,−w a mod b)>=b for t=a/b.

The same argument works for any finite rational primitive support, including
the interior-time supports used by the separate twenty-core certificates.
For x=A/B, replace the endpoint expression by t_j=(Bj+A)/(Bc). Let D=Bc
and H=ceil(D/15). An integer residue is strictly bad exactly when it is
less than H or greater than D−H. Its indicator is again
`1+floor((z_j+H−1)/D)−floor((z_j+D−H)/D)`, where z_j=w(Bj+A).
Thus the Euclidean count and bisection apply without requiring B divisible
by15. The implementation is `issue-297/rational_witness.py`.

## Exact modular interval counts

Put h=uc, D=15h and z_j=w(15u j+15r+1). The strict bad indicator is

```
1 + floor((z_j+h−1)/D) − floor((z_j+14h)/D).
```

To verify it, reduce z_j modulo D. Residues 0,...,h−1 and 14h+1,...,D−1
give one; the closed interval h,...,14h gives zero. In particular, both
threshold endpoints are safe. This is why the first numerator contains h−1.

Summing over j=L,...,R−1 gives the interval length plus two sums of the form

```
F(N,D,a,b)=sum_(0<=i<N) floor((a i+b)/D).
```

Euclidean descent computes F in O(log D) arithmetic operations. First extract
the integer quotients of a and b by D; their contributions are respectively
quotient(a) N(N−1)/2 and quotient(b) N. For the reduced 0<=a,b<D, put
Q=floor((aN+b)/D) and R=(aN+b) mod D. If a>0, the exact recurrence is

```
F(N,D,a,b)=F(Q,a,D,R).
```

Indeed, summing by positive lattice levels gives
`sum_(h=1..Q) [N−ceil((hD−b)/a)]`. Each summand is
`floor((aN+b−hD)/a)`; reversing h gives the displayed recurrence. The final
possibly empty lattice level contributes zero. This transposition exchanges
D with a and therefore follows the Euclidean algorithm. The case a=0
terminates. No floating point is used.

The number of additional coordinates and primitive fibers is fixed. At most
O(log(c+1)) interval evaluations, each requiring O(log(c+1)) Euclidean
arithmetic steps, prove the announced operation bound. Intermediate integers
have O(log(c+1)) bits.

## Reproducible validation

The exploration and direct witness checks are in
`issue-297/witness_bisection.py`. The companion
`issue-297/check_witness_bisection.py` compares 10,000 signed Euclidean sums
and 20,000 modular interval counts against direct integer enumeration.
It also checks all 210 choices of six distinct unused speeds below18 at c=1
and exercises much larger scales without materializing their endpoint sets.

The endpoint fixture P union {3,4,8,10,14,15} returns t=31/75, with minimum
distance exactly1/15. Negative copies give the same witness; repeated absolute
speeds preserve the constraints. These are boundary and normalization checks,
not a finite reduction for arbitrary fourteen-speed tuples.
