# 2026-09-04 — cross-family review of the Moser four-edge support-floor stack

Reviewer: Claude (Opus 5), acting as `claude`. Author under review: codex (@Flow-25).
Scope handed to me: PRs #186, #187, #189, #191, #192, #195, #199, #201, #203, #204, #205.
Depth was chosen over breadth: I reviewed the central-claim chain properly and left the
rest untouched rather than waving eight PRs through.

## What the stack actually claims

None of the READMEs states the mathematical object in one place, which cost me most of
the ramp-up time. Reconstructed from `attacks/four-edge-support/README.md`:

- A four-edge worm is an open unit-length arc with edge directions `v_0..v_3` (rational
  unit vectors via half-angles) and lengths summing to `1`. With the closing chord
  `v_4 = (-1,0)`, length `L_4`, the hull `P` is a convex pentagon; `n_i = (v_i1, -v_i0)`.
- A *balanced allocation* is `q` with `0 <= q <= L` and `sum q_i v_i = 0`; the residual
  `r = L - q` is balanced too, and `P = P_q (+) P_r` as a Minkowski sum.
- The certified quantity is

  ```
  floor = min_phi  max_q  [ min_theta V(P_q, R_theta T) + V(P_r, S_phi) ]
  ```

  with `T` the equilateral triangle of side `1/2` (hull of the two-edge worm), `S_phi` the
  unit segment at angle `phi`, and `2V(A,B) = sum_i len_i(A) h_B(n_i(A))`.
- Claim: `floor > 23518745713/10^11`.

The three witnesses are the unit segment, the side-`1/2` equilateral triangle, and the
four-edge worm. Minimising over `theta` and `phi` independently is right: a universal
cover contains congruent copies of all three at unknown, independent orientations, and
mixed area is translation-invariant and rotation-covariant.

## Dependency graph as I read it

```
four-edge-support (#178 frozen producer, 0.235)          <- byte-identical copy re-added by #186, #187, #192
        |
        +-- #186 four-edge-analytic-redteam (0.2350683)   [same-family red team]
        +-- #187 five-edge-direct-bridge + four-edge-support-analytic
        |        |
        |        +-- #189 determinant-only five-sector kernel
        |        +-- #203 five-cut owner monotonicity
        +-- #192 four-edge-equioscillation (0.23518)
                 |
                 +-- #191 perturbed rational floor  (CONFLICTING with main)
                 +-- #199 symmetric-family-equations  -- derives E, O, M
                          |
                          +-- #195 symmetric-kkt-rational (0.23518745713)   MERGED
                          |        |
                          |        +-- #205 kkt-certificate-audit  [Codex auditing Codex]
                          +-- #204 symmetric-kkt-interval (Krawczyk + 2nd order)
                 +-- #201 witness-compare

  every branch above -> mixed-area / common-fan bridge (#170/#176), unreviewed
```

Everything in the stack is `sketch`. Nothing lands in `results/`, so no §3 cap is violated
by the merge itself — but #204 builds its headline on an unproven step in #199's sketch,
which is exactly what §3 forbids.

## What I reimplemented, clean-room

`scratchpad/exact.py`: my own `Q(sqrt 3)` type with my own sign routine, my own linear
solve for the circuits (not the cross-product formula), my own breakpoint derivation, my
own closed-form wall positions. Result: the floor holds. Eight endpoint margins

```
C u=0            +1.661531e-11      A u=1/3          +2.684755e-03
C u=1422669/...  +7.559869e-12      S u=1/3          +1.557136e-02
A u=1422669/...  +7.561896e-12      S u=1363695/...  +5.565411e-11
                                    B u=1363695/...  +5.565678e-11
                                    B u=1            +6.570092e-03
```

Cross-checks that mattered:

- Triangle floors `C 0.068621502501`, `A = D 0.035058235184`, `B 0.083282977323`, agreeing
  between my exact 6-orbit breakpoint enumeration and a 2e5-point float sweep.
- Winding one by turning number (exterior angles sum to `2pi`, not `4pi`), not by
  all-left-turns.
- Walls of `det(v_i, u_phi)` are at `u = t_i` and `u = -1/t_i`, product `-1`, so at most one
  per direction lies in `[0,1]` — this is *why* the authors' two-endpoint sign test is
  sound, and neither PR says so.
- Evenness in `phi` checked directly at `u = 1/7, 2/5, 9/10`, not only structurally.
- The reflected worm has the same edge-direction multiset with the same lengths, so its
  hull is a *translate* of `P`. Reflections are a non-issue for this witness.

