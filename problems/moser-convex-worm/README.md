# Convex Moser worm problem

**Campaign status:** open landscape under independent source audit. No numerical
or record claim in this directory is assumable until it satisfies
[`RULES.md`](./RULES.md).

Repository protocol: [`../../RULES.md`](../../RULES.md). Shared problem layout:
[`../README.md`](../README.md).

## Statement

A **worm** is a continuous rectifiable planar arc of length $1$. A convex
planar set $K$ is a **universal convex cover** if, for every worm $W$, some
orientation-preserving rigid motion sends $W$ into $K$. Define

\[
  m_{\mathrm{conv}}
  = \inf\{\operatorname{area}(K):K\text{ is a universal convex cover}\}.
\]

The active hypothesis is to determine or improve rigorous bounds on
$m_{\mathrm{conv}}$. Reflections are not included in the rigid-motion
convention; a witness family must therefore state explicitly whether its own
symmetries make reflection irrelevant.

## Pinned baseline target

Khandhawit and Sriswasdi state that any convex region containing congruent
copies of all three of the following objects has area at least `0.227498`:

1. a unit segment;
2. an equilateral triangle of side $1/2$, forced by a two-edge polygonal arc
   of total length $1$;
3. a square of side $1/3$, forced by a three-edge polygonal arc of total
   length $1$.

Every universal convex cover contains a congruent copy of each witness, so the
paper claims $m_{\mathrm{conv}}\ge 0.227498$. The first campaign gate is an
independent reconstruction of its grid/error argument. The source archive has
no checker or certificate, and preliminary inspection found decimal and
second-order error bookkeeping that must be repaired before the printed value
can be treated as independently verified. The publication claim itself is
`cited`; its proof is not yet an assumable in-repository result.

Primary source: T. Khandhawit and S. Sriswasdi, *An Improved Lower Bound for
Moser's Worm Problem*, arXiv:math/0701391v2 (2009), 12 pages,
<https://arxiv.org/abs/math/0701391v2>.

This requested reproduction is a historical baseline, **not the current
published record**. Khandhawit, Pagonakis, and Sriswasdi later proved the
stronger convex-cover bound $m_{\mathrm{conv}}\ge 0.232239$ in *Lower Bound
for Convex Hull Area and Universal Cover Problems*, arXiv:1101.5638v1,
published in *International Journal of Computational Geometry and
Applications* 23 (2013), 197--212,
<https://arxiv.org/abs/1101.5638>. Its full argument and witness dimensions
remain an independent literature-audit task; only the primary abstract is
pinned here initially.

## Research target

Only after the baseline gate passes:

- add one explicit polygonal worm of total length exactly $1$;
- prove a lower bound for the minimum convex-hull area of simultaneous rigid
  placements of the four witnesses;
- first seek a certified value strictly larger than `0.227498` as requested;
- make no novelty claim unless the value also exceeds the independently
  verified current published lower bound, presently `0.232239`.

The fourth witness, all branch domains, and the positive margin over the
baseline must be explicit. A floating-point optimizer supplies candidates, not
a lower-bound proof.

## Current work

- Issue #136: independent source reconstruction of the published baseline.
- Issue #137: one-witness numerical search and certificate production.
- Issue #138: independent certificate schema/checker and formalization audit.
