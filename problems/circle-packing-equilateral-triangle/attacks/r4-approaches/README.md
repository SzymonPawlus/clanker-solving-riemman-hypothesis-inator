# Round-4 proposals and results

```
status:  sketch      — every proposal and every judgement in this file
         numerical   — the results summarised in §2, which live with their own
                       write-ups in the sibling attacks/r4-* directories
authors: claude, 2026-08-24. Ideation by two Fable 5 workers on disjoint lenses
         (RULES.md §8); execution and triage on Opus 5. The generating model was
         never the checking model.
issue:   #110
```

**Nothing here is assumable** (`RULES.md` §3). Rounds 1–3 are `../candidate-approaches/` (A–H),
`../approaches-round-2/` (I–O) and `../r3-approaches/` (V–AD). This round continues at **AE–AI**
plus the named construction proposals below.

---

## 0. What round 4 changed about the board

### 0.1 Two lower-bound families are now closed with reasons, not just verdicts

Round 3 killed the moment/SOS hierarchy on strength and left the Delaunay-scoring family
unmeasured. Round 4 closed the second **and explained the first**:

- **Euler-localised Delaunay scoring collapses onto Oler** (`../r4-delaunay/`), and the collapse
  is now backed by an **exact rational dual certificate** (`../r4-dual/`) rather than a float LP.
  The dual verifies with no rounding and no repair, both constraints tight, objective exactly
  `n − 1`, giving `d_family(n) ≤ √(8n+1) − 3`.
- The dual relations hold as **symbolic identities**, so the collapse is not a per-`n`
  measurement — it holds at every `n`.

**The structural reading is the transferable part** (`sketch`, from `r4-dual`): what pins the
family is not that nonlinearity gets suppressed, but **the shape of its conclusion** — affine in
(area, perimeter) of the hull. *Beating Oler needs a different-shaped conclusion, not a cleverer
score.* Any future proposal in this space should answer that objection first.

### 0.2 `n = 16` is the worst open target, on every axis

The case-specific lens argued, and the board's own history supports, that the campaign's default
target is the *least* tractable open case: widest remaining window (`≈ 0.892` in `d`), no closed
form (only a PSLQ degree-10 minimal-polynomial candidate), and no anchor value. It explicitly
recommended spending no round-4 slot on it, and none was.

Its reconstruction of *why* the `Δ(k) − 1` cases resist: the repo's three independent exact
break-even theorems (partition, convex-cut, corner-count) each close **exactly zero** of the
missing `+1` point, because every tool tried so far is **interaction-blind** — the `+1` lives only
in region *interactions*. It also argues the softest "one case" is a **reconstruction** of a
`cited` result, not an open `n`: validate the machine where the answer is known before pointing it
anywhere open.

### 0.3 `verified:lean` is unreachable from this session type

Recorded in `FINDINGS.md`. The Lean toolchain hosts return 403 from the egress proxy and the
container has no `elan`/`lake`/Mathlib cache, so the strongest status in `RULES.md` §3 cannot be
produced here at all. Every Lean proposal below is **undispatchable in this environment**, however
good — including one that would have been the repo's first machine-checked *optimality* artifact.

---

## 1. Proposals recorded (mostly unstaffed — the board's next round starts here)

### From the case-specific lens

- **AE — k = 7 conditional: certified lattice-count theorem + one named forcing hypothesis.**
  Make `max_Λ |Λ ∩ T(a)| ≤ 26` for `a < 6` a *proven* finite theorem by certified 3-parameter
  branch-and-bound (measured value 22, so 4 points of slack), and isolate robust lattice-forcing
  as the single explicit, falsifiable hypothesis implying EO(7). Ranked first by its lens: the
  first genuinely finite object any lower-bound effort here has had.
- **AF — complete the repo's stalled EO(4) reconstruction.** Measured-cheap exhaustion to
  `a > 2.95` plus a near-lattice endgame on `(2.95, 3)`. This *is* the mechanised Melissen shape,
  calibrated on a case with a `cited` answer. Ceiling at `k = 6` stated in advance.
- **AG — decide the `k = 4` covering question two-sidedly.** Either an explicit 8-piece
  diameter-`< 1` cover of `T(3⁻)` (⟹ EO(4) by finite certificate, uniform in `a`) or an LP-dual
  atomic-measure certificate that no 8-cover exists. **Attempted this round and not closed** — see
  §2.
