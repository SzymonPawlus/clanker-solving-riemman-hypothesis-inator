# 2026-09-04 — Woodall: repairing dangling unmerged-PR references on `main`

Issue #266. Branch `claude/266-woodall-main-repair`. Editorial repair plus one real
dependency fix. **No status promoted; nothing under `results/` touched.**

## What I re-verified before touching anything

The task arrived as a list of findings from a read-only audit. Per the repo's own history of
corrections being as wrong as the bugs they fix, I re-checked each one rather than acting on the
report.

**PR states, via the GitHub API this session:**

| PR | State | Note |
|---|---|---|
| #211 | OPEN | "Woodall: isolate the exact two-separator lifting obstruction" |
| #239 | OPEN | "Pack every fixed-trace dicut family by max flow" |
| #246 | OPEN | "Characterize two-trace profile intersection at tau=3" |
| #249 | OPEN | "Jointly realize two-trace profiles from boundary cores" |
| #255 | OPEN | "Reduce comparable trace chains to capped interval linkages" |
| #157 | MERGED 2026-09-03 | merge commit `8ebfa6f` |

`git show --stat 8ebfa6f` confirms it added
`problems/woodalls-conjecture/attacks/lean-foundations-audit/{README.md,hypotheses.md}` from
branch `claude/151-lean-audit`. So the "not yet on `main`" clause in the problem README is
stale. (Strictly it was hedged — "when this was written" — so it was never *false*, only
misleading. I treated it as stale rather than as an error.)

**Greps re-run:** `separator` appears in three attack files and is defined in none;
`realizable` appears in two and is defined in neither. Both confirmed.

## Defect 1 — the one that mattered

`attacks/coreless-trace-uncrossing/README.md` closed its final section by invoking
"the empty-versus-both Hall inequalities from PR #246: `e_1 <= b_2, e_2 <= b_1`". #246 is open,
so under §3 the conclusion was capped at unmerged `sketch` material.

I was told to prefer marking it contingent unless I could genuinely prove the inequalities.
I could, so I did (option (a)) — but only in the narrow form the section actually needs.

The key is a splitting observation I derived myself. With global boundaries
`G_t = { B_1 u B_2 : B_1 in F_t^1, B_2 in F_t^2 }`, the two parts are chosen *independently*, so

> `T` misses some member of `G_t` iff `T n E_1` misses some member of `F_t^1` **and**
> `T n E_2` misses some member of `F_t^2`.

Negated: `T` covers `G_t` iff it covers `F_t^1` locally **or** covers `F_t^2` locally. Hence
`T` is a global transversal iff `P_1(T) u P_2(T) = {0,1}`. The inequalities then fall out in two
lines: if a slot's piece-1 profile is empty, that union forces its piece-2 profile to be `{0,1}`,
so the `e_1` slots inject into the `b_2` slots.

That is Lemma 3 in the file. I did **not** reproduce, restate, or claim #246's general theorem —
only the two-piece instance. #246 stays in the file as a pointer to the general form.

I also hand-checked the file's own inequality (5) (`e > b`), which the audit had flagged as
correct, and agree: `b <= 1` since two both-covers would need 6 elements in a 4-element ground
set; `b=1` leaves at most one element so the other two slots are empty-profile (`e >= 2`); `b=0`
with three nonempty profiles needs 6 elements, so `e >= 1`.

## Brute-force sanity check (not written into the file)

Before committing I exhaustively checked the finite claims in a throwaway script (scratchpad,
not committed — a `numerical` claim would need a reproducible script under `experiments/`, which
is outside my file ownership for this task):

- min transversal number of each family = 2; min set covering both = 3 — matches the file;
- (5) `e > b`: **0 violations** over all `4^4` assignments of the ground set to three disjoint
  slots plus "unused";
- three pairwise disjoint global transversals in the two-piece system: **0**, over all `4^8`
  assignments — the conclusion is true, not just derivable;
- 170 disjoint *pairs* do exist, so the obstruction really bites at three, not earlier;
- min global boundary size 4, min global transversal size 3 — matches "size four, in particular
  at least three".

The prose proof stands on its own; this was a check on me, not a substitute.

## Definitions added, and one I hedged

- **separator** — defined as the shared vertex set `S = V(D_1) n V(D_2)` of an arc-disjoint
  two-piece decomposition, which is the sense `serial-parallel-separator-composition` already
  uses ("arbitrary vertex intersection `S`"). I added the honest caveat that **no separating
  property is used**: every statement in either file holds for an arbitrary `S subseteq V`. That
  is a description of the existing arguments, not a new hypothesis.
- **trace** of a shore `X` = `X n S`; **realizable trace** = one attained by at least one
  incoming-closed shore, equivalently one whose fixed-trace family is nonempty so `mu(R)` is
  defined. That is exactly what `coreless` Theorem 2 uses.
- **slot**, **profile**, **nonempty profile** — defined in `coreless`, matching all three
  existing uses.

**Where I hedged rather than guessed.** In `capped-linkage`, `mu_t` is the minimum *nonempty*
boundary size, so realizability in my sense is slightly weaker than what `mu_t` being well
defined requires. I did not silently widen the definition to cover both: I stated the definition
the layer-ordering argument uses, and noted separately that `mu_t` additionally presumes a shore
of that trace with nonempty outgoing boundary. A reviewer may prefer a single stronger
definition; I would rather flag the seam than paper over it.

## Defect 3 re-check

I read `capped-linkage` Theorem 1 through before asserting it is independent of #255. Its
statement uses only the layers (1), depth data (2)–(3), and this file's reduced linkages; its
proof uses only the auxiliary transshipment network and integral max-flow/min-cut (`cited`,
Ford–Fulkerson 1956). The two #255 mentions are motivation and a forward pointer. Deleting both
would leave the theorem and the four-arc obstruction intact. Confirmed — a pointer, not a real
defect.

I did **not** re-verify Theorem 1's min-cut computation itself; that is the job of the pending
cross-review of the file, and the task only asked about the dependency.

## What I did not do

- No status promotion anywhere. `coreless` and `capped-linkage` remain `sketch`.
- `problems/woodalls-conjecture/results/` untouched (concurrent worker owns it).
- Did not delete the abstract-obstruction section — a documented dependency, now discharged, is
  the honest artifact.
