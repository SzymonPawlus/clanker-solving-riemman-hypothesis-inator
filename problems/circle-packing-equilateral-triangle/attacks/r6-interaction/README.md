# r6-interaction — conclusion shapes that are **not** affine in (area, perimeter)

**Claim kind: optimality / lower bound** (problem [`RULES.md`](../../RULES.md) §1). No packing is
constructed and no new lower bound on `s(n)` is proved. The output is a **measurement of what the
non-affine conclusion shapes can possibly give**, plus one lemma that closes a strictly larger
class than `r4-dual` did.

```
status:  sketch     — the Jump Lemma (§3), Proposition C2 (§4), and every reading
         numerical  — the rho-probe optimisations (§4.3) and the jump-structure table (§3.2)
author:  claude (Opus 5), worker r6-interaction, 2026-08-26
code:    experiments/packing-r6-interaction/   (three commands, README there)
kill:    KILL-CRITERION.md — FIRED, in the informative direction (one candidate survived step 2)
```

**Nothing here is assumable** (repo `RULES.md` §3). It builds on nothing unmerged. Where it quotes
`r4-dual`, `r5-exhaust4`, `r5-cover4`, `r5-eo7`, `r4-theta`, `r5-theta2` it says so and says whether
it re-derived the quoted fact (§7).

---

## 0. Result

Normalisation: **separation 1**, container `T(a)` = closed equilateral triangle of side `a`; the
repo's `d = 2a`, `s = d + 2√3`.

| | |
|---|---|
| Question | is there a lower-bound scheme whose conclusion is not affine in (area, perimeter), and which charges for interactions between regions? |
| Candidates written down | **four** (§2), each answered against F1/F2/F3 |
| Survived step 2 (matches Oler at every triangular `n`) | **one** — C2, the (A, M)-**realisability** bound |
| C2's measured ceiling at `n = 16` | `d(16) ≥ 8.4853` against Oler's `8.3578` — **+0.1275**, i.e. **14.3 %** of the way from Oler to the best known construction `9.2495` |
| C2's measured ceiling at `n = 9` (= `Δ(4) − 1`) | `2.8284` against the target `3` — **does not close EO(4)**, short by `0.1716` in `a` |
| Main negative | **Jump Lemma** (§3): *no* bound whose container-level conclusion is left-continuous at `a = k − 1` can ever prove `EO(k)` — **whatever shape it has** |
| Consequence | `r4-dual`'s collapse is **not special to affine conclusions**. On the `Δ(k) − 1` family the obstruction is not affineness at all; it is **continuity**, and it kills every measure-type conclusion of every shape |

**One-line answer to the assignment.** Escaping the affine shape is possible and buys a measurable,
bounded amount (14 % of the `n = 16` gap, zero at triangular `n`). It does **not** buy the `+1` at
`Δ(k) − 1`, and the reason is now a lemma rather than a pattern: at `Δ(k) − 1` the true counting
function jumps by **2**, so a bound must jump by more than **1**, and continuity — not affineness —
is what forbids that.

---

## 1. Coordinates, and what "the shape of the conclusion" means here

Oler (1961), `cited`: for finite non-collinear `E ⊂ R²` with pairwise distances `≥ 1`,

```
|E| ≤ (2/√3)·area(conv E) + perim(conv E)/2 + 1.
```

Put `r(E) := 4·area(conv E)/√3` and `M(E) := perim(conv E)`. Then Oler is

> **(O)** `n ≤ (r + M)/2 + 1`.

These are the right coordinates because on a hull tiled by unit triangles with every boundary edge
of length exactly 1 — the tight family `r4-dual` uses — `r` is the number of faces and `M` the
number of boundary edges, both integers, and `r + M = 2(n − 1)` exactly. For `T(a)`:
`r = a²`, `M = 3a`, so (O) reads `n ≤ (a² + 3a)/2 + 1`, i.e. `a ≥ a_Oler(n) = (√(8n+1) − 3)/2`,
`d ≥ √(8n+1) − 3`. (Verified exactly, `shapes.py` block (a): Oler's RHS equals `n` exactly at
`n = Δ(k)`, `a = k − 1`, for `k = 2..8`.)

`r4-dual`'s theorem is about conclusions of the form `n ≤ c_A·A + c_L·M + 1` — **affine in
(A, M)**. This lane asks what happens when that restriction is dropped.

---

## 2. The candidate table — four conclusion shapes, killed or kept on paper

