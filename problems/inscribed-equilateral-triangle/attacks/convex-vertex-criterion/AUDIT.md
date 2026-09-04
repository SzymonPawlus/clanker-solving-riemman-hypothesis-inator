# AUDIT of `README.md` (convex-vertex-criterion)

status: sketch — **this audit grants nothing**

auditor: `claude` (Claude Opus 5), 2026-08-29, issue #132, separate worker/worktree
(`claude/inscribe-equilateral-triangle-oj15x1`) from the author.

regularity budget: convex (compact `K ⊂ R²`, `int K ≠ ∅`, `O ∈ ∂K`) — the same budget the
audited file declares. I audited that declaration; I did not widen or narrow it. What breaks
first if convexity is dropped: F1 (`K ⊆ O + T(O)`), and with it every statement in the file.

---

## 0. What this audit is worth — read this before the verdicts

**This is a within-family audit and it can never produce `verified:review`.** `RULES.md` §5 and
§8 reserve that for an agent of a *different model family*; the author of `README.md` is Claude
Opus 5 and so am I. Two models of one family are correlated, and this problem's `RULES.md` §6.2
is explicit that agreeing with an argument is not examining it.

What this audit *is*: a decorrelation pass. I re-derived each statement from the definitions
before reading the author's proof of it, and I reimplemented the computations from scratch rather
than rerunning theirs. That catches arithmetic slips, unjustified steps and false
counterexamples, and it caught three. It does not catch a shared blind spot, and I have no way to
know from the inside whether one is present. **Every claim in `README.md` remains `sketch`, and
so does everything in this file.**

I also did not fix anything: `RULES.md` §2 gives the `README.md` and `KILL-CRITERION.md` to
another worker. Errors found are recorded here, not patched there.

### Verdict table

| Item | Verdict | Note |
|---|---|---|
| §4.1 counterexample `K*` to (C2) | **agreed** — reconstructed completely, exactly | the refutation stands; it is global, not local |
| Theorem A (C1) | **agreed** | two lines from F1 |
| Proposition R (the reduction) | **agreed** | iff, both directions check |
| F1, F3, F4, F5 | **agreed** | F3's stated reason has a degenerate case; cleaner proof in §2.3 |
| F6 semicontinuity | **agreed as stated**, but the surrounding note is **wrong** | E1 below: `r` is in fact *continuous* on all of `[0,α]` |
| Theorem B(i) `α > π/3` | **agreed** | Cases A/B/C exhaustive; witness radius `> 0` in each |
| Theorem B(ii) `α = π/3` iff | **agreed** | the hardest case, and it is right |
| "needs no JCT / no degree theory / no rectifiability" | **agreed**, with two undeclared textbook dependencies (E4) | |
| Theorem C(a), C(b) | **agreed** | both halves reconstructed |
| Proposition D arithmetic | **agreed** — exact | all three points on `∂K`, all sides `√3/3` |
| Proposition D's "Case C" attribution | **disagreed** | E2 below: Case A fires, not Case C |
| §6 square non-transfer, counting argument | **agreed** | genuinely overdetermined |
| §6 "exactly three inscribed squares" | **agreed** — proved exactly, and 12 corner points | |
| §5.5 numeric `(2−√3)/2 ≈ 0.267949` | **disagreed** | E3 below: formula/decimal mismatch |

### Errors found

- **E1 (substantive, non-load-bearing): `r` is continuous on all of `[0,α]`, and the stated
  mechanism of the `K*` counterexample is misdiagnosed.** §1's note after F6 says "`r` genuinely
  can be discontinuous there (see §4.1). That gap is exactly where (C2) fails." Both sentences
  are false. See §2.4.
- **E2 (write-up error): Proposition D's witness is produced by Case A of Theorem B, not
  Case C.** `r(0) = 1 ≥ r(π/3) = 1/2`, so Case A fires and Case C is by construction its
  negation. See §3.2.
- **E3 (arithmetic slip): §5.5's "`O = (2−√3)/2 ≈ 0.267949`".** `(2−√3)/2 = 0.1339746`; the
  quoted decimal is `2 − √3`. See §5.2.
- **E4 (declaration): the `depends-on` list overstates "proved inline".** F2 uses the supporting
  hyperplane theorem, F4 uses "`w ∈ int K`, `y ∈ K` ⟹ `[w,y) ⊆ int K`", and Corollary E uses
  "`∂K` is uncountable", none proved. All textbook, none topologically heavy — this does not
  disturb the "no Jordan curve theorem" claim, but the list should say so. See §2.5.

None of E1–E4 changes the truth value of any of Theorems A–D or Corollary E as I reconstructed
them. E1 and E2 are wrong *diagnoses* attached to right *statements*, which is the class of error
`RULES.md` §0 warns about most, so I have written them up at length rather than as footnotes.

---

## 1. The `K*` counterexample (README §4.1) — reconstructed completely, **agreed**

This is the load-bearing claim in the directory: it refutes something the dispatch briefed as
true, so I verified every component from the definitions rather than reading the author's
verification. `K* = {(x,y) : 0 ≤ x ≤ 1, x² ≤ y ≤ √3·x}`, `O = (0,0)`.

