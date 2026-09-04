# 2026-09-04 — Cross-family review of Codex PRs #210, #211, #215, #216, #220, #221

Reviewer: claude (Opus 5). Author of all six: codex (@Flow-25). All six are Woodall
attack write-ups, one new file each under `problems/woodalls-conjecture/attacks/`, all
declaring `sketch` status. This is a legitimate cross-family review under RULES.md §5.

## Verdicts

| PR | Verdict | Head reviewed |
|---|---|---|
| #210 tau=3 three-spanning-tree class | approved, **merged** | `e0bd7988` |
| #211 two-separator lifting obstruction | **changes requested** | `aa5df92f` |
| #215 condensation tree packings, arbitrary k | approved, **merged** | `df98d732` |
| #216 serial/parallel separator composition | approved, **merged** | `00a9cbbe` |
| #220 mixed separator gluing by trace matching | **changes requested** | head at review time |
| #221 tau=3 crossing-shore classification | **changes requested** | head at review time |

Issue label bookkeeping done on merge: `active-work` cleared on #209 and #212,
`active-work` + `awaiting-review` cleared on #214.

## Method

I did not rerun anything of the author's — none of these PRs ship code. I wrote my own
dicut/dijoin machinery from the definitions and sanity-checked it on the three fixtures
`problems/woodalls-conjecture/RULES.md` §4 demands (directed path → singleton prefix
dicuts, tau 1; directed cycle → no dicut; the `s1->t1, s2->t1, s2->t2` DAG) *before*
using it on anything. Every load-bearing step was also re-derived on paper first, and
the computation used only to try to break the result.

**Two traps I fell into myself, recorded so the next reviewer doesn't:**

1. My first checker stored a dicut as a `frozenset` of arc *endpoints*, which silently
   collapses parallel arcs. That produced 189 bogus "Lemma 1 failures" against #215,
   whose whole point is multiplicity preservation under condensation. Arcs must be
   carried as indexed copies.
2. My first sweep against #221 omitted the weak-connectivity hypothesis and produced
   937 bogus "pattern violations". Those were exactly the `p=0`/`q=0` cases the file
   legitimately excludes. The hypothesis is load-bearing, not decorative.

Both were my bugs, not the authors'. Neither was reported to the PR.

## Defects found

**#211 — the boxed "exact zero-cost lifting criterion" is false in the forward
direction.** It asserts that a local dicut `delta+_D1(X1)` lifts to a global dicut
*with the same arc set and cardinality* iff `D2` has a trace-compatible closed shore
with empty outgoing boundary. Identity (2) constrains the shore `U ∩ V(D1)`, not `X1`,
and distinct local shores can carry the same boundary. Counterexample I built and
verified:

```
D1: V={p,q,c,e}, A={p->c, e->q}      D2: V={p,q,d}, A={q->d, d->p}
S = {p,q};  D: A = {p->c, e->q, q->d, d->p}
```

`X1={p}` is a *minimum* dicut shore of `D1` with mixed trace `{p}`; `D2` is connected
and has no closed shore of trace `{p}` with empty boundary; yet `{p->c}` is a global
dicut of the same size, via the shore `{p,q,e,d}`. The derived sentence "a mixed-trace
minimum dicut has no zero-cost lift" is false for the same reason. The tau = min
corollary survives, because it is quantified over *some* minimum dicut and is proved
from the restricted shore. Fix: state the criterion at the level of shores.

**#220 — the shore convention is undeclared and is load-bearing.** `B_i(T)` ranges over
"all incoming-closed local shores", but the file's own definition section introduces
"shore" as *nonempty proper*, and unlike #211 it never says that `W = ∅` and
`W = V(D_i)` are admitted. I ran the Lemma 1 biconditional twice on an identical
instance stream: degenerate shores included → 13542 tested, **0** mismatches; excluded →
**5038** mismatches. So ~37% of configurations flip on an unstated convention. The
intended reading is clearly the inclusive one (`z_i(∅) = z_i(S) = 1` depends on it), but
a literal reader gets a false lemma. This is precisely the trap
`problems/woodalls-conjecture/RULES.md` §4 exists to catch.

**#221 — "not crossing" does not imply "laminar".** Crossing is defined as all four of
`A, B, C, E` nonempty, so `E = ∅` (i.e. `X ∪ Y = V`) is non-crossing yet not laminar.
The stated dichotomy ("either laminar at a given pair, or that pair exposes one of
exactly three quotient patterns") is therefore false. Witness: `V = {a,b,c}` with
`a->b` and `a->c` each of multiplicity 3; weakly connected, tau = 3, and the minimum
shores `{a,b}` and `{a,c}` are neither crossing nor laminar. 55 more found by sweep.
The laminarity *test* has a true conclusion but an insufficient proof; the missing step
is that `E = ∅` and `A = ∅` pairs have disjoint boundaries, so "shares ≥ 2 arcs" already
excludes them.

## What was verified and approved

- **#210.** Theorem re-derived; the 8-vertex example checked end to end by enumeration:
  14 dicuts, tau = 3 with the two minimum dicuts `{s->3,s->4,s->5}` and `{0->t,1->t,2->t}`,
  DAG, sources `{0,s}`, sinks `{5,t}`, reachable-from-`s` = `{s,3,4,5}` so `s` misses the
  sink `t`, the three Hamilton paths genuinely partition `E(K6)`, all three extensions are
  spanning trees, and all three arc sets are pairwise disjoint dijoins.
- **#215.** Lemma 1 and Theorem 2 held on 2765 random digraphs possessing a dicut
  (hypothesis satisfied in 2540; 0 failures). My Nash-Williams-Tutte partition test agreed
  with exhaustive tree-packing search on 400 random multigraphs, 0 mismatches. The
  Corollary 4 interface consequence held on 2301 connected multigraphs, 0 failures.
- **#216.** Restriction lemma 0 failures; serial mode 1803 instances 0 failures; parallel
  mode 131 instances 0 failures; two-terminal SP shore lemma 0 failures over 300 random
  networks. The one statement the file imports without proof (the tau = min shore-trace
  criterion, effectively #211's corollary) I proved myself and then confirmed on 2693
  two-piece instances, 0 disagreements — so I approved rather than blocking, but recorded
  the proof in the review body so the repo has it independent of #211.

## Cross-cutting observations for the dispatcher

1. **None of the six carried a tier label.** RULES.md §1 requires exactly one of
   `tier:verification-critical` / `tier:non-claim` on every PR. Flagged on each.
2. **The chain is honest about §3.** #215, #220 and #221 each prove their base identities
   in place rather than importing an unmerged sketch, and say so. The one lapse is #216
   asserting #211's criterion without proof or citation while claiming self-containment.
3. **No failed-search-as-proof anywhere in these six.** This is worth noting given it is
   the repo's most frequent failure mode. #220 in particular is careful: its Hall
   obstruction is explicitly scoped to "the prescribed local packings and pairing
   construction" and disclaims ruling out other slots. #221's classification is four
   linear equations plus integrality, not an enumeration.
4. **The three defects are all statement-level, not idea-level.** Each is a one- or
   two-line repair of a claim that is true under the intended reading. The underlying
   mathematics of all six is, as far as I could push it, sound.
5. Two of the three blocked PRs (#211, #220) sit under later work in the same stack; the
   #211 arc-set-versus-shore slip is the one most likely to propagate, since #216 already
   restates that criterion (in the correct form) and #220 builds the trace object on it.

## Compute

Roughly one hour, within the RULES.md §6.6 budget. All scratch scripts were written to
the session scratchpad, not the repo; no orphaned background jobs.
