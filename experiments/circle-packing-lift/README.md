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
normals need not. This code therefore reports only **zero-contact points** as
`obvious_rattlers`; they have two completely absent Jacobian columns. It also
reports the full rank deficiency. A later stage must certify the actual jammed core
using an infinitesimal-motion/inequality test, not a degree threshold.

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

These are numerical diagnostics of the checked-in float files, not statements about
all optimal packings for those `n`.

As a calibration, the `n=8` Newton lift recovers

```text
m = (sqrt(33) - 3) / 8
```

to more than 90 decimal places, with every extracted active equation below a
`1e-80` residual. This validates the candidate-system construction numerically;
recognizing the published expression is not an exact certificate.

## Next stage

Validate a small interval box with interval Newton or a Krawczyk operator. Start
with the lifted `n=8` system above, whose published algebraic value is known. Any
minimal-polynomial recovery is conjectural until substitution and an exact/rigorous
interval feasibility check certify the resulting coordinates.
