# Contact-graph lift for circle-packing candidates

**Status: `numerical`.** This directory diagnoses floating-point candidates and
constructs a candidate polynomial system. It does not produce a certificate yet,
does not establish optimality, and must not write to `problems/**/results/`.

Issue: [#11](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/11).

## Scope and dependency boundary

The input is an `out/nNN.json` candidate from
[`../circle-packing-search/`](../circle-packing-search/). This attempt owns only
`experiments/circle-packing-lift/**`; it reads but never modifies search output.

PR #16's exact checker is intentionally **not imported**. Its current untrusted-input
resource-exhaustion blocker does not prevent us from extracting contacts, checking
tolerance stability, or specifying the algebraic system. A future exact/interval
certificate must pass the checker after that blocker is fixed, but this numerical
front-end can be developed independently.

## First gate: is there a stable square system?

For points in the unit equilateral triangle and measured minimum separation `m`,
the active equations are

```text
(xi-xj)^2 + (yi-yj)^2 - m^2 = 0       pair contact i--j
yi = 0                                  bottom-wall contact
sqrt(3) xi - yi = 0                     left-wall contact
sqrt(3) (1-xi) - yi = 0                 right-wall contact
```

`analyze.py` extracts the active set at several absolute tolerances. A candidate
passes this first gate only if the contact signature is identical at `1e-6`,
`1e-8`, and `1e-10`. It then forms the Jacobian with columns
`x0,y0,...,x(n-1),y(n-1),m`, reports its numerical rank, and selects a maximal
independent subset of contact equations. Full column rank is evidence that the
chosen equality system locally isolates the candidate; it is not an exact proof.
For a stable, full-rank core, `solve.py` then applies Decimal Newton at 100 digits
to an independent square subsystem and checks the residual of **every** active
equation, including redundant rows.

### Rattlers: a correction to the issue sketch

“Fewer than three contacts” is not a sound rattler criterion by itself. Two
independent contacts can isolate a point locally, while three collinear constraint
normals need not. This code reports only points of degree **zero or one** as
`obvious_rattlers`: with all other points fixed, they have an immediate feasible
motion away from their sole contact or into the triangle. Degree two is left to a
real rigidity test. The code also reports the full rank deficiency; a later stage
must certify any less obvious jammed core using an infinitesimal-motion/inequality
test, not a degree-three threshold.

## Reproduce the current gate

No third-party runtime dependency is used:

```bash
./run.sh
```

The known nontrivial candidates currently give stable signatures:

| n | pair contacts | wall contacts | obvious rattlers | core rank / columns |
|---:|---:|---:|---|---:|
| 8  | 9  | 9  | none | 17 / 17 |
| 11 | 11 | 11 | point 6 | 21 / 21 |
| 13 | 18 | 12 | none | 27 / 27 |
| 16 | 21 | 13 | point 4 | 31 / 31 |

These are numerical diagnostics of the checked-in float files, not statements about
all optimal packings for those `n`.

As a calibration, the `n=8` Newton lift recovers

```text
m = (sqrt(33) - 3) / 8
```

to more than 90 decimal places, with every extracted active equation below a
`1e-80` residual. This validates the candidate-system construction numerically;
recognizing the published expression is not an exact certificate.

`exact_n8.py` then reconstructs the corresponding coordinates in the field
`Q(sqrt(3),sqrt(11))` and self-checks all 28 distance and 24 containment
inequalities without floats. The resulting candidate is
`candidates/n008-lifted.json`. It deliberately remains `status: numerical`:
the check was written by the same author, so the problem's independent-checker
gate has not been met.

For the open `n=16` candidate, the core lift also converges at 100 digits. A
250-digit PSLQ run (`./recover_n16.sh`, using the neighbouring search experiment's
pinned `mpmath==1.3.0`) finds no relation through degree 9 and proposes at degree 10

```text
331654 m^10 - 1211242 m^9 + 1925755 m^8 - 1772356 m^7
 + 1055998 m^6 - 429448 m^5 + 121624 m^4 - 23836 m^3
 + 3112 m^2 - 246 m + 9 = 0.
```

This is recorded in `findings/n016-minpoly-candidate.json` as `numerical`. PSLQ
does not prove exact vanishing or minimality; the polynomial is a concrete target
for elimination/substitution, not yet an algebraic certificate.

`exact_poly_n16.py` advances only the intrinsic algebra of that target, using exact
integer/rational arithmetic with no CAS dependency.  A Rabin test proves that its
reduction modulo 43 is irreducible; since the polynomial is primitive, Gauss's
lemma proves irreducibility over `Q`.  A Sturm sequence proves that it has exactly
two real roots and exactly one root in
`[216227269309781821/10^18, 216227269309781822/10^18]`, the interval containing the
Newton lift.  These are exact facts about the proposed polynomial, **not** proof
that the contact system's separation is its root.  The missing elimination link
keeps the finding and the whole directory at `numerical`.

## Next stage

An interval-Newton box can certify existence and uniqueness of the contact-system
root, but a nondegenerate coordinate box cannot directly certify a **tight** packing
under the current certificate semantics: interval evaluation around an exact contact
necessarily includes overlapping points. The useful next step is therefore exact
algebraic recovery (as calibrated for `n=8`) or a richer root-existence proof artifact,
followed by an independent exact checker. Do not label a tight interval box as a
feasible packing merely because it contains one feasible root.
