# Universal measures for 160 explicit nine-speed cores

Status: `sketch`; exact author generation and standalone replay passed,
fresh independent checking in progress. This is separate from the frozen
seven-row proofs. The census is bounded, but each individual measure proves
an all-scale statement within its explicitly stated core family.

## Claim and sanity filters

For every explicitly listed nine-speed pattern `P` in
`issue-304/eight-core-phase-to30.json`, every positive integer `c`, and every
set of at most five arbitrary positive integer speeds below `c max(P)`,
there is one common rational time at which every speed in the combined set
has distance at least `1/15` from an integer.

There are fourteen moving velocities and fifteen total runners. Negative
velocities can be replaced by absolute values; repetitions add no constraint.
All coordinates use the same time. Only the nine-speed core is scaled by
the one common integer `c`; the five added speeds may have any residue
classes. Forbidden arcs are strict. In particular, both `1/15` and `14/15`
are allowed for speed one, while zero is forbidden.

The 160 patterns come from the helper's exact census of every eight-element
subset of `{1,...,M-1}` for `9<=M<=30`: 14,307,150 subsets, no symmetry
quotient. Every listed core covers the maximal lower endpoints, has a
private endpoint for every one of its eight smaller speeds, and has gcd
one. Their maxima are 20 (16 cores), 22 (3), 24 (12), 26 (1), and 30 (128).
No unbounded classification of eight-row covers is asserted.

## Complete mathematical certificate specification

Each case supplies positive rational atom weights `z_i` at rational times
`x_i` in `[0,1)`. Check directly that every fixed speed is allowed:

```text
||v*x_i|| >= 1/15 for every v in P,
5 < T=sum_i z_i <= 51/10.
```

For every `1<=n<=14`, every `1<=q<max(P)*n` with `gcd(n,q)=1`, excluding
`q in P` only at `n=1`, check the exact strict count

```text
sum_i z_i * #{0<=k<n : ||q(k+x_i)/n||<1/15} <= n.
```

These are the complete finite inequalities. The atom-search grid is not a
claim of completeness and need not be independently reconstructed: atom
safety, positivity, mass, and the displayed columns are sufficient.

To prove the claim, at scale `c` give each time `(k+x_i)/c`, for `0<=k<c`,
weight `z_i/c`. It is allowed by every scaled fixed speed and total mass
stays `T`. For an arbitrary added speed `w`, put `d=gcd(c,w)`, `n=c/d`,
`q=w/d`. The bad weight is the displayed finite count divided by `n`,
because the `c` fibers consist of `d` repeats of the reduced `n` fibers.
Multiplication by `q` permutes those reduced equally spaced points.

For every denominator `n>=15`, each atom contributes at most
`ceil(2n/15)` bad points, so its total load is bounded by

```text
(51/10) ceil(2n/15)/n
 <= (51/10)(2n+14)/(15n)
 <= 1,
```

where the last inequality is `714<=48n`, true for `n>=15`. Thus every
added speed kills weight at most one. Five added speeds kill weight at
most five, less than `T`; a single supported rational time survives all
coordinates. Strict bad arcs preserve equality as success throughout.

The stronger denominator tail beginning at eleven is also available, but
is not needed or assumed by this certificate format.

## Review and scope

An independent checker should implement the mathematical specification
above without reading or importing the author discovery or checking code.
It can additionally compare the 160 pattern tuples against the separate
bounded census, and directly validate all private endpoint certificates.

Four of the eight-row cores omit period two; all four have maximum 24.
Hence the newly proved seven-row period-two necessity does not extend to
eight rows without further restrictions. These explicit examples are not
counterexamples to Lonely Runner; their universal measures establish
loneliness for every five-speed completion at all common scales.

The frozen author replay checks 289,120 finite columns and 3,344 positive
atoms. The smallest total mass is `50981/10000`; the greatest finite load
is `19999/20000`. The manifest SHA-256 is
`5598c63635bf372fbac906943da45ede93c7e5a9b827d49787132a8b9cf676ec`.
It remains unchanged during independent review.
