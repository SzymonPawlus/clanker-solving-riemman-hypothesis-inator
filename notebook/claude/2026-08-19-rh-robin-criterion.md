# 2026-08-19 — opening problems/riemann-hypothesis: Robin's criterion (issue #75)

First work in the RH directory. Chose Robin's criterion over Lagarias / Li /
Lean-statement because it has the crispest known-answer validation gate (the finite
exception list below 5041) and because exact arithmetic buys the most there:
sigma(n) is exactly computable, so the *only* analytic content is one transcendental
threshold, which mpmath interval arithmetic encloses certifiably.

Decisions worth remembering:

- **Two-tier check.** Doubles only in a conservative per-segment filter whose
  threshold is itself certified in interval arithmetic and down-shifted by a 1e-9
  relative margin (>> the filter's ~1e-15 rounding error). Anything flagged gets the
  real decision: exact sigma (recomputed independently by factorization) vs an
  outward-rounded interval enclosure of e^gamma·n·log log n at up to 200 bits.
  Zero load-bearing floating point. This pattern should be reusable for Lagarias's
  criterion (H_n exact as a rational, exp(H_n)·log(H_n) enclosed).
- **Validation gates before the long run**: (1) reproduce the 27 known Robin
  exceptions in [2, 5040] exactly — passed on first run; (2) 100k sieve values vs
  factorization sigma, 500 vs sympy — all exact. Only then launch.
- The first sieve segment massively over-flags (680 candidates) because the
  threshold uses log log L across a segment where log log n grows 18%; harmless,
  certification is ~1ms/candidate. All later segments flag zero.
- Egress proxy blocks arxiv/springer/etc., so the two classical inputs are cited
  from memory and flagged as such in the attack README. Did NOT fake a literature
  survey.
- Near-miss argmaxes come out primorial-shaped (multiples/truncations of
  720720 = 2^4·3^2·5·7·11·13 early on), consistent with the colossally-abundant
  prediction — a cheap structural sanity check that the sieve isn't subtly wrong.

Status of output: `numerical`, tier non-claim, nothing near results/. The attack
README says explicitly that the computation carries no information about RH itself;
problems/riemann-hypothesis/RULES.md §2 already makes the general point.

Post-run lesson worth keeping: my first `robin_decide` converted the interval
endpoints to ambient 53-bit mpf before comparing — a re-rounding that could in
principle move an endpoint past the true value, i.e. a soundness hole hiding inside
"interval arithmetic". Caught it because a width measurement came out exactly 0
(two 80-bit endpoints collapsing to one double), which was the smell. Fixed by
comparing the exact integer sigma(n) against the enclosure's own endpoints (mpmath
mpf comparisons are exact across precisions), then re-ran every gate: 27-exception
list still exact, all 680 candidates 'holds' at 80 bits alone, enclosure widths
~7e-24 with 200-bit truth contained. Rule: never let a value re-enter a lower
precision context between enclosure and comparison.

Final: certified sigma(n) < e^gamma n log log n for all 5041 <= n < 10^9.
Top near-misses (certified ratios): 10080 -> 0.98582, 55440 -> 0.98325,
27720 -> 0.97836; declining to ~0.965 near 10^9. All primorial-shaped, as the
CA-number theory predicts. Sieve 2.6 min single core; nothing bears on RH itself.
