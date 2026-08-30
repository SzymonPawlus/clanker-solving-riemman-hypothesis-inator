# Square Peg formalization

This directory contains the issue #134 formalization interface for the
`C^{0,2-var}` prescribed-angle rectangle argument discussed in PR #122.
It proves the prescribed-angle rectangle result for the stated vanishing
critical `2`-variation class. It does not claim the full conjecture for every
Jordan curve.

## Files

- `c02var-prescribed-angle-formalization.tex` gives the precise mathematical
  interfaces, elementary proofs, and dependency/status ledger.
- `c02var-prescribed-angle-formalization.pdf` is the generated, reviewable
  build of that source.
- The executable Lean counterpart is
  `../../../lean/Verified/SquarePeg/C02Var.lean`. It must be reachable from
  `../../../lean/Verified.lean` to be checked by CI.

## Exact status

- Fine-mesh and interpolation estimates: proved in the LaTeX draft.
- Regular parametrized `C^∞` smoothing: **PROVED** by periodic mollification,
  with regularity, global injectivity, seam compatibility, and the explicit
  `1`-variation bound discharged.
- Excursion/current winding estimate: **PROVED**, using exact independently
  checked Jordan, isodiametric, index-integrability, and Green citations.
- Boedihardjo–Geng and generalized Green inputs: **CITED**, with exact
  version/theorem/page and independently checked hypotheses.
- Asano–Ike approximation and four-distinct/off-diagonal conclusion:
  **CITED**, arXiv:2412.21057v3, Theorem 1.1 (p. 2), definition/discussion
  (pp. 2–3), and Theorem 4.1 proof (p. 19).
- Positive-size square for the stated class: **PROVED** from those cited
  inputs and the internal perpendicular-diagonal lemma.

The Lean module formalizes only the elementary algebraic core, not the whole
analytic proof. No `axiom`, `sorry`, or `native_decide` may be counted as
proof, and the LaTeX theorem must not be labelled `verified:lean`.

## Checks

Build from the repository's `lean/` directory:

```sh
lake build Verified.SquarePeg.C02Var
lake build
```

Before any `verified:lean` claim, run `#print axioms` on each exported theorem
and record the output. Only the repository-permitted standard Lean axioms may
appear; `sorryAx` or a newly declared axiom means the result is not verified.

Compile the mathematical specification from the repository root with:

```sh
pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory=/tmp \
  problems/square-peg/formalization/c02var-prescribed-angle-formalization.tex
```

There is currently no `problems/square-peg/RULES.md`. Root `RULES.md` is
therefore the governing protocol; the missing problem-level protocol does
not authorize a status promotion.