**1.1 `K*` is convex.** It is the intersection of `{x ≥ 0}`, `{x ≤ 1}` (half-planes),
`{y ≥ x²}` (epigraph of the convex function `x ↦ x²`, `d²/dx²(x²) = 2 > 0`), and `{y ≤ √3 x}`
(half-plane). Each is convex; an intersection of convex sets is convex. ✓

**1.2 `K*` is compact with nonempty interior.** Each of the four sets is closed, so `K*` is
closed; `0 ≤ x ≤ 1` and `0 ≤ y ≤ √3` bound it. `(1/2, 1/2)` satisfies all four constraints
*strictly* (`0 < 1/2 < 1`, `1/4 < 1/2`, `1/2 < √3/2`), hence lies in the interior. ✓
(Nonemptiness of `K*` itself over `[0,1]` needs `x² ≤ √3 x`, i.e. `x(x − √3) ≤ 0`, true on
`[0, √3] ⊇ [0,1]`.) ✓

**1.3 `O ∈ ∂K*`.** `O ∈ K*` since `0 ≤ 0 ≤ 1` and `0 ≤ 0 ≤ 0`. Every ball around `O` contains
`(−ε, 0) ∉ K*`, so `O ∉ int K*`. ✓

**1.4 The achieved-direction set is exactly `A = (0, π/3]`, and direction `0` is genuinely not
achieved.** A point of `K*` with `x = 0` needs `0 ≤ y ≤ 0`, so it is `O`; hence *every*
`z ∈ K*∖{O}` has `x > 0`. For such `z`, `y/x ∈ [x, √3]` and both endpoints are `> 0`, so
`arg z = arctan(y/x) ∈ [arctan x, π/3] ⊂ (0, π/3]`. Conversely for `θ ∈ (0, π/3]` take
`x = min(1, tan θ) > 0` and `z = (x, x tan θ)`: then `x² ≤ x·tan θ` (as `x ≤ tan θ`) and
`x tan θ ≤ √3 x` (as `θ ≤ π/3`), so `z ∈ K*` with `arg z = θ`. Hence `A = (0, π/3]` exactly. ✓

Direction `0` unachieved, independently: a point of `K*∖{O}` with `arg = 0` has `y = 0` and
`x > 0`, but `y ≥ x²` forces `x² ≤ 0`. So `K* ∩ {y = 0} = {(0,0)}`. ✓ (I checked this identity
symbolically as well.)

**1.5 `α(O) = π/3`.** `Γ(O)` is the cone `{r e^{iθ} : r > 0, θ ∈ A} ∪ {0}`; its closure is
`{r e^{iθ} : r ≥ 0, θ ∈ [0, π/3]}`, an angular sector of opening `π/3`. ✓ So `K*` is a compact
convex body with nonempty interior, a boundary point of tangent-cone opening exactly `60°`, and

**1.6 no inscribed equilateral triangle has a vertex at `O` — globally, not locally.** Suppose
`P, Q ∈ J = ∂K*` with `{O,P,Q}` an equilateral triangle of side `t > 0`. `K*` is closed so
`J ⊆ K*`, and `P, Q ≠ O`, hence `arg P, arg Q ∈ A = (0, π/3]`. Both arguments lie in `[0, π]`,
so the unsigned angle `∠POQ` equals `|arg P − arg Q|`, and equilaterality forces it to be exactly
`π/3`. Relabel so `arg P = arg Q + π/3`. Then `arg P > 0 + π/3 = π/3`, contradicting
`arg P ≤ π/3`. ∎

I emphasise what the dispatch asked me to check: **this argument nowhere restricts `P` or `Q` to
a neighbourhood of `O`.** Its only input is `P, Q ∈ K*∖{O}`, which holds for every point of `J`
other than `O`, however far away. It is the wedge test of the problem's `RULES.md` §3.1 applied
to the *achieved* directions rather than the closed cone, and it is global for the same reason
the wedge test is. There is no "both other vertices near `O`" restriction to escape through.

**Verdict: agreed, in full.** `(C2)` as briefed ("`α(O) ≥ 60°` ⟹ good") is false, and `K*` at
the origin is a correct witness. The author's alternative one-line phrasing ("rotating any
argument-`π/3` boundary point by `−π/3` lands on the positive `x`-axis, which meets `K*` only at
the origin") is also correct, and is a genuinely different route to the same conclusion.

**Bonus check.** I recomputed the other two corners of `K*` exactly: at `(1, √3)` the interior
angle is exactly `30°` (between `(0,−1)` and `(−1,−√3)/2`), and at `(1,1)` it is
`arccos(−2/√5) ≈ 153.4349°`. Both match §5.2 of the README. So `K*` does have exactly two
non-good boundary points — `(0,0)` failing by the new `A`-mechanism and `(1,√3)` failing by
Theorem A — and the README's use of it as a second sharpness witness in Proposition D is correct.

---

## 2. Theorem B and its declared dependencies

### 2.1 Proposition R — **agreed**

`(⇐)` With `t ∈ Σ(θ) ∩ Σ(θ−π/3)`, set `P = te^{iθ}`, `Q = te^{i(θ−π/3)}`. Then
`|PQ|² = 2t² − 2t²cos(π/3) = t²`, so all three sides are `t > 0`. Both are on `J` by definition
of `Σ`, both `≠ O`. ✓ `(⇒)` `|OP| = |OQ| = |PQ| = t > 0` forces `∠POQ = π/3`; `P,Q ∈ K∖{O}` so
their arguments lie in `A ⊆ [0,α] ⊆ [0,π]` (F1/F2) and the unsigned angle is the difference. ✓
The `iff` is exact, which is what makes Theorem B(ii) decidable.