Each row answers the round-6 filter: **(F1)** the shape of the conclusion as a formula;
**(F2)** what interaction it charges for; **(F3)** its behaviour at the exact-equality configuration.

| | shape (F1) | interaction charged (F2) | at equality (F3) | verdict |
|---|---|---|---|---|
| **C1** | `n ≤ c_A·A + c_L·M + 1` | none — regions independent | tight at every `Δ(k)`, no margin | **baseline**, = Oler; closed by `r4-dual` |
| **C2** | `n ≤ f*(A, M)` with `f*` the **true** max count at hull area `≤ A`, perimeter `≤ M`; equivalently `a(n) ≥ ρ(n) := min_E max(√r(E), M(E)/3)` | the **joint realisability** of the two hull statistics — Oler constrains only their *sum* | matches Oler **exactly** at every `Δ(k)`; jumps at `√8` not `3` for `Δ(4) − 1` | **SURVIVES step 2**; gains ≤ 14 % at `n=16`; **cannot** close `Δ(k) − 1` |
| **C3** | `n ≤ (r + M)/2 + 1 − D(E)`, `D ≥ 0` a discharging/defect term (charges moved between a face and its *star*, not per-face) | genuine — a face's charge depends on its neighbours, which is exactly what `r4-dual` §2 does **not** cover | validity forces `D = 0` at every Oler-tight configuration; the `Δ(k) − 1` optimum is a lattice minus a point, so `D → 0` and the margin `→ 0` | **DEAD by F3** for `Δ(k) − 1`; unquantifiable elsewhere |
| **C4** | two-point/pair-correlation: `n ≤ sup{ Σᵢⱼ …}` over kernels `f(|x−y|) ≤ 0` for `|x−y| ≥ 1` — the Delsarte/Cohn–Elkies shape for a bounded container | pairs, at given distances — the literal "quadratic analogue" of Oler | measured elsewhere in this repo as gain **exactly `0.000000`** at all 28 critical witnesses | **DEAD**, and it is not new: **this shape *is* `ϑ′`** (§2.4) |

### 2.1 C1 — the baseline, and why it is exactly Oler

`r4-dual` proves this with an exact dual. I did not re-derive its certificate; I re-derived the two
facts it rests on that I actually use: Oler is exactly tight at `T(k−1)` for `n = Δ(k)`
(`shapes.py` (a), exact rational arithmetic), and the lattice `T(m)` and the `P×Q` lattice rhombus
have `r + M = 2(n − 1)` (`shapes.py` (b)).

### 2.2 C2 — the survivor. Statement and proof in §4.

### 2.3 C3 — discharging, and the one gap it does exploit

Discharging is a **classical technique** (planar-graph colouring); nothing about applying it here is
a new idea, and the repo should not treat it as one. What is worth recording is precisely *where*
it escapes `r4-dual`:

`r4-dual` §2 proves the free-score LP collapses because each face's score `σ(f)` is capped by a
function of that face **alone** (`σ(f) ≤ c_A·area(f) − 1/2`), and (V) is monotone, so replacing `σ`
by its cap keeps feasibility. A discharging rule in which a face's charge depends on the *star* of
`f` — its neighbours — is **not** of that form, and its summed conclusion is

```
n ≤ c_A·A + c_L·M + 1 − Σ_f defect(star f)          (not affine in (A, M))
```

So C3 genuinely escapes `r4-dual`. It then dies at **F3** for the family that matters, and the
death is forced, not accidental: any valid bound of the form "Oler minus `D`, `D ≥ 0`" must have
`D = 0` at every Oler-tight configuration, because Oler is attained there and the bound would
otherwise be false. The `Δ(k) − 1` extremal hull *is* Oler-tight — for `k = 4` the corner-deleted
trapezoid has `(r, M) = (8, 8)`, Oler RHS `= 9 = n` exactly (`shapes.py` (f); I re-derived this
equality case myself from Oler's statement, and it agrees with `r5-exhaust4` §4.1(iii), which I did
not re-check). So the margin of any Oler-minus-defect bound is **exactly zero at the configuration
it must beat**. That is the F3 failure mode the brief warns about, arriving on schedule.

### 2.4 C4 — the "quadratic analogue" already has a name in this repo

The natural second-order analogue of a linear counting bound — score pairs by a kernel `f(|x−y|)`,
require `f ≤ 0` beyond the separation and positive semidefiniteness — is the Delsarte / linear
programming bound. For a **bounded container** this is exactly the Lovász-theta-type quantity the
repo calls `ϑ′` (`attacks/r4-theta/`). So a round-6 worker proposing "count pairs at given
distances" is proposing the `ϑ′` lane again under a different name, and should be told so.

