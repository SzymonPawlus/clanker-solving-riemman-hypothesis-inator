# Audit — the `n = 17` disagreement between `r3-qsqrt3` and `r4-famcert` is real, benign, and now explained

**This is an AUDIT of two existing CONSTRUCTIONS. No optimality is claimed anywhere in this file,
and none of `n = 17, 24, 31, 40, 49` is a solved case.** Both configurations remain upper-bound
certificates: `s(17) ≤ 6 + 4√3`, `s(24) ≤ 8 + 4√3`, `s(31) ≤ 10 + 4√3`.

```
status:  numerical  — every check and count below (exact Q(sqrt3) arithmetic; computation,
                      not proof; same model family as both authors, so not cross-family checked)
         sketch     — the explanation and the recommendation in §5
author:  claude (Opus 5), worker r5-n17, 2026-08-26
code:    experiments/packing-r5-n17/   (reproduce: python3 run_all.py, ~40 s)
kill:    KILL-CRITERION.md — did not fire; neither configuration is broken
```

**Nothing here is assumable** (`RULES.md` §3), and this worker **cannot** grant `verified:review`:
it is the same model family as both authors, so problem `RULES.md` §3 is not satisfied and nothing
is promoted. What this buys is a *third* independent implementation agreeing with the other two.

---

## 0. Verdict in one paragraph

