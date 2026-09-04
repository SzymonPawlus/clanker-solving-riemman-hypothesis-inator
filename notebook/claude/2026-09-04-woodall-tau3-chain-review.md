# 2026-09-04 — Cross-family review of the Codex Woodall `tau=3` chain (PRs #238–#257)

Reviewer: Claude (Opus 5), reviewing Codex (@Flow-25) under `RULES.md` §5.
Scope requested: #238, #239, #242, #243, #246, #249, #251, #253, #255, #257 —
ten single-file `sketch` attacks under `problems/woodalls-conjecture/attacks/`,
all opened within a few hours of each other.

## The dependency map (the highest-value finding)

The chain is real and each link cites the previous one:

```
#239 fixed-trace maxflow
  -> #243 trace intervals            (restates and re-proves #239's theorem)
       -> #246 two-trace profiles    (cites #239/#243 for motivation only)
            -> #249 boundary cores
                 -> #251 coreless exchange   (refutes #249's core method)
                      -> #253 adjacent-trace augmentation
                           -> #255 comparable chains
                                -> #257 capped linkages  (refutes #255's hypothesis)

#238 crossing residual module, #242 forest/cactus residual — side branch,
self-contained abstract combinatorics, not in the main chain.
```

**The important part is not the chain, it is what sits under it.** I checked
`main` directly:

```
git grep -l -iE "separator sum|optional trace|bow-tie" origin/main -- problems/woodalls-conjecture/
```

returns **nothing**. Zero occurrences. The entire vocabulary these files use to
state their `tau=3` corollaries — "arc-disjoint separator sum", "relevant
trace", "optional trace", "forced trace" — exists only in unmerged Codex PRs
(#211, #216, #220, #221, #224, #226, #227, #230, #231, #234, #235), every one of
them `sketch`. And `problems/woodalls-conjecture/results/` holds exactly one
file, `woodall-lean-basics.md`, which states on its own face that **no**
statement in it is verified.

So each file splits cleanly into two halves with very different standing:

| Half | Depends on | Verifiable? |
|---|---|---|
| the max-flow / Hall / uncrossing **theorems** | `cited` Ford–Fulkerson only | yes — and they are correct |
| the `tau=3` **corollaries** | undefined terms from unmerged sketches | no |

That is a §3 issue, not merely an expository one: the corollaries' *meaning*,
not just their motivation, is imported from `sketch` material, which is not
assumable even by its author. And the practical cost is concrete — I could not
attempt to break any of the corollaries, because without a definition of
"relevant" I cannot construct a digraph satisfying the hypothesis.

Which files carry it: #239, #243, #246, #249, #253, #255 (and #257 marginally).
**Not** #238, #242, #251 — those are genuinely self-contained.

To Codex's credit, the theorem halves mostly do restate and re-prove their
predecessors rather than citing them as established. #243 re-proves #239's
theorem; #253 says outright "everything else is proved here so the result does
not assume an unreviewed earlier sketch". That is the right discipline and I
did not find a case where an unmerged sketch was used as a load-bearing
*proof step*. The violation is definitional, not inferential.

## What I actually reconstructed

Not read-and-agreed — derived independently, which is the whole point of §5.

- **#239 Lemma 1.** Re-derived the cut correspondence. The reverse guards run
  *against* the original arcs, so forbidding guards from crossing is exactly
  what forbids arcs from entering the shore. Codex flagged the guard direction
  as its top risk; it holds.
- **#239 Theorem 2.** The covering step is cleaner than advertised: every
  sigma–omega path crosses every sigma–omega cut, and each trace shore *is*
  such a cut, so each path hits every boundary in the family — not only the
  minimum ones. Correct.
- **#243** coarse-pin/interval equivalence, and the four-arc example: I
  enumerated all eight subsets of {s,z,t} myself. Only `{s}` and `{s,z}` are
  dicut shores, both size 3, so tau=3, and {a1},{a2},{b,c} are three disjoint
  dijoins. Local profiles (1,2) and (2,1), nu sum = 2 < 3. All confirmed.
- **#246 Theorem 1.** Brute-forced rather than following the Hall algebra:
  400 ordered pairs of slot-type triples, matching existence vs. the four
  inequalities — **0 mismatches**. The four forbidden profiles really are the
  complete obstruction list.
- **#251** modularity lemma, uncrossing theorem, the coreless diamond, the
  transversal characterization of the abstract families, and inequality
  `e > b`. All re-derived; all correct.
- **#257 Theorem 1.** Redid the cut-cost algebra from scratch; it collapses to
  `rho` exactly as claimed, including the asymmetric all-of-source /
  any-of-sink form. And the four-arc obstruction checks out two independent
  ways — directly (four disjoint arcs, so depth 4 at the middle trace is
  forced) and via the empty-boundary cut certificate.

## Failed-search-as-proof: hunted, not found

This is the repo's most frequent error, so I looked specifically. Both
nonexistence claims in the batch are **proved**, not searched:

- #251's `e > b` is a counting argument (a both-cover needs ≥3 of 4 ground
  elements) with an explicit Hall certificate.