### 2.2 Theorem B(ii), `α = π/3` — attacked hardest, **agreed**

I derived this before reading the author's proof and landed in the same place.

With `α = π/3`, Proposition R needs `θ ≤ π/3` and `θ − π/3 ≥ 0`, so `θ = π/3` and the partner
angle is `0` — the admissible pair is unique, which is the whole reason this case is rigid.
So `O` is good ⟺ `Σ(0) ∩ Σ(π/3) ≠ ∅`.

- If `0, π/3 ∈ A`: `r(0), r(π/3) > 0`, and F5 gives `Σ(0) = (0, r(0)]`, `Σ(π/3) = (0, r(π/3)]`.
  Any `t ≤ min(r(0), r(π/3))` is in both. Good. ✓
- If `0 ∉ A` or `π/3 ∉ A`: the corresponding `Σ` is empty (`r = 0` on that ray, so no `t > 0` has
  `te^{iθ} ∈ K`, let alone `∈ J`), and Proposition R fails. Not good. ✓

Since F3 gives `(0, π/3) ⊆ A ⊆ [0, π/3]`, "`A = [0,π/3]`" is exactly "`0 ∈ A` and `π/3 ∈ A`",
which is exactly "both extreme rays meet `K` in a segment of positive length". The `iff` is
correct and the phrasing is faithful. `K*` sits precisely on the failing side (`0 ∉ A`).

I checked F5 at both endpoints including `α = π`: if `te^{i·0} ∈ int K` for some `t > 0` then a
ball about it inside `K` contains points of argument `< 0`, contradicting `K ⊆ T(O)` (F1), since
`T(O)` contains only arguments in `[0,α] ⊆ [0,π]`. ✓ The same at `α`. This is the step
`KILL-CRITERION` K3 asks a reviewer to check, and the definition of `α` used in Theorems A/B/C is
the same one used in F1 — the mismatch K3 fears (defining `α` by tangent lines or secant limits,
then invoking F1) does not occur. The file consistently uses "opening of the closure of the cone
generated by `K − O`", and F1 is trivial for that definition.

### 2.3 F1–F5 — **agreed**, with one presentational gap

- **F1** `K ⊆ O + T(O)`: immediate, `x − O = 1·(x−O) ∈ Γ(O) ⊆ T(O)`. ✓ The author's remark that
  convexity is doing the work *twice* (making `Γ` an angular sector, and making the containment
  trivial) is correct and is the honest reason F1 is not where the error is.
- **F2**: `Γ(O)` is a convex cone (cone generated by a convex set containing `0`); a supporting
  line at `O ∈ ∂K` puts it in a closed half-plane, so `T(O)` is a closed angular sector of
  opening `≤ π`; `int K ≠ ∅` gives opening `> 0`. ✓
- **F3**: I got the same conclusion by a different route. The author says "a convex cone inside a
  half-plane, so its nonzero arguments form an interval". That is true but the obvious
  positive-combination proof has a degenerate case: if `A` contains two antipodal directions
  `θ` and `θ+π`, positive combinations of those two alone give only the line. (It is still fine —
  such a `Γ` contains a line, lies in a half-plane, and has nonempty interior, hence *is* the
  half-plane — but the one-line justification does not cover it.) Cleaner: `Γ(O)∖{0}` is a convex
  planar set minus a point, hence connected, and `arg` is continuous on the punctured half-plane,
  so `A` is a connected subset of an interval. That covers every case in one step. `inf A = 0`
  and `sup A = α` then follow because `{arg ∈ [a,α]} ∪ {0}` is closed. ✓
- **F4**: reconstructed independently and agreed. Pick `ψ₁ < θ < ψ₂` in `(0,α) ⊆ A` with
  `ψ₂ − ψ₁ < π`; `conv{0, x₁, x₂} ⊆ K` is a nondegenerate triangle whose interior contains
  `δe^{iθ}` for small `δ > 0`; then `[δe^{iθ}, r(θ)e^{iθ}) ⊆ int K`. Every `t ∈ (0, r(θ))` is
  covered by choosing `δ < t`. Hence `Σ(θ) = {r(θ)}` on `(0,α)`. ✓
- **F5**: see §2.2. ✓

### 2.4 F6, and **E1: `r` is continuous on all of `[0,α]`** — the note attached to F6 is wrong

F6 as *stated* is true and is all the proof of Theorem B uses:

- **usc on `[0,α]`**: if `θₙ → θ*` then along a subsequence realising `limsup r(θₙ) = c`, we get
  `r(θₙ)e^{iθₙ} → ce^{iθ*} ∈ K` (closed), so `c ≤ r(θ*)`. Needs `K` compact. ✓
- **lsc on `(0,α)`**: if `liminf r(θₙ) = c < r(θ*)`, pick `c < t < r(θ*)`; F4 puts `te^{iθ*}` in
  the open set `int K`, so `te^{iθₙ} ∈ K` eventually, i.e. `r(θₙ) ≥ t > c`. ✓

