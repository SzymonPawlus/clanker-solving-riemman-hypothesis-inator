# AB-dual. The Euler-localised scoring family provably cannot beat Oler — exact dual certificate

**This is a lower-bound (optimality-side) attack. It produces no construction and claims no
packing. It establishes no new bound on `s(n)`: its result is that a family of candidate bounds
provably collapses onto one the repo already has.**

```
status:  numerical  — the certificate computation (exact arithmetic, but it is a
                      computation, not a proof, and it is not assumable)
         sketch     — the collapse proposition of §2 and the readings in §4,
                      unreviewed prose by an agent
author:  claude (Opus 5), worker r4-dual, 2026-08-24
upgrades: attacks/r4-delaunay README §5.1 (the missing collapse proposition)
          attacks/r4-delaunay README §5.2 (the missing exact dual certificate)
code:    experiments/packing-r4-dual/   (single command: python3 certify.py)
kill:    KILL-CRITERION.md — did NOT fire
```

**Nothing here is assumable** (`RULES.md` §3). It depends on nothing unmerged; in particular it
does **not** use the `n = 16` covering bound of PRs #98/#104, and — see §1 — the *negative* result
does not even use Oler's theorem.

---

## 0. Result

| | |
|---|---|
| Question | can the Euler-localised Delaunay scoring family of `attacks/r4-delaunay` beat Oler? |
| Previous answer | "no, measured" — a float LP returned Oler's value; deviation from the linear member `0.00e+00` |
| This answer | **"no, certified"** — an exact dual certificate, checked in `Q(√(8n+1))` with `fractions.Fraction`, with no floating point in any accept/reject decision |
| At | `n = 16, 17, 18`, twice each (two independent brackets) |
| Rounding needed | **none.** The natural dual is exactly feasible; both dual constraints hold with **equality** |
| Collapse proposition | **closes** — §2 |
| Reach | the argument is an algebraic identity, so it holds at **every** `n`, not only 16–18 (§3) |

In one line: **the family's LP optimum is not merely observed to equal Oler's bound; it is forced
to, by two lattice configurations, exactly.**

---

## 1. The exact dual certificate

### 1.1 What had to be certified

`attacks/r4-delaunay` formalises the family (verbatim from its `lp.py`) as a pair `(σ, τ)` with
constants `c_A, c_L ≥ 0` satisfying

- **(D)** `σ(f) ≤ c_A·area(f) − 1/2` for every triangle with sides `≥ 1`, and
  `τ(l) ≤ c_L·l − 1/2` for every `l ≥ 1`;
- **(V)** `Σ_faces σ(f) + Σ_{boundary edges} τ(l_e) ≥ 0` for every finite non-collinear
  unit-separated `E` and every triangulation of `conv(E)` with vertex set `E`.

Applying (D) then (V) to one configuration `K` and telescoping with Euler `F = 2n − b − 2` gives
the **necessary** condition

> **(R)**  `c_A·A_K + c_L·M_K ≥ n_K − 1`

on any family member, where `A_K, M_K` are the area and perimeter of `conv(E)`. Inside an
equilateral triangle of side `a` the family's conclusion is `n ≤ B(a) := 1 + c_A(√3/4)a² + 3c_L·a`.
So the strongest bound the family can give at side `a` is the LP

```
minimise  B(a) − 1 = c_A·(√3/4)a² + 3·c_L·a
subject to (R) for every library configuration K,  and  c_A, c_L ≥ 0.
```

Because (R) is only *necessary*, this LP is an **optimistic relaxation**: the family cannot do
better than the LP says. To show the family cannot beat Oler one therefore needs a **lower** bound
on this minimum, which is exactly what a feasible **dual** provides.

### 1.2 Oler-tight configurations and their slope

Call `K` **Oler-tight** if `(2/√3)A_K + M_K/2 = n_K − 1`, i.e. Oler's inequality holds on `K` with
equality. Write `A_K = (√3/4)·r_K` (both families below have rational `r_K`) and define

> **slope**  `s(K) := 4√3·A_K / M_K = 3 r_K / M_K`, a rational number.

Two families, reconstructed exactly in `experiments/packing-r4-dual/configs.py` with five checks
asserted at construction (separation `≥ 1`; Euler; faces tile the hull; every boundary edge of
length *exactly* 1, so `M` is exactly rational with no rounding; Oler-tightness):

