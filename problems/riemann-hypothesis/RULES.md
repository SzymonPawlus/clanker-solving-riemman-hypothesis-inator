# Rules — Riemann Hypothesis

Problem-specific. The repo-wide protocol in [`../../RULES.md`](../../RULES.md) applies in full.

---

## 0. Status of this directory

RH is the repo's joke target and its hardest case. Unlike
[`../circle-packing-equilateral-triangle`](../circle-packing-equilateral-triangle) and
[`../woodalls-conjecture`](../woodalls-conjecture), there is **no realistic partial result an
agent can produce that constitutes progress on the conjecture itself.**

Treat this directory as a formalisation and exposition exercise, not an attack. If you want to do
work that might actually matter, work on one of the other two problems.

## 1. What counts as a contribution here

Only these:

1. **Formalising a classical result** in Lean — a step toward Mathlib-quality analytic number
   theory. This is the main legitimate activity.
2. **Correctly stating a known equivalence** (Robin, Lagarias, Nyman–Beurling, Li, Weil
   positivity) with citations, so it is available to reason about.
3. **Numerical exploration** of zeros, clearly marked `numerical`.
4. **Pinning the `README.md` landscape table to primary sources** — it is currently unverified.

## 2. What does not count

- A new "approach" to proving RH. The space of natural ideas is exhaustively explored; anything
  an agent generates in a session is, with overwhelming probability, either known or wrong.
  Before opening an attack issue, find the idea in the literature and cite where it fails.
- Reformulating RH into an equivalent statement and treating that as progress. Equivalences are
  cheap; the difficulty is invariant under them.
- Numerical verification of more zeros. This has been done to $\sim 10^{13}$ and additional
  zeros carry no information about the conjecture.

## 3. Extraordinary claims

`../../RULES.md` §7 applies with maximum force. Any PR asserting a proof of RH, or a proof of
any statement known to imply RH, must be labelled `extraordinary-claim`, must not be merged, and
requires both humans.

Specifically: if you find yourself with a short argument for RH, the error is real and locating
it is the actual task. Write up where the argument breaks — that is the useful output, and it is
genuinely interesting.

## 4. Lean specifics

Mathlib's `RiemannHypothesis` is the canonical statement; alias it rather than restating it (see
`../../lean/Verified/RiemannHypothesis/Basic.lean`). A locally restated variant that looks
equivalent is a standard route to proving something strictly weaker without noticing.

Confirm every Mathlib name with `#check` or by grepping the source. See
[`../../lean/README.md`](../../lean/README.md).
