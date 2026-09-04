# 2026-08-29 — inscribed equilateral triangles on polygons: the exact enumerator

Issue [#132](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/132).
Lane: `experiments/inscribed-triangle-polygons/`. Everything below is **`numerical`** in the
sense of `RULES.md` §3 — see the caveat at the bottom, which is the part I care about most.

## What I was asked to build

Decide, exactly, whether a given point `O` on the boundary `J = ∂P` of a simple polygon `P` is
the vertex of a nondegenerate equilateral triangle with all three vertices on `J`. Call such an
`O` **good**.

## The reduction — checked before writing any code

> `O` is good ⟺ for some `σ ∈ {+1,−1}` there is `X ∈ ρ_σ(J) ∩ J` with `X ≠ O`,
> where `ρ_σ` is rotation by `σ·60°` about `O`.

(⇐) Put `Q = ρ_σ^{-1}(X) ∈ J`. Rotations are isometries fixing `O`, so `|OQ| = |OX|`, and the
angle `∠QOX` is exactly 60°. An isoceles triangle with apex angle 60° has base angles
`(180−60)/2 = 60`, so `OQX` is equilateral. Nondegenerate: `X ≠ O` gives side `> 0`, and a 60°
apex forces `Q ≠ X`.

(⇒) If `OAB` is equilateral with side `s > 0` and all three on `J`, then `B` is the image of `A`
under rotation about `O` by `+60°` or `−60°` — the two neighbours of a vertex of an equilateral
triangle sit at exactly those two angles, at equal radius. For that `σ`, `X = B` is in `J` and
in `ρ_σ(J)`, and `X ≠ O`.

The reduction held up. Both directions are short and I could not find a gap. **The trap it
creates** is that `ρ_σ(O) = O` always, so `O ∈ ρ_σ(J) ∩ J` unconditionally — the intersection is
never empty. Reporting that as a triangle would be reporting a triangle with two coincident
vertices, and would silently make *every* point good. Excluding it is the whole implementation
risk, and the 30°-apex control below exists to catch exactly that failure.

## Why `Q(√3)` is the whole story

The only irrationality is `sin 60° = √3/2`. Rotating a rational point by ±60° lands in `K = Q(√3)`;
intersecting two `K`-segments uses only `+ − × ÷`, so it stays in `K`. So every number in the
pipeline lives in `K`, and I represent an element as a pair of `Fraction`s `(a, b)` meaning
`a + b√3`.

Two facts make this total and exact, both worth writing down because they are what removes
floating point entirely:

1. **Zero test is syntactic.** `√3 ∉ Q`, so `a + b√3 = 0` forces `a = b = 0`. No tolerance.
2. **Sign test is a rational comparison.** Same-sign coefficients decide immediately; opposite
   signs are decided by comparing `a²` against `3b²`. `a² = 3b²` with `b ≠ 0` would make `√3`
   rational, so it never fires — the code raises rather than returning 0 there.

I wrote this from scratch (stdlib `fractions` only) rather than using sympy, because I wanted the
arithmetic under a decision procedure to be two screens of auditable code. sympy then gets used
*against* me, as an independent second opinion (below).

## Predictions in the brief, and what actually happened

| Prediction | Outcome |
|---|---|
| equilateral triangle: every vertex good | ✅ confirmed, side² = 1 exactly |
| 30-30-120: both 30° apexes **not** good | ✅ confirmed |
| 30-30-120: the 120° apex **is** good | ✅ confirmed |
| square: all four corners good | ✅ confirmed |
| convex: good ⟺ interior angle ≥ 60° | ✅ 0 violations in 88 346 convex vertices |
| convex: every non-vertex point good | ✅ 0 violations in 1 177 sampled points |
| non-convex: a sub-60° vertex can still be good | ✅ constructed, down to 0.286° |
| convex: no polygon has 3 non-good vertices | ✅ max observed 2, over 20 182 convex polygons |

(Counts: C1 was tested on 88 346 convex vertices — 721 in the battery, 87 625 in the seeded hunt
over 20 000 pseudorandom convex polygons. 30 568 sub-60° vertices, all not good; 57 057 vertices
at ≥ 60°, all good; no exceptions in either direction.)

Nothing in the brief turned out to be wrong. The one thing I'd flag as *sharper than expected*:
non-convexity by itself buys nothing. My `ncv-dart` fixture has a 11.42° vertex where the entire
curve still lies inside an 11.42° cone, and it is **not** good — while the *wing tips* of the same
dart, at 3.38° and 7.79°, **are** good, because from a wing tip the curve wraps around and
subtends ~90°. The relevant quantity is not the interior angle, it is the angular spread of `J`
as seen from `O`. That distinction is what I'd want any convexity-based argument in the other
lanes to be explicit about.

## The 60° boundary, and why exactness earned its keep

A convex vertex at exactly 60° is good, and it is good for a reason that is easy to state: the
rotated cone meets the original cone in exactly the ray along the other edge, so any `Q` on one
edge at distance `q ≤ min(|OA|,|OB|)` works. That is a boundary case, so I bracketed it: the
isoceles family `O=(0,0)`, `A=(1,0)`, `B` a rational point on the unit circle at angle
`2·arctan t`, with `t` straddling `tan 30° = 0.577350269189625764…`. At
`t = 5773502691896257/10^16` and `t = 5773502691896258/10^16` the apex angles are

    59.999999999999992909…°   →  not good
    60.000000000000007105…°   →  good

a gap of `1.4 × 10^-14` degrees. Double precision cannot separate those angles reliably; the
exact code separates them without effort, because it never computes an angle at all — it compares
`s²` against `3c²` where `s = cross(u,w)`, `c = u·w`.

A related small fact that fell out and that I like: **a polygon with rational vertices can never
have an interior angle of exactly 60°**, since `tan θ = |s|/c` would be rational but `tan 60° = √3`.
So the exactly-60 cases *require* `Q(√3)` coordinates; they cannot be reached at all by a rational
fixture. Verified as check `C7` (740 rational vertices, 0 at exactly 60°).

## Cross-check — the one genuinely surprising result of the day

`crosscheck_sympy.py` re-decides every named fixture through a completely different code path:
sympy `Rational`/`sqrt(3)` expressions instead of my pairs, and `sympy.geometry.Segment2D.intersection`
— which I did not write — instead of my segment code. Only the reduction and the fixture list are
shared.

**It disagreed on 3 of 176 vertices.** All three were on the two 10^-14-degree boundary fixtures,
and in all three sympy said *good* where I said *not good*. A disagreement means one of us is
wrong, so I stopped and adjudicated it (`diagnose_disagreement.py`) rather than picking a side:

1. An exact-rational **proof** that each disputed vertex is not good, trusting neither
   implementation: each fixture is convex, so the polygon lies in the closed cone of the interior
   angle at that vertex; the angle is `< 60°` (one comparison of `s²` against `3c²`); a sub-60°
   cone rotated by ±60° meets itself only at the apex; therefore `ρ(J) ∩ J = {O}`. No segment
   enumeration needed. All three: not good.
2. Evaluating sympy's own witnesses at **60 decimal digits** shows each lies on one of the two
   segments it was supposedly the intersection of and misses the other by `3e-17` to `1e-16`.
   sympy contradicts itself.
3. Converting each witness back to `Q(√3)` and testing the real condition — `X ∈ J` **and**
   `ρ^{-1}(X) ∈ J` — fails for all three.

So sympy was wrong three times and I was right three times. `Segment2D.intersection` starts
returning false positives once coefficients reach ~16 significant digits; it was fine on every
coarser fixture, including the `t = 5773502/10^7` pair.

I want to note the trap I nearly fell into inside the adjudication itself. My first version of
check (3) only tested `X ∈ J`. One of the three witnesses is a genuine polygon vertex — sympy
returned the real point `(0,0)` — so that check *passed* and the diagnostic reported "unresolved".
The thing that is off the curve there is `ρ^{-1}(X)`, not `X`. Checking half of a two-sided
condition and getting a green light is precisely the §0 failure mode, and it took a second look to
see it.

The wider lesson for this repo: the brief offered sympy as a reasonable way to do the exact
arithmetic. Had I taken it, this experiment would have returned wrong answers at exactly the
boundary it was built to probe, silently, because a false witness is indistinguishable from a real
one unless something separate checks it. ~90 lines of `Fraction` pairs that never leave `Q` do not
have this failure mode. Both disputed fixtures are now pinned as regression tests.

## The caveat I want on the record

The arithmetic is exact, so **each fixture's answer is certain**. That is *not* the same as the
conjectures being established. C1–C7 are statements about infinite families of curves, and I have
checked finitely many polygons, chosen by me and by a seeded generator I also wrote. The status is
`numerical` and it stays `numerical`: this is a control on the other lanes' arguments — if a
prose argument in `problems/inscribed-equilateral-triangle/attacks/` disagrees with a fixture
here, the fixture wins and the argument is broken. It cannot be run the other way round.

Where I'd look first if this is wrong: the fixture families are all *my* idea of extreme, and
they are all small (≤ 12 vertices). A convex polygon with hundreds of vertices, or a non-convex
one with deep nested spirals, is not represented. Someone should extend the battery there before
anyone leans on C1 too hard.
