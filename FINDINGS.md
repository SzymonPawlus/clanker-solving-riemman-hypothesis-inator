# Findings

Running log of things worth a human's attention. Newest first. Agents append here when they find
something genuinely interesting — a result, a refutation, a near-miss, or an error in our own work.

**This is a highlights log, not a claims register.** Nothing here is citable. Every entry points at
the PR or file where the claim lives with its real status (`RULES.md` §3).

---

## 2026-08-17

### Oler's inequality cannot settle any open case — kill-criterion triggered
`PR #21` · status `refuted` as an independent attack

The primary source was obtained and read (Cambridge Core scan of Oler, *CMB* **4** (1961) 153–155,
all three pages). Specialising the inequality to our formulation gives

$$s(n) \ge 2\sqrt3 + \sqrt{8n+1} - 3$$

which is tight exactly when $8n+1$ is a perfect square — i.e. **exactly at the triangular
numbers**, which are precisely the cases Oler already settled in 1961. For $n = 16, 17, 18$ it
falls 0.89 / 0.76 / 0.79 short of the best known construction. A circle has diameter 2, so Oler is
out by roughly **half a circle**.

Consequence: any future optimality proof needs something strictly beyond Oler. The published
small-$n$ proofs confirm this — none uses Oler as the engine past the triangular numbers. Melissen
uses hand-designed dissections plus pigeonhole; Joós spends 31 pages of case analysis on $n = 13$
alone. One $n$ per paper, over 60 years.

Honest limit recorded: for $n \ge 16$ the optimum is unknown, so slackness there is inferred from
published constructions, not proved. Labelled `numerical`.

### No float tolerance can be correct — the exact-arithmetic rule is empirically necessary
`PR #16` · `experiments/circle-packing-checker/tests/naive_float.py`

A float checker faces a genuine dilemma, not merely a precision preference:

- tolerance `0` **rejects the valid $n=10$ packing** — exact contact computes as
  `1.9999999999999998`, because $\sqrt3$ is not representable;
- the smallest tolerance admitting it (`1e-9`) **accepts a `1e-12` overlap** — and `1e-18`,
  and `1e-30`.

No tolerance does both jobs. This turns "use exact arithmetic" from a stylistic rule into a
demonstrated requirement.

### Lean: first machine-checked packing results
`PR #19` (merged) · status `verified:lean`

Feasibility of explicit packings for $n = 3$ and $n = 6$, all seven theorems printing exactly
`[propext, Classical.choice, Quot.sound]`. **Upper bounds only** — no optimality claim.

The load-bearing guard is `inTriangle_iff_mem_convexHull`: the half-plane definition is proved to
be *exactly* the convex hull of the three vertices, both directions. Without it, everything above
could have been proving something weaker while still building clean.

### Mathlib has essentially no polygon geometry
`PR #21` · checked against the actual checkout, not assumed

`grep -rli "perimeter"` over all of Mathlib returns **zero files**. `Geometry/Polygon/Basic.lean`
is a bare `Fin n → P` vertex structure with no area. No Jordan curve theorem, no shoelace formula,
no Delaunay triangulation; `GeometryOfNumbers.lean` has three theorems, all Minkowski.

Even *stating* Oler's inequality faithfully in Lean is blocked. This is the "large Mathlib gap"
case of `RULES.md` §4 and it constrains what the Lean gate can reach on this problem.

### The search is exact locally and runs out globally
`PR #25` · status `numerical`

Reproduces the published exact closed form for **every** $n = 3 \dots 15$ to 15–16 significant
digits, and matches 14 of 19 Graham–Lubachevsky records for $16 \le n \le 34$. **Nothing beat a
published record** — every deviation was in the safe direction.

The five misses are the actual finding: at $n = 26, 29, 32, 34$ it converged to 15 digits onto
packings **GL themselves rank second best** (`t26b`, `t29b63.2`, `t32b`, `t34c`). That is
basin-coverage failure, not convergence failure — restart counts fall from ~200 at $n=16$ to ~55 at
$n=32$. The local step is exact; the global search is what degrades past $n \approx 26$.

### Near-miss: a silent NaN would have faked convergence
`PR #25` · commit `851c496`

A degenerate SLSQP solve returned coincident points ($m = 0$) and crashed on $2/m$. **The crash was
the lucky outcome.** A `NaN` would have passed silently, because `NaN > best_m` evaluates to
`False` — the search would have frozen on its previous best and reported it as converged. Worth
remembering as a general pattern: comparison-guarded incumbent updates fail open on `NaN`.

### Cross-model review caught a claude error — twice, independently
`PR #20`, `PR #22` (both merged)

Our README claimed *"a dijoin is exactly a set of arcs whose reversal makes $D$ strongly
connected"*, offered as a coding aid. **False** — the correct characterisation is *contraction*;
reversal-sets are sufficient but not necessary.

Codex fixed the prose in one PR and independently avoided the trap in the other, whose
implementation *adds* reverse arcs rather than replacing them, with the directed path as
counterexample. Verified directly: replace-by-reversal is not strongly connected, add-reverses is.

Two independent catches of the same error, by the other model family, in two separate PRs. This is
the decorrelation argument in `RULES.md` §5 doing exactly its job — and the first time it caught
claude rather than the reverse. The bad line was load-bearing: an implementation built on it would
have been silently wrong.

### Literature: our own table was wrong in three ways
`PR #10` (merged)

Optimality is proven for **all $n \le 15$**, every triangular number, and $n = 20$. In correcting
this we found our previous table had: three values wrongly listed as disputed (Friedman marks
$n = 7, 8, 11$ as *proved*), and **$n = 11$ and $n = 12$ swapped**. The two genuine gaps closed
after Friedman's page was written — $n = 14$ by Payan (1997), $n = 13$ by Joós (online Sept 2020).

Cross-checked independently: Joós's $t_{13}$ maps to $11.40649585375161$ against our tabulated
$11.40649585375171$ — agreement to $10^{-13}$.

### ⚠️ Open question: is $n = 20$ actually proven?
`issue #14` · under investigation

Payan's own abstract says the $k = 6$ case *"can be extended"*, while Tedeschi & Mackey (2021) list
it flatly as proven. **Our README currently asserts the stronger claim**, on a secondary source.
If Payan's result is conditional, `main` is wrong. This would be the third time a secondary source
misled this repo.

---

## Standing gaps

- **The repo has no lower-bound artifact of any kind.** Every result so far is an upper bound (an
  explicit packing). Optimality needs lower bounds; `issue #27` is the first attempt at one, via
  pigeonhole partition certificates with rational vertices.
- An unreviewed 2024/25 preprint claiming a general Erdős–Oler proof was spotted during triage and
  deliberately **not** cited pending assessment (`issue #29`).
