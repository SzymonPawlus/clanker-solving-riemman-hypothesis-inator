# Kill-criterion — AB-dual (exact dual certificate for the Delaunay scoring family)

## As stated in the assignment

> If the exact dual cannot be made feasible after rounding and one repair attempt — e.g. the LP is
> degenerate, or the rational reconstruction blows up in denominator size — record the obstruction
> concretely (which constraints fail, by how much, denominator sizes) and STOP. Do not iterate
> solver settings for an hour.

## Verdict: **did NOT fire**

The dual was exactly feasible on the first attempt, and the rounding path the criterion guards
against was never entered.

The reason is worth recording, because it is the reason the criterion could not fire: **the dual
did not have to be reconstructed from a float solution at all.** The Oler-tight configurations
(triangular lattices, lattice rhombi) make the LP's binding constraints a pencil of half-planes
whose boundary lines all pass through Oler's coefficient point, so the optimal dual is available in
closed form as a convex combination of two of them:

```
λ = (s₂ − a)/(s₂ − s₁),      y₁ = 3aλ/M₁,      y₂ = 3a(1 − λ)/M₂
```

with `s(K) = 4√3·A_K/M_K` the configuration's slope. No float LP was solved to find it, so there
was nothing to round.

Denominator sizes, the quantity the criterion asks about: the dual variables are elements of
`Q(√(8n+1))` with **two-digit** numerators and denominators — e.g. at `n = 16` with the
lattice-only bracket, `y₁ = −21/2 + √129` and `y₂ = 81/10 − (7/10)√129`. Both dual constraints hold
with **equality** and the dual objective is exactly `n − 1`. There is no `ε` anywhere.

## What the run actually reports

| check | outcome |
|---|---|
| exact dual checker validated on a hand-solved LP (optimum `7/5`) | pass |
| checker rejects 3 deliberately bad duals (negative entry, `Aᵀy > c`, infeasible by `1/1000`) | pass |
| exact dual certificate, `n = 16, 17, 18`, tightest bracket | verified |
| exact dual certificate, `n = 16, 17, 18`, lattice-only bracket | verified |
| dual constraints tight (equality) in all six | yes |
| dual objective `= n − 1` exactly in all six | yes |
| three dual relations hold as symbolic identities in `(a, r₁, M₁, r₂, M₂)` | verified |
| Euler telescoping `(F+b)/2 = n−1` on all 22 configurations | verified |
| bridge to the sibling's outward-rounded LP rows (`ε = 10⁻³⁰`) | verified, excess `≤ 2·10⁻²⁹ + 10⁻⁴⁰` in `d` |
| all six rows of the sibling's published LP table reproduced by the proposition | yes |

## The second half of the assignment

The assignment also asked for the **collapse proposition**, with the explicit instruction to report
honestly if it did not close. **It closes** — README §2. The argument is that (D) caps each score
variable pointwise by the linear member's value, (V) is monotone nondecreasing in those variables,
so raising them all to their caps preserves feasibility; the objective sees only `(c_A, c_L)`, so
the free-score LP and the reduced LP have the same optimum, and at the cap (V) plus Euler is
literally the reduced constraint.

One thing it does **not** give, stated plainly rather than glossed: it shows the linear member is
*an* optimal solution and that the optimal *value* is unchanged, not that *every* optimal solution
has `σ` at its cap. The sibling's measured `max|σ − linear| = 0.00e+00` is consistent with the
proposition but is not implied by it in that stronger sense.

## What this licenses, and what it does not

- It **does** upgrade `attacks/r4-delaunay`'s central negative from `numerical`-by-float-solver to
  a certificate checkable in exact arithmetic, and it extends it from `n = 16, 17, 18` to every `n`
  (the certificate is an algebraic identity, and consecutive lattices bracket every `a ≥ 1`).
- It **does not** say a localised-scoring bound is impossible in principle. It is a statement about
  the LP over *this* formalisation of *this* family — see README §5, which lists six explicit
  scope limits including two things I did not check.
- Its status is `numerical` (computation) and `sketch` (prose). **Neither is assumable, including
  by me.** Promotion requires a different model family to reimplement the checker, per the problem
  `RULES.md` §3.

## Recorded so it is not re-tread

Do not attempt to beat Oler with any bound whose conclusion is affine in `(area, perimeter)` of the
convex hull. The lattices and the lattice rhombi are simultaneously tight for every such bound and
their slopes bracket every side length `a ≥ 1`, which pins the whole two-parameter family to Oler
at every `n`. An improvement needs a conclusion of a different shape, not a cleverer score.
