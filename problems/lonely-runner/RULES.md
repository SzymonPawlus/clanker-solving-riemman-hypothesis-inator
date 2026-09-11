# Rules — Lonely Runner Conjecture

Problem-specific.  The repo-wide protocol in [`../../RULES.md`](../../RULES.md) applies in full;
this file adds the controls needed for a Diophantine problem where a finite computation can be
complete only through a delicate reduction theorem.

## 0. The dominant failure modes

Numerical sampling can miss an isolated valid endpoint, and an enormous finite search says
nothing about the conjecture unless a proved theorem reduces every normalized integer vector to
that search.  The governing rules are therefore:

- floating-point output is exploratory only;
- endpoint inequalities are checked exactly and are nonstrict on the witness side;
- every finite box and every quotient of it is stated exactly; and
- computational exhaustiveness is never inferred beyond the hypotheses of its reduction theorem.

The preprints at the current frontier are load-bearing literature, not axioms.  Their theorem
hypotheses and certificate semantics must be reconstructed from the papers before their
conclusions are used.

## 1. Mandatory sanity filters

Before writing up an argument or program, report the outcome of all four filters.

1. **Quantifier filter.** The input is an arbitrary tuple of nonzero integer velocities and the
   output is one common real time.  Do not choose a different time for each coordinate.  If a
   physical distinct-speed formulation is used instead, state and prove the translation.
2. **Boundary filter.** A witness satisfies
   \(\lVert t v_i\rVert\geq1/(k+1)\).  Thus the forbidden arcs use the strict inequality `<`,
   while equality is success.  Test a fixture whose only reported witness is an endpoint.
3. **Scaling filter.** Common integer scaling and gcd normalization are valid; coordinatewise
   scaling is not.  Any further canonicalization requires its own proof.
4. **Dimension filter.** State both the number \(k\) of moving velocities and \(k+1\) total
   runners.  In this directory the frontier target is currently \(k=14\), fifteen total runners,
   at threshold \(1/15\).

## 2. Exact computation and certificates

A checker must represent integers and rationals exactly.  It must not decide success from a
floating-point distance, tolerance, rounded logarithm, or plot.

For one fixed vector, the forbidden set for speed \(a=|v_i|\) is

\[
 B_a=\{t\in\mathbb R/\mathbb Z:\lVert at\rVert<1/(k+1)\}.
\]

Its endpoints are rational.  A no-witness certificate must give an exact covering of the entire
circle by these **open** arcs, including a convention that proves what happens at every endpoint.
A witness certificate is simply an exact rational \(t\) together with the coordinatewise integer
inequalities certifying the lower bound.

Every finite campaign must record:

- the normalized input set before sieving;
- every symmetry quotient and a proof that representatives are complete;
- each sieve as a mathematical implication, separately from its code;
- exact counts after every stage; and
- the finite-reduction theorem, with all hypotheses instantiated.

Large computations must be resumable and must bind their certificates to code and input versions
with hashes.

## 3. Independent verification and status

- A prose special-case proof remains `sketch` until cross-examined by the other model family; it
  may then earn `verified:review`.
- A sorry-free formal proof may earn `verified:lean`.
- A bounded search with no counterexample is `numerical`, even when exact and exhaustive in its
  stated box.
- A positive finite-case proof that relies on a published reduction cannot outrank the weakest
  status of that reduction.
- A proposed counterexample is an extraordinary claim.  It requires the explicit normalized
  vector and two independently implemented exact circle-covering checks.  Do not merge it on one
  solver's infeasibility report.

The independent checker must be written from the mathematical certificate specification, without
reading, importing, or translating the author's checker.

## 4. Frontier discipline

As of 2026-09-11, arXiv:2609.02604v1 claims \(k=13\) (fourteen total runners), superseding the
frontier stated in the initial campaign issue.  Treat this as a fresh primary-source claim pending
reconstruction.  Work aimed at the next uncovered finite case must say \(k=14\), fifteen total
runners; work auditing the preprint must say \(k=13\).

If a newer claimed finite case appears, update the README and target deliberately.  Do not silently
continue advertising an already-claimed case as open.

## 5. Useful targets

1. Independently reconstruct and test the single-vector exact interval semantics.
2. Reproduce one published case, including the finite-reduction hypotheses rather than only the
   inner modular search.
3. Audit Allikvere's 111 gate certificates with an independently specified checker.
4. Add proved structural sieves (congruence, divisibility, sparse spectra) for \(k=14\).
5. Only then attempt a complete \(k=14\) finite campaign.