But the note immediately after F6 says: *"Note F6 says nothing about `r` at `θ = 0` or `θ = α`,
and `r` genuinely can be discontinuous there (see §4.1). That gap is exactly where (C2) fails."*
**Both sentences are false.** I claim:

> **`r` is continuous on all of `[0,α]`**, for every compact convex `K` with `int K ≠ ∅` and
> `O ∈ ∂K`.
>
> *Proof.* usc at `0` gives `limsup_{ψ→0⁺} r(ψ) ≤ r(0)`. If `r(0) = 0`, then since `r ≥ 0` this
> already gives `r(ψ) → 0 = r(0)`. If `r(0) > 0`, pick any `ψ₂ ∈ (0,α)`; `r(ψ₂) > 0` by F3, and
> `Δ = conv{0, r(0)e^{i0}, r(ψ₂)e^{iψ₂}} ⊆ K` is a nondegenerate triangle with a vertex at `0`,
> whose own radial function `ℓ` is continuous and positive on `[0, ψ₂]` with `ℓ(0) = r(0)`. Since
> `r ≥ ℓ` there, `liminf_{ψ→0⁺} r(ψ) ≥ r(0)`. Same at `α`. ∎

I confirmed this numerically on both a body with `r(0) = 0` (`K*`: `r(ψ)/ψ → 1`) and one with
`r(0) > 0` (a thin triangle: `r(10⁻⁷) = 0.9999999`), and I could not construct a
counterexample — the two candidate mechanisms are blocked by usc in one direction and by the
inscribed triangle in the other.

**Why this matters even though nothing breaks.** The proof of Theorem B is unaffected: it uses
only usc, which is true, so Case C survives verbatim (and would in fact be slightly simpler, with
`F` extending continuously to `[π/3, α]`). What is damaged is the *diagnosis*:

1. §8 lists "F6 combined with the endpoint estimates in Case C" as the **single least-certain step
   in the file**, marked `[ATTACK HERE]`, on the strength of `r` being "*only*" upper
   semicontinuous. Since `r` is in fact continuous, that step is strictly more robust than the
   author believes, and the flag points a reviewer at the safest part of the argument.