Its status, **quoted and not re-derived by me**: `ϑ′` is *not* ceiling-bound (`d_{ϑ′}(n) = Θ(√n)`,
the right order), but `r5-theta2` measures the finite-witness route's gain as **exactly `0.000000`
at criticality**, at all 28 critical witnesses. That is again F3. I flag one thing the repo should
not lose: **C4 is the only candidate whose *order* is known to be right**, so its F3 failure is a
failure of the *witness route*, not of the shape. It remains the strongest non-affine shape on the
table, and it is unmeasured.

---

## 3. The Jump Lemma — the main negative, and a strict strengthening of `r4-dual`

### 3.1 Statement

Let `N(a) := max{|E| : E ⊂ T(a), pairwise distances ≥ 1}` (the max exists by compactness), and let
`a(n) := min{a : N(a) ≥ n}`, so `d(n) = 2·a(n)`. `EO(k)` is the statement
`a(Δ(k) − 1) = a(Δ(k)) = k − 1`.

Call a method's output a **container-level conclusion** `B : [1, ∞) → R` if what it proves is
`N(a) ≤ B(a)` for every `a`. To prove `EO(k)` it must give `B(a) < Δ(k) − 1` for all `a < k − 1`.

> **Jump Lemma** (`sketch`, mine; elementary and quite possibly folklore).
> Every valid `B` satisfies `B(k − 1) ≥ Δ(k)`, because the triangular lattice `T(k−1)` is an
> explicit witness with `Δ(k)` points. Hence if
> `liminf_{a ↑ k−1} B(a) ≥ B(k − 1) − 1` — in particular if `B` is **left-continuous** at
> `a = k − 1` — then `B` cannot prove `EO(k)`.
>
> *Proof.* `liminf_{a↑k−1} B(a) ≥ Δ(k) − 1 > Δ(k) − 1 − ε` for every `ε`, so `B(a) ≥ Δ(k) − 1` for
> `a` in a left-neighbourhood, contradicting `B(a) < Δ(k) − 1`. ∎

It is **unconditional**: it does not assume `EO(k)` is true, and it uses only the lattice witness.

### 3.2 Why this is the right lemma — the jump structure, verified

`jumps.py` reads the `cited` `s(n)` table out of the problem `README.md`, converts to
`a(n) = (s(n) − 2√3)/2`, and groups the `n` that share a value of `a(n)` — i.e. it reads off the
jump sizes of `N`. Over the **entire proven range**:

| `a` | jump size | `n` | |
|---|---|---|---|
| 1.000000 | **2** | 2, 3 | `Δ(2)`, `a = k−1` |
| 1.732051 | 1 | 4 | |
| 2.000000 | **2** | 5, 6 | `Δ(3)` |
| 2.732051 | 1 | 7 | |
| 2.914854 | 1 | 8 | |
| 3.000000 | **2** | 9, 10 | `Δ(4)` |
| 3.632993 | 1 | 11 | |
| 3.732051 | 1 | 12 | |
| 3.971197 | 1 | 13 | |
| 4.000000 | **2** | 14, 15 | `Δ(5)` |
| 5.000000 | **2** | 20, 21 | `Δ(6)` |

Every jump of size 2 sits at `a = k − 1`; every other jump has size 1. That is the whole content of
"the missing `+1` lives only at `Δ(k) − 1`", and it gives the **dichotomy**:

- at an `n` whose jump has size **1** (every non-`Δ(k)−1` case, including `n = 16, 17, 18, 19`), a
  *continuous* `B` can in principle be sharp: it may rise to `n` from below and hit it exactly at
  `a(n)`. **No obstruction.**
- at `n = Δ(k) − 1`, where the jump has size **2**, a continuous `B` provably cannot. **Total
  obstruction, for every shape.**

### 3.3 What this adds to `r4-dual`

`r4-dual` closed the conclusions **affine in (A, M)**, and its own reading asked whether the
collapse extends to a wider class. It does, and much wider than expected — but only on one family:

> On the `Δ(k) − 1` family, *every* conclusion that is a continuous function of the container scale
> fails, of whatever shape: quadratic in `(A, M)`, any continuous `f(A, M)`, any moment/SDP
> relaxation whose feasible set scales continuously, any Oler-minus-defect bound with continuous
> defect. Affineness is not what is doing the work there; **continuity is.**

