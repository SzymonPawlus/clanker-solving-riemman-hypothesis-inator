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
