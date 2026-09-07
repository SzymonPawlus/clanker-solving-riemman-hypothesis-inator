# Issue #170 — finite polygon bridge checkpoint

Date: 2026-09-02

Status remains `sketch` globally. The Lean algebra below is kernel-checked, but
the geometric existence layer is not yet complete.

## Completed in Lean

- cyclic scalar and determinant summation by parts over `ZMod n`;
- common-fan mixed-surface symmetry;
- self-surface equals cyclic shoelace twice-area;
- pointwise support containment implies mixed surface at most shoelace area;
- convex-coordinate support monotonicity;
- existence of an active maximizing vertex on each ray of a supplied finite fan;
- simultaneous active selection on a finite fan;
- repeated support-vertex insertion preserves chain and closed shoelace sums;
- sorted merge of two abstract ray ledgers, exact membership, and preservation
  of each sorted input as a sublist;
- a concrete four-quadrant algebraic ray key, positive-rescaling invariance,
  determinant/order equivalence in every quadrant, and the exact strictly
  sorted worm-normal ledger;
- cyclic reindexing invariance of surface and area;
- exact horizontal unit-base triangle determinant area;
- both base-apex triangles are subsets of any convex set containing their
  vertices;
- opposite base-apex triangles intersect only on the horizontal base line;
- a finite common-fan allocation theorem ending at half the containing
  polygon's shoelace sum.

`#print axioms` for the principal theorems reports exactly
`[propext, Classical.choice, Quot.sound]`.

## Remaining existence layer

The abstract fan merge and concrete algebraic key are complete. One must:

1. choose/rotate to a cyclic cut avoiding the finitely many rays;
2. show each convex polygon's outward edge ledger is sorted after cyclic
   rotation;
3. show active support vertices are constant between successive edge-normal
   rays and change by exactly the corresponding polygon edge;
4. transfer repeated-vertex insertion invariance back to the original cyclic
   shoelace polygon.

For the direct segment proof, convex containment, determinant triangle areas,
null intersection, and product-measure union additivity are complete. One
still needs to identify product measure of each convex-hull triangle with its
determinant area and connect the containing convex set to a finite polygon's
shoelace area.
The degenerate common-fan route can avoid measure theory once steps 1–5 are
complete.

No theorem equivalent to common-fan existence is assumed, and no `sorry`,
custom axiom, `unsafe`, or floating-point computation occurs in the Lean
module.