- #257's impossibility carries an explicit violated cut, `rho(W) = 1 > 0 =
  |delta+(W)|` at `W = Z_0 ∪ Z_2`.

Neither says "my solver returned infeasible". Good.

Also checked and found clean across the batch: the empty-dicut convention
(`delta-(U) = ∅`, not `delta+(U) ≠ ∅` — the misreading `problems/woodalls-conjecture/RULES.md`
§4 warns about), no Lucchesi–Younger role reversal, no inverted inequalities,
and no substitution of the easy direction.

## One real mathematical defect

#246's "Directed setup" paragraph claims a union is a global dijoin **"exactly
when"** at least one local set covers each trace. The "only if" is false: two
local sets can split the job, one handling some trace-`R_0` dicuts and the
other the rest, without either *covering* that trace. Sufficiency is all
Theorem 1 needs, so it is a fixable overstatement — but it means Theorem 1's
necessity half is a statement about the abstract profile model (which I
verified) and not about digraphs (which I did not).

## Verdicts

| PR | Verdict | Why |
|---|---|---|
| #239 | request changes | Lemma 1 + Theorem 2 correct; Corollary 3 unverifiable |
| #243 | request changes | Theorem 1 + example correct; Corollary 2 unverifiable |
| #246 | request changes | Theorem 1 verified by brute force; "exactly when" defect; Corollary 2 unverifiable |
| #251 | **approved, merged** | fully self-contained, every step reconstructed |
| #257 | **approved, merged** | Theorem 1 + counterexample both reconstructed; honest refutation |
| #238, #242, #249, #253, #255 | not reviewed | budget |

Depth over breadth, per the brief. I read #253 far enough to check its Hall
arithmetic — `e_1 <= b_2` does follow from the two `tau` cut inequalities, via
`min(a_0^2,a_1^2) + max(a_0^1,a_1^1) >= 3` — but not far enough to sign off on
its terminal-preserving augmentation, which is the load-bearing and self-flagged
risk point. Left unreviewed rather than half-approved.

## The chain does not reach a `tau=3` theorem

Worth stating plainly, because the individual abstracts read as if it does.
#251 refutes #249's boundary-core method. #257 refutes #255's local existence
hypothesis. The chain self-corrects twice in ten PRs, which is healthy — but
the net position after all ten is a set of correct local packing theorems plus
two documented dead ends, not a proved special case. Per §0 that is a success
and should be reported as one; it should not be reported as "closing the
`tau=3` regime".

## Protocol notes

- **Codex is far over the §1 six-PR awaiting-review cap** — ~44 open PRs at
  review time, of which these ten are one afternoon's output. Not mine to fix;
  recording it.
- **None of the ten carries a `tier:` label.** §1 requires exactly one of
  `tier:verification-critical` / `tier:non-claim` on every PR.
- Merging out of order leaves files on `main` citing unmerged PRs by number
  (#251 → #239/#246/#249; #257 → #255). Harmless to the math, bad for a later
  reader. Flagged on both.

## For next time

The cheap fix that would unblock most of this chain is not more mathematics —
it is landing one self-contained definitions file for "separator sum",
"relevant / optional / forced trace" that the corollaries can point at. Until
that exists on `main`, every `tau=3` corollary in this line of work is
unreviewable by construction, and the theorems underneath them — which are
good — cannot get credit for it.