| configuration | `n` | `r` (`A = (√3/4)r`) | `M` | slope |
|---|---|---|---|---|
| side-`m` triangular lattice `T(m+1)` | `(m+1)(m+2)/2` | `m²` | `3m` | `m` |
| `P×Q` lattice rhombus | `(P+1)(Q+1)` | `2PQ` | `2(P+Q)` | `3PQ/(P+Q)` |

The name is geometric. Put `g = (√3/4)c_A`, `h = 3c_L`. Oler's own member is `(g, h) = (1/2, 3/2)`.
In these coordinates the constraint (R) from an Oler-tight `K` is

```
s(K)·(g − 1/2) + (h − 3/2) ≥ 0,
```

a half-plane whose **boundary line passes through Oler's point**, with slope determined by `s(K)`.
Every Oler-tight configuration contributes such a half-plane. Their intersection is a cone with
apex exactly at Oler.

### 1.3 The certificate

Fix `n`, let `D = 8n + 1` and `a = a_Oler(n) = (√D − 3)/2`, an element of the real quadratic field
`Q(√D)` with minimal polynomial `a² + 3a = 2n − 2`. Pick two Oler-tight configurations with
`s₁ ≤ a ≤ s₂` and set

```
λ = (s₂ − a)/(s₂ − s₁) ∈ [0, 1],      y₁ = 3aλ/M₁ ,      y₂ = 3a(1 − λ)/M₂ .
```

Then, **as identities**:

| | |
|---|---|
| `y₁, y₂ ≥ 0` | because `λ ∈ [0,1]`, `a > 0`, `M_i > 0` |
| `y₁r₁ + y₂r₂ = a²` | dual constraint for `c_A`, **tight** |
| `y₁M₁ + y₂M₂ = 3a` | dual constraint for `c_L`, **tight** |
| `y₁(n₁−1) + y₂(n₂−1) = (a² + 3a)/2 = n − 1` | the dual objective |

(The change of variable `x₀ = (√3/4)c_A ≥ 0`, `x₁ = c_L ≥ 0` is order-preserving and clears `√3`
out of the LP entirely, which is why everything lives in the single field `Q(√D)`.)

By weak duality the LP minimum is `≥ n − 1`, so `B(a_Oler(n)) ≥ n`. Since `B(a)` is nondecreasing
in `a` for `c_A, c_L ≥ 0`, the family's threshold `a* = sup{a : B*(a) < n}` satisfies
`a* ≤ a_Oler(n)`. In this repo's normalisation `d = 2a`, so

> **`d_family(n) ≤ √(8n+1) − 3 = d_Oler(n)`.** The family cannot beat Oler.

**No rounding, and no repair, was required.** The assignment anticipated rounding a float dual to
nearby rationals and repairing infeasibility; that step turned out to be unnecessary, because the
dual is available in closed form and is exactly feasible with both constraints tight. The
"round-and-repair" contingency was therefore never exercised — this is worth saying plainly rather
than implying a harder path was walked.

Certified brackets actually used (both succeed independently, for each `n`):

| `n` | `a_Oler(n)` | bracket (A), tightest | bracket (B), lattices only |
|---|---|---|---|
| 16 | `(√129 − 3)/2` | lattice side 4 (`s=4`), rhombus 2×5 (`s=30/7`) | lattice side 4, lattice side 5 |
| 17 | `(√137 − 3)/2` | rhombus 2×5 (`s=30/7`), rhombus 3×3 (`s=9/2`) | lattice side 4, lattice side 5 |
| 18 | `(√145 − 3)/2` | rhombus 3×3 (`s=9/2`), lattice side 5 (`s=5`) | lattice side 4, lattice side 5 |

Bracket (B) uses only `cfg_lattice(4)` and `cfg_lattice(5)`, which are in the sibling's own library
from refinement size 5 onward — so it covers every headline row of their report (sizes 6, 8, 10).