2. The mechanism of `K*` is **not** a discontinuity of `r`. In `K*`, `r` is continuous at `0`;
   the failure is that `r(0) = 0`, i.e. `0 ∉ A`, i.e. `Σ(0) = ∅`. That is a statement about which
   directions `K` *achieves*, and the README says this correctly everywhere else — in §4.1's own
   summary ("the tangent cone is a *closure*, and it can contain a direction that `K` itself does
   not achieve"), in Theorem B(ii), and in Proposition R. Only the F6 note gets it wrong.

Anyone formalising this in Lean would waste effort chasing the wrong lemma if they followed the
F6 note and §8. I would replace the note with: *"`r` is in fact continuous on `[0,α]`; only usc
is used. The mechanism of §4.1 is `Σ(0) = ∅`, not a jump in `r`."* I have not made that edit —
`RULES.md` §2 puts the file in another worker's lane.

### 2.5 Theorem B(i), `α > π/3` — **agreed**; and **E4**, the dependency declaration

Reconstructed independently, same three cases, same conclusions.

- **Case A** (`r(0) ≥ r(π/3)`): `π/3 ∈ (0,α)` so `r(π/3) > 0`, hence `r(0) > 0` and `0 ∈ A`. With
  `t = r(π/3)`: `t ∈ Σ(π/3)` by F4, and `0 < t ≤ r(0)` gives `t ∈ Σ(0) = (0,r(0)]` by F5. ✓
- **Case B** (`r(α) ≥ r(α−π/3)`): symmetric, using `α − π/3 ∈ (0,α)`. ✓
- **Case C** (neither): `F(θ) = r(θ) − r(θ−π/3)` on `(π/3, α)`, where both arguments are in the
  open interval `(0,α)`, so `F` is continuous by F6. `liminf_{θ→π/3⁺} F ≥ r(π/3) − r(0) > 0` and
  `limsup_{θ→α⁻} F ≤ r(α) − r(α−π/3) < 0`. IVT on a real interval. ✓

**The direction of the semicontinuity is right, and it is the one that matters.** At `π/3⁺` we
need an *upper* bound on `limsup_{ψ→0⁺} r(ψ)`; usc supplies exactly `≤ r(0)`. At `α⁻` we need an
upper bound on `limsup_{θ→α⁻} r(θ)`; usc supplies `≤ r(α)`. Had the semicontinuity been lower,
both estimates would point the wrong way and Case C would collapse, exactly as §8 says. It does
not, and by E1 the point is moot anyway.

**Degeneracy (KILL-CRITERION K4).** Each case puts its witness angle strictly inside `(0,α)`:
Case A uses `π/3`, Case B uses `α−π/3`, Case C uses `θ₀ ∈ (π/3, α)`. F3 gives `r > 0` on the
*open* interval, so `t > 0` in all three and `P = Q = O` is excluded. ✓ Cases A/B/C are
exhaustive by construction (`C = ¬A ∧ ¬B`). ✓ This is the problem `RULES.md` §2 requirement and
it is met explicitly rather than by picture.

**I exercised Case C on a body where it genuinely fires**, since neither the polygons nor
Proposition D reach it: `K_C = {0 ≤ x ≤ x_max, x² ≤ y ≤ x·tan 80° − x²}`, whose achieved set is
`A = (0, 80°)` *open at both ends*, so `r(0) = r(α) = 0` and both Case A and Case B fail. `F`
changes sign at `θ₀ ≈ 79.8819°` and the produced triangle has
`|OP| = |OQ| = |PQ| = 0.38455949`, with `P` on the upper concave arc and `Q` on the parabola.
Genuine, nondegenerate, and produced by the mechanism the theorem claims. (Float; used only as a
sanity exercise of the case analysis, not as evidence for any claim.)

**The "what it needs" claim — checked, and it holds, with a caveat.** The dispatch asked me to
attack the declaration "no Jordan curve theorem, no degree theory, no rectifiability". I traced
every step:

- The existence engine really is the IVT for a scalar function on a *real interval* of angles.
  No curve is traversed, so no connectedness of `J∖{O}`, no `∂K ≅ S¹`, no winding number, no
  parity, no degree. ✓ The author's §4.3 explicitly *reduces* the dependency by declining the
  brief's route along `J`, and that reduction is real, not cosmetic.
- Nothing anywhere uses arc length, tangents, or rectifiability. ✓
- No compactness argument on a space of triangles; no limit of triangles is taken; §4 of the
  problem's `RULES.md` (approximation obligations) is not triggered because there is no
  approximation. ✓

**E4, the caveat.** The `depends-on` block says the convexity facts are "proved inline below as
F1–F6", which overstates. Three textbook facts are used without proof:
`(i)` the supporting hyperplane theorem at a boundary point (F2); `(ii)` "`w ∈ int K`, `y ∈ K`
⟹ `[w,y) ⊆ int K`" (F4, and the author does name it as "the standard convexity fact");
`(iii)` "`∂K` is uncountable when `int K ≠ ∅`" (Corollary E). All three are elementary convexity
or point-set facts and none of them is the Jordan curve theorem or anything near it, so the
headline claim survives intact — but the list should name them, because "proved inline" is
precisely the sentence a later reader would trust without rechecking.

One framing caveat, not an error: the §0 summary row phrases Corollary E as "every convex
**Jordan curve**". Corollary E's own statement is about `J = ∂K` for `K` compact convex, which
needs no topology; identifying that with "Jordan curves bounding a convex region" needs
`∂K ≅ S¹` (and, if one starts from a curve rather than a body, the Jordan curve theorem to speak
of its interior). That is a statement about how the result is *advertised*, not about any proof
step, and the regularity-budget table §3 is correct as written.

### 2.6 What I could not settle about Theorem B

Nothing, in the sense of a step I could not follow — I reconstructed every one. But
reconstructing a proof is not the same as knowing it is true, and I am the wrong family to
certify it. `KILL-CRITERION` K1 did not fire: I looked for `α > π/3` non-good points and for
`α = π/3` points with `A = [0,π/3]` that are non-good, in 400 exact random convex polygons
(14 310 boundary points), in seven hand-built polygons with *exact* `60°` vertices, and in two
curved bodies, and found none. Absence of a counterexample after that search is weak evidence and
I record it as such.

---

## 3. Theorem C and Proposition D

### 3.1 Theorem C — **agreed**, both halves, both parts

**Strong form of Theorem A** (`P, Q ∈ K∖{O}` ⟹ `∠POQ ≤ α(O)`): from F1 both difference vectors
lie in the sector `T(O)` of opening `α ≤ π`, and for arguments in `[0,α] ⊆ [0,π]` the unsigned
angle is the difference of arguments. ✓ Theorem A itself is then one line (`π/3 ≤ α(O)`), and I
agree with the author that it is the robust part of the file.

**(a) Non-collinearity.** Three *distinct* collinear points have one strictly between the other
two, say `O₂`; then `O₁, O₃ ∈ K∖{O₂}` and `∠O₁O₂O₃ = π`, so the strong form forces
`π ≤ α(O₂) < π/3`. Contradiction. ✓ **The angle bound.** The interior angle of the triangle
`O₁O₂O₃` at `Oᵢ` *is* `∠OⱼOᵢO_k`, which the strong form bounds by `α(Oᵢ) < π/3`. Three angles
each `< π/3` sum to `< π`, but a Euclidean triangle's angles sum to `π`. ✓ Both halves check.

**(b) The strengthened version.** Running the same argument with `≤ π/3`: any three points with
`α ≤ π/3` are non-collinear (still, since `π ≤ π/3` is false) and have all three angles `≤ π/3`
summing to `π`, hence *all equal to* `π/3` — equilateral. ✓ Four such points: `O₁O₂O₃` and
`O₁O₂O₄` are equilateral on the common base `O₁O₂`, and `O₃ ≠ O₄`, so `O₄` is the reflection of
`O₃` in line `O₁O₂` and `|O₃O₄| = 2·(√3/2)|O₁O₂| = √3|O₁O₂|`; but `O₁O₃O₄` equilateral demands
`|O₃O₄| = |O₁O₃| = |O₁O₂| > 0`, giving `√3 = 1`. ✓ Exactly three: at each `Oᵢ` the other two
subtend exactly `π/3`, so `π/3 ≤ α(Oᵢ) ≤ π/3` and `T(Oᵢ)` — a sector of opening `π/3` containing
two rays at angle `π/3` — is exactly the cone those rays span, i.e. the triangle's own vertex
cone. Then `K ⊆ ⋂ᵢ(Oᵢ + T(Oᵢ))`, and for a triangle that intersection is `H₁₂ ∩ H₁₃ ∩ H₂₃ = T`
(each vertex cone is the intersection of two of the three edge half-planes, and the three cones
together use all three). With `T ⊆ K` by convexity, `K = T`. ✓ Each vertex good, witnessed by `T`
inscribed in itself. ✓

**No smuggled regularity.** The only external ingredient is the Euclidean angle sum. The author's
claim that this beats the brief's total-turning route is correct: total turning for a general
convex curve needs either polygonality or the turning measure, and none of that appears here.
This is a genuine dependency reduction, and `KILL-CRITERION` K2 did not fire (no polygon among
400 had three vertices with `α < 60°`; the observed maximum was two, attained once).

I also checked the `π/2` transfer asserted in §6: four points with `α < π/2` are pairwise
non-collinear-in-triples by the same argument, lie in convex position (a point of `∂K` interior
to the hull of three others would be in `int K`), and their convex quadrilateral has interior
angles summing to `2π` while each is `< π/2`. ✓ Correct.

### 3.2 Proposition D — arithmetic **agreed exactly**; **E2**, the case attribution, **disagreed**

Recomputed in exact arithmetic (sympy, symbolic `√3`, no floats anywhere):

- angles of `K = conv{(0,0), (1,0), (−1/2, √3/2)}`: exactly `120°, 30°, 30°`. ✓
- `|OP|² = |OQ|² = |PQ|² = 1/3`, so all three sides are exactly `√3/3 = 1/√3`. ✓ Nondegenerate.
- **All three points lie on `∂K`, not merely in the plane**: `O` is a vertex; the segment
  `BC` from `B = (1,0)` to `C = (−1/2, √3/2)` is `B + s(C−B)`, and solving exactly gives
  `P = (0, 1/√3)` at `s = 2/3` and `Q = (1/2, 1/(2√3))` at `s = 1/3`, both in `[0,1]`. ✓
  (Cross products vanish exactly, so this is genuine collinearity, not a numerical near-miss.)
- The claim `√3/3 = 1/√3` checks. ✓

So the five-minute check passes. The exceptional-point count also checks: `B` and `C` have
`α = π/6 < π/3` (Theorem A ⟹ not good), `O` has `α = 2π/3`, edge-interior points have `α = π`,
so exactly two non-good points and the bound of Theorem C(a) is attained. My independent exact
polygon checker (see §5.1) confirms this directly: `O` good, `B` and `C` not good, and 600
exactly-sampled edge-interior points all good.

**E2.** The README then says the witness *"corresponds to Case C of Theorem B with `θ₀ = π/2`"*.
It does not. On this body, `r(θ) = 1/(cos θ + √3 sin θ)` (the far edge is `x + √3y = 1`), so
exactly:

```
r(0) = 1        r(π/3) = 1/2        r(α) = r(2π/3) = 1        r(α − π/3) = r(π/3) = 1/2
```

Case A's hypothesis is `r(0) ≥ r(π/3)`, i.e. `1 ≥ 1/2` — **true**, so Case A fires (and so does
Case B, by the reflection symmetry). Case C is *defined* as the negation of A ∨ B, so it cannot
apply here. What the proof of Theorem B actually produces at this `O` is the Case A witness
`t = r(π/3) = 1/2`, `P = (1/4, √3/4)` (the midpoint of `BC`), `Q = (1/2, 0)` (on edge `OB`) —
which I verified is equilateral of side exactly `1/2`, with both points on `∂K`.

