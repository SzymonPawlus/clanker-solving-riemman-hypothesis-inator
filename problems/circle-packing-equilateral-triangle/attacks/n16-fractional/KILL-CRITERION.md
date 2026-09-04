# Kill-criteria — fractional covering relaxation for $n=16$

Fixed **before** any computation (worker F2, `claude`, 2026-08-22, issue #97). The lane: replace
the integral 15-piece covering pigeonhole by its LP relaxation — weighted, overlapping pieces of
diameter strictly $<1$ whose total incident weight is $\ge 1$ everywhere on $T_a$ and whose total
weight is $< 16$ — which excludes 16 separated points and so proves $a_{16}\ge a$.

All arithmetic that decides anything: exact integers/`Fraction`s. Grid unit $1/64$ of the
separation distance; pieces of diameter $\le 63$ units $=63/64$; a certificate at side $N$ units
dilates to the bound $a_{16}\ge N/63$ (limit argument as in `n16-covering-2`).

## K1 — controls (soundness *and* power), before the open case is touched

Run the identical pipeline with budget $n$ on the three known values $a_4=\sqrt3$, $a_6=2$,
$a_{10}=3$.

- **Soundness (fatal):** the pipeline must never produce a verified certificate at
  $N > \lfloor 63\,a_n\rfloor$, i.e. never certify $N \ge 110$ for $n=4$, $N \ge 127$ for
  $n=6$, $N \ge 190$ for $n=10$. One such certificate = a bug in the verifier; the lane stops
  and reports the bug, not a bound.
- **Power (abandonment):** the pipeline must certify at least $N = \lfloor 63\,a_n\rfloor - 3$
  in each control ($\ge 106$, $\ge 123$, $\ge 186$). Cell granularity is expected to cost 1–2
  units; if it cannot get within 3 units of a *known* answer, it has no business reporting
  anything about an open one — abandon and write the negative up.

## K2 — no gain over the standing record

The standing record is $a_{16}\ge 1+2\sqrt3 = 4.4641\ldots$, i.e. $N/63 > 1+2\sqrt3$ requires
$N \ge 282$. If, within the compute budget, the best exactly-verified certificate for $n=16$ is
$N \le 281$ ($a \le 4.4603 < 1+2\sqrt3$), the fractional relaxation (as implemented, with this
family and grid) **has not beaten the integral method**: report the LP-value-vs-$N$ table as a
negative result and stop. No re-scoping to "but a richer family would…" — that is a new issue,
not this one.

## K3 — §7 tripwire

If any verified certificate implies $a_{16}\ge 4.62$, **stop immediately**: do not extend the
search, treat it as a probable input error (the repo has a documented near-miss of exactly this
shape), re-check the circularity guard and the verifier on the controls, and flag the possible
extraordinary claim per repo `RULES.md` §7 in the report. Note $288/63 = 4.5714$,
$291/63 = 4.6190$, $292/63 = 4.6349 > 4.6248$ (best known packing): a verified $N \ge 292$ is
*necessarily* a bug, since the sandwich $\omega \le \tau_f$ makes the method incapable of
certifying past the true $a_{16}$, and a 16-point packing at $4.6247637$ is believed to exist.

## K4 — budget

$\le 45$ min wall clock of computation, $\le 1$ core for anything long. Checkpoint every LP
result to `experiments/packing-n16-fractional/certs/` as it completes. When the budget is spent,
the best *verified* $N$ is the result, whatever the LP hints more might be possible.

---

## Addendum (worker F3, 2026-08-23) — family-adequacy gate, fixed before computing

F2's K1 controls tested small $n$ on families that happened to contain the obvious lattice
subdivision; they never tested whether the $n=16$ family contains *any* 15-piece cover. The
manager's post-mortem shows it does not: at $N=281$ the ratio $281/63 = 4.4603 < 1+2\sqrt3$, so a
15-piece cover exists in the continuum, yet the LP on F2's family needs $17.67$. The criteria
below are fixed before any new computation; K1–K4 above stand unchanged.

- **A1 — adequacy gate (blocking).** Seed the family with grid-rationalised pieces of the
  record's own 15-piece cover ([`../n16-covering-2/`](../n16-covering-2/)), plus small lattice
  translates of them (translation preserves diameter), clipped to $T_N$. At $N = 281$ the LP
  value must come out $\le 15.1$ (target $15.0$; up to $0.1$ allowed for residual cell
  granularity). If it does not, the family is still inadequate: **no sweep result at any $N$ may
  be reported as evidence about $A_{16}^{\mathrm{frac}}$**, and the write-up must say the lane
  remains untested.
- **A2 — what counts as an answer at $N \ge 282$.** Only after A1 passes. For each $N \ge 282$
  the LP row is `numerical`; a claim $a_{16} \ge N/\sqrt{q_{\max}}$ requires the exact
  `Fraction` re-verification *and* an independent pass of
  `experiments/packing-n16-fracverify/fracverify.py` (not modified by me). A verified $N \ge
  282$ beats the record and must be flagged prominently, not just tabulated; K3 still caps
  everything at $4.62$.
- **A3 — seed provenance / circularity.** The seed is the record's 15-piece *covering*
  (`sketch`, [`../n16-covering-2/`](../n16-covering-2/)) — an input to the *family*, not to the
  bound: Lemma F + the exact verifier alone produce the bound, and a wrong or misremembered seed
  can only make the LP value *worse* (higher), never certify anything false. No number derived
  from any 16-point packing is an input; `EXCLUDE_POINTS = 16` remains the only $n=16$-specific
  constant.
- **A4 — budget for this round.** $\le 45$ min wall clock, $\le 1$ core, checkpoints to
  `certs/` as in K4; background jobs killed before the session ends.
