# Approach Y — exact tight $\mathbb{Q}(\sqrt3)$ certificates at $n = 17, 24, 31$

**This is a CONSTRUCTION (upper bound). It is not an optimality claim.** What is established is
$s(17) \le 6 + 4\sqrt3$, $s(24) \le 8 + 4\sqrt3$, $s(31) \le 10 + 4\sqrt3$, exactly. Nothing here
bears on the lower bound; all three $n$ remain open.

```
status:  numerical      — every claim in this file, without exception
author:  claude (Opus 5), worker r3-qsqrt3, 2026-08-23
code:    experiments/packing-r3-qsqrt3/   (reproduce: python3 run_all.py, ~11 s)
scope:   round-3 approach Y, exploiting attacks/r3-approaches/README.md §0.2
```

Under [`../../RULES.md`](../RULES.md) §3 this is `numerical` and stays `numerical` until an agent
of a **different model family** writes its own checker from `../../README.md` — not by reading,
importing, or running `check.py`. Until then **nothing here may be built on** (repo `RULES.md` §3),
and the certificates deliberately sit in `experiments/packing-r3-qsqrt3/certificates/` rather than
in `../../results/`.

---

## 1. What was tested

Round-3 §0.2 noticed that among the open cases $16 \le n \le 34$, exactly three have a best-known
value of the form $a + b\sqrt3$ with small integers — $n = 17, 24, 31$, spaced 7 apart and each
$2$ larger than the last — and inferred that these, not $n = 16$, are the cheapest open cases for
exact work. That was a `sketch` observation about a `numerical` table. The question here is whether
it cashes out into an actual artifact: **an exact and *tight* certificate for an open $n$**, of
which the repo had none.

## 2. What was established

All three configurations lift exactly into $\mathbb{Q}(\sqrt3)$, and the certificates are tight.

| $n$ | $d$ | $s$ | coords in $\mathbb{Q}(\sqrt3)$ | rattlers | contacts $= 2$ exactly | on boundary | tight |
|---:|---|---|---:|---:|---:|---:|:--|
| 17 | $6 + 2\sqrt3$ | $6 + 4\sqrt3$ | 16 / 17 | 1 | 26 | 11 | yes |
| 24 | $8 + 2\sqrt3$ | $8 + 4\sqrt3$ | 24 / 24 | 0 | 45 | 15 | yes |
| 31 | $10 + 2\sqrt3$ | $10 + 4\sqrt3$ | 30 / 31 | 1 | 59 | 18 | yes |

In each case the minimum squared pairwise distance is **exactly 4** — not $4 + \epsilon$ and not
$4 - \epsilon$ — and the exact minimal enclosing side equals the declared side. Every arithmetic
step is exact in $\mathbb{Q}(\sqrt3)$; no float appears in any accept/reject decision.

**Three findings worth separating from the headline:**

1. **Tightness is achievable, and it was not before.** The repo's existing generator
   (`experiments/circle-packing-ls/certificate.py`) rounds to rationals and inflates $s$ by
   $\approx 10^{-11}$ until feasibility is restored — honest, but permanently loose. Working in
   the right number field removes the inflation entirely. `RULES.md` §2 requires tightness for any
   record claim, so this is the difference between a certificate that could *support* a record
   claim and one that structurally cannot.
2. **The $\mathbb{Q}(\sqrt3)$ structure is stronger than the table alone suggests.** It is not
   merely that $s(n)$ lies in $\mathbb{Q}(\sqrt3)$ — every *coordinate* does, with numerators
   bounded by 10, and the packings are visibly triangular-lattice blocks with a few defects. The
   snap residuals are $\sim 10^{-15}$ against a proven lattice separation of $4.6\times10^{-3}$,
   so the identification is not a numerical coincidence at the coordinate level either.
3. **The rattlers are real and they are the only non-lattice points.** At $n = 17$ and $n = 31$
   exactly one point fails to snap, and in both cases it is a genuine rattler: at the optimiser's
   own float position it clears its nearest neighbour by $2.300$ ($n=17$) / $2.134$ ($n=31$) and has
   strict slack in every wall constraint. This is a mild
   independent confirmation of the rest: the snap procedure did not silently absorb a defect,
   it isolated it.

   > **Narrowing added by the manager, 2026-08-24, from the audit in
   > [`../r5-n17/`](../r5-n17/README.md).** Every number in this item is correct, but the phrase
   > "strict slack in every wall constraint" describes the **optimiser's float position**, not the
   > position actually committed. The committed `n = 31` rattler sits at `(7, 0)` — i.e. **on**
   > wall `AB` — and rattles by *sliding along the edge*, its exact free region being the segment
   > `{(x,0) : 6 ≤ x ≤ 4+2√3}`. Consequence for anyone writing tooling: a rattler census defining
   > "rattler = no contact at distance 2 **and** strictly interior to all three walls" will report
   > **0 rattlers at `n = 31`** and appear to contradict this paragraph. That is a definitional
   > gap, not a defect in the certificate. The audit also confirmed the rattler *counts* here are
   > right rather than understated: at `n = 17` the certificate has exactly 1 rattler and the
   > `r4-famcert` generator has 0, and the two configurations are genuinely distinct packings, not
   > rattler-variants of one another.

## 3. Relation to the published record

`beats_record: "no"` in all three certificates. These **reproduce** the Graham–Lubachevsky values
(EJC 2 (1995) #A1, as tabulated in `experiments/circle-packing-search/reference.py`) exactly, which
`RULES.md` §4 names as the good outcome. Agreement is to within one unit in the last published
significant figure ($n = 17$ and $31$ match all 15 s.f.; $n = 24$'s published $0.174457630187010$
differs by 1 in the 15th place from the implied $0.174457630187009439$ — the same last-place offset
already recorded in `experiments/circle-packing-ls/README.md`).

No record is claimed and §4's escalation procedure was not triggered, because nothing here is
better than the published value. Had it been, the ordering §4 prescribes — bug, misread table,
infeasible configuration, genuine record — would apply.

## 4. What this does *not* show

- **Not optimality.** $6 + 4\sqrt3$ is an upper bound on $s(17)$. Whether it is $s(17)$ is exactly
  as open as it was. The 26 exact contacts at $n = 17$ are suggestive of rigidity and are *not*
  an argument: a jammed configuration is a local statement.
- **Not that the published optima *are* these numbers.** §1's agreement is a 15-digit float
  match. A proof would need the contact system's exact solution to be shown unique, which is not
  attempted here.
- **Not a dependency for anything.** `numerical` (`RULES.md` §3).

## 5. What it does buy the campaign

- A validated exact pipeline from LS float output to a tight certificate, with solved-instance and
  negative controls, reusable for any $n$ whose optimum lies in a small field.
- The first exact tight certificates for open $n$ in this repo — the artifacts an optimality proof
  would eventually have to match, and concrete input for approach **V** (the contact graphs at
  $n = 17, 24, 31$ are now exactly known, not float-estimated).
- A cheap negative signal about $n = 16$: it is the one case in this range where this method does
  not apply, which is consistent with, but does not explain, why it has resisted the campaign's
  effort.

## 6. Kill-criterion

Did not fire. See [`KILL-CRITERION.md`](KILL-CRITERION.md).

## 7. Least certain step

Not the arithmetic — the check is short and has negative controls. The exposure is **convention**:
if the triangle placement or the meaning of `side_length` were read differently here than in
`../../README.md`, every number above would be self-consistent and wrong. That is precisely the
failure mode `../../RULES.md` §3's independent reimplementation exists to catch, and it is the
reason this is `numerical` rather than anything stronger.
