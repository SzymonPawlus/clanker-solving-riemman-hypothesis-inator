# The Lonely Runner Conjecture

**Status:** open in general.  A preprint posted on 2 September 2026 claims the case of fourteen
total runners.  Accordingly, the first case beyond the primary-source claims currently located
by this project is **fifteen total runners**, or fourteen nonstationary velocities in the
normalization below.  The fresh fourteen-runner claim has not yet been independently verified in
this repository.

Shared conventions: [`../README.md`](../README.md).  Repo-wide protocol:
[`../../RULES.md`](../../RULES.md).  **Problem-specific rules: [`RULES.md`](./RULES.md) — read
before working on this problem.**

## Exact formulation and conventions

For a real number `x`, let

\[
  \lVert x\rVert=\min_{m\in\mathbb Z}|x-m|
\]

be its distance to the nearest integer.  The arithmetic form of the Lonely Runner Conjecture is:

> For every integer \(k\geq 1\) and every tuple of nonzero integers
> \(v=(v_1,\ldots,v_k)\), there is a real \(t\) such that
> \[
>   \lVert t v_i\rVert\geq \frac1{k+1}\qquad(1\leq i\leq k).
> \]

This is the stationary-runner normalization: there are \(k+1\) total runners, one runner is
made stationary, and the \(v_i\) are the relative velocities of the other \(k\).  Thus
"fifteen runners" means \(k=14\) and the target separation is \(1/15\).  Papers do not always
use the same counting convention; every note here must state both \(k\) and the total number of
runners.

The inequality is **nonstrict**.  A time at which one coordinate is exactly \(1/(k+1)\) is a
valid witness.  Zero velocities are excluded.  Repeated coordinates and opposite coordinates
are harmless in the arithmetic statement: they impose repeated constraints.

## Symmetries and normalization

The following operations preserve the existence of a witness:

- permuting the coordinates;
- changing any signs, since \(\lVert-t v_i\rVert=\lVert t v_i\rVert\);
- multiplying every coordinate by the same nonzero integer; and
- dividing every coordinate by their positive gcd.

For the scaling claim, as \(t\) ranges over \(\mathbb R\), so does \(ct\).  Consequently every
integer instance may be normalized to
\(0<v_1\leq\cdots\leq v_k\) and \(\gcd(v_1,\ldots,v_k)=1\).  For a fixed original \(k\), its
constraint set may be represented by the distinct absolute values, but the threshold remains
\(1/(k+1)\): deleting a repeated constraint does **not** license reinterpreting the shorter list
as a lower-dimensional LRC instance.  **A finite search must not quotient by any further
operation without proving it preserves the quantified problem.**

The witness search may be restricted to \(t\bmod 1\), since all velocities are integers.  This
makes the domain the circle \(\mathbb R/\mathbb Z\), not an unbounded real interval.

## Current primary-source frontier

The table records what the cited sources claim; it is a reading map, not an in-repository
verification of their computer-assisted arguments.

| Moving velocities \(k\) | Total runners | Primary-source claim | Repository standing |
|---:|---:|---|---|
| \(10,11,12\) | \(11,12,13\) | Sungkawichai–Trakulthongchai give a computer-assisted proof | source located; proof/certificates not yet reconstructed |
| \(13\) | \(14\) | Allikvere gives a computer-assisted extension closing 111 prime gates | fresh source located; claim not independently verified here |
| \(14\) | \(15\) | no proof located as of 2026-09-11 | **active finite-case target** |

Primary sources:

1. Touch Sungkawichai and Tanupat Trakulthongchai,
   [*Eleven, twelve, and thirteen lonely runners*](https://arxiv.org/abs/2604.23906),
   arXiv:2604.23906v1 (2026).
2. Jaan Allikvere,
   [*Fourteen lonely runners*](https://arxiv.org/abs/2609.02604),
   arXiv:2609.02604v1 (2026).

The Allikvere preprint appeared only nine days before this snapshot.  Its existence changes the
frontier from \(k=13\) to \(k=14\); it does not become an assumable verified result merely by
being recent or by reporting exact certificates.

## Active directions

- Reconstruct the finite-reduction theorem and exact modular sieves in the two sources above,
  independently of their implementations.
- Reproduce a published finite case using a separately written exact checker before attempting
  \(k=14\).
- Develop exact congruence and divisibility sieves that discard structured families before the
  expensive finite reduction.
- Prove special cases for sparse absolute spectra and other structured velocity families.

See [`attacks/elementary-structural-sieves/`](./attacks/elementary-structural-sieves/) for the
first exact special cases at the new \(k=14\) frontier.