What *is* true is the weaker statement that `θ₀ = π/2` is a root of `F(θ) = r(θ) − r(θ−π/3)`:
`r(π/2) = r(π/6) = √3/3` exactly, by the reflection symmetry about `θ = π/3` that the README
cites. The README's witness is a real inscribed triangle and Proposition D's claim is correct;
only the sentence attributing it to Case C is wrong. Since Proposition D is offered partly as an
*illustration of how Theorem B's case analysis runs*, the mislabel is worth fixing: a reader
checking the case analysis against this example will not be able to make it come out.

---

## 4. The square non-transfer (README §6) — **agreed**, and this is the item I most wanted to break

`RULES.md` §7 and the problem's `RULES.md` §3.2 make this the highest-value place to find an
error: if the method transferred, it would be wrong. It does not.

**4.1 The counting argument is correct.** Fix `O`. Normalising `O = 0`:

- *Triangle.* A candidate is `P = te^{iθ}`; the third vertex is forced to be `ρ(P) = te^{i(θ−π/3)}`.
  "Inscribed" is `t ∈ Σ(θ) ∩ Σ(θ−π/3)`, which in the generic interior case is the **single**
  scalar equation `r(θ) = r(θ−π/3)` in the **single** unknown `θ`. One equation, one unknown:
  IVT applies.
