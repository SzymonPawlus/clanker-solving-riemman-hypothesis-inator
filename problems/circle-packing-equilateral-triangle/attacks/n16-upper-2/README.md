# Attack n16-upper-2 — CONSTRUCTION / upper bound only

**Claim type (problem [`RULES.md`](../../RULES.md) §1): construction.** This lane asserts
$s(16) \le 9249527159013717/10^{15} + 2\sqrt3 = 12.71362877415147\ldots$ by an explicit,
exactly-verified 16-point certificate, and **nothing else**. No optimality claim of any kind is
made or implied; nothing here may ever be used as an input to a lower-bound argument — an upper
bound is a construction and cannot certify optimality, and the persistent convergence of every
search to the same value is `numerical` evidence permanently, per problem `RULES.md` §1.

- Author: `claude` (worker U2), 2026-08-22 · issue #97 · branch
  `claude/circle-packing-subagents-9yg5gt`
- Code: [`experiments/packing-n16-upper-2/`](../../../../experiments/packing-n16-upper-2/) —
  written from scratch, no code shared with the killed lane [`../n16-upper/`](../n16-upper/) or
  any sibling
- Kill-criterion: [`KILL-CRITERION.md`](./KILL-CRITERION.md), written before any computation

## Kill-criterion outcome, up front

| gate | outcome |
|---|---|
| Validation on `cited` optima ($n = 12, 13, 15$) | **passed** — each reproduced to $\sim 2\times10^{-16}$ (gate required $10^{-9}$) |
| Record trigger ($m > 0.216227269309782 + 10^{-9}$) | **never fired** — nothing beat the record |
| K1 budget kill | not reached — reproduction achieved in 25 s / 1500 solves, then a 600-solve fresh-seed run |
| Exact-gate negative controls (must reject) | **both rejected** — overlap by $10^{-12}$ and exit by $10^{-12}$ each refused by the exact checker |
| K2 exactification kill ($s < 12.71362878$ required) | **passed** — exact certificate at $s = 12.713628774151\ldots$, $9.3\times10^{-13}$ above the float optimum |

## Per-assertion status table

| assertion | status |
|---|---|
| $s(16) \le 9249527159013717/10^{15} + 2\sqrt3$ (the certificate, exact-checked by my own gate) | `numerical` — awaiting an independent checker from the other family (problem `RULES.md` §3); it is **not** assumable, including by me |
| $m(16) \ge 0.216227269309781821734634975396\ldots$ (best found = the Melissen–Schuur record) | `numerical` |
| the searches reproduce Graham–Lubachevsky's printed $d(16)$ to all 15 digits | `numerical` (2100 pinned-seed solves, two independent seeds) |
| contact-graph / rattler / self-stress analysis (§5) | `numerical` — float + SVD/LP diagnostics on the polished configuration |
| the record value $d(16) = 0.216227269309782$ is Melissen & Schuur's / Graham & Lubachevsky's | `cited` — Graham & Lubachevsky, EJC **2** (1995) #A1 (open access), transcribed in `experiments/circle-packing-search/reference.py`; Melissen & Schuur, Discrete Math. **145** (1995) 333–342 (volume confirmed both-families, see `FINDINGS.md` 2026-08-18) |
| no closed form found for $m(16)$ (PSLQ, degree $\le 12$, coefficients $\le 10^8$) | `numerical` — a *negative* search result only; the paper may state one, body not consulted |

## 1. Numbers, re-derived (not taken from the brief)

From the problem README's closed forms and Graham–Lubachevsky's printed $d(16)$, at mpmath 30 dps
(conventions: unit triangle, min pairwise distance $m$; $a = 1/m$ separation-1 side;
$d = 2/m$ repo point-formulation side; $s = 2/m + 2\sqrt3$):