- **AH — Lean-verify EO(3)** (`d(5) = 4` plus witness): would be the repo's **first machine-checked
  optimality result**, strictly stronger in kind than the board's feasibility-only Lean targets.
  **Blocked by §0.3, not by mathematics.**
- **AI — Markót-class active-region branch-and-bound, targeting `n = 24` rather than `n = 16`**
  (no rattler, exact `Q(√3)` anchor, narrowest non-EO window). Hard `n = 12` calibration gate.
  Heaviest item; ranked last by its lens.

### From the constructions/Lean lens

- **FAM-CERT** — certify the staircase past 34. **Executed, see §2.**
- **LEAN-STAIR** — staged `verified:lean` upper bounds: `n = 27` (351 integer-arithmetic goals,
  and the machine-checked upper half of Erdős–Oler `k = 7`) then `n = 24` (276 `Q(√3)` goals via a
  once-proved sign-rule lemma, no rattler). The lens argues Mathlib's polygon gap is a red herring
  because the merged half-plane formulation suffices. **Blocked by §0.3.**
- **QLIFT-2234** — finish the exact certified table on 16–34. **Substantially achieved by a
  different route, see §2.**
- **BUDGET-CURVE** — hit-rate-versus-budget curves per generator arm with within-repo labelled
  controls, to separate budget artifact from landscape hardness before anyone calls a record
  "soft". Pre-registered kill if everything turns out budget-limited. Honestly notes it cannot
  conclude softness on its own. **Unstaffed.**

---

## 2. What was executed, and what happened

| lane | outcome | status |
|---|---|---|
| `r4-delaunay` (AB) | family **collapses onto Oler**; kill-criterion fired, outcome (a) | `numerical` |
| `r4-dual` | **exact dual certificate**, no rounding, no repair; collapse proposition closes; holds at every `n` by symbolic identity | `numerical`/`sketch` |
| `r4-krawczyk` | **20 exact tight certificates**, Krawczyk contracted at all 20 | `numerical` |
| `r4-famcert` (FAM-CERT) | staircase certified at **`n = 40` and `n = 49`**; reproduction gate passed | `numerical` |
| `r4-theta` (AC) | **delivered**: AC's dominance claim correct, its *size* claim false, and **no `√6`-style ceiling exists**; survived the manager error below | `numerical`/`sketch` |
| `r4-cover4` (AG) | **not delivered** — killed mid-run at "still SAT", before either direction closed; left probe scripts only, no results, not merged | — |

### θ′ is NOT ceiling-bound — and do not extend `r3-sdpgate`'s verdict to it

`../r4-theta/` is the round's sharpest correction to the *rest* of this file, so it is worth
reading before believing §0.1's framing too broadly.

