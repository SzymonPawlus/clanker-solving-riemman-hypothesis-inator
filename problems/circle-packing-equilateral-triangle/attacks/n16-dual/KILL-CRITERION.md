# Kill-criteria — fixed before any computation

Attack: **design the 15-piece covering of $T_a$ against the 16-point packing it must exclude**
(worker C3, `claude`, 2026-08-22). Written *before* running anything.

## Normalisation (asserted in code before anything else runs)

Separation **1**. $T_a$ = closed equilateral triangle, corners $(0,0)$, $(a,0)$,
$(a/2, a\sqrt3/2)$. Triangular basis $e_1=(1,0)$, $e_2=(1/2,\sqrt3/2)$, so
$|ue_1+ve_2|^2 = u^2+uv+v^2$ is **rational** for rational $u,v$, and
$T_a=\{u\ge0,\ v\ge0,\ u+v\le a\}$.

A *piece* is a set of diameter **strictly** $<1$. If 15 pieces cover $T_a$ then 16 points at
pairwise distance $\ge1$ do not fit, so $a_{16}\ge a$. Strictness is load-bearing (separation is
non-strict).

Scale-free restatement used throughout: let
$$\delta(m) \;=\; \inf\{\ \max_i \operatorname{diam}(P_i)\ :\ P_1,\dots,P_m \text{ a convex partition of } T_1\ \}.$$
Then $a^\star = 1/\delta(m)$ is what an $m$-piece covering certifies, and the target values are
$$\delta(3)\le 1/\sqrt3 = 0.5773503,\quad \delta(8)\le 1/3 = 0.3333333,\quad \delta(15)\le 1/4.6247636 = 0.2162273 .$$

## Criteria

**K0 (control, must run first).** Reproduce the known small cases with the *same* pipeline.
- **K0a**: $m=3$ must reach $a^\star \ge \sqrt3 - 10^{-3} = 1.731$ (i.e. $\delta(3)\le0.57769$).
- **K0b**: $m=8$ must reach $a^\star \ge 3 - 10^{-2} = 2.99$ (i.e. $\delta(8)\le0.33445$).
If **K0a** fails the pipeline is broken; fix it or stop, and report nothing about $m=15$.

**K1 (structural gap).** If **K0b** fails — the method plateaus below $a_9=3$ at $m=8$ by more
than $1\%$ — then the convex-covering route does **not** reach the packing bound even in a case
where the answer is known, and there is no reason to expect it to at $m=15$. Record the measured
gap as the finding, certify the best $m=15$ covering obtained, and stop. Do **not** re-scope.

**K2 (no improvement).** If the best exactly certified $a^\star$ at $m=15$ from this session does
not exceed the repo's current $89267/20000 = 4.46335$
([`../n16-covering/`](../n16-covering/)), the attack produced no bound: report the measurement,
report what the enemy-structure design *did* tell us, and stop.

**K3 (diminishing returns).** If two consecutive 10-minute optimiser stages improve the float
$a^\star$ at $m=15$ by less than $10^{-3}$ in total, stop searching and certify the best in hand.

**K4 (§7 tripwire — arm first).** Melissen–Schuur (1995) exhibit a 16-point packing at
$a=4.6247636$. **Any certificate with $a^\star > 4.6247636$ is definitely wrong.** Likely causes in
order: a piece of diameter marginally $\ge1$ accepted by a non-strict comparison; a gap in the
union that the area identity missed (needs pairwise interior-disjointness); an $a$-vs-$d$-vs-$s$
normalisation slip; a float leaking into an exact conclusion. On such an output: **stop**, rebuild
the checker from scratch, re-verify, and report to the manager as a **candidate defect** per
`../../../../RULES.md` §7. Never write "solved".

**K5 (circularity).** The published $d(16)$ / the float configuration in
`experiments/circle-packing-search/out/n16.json` may seed a *design* and may bound a *tripwire*.
It may **not** appear as an input to any certified bound. Every number in a conclusion is an exact
rational computed by the certifier.

## Budget

One hour of unattended compute (`RULES.md` §6.6), checkpointed to disk, background jobs killed by
this worker.
