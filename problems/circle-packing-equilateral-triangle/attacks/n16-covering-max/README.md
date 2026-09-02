# Attack: is $A_{15} = 1 + 2\sqrt3$? — **cut off mid-run, no verdict**

**Claim type: NEITHER of the two in problem [`../../RULES.md`](../../RULES.md) §1.** Nothing here
bounds $s(16)$ or $a_{16}$ in either direction. The quantity this lane was opened on is

$$A_{15} \ :=\ \sup\{\,a > 0 \ :\ T_a \text{ is covered by 15 sets of diameter} < 1\,\},$$

the resource the covering route consumes. An upper bound on $A_{15}$ bounds the *method*, not the
problem; a construction above $1+2\sqrt3$ would bound the problem. **Neither was obtained.**

- Worker: `claude` **C5** (Fable 5), 2026-08-22, branch `claude/circle-packing-subagents-9yg5gt`,
  issue [#97](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/97)
- **Terminated by a session API limit** after fixing its kill-criteria and writing two scripts,
  before running either and before any write-up. This file is the **manager's** record of the
  partial state, per repo [`RULES.md`](../../../../RULES.md) §6 ("report partial results — silence
  is not"), following the precedent of [`../n16-covering/`](../n16-covering/), whose worker was
  lost the same way.
- Kill-criteria, fixed by C5 before computing and reproduced unaltered:
  [`KILL-CRITERION.md`](./KILL-CRITERION.md)
- Code as C5 left it: [`experiments/packing-n16-covermax/`](../../../../experiments/packing-n16-covermax/)

## Status of everything in this directory

| item | status |
|---|---|
| `KILL-CRITERION.md` | C5's, written before computing, **unmodified** |
| `search_above.py` (direction A, float search) | code only; run once by the manager, output below |
| `certify_beta.py` (direction B, exact certification of a structural ceiling) | **code only, never run — and it should not be run as written**, see §3 |
| every number below | `numerical`, float search, decides nothing (problem `RULES.md` §5) |

Nothing here is assumable by anyone, including the manager (`RULES.md` §3).

## 1. What the lane was asked

The standing record is $a_{16}\ge 1+2\sqrt3$ from a 15-piece covering
([`../n16-covering-2/`](../n16-covering-2/)). Three independent search methods land on exactly that
value and its flip-neighbourhood is far worse, but the *method's* proved ceiling is only
$A_{15}\le 4.914308$ ([`../n16-covering-limit/`](../n16-covering-limit/)). So the campaign does not
know whether the lane is closed or merely hard — which is what decides where the next several
worker-days go. C5 was asked to settle it in either direction.

## 2. Direction A — the one run that happened, and the symptom in it

The manager ran `search_above.py` once, unmodified, with C5's pinned seed (`20260822`). It is a
float minimax descent on the record's cell complex — face combinatorics fixed, boundary vertices
sliding along their sides, corners pinned, with jittered asymmetric restarts.

```
a=4.40: baseline maxdiam^2=0.971487483 (scaled record 0.971487483), best after  6 descents: 0.971487483
a=4.47: baseline maxdiam^2=1.002644331 (scaled record 1.002644331), best after 18 descents: 1.002644331
a=4.50: baseline maxdiam^2=1.016147807 (scaled record 1.016147807), best after 18 descents: 1.016147807
```

Read literally: no covering above the record was found, and K4's control direction passes in the
weak sense that $\max\mathrm{diam} = 0.98564 < 1$ at $a = 4.40$.

**But that reading is not available, and the reason is the finding.** At all three side lengths the
best of every restart equals the baseline **to all nine printed digits**. The baseline is just the
record rescaled by $a/a_0$. So either every jittered restart returned to the identical
configuration, or `descend` is returning its input — and the run does not distinguish those. A
descent that never improves on its own starting point at *any* input is the signature of a no-op,
and C5 was killed before it could look at this output.

**Consequence: this is not a negative result.** A search that cannot be shown to search does not
license "no covering above $1+2\sqrt3$ exists on this structure". The honest statement is that
direction A produced **no evidence in either direction**, and that the first job of whoever picks
this lane up is to instrument `descend` and confirm it moves before any of its verdicts are used.
The K4 control was written to catch a broken optimiser and is, in retrospect, too weak to do so: it
checks that the machinery reports $<1$ at $a = 4.40$, which the *unmodified baseline* already
satisfies. A control that a broken optimiser passes is not a control.

## 3. Direction B — why `certify_beta.py` was left unrun

C5's plan (see `KILL-CRITERION.md`) was to derive a structural ceiling on $A_{15}$ from the "forced
coarse structure" of [`../n16-covering-2/`](../n16-covering-2/) §"Why this is where the family
stops", finding 1 — that a 15-piece covering must be 3 corner + 9 edge + 3 interior — and feed the
forced counts into an area budget.

**That input is now disputed by two independent audits, both delivered while C5 was running:**

- [`../n16-verification-3/`](../n16-verification-3/) (worker V3): the case split over $n_2$, the
  number of pieces meeting two sides, is **not exhaustive** — $n_2 = 4$ and $n_2 = 5$ satisfy every
  inequality the derivation produces and are never addressed.
- [`../n16-redteam/`](../n16-redteam/) (worker R1): the failure is **earlier**. R1 exhibits a piece
  meeting two sides that still reaches into the middle of one of them, which is what the $n_1\ge9$
  count assumes cannot happen. Witness: $P = (21/20,\,0)$ on $AB$ and $Q = (1/4,\,\sqrt3/4)$ on
  $AC$, with $|PQ|^2 = 331/400 < 1$, while $P$ lies at distance $1.05 > 1$ from $A$ and
  $3.414\ldots > 1$ from $B$, i.e. in the middle $m_{AB}$. The manager re-derived this exactly and
  it holds; the same pair also passes the footpoint test $\alpha^2+\beta^2-\alpha\beta = 331/400 < 1$
  that §1 uses to confine two-side pieces to a corner.

R1 further reports that V3's write-up explicitly certifies as correct the sub-step R1 breaks. **The
two audits agree the conclusion is unproved and disagree about which step fails.** Problem
`RULES.md` §3 is explicit that a disagreement between checkers is a finding to investigate, not to
average, and it is **unresolved as of this file**.

So `certify_beta.py` would compute a ceiling conditional on a premise two auditors have flagged and
neither has repaired to the other's satisfaction. Running it would produce a number that reads like
a theorem and is conditional on a disputed claim — the exact shape of error `RULES.md` §0 exists to
catch. It was left unrun deliberately, and that is a decision, not an omission.

R1 also offers a **repair** — count corner-containing pieces out of the middles instead, giving
$n_1 + n_2 \ge 12$ and hence $n_{\mathrm{int}} \le 3$ unconditionally, with 33 layouts surviving
rather than one. If that repair holds, direction B becomes a 33-case exhaustion rather than a
1-case one: still finite, still worth doing, and **not** what `certify_beta.py` currently computes.

## 4. What to review hardest

1. **The `descend` no-op question** (§2). Everything direction A could ever say depends on it, and
   it is one instrumentation run to settle.
2. **The V3/R1 disagreement** (§3). Both audits are `sketch` and same-family; the sub-step is a
   short, exactly checkable piece of plane geometry, so it should be decidable outright.
3. **R1's repair**, before anyone builds on it.

## 5. Reproduce

```bash
python3 experiments/packing-n16-covermax/search_above.py    # ~2 min, seed pinned at 20260822
```

`certify_beta.py` is present but **must not be run for a result** until §3 is resolved.

## 6. Kill-criterion outcomes

- **K1 (direction B no-improvement):** did not fire and **could not** — direction B never ran.
- **K2 (tripwire below the certified record):** did not fire; nothing was certified.
- **K3 (certification):** not reached.
- **K4 (direction A control):** nominally passed, and §2 argues the control is too weak to mean
  what it was written to mean.

No kill-criterion was restated, weakened, or re-scoped. The lane is **open**, not refuted.
