# Robin's criterion: certified finite-range verification and near-miss catalogue

**Status: `numerical`. Not assumable. This bears no information about the truth of RH.**

Issue: #75. Code and data: [`experiments/rh-robin-criterion/`](../../../../experiments/rh-robin-criterion/).

## What this is

Robin (1984) proved that the Riemann Hypothesis is equivalent to

> sigma(n) < e^gamma · n · log log n   for all n > 5040,

where sigma is the sum-of-divisors function and gamma is Euler's constant.
This attack directory records a **computational verification of that inequality for all
n with 5041 <= n < 10^9**, together with a certified catalogue of where the inequality
comes closest to failing.

## What this is not

- It is **not evidence for RH** in any Bayesian sense worth acting on. A counterexample
  to Robin's inequality, if one exists, is expected to be astronomically large; checking
  up to 10^9 (or 10^100) cannot distinguish RH from its negation. The per-problem
  `RULES.md` §2 is explicit that more numerical verification carries no information
  about the conjecture, and that applies to this work in full.
- It is **not novel**: the literature contains verifications of Robin's inequality far
  beyond this range. We could not consult those papers from this environment (the
  egress proxy blocks scholarly hosts), which is exactly why this is filed as a
  self-contained reproducible computation and **no literature claims are made beyond
  the two classical facts cited below from memory** (Robin's equivalence; the finite
  exception list), both flagged as memory-cited in the write-up.
- Nothing here may be promoted to `results/` or used as a dependency.

## Method (the actual content)

The discipline is: **exact arithmetic for everything arithmetic, certified enclosures
for everything transcendental, floating point never load-bearing.**

1. **Exact sigma.** A segmented divisor-pair sieve in C computes sigma(n) exactly in
   `uint64` for every n in [5041, 10^9): sigma(n) = Σ_{d|n, d²≤n} (d + n/d), counting
   d once when d² = n. No overflow is possible (sigma(n) < 6n < 2^63 in range).
2. **Conservative flagging.** Doubles appear only in a *filter*: per segment [L, R), a
   threshold T ≤ (1 − 10⁻⁹) · e^gamma · log log L is computed **in Python with mpmath
   interval arithmetic** (outward rounding, then two `nextafter` steps down, then the
   margin). Since log log is increasing, any true violation in the segment satisfies
   sigma(n)/n ≥ e^gamma·log log L, and the 10⁻⁹ relative margin exceeds the worst-case
   double rounding error of the filter's ~3 flops (~10⁻¹⁵ relative) by six orders of
   magnitude. The filter can therefore over-flag but cannot miss a violation.
