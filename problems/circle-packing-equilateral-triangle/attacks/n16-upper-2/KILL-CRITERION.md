# Kill-criterion — attack `n16-upper-2`

Written **before** any optimiser was run, per repo [`RULES.md`](../../../../RULES.md) §6.2.
Committed as-is; the attack is judged against this text, not a rewritten one.

- Author: `claude` (worker U2), 2026-08-22, issue #97, branch
  `claude/circle-packing-subagents-9yg5gt`
- Lane: **upper bound / construction for $n = 16$** — reproduce and exactly certify the
  Melissen–Schuur record, or beat it. Independent of the killed lane
  [`../n16-upper/`](../n16-upper/); no code is shared with it.

## Normalisation, fixed here and re-derived from scratch

Separation 1, unit triangle, maximise the minimum pairwise distance $m$ of 16 points; then
$a = 1/m$ (covering-lane side), $d = 2/m$ (repo point-formulation side, separation 2), and
$s = 2/m + 2\sqrt3$ (side of the triangle holding the unit circles; certificates report $s$).
Re-derived targets (mpmath, 30 dps, from the closed forms in the problem README and
Graham–Lubachevsky's printed $d(16) = 0.216227269309782$):

| $n$ | target $m$ | $a = 1/m$ | $s$ |
|---|---|---|---|
| 12 | $2-\sqrt3 = 0.2679491924311227$ | $2+\sqrt3$ | $4+4\sqrt3 \approx 10.9282032$ |
| 13 | $0.2518132366530605$ | $3.9711971193$ | $\approx 11.4064958538$ |
| 15 | $1/4$ | $4$ | $8+2\sqrt3 \approx 11.4641016$ |
| 16 | $0.216227269309782$ (GL, 15 s.f.) | $4.6247635795064$ | $\le 12.7136287742$ |

## Validation gate (must pass before any n = 16 run)

The pipeline must reproduce the **`cited`** optima $m(12)$, $m(13)$, $m(15)$ each to within
$10^{-9}$ from pinned-seed multistart. If it cannot after code fixes within the budget, **stop:
the pipeline is broken and no n = 16 output from it is admissible.**

## Exact-gate control (must pass before any certificate is written)

The exact rational checker must **reject** a negative control: the certified configuration with
one coordinate perturbed so that one pairwise distance falls below 2 by $10^{-12}$ (and a second
control pushing one point outside the triangle by $10^{-12}$). If either control is *accepted*,
the gate is broken and nothing downstream is admissible.

## Record trigger (before writing anything that says "beat")

Any polished configuration with projected feasible $m > 0.216227269309782 + 10^{-9}$ triggers
problem `RULES.md` §4 in full: literature check (Graham–Lubachevsky, Friedman, Packomania — via
WebSearch, since WebFetch is blocked), error-bar check, fresh-seed reproduction, and the explicit
bug / misread-table / infeasible triage, **in that order**, before any claim is drafted. An
improvement of $\sim 10^{-7}$ is a bug until proven otherwise. Until all steps pass, the word
used is "candidate", never "record".

## K1 — budget kill

Stop and write up whatever is in hand when **any** of:

- 45 minutes total wall clock spent on search + polish (checkpointed to disk, 1 core);
- $\ge 3000$ local solves at $n = 16$ across the seed families (`uniform`,
  `lattice_defect` = $T(6)$ minus 5, `t5_plus_one`, `perturb_best`) without the record trigger
  firing **and** with best $m \ge$ target $- 10^{-9}$ (reproduction achieved → proceed to
  exactification, which is the deliverable);
- best $m <$ target $- 10^{-6}$ after the full solve budget → **reproduction failed**; report
  the miss honestly as a pipeline limitation, with per-family solve counts. Do not extend the
  budget silently.

## K2 — exactification kill

If the rational rounding cannot be made exactly feasible at any $s < 12.71362878$ (i.e. within
$10^{-8}$ of the float value) after 3 attempts at increasing denominator precision, report the
certificate at the best exactly-feasible $s$ achieved and say plainly how far it is from the
record. A slightly-loose exact certificate is an honest upper bound; a tight-looking float is
nothing.

## What this attack may never conclude

- **No optimality claim, ever.** This lane is a construction; an upper bound cannot certify a
  lower bound, and nothing here may be fed into any lower-bound argument. If the searches all
  plateau at the record value, that is `numerical` evidence and stays so permanently
  (problem `RULES.md` §1).
- Nothing enters `results/` from this lane; the certificate lives in this attack directory at
  status `numerical` until an independent checker (other family) examines it.
- Rattlers are reported, not "fixed" (problem `RULES.md` §5).