And correspondingly, `shapes.py` (e) makes the shortfall visible: Oler at `a = (k−1) − 10⁻⁹` returns
`9.999999995` when it needs `< 9`. The shortfall is `0.999999995` and it converges to exactly **1**.
The repo has repeatedly described this as "the missing `+1`". It is more precisely **one half of a
jump of two**, and the half that is missing is the half continuity cannot supply.

### 3.4 The classification this produces — where every closed lane sits

Read this as: a method either has a continuous `B` (dead at `Δ(k)−1` by §3.1) or a discontinuous
one, and then the question is **where its jump is located**. Rows marked *(quoted)* are taken from
sibling directories and **not re-derived by me**; rows marked *(mine)* are measured in this lane.

| method | `B` continuous? | jump location at `k = 4` | needed | verdict |
|---|---|---|---|---|
| Oler / affine scoring (`r4-dual`) | **yes** | — | `a = 3` | dead by §3.1 |
| moment–SOS level 2 (`r3-sdpgate`) | **yes** | — | `a = 3` | dead by §3.1 *and* by its own ceiling `√6` |
| dyadic cell exhaustion (`r5-exhaust4`) *(quoted)* | effectively yes — bound `→ 9⁺`, never reaching 9 | none | `a = 3` | dead by §3.1 |
| Oler-minus-defect / discharging (C3) | **yes** (defect continuous, `= 0` at the lattice) | — | `a = 3` | dead by §3.1 + F3 |
| **(A, M)-realisability (C2)** *(mine)* | **no** — `f*` is a step function | `a = √8 = 2.8284` | `a = 3` | **mislocated by 0.1716** |
| covering by diameter-`< 1` pieces (`r5-cover4`) *(quoted)* | **no** — covering number is integer-valued | `a ≈ 2.99999` | `a = 3` | **mislocated by ~10⁻⁵** |
| line/row counting (`r5-eo7`, AE) *(quoted)* | **no** — but the jump goes the **wrong way** (24 at `δ = 0`, 27 at `δ > 0`) | wrong sign | `a = 3` | dead |
| rigidity / uniqueness at the lattice (Melissen) | **no** — by construction | `a = 3` exactly | `a = 3` | **the only located jump known**; not mechanised (`r5-exhaust4` §6) |

This is the measurement the assignment asked for. **Every discontinuous method in the repo has its
jump in the wrong place, and every continuous one has no jump at all.** The gap between "covering,
mislocated by `10⁻⁵`" and "rigidity, located exactly" is the whole remaining difficulty of
`EO(k)`, and it is a difficulty of *location*, not of shape and not of budget.

---

## 4. C2, the survivor: the (A, M)-realisability bound

### 4.1 Statement and proof — `sketch`, mine, elementary

For a finite unit-separated `E`, define `φ(E) := max( √(r(E)), M(E)/3 )`.

> **Proposition C2.** `a(n) ≥ ρ(n) := inf{ φ(E) : |E| = n, pairwise distances ≥ 1 }`, and
> `ρ(n) ≥ a_Oler(n)` for every `n`, with **equality at every triangular `n`**.
>
> *Proof.* If `E ⊂ T(a)` then `conv E ⊆ T(a)`, and both area and perimeter are monotone under
> inclusion of convex sets, so `r(E) ≤ a²` and `M(E) ≤ 3a`, i.e. `φ(E) ≤ a`; taking the infimum over
> `n`-point `E` gives the first claim. For the second, write `a = φ(E)`; then `r ≤ a²` and `M ≤ 3a`,
> so Oler gives `2(n − 1) ≤ r + M ≤ a² + 3a`, i.e. `a ≥ a_Oler(n)`. For triangular `n = Δ(k)` the
> lattice `T(k−1)` has `r = (k−1)²`, `M = 3(k−1)`, so `φ = max(k−1, k−1) = k − 1 = a_Oler(Δ(k))`. ∎

Two things this is and is not:

- **It is the optimum of the whole "(A, M)-only" class.** The pointwise smallest valid function
  `f(A, M)` is `f*(A, M) = max{|E| : r(E) ≤ 4A/√3, M(E) ≤ M}`, which is nondecreasing in both
  arguments, so evaluating it at the container's own `(A, M)` is the best that class can do — and
  that is exactly `a ≥ ρ(n)`. So C2 measures the ceiling of **every** `(A, M)`-shaped conclusion,
  affine or not. `r4-dual` measured the affine sub-class; this measures the rest.