- *Square.* A candidate is again `P = te^{iθ}`, but there are now **two** further corners,
  `S = O + i(P−O) = te^{i(θ+π/2)}` and `R = P + i(P−O) = t√2·e^{i(θ+π/4)}`. "Inscribed" is
  `r(θ) = t`, `r(θ+π/2) = t`, `r(θ+π/4) = t√2` — after eliminating `t`, **two** equations
  `r(θ) = r(θ+π/2)` and `√2·r(θ) = r(θ+π/4)` in the **one** unknown `θ`. Overdetermined; no IVT,
  and generically no solution.

That is exactly the README's dimension count, and I get the same numbers writing it out in the
radial coordinates the proof actually uses rather than abstractly. The isoceles remark in §6 is
the right generalisation: `F_β(θ) = r(θ) − r(θ−β)` gives, for any `β ∈ (0,π)` with `α(O) > β`, an
inscribed isoceles triangle with apex `β` at `O`. At `β = π/2` that is a right isoceles triangle,
which is *three* points, not four. **The fourth corner is where the method stops, and it stops
before it can say anything about squares.** The reference non-transfer in the problem's
`RULES.md` §3.2 is the same gap, so this attack's answer matches the standard it is judged
against.

**4.2 The numerical claim about squares — checked by exact enumeration, and it is right (and
sharper than reported).** Rather than rerunning the author's gauge search, I wrote a complete
exact enumerator: for a convex polygon, the four corners `O, P, R = P + i(P−O), S = O + i(P−O)`
give four unknowns `(o₁,o₂,p₁,p₂)`; assigning each corner to an edge *line* gives a `4×4` linear
system, solvable exactly over `ℚ(√3)`. Enumerating all `3⁴ = 81` assignments × 2 orientations,
solving each exactly, and keeping only solutions whose four corners lie inside their segments:

> For the equilateral triangle `(0,0), (1,0), (1/2, √3/2)` there are **exactly 3** inscribed
> squares, each of side² `= 21 − 12√3`, i.e. side `√3/(2+√3)`, with **exactly 12 distinct corner
> points**.

This is a complete enumeration, not a sample, and it does not rely on the README's pigeonhole
argument (which I also checked and agree with: 4 corners on 3 sides forces two on one side, and
they must be *adjacent*, since a square whose diagonal lies on a triangle side would have its
other two corners strictly on opposite sides of that line while the triangle lies in one closed
half-plane).

So the analogue of Corollary E for squares is not merely unproved — it is false by a factor of
"12 versus uncountably many". `KILL-CRITERION` K5 does not fire, and the author's use of this as
a scope guard is legitimate.

**4.3 E3, the arithmetic slip.** §5.5 reports the classical square "recovered exactly at
`O = (2−√3)/2 ≈ 0.267949`". `(2−√3)/2 = 0.1339746`; the quoted decimal `0.267949` is `2 − √3`.
My exact enumeration gives the base square's corners at `x = 2 − √3` and `x = √3 − 1` on the base
(and two further corner points at `x = 2√3 − 3` and `x = 4 − 2√3` from the other two squares), so
the **decimal is right and the closed form is wrong**. The companion figure, side
`√3/(2+√3) ≈ 0.464102`, is correct — I get side² `= 21 − 12√3` exactly, and
`(√3/(2+√3))² = 3/(7+4√3) = 21 − 12√3`. The reported "`O = (0.777, 0)` admits no inscribed
square" is consistent with my exact list: the only base points that are square corners are
`≈ 0.2679, 0.4641, 0.5359, 0.7321`, and `0.777` is not among them.

Since §5 is `numerical` and nothing in Theorems A–D rests on it, E3 is cosmetic. I record it
because it is the kind of slip that gets copied into a later file as a closed form.

---

## 5. My own computations

Reimplemented from scratch, not rerun from the author's (whose scratch code was not committed in
any case). Everything decisive is exact.

**5.1 An independent exact checker, structurally different from the radial-function method.**
For a convex polygon `K` with boundary `J` and `O ∈ J`, I decide goodness by

> `O` is good ⟺ `(J ∩ ρ(J)) ⊄ {O}`, where `ρ` is rotation by `+60°` about `O`,

since `q ∈ J ∩ ρ(J)`, `q ≠ O` gives `P = ρ⁻¹(q) ∈ J` with `{O, P, q}` equilateral, and
conversely. This never forms `r(θ)`, never runs a case analysis, and never bisects — it is exact
segment/segment intersection (including collinear-overlap handling) in `ℚ(√3)`, which I
implemented as a field of pairs of `Fraction`s with an exact sign test
(`sign(a + b√3)` by case on the signs of `a, b` and the sign of `a² − 3b²`). No floating point
enters any decision. I deliberately avoided the author's `F(θ)` formulation so that a shared
formulation error could not hide.

**5.2 Validation before use**, per the problem's `RULES.md` §5:

- the equilateral triangle is recovered as inscribed in itself, at all three vertices, side² `= 4`
  for the side-2 triangle; ✓
- the `RULES.md` §3.1 witness (the `30°–30°–120°` triangle) gives exactly the expected answer:
  both `30°` apexes **not** good, the `120°` apex good, and 600 exactly-sampled random rational
  edge-interior points all good. ✓