- **AC's dominance claim is correct**, re-derived by an explicit clique-cover kernel:
  `α ≤ ϑ′ ≤ χ̄`. A consequence the assignment missed — ϑ′ *inherits the covering plateau*
  `d(16) ≥ 2 + 4√3 = 8.928` (PRs #98/#104, `sketch` and unmerged; quoted, **not** depended on),
  which already exceeds Oler's `8.358`. **So the gate this lane was given was aimed at the wrong
  quantity**: "does ϑ′ beat Oler?" has an a-priori answer of yes.
- **AC's headline *size* claim is false.** A feasible kernel needs `rank Z ≥ α(G_d) − 1`
  (pairwise-obtuse vectors), and a bidegree-`m` kernel has rank `≤ C(m+2,2)`, forcing
  `m ≳ √(2n)`. So it is four *variables* for every `n`, but degree `∼√n`, Putinar blocks `∼n²/6`,
  scalar variables `∼n⁴`. "Independent of `n`" is true of the wrong quantity.
- **There is no `√6`-style ceiling here.** `α ≤ ϑ′ ≤ χ̄` with both ends `Θ(d²)` (hexagon tiling at
  the upper end) gives `d_{ϑ′}(n) = Θ(√n)` — the *right order*, unlike the moment hierarchy's
  bounded `√(6(n−1)/n)`. **`r3-sdpgate`'s verdict must not be extended to AC**, and §0.1 above
  should be read as being about the moment/SOS hierarchy specifically, not about convex
  relaxations in general.

**What it measured, and the honest limit.** A reusable one-sided instrument: for finite
`W ⊂ T_d`, a feasible kernel restricts, so `ϑ′(G_d[W]) ≤ ϑ′(G_d)` — finite subgraphs upper-bound
the achievable ϑ′ floor against *every* kernel of *every* degree, with no SOS needed. Across 20
solves at 7 values of `n`, `ϑ′(G_d[W])` never reached `n`; cleanest row is `n = 16` at
`d = √129 − 3` with an anchored 153-point witness giving `α = 15` (exactly `α(G_d)` there) and
`ϑ′ = 15.0000`. Largest observed `ϑ′ − α` gain was `+0.447`; firing needs `+1`.

**The lane never solved the SOS problem**, so it contains **no ϑ′-derived value for any `n`**. The
instrument is one-sided and can only detect weakness; it detected none. That is a null result and
weak evidence — explicitly *not* support for AC. The kill-criterion could not fire, and its file
says so with the reason.

### A manager error that this lane survived, recorded anyway

While the θ′ worker was still running and had not yet reported, the manager ran
`git worktree remove --force` across all lanes as cleanup, deleting its worktree mid-solve with
nothing yet committed. **The worker recovered on its own** — it detected the deletion, recreated
the worktree with `git worktree add`, rebuilt every file, committed *before* re-running, and re-ran
the measurements from scratch. Its branch survived because branches are not worktrees.

The manager, meanwhile, had already written this lane off as destroyed on the strength of a single
line recovered from the deleted log's open file descriptor, and correctly declined to draw a
conclusion from it. That fragment is now interpretable and consistent with the delivered results
(`n = 8`, `fires: false` — ϑ′ on a finite witness not reaching `n`).

**Both halves are worth keeping.** The procedural lesson stands: worktrees must not be reclaimed
until every dispatched worker has reported, and a worker that commits nothing until the end has no
partial-result story. But so does the correction: **the manager declared a lane dead while it was
alive**, which is the same class of error as declaring a result true while it is unproved, and it
was caught by the worker rather than by the manager.

### The Krawczyk result, and its load-bearing negative

`../r4-krawczyk/` obtained exact tight certificates at 20 values of `n`, including 13 of the 15
with a published Graham–Lubachevsky entry reproduced exactly, 2 above, **none below** (so
problem `RULES.md` §4's escalation was correctly not triggered). Its independent control was
`packing-r3-recheck/recheck.py`, written by a different worker straight from the problem
statement, which accepts all 20 — same model family, so no `verified:review`.

Two things in it are worth more than the table:

1. **It kept two statements apart.** A Krawczyk box certifies existence and uniqueness of a
   solution to a *square subsystem* — an equation statement, not a packing. The bound comes
   separately from an explicit exact `Q(√3)` configuration, verified from scratch.
2. **The tight constraint set is over-determined at all 20 configurations** (`K > rank`,
   deficiency 1–24), so any square subsystem must drop constraints that are *active* at the
   solution. **The Krawczyk box therefore can never certify feasibility on its own at these
   packings.** That is a precise statement of why the repo's exactification kept stalling, and it
   sits alongside `r3-stationarity`'s finding that underdetermined strata are forced for sparse
   supports — the two are the same obstruction seen from opposite sides.

Also methodologically important: comparisons were made against the **exact rational band implied
by G–L's printed 15 significant figures**, not a single rounded float. Doing it the naive way
"would have manufactured a false record at `n = 25` and `n = 29`".

### The staircase

`../r4-famcert/` certifies `s(40) ≤ 12 + 4√3` and `s(49) ≤ 14 + 4√3` exactly and tightly, after a
reproduction gate that recovers the three `cited` proven optima at `n = 4, 7, 12` and the
committed `n = 24` certificate point-for-point. **Not records and not new territory** — Amore
(2022) covers the triangle to `N = 400` and is behind the egress block.

---

## 3. Ranking for whoever picks this up

1. **AE (k = 7 conditional)** — the only proposal that would hand the project a finite object on
   the lower-bound side, and the lower-bound side is where everything has failed.
2. **AF / AG (reconstruct a `cited` case)** — validate the mechanised case-analysis machine where
   the answer is known. AG was attempted and is unfinished, with its `k = 3` calibration the
   sensible restart point.
3. **Cross-family review.** Not a proposal, but per §0.3 it is now the binding constraint: every
   certificate this round produced is same-family `numerical` and cannot ripen without Codex.
4. **AI**, then **BUDGET-CURVE**.
5. **AH / LEAN-STAIR** — best-in-kind, and undispatchable until the environment changes.

**Ranking is the triaging author's judgement and is `sketch` like everything else.**
