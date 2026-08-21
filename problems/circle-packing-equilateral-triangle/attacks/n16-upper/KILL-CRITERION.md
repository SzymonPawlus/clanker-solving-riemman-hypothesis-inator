# Kill-criterion — attack `n16-upper`

Written **before** any optimiser was run, per repo [`RULES.md`](../../../../RULES.md) §6.2 and the
compute-budget guidance in §6. Committed as-is; if the attack survives, it survives against this
text and not against a rewritten one.

- Author: `claude` (Claude Opus 5), worker N4, 2026-08-22
- Branch: `claude/circle-equklatetal-problem-sa7tx7`
- Target: the **upper bound** for $n = 16$. Best known is Melissen–Schuur (1995),
  $d(16) = 0.216227269309782$ (Graham–Lubachevsky's tabulated 15 s.f. value, via
  [`experiments/circle-packing-search/reference.py`](../../../../experiments/circle-packing-search/reference.py)),
  i.e. side $a_{16} \le 4.6247635795\ldots$ at separation 1 and $s(16) \le 12.7136292\ldots$.

## Normalisation, fixed here

Separation 1, side $a$; the optimiser works in the **unit** triangle and maximises the minimum
pairwise distance $m$, so $a = 1/m$. Graham–Lubachevsky's $d(n)$ **is** $m(n)$ in this
normalisation. The repo's certificates use separation 2, side $d = 2a$, and $s = d + 2\sqrt3$.
Every number in this attack is stated in the $(a, m)$ separation-1 normalisation unless the word
$s$ or $d$ appears. `normalisation.py` asserts the round-trip in code.

## Abort-and-exactify trigger

$d(16)$ is known to this project only as a 15-significant-figure decimal. Round-to-nearest at that
precision gives $d(16) \le D_{\mathrm{hi}} = 0.2162272693097825$. **Any** local solve returning a
projected-into-the-triangle minimum distance $m > D_{\mathrm{hi}} + 10^{-9}$ stops the search
immediately, and the configuration goes through the exact rational gate (both checkers) before
anything else happens — including before it is written into a summary line.

## K1 — budget kill (stop and report a null)

Stop and write up the quantitative null if **all** of the following have been spent without the
trigger firing:

1. $\ge 100{,}000$ local SLSQP solves at $n = 16$, spread over **all** seed families listed below
   with at least 5,000 solves in each;
2. the structural stage complete: the $T(5)$ lattice plus one point at every distinguishable
   insertion site, each relaxed;
3. the symmetry stage complete: $C_3$ and mirror ansätze solved in reduced coordinates;
4. the feasibility stage complete: $\ge 20{,}000$ fixed-side feasibility attempts at
   $a$ strictly below $1/D_{\mathrm{hi}}$;
5. LS billiard run as an independent generator, $\ge 2{,}000$ jammed configurations.

Seed families: `uniform`, `lattice_defect` ($T(6)$ choose 16), `t5_plus_one`, `rotated_lattice`,
`rows`, `symmetric`, `perturb_known`, `ls`.

## K2 — structural kill (a *stronger* claim, and I expect not to earn it)

K2 would be: the margin ladder shows a **clean gap** below $d(16)$ — no local optimum in
$(d(16) - \varepsilon_0,\ d(16))$ for some $\varepsilon_0$ resolvably larger than solver noise —
so that the Melissen–Schuur basin is isolated in the sampled landscape. Yesterday's hunt did not
earn its K2 and said so; if the values here trail off continuously I will say the same. **K2 not
met is the expected outcome and must be reported as such, not quietly dropped.**

## What would make me abandon the attack early

- The pipeline fails to reproduce $d(16)$ to $\ge 12$ significant digits from a fresh seed. Then
  the search is broken and no null from it is worth anything; fix or stop.
- The negative control (a configuration shrunk by $10^{-12}$) is *accepted* by either exact
  checker. Then the gate is broken and nothing downstream is admissible.
- Wall-clock exceeds the one-hour unattended budget of `RULES.md` §6.6. Report partial coverage
  with exact solve counts per family; do not extend silently.

## What this attack may never conclude

- No optimality claim of any kind. Failing to beat $d(16)$ is **not** evidence that $d(16)$ is
  optimal beyond the `numerical` level, and the coverage section of the write-up must state which
  regions were not visited.
- Nothing here enters `results/`, and nothing here is assumable — including by me.
- If the trigger *does* fire and both checkers agree, the output is a **candidate needing the
  `RULES.md` §7 procedure**, reported to the manager as such. Not a result, not a headline.