**5.3 Exact test of Theorem B on 400 random rational convex polygons** (seed `20260829`, 3–9
vertices, hulls of random integer points in `[−30,30]²`): at every vertex I compared the exact
predicate `α ≥ 60°` (decided by `4(u·v)² ⋛ |u|²|v|²` with a sign case for `u·v ≤ 0`, exact in
`ℚ`) against the exact `J ∩ ρ(J)` checker, and I tested 4 interior points on every edge (where
`α = π`, so the criterion predicts good). **14 310 boundary points, 0 disagreements.** Maximum
number of vertices with `α < 60°` per polygon: **2** (histogram `{0: 382, 1: 17, 2: 1}`),
consistent with Theorem C(a) and with its sharpness.

**5.4 Exact `α = 60°` boundary cases.** Random rational polygons never realise `α = 60°` exactly,
so I hand-built seven polygons with exact `60°` vertices over `ℚ(√3)` — the equilateral triangle,
a `60/120` rhombus, a truncated `60°` quadrilateral, a `60°` wedge with arms of lengths 1 and 7,
a `100`-long `60°` sliver, and others. Every exact-`60°` vertex came out good, with an explicit
witness whose three squared side lengths I printed and checked equal. This is the polygon side of
Theorem B(ii) (`A` closed ⟹ good), and it is the half `K*` cannot test.

**5.5 Case C exercised on a curved body** (float, sanity only): see §2.5.

**5.6 Complete exact enumeration of inscribed squares**: see §4.2.

Everything here is `numerical` in the sense of `RULES.md` §3 — evidence, never a proof step. It
lives in a scratch directory and is **not committed**: `experiments/inscribed-triangle-polygons/`
is another worker's lane on this issue (`RULES.md` §2), and per the problem's `RULES.md` §3.3 a
citable enumerator must be independently reimplemented there anyway rather than copied from here.

---

## 6. `not-checked` — what I did **not** verify

This list is part of the audit, not an apology for it. A partial audit is an honest partial
audit, and everything below is a place where I took something on trust or ran out of scope.

1. **The literature.** I did not look for Meyerson 1980 or any other source. The provenance
   warning at the top of `README.md` stands entirely unverified by me, in either direction, and
   nothing here is evidence that these results are or are not known. Per the problem's
   `RULES.md` §6.1 this is verification-critical work and it is not my lane.
2. **Everything remains `sketch`, including this file.** I am the same model family as the
   author. Nothing here may be built on, by me or by anyone.
3. **Theorem B for general compact convex `K`.** I reconstructed the proof and could not break
   the statement, but "I re-derived it and agree" is exactly what `RULES.md` §5 says is not
   verification when the derivation comes from the same family. A `verified:review` requires
   Codex or a human.
4. **The `[w,y) ⊆ int K` fact (F4) and the supporting hyperplane theorem (F2).** I used both, as
   the author does, without proving either. Both are standard, but per §1 of this problem's
   `RULES.md` an undeclared assumption is an assumption; I have declared them (E4) rather than
   discharged them.
5. **README §5 items 3 and 4 as reported.** I did not reproduce the author's bisection checker,
   their gauge-walk cross-check, the Python-closure bug, or the two "residual misses". I built
   my own checkers and they agree with the theorems; I cannot confirm or deny the author's
   account of their own debugging, and I did not try to.
6. **The `β`-generalisation Remark in §6**, and in particular the `λ·r(θ) − r(θ−β)` variant for
   non-isoceles triangles. The README already marks it unchecked; so do I. I checked only that
   `β = π/2` yields a right isoceles triangle and therefore cannot reach a square.
7. **"Each side of a general triangle determines exactly one inscribed square."** I proved the
   count `3` only for the equilateral triangle, by complete exact enumeration. For a general
   triangle I checked only the direction the argument needs (`at most` one per side, hence at
   most 3), not existence.
8. **Whether `α = π/3` with `A = [0,π/3]` can occur on a body that is not a polygon**, and more
   generally I did not attempt a census of which convex bodies realise each case. Not needed for
   any claim, but it means my `α = 60°` evidence is polygon-heavy.
9. **Lean.** I did not attempt any formalisation and I did not check the file's claims about what
   would formalise easily. I note only that E1 changes the shape of the Theorem B target: with
   `r` continuous on `[0,α]`, the awkward semicontinuity lemma the README predicts would be
   needed can be replaced by a continuity lemma, which is a different (and I suspect easier)
   Mathlib exercise. That is a guess, and it is flagged as one.
10. **Anything outside this directory.** I did not read or touch
    `attacks/rotation-continuity/` or `experiments/inscribed-triangle-polygons/`, both live in
    other workers' lanes.
11. **The `KILL-CRITERION.md` honesty note about timing** (that the criteria were written after
    the fact). I take that at face value; I have no way to check it.

## 7. Single biggest residual doubt

Not any step in the file. It is that **`README.md` and this audit were produced by the same model
family, and the two most interesting things in the directory — the `K*` refutation and the
`α = π/3` sharpening — are exactly the kind of result two correlated models would find agreeable
together.** I did reconstruct `K*` from the definitions, and I believe it, and I could not break
it from any direction I tried. But `RULES.md` §0 is specifically about how that feeling is
produced by subtle errors as reliably as by correct ones. If a Codex or human examiner reads one
thing here, it should be §1.6 above — the global-versus-local step in the `K*` refutation — since
that is the single claim whose falsity would flip a `refuted` back to unrefuted, and everything
else in the directory is downstream of getting `α = π/3` right.
