# Rules — convex Moser worm problem

The repository-wide [`../../RULES.md`](../../RULES.md) applies in full. These
rules add the discipline required for a continuous rigid-placement and convex
area optimization problem.

## 1. Claim type

The campaign seeks **lower bounds** for the area of every universal convex
cover. An explicit finite witness family gives a valid reduction, but a lower
bound for that family's best simultaneous placement still requires a global
argument. A local optimizer, dense grid, or repeated convergence is only
`numerical` evidence.

State separately:

- witness validity: every listed polygonal arc has total length exactly $1$;
- finite-family reduction: every universal convex cover contains a congruent
  copy of every witness;
- global optimization: every simultaneous placement has convex-hull area at
  least the claimed constant.

The status of a combined claim is capped by the weakest item.

## 2. Fixed conventions

- Motions are translations followed by rotations; do not silently add
  reflections.
- Fix Euclidean gauge freedoms in every certificate: pin one witness placement
  and state the compact remaining parameter domain.
- Polygonal witnesses list vertices in traversal order. Their length is the
  sum of consecutive edge lengths; an unlisted closing edge is not part of the
  worm.
- Area means two-dimensional Lebesgue area of the convex hull of the union of
  the placed witnesses.
- A strict improvement over the historical baseline means a rigorously rounded
  lower endpoint greater than `0.227498`; it is not a literature improvement.
  A record improvement must rigorously exceed the independently checked current
  published lower bound, presently `0.232239`.

## 3. Baseline gate

No new-witness result may build on the published decimal until Issue #136 has
independently reconstructed the source's symmetry and compact-domain
reductions, minimal-position argument, geometric $f,g,h$ inequalities, and
directed trigonometric rounding. The grid search and its flawed error estimate
concern a separate numerical upper candidate and are not Theorem 1 premises.
Record the paper version and exact theorem used. If reconstruction certifies a
weaker decimal, that weaker value is the campaign baseline.

## 4. Certificates and independent checking

A computational lower-bound certificate must expose:

1. exact rational or algebraic witness vertices and exact unit-length proofs;
2. normalized placement variables and a complete compact search domain;
3. a finite subdivision/branch tree covering that domain;
4. for each leaf, outward-rounded interval bounds proving the claimed area
   inequality or a documented sound pruning lemma;
5. tool versions, rounding mode, and a deterministic replay command.

The producer's checker cannot grant `verified:review`. The other agent must
implement the mathematical predicates independently from this specification,
without importing or adapting producer code. Disagreement blocks the claim.

`verified:lean` requires a `sorry`-free formal proof of the finite certificate
and its geometric interpretation. An oracle call, custom axiom, `unsafe`, or
unverified floating-point evaluation does not qualify.

## 5. Cheap failure filters

Before reporting an improvement, verify all of the following:

1. the proposed fourth object is a rectifiable arc of total length exactly
   $1$, not a closed perimeter accidentally exceeding $1$;
2. every placement degree of freedom, including orientation and reflection
   convention, is covered;
3. the objective is the convex hull of the entire placed family, not sampled
   vertices missing edges;
4. minimization is global over the stated domain;
5. interval bounds are outward rounded and the final decimal is rounded in the
   conservative direction;
6. the witness/lower-bound route is checked against the current literature.

Failure of any filter is recorded under `attacks/` as `refuted` or
`numerical`, never promoted.

## 6. Realistic checkpoints

1. Reproduce the source's `0.227498` theorem independently.
2. Publish an exact schema, a producer implementation, and one independently
   written baseline checker (two implementations total).
3. Search simple one-parameter polygonal families and preserve negative data.
4. Certify one explicit four-witness lower bound.
5. Claim a strict improvement only after literature review and independent
   certificate verification.
