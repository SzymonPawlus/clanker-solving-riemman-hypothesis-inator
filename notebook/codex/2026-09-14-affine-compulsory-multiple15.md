# A compulsory multiple-of-fifteen slope in small affine covers

Status: `sketch`, pending Claude or human review. This is a new helper
argument derived directly from the common positive-strip condition. It
does not assume any computational cover classification or lifting lemma.

Let integer pairs `(a_i,b_i)`, with `a_i!=0`, have a common point `x` with
`0<a_i x+b_i<1`. Suppose the strict bad sets

```
||a_i z+b_i/15||<1/15
```

cover all open cells cut out by their endpoints. If no slope `a_i` is
divisible by 15, there must be at least ten rows. Consequently every
eight-row affine open-cell cover with a common positive strip contains
a slope divisible by 15. The condition is on the slope, not on a
constructed original velocity or its reduced period.

## Proof

Write `alpha_i=a_i x+b_i`, so `0<alpha_i<1`, and test the fifteen common
circle points `z_j=(x+j)/15 (mod 1)`, for `j=0,...,14`. The phase of row
`i` is `(a_i j+alpha_i)/15 (mod 1)`. None of these points is an endpoint
of any row: a boundary would require `a_i j+alpha_i` to be an integer
congruent to 1 or -1 modulo 15. Thus every tested point must be covered
under the open-cell hypothesis. Its strict badness is exactly

```
a_i j == 0 or 14 (mod 15).
```

There are eight unit residues `j` modulo 15. If `15` does not divide
`a_i`, then `a_i j` cannot be zero at a unit `j`. The alternative
`a_i j=14` requires `a_i` to be a unit too; each unit slope residue
covers exactly one of these eight unit indices. Therefore at least
eight rows with unit slopes are necessary, representing all eight unit
residues modulo 15.

At `j=3`, the residue `3a_i` cannot be 14, so some additional row must
have `5|a_i`. At `j=5`, some additional row must have `3|a_i`. These
two rows are not unit rows and cannot be the same row unless `15|a_i`,
which was excluded. Hence at least `8+1+1=10` rows are necessary.

This lower bound is sharp for the fifteen-point residue problem alone:
take all eight unit slope residues and add one residue of gcd 3 with 15
and one of gcd 5 with 15. This observation is not a claim of a ten-row
continuous affine cover in a common positive strip.

## Exact check and scope

`helper_affine_residue15_audit.py` checks all `2^14=16384` subsets of
nonzero slope residues. It finds minimum residue-cover size ten and
exactly eight minimizing residue sets. A separate literal phase check
uses all 160 nonzero integer slopes from -80 through 80 at `x=2/163`,
and all fifteen common points: all 2,400 strict inequalities agree with
the residue rule, with no boundary coincidences.

The motivating target remains fourteen moving, fifteen total runners,
at 1/15. Every argument uses one common phase and safe equality; no
coordinatewise scaling is used. This lemma supplies a necessary sieve
for the affine-template search. It neither establishes that a qualifying
template exists nor excludes all templates containing a multiple of 15.
