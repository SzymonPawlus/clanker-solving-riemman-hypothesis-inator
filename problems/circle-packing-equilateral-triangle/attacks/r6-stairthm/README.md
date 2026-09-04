# The four-grain staircase, proved for every j

**CONSTRUCTION / upper bound only. No optimality is claimed anywhere in this file, and every
`n(j)` for `j ≥ 3` is an open case.**

```
status:  sketch     — the theorem's prose and its case structure (agent-written, uncross-examined)
         numerical  — every finite exact check below, and the n = 60 certificate
author:  claude (worker r6-stairthm), 2026-08-26; write-up by the manager after the worker
         was terminated by an account session limit mid-run
issue:   #110, round-6 execution of the ideation lane's STAIR-THM proposal
code:    experiments/packing-r6-stairthm/
kill:    KILL-CRITERION.md — did not fire
```

**Nothing here is assumable** (`RULES.md` §3). It does not use the unmerged `n = 16` bound, and it
re-derives the construction from `r4-famcert`'s published spec rather than importing its code.

---

## 0. The statement

For `j ≥ 0` define

$$n(j) = \Delta(j+2) + \lfloor j/2 \rfloor + 1, \qquad s(n(j)) = 2j + 4\sqrt3, \qquad d = 2j + 2\sqrt3.$$

**Theorem (`sketch` + `numerical`).** For **every** `j ≥ 0`, the four-grain configuration `P(j)` is
feasible (all pairwise distances `≥ 2`), contained in the closed `T_d`, and **tight** (the exact
minimal enclosing side equals `d`). Hence

$$s(n(j)) \;\le\; 2j + 4\sqrt3 \qquad \text{for all } j.$$

`n(j) = 4, 7, 12, 17, 24, 31, 40, 49, 60, 71, 84, 97, 112, 127, 144, …`

This replaces `r4-famcert`'s **member-by-member** verification, whose own write-up warned that the
law was `sketch` and **must not be extrapolated** — its author's first `n = 49` transcription was
actually infeasible. The first three members (`n = 4, 7, 12`) are `cited` **proven optima** and sit
on the law exactly.

## 1. How the proof is finite

The construction is four same-orientation triangular-lattice grains — two bottom corners, an
inverted centre, a top grain — at offsets `(0,0)`, `(√3,1)`, `(√3,3)`, `(2√3,0)`. Grain sites are
indexed by `(r, x)` with `x ≡ r (mod 2)`, parameterised by `U = ⌈j/2⌉`, `M = ⌊j/2⌋`.

- **Step A — grain lemmas as symbolic identities.** All **17** range lemmas (`r ≥ 0`, `x − r ≥ 0`,
  `x + r ≤ 2U`, `r ≤ U`, and their per-grain analogues) are verified to be *identities*
  in `(U, M, p, q)` — each slack is an explicit nonnegative expression such as `2U − 2p − 2q`. Being
  identities, they hold for **every** `j`, which is what makes the argument finite rather than
  per-member. Re-checked mechanically against the generated site lists for `j = 0..40`, including
  `x ≡ r (mod 2)` at every site.
- **Step B — forbidden difference vectors, `j`-free.** *Intra-grain* violating pairs are
  **impossible**: the separation-2 triangular lattice has minimum distance exactly 2
  (`dx² + 3dr² ≥ 4` whenever `dx ≡ dr (mod 2)`, not both zero), so `F(g,g) = ∅` for all four grains.
  *Cross-grain* forbidden sets are finite and independent of `j`, with `|F| = 3` or `4` for each of
  the 12 ordered pairs — **42 vectors in total, checked once.**
- **Step C — separating functionals.** For each ordered grain pair a linear functional separates the
  grains' index ranges, and the finite check `L(f) > 0` rules out the forbidden vectors for all `j`.
- **Containment and tightness** are proved by explicit inequalities against the three walls, with the
  worst cases exhibited (`AC` at `x − r = 0`, `BC` at `2j − x − r = 0`). Tightness holds because
  `max_g (a + b/3)√3 = 2√3` is **attained** by grain BR, which contains `(r,x) = (0, 2j)` for every
  `j`; confirmed mechanically for `j = 0..40`.

## 2. Independent confirmations

- **Brute force, `j = 0..14`** (up to `n = 144`, 10 296 pairs at `j = 14`): all 15 members feasible,
  contained and **tight** in exact `Q(√3)`. This is a *confirmation* of the theorem, not a
  substitute — `theorem.py` covers every `j`, this covers 15 of them pair by pair.
- **`n = 60` (`j = 8`) certificate emitted** — the first member nobody had ever verified.
  **The manager re-verified it independently** from the certificate alone, with a self-tested
  parser: 1770 pairs, **0 separation violations**, **135 contacts at distance exactly 2**,
  **0 containment violations**, 27 boundary points, and exact minimal enclosing `d = 16 + 2√3`
  equal to the declared value — **tight**.
- **Periodicity pilot reproduced and extended.** The round-6 ideation lane's claim (cross-grain
  close-pair types 2-periodic in `j` from `j = 4`, 36 even / 38 odd, through `j = 12`) was
  independently reproduced and pushed to `j = 13`, with exact set equality `types(j) = types(j−2)`.
- **Seam depth is forced.** A scan over alternative grain offsets shows `C = (1,2)`, `T = (1,3)` is
  the *unique* working choice in a 441-point box; every neighbouring offset fails on separation or
  containment. This is precisely the degree of freedom that made a hand transcription infeasible in
  `r4-famcert`.
- **Falsification search at `n = 60` found nothing better.** A relaxation started *at* the
  construction returns exactly the construction's value (`m = 0.102753265449690`, `d = 19.4641…`).

## 3. What this is not

- **Not optimality.** `n(j)` for `j ≥ 3` are open. This bounds `s` from above and says nothing about
  lower bounds.
- **Not a record claim.** Amore (2022) reports triangle numerics to `N = 400` and is behind this
  environment's egress block, so "no published value" does not mean "nobody has done better"
  (problem `RULES.md` §4). The falsification search found nothing better *within its budget*, which
  is weak evidence and not a uniqueness claim.
- **Not assumable, and not cross-examined.** `sketch` + `numerical`, same model family throughout.
  Step A's identities and the `Q(√3)` arithmetic are machine-checked; the *case structure* — that
  Steps A–C together cover every pair for every `j` — is agent prose and is the thing a reviewer
  should attack first.

## 4. A manager error worth recording

Verifying the `n = 60` certificate, the manager's **first** independent checker reported **14
separation violations** — which would have been a refutation of the whole lane. It was wrong: a
regex parser read `"2*sqrt(3)"` as `2 + 1·√3` instead of `0 + 2·√3`. The certificate was correct
throughout.

This is the fourth instance in this campaign of the same pattern, and the first where the fault was
in the *checker* rather than in the input selection. The fix that caught it was cheap and should be
standard: **the corrected parser self-tests on seven hand-written cases before it is allowed to
judge anything.** A checker that has not been tested against known answers is not evidence, in
either direction.

## 5. Reproduce

```
cd experiments/packing-r6-stairthm
python3 theorem.py      # Steps A-C, the general-j argument  (STDLIB ONLY, no deps)
python3 validate.py     # brute-force exact check, j = 0..14, emits the n=60 certificate
python3 periodicity.py  # the 2-periodicity of cross-grain types
python3 seamdepth.py    # uniqueness of the seam offsets
```

Exact `Q(√3)` throughout; no float in any accept/reject decision.