**What the negative rests on.** Only: (i) the two configurations are genuine unit-separated point
sets with the stated `n, b, F, A, M` — asserted exactly at construction; (ii) (R) is a necessary
condition on family members — the sibling's own derivation, `sketch`; (iii) weak duality, which is
three lines and is written out in `exact.py`'s docstring. **It does not use Oler's theorem.** Oler
is needed only for the matching *upper* bound `B* ≤ B_Oler` (Oler's member is LP-feasible), which
is the direction the sibling already measured and which is not what makes the negative meaningful.

### 1.4 Against the sibling's own LP data

The sibling's `framework.py` feeds its LP **outward-rounded** `A_up ≥ A`, `M_up ≥ M`, which weakens
the constraints further. A dual for the exact LP is therefore not automatically a dual for theirs.
STEP 4 of `certify.py` repairs this exactly: it verifies `A_up ≤ (1+ε)A` and `M_up ≤ (1+ε)M` with
`ε = 10⁻³⁰` on the two support configurations (comparisons in `Q(√3)`), from which `y/(1+ε)` is
dual-feasible for their relaxed LP; it then re-runs the certificate at an explicit **rational**
side length `ā > a_Oler(n)`, so every number in that check is a `Fraction`. Result:

> even against the sibling's own outward-rounded rows, the family's threshold in `d` exceeds
> `√(8n+1) − 3` by at most `2·10⁻²⁹ + 10⁻⁴⁰`, for `n = 16, 17, 18`.

That is 14 orders of magnitude below the `1.78e-15` at which their float solver reported agreement,
so their float result is not a solver artefact.

---

## 2. The collapse proposition

This is the argument `attacks/r4-delaunay`'s run report referred to and never wrote. It closes.

> **Proposition.** The *free-score* LP — one independent variable `σ_s` per distinct face shape and
> one `τ_t` per distinct boundary-edge length, plus `(c_A, c_L)`, under (D) per shape/length and
> (V) per configuration — has the **same optimal value** as the two-variable reduced LP, and the
> linear member is always among its optimal solutions.

**Proof.** Let `(c_A, c_L, σ, τ)` be feasible for the free-score LP. Define the *cap*
`σ̂(s) = c_A·area(s) − 1/2`, `τ̂(l) = c_L·l − 1/2`; this is exactly the linear (Oler-type) member
with the same `(c_A, c_L)`.

1. **(D) is precisely `σ ≤ σ̂` and `τ ≤ τ̂` pointwise**, and `(σ̂, τ̂)` satisfies it with equality.
2. **(V) is monotone.** For each configuration `K`, (V) is `Σ_f σ(shape f) + Σ_e τ(len e) ≥ 0`, a
   sum of the variables with all coefficients `+1`, hence nondecreasing in every variable.
   Therefore `Σ σ̂ + Σ τ̂ ≥ Σ σ + Σ τ ≥ 0`: the cap satisfies (V) too.
3. So `(c_A, c_L, σ̂, τ̂)` is feasible whenever `(c_A, c_L, σ, τ)` is. The objective involves only
   `(c_A, c_L)`, which are unchanged. Hence the two LPs have the **same feasible projection onto
   `(c_A, c_L)`**, and therefore the same optimal value, with the linear member always optimal.
4. **The projection is the reduced LP.** Evaluate (V) at the cap on configuration `K`. Since the
   faces tile `conv(E)`, `Σ_f area(f) = A_K` exactly, so
   `Σ σ̂ = c_A·A_K − F_K/2` and `Σ τ̂ = c_L·M_K − b_K/2`, giving
   `c_A·A_K + c_L·M_K − (F_K + b_K)/2 ≥ 0`. Euler `F = 2n − b − 2` gives `(F_K + b_K)/2 = n_K − 1`,
   so this is exactly (R). ∎

Step 4's arithmetic — `(F + b)/2 = n − 1` — is verified exactly, in integers, on all 22
configurations in STEP 3 of the run.

**What this settles and what it does not.** It settles that the observed
`max |σ − linear| = 0.00e+00` is *not a coincidence of the solver*: the optimal **value** is
unchanged by freeing `σ` pointwise, and the linear member is always an optimal solution. It does
**not** prove that *every* optimal solution has `σ` at its cap — where (V) is slack the LP has
other optima, and which vertex HiGHS reports is not determined by this argument. The sibling's
measurement is consistent with the proposition; it is not implied by it in that stronger sense.

---

## 3. The reach of the certificate: it is an identity, so it holds at every `n`

The three dual relations in §1.3 were verified **symbolically** in `(a, r₁, M₁, r₂, M₂)` (STEP 2,
`sympy`), using only Oler-tightness `n_i − 1 = (r_i + M_i)/2` and `s_i = 3r_i/M_i`. They are not
fitted to `n = 16, 17, 18`. Because the side-`m` lattice has slope exactly `m`, **every `a ≥ 1` is
bracketed** by the lattices of side `⌊a⌋` and `⌊a⌋ + 1`. Hence (`sketch`):

> For every `a ≥ 1`, over any configuration library containing those two lattices, the LP optimum
> is exactly Oler's `1 + (a² + 3a)/2`; and when the bracket is strict (`s₁ < a < s₂`) Oler's
> coefficients `(c_A, c_L) = (2/√3, 1/2)` are its **unique** minimiser.

Uniqueness follows because `au + v = λ(s₁u + v) + (1−λ)(s₂u + v)` with `λ, 1−λ > 0`, so the minimum
`0` forces both bracketing constraints to vanish, i.e. `u = v = 0`, i.e. Oler.

So the collapse is not a feature of `n = 16..18`, nor of the particular library: it holds at every
`n`, for every library rich enough to contain two consecutive lattices.

---

## 4. Reading: *why* it collapses, and what would have to change

The structural reason is sharper than "the nonlinearity gets suppressed", and it is worth stating
because it tells the next worker what not to retry.

**(D) and (V) are used only through their consequence (R).** Note further that even the strictly
larger family obtained by replacing pointwise (D) with its *summed* form

```
Σ_f ( σ(f) − c_A·area(f) + 1/2 ) ≤ 0     per configuration
```

yields the same (R), because `Σ_f area(f) = A_K` exactly. Weakening (D) to the weakest form that
still telescopes therefore buys nothing at all. The nonlinearity of `σ` is not what is being
suppressed.

What actually pins the family is **the shape of its conclusion**. Whatever `σ` and `τ` are, the
family emits a bound of the form

```
n ≤ 1 + c_A·area(conv E) + c_L·perimeter(conv E),
```

affine in (area, perimeter). The lattices and rhombi make *every* such bound tight simultaneously
at Oler's coefficients, and they bracket every `a ≥ 1`. So the affine-in-(area, perimeter) family
has Oler as its optimum everywhere, and any improvement must come from a conclusion that is **not**
affine in area and perimeter — for instance one that sees the container's shape, or a second-order
term, or the boundary structure beyond its total length.

That is also, incidentally, a precise restatement of wall (3) in the round-3 frontier ("Oler is
slack by ~half a circle at `n = 16..18`"): the slack is *not* reachable by re-weighting area
against perimeter, because that whole two-parameter space is already optimised.

---

## 5. Scope — what is NOT claimed

Stated explicitly, because an over-broad claim here would be exactly the `RULES.md` §0 failure.

1. **This is not a theorem that no localised-scoring bound can beat Oler.** It is a theorem about
   the LP over *this* formalisation — the (D)/(V) conditions, the Euler telescoping, and a
   conclusion affine in area and perimeter — as written in
   `experiments/packing-r4-delaunay/lp.py`. A different localisation, a different telescoping, or a
   conclusion of a different shape is untouched by it.
2. **It is not a lower bound on `s(n)`.** It is an upper bound on what one *method* can prove.
   `s(16)`'s true value is not constrained by anything here.
3. **It does not say Oler is optimal among all bounds of any kind**, only among those of the affine
   form above, and only given that the two bracketing lattice configurations are legitimate — which
   is checked, exactly, in `configs.py`.
4. **The §2 proposition and the §3–§4 readings are `sketch`.** They are unreviewed prose by an
   agent. The computation is `numerical`. Neither is assumable, including by me
   (`RULES.md` §3).
5. **Not checked:** that the sibling's *full* free-score LP as coded (with its `±1e6` box bounds on
   the score variables) is unaffected by those artificial bounds. Mathematically the family has no
   such box; if the cap `σ̂` exceeded `1e6` the substitution in §2 step 3 would leave the coded
   feasible region. At the optimum `c_A = 2/√3` and the library's face areas, it does not come
   close — but I did not verify it as an inequality, and it is a property of their code, not of the
   family.
6. **Not checked:** anything about libraries that do *not* contain two bracketing Oler-tight
   configurations. For those the LP can and does return values above Oler; STEP 5 of the run models
   that regime and reproduces the sibling's `d(18) = 136/15` row at library size 4, but the model's
   upper branch is a prediction, not proved here.

---

## 6. Reproduce

```
cd experiments/packing-r4-dual && python3 certify.py
```

Deterministic, a few seconds, no seeds, no network. Regenerates `out/report.txt` in full: the
validation of the exact dual checker on a hand-solved LP with three negative controls, the
configuration self-checks, the six certificates, the symbolic identity, the Euler table, the bridge
to the sibling's rounded data, and the consistency table.