- **It is a reduction, not yet a bound.** Using it needs a *lower* bound on `ρ(n)`, and `ρ(n)` is
  itself a global optimisation. What changed is that the **container is gone**: `ρ(n)` is a
  container-free question about free configurations, constrained by two scalar hull functionals.
  Whether that is easier is open; §5.

**Novelty:** unknown and probably nil. This is elementary and the literature is unreachable here
(`BRIEF-R6` §6); it is the sort of remark Groemer or Folkman–Graham may well have made. Treat it as
"applied here", not "new".

### 4.2 Step 2 of the assignment — does C2 match Oler where Oler is exactly tight?

**Yes, exactly, at every triangular `n`.** Both the identity (§4.1) and the numerics agree:
`shapes.py` (b) computes `min over Oler-tight (r, M) of max(√r, M/3)` for `k = 2..8` and gets
`k − 1` every time, equal to `a_Oler(Δ(k))` to machine zero. C2 is therefore the one candidate that
passes step 2, which is why it is the only one taken to step 3.

### 4.3 Step 3 — the measured ceiling (`numerical`)

Two independent estimates of `ρ(n)` from above:

1. **Restricted to Oler-tight configurations** (`shapes.py` (c)): those have integer `r, M` with
   `r + M = 2(n − 1)`, so the minimisation is a one-line integer search.
2. **Unrestricted, by multistart continuous optimisation** (`rho_probe.py`): minimise `φ(E)` over
   all `n`-point configurations subject to the `C(n,2)` separation constraints (SLSQP, hull area and
   perimeter from `scipy.spatial.ConvexHull`, every returned point rescaled so that the minimum
   separation is exactly `1` before its value is recorded — so no reported value comes from an
   infeasible configuration).

| `n` | `a_Oler` | `ρ ≤` (tight family) | `ρ ≤` (multistart) | argmin `(r, M)` | gain in `d` |
|---|---|---|---|---|---|
| 9 = `Δ(4)−1` | 2.772002 | 2.828427 | **2.828427** (300 starts) | `(8, 8)` — corner-deleted trapezoid | +0.1129 |
| 16 | 4.178908 | 4.242641 | **4.242641** (60 starts, see §4.4) | `(18, 12)` — `3×3` lattice rhombus | +0.1275 |
| 25 | 5.588723 | 5.656854 | — | `(32, 16)` | +0.1363 |
| 28 = `Δ(7)` | 6.000000 | 6.000000 | — | `(36, 18)` | **0.0000** |

The optimiser reproduces the lattice value to 8 decimals from random starts and finds nothing
better, which is what one wants from a ceiling measurement: **the ceiling is real and it is small.**

**Headline numbers.**

- `n = 16`: `ρ(16) ≤ 3√2 = 4.2426`, so the best conceivable `(A, M)`-shaped bound is
  `d(16) ≥ 8.4853` (`s ≥ 11.9494`) against Oler's `8.3578`. The remaining gap to the best known
  construction `9.2495` is `0.8917`; the whole non-affine part of the `(A, M)` class is worth at
  most **14.3 %** of it.
- `n = 9`: `ρ(9) ≤ 2√2 = 2.8284`, target `3`. C2 **cannot** close `EO(4)` — short by `0.1716` in
  `a`. Its jump is real but mislocated, exactly as §3.4 predicts.

### 4.4 Honest limits of the probe

`numerical`, and weakly so. The multistart minimisation is a heuristic: it gives an **upper** bound
on `ρ(n)`, so it can only ever *lower* the ceiling, never raise it. It agreeing with the tight-family
value is evidence that the tight family is where the minimum lives, not proof. The `n = 16` row is
60 starts (a 300-start rerun was launched; see `out/log16.txt` for whatever it reported) and `n = 9`
is 300 starts; both returned the lattice value from the first few starts and never improved.

### 4.5 C2 against the filter

- **(F1)** shape: `n ≤ f*(A, M)`, `f*` a step function; equivalently `a ≥ min_E max(√r, M/3)`. The
  container enters through a **max**, not a linear combination. **Not affine, and not even
  continuous** — it is the pointwise-minimal valid function on `(A, M)`.
- **(F2)** interaction charged: the **joint realisability** of area and perimeter. Oler constrains
  only `r + M`; C2 additionally demands that one single configuration achieve both coordinates. That
  is a real interaction *between the two statistics* — and it is honestly **not** an interaction
  between regions. **C2 does not answer F2.** It is still region-blind, and §4.3 shows exactly what
  that costs: it closes zero of the `+1`.
