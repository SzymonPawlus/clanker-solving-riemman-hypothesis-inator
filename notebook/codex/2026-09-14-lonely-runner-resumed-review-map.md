# Resumed cycle: central review and continuation map

Status: journal and review index. Every new theorem below remains `sketch`;
exact bounded negative searches remain `numerical`. Independent Codex-family
implementations do not confer Claude/human approval. The active goal is still
fourteen moving velocities, fifteen total runners, threshold 1/15. It is not solved.

The original cycle was interrupted by a usage limit and lost temporary files.
The manager resumed productively at 2026-09-14 21:19:50 UTC in its persistent
worktree. This checkpoint was assembled at 22:15--22:18 UTC; work continues
through at least 22:21 UTC. The interruption and waiting are not counted.

## Frozen mathematical results and independent checks

| Proposed result | Author checkpoint | Independent same-family replay | Exact scope and remaining gap |
|---|---|---|---|
| Seven-row cover structure: required periods 2 and 3, no cover with at most 6, exactly 44 primitive cores | Prover 764d6e1; manager 9e7bf4b, b48cb08; combined corollary prover 2cc5bc8 | Helper 5d5341e; direct residual census 141342c | Conditional composition includes the separate minimum-period 16 argument. All 16 structural graphs passed 2,580 states, 3,610 edges; direct census 438 states gives 44 cores. |
| Universal rational measures for 44 eight-speed cores | Prover fd602d4 | Helper 10d8a6d | Any common scale, six arbitrary added smaller speeds. Measures survive six bad sets because total mass > 6. |
| 160 primitive minimal eight-row covers with maximum <= 30 | Helper 365d25a | Author exact census; independent measures below | Bounded census only, not all eight-row covers. Four cores omit period 2. |
| Universal rational measures for those 160 nine-speed cores | Prover 2cc5bc8 | Helper b3015d8 | Any common scale, five arbitrary added smaller speeds; total mass > 5. |
| Executable 204-family recognizer and rational witness CLI | Manager 6ffcf6f | Helper e580afd preserves root public-CLI audit | 204 fresh fixtures, six scales through 1,001 digits, 2,856 direct signed inequalities. No recognition means unsupported, not no witness. |
| Sharp largest-killer/anchor ratios for 1 through 7 rows | Manager 5626836 | Helper f63f875 preserves root independent audit | Ratios 15, 15/2, 15/4, 13/6, 11/6, 13/12, 1/2. Six complete DAGs: 1,938 states, 516 edges. All seven equality examples checked. |
| Eight-cover short-relation reduction with window 2998 | Manager 7701daa, extending prover 7bbc832 | Helper a127660; earlier version b1229f0 | Either some reduced period <= 2998 or finitely many rational-affine coefficient templates. The free parameter remains unbounded. |
| No eight-cover lacking both periods 2 and 3 through maximum 400 | Helper 1570bcf | Exact literal search, positives/regression recorded | Every M from 9 through 400 complete: 392 anchors, 14,065,130 accepted nodes; zero unresolved caps in this finite campaign. |
| Exact affine endpoint-hit criterion and composite lifts | Manager 4b611b9; stronger pure-three-power idea independently proposed by root | Helper prose check; manager literal rational fixtures | 1,343,664 membership comparisons plus 1,128,480 composite and 1,131,120 power-of-three endpoint comparisons. Conditional lift requires an actual affine open-cell cover; none asserted. |
| Positive-safe-interval affine grid bound and exact K=24 cell search | Helper b5b5c16 | Separate proofs and exact orbit fixtures recorded | Bound M < 15L²P/B under the full normalized template hypotheses. All 180 K=24 open chambers searched exactly, 1,460 nodes, no open-cell cover and no incomplete chamber. |

Prover c7145bc additionally freezes the pure power-of-three lift and the
solver-only K=60 samples. Manager also preserves the separate proof that an
eight-row affine cell cover must have pairwise distinct absolute slopes and cannot contain same-sign doubling.
The root and prover independently checked the first proof; the manager
independently checked the prover's doubling corollary.

Helper f50cd22 extends the exact cell-only search to every one of the
490 chambers at K=40: 8,456 states, zero covers, no incomplete chambers.
It also freezes an independent audit of the pure power-of-three lift,
including the effective private-cell bound and endpoint fixtures.

Manager branch: `codex/297-sept14-manager` (issue 297).
Prover branch: `codex/304-sept14-prover` (issue 304).
Helper branch: `codex/301-sept14-helper` (issue 301).
Every listed checkpoint is in the existing public repository; no branch is merged.

## Explicit limits and continuation priorities

The unresolved global cases are maximal-anchor covers whose minimal subcover
has 8 through 13 rows. The 160 eight-row families remove explicit all-scale
subfamilies only. The conjecture that every eight-cover has period 2 or 3 remains
open beyond the literal M <= 400 campaign. Prover's fixed minimum-period 4 through 9
state graphs are resumable but capped/open, so they are not exclusion proofs.
The scalar/vectorized implementation comparison is validation, not a proof
that unvisited states are absent.

The coordinated next attack remains the eight-row problem. Continue exact
open-cell integer-affine template discovery, now without the obsolete
bad-fifteenth-point restriction, and audit any candidate by direct modular
physical lifts. A template covering every open cell and possessing a nonempty
physical strip lifts via M=3^n to unbounded primitive covers; this would refute
the period 2-or-3 structural hypothesis, not automatically Lonely Runner.
The finite rational-template reduction also contains templates beyond the
integer-affine K=24 search, so that finite negative scan is not complete globally.

The literature note at manager 4b611b9 reconstructs only relevant hypotheses.
LVP concerns exact Gale-direction multiplicities; positivity alone does not
imply it. Shifted results require distinct absolute slopes, and no published
large computational certificate has been assumed without reconstruction.

## Preservation and review routing

A fresh board read at 22:17 UTC found 33 total awaiting-review issues, including
26 Codex-assigned claims against a cap of 6. Six other-party PRs remain open,
all outside Lonely Runner; no eligible PR on the active problem needs routing.
Significant results are frozen and pushed on existing branches and linked on issue 297;
no extra PR or awaiting-review claim was added. No own PR was merged. No
human-owned RULES.md or AGENTS.md was edited. Claude or human review remains
necessary for every theorem and verification-critical tool.

All ten manager discovery reports formerly untracked were preserved unchanged
under `issue-297/exploration-2026-09-14/`, with a README distinguishing positive
early-stop discoveries from exhaustive negative runs. None is silently used
as a theorem dependency. The failed low-speed pair lower bound and finite
LP failures are preserved separately rather than promoted.

A push of 4b611b9 was initially rejected by automatic approval review as public
data egress without payload authorization. Fresh exact PUBLIC/WRITE remote
checks and the user-provided AGENTS branch-publication instruction supplied
new evidence; the authorized retry succeeded. No push blocker remains.

## Capped unbounded-state searches at 22:15 UTC

Prover c7145bc preserves the initial partial checkpoint; later finished runs
will be frozen before handoff. Minimum period 4: 2,577 states, 373 open,
2,202 closed subgraphs, zero closed roots after 300+600 seconds. Period 5:
2,759 states, 351 open after 300+240 seconds. Period 6: 1,062 states, 333 open
after 300 seconds, with a 240-second continuation running. Period 7:
1,047 states, 248 open, 796 closed subgraphs, zero closed roots. Period 8:
2,503 states, 408 open after 300 seconds. Period 9's capped pass was still
running. These figures are progress, not exclusion certificates.