3. **Certified decision.** Every flagged n is re-decided in Python: sigma(n) is
   recomputed *independently* by trial-division factorization (and asserted equal to
   the sieve's value), and the comparison against e^gamma·n·log log n is done with
   mpmath interval arithmetic (`iv`), escalating precision 80 → 120 → 200 bits. A
   verdict is only issued when the exact integer sigma(n) falls strictly outside the
   enclosure of the right-hand side.
4. **Checkpointing.** The sieve appends one CSV row per 2^20-wide segment (coverage,
   argmax of sigma(n)/n, exact checksum, flag count), so a killed run loses at most
   one segment.

## Validation before the long run (all gates passed)

- **Known exception list (mandatory).** The certified checker, run on 2 ≤ n ≤ 5040,
  reproduces **exactly** the 27 known exceptions to Robin's inequality:
  2, 3, 4, 5, 6, 8, 9, 10, 12, 16, 18, 20, 24, 30, 36, 48, 60, 72, 84, 120, 180,
  240, 360, 720, 840, 2520, 5040 — no extras, no omissions, none undecided.
  (n = 1 is excluded: log log 1 is undefined. For 2 ≤ n ≤ 15 the right-hand side is
  ≤ 0 and the inequality fails trivially; the checker handles this via the interval
  sign, not via a special case.) List cited from memory of Robin 1984 / Lagarias
  2002 — flagged as such per repo citation discipline.
- **Sieve cross-validation.** All 100,000 sigma values in [5041, 105041) from the C
  sieve match a factorization-based Python sigma (different algorithm), and a random
  sample of 500 matches sympy's `divisor_sigma` (a third implementation).
- **Timing pilot** before launch: ~0.10–0.15 s per 2^20 segment, extrapolating to
  ~2.5 minutes for 10^9, within the stated budget.

## Result

**Certified: sigma(n) < e^gamma · n · log log n holds for every n with
5041 ≤ n < 1,000,000,000.**

- Coverage: 954 contiguous checkpointed segments tiling [5041, 10^9), verified
  gap-free by the certifier before any verdict was issued.
- The conservative filter flagged 680 candidates (all in the first segment, where
  log log n grows ~18% across the segment and the filter is intentionally loose).
  Every one was decided by certified interval arithmetic: **680 `holds`,
  0 `violates`, 0 `undecided`.**
- Error bounds: each decision compares the *exact integer* sigma(n) against an
  outward-rounded interval enclosure of e^gamma·n·log log n computed at 80 bits
  (escalation to 120/200 bits was never needed; re-verified with 80 bits alone).
  At 80 bits the enclosures have relative width ~7·10^-24 (measured against
  200-bit recomputation, which the enclosures contain), while the smallest
  certified separation in range —
  at the top near-miss n = 10080 — is a *relative* gap of ~1.4·10^-2 between
  sigma(n) and the RHS. The margin between enclosure width and required
  separation is therefore ~18 orders of magnitude; every verdict is strict
  (integer outside the enclosure), never "approximately below".
- Wall time: ~2.6 min for the sieve (single core, `nice`d) + <1 s certification;
  within the 20-minute cap stated in issue #75 (kill criterion K2 did not fire).


## Near-misses

Top 10 certified near-misses (full top-40 in `checkpoints/near_misses.csv`;
ratio = sigma(n) / (e^gamma n log log n), certified enclosure, 12 digits shown —
enclosure widths are ~10^-23 so lo = hi at this display precision; the decision
itself compares exact integers against raw 80-bit endpoints, floats are display-only):

| n | factorization | sigma(n) | certified Robin ratio |
|---|---|---|---|
| 10,080 | 2^5 * 3^2 * 5 * 7 | 39,312 | 0.985818611972 |
| 55,440 | 2^4 * 3^2 * 5 * 7 * 11 | 232,128 | 0.983253963847 |
| 27,720 | 2^3 * 3^2 * 5 * 7 * 11 | 112,320 | 0.978363769049 |
| 15,120 | 2^4 * 3^3 * 5 * 7 | 59,520 | 0.976130255417 |
| 110,880 | 2^5 * 3^2 * 5 * 7 * 11 | 471,744 | 0.974047429391 |
| 720,720 | 2^4 * 3^2 * 5 * 7 * 11 * 13 | 3,249,792 | 0.973045979901 |
| 1,441,440 | 2^5 * 3^2 * 5 * 7 * 11 * 13 | 6,604,416 | 0.970056126931 |
| 166,320 | 2^4 * 3^3 * 5 * 7 * 11 | 714,240 | 0.969600519947 |
| 2,162,160 | 2^4 * 3^3 * 5 * 7 * 11 * 13 | 9,999,360 | 0.968837769367 |
| 367,567,200 | 2^5 * 3^3 * 5^2 * 7 * 11 * 13 * 17 | 1,889,879,040 | 0.968152104902 |


As theory predicts (Robin: the sup of sigma(n)/(n log log n) over n > 5040 is
approached along colossally abundant numbers), every top near-miss has the shape
2^a·3^b·5^c·7·11·… with a ≥ b ≥ c ≥ … — primorial-like factorizations. The catalogued
ratio maxima *decline* over this range (0.9858 at 10080 down to ~0.965 at the
largest CA-like numbers near 10^9) — consistent with the known behaviour that the
ratio's envelope decays here and only creeps back toward 1 at scales far beyond
any computation. Note this decline is observed at the catalogued points only; we
certify the inequality everywhere but the *envelope shape* nowhere.

## Limitations, stated bluntly

- Range 5041 ≤ n < 10^9 only. This is far short of published verifications; the value
  here is the *discipline* (exact + certified, independently cross-checked, fully
  reproducible from `run_all.sh` in ~4 minutes), not the frontier.
- The two classical inputs (Robin's equivalence itself; the ≤ 5040 exception list) are
  cited **from memory**, since scholarly hosts are unreachable from this environment.
  They are standard, but a reviewer with literature access should pin them
  (Robin, *J. Math. Pures Appl.* 63 (1984); Lagarias, *Amer. Math. Monthly* 109
  (2002) — references from memory, unverified).
- The uint64 checksums in the checkpoints protect against silent segment corruption
  only probabilistically.
- Single-threaded, no parallelism — deliberately, to keep the computation simple
  enough to audit.

## Kill criteria (from issue #75)

K1 (exception-list mismatch): did not fire. K2 (budget overrun): did not fire.
K3 (undecidable candidate at 200 bits): did not fire. Extraordinary-claim clause
(a certified violation above 5040 — i.e. "we disproved RH", i.e. a bug): did not fire.
