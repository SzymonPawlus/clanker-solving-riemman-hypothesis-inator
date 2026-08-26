# The four-grain staircase family, certified exactly at n = 40 and n = 49

**These are CONSTRUCTIONS (upper bounds). No optimality is claimed anywhere in this file, and
none of `n = 17, 24, 31, 40, 49` is a solved case.**

```
status:  numerical  — every certificate and every count below (exact arithmetic,
                      but computation, not proof; and not cross-family checked)
         sketch     — the family law and the geometric mechanism, prose by an agent
author:  claude (Opus 5), worker r4-famcert (generator) + manager (validation ladder), 2026-08-24
issue:   #110
code:    experiments/packing-r4-famcert/
kill:    KILL-CRITERION.md — did not fire
```

**Nothing here is assumable** (`RULES.md` §3). Depends on the `cited` optima at
`n = 4, 7, 12` and on nothing unmerged.

> **Provenance.** The generator, dissector and exact checker were written by the `r4-famcert`
> worker, which was terminated by a connection loss before writing up or emitting certificates.
> **The validation ladder `validate.py` and this write-up are the manager's**, and the results
> below are from the manager's own run, not from the worker's unrecorded claim. The worker's
> last message asserted "n = 40 and n = 49 are feasible and tight" *before* running its
> reproduction gate; that assertion was not taken on trust — it is re-established here in the
> required order, gate first.

---

## 0. The family

Round-3 §0.2 recorded `n = 17, 24, 31` as three isolated open cases with values in
`Q(√3)`, "spaced 7 apart". That spacing was a two-term coincidence (corrected in
`attacks/r3-approaches/README.md` §0.2). They are the `[16,34]` window of a single staircase,
which the generator realises in closed form:

$$n(j) \;=\; \Delta(j+2) + \left\lfloor j/2 \right\rfloor + 1, \qquad
s(n(j)) \;=\; 2j + 4\sqrt3, \qquad d = 2j + 2\sqrt3 .$$

| j | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| n | 4 | 7 | 12 | 17 | 24 | 31 | **40** | **49** | 60 |
| s | 4√3 | 2+4√3 | 4+4√3 | 6+4√3 | 8+4√3 | 10+4√3 | **12+4√3** | **14+4√3** | 16+4√3 |
| status | proven | proven | proven | open | open | open | open | open | open |

Equivalently the merge of `4Δ(k) = 4, 12, 24, 40, 60` and `2(k+1)^2 − 1 = 7, 17, 31, 49`.

**The mechanism** (`sketch`, from the generator's docstring, reverse-engineered from the
`n = 17/24/31` certificates): four same-orientation triangular-lattice grains — two bottom
corners, an **inverted** centre grain, and a top grain — separated by length-2 "stacking-fault"
seams. The grain offsets `(0,0)`, `(√3,1)`, `(√3,3)`, `(2√3,0)` are all sums of length-2 vectors.
With `U = ⌈j/2⌉`, `M = ⌊j/2⌋`, the grain sizes are `Δ(U+1)` twice and `Δ(M+1)` twice, less one
site when `j` is odd — which is exactly `n(j)`.

## 1. Gate 1 — reproduction. The generator must produce what is already known.

A generator that gets the right `n` and `d` with the wrong configuration is not validated, so
this gate compares **point sets**, not just side lengths.

| j | n | s | feasible | tight | min sq dist = 4 | contacts | vs known |
|---|---|---|---|---|---|---|---|
| 0 | 4 | 4√3 | yes | yes | yes | 3 | **matches `cited` proven optimum** |
| 1 | 7 | 2+4√3 | yes | yes | yes | 7 | **matches `cited` proven optimum** |
| 2 | 12 | 4+4√3 | yes | yes | yes | 18 | **matches `cited` proven optimum** |
| 3 | 17 | 6+4√3 | yes | yes | yes | 28 | same `s`; point set differs (shared 12/17) |
| 4 | 24 | 8+4√3 | yes | yes | yes | 45 | **point set identical to the committed certificate** |
| 5 | 31 | 10+4√3 | yes | yes | yes | 61 | same `s`; point set differs (shared 30/31) |

**Gate 1 passed.** Three `cited` proven optima are reproduced exactly, and `n = 24` reproduces the
committed `r3-qsqrt3` certificate point-for-point.

**On the two that differ — RESOLVED, see [`../r5-n17/`](../r5-n17/README.md).**

