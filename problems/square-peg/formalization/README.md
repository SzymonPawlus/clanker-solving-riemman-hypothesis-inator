# Square Peg formalization

This directory contains the issue #134 formalization interface for the
`C^{0,2-var}` prescribed-angle rectangle argument discussed in PR #122.
It is a dependency specification and conditional reduction, not an
unconditional proof of Square Peg.

## Files

- `c02var-prescribed-angle-formalization.tex` gives the precise mathematical
  interfaces, elementary proofs, and dependency/status ledger.
- The executable Lean counterpart is
  `../../../lean/Verified/SquarePeg/C02Var.lean`. It must be reachable from
  `../../../lean/Verified.lean` to be checked by CI.

## Exact status

- Fine-mesh and interpolation estimates: proved in the LaTeX draft.
- Regular parametrized `C^∞` smoothing: **UNKNOWN**.
- Excursion and planar-current package: **STANDARD-ASSUMED** and requires
  source pinning or a formal proof.
- Boedihardjo–Geng and generalized Green inputs: cited external interfaces.
- Asano–Ike approximation criterion: **UNKNOWN/CITED-UNVERIFIED** for this
  formalization-status ledger.
- Four-distinct/off-diagonal nondegeneracy (`AI_ND`): **UNKNOWN**, exposed as
  a separate hypothesis.
- Positive-size square: **CONDITIONAL** on all external interfaces, including
  `AI_ND`.

No `axiom`, `sorry`, or `native_decide` may be counted as proof. A Lean file
that merely packages the external interfaces can compile while proving only
the logical reduction from those hypotheses.

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
