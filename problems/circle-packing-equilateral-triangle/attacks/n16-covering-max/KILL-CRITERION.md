# Kill-criteria — n16-covering-max (worker C5, 2026-08-22)

Fixed **before** any computation. The question of this lane: is $A_{15} = 1+2\sqrt3$ exactly,
where $A_{15} = \sup\{a : T_a \text{ is covered by 15 sets of diameter} < 1\}$?

Two directions are attempted; each has its own kill switch.

## Direction B — a structural upper bound on $A_{15}$

The plan, fixed now: (i) re-derive the forced coarse structure (3 corner + 9 edge + 3 interior)
from first principles with corrected constants, for arbitrary sets (no convexity assumption);
(ii) feed the forced per-side edge count $k_e = 3$ and the interior count $n_I = 3$ into the
area budget with the closed-form slice bound
$g(\ell) = \pi/2 - \arcsin(\ell/2) - (\ell/2)\sqrt{1-\ell^2/4}$ for edge pieces, $\pi D^2/6$ for
corner pieces, $\pi/4$ for interior pieces; (iii) certify the resulting threshold $\beta$ by
exact rational arithmetic at a fixed rational $a^\*$.

- **K1 (no improvement).** If the certified $\beta \ge 4.914308$ (the existing Lemma-S ceiling
  U2 of `../n16-covering-limit/`), direction B has produced nothing and is reported as failed.
  **No post-hoc sharpening**: the ingredient list above (structure + $g$ + $\pi/6$ + $\pi/4$) is
  frozen now; I will not bolt on additional weight functions after seeing the numbers to rescue
  a disappointing $\beta$.
- **K2 (tripwire — bound below the certified record).** If at any point the argument yields
  $\beta \le 1+2\sqrt3 = 4.46410\ldots$, that contradicts the repo's exactly certified 15-piece
  covering and is a **bug in my argument**. The code must assert `beta > 4.4641016151` and fail
  loudly, never report such a $\beta$ as a result.
- **K3 (certification).** If the exact rational certification of $F(a^\*)>0$ fails at the chosen
  $a^\*$ (enclosures too wide, or the sign genuinely wrong), the reported bound moves up to the
  smallest rational $a^\*$ that does certify; if none below $4.914308$ certifies, K1 fires.

## Direction A — push a construction above $1+2\sqrt3$

Search representation: minimax vertex optimisation on explicit cell complexes (the record's
structure and mutations of it: extra corner chords, asymmetric perturbations, vertex insertions)
plus power-diagram multistarts for structural diversity. Test sides fixed now:
$a \in \{4.40\ (\text{control}),\ 4.47,\ 4.50\}$.

- **K4 (control first).** At $a = 4.40 < 1+2\sqrt3$ a strict covering exists (scaled record,
  max diam $= 4.40/(1+2\sqrt3) = 0.98564\ldots$). If the search machinery cannot find max diam
  $< 1$ at $4.40$, the machinery is broken and every negative result at $4.47/4.50$ is
  **uninformative**; report that and draw no conclusion from direction A.
- **K5 (budget).** Search wall-clock $\le 15$ minutes, single core; total compute this session
  $\le 45$ minutes. When the budget is spent, the best value found is reported as-is.
- **K6 (success handling).** If any run at $a \ge 4.4642$ reaches float max diam $< 1$: STOP the
  search, freeze coordinates, attempt exact rational verification. Only an exactly verified
  certificate is reported as a covering. A verified covering at $a \ge 4.62$ additionally trips
  repo `RULES.md` §7 (extraordinary-claim procedure); a verified covering in
  $(4.4641, 4.62)$ overturns "the lane is closed" and is flagged prominently but is not
  extraordinary.

## Global guards

- **K7 (circularity).** No value of $a_{16}$, $d(16)$, $s(16)$, and no coordinate of the
  best-known 16-point packing, is an input to any bound. The number $4.6247636$ appears only as
  a comparison target, held in a named constant `COMPARISON_ONLY_packing_target`. The forced
  structure and the area budget use only: the isodiametric inequality (`cited`), and elementary
  geometry derived in the file.
- **K8 (no re-scoping).** If both directions end with "structure forced, $\beta \approx 4.8$,
  no construction above $1+2\sqrt3$", the honest deliverable is exactly that — the question
  "$A_{15} = 1+2\sqrt3$?" is reported as **open**, with the interval narrowed. I will not
  re-scope into packing search or piece-budget $\ne 15$ to manufacture a positive.