At `n = 17` and `n = 31` the generator emits a *different* valid packing at the *same* `s`. Both
are feasible and tight, so both are legitimate constructions. When this file was first written the
`n = 17` case (5 points differing, against a reported single rattler) was flagged as unexplained
and as the first thing a reviewer should check. A dedicated audit lane then checked it, with its
own `Q(√3)` layer, parser and checker written from the problem statement and validated on proven
optima plus negative controls. The outcome, `numerical`:

- **All six point sets are exactly feasible, exactly tight, min squared distance exactly 4.**
  Nothing is broken, and the three overlap figures quoted above (12/17, 24/24, 30/31) are correct
  — re-derived, not inherited.
- **`n = 24`: identical, and now explained.** That packing is invariant under the *full* `D₃`
  (stabiliser order 6) and is infinitesimally rigid. An optimiser and a lattice construction had
  nowhere else to land.
- **`n = 31`: one differing point, and it is exactly the rattler.** Its free region is exactly the
  segment `{(x,0) : 6 ≤ x ≤ 4+2√3}` on edge `AB`, endpoints verified feasible and just-outside
  infeasible. The certificate parks it interior at `x = 7`; the generator parks it at the jammed
  left endpoint `x = 6`. **Same packing.**
- **`n = 17`: two genuinely distinct packings at the same `s`** — benign, and the interesting one.
  Ruled out exactly: a rigid motion (all six isometries of the fixed triangle constructed in
  `Q(√3)`; none maps one to the other, and both have trivial stabiliser); rattler freedom (the
  certificate has exactly 1 rattler, the generator 0 — so `r3-qsqrt3`'s rattler count was *right*,
  not an understatement); and any deformation between them (generator rigidity kernel **0**,
  certificate kernel **2**, exactly the rattler's translations). Separating invariants:
  **26 vs 28 contacts, 11 vs 12 boundary points, non-isomorphic contact graphs.** The generator's
  is the more jammed of the two.

So the original suspicion — "related by more than a single free placement" — was correct, and the
resolution is that they are *not related at all*: two distinct tight configurations coexist at
`s(17) = 6 + 4√3`. Nothing here is promoted; the audit is same-model-family, so it is a third
agreeing implementation and not `verified:review`.

## 2. Gate 2 — the predictions, past the published table

Only meaningful because Gate 1 passed.

| j | n | s | pairs checked | feasible | tight | min sq dist = 4 | contacts |
|---|---|---|---|---|---|---|---|
| 6 | **40** | **12 + 4√3** | 780 | yes | yes | yes | 84 |
| 7 | **49** | **14 + 4√3** | 1176 | yes | yes | yes | 106 |

All in exact `Q(√3)`; no floating point in any accept/reject decision. So, as constructions:

$$s(40) \le 12 + 4\sqrt3, \qquad s(49) \le 14 + 4\sqrt3 .$$

**Negative controls** (a checker that accepts everything proves nothing): duplicate point →
rejected; `s` deflated by 1 → rejected; `s` inflated by 1 → **accepted but reported not tight**,
which is the correct behaviour and the one a naive checker gets wrong.

## 3. What this is NOT

- **Not a record, and not new territory.** The published Graham–Lubachevsky table stops at
  `n = 34`, but "no published value here" does **not** mean "nobody has done better". Amore
  (2022, [arXiv:2212.12287](https://arxiv.org/abs/2212.12287)) reports equilateral-triangle
  numerics up to `N = 400`, and that paper is behind this environment's egress block (403 on
  CONNECT). **These are exact certified upper bounds and nothing more.** If Amore's `n = 40` or
  `n = 49` is better, there is no way to know that from here.
- **Not optimality.** Nothing here bears on lower bounds at any `n`.
- **Not assumable.** `numerical`, and same-model-family throughout — problem `RULES.md` §3 needs
  an independently reimplemented checker from a different family before any of this is
  `verified:review`.
- **Not a proof that the law continues.** `n = 60` (`j = 8`) was not certified. The law is
  `sketch`; each member must be verified, never extrapolated. The authoring worker's own first
  `n = 49` transcription came out **infeasible** because of a seam-depth degree of freedom — a
  concrete reminder that the pattern does not certify itself.

## 4. Reproduce

```
cd experiments/packing-r4-famcert && python3 validate.py
```

Deterministic, exact, no seeds, no network. Prints Gate 1, Gate 2 and the negative controls;
transcript committed at `out/validate.txt`.