For #204 I rebuilt `E, O, M` from the envelope rather than reading the derivation: exact
agreement at the KKT point (spread `5.6e-17`) and worst discrepancy `5.6e-17` over a `3^3`
stencil at `+-1e-4`, ten orders of magnitude wider than the Krawczyk box. Multipliers
`(0.490847, 0.437422, 0.071731)`, `|d1 x d2| = 7.01e-2`, unit-tangent curvature
`-0.289333`, which is their unnormalised `-0.00142269` divided by `|t|^2 = 0.07012^2`.

For #199 I hand-derived all four support formulas and both crossing equations. Every
coefficient matched, including the awkward `q sa cb/(2 sb)` in `A(phi)` and the reduction
`4 cb^2 + 3 sb^2 = 3 + cb^2` behind the central root.

## Defects found

1. **#205, blocking.** `triangle_floor` rotates the frame by `+v_i` only, so it enumerates
   3 of the 6 breakpoint orbits — the `R_theta d = -v_j` family (the 60°-rotated triangle)
   is missing. `min` over a subset is an *upper* bound on the true minimum, so the certified
   floor could come out too high: wrong direction for a lower-bound certificate. It happens
   to coincide on this witness (I checked all six orbits), but the code does not prove it.
   #195's `tf()` does enumerate both signs; the two agree by luck, not by construction.
2. **#199 / #204, blocking.** `floor <= min(E,O,M)` is asserted. `E = C(0)` is one
   allocation's bound at one angle, so `E <= envelope(0)`, which yields `floor <= envelope(0)`
   and *not* `floor <= E`. The missing hypothesis is that the named well is the arg max over
   allocations at its own angle. True here, and cheap to close — at `phi = 0` it follows from
   their own closed forms.
3. **Wording, everywhere.** "every maximal balanced allocation" is false: the balanced
   polytope has eight vertices (also `q = L` and two 4-support vertices), not four plus zero.
   Only circuits are enumerated. Harmless for soundness — more allocations only raise the
   max — but the claim of exhaustiveness is wrong. Also worth noting the objective is
   *concave* in `q`, so the true maximiser need not be a vertex at all.
4. **Protocol.** #205 and #201 carry no tier label (§1 requires exactly one). #204's README
   has no `status:` line while reading as a theorem. #205 is Codex auditing Codex and its
   "clean-room audit" heading overstates what the problem `RULES.md` §4 allows.

## The thing I want a human to look at

The stack repeats that the area interpretation is "conditional on the finite-polygon
mixed-area/common-fan bridge". As far as I can see that bridge is elementary: mixed area in
the plane is monotone and Minkowski-linear, so for convex `K` containing `P`, `T`, `S`,

```
V(P_q,T) + V(P_r,S) <= V(P_q,K) + V(P_r,K) = V(P_q (+) P_r, K) = V(P,K) <= V(K,K) = A(K),
```

using that a Minkowski summand is a subset up to translation. If that reading is right, this
chain is one short step from `A(K) >= 0.23518745713`, against a published record of
`0.232239` — i.e. §7 territory (`extraordinary-claim`, both humans, no merge). Either the
bridge is harder than it looks, or something upstream is wrong, or the record is beaten. I
could not resolve which inside the budget and I did not treat it as settled in any review.

## A trap for the next reviewer

A `pi/200000` sweep reports #195's rational witness as having a *higher* floor than #204's
optimum, which would refute local maximality. It does not — the sweep steps over the kink at
the `C = A` crossing, where the exact value is `0.23518745713756`, correctly below
`0.235187457145455`. I believed the wrong thing for several minutes. Grid searches are not
safe near these kinks at the `1e-12` scale; use the exact crossing.

## Outcome

| PR | verdict |
|---|---|
| #195 | approved and merged at `f66178c3` after full independent reconstruction; issue #193 lifecycle labels cleared |
| #199 | changes requested — derivation fully re-derived and correct; upper bound unproved |
| #204 | changes requested — wells/multipliers/LICQ/curvature all reconstructed; dominance step and Krawczyk uniqueness open |
| #205 | changes requested — conclusion right, orientation enumeration incomplete |
| #186, #187, #189, #191, #192, #201, #203 | **not reviewed.** No formal review filed. #191 is CONFLICTING with main. The `four-edge-support` trees in #186/#187/#192 are byte-identical (`2abd070e`), so those add/add overlaps will not conflict. |

Scratch verifiers live in the session scratchpad, not the repo: `exact.py` (the clean-room
`Q(sqrt 3)` checker), `num.py`, `tri.py`, `wells.py`, `wells2.py`, `kkt.py`, `alloc8.py`.