- **(F3)** at equality: margin **exactly zero** at every triangular `n` (§4.2) — it neither gains
  nor loses there. At `Δ(k) − 1` its jump is at `√(2(k−1)²−…)`-type lattice values (`√8` for
  `k = 4`), strictly below `k − 1`. So C2's margin is largest **away** from the equality case, which
  is the failing pattern the brief names — but unlike C3 and C4 it does not go to zero, it goes to a
  measured constant.

---

## 5. What would have to be true for any of this to become a proof

Two concrete, separable questions, both of which this lane leaves open and neither of which is a
framework:

1. **A rigorous lower bound on `ρ(16)`.** Needed: no 16-point unit-separated configuration has hull
   area `≤ (√3/4)·a²` and perimeter `≤ 3a` simultaneously, for `a < 3√2`. The container is gone, so
   this is a free two-functional packing question. A *qualitative* strictness argument is already
   available and cheap: if `φ(E) = a_Oler(n)` then Oler must hold with equality and `r = a²`,
   `M = 3a` exactly; if Oler's equality cases are exactly the unit-triangle-tiled hulls (which have
   **integer** `r` and `M`), then `a_Oler(16) = (√129 − 3)/2` being irrational forces
   `ρ(16) > a_Oler(16)` strictly. **I could not verify the equality characterisation** — literature
   is unreachable (`BRIEF-R6` §6) — so this is conditional, and it is qualitative anyway: it gives
   no size for the gap.
2. **A quantitative stability version of Oler.** "If `(r + M)/2 + 1 − n < δ` then `E` is within
   `ε(δ)` of a unit-triangle-tiled configuration." This is the one input that would make both C2
   (giving a size for the gap in 1) and C3 (giving `D` a positive lower bound off the lattice) into
   real bounds, and it is the honest form of the brief's F3 suggestion "exploit the equality case
   rather than losing to it". It is also, per §3.1, still **not** enough for `Δ(k) − 1`: stability
   is a continuous statement, and continuity is precisely what the Jump Lemma forbids there. For
   `Δ(k) − 1` the only shape left standing is a **classification** — the rigidity route
   `r5-exhaust4` §6 names, which is what Melissen's proof does and which nobody has mechanised.

---

## 6. Kill-criterion

See [`KILL-CRITERION.md`](KILL-CRITERION.md). It **fired**, in the informative direction: the
pre-declared kill was "no candidate survives step 2", and one did (C2). The lane therefore reports
both a survivor with a measured ceiling and a negative (§3) that is stronger than the one it was
sent to look for.

---

## 7. Inputs — what I verified myself (PROTOCOL-R5 §6)

**Verified myself, with my own code, from the problem statement:** Oler in `(r, M)` coordinates and
its exact tightness at every `Δ(k)` (exact rational arithmetic); the `r + M = 2(n−1)` bookkeeping of
the lattice and rhombus families; Proposition C2 and its proof; the Jump Lemma and its proof; the
jump-structure table (§3.2), computed from the problem `README.md`'s `cited` `s(n)` values; the
`k = 4` corner-deleted-trapezoid equality case `(r, M) = (8, 8)`; all `ρ` numerics.

**Taken as `cited`:** Oler's inequality; the `s(n)` table for `n ≤ 15`, `n = 20, 21` from the
problem `README.md` (with its own `n = 20` provenance qualification); the best known
`d(16) ≈ 9.2495`.

**Quoted from siblings and NOT re-derived:** `r4-dual`'s exact dual certificate and its §2 collapse
proposition (I use only its *statement* of what the affine class gives, and I re-derived the two
Oler-tightness facts I actually rely on); `r5-cover4`'s "no 8-cover of `T(a)` for `a ≥ 2.99999`";
`r5-exhaust4`'s Theorem 2 and its `→ 9⁺` table; `r5-eo7`'s 24-vs-27 discontinuity; `r4-theta`'s
`d_{ϑ′}(n) = Θ(√n)` and `r5-theta2`'s "gain exactly `0.000000` at criticality". Every one of these
appears only in §2.4 and §3.4, as classification, never as an input to a proof.

**Not used at all:** the covering plateau `d(16) ≥ 8.9282` of the unmerged PRs #98/#104.

**Known-technique disclaimer:** discharging (C3) and Delsarte/two-point correlation bounds (C4) are
classical techniques applied here, not new ideas. The Jump Lemma is elementary and may well be
folklore; novelty cannot be established in this session.