`attacks/r4-famcert/README.md` §1's flag should be **resolved as benign, with the reason, and
narrowed** — option (a)+(b), not escalated. Both point sets are exactly feasible, exactly tight,
and have minimum squared pairwise distance exactly 4, at all three `n`, verified here by a checker
written from the problem statement rather than from either author's code. The `12/17` figure is
correct. It is **not** explained by a rattler and it is **not** explained by a rigid motion: at
`n = 17` the two are **genuinely distinct, non-isomorphic packings at the same side length**, one
of which (the generator's) is infinitesimally rigid and the other of which is rigid apart from one
free interior rattler. That is a legitimate and unremarkable state of affairs for a packing
problem, and the famcert README's own §1 already allows for it — what was missing was the
demonstration, and one invariant that separates the two. Separately, the `n = 31` case **is**
exactly the one-rattler story the famcert README hoped for, and `n = 24` **is** identical.

## 1. What I verified myself, and what I inherited

Inputs, and their provenance (round-5 protocol §6):

| input | source | did I re-derive it? |
|---|---|---|
| `n = 17/24/31` certificates | `experiments/packing-r3-qsqrt3/certificates/*.json` | **parsed with my own parser**, re-checked with my own checker |
| four-grain generator | docstring spec of `experiments/packing-r4-famcert/generator.py` | **re-transcribed from the spec** into `famgen.py`; its output cross-checks against the original generator for `j = 0..5` |
| "shared 12/17", "30/31", "identical at 24" | `attacks/r4-famcert/README.md` §1 | **re-derived** — all three confirmed |
| famcert Gate-1/Gate-2 table (contacts at `j = 0..7`) | `attacks/r4-famcert/README.md` §§1–2 | **re-derived**, all eight rows |
| `r3-qsqrt3` rattler/contact/boundary table | `attacks/r3-qsqrt3/README.md` §2 | **re-derived**; correct, with one wording narrowing (§4) |
| triangle placement, meaning of `side_length`, closed inequalities | problem `RULES.md` §2 | taken as given (they are the rules) |

Nothing else is inherited. Arithmetic is exact `Q(√3)` (`Fraction` pairs) with an exact sign rule;
no float enters any accept/reject decision. The checker was validated *before* use on `n = 3, 4,
6, 10` proven optima and on five negative controls, including the one a naive checker gets wrong
(`s` inflated → accept, but report **not tight**).

## 2. Both configurations are valid — this is the important negative result

| `n` | configuration | feasible | min sq dist | tight (`d_min = d`) | contacts | boundary pts |
|---:|---|:--|:--|:--|--:|--:|
| 17 | `r3-qsqrt3` cert | **yes** (136 pairs) | **exactly 4** | **yes**, `6 + 2√3` | 26 | 11 |
| 17 | famcert `j = 3` | **yes** (136 pairs) | **exactly 4** | **yes**, `6 + 2√3` | **28** | **12** |
| 24 | `r3-qsqrt3` cert | yes (276) | exactly 4 | yes, `8 + 2√3` | 45 | 15 |
| 24 | famcert `j = 4` | yes (276) | exactly 4 | yes, `8 + 2√3` | 45 | 15 |
| 31 | `r3-qsqrt3` cert | yes (465) | exactly 4 | yes, `10 + 2√3` | 59 | 18 |
| 31 | famcert `j = 5` | yes (465) | exactly 4 | yes, `10 + 2√3` | **61** | 18 |

**Neither pipeline is broken.** The kill-criterion (either configuration infeasible, not tight, or
misreported) did **not** fire. As a by-product the whole famcert table re-verifies with my
checker, `j = 0..7`, contacts `3, 7, 18, 28, 45, 61, 84, 106` — matching their §1/§2 tables row
for row, including `n = 40` and `n = 49`.

## 3. What explains each case

### 3.1 `n = 24` — identical, and fully symmetric

Exact set equality: `24/24`. Extra fact not previously recorded: this configuration is invariant
under the **whole** symmetry group of the triangle (stabiliser order 6, `D₃`) — which is exactly
why an optimiser's output and a lattice construction landed on the same point set, and it is
infinitesimally rigid (rigidity rank `48 = 2n`, kernel 0). The "identical" claim is confirmed, not
inherited.

### 3.2 `n = 31` — one rattler, on the boundary, and the famcert README's guess is right

Exact set difference is **one point**: the certificate has `(7, 0)`, the generator has `(6, 0)`.
Everything else coincides. That point is a genuine rattler and its free region is, exactly,

  the segment `{ (x, 0) : 6 ≤ x ≤ 4 + 2√3 }` on the bottom edge, of length `2√3 − 2 ≈ 1.4641`.

Verified exactly: `x = 6` and `x = 4 + 2√3` are feasible, `6 − 1/1000` and `4 + 2√3 + 1/1000` are
not. The certificate places it strictly inside the segment (`x = 7`, zero contacts, rigidity
kernel **1** — precisely this one sliding degree of freedom). The generator places it at the left
endpoint, where it picks up 2 contacts and the configuration becomes infinitesimally rigid
(kernel 0, 61 contacts). **Same packing, rattler parked differently.** The famcert README's
"one rattler ⇒ one differing point" reading is correct here.

### 3.3 `n = 17` — two genuinely different packings, and here is what separates them

Five points differ each way. Tested and **excluded**:

- **A rigid motion.** All 6 isometries of the fixed triangle (3 rotations, 3 reflections, built
  exactly in `Q(√3)` as the affine maps permuting `A, B, C`) were applied to the certificate's
  point set; **none** maps it to the generator's. Both configurations have trivial stabiliser.
  This was the cheapest and most likely explanation and it is dead.
- **Rattler freedom.** The certificate has exactly **one** rattler — `(5/2, 4)`, zero contacts,
  strictly interior, free disc of radius exactly `5√3/4 − 2 ≈ 0.16506` (wall `AC` binds; the
  nearest neighbour is at squared distance `77/4 − 8√3 ≈ 5.3936`, which would allow `≈ 0.3226`).
  The generator has **zero** rattlers. So the `r3-qsqrt3` rattler count is *not* an understatement:
  it is exactly right, and one rattler genuinely cannot account for five points.
- **A continuous deformation between them.** The generator's configuration has rigidity rank
  `34 = 2n`, kernel **0**: it is infinitesimally rigid, hence an isolated solution. The
  certificate's has kernel **2** — exactly the rattler's two translational degrees of freedom and
  nothing more. Neither can flex into the other.

What is left is the truth: **two distinct packings of 17 points at `s = 6 + 4√3`.** They are
separated by honest invariants:

| invariant | `r3-qsqrt3` cert | famcert `j = 3` |
|---|--:|--:|
| contacts at distance exactly 2 | 26 | **28** |
| points on the boundary | 11 | **12** |
| contact-degree histogram | `0:1, 2:3, 3:6, 4:7` | `2:4, 3:5, 4:7, 5:1` |
| rattlers (no contact, strictly interior) | 1 | 0 |
| rigidity-matrix kernel | 2 | **0** |
| stabiliser in `D₃` | trivial | trivial |

The contact graphs are not isomorphic (different edge counts and different degree sequences), so
this is not a relabelling. The generator's packing is the **more jammed** of the two: strictly
more contacts, one more boundary point, no rattler, infinitesimally rigid. The certificate's is
the optimiser's local minimum with a loose circle in it. Both are valid, and neither is better —
they realise the same `s`.

The four differing certificate points are `(4+√3, 1)`, `(5+√3, 1+√3)`, `(3+√3, 3+√3)` (4 contacts
each) and `(5+√3, 3+√3)` (3 contacts, on wall `BC`); the four differing generator points are
`(3+2√3, √3)`, `(2+√3, 1+2√3)`, `(4+√3, 1+2√3)` (4 contacts each), `(2, 2√3)` (3 contacts, on
`AC`) and `(4+2√3, 2√3)` (3 contacts, on `BC`). None is a rattler; the rearrangement is a genuine
change of the jammed core, not a wobble.

## 4. Two narrowings for the record

1. **`attacks/r4-famcert/README.md` §1** infers from `r3-qsqrt3`'s rattler counts that the `n = 24`
   match and the `n = 17/31` mismatches "correspond". Half of that inference is confirmed
   (`n = 24`, `n = 31`), and half is a coincidence: at `n = 17` the mismatch has nothing to do with
   the rattler. The sentence "the `n = 17` disagreement is larger than one rattler can explain …
   That is not explained here" is exactly right and is what this audit resolves.
2. **`attacks/r3-qsqrt3/README.md` §2, finding 3** says the `n = 17` and `n = 31` rattlers each
   have "strict slack in every wall constraint". That is a statement about the *optimiser's float
   position*, and it does not survive the snap: in the **committed** `n = 31` certificate the
   rattler sits at `(7, 0)`, i.e. **on** wall `AB`, with slack 0 there, and it rattles by sliding
   *along* the edge rather than in a disc. Its rattler status is unaffected (rigidity kernel 1),
   and the counts in that README's table are all correct — but a checker that defines "rattler" as
   "no contact **and** strictly interior to all three walls" will report **0** rattlers at `n = 31`
   and disagree with the table. That definitional gap is worth pinning down before anyone builds a
   rattler census. (My own §3.3 count at `n = 17` uses the strict-interior definition and agrees
   with the table because that rattler *is* strictly interior.)

## 5. Recommendation

`attacks/r4-famcert/README.md` §1's flag: **resolve as benign (a), with narrowing (b).** Suggested
replacement for the unexplained sentence, for whoever owns that file:

> At `n = 31` the two configurations differ in exactly one point, a rattler free to slide along
> the segment `6 ≤ x ≤ 4 + 2√3` of the bottom edge; the generator parks it at the jammed left
> endpoint and the certificate leaves it interior. At `n = 17` they are genuinely two different
> packings at the same `s`: not related by any symmetry of the triangle, contact graphs
> non-isomorphic (26 vs 28 contacts, 11 vs 12 boundary points), the generator's infinitesimally
> rigid with no rattler and the certificate's rigid apart from one interior rattler of free radius
> `5√3/4 − 2`. Audited independently in `attacks/r5-n17/`.

**No escalation.** Nothing is wrong with either pipeline, the certificate schema's interpretation
is unaffected, and no merged sibling result is invalidated.

## 6. What this does *not* show

- **Not optimality.** Nothing here touches lower bounds. `n = 17, 24, 31` are exactly as open as
  before.
- **Not that these are the only two packings at `s = 6 + 4√3`.** Two were compared; no search for
  others was run. "Genuinely distinct" means distinct from each other, not extremal in any sense.
- **Not `verified:review`.** Same model family as both authors (`RULES.md` §3, problem `RULES.md`
  §3). A third agreeing implementation from inside the family raises confidence and promotes
  nothing.
- **Not a claim that infinitesimal rigidity implies local optimality.** Kernel 0 says the
  configuration is an isolated solution of its own contact system at this `s`; it says nothing
  about whether a smaller `s` admits 17 points.

## 7. Least certain step

The `Q(√3)` **conventions**, exactly as `attacks/r3-qsqrt3/README.md` §7 says of itself. My
checker reads the triangle placement, `side_length = s = d + 2√3`, and closed inequalities from
problem `RULES.md` §2 — the same source the other two read. If that reading is wrong, three
implementations are consistently wrong together and this audit does not catch it. That is
precisely what cross-family review exists for. Second-least certain: the rigidity ranks are
first-order only; kernel 0 rules out a first-order flex and hence any finite one, but kernel 2 at
the `n = 17` certificate is an upper bound on the flex count that happens to be attained by the
rattler — I did not prove there is no additional higher-order-only motion, and there cannot be one
here only because the two dimensions are already exhibited as genuine translations.