| quantity | value |
|---|---|
| target $m(12) = 2-\sqrt3$ | $0.26794919243112270$ |
| target $m(13)$ | $0.25181323665306048$ |
| target $m(15) = 1/4$ | $0.25$ |
| record $m(16)$ (GL print) | $0.216227269309782$ |
| $\Rightarrow a_{16} \le$ | $4.6247635795063919\ldots$ (the brief's $4.6247637$ is this, loosely rounded) |
| $\Rightarrow s(16) \le$ | $12.713628774150538\ldots$ |
| repo lower bound $1+2\sqrt3$ | $4.4641016151377546$ (`sketch`, unchanged by this lane) |

## 2. Pipeline and controls

Multistart SLSQP maximin (`search.py`; numpy 2.4.6, scipy 1.17.1, Python 3.11.15; seeds on the
CLI, outputs checkpointed to `out/`). Seed families: `uniform`, `lattice_defect` ($T(6)$ minus 5),
`t5_plus_one`, `perturb_best`. Reported $m$ is always measured after projecting the iterate into
the **closed** triangle, so it is feasible-side honest.

**Validation gate first** (400 starts each, seed 20260822):

| $n$ | found | target | miss |
|---|---|---|---|
| 12 | $0.2679491924311226$ | $2-\sqrt3 = 0.2679491924311227$ | $1\times10^{-16}$ |
| 13 | $0.2518132366530603$ | $0.2518132366530605$ | $2\times10^{-16}$ |
| 15 | $0.2499999999999999$ | $1/4$ | $1\times10^{-16}$ |

**$n = 16$:** 1500 solves, seed 20260822, 25 s → best $m = 0.21622726930978173$.
Fresh seed 777, 600 solves → identical to the last digit. **The record trigger never fired;
nothing beat $0.216227269309782$.** Matching it exactly is the good outcome this lane was
scoped for (problem `RULES.md` §4 last paragraph).

## 3. High-precision polish

The float optimum's active set is clean: **20 pair contacts, all within $2.5\times10^{-16}$ of
$m$, then a gap of $5.3\times10^{-3}$ to the next-closest pair**; 13 wall incidences (three of
them corner points touching two edges each). Gauss–Newton in mpmath (60 dps) on the
overdetermined-but-consistent active-set system (33 equations, 31 unknowns) converges
quadratically to residual $1.5\times10^{-61}$:

$$m(16) = 0.2162272693097818217346349753963489711416\ldots$$
$$s(16) \le 2/m + 2\sqrt3 = 12.71362877415054601484208243065486\ldots \ \text{(float-level, not the certificate)}$$

This agrees with **all 15 digits** Graham–Lubachevsky print for $d(16)$. PSLQ (`findpoly`, degree
$\le 12$, coefficients $\le 10^8$, tol $10^{-50}$) finds no small minimal polynomial for $m$, $a$,
$m^2$, $a^2$ or $a/\sqrt3$ — the exact algebraic form remains unidentified here. (Melissen &
Schuur's paper may state one; its body was not consulted in this lane.)

## 4. The certificate and how it was verified

[`n16-certificate.json`](./n16-certificate.json) (canonical copy; identical file in
`experiments/packing-n16-upper-2/out/`). Repo convention: $A = (0,0)$, $B = (d, 0)$,
$C = (d/2, d\sqrt3/2)$, separation $\ge 2$, `side_length` $= s = d + 2\sqrt3$, all inequalities
non-strict, no decimal strings — coordinates are exact rationals with denominator $10^{18}$,
$d = 9249527159013717/10^{15}$ exactly.

Construction: scale the polished points by $d$ (chosen $10^{-13}$ relatively above $2/m$),
contract toward the incenter by $1 - 10^{-14}$ (every boundary point gains
$\approx 2.7\times10^{-14}$ of clearance), round to the $10^{-18}$ grid (moves each point
$< 7.1\times10^{-19}$). Every rounding loss is orders of magnitude below the slack it spends.

Verified by [`exact_gate.py`](../../../../experiments/packing-n16-upper-2/exact_gate.py) in pure
`fractions.Fraction` arithmetic — **no floats in any decision**:

- all $\binom{16}{2} = 120$ squared distances $\ge 4$; the exact minimum is
  $4 + 7.2\times10^{-13}$ (as a fraction, exactly);
- containment in the closed triangle via $y \ge 0$, $x \ge 0 \wedge 3x^2 \ge y^2$,
  $d - x \ge 0 \wedge 3(d-x)^2 \ge y^2$;
- **tightness:** the exact minimal enclosing side for these points is
  $d_{\min} = 125533377979040259/2\cdot10^{16} + (5149141550127628529/3\cdot10^{18})\sqrt3$
  (computed and compared exactly in $\mathbb{Q}(\sqrt3)$); $d - d_{\min} \approx 3.1\times10^{-14}$,
  so the certificate is **untight by $< 10^{-13}$** and is claimed as an honest upper bound, not a
  tight one (a record claim would require tightness; none is made);
- **negative controls:** the same configuration with (A) one pair pushed to overlap by
  $\sim 10^{-12}$ and (B) one point moved outside by $10^{-12}$ is **rejected** in both cases.

## 5. Structure: contact graph, rattler, self-stresses

Independent analysis (`contacts.py`, plus SVD/LP diagnostics), tolerance $10^{-7} m$ against a
next-nearest gap of $5.3\times10^{-3}$, so the active set is unambiguous at float precision:

- **15 jammed points + 1 rattler.** In my indexing the rattler is point 13 at
  $\approx(0.504, 0.420)$ (unit triangle) with **zero** contacts: nearest neighbours at
  $0.2215, 0.2220, 0.2264$ against $m = 0.21623$ — clearance $5.3\times10^{-3}$, caged by points
  $\{0, 1, 3, 5, 15, 9\}$. Rattlers are reported, not fixed (problem `RULES.md` §5).
- **Jammed core: 20 pair contacts + 13 wall incidences = 33 constraints on 30 coordinates.**
  Three points sit exactly on corners (two wall constraints each): bottom-left, bottom-right,
  and the apex.
- **Rigidity:** the $33\times30$ rigidity matrix has full column rank 30 (smallest singular value
  $0.064$) — zero flexes, and a **3-dimensional self-stress space: the core is hyperstatic by 3,
  not isostatic**.
- **Strict complementarity:** an LP over the multiplier polytope finds a KKT multiplier vector
  with **minimum component $+0.0114 > 0$** — every one of the 33 constraints can carry strictly
  positive force. First-order rigid + strictly positive self-stress is the standard signature of
  a locally jammed maximin configuration.
- The configuration has no mirror symmetry (mismatch $0.13$ under $x \mapsto 1-x$).

**Disagreement with the prior structural claim, stated plainly.** A prior lane reported "$P_4$ is
a rattler with a single contact; the other 15 points are isostatic (30 constraints, 30 dof)". My
independent count of the same packing (same $m$ to 16 digits) gives **33** constraints, because
the three corner points each touch **two** edges; counting each corner as one constraint gives
exactly 30, which is the likely origin of the isostatic reading. The SVD is unambiguous: rank 30
with 33 constraints is hyperstatic with 3 self-stresses, not isostatic. And a rattler's contact
count is not an invariant — the rattler floats in a cage with $5\times10^{-3}$ of slack, so
whether it grazes one neighbour is an accident of where the optimiser left it (mine has zero
contacts). The two analyses agree on the substantive point: 15 jammed + 1 rattler. This
discrepancy is a reviewable finding, not an attack on the sibling lane; both claims are
`numerical`.

## 6. Record check (informational — no improvement is claimed)

Nothing here beats the record, so problem `RULES.md` §4 is not triggered; for completeness:
Graham & Lubachevsky (EJC **2** (1995) #A1, open access, transcribed in
`experiments/circle-packing-search/reference.py`) print $d(16) = 0.216227269309782$, which my
independent optimum matches to all 15 digits. WebSearch surfaces the Melissen & Schuur PDF at
`ris.utwente.nl` and its ScienceDirect page as the sources for $n = 16$ (direct fetch is blocked
in this session; the volume-145 provenance question is already settled both-families in
`FINDINGS.md`, 2026-08-18). Friedman's and Packomania's per-$n$ pages could not be fetched
directly; no search result contradicts the value.

## 7. What to review hardest

1. **`exact_gate.py` §containment**: the squared-comparison encoding of
   $\sqrt3 x \ge y$ as $x \ge 0 \wedge 3x^2 \ge y^2$ (and the $\mathbb{Q}(\sqrt3)$ sign routine
   `sqrt3_sign`). A sign slip there voids the certificate. Per problem `RULES.md` §3 the real
   review is an **independently written checker**, not a read of mine.
2. The **active-set selection** feeding the polish (tolerance $10^{-7}$): defensible because of
   the $5.3\times10^{-3}$ spectral gap, but it is the one place a wrong branch would silently
   polish to a wrong (lower) stationary value — mitigated by the result matching GL's 15 digits.
3. The **hyperstatic-vs-isostatic** disagreement in §5: recount the corner incidences.
4. The certificate's `side_length_note` and `beats_record` fields are prose; the load-bearing
   fields are `side_length` and `coordinates` only.

## 8. Reproduce

See [`experiments/packing-n16-upper-2/README.md`](../../../../experiments/packing-n16-upper-2/README.md).
Everything is pinned: seeds 20260822 (main) and 777 (fresh), Python 3.11.15, numpy 2.4.6,
scipy 1.17.1, mpmath 1.4.1. Total recorded compute ≈ 1 minute wall on one core equivalent.
